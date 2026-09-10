#!/usr/bin/env node
/*
 * Render the human-readable claim tables in docs/analysis/claims.md from the
 * normative record docs/analysis/analysis.json.
 *
 * Usage:
 *   node tools/render-claims.mjs          # rewrite the generated block
 *   node tools/render-claims.mjs --check  # fail if the block is stale
 *
 * Only the region between the CLAIMS:BEGIN / CLAIMS:END markers is generated.
 * Prose around it is authored by hand and is never touched.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const JSON_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.json');
const MD_PATH = path.join(ROOT, 'docs', 'analysis', 'claims.md');

const BEGIN = '<!-- CLAIMS:BEGIN (generated from analysis.json — do not edit by hand) -->';
const END = '<!-- CLAIMS:END -->';

const GROUPS = [
  ['current-system', 'Current-system claims'],
  ['architecture-boundary', 'Architecture-boundary claims'],
  ['scope-and-absence', 'Scope and absence claims'],
  ['plan-history-hypothesis', 'Plan, history and hypothesis claims']
];

const record = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
const claims = record.claims;

function cell(text) {
  return String(text).replace(/\|/g, '\\|').replace(/\n+/g, ' ');
}

function renderGroups() {
  const out = [];
  for (const [key, title] of GROUPS) {
    const rows = claims.filter(c => c.group === key);
    if (rows.length === 0) continue;
    out.push(`### ${title}`);
    out.push('');
    out.push('| Claim ID | Statement | claim_kind | implementation_state | test_state | evidence_level | verification_result | Evidence | Interpretation |');
    out.push('| --- | --- | --- | --- | --- | --- | --- | --- | --- |');
    for (const c of rows) {
      const evidence = c.evidence.map(e => `[EVID:${typeof e === 'string' ? e : e.id}]`).join(' ');
      const marker = c.verification_result === 'CONTRADICTED' ? '**CONTRADICTED**' : c.verification_result;
      out.push(`| \`${c.id}\` | ${cell(c.statement)} | \`${c.claim_kind}\` | \`${c.implementation_state}\` | \`${c.test_state}\` | \`${c.evidence_level}\` | \`${marker}\` | ${evidence} | ${cell(c.interpretation)} |`);
    }
    out.push('');
  }
  return out.join('\n').trimEnd();
}

const block = `${BEGIN}\n\n${renderGroups()}\n\n${END}`;
const md = fs.readFileSync(MD_PATH, 'utf8');

const start = md.indexOf(BEGIN);
const end = md.indexOf(END);
if (start < 0 || end < 0) {
  console.error(`FAIL: markers not found in ${path.relative(ROOT, MD_PATH)}`);
  process.exit(2);
}

const updated = md.slice(0, start) + block + md.slice(end + END.length);

if (process.argv.includes('--check')) {
  if (updated !== md) {
    console.error('FAIL: claims.md tables are stale — run node tools/render-claims.mjs');
    process.exit(1);
  }
  console.log(`claims.md is up to date (${claims.length} claim records)`);
  process.exit(0);
}

fs.writeFileSync(MD_PATH, updated);
console.log(`rendered ${claims.length} claim records into ${path.relative(ROOT, MD_PATH)}`);
