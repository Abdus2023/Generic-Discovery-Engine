#!/usr/bin/env node
/*
 * ============================================================================
 * Verification-run recorder
 * ============================================================================
 *
 * Brief 11 requires that every verification run is recorded, with the phase it
 * failed in and every error, in a consistent structure that allows tracking
 * across runs — and that the validator itself never mutates the repository
 * (section 241). The two requirements are why this program exists separately
 * from the validator:
 *
 *   tools/validate-analysis.mjs   a pure function of document + registries,
 *                                 prints a report and exits non-zero when invalid
 *   tools/validation-run.mjs      runs the validator, hashes the tree before and
 *                                 after, and appends one entry to
 *                                 docs/analysis/validation-runs.json
 *
 * The only file this program writes is the run store, and that file is excluded
 * from the digest it compares — so "verification modified nothing" is a
 * measurement rather than an assurance (EVV-008).
 *
 * Usage:
 *   node tools/validation-run.mjs                                  # current working tree
 *   node tools/validation-run.mjs --label "after registry split"
 *   node tools/validation-run.mjs --revision <rev>                 # an archived revision's inputs
 *   node tools/validation-run.mjs --json                           # print the entry
 *
 * Entries are append-only: an existing id is never rewritten.
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const STORE_PATH = path.join(REPO_ROOT, 'docs', 'analysis', 'validation-runs.json');
const VALIDATOR = path.join(REPO_ROOT, 'tools', 'validate-analysis.mjs');

const argv = process.argv.slice(2);
const option = (name, fallback = null) => {
  const index = argv.indexOf(name);
  return index > -1 && argv[index + 1] && !argv[index + 1].startsWith('--') ? argv[index + 1] : fallback;
};
const flag = name => argv.includes(name);

/* The store is the recorder's own output, so it is the one path excluded from
   the tree digest; snapshots report their own digests. */
const EXCLUDED_FROM_DIGEST = ['docs/analysis/validation-runs.json'];

function manifest(root) {
  const files = [];
  const skip = new Set(['.git', 'node_modules', ...EXCLUDED_FROM_DIGEST]);
  const walk = dir => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      const rel = path.relative(root, full).split(path.sep).join('/');
      if (skip.has(rel) || entry.name === '.git') continue;
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile()) files.push([rel, crypto.createHash('sha256').update(fs.readFileSync(full)).digest('hex')]);
    }
  };
  walk(root);
  files.sort((a, b) => (a[0] < b[0] ? -1 : 1));
  return files;
}

function treeDigest(root) {
  const files = manifest(root);
  const digest = crypto.createHash('sha256').update(files.map(([p, h]) => `${p} ${h}`).join('\n')).digest('hex');
  return { digest, files: files.length };
}

function run(command, args, cwd) {
  try {
    const output = execFileSync(command, args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return { ok: true, output };
  } catch (error) {
    return { ok: false, output: String(error.stdout || error.message), error: String(error.stderr || '') };
  }
}

/* The HEAD revision at the moment of the run: for a worktree run this is what
   the inputs were read from, for a snapshot run the revision that was archived. */
function headRevision() {
  try {
    return execFileSync('git', ['rev-parse', 'HEAD'], { cwd: REPO_ROOT, encoding: 'utf8' }).trim();
  } catch {
    return null;
  }
}

function snapshot(revision) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'gde-run-'));
  const archive = execFileSync('git', ['archive', '--format=tar', revision], { cwd: REPO_ROOT, maxBuffer: 1 << 28 });
  execFileSync('tar', ['-x', '-C', dir], { input: archive, maxBuffer: 1 << 28 });
  const resolved = execFileSync('git', ['rev-parse', revision], { cwd: REPO_ROOT, encoding: 'utf8' }).trim();
  return { dir, resolved };
}

function readStore() {
  if (!fs.existsSync(STORE_PATH)) {
    return {
      schema_version: '1.0',
      $comment: 'Append-only ledger of verification runs (brief 11 sections 241-242). tools/validation-run.mjs writes it; tools/validate-analysis.mjs never writes anything. Each entry binds a verdict to the digests of the document, the schema, the registries and the tool that produced it, so a run can be checked later without re-running it.',
      runs: [],
    };
  }
  return JSON.parse(fs.readFileSync(STORE_PATH, 'utf8'));
}

function nextId(store) {
  const highest = store.runs.reduce((max, entry) => Math.max(max, Number(String(entry.id).replace(/\D/g, '')) || 0), 0);
  return `RUN-${String(highest + 1).padStart(3, '0')}`;
}

function phasesOf(json) {
  return (json.phases || []).map(p => ({ phase: p.phase, state: p.state, checks: p.checks, errors: p.errors }));
}

function main() {
  const revision = option('--revision');
  const label = option('--label') || (revision ? `archived inputs at ${revision}` : 'current working tree');
  const startedAt = new Date().toISOString();

  let root = REPO_ROOT;
  let mode = 'WORKTREE';
  let resolved = null;
  let scratch = null;

  if (revision) {
    const snap = snapshot(revision);
    root = snap.dir;
    resolved = snap.resolved;
    scratch = snap.dir;
    mode = 'SNAPSHOT';
  }

  const before = treeDigest(root);
  const args = ['--json'];
  if (root !== REPO_ROOT) args.push('--root', root);
  const result = run(process.execPath, [VALIDATOR, ...args], REPO_ROOT);
  const after = treeDigest(root);
  if (scratch) fs.rmSync(scratch, { recursive: true, force: true });

  let payload = null;
  try {
    payload = JSON.parse(result.output);
  } catch {
    payload = null;
  }

  const entry = {
    id: nextId(readStore()),
    label,
    mode,
    ...(resolved ? { revision: resolved } : {}),
    head: resolved || headRevision(),
    started_at: startedAt,
    completed_at: new Date().toISOString(),
    verdict: payload ? payload.verdict : 'UNREADABLE',
    tool: payload
      ? payload.validator
      : { path: 'tools/validate-analysis.mjs', sha256: crypto.createHash('sha256').update(fs.readFileSync(VALIDATOR)).digest('hex') },
    inputs: payload ? payload.inputs : {},
    phases: payload ? phasesOf(payload) : [],
    errors: payload ? payload.errors : [{ code: 'RUN-000', phase: 'STRUCTURAL', object: 'validator', message: 'the validator produced no JSON report' }],
    repository: {
      scope: mode === 'WORKTREE' ? 'worktree' : 'snapshot',
      tree_digest_before: before.digest,
      tree_digest_after: after.digest,
      files: before.files,
      unchanged: before.digest === after.digest,
      excluded_from_digest: EXCLUDED_FROM_DIGEST,
    },
  };

  const store = readStore();
  if (store.runs.some(r => r.id === entry.id)) {
    console.error(`refusing to rewrite run ${entry.id}: the ledger is append-only`);
    process.exit(2);
  }
  store.runs.push(entry);
  fs.writeFileSync(STORE_PATH, `${JSON.stringify(store, null, 2)}\n`);

  if (flag('--json')) {
    console.log(JSON.stringify(entry, null, 2));
  } else {
    console.log(`${entry.id}  ${entry.verdict.padEnd(9)} ${entry.mode.padEnd(24)} ${label}`);
    for (const phase of entry.phases) {
      if (phase.errors > 0) console.log(`   ${phase.phase.padEnd(14)} FAILED  ${phase.errors} error(s)`);
    }
    if (entry.errors.length) {
      console.log(`   ${entry.errors.length} error(s):`);
      for (const error of entry.errors) console.log(`     ${error.phase} · ${error.code} · ${error.object} — ${error.message.slice(0, 120)}`);
    }
    console.log(`   tree ${entry.repository.unchanged ? 'unchanged' : 'CHANGED'} (${before.files} files, ${before.digest.slice(0, 12)} → ${after.digest.slice(0, 12)})`);
    console.log(`   recorded in ${path.relative(REPO_ROOT, STORE_PATH)}`);
  }
  process.exit(entry.verdict === 'VALID' ? 0 : 1);
}

main();
