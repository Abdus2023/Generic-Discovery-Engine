#!/usr/bin/env node
/*
 * ============================================================================
 * Generic Discovery Engine — static verification
 * ============================================================================
 *
 * Checks documentation claims against the prototype artifact using static
 * analysis only (Node built-ins; no dependencies).
 *
 * Usage:
 *   node tools/verify.mjs
 *
 * Exit codes:
 *   0  every check passed
 *   1  at least one check FAILED  (documentation or code drifted)
 *
 * Check kinds:
 *   [PASS]         claim holds in the artifact
 *   [FAIL]         claim does not hold  -> drift between docs and code
 *   [DEFECT]       known, documented defect (see docs/prototype/limitations.md)
 *   [INFO]         informational observation
 *
 * The distinction matters: [DEFECT] entries are *known* properties of the
 * shipped prototype and are documented as such; they do not fail the build.
 * A check that turns [PASS] -> [FAIL] means documentation and code disagree.
 */

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARTIFACT = path.join(ROOT, 'prototype', 'generic-discovery-engine.user.js');

const results = [];
const pass = (name, note = '') => results.push({ level: 'PASS', name, note });
const fail = (name, note = '') => results.push({ level: 'FAIL', name, note });
const defect = (name, note = '') => results.push({ level: 'DEFECT', name, note });
const info = (name, note = '') => results.push({ level: 'INFO', name, note });

const source = fs.readFileSync(ARTIFACT, 'utf8');

/** Return the body of a class declaration by name. */
function classBody(name) {
  const start = source.indexOf(`class ${name} `);
  if (start < 0) return null;
  // next top-level class starts at a lower indentation
  const rest = source.slice(start + 1);
  const next = rest.search(/\n\s{0,8}class\s+\w+/);
  return next < 0 ? rest : rest.slice(0, next);
}

function methodBody(className, methodName) {
  const body = classBody(className);
  if (!body) return null;
  const re = new RegExp(`\\n\\s*(?:async\\s+)?${methodName}\\s*\\([^)]*\\)\\s*\\{`);
  const m = body.match(re);
  if (!m) return null;
  const from = m.index + m[0].length;
  let depth = 1, i = from;
  while (i < body.length && depth > 0) {
    if (body[i] === '{') depth++;
    else if (body[i] === '}') depth--;
    i++;
  }
  return body.slice(from, i - 1);
}

/* -------------------------------------------------------------------------- */
/* 1. Artifact integrity                                                      */
/* -------------------------------------------------------------------------- */

try {
  new vm.Script(source, { filename: 'generic-discovery-engine.user.js' });
  pass('artifact parses as JavaScript', 'node vm.Script');
} catch (error) {
  fail('artifact parses as JavaScript', String(error.message));
}

const version = (source.match(/@version\s+([0-9.]+)/) || [])[1];
info('artifact version', version || 'unknown');

/* -------------------------------------------------------------------------- */
/* 2. Candidate claiming invariant (code level)                               */
/* -------------------------------------------------------------------------- */

const claim = methodBody('KnowledgeBase', 'claimNextCandidate');
if (!claim) fail('claimNextCandidate() exists', 'method not found');
else {
  if (!/\bawait\b/.test(claim)) pass('claimNextCandidate() is synchronous', 'no await inside the method');
  else fail('claimNextCandidate() is synchronous', 'await found inside the claim operation');

  const marksClaimed = /status\s*=\s*'claimed'/.test(claim);
  const returnsAfterMarking = claim.indexOf("status = 'claimed'") < claim.lastIndexOf('return');
  if (marksClaimed && returnsAfterMarking) pass('claim marks ownership before returning');
  else fail('claim marks ownership before returning');

  const eligible = claim.includes("candidate.status !== 'queued'") && claim.includes("candidate.status !== 'failed'");
  if (eligible) info('claim eligibility', "statuses 'queued' and 'failed'");
  else fail('claim eligibility filter unchanged', 'expected queued/failed filter');
}

const worker = methodBody('GenericDiscoveryEngine', 'worker');
if (!worker) fail('worker() exists');
else {
  const claimAt = worker.indexOf('claimNextCandidate');
  if (claimAt < 0) fail('worker() calls claimNextCandidate()');
  else {
    const boundary = worker.slice(0, claimAt);
    const awaitedClaim = /await\s+this\.db\.claimNextCandidate/.test(worker);
    if (!awaitedClaim) pass('worker() claims without awaiting a shared resource');
    else fail('worker() claims without awaiting a shared resource', 'claim is awaited');

    const afterClaim = worker.slice(claimAt);
    const nextAwait = afterClaim.search(/\bawait\b/);
    const between = nextAwait < 0 ? afterClaim : afterClaim.slice(0, nextAwait);
    if (/executePlan|markSkipped/.test(between)) {
      pass('ownership is handed straight to execution after the claim',
        'no await between claim and executePlan/markSkipped');
    } else {
      fail('ownership is handed straight to execution after the claim',
        'unexpected work between claim and first await');
    }
    void boundary;
  }
}

/* -------------------------------------------------------------------------- */
/* 3. Re-queue path (known defect)                                            */
/* -------------------------------------------------------------------------- */

const queue = methodBody('KnowledgeBase', 'queueCandidate');
if (!queue) fail('queueCandidate() exists');
else {
  const refusesOnlyTerminal = queue.includes("'completed'") && queue.includes("'skipped'")
    && !/'claimed'|'acquiring'|'planned'|'observed'/.test(queue);
  if (refusesOnlyTerminal) {
    defect('queueCandidate() re-queues in-flight candidates',
      'only completed/skipped are refused -> re-discovery can give a candidate a second owner');
  } else {
    pass('queueCandidate() refuses non-terminal statuses',
      'in-flight candidates can no longer be re-queued');
  }
}

const addCandidate = methodBody('KnowledgeBase', 'addCandidate');
if (addCandidate && /return existing;/.test(addCandidate)) {
  info('addCandidate() deduplicates by identity key and returns the existing object',
    'callers must therefore decide whether re-queueing is safe');
}

/* -------------------------------------------------------------------------- */
/* 4. Failure handling (known defect)                                         */
/* -------------------------------------------------------------------------- */

const markFailed = methodBody('KnowledgeBase', 'markFailed');
if (markFailed && !/nextAttemptAt/.test(markFailed)) {
  defect("markFailed() sets no backoff and 'failed' stays claimable",
    'terminal failure can be re-claimed immediately, consuming the request budget');
} else if (markFailed) {
  pass('markFailed() applies a terminal state');
}

/* -------------------------------------------------------------------------- */
/* 4b. Evidence collected but unused, and reporting gaps                      */
/* -------------------------------------------------------------------------- */

{
  const writes = (source.match(/fingerprintIndex\.(has|set|get)/g) || []);
  const reads = (source.match(/fingerprintIndex\.get\(/g) || []);
  if (writes.length > 0 && reads.length === 0) {
    defect('content fingerprints are indexed but never used',
      `${writes.length} write/probe sites, 0 read sites -> content identity cannot affect any decision (D8)`);
  } else if (reads.length > 0) {
    pass('content fingerprint index is consulted', `${reads.length} read site(s)`);
  } else {
    info('content fingerprint index', 'not present');
  }
}

{
  const writtenAcquired = /stats\.acquired\s*(\+\+|\+=|=)/.test(source)
    || /\.acquired\s*\+\+/.test(source);
  if (!writtenAcquired) {
    defect('stats.acquired is never incremented', 'the counter stays 0 in the UI and in exports (D7)');
  } else {
    pass('stats.acquired is maintained');
  }
}

{
  const restoreBody = methodBody('GenericDiscoveryEngine', 'restore') || '';
  if (/this\.ledger\.restore\(/.test(restoreBody)) pass('the decision ledger survives a restore');
  else fail('the decision ledger survives a restore', 'restore() does not call ledger.restore()');

  if (/this\.requestsReserved\s*=\s*0/.test(restoreBody)) {
    info('request budget semantics on restore', 'a new execution context gets a fresh budget (by design)');
  }
}

/* -------------------------------------------------------------------------- */
/* 5. Provider boundary                                                       */
/* -------------------------------------------------------------------------- */

const providerNames = [
  'HtmlProvider', 'JsonProvider', 'XmlProvider', 'CssProvider',
  'JavaScriptProvider', 'TextProvider', 'BinaryProvider'
];

const missing = providerNames.filter(name => {
  const body = classBody(name);
  return !body || !/matches\s*\(/.test(body) || !/recognize\s*\(/.test(body);
});
if (missing.length === 0) pass('every provider implements matches() and recognize()', providerNames.join(', '));
else fail('every provider implements matches() and recognize()', `missing: ${missing.join(', ')}`);

const registry = classBody('ProviderRegistry') || '';
const notRegistered = providerNames.filter(n => !registry.includes(`new ${n}(`));
if (notRegistered.length === 0) pass('every provider is registered', providerNames.length + ' providers');
else fail('every provider is registered', notRegistered.join(', '));

{
  const textBody = classBody('TextProvider') || '';
  if (/type\.startsWith\(.text\/.\)/.test(textBody) && /type === ''/.test(textBody)) {
    pass('TextProvider scope is documented', "matches text/* or an empty content type; not a universal fallback");
  } else {
    fail('TextProvider scope is documented', 'matching rule changed; update docs/architecture/provider-model.md');
  }
}

const ioInProviders = providerNames.filter(n => /GM_xmlhttpRequest|\bfetch\s*\(|XMLHttpRequest/.test(classBody(n) || ''));
if (ioInProviders.length === 0) pass('providers perform no network I/O');
else fail('providers perform no network I/O', ioInProviders.join(', '));

if (!/candidates\s*\(/.test(classBody('Provider') || '')) {
  info('provider contract', 'matches() + recognize(); candidate expansion is owned by the engine');
}

const ioClasses = ['Acquisition', 'NetworkObserver'].filter(n => /GM_xmlhttpRequest/.test(classBody(n) || ''));
if (ioClasses.length > 0) pass('network execution is confined to acquisition', ioClasses.join(', '));
else info('network execution location', 'GM_xmlhttpRequest not found in Acquisition/NetworkObserver');

/* -------------------------------------------------------------------------- */
/* 6. Provenance chain                                                        */
/* -------------------------------------------------------------------------- */

const discovery = classBody('Discovery') || '';
const hasChain = ['candidateId', 'observationId', 'provenance'].every(f => discovery.includes(f));
if (hasChain) pass('Discovery links candidate + observation + provenance');
else fail('Discovery links candidate + observation + provenance');

const candidate = classBody('Candidate') || '';
if (/\bparent\b/.test(candidate)) pass('Candidate records its parent');
else fail('Candidate records its parent');

if (/recordCandidateDiscovered/.test(classBody('DecisionLedger') || '')) {
  pass('discovery events are recorded in the ledger');
} else fail('discovery events are recorded in the ledger');

/* -------------------------------------------------------------------------- */
/* 7. Scope claims: what the prototype must NOT contain                       */
/* -------------------------------------------------------------------------- */

const DVB_SYMBOLS = [
  'symbolRate', 'symbol_rate', 'demodulat', 'PSI/SI', 'transportStream',
  'transport_stream', 'tuner', '\\bSDR\\b', 'frontend', 'constellation',
  '\\bFEC\\b', 'dvb[-_]?s\\d?\\b', 'dvb[-_]?t\\d?\\b', 'dvb[-_]?c\\b'
];
const dvbHits = DVB_SYMBOLS.filter(sym => new RegExp(sym, 'i').test(source));
if (dvbHits.length === 0) pass('no DVB/RF implementation symbols', 'analogy only, no physical layer');
else fail('no DVB/RF implementation symbols', dvbHits.join(', '));

const FUTURE_SYMBOLS = [
  'EvidenceGraph', 'LeaseManager', 'WorkItem', 'DiscoveryDomain', 'ScanSession',
  'CoverageClaim', 'CompletenessClaim', 'FencingToken', 'ConflictResolver',
  'QueryPlanner', 'TacticRuntime', 'CapabilityLattice'
];
const futureHits = FUTURE_SYMBOLS.filter(sym => new RegExp(`\\b${sym}\\b`).test(source));
if (futureHits.length === 0) pass('no later-design layers present', 'v0.8+ architecture is not implemented');
else fail('no later-design layers present', futureHits.join(', '));

/* -------------------------------------------------------------------------- */
/* 7b. Evidence traceability                                                  */
/* -------------------------------------------------------------------------- */

{
  const registerPath = path.join(ROOT, 'docs', 'analysis', 'evidence-register.md');
  if (!fs.existsSync(registerPath)) {
    fail('evidence register exists', 'docs/analysis/evidence-register.md missing');
  } else {
    const register = fs.readFileSync(registerPath, 'utf8');

    // every "| ID |" row in the register tables
    const defined = new Set(
      [...register.matchAll(/^\|\s*((?:CODE|TEST|DOC|CFG|HIST|ARCH|SCOPE|CONC|PROV|FAIL)-\d{3})\s*\|/gm)]
        .map(m => m[1])
    );

    if (defined.size === 0) fail('evidence register defines IDs', 'no ID rows found');
    else info('evidence IDs defined', `${defined.size} ids`);

    // every citation in every markdown document
    const cited = new Map();
    const mdFiles = [];
    const walk = (dir) => {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (entry.name !== '.git') walk(full);
        } else if (entry.name.endsWith('.md')) mdFiles.push(full);
      }
    };
    walk(ROOT);

    for (const file of mdFiles) {
      const text = fs.readFileSync(file, 'utf8');
      for (const m of text.matchAll(/\[EVID:([A-Z0-9-]+)\]/g)) {
        if (!cited.has(m[1])) cited.set(m[1], path.relative(ROOT, file));
      }
    }

    const dangling = [...cited.keys()].filter(id => !defined.has(id));
    if (dangling.length === 0) {
      pass('every [EVID:…] citation resolves to the register',
        `${cited.size} distinct ids cited across ${mdFiles.length} documents`);
    } else {
      fail('every [EVID:…] citation resolves to the register', dangling.join(', '));
    }

    // register rows that point at repository paths must point at real files
    const missingPaths = [];
    for (const m of register.matchAll(/^\|\s*(?:CODE|CFG|TEST|DOC)-\d{3}\s*\|\s*`([^`]+)`/gm)) {
      const target = m[1];
      if (/^[a-z-]+(\.md)?$/.test(target) && target.endsWith('.md')) {
        if (!fs.existsSync(path.join(ROOT, target))) missingPaths.push(target);
      }
      if (target.includes('/') && !fs.existsSync(path.join(ROOT, target))) missingPaths.push(target);
    }
    if (missingPaths.length === 0) pass('evidence register paths exist');
    else fail('evidence register paths exist', [...new Set(missingPaths)].join(', '));

    // the register must state the access classification
    if (/Access classification\s*\|[^|]*FULL ACCESS/.test(register)) {
      pass('repository access is recorded in the register');
    } else {
      fail('repository access is recorded in the register');
    }

    // negative-evidence claims must be labelled
    const absenceLines = register.split('\n').filter(l => /ABSENCE_VERIFIED|NOT_FOUND/.test(l));
    if (absenceLines.length > 0) info('negative-evidence claims recorded', `${absenceLines.length} row(s)`);
    else fail('negative-evidence claims recorded');
  }
}

/* -------------------------------------------------------------------------- */
/* 7c. Governance: frozen code, canonical record, authorization               */
/* -------------------------------------------------------------------------- */

{
  const crypto = await import('node:crypto');
  const digest = crypto.createHash('sha256').update(source).digest('hex');
  const FROZEN = '8f5fc5c50e7f0886aa76fdbc7a6a633b3c4de72e7eb8b2d62525b807e354c474';

  const registerText = fs.readFileSync(
    path.join(ROOT, 'docs', 'analysis', 'evidence-register.md'), 'utf8');

  if (!registerText.includes(FROZEN)) {
    fail('evidence register pins the artifact digest', 'digest not recorded');
  } else if (digest === FROZEN) {
    pass('source artifact is unchanged since the recorded revision',
      `sha256 ${digest.slice(0, 12)}… (code changes were out of authorized scope)`);
  } else {
    fail('source artifact is unchanged since the recorded revision',
      `digest ${digest} differs from the recorded ${FROZEN} — update the register and the change register together`);
  }
}

{
  /* The normative record exists and is machine-validatable. The full schema,
     enum and authorization checks live in tools/validate-analysis.mjs; here we
     assert only that it is present and internally consistent. */
  const recordPath = path.join(ROOT, 'docs', 'analysis', 'analysis.json');
  if (!fs.existsSync(recordPath)) {
    fail('canonical analysis record exists', 'docs/analysis/analysis.json missing');
  } else {
    const record = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
    const fiveFields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result'];
    const missing = [];
    for (const claim of record.claims) {
      for (const field of fiveFields) if (!(field in claim)) missing.push(`${claim.id}.${field}`);
    }
    if (missing.length === 0) {
      pass('every claim record carries all five typed fields',
        `${record.claims.length} records`);
    } else {
      fail('every claim record carries all five typed fields', missing.slice(0, 6).join(', '));
    }

    const collapsed = record.claims.filter(c => ['IMPLEMENTED', 'TESTED', 'DOCUMENTED', 'MISSING', 'TRUE', 'FALSE']
      .includes(c.verification_result));
    if (collapsed.length === 0) pass('verification_result never carries a non-verification value');
    else fail('verification_result never carries a non-verification value', collapsed.map(c => c.id).join(', '));

    const exec = record.execution.result;
    if (['NOT_EXECUTED', 'SUCCEEDED', 'PARTIALLY_SUCCEEDED', 'FAILED', 'STOPPED'].includes(exec)) {
      pass('execution.result uses the execution enum', `${exec}, ${record.execution.executed_changes.length} executed change(s)`);
    } else {
      fail('execution.result uses the execution enum', String(exec));
    }

    if (record.authorization.forbidden_operations.includes('MODIFY_SOURCE_CODE')) {
      pass('authorization forbids source mutation', 'code changes are plan-only');
    } else {
      fail('authorization forbids source mutation', 'unexpected: source mutation appears authorized');
    }
  }
}

/* -------------------------------------------------------------------------- */
/* 7d. No document collapses the status dimensions                            */
/* -------------------------------------------------------------------------- */

{
  const behaviourDocs = [
    ...['discovery-model.md', 'candidate-model.md', 'scheduler.md', 'provider-model.md',
        'provenance.md', 'concurrency.md', 'search-space.md']
      .map(f => path.join('docs', 'architecture', f)),
    ...['userscript.md', 'scope.md', 'limitations.md'].map(f => path.join('docs', 'prototype', f)),
    ...['dvb-blind-scan-inspiration.md'].map(f => path.join('docs', 'research', f)),
    ...['future-architecture.md'].map(f => path.join('docs', 'roadmap', f))
  ];

  const undeclared = [];
  for (const rel of behaviourDocs) {
    const full = path.join(ROOT, rel);
    if (!fs.existsSync(full)) { undeclared.push(`${rel} (missing)`); continue; }
    const text = fs.readFileSync(full, 'utf8');
    if (!/claim_kind/.test(text) || !/verification_result/.test(text)) undeclared.push(rel);
  }
  if (undeclared.length === 0) {
    pass('every behaviour document declares its typed status fields', `${behaviourDocs.length} documents`);
  } else {
    fail('every behaviour document declares its typed status fields', undeclared.join(', '));
  }

  // collapsed verdicts must not appear as a bare status label
  const offenders = [];
  for (const rel of behaviourDocs) {
    const full = path.join(ROOT, rel);
    if (!fs.existsSync(full)) continue;
    const text = fs.readFileSync(full, 'utf8');
    if (/^Status:\s*\**(IMPLEMENTED|TESTED)\**/m.test(text)) offenders.push(rel);
  }
  if (offenders.length === 0) pass('no document uses a collapsed status label');
  else fail('no document uses a collapsed status label', offenders.join(', '));

  // the five fields must not be substituted for one another
  const substitution = [];
  for (const rel of behaviourDocs) {
    const full = path.join(ROOT, rel);
    if (!fs.existsSync(full)) continue;
    const text = fs.readFileSync(full, 'utf8');
    if (/claim_kind:\s*(DIRECT|CORROBORATED|INDIRECT|ABSENT|INACCESSIBLE)/.test(text)) {
      substitution.push(`${rel} (claim_kind holds an evidence level)`);
    }
    if (/evidence_level:\s*(IMPLEMENTED|PARTIAL|NOT_IMPLEMENTED)/.test(text)) {
      substitution.push(`${rel} (evidence_level holds an implementation state)`);
    }
  }
  if (substitution.length === 0) pass('typed status fields are not substituted for one another');
  else fail('typed status fields are not substituted for one another', substitution.join(', '));
}

/* -------------------------------------------------------------------------- */
/* 8. Documentation integrity                                                 */
/* -------------------------------------------------------------------------- */

const docs = [];
for (const dir of ['docs', 'tools', 'prototype', 'archive']) {
  const walk = (d) => {
    for (const entry of fs.readdirSync(d, { withFileTypes: true })) {
      const full = path.join(d, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith('.md')) docs.push(full);
    }
  };
  walk(path.join(ROOT, dir));
}
docs.push(path.join(ROOT, 'README.md'));

let broken = [];
for (const file of docs) {
  if (!fs.existsSync(file)) continue;
  const text = fs.readFileSync(file, 'utf8');
  for (const m of text.matchAll(/\]\(([^)#\s]+\.(?:md|js|mjs|user\.js))\)/g)) {
    const target = path.resolve(path.dirname(file), m[1]);
    if (!fs.existsSync(target)) broken.push(`${path.relative(ROOT, file)} -> ${m[1]}`);
  }
}
if (broken.length === 0) pass('every relative documentation link resolves', docs.length + ' documents');
else fail('every relative documentation link resolves', broken.join('; '));

/* README must not describe designed-only layers as implemented.
 * Terms that are legitimate in a scope/non-goal/roadmap context must not appear
 * in the sections that describe what exists today.                              */

const readme = fs.readFileSync(path.join(ROOT, 'README.md'), 'utf8');

/**
 * Return the text of one '## ' section, stopping at the next '## ' heading.
 * Robust to heading renames: it never swallows the rest of the document.
 */
function section(md, startHeading) {
  const lines = md.split('\n');
  const start = lines.findIndex(l => l.trim() === startHeading);
  if (start < 0) return '';
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) {
    if (/^## \S/.test(lines[i])) { end = i; break; }
  }
  return lines.slice(start, end).join('\n');
}

const implementedText = [
  section(readme, '## Current Prototype'),
  section(readme, '## Core Architecture'),
  section(readme, '## Discovery Loop'),
  section(readme, '## Candidate Lifecycle'),
  section(readme, '## Concurrency Invariant'),
  section(readme, '## Provider Model'),
  section(readme, '## Provenance'),
  // the "Implemented" paragraph inside Scope
  (readme.match(/\*\*Implemented\*\*[\s\S]*?\n\n/) || [''])[0]
].join('\n');

const DESIGN_ONLY_TERMS = ['lease', 'fencing', 'evidence graph', 'coverage claim',
  'completeness of the open web', 'capability lattice', 'work item'];

const leaked = DESIGN_ONLY_TERMS.filter(t => new RegExp(t, 'i').test(implementedText));
if (leaked.length === 0) pass('README does not claim unimplemented layers in implemented sections');
else fail('README does not claim unimplemented layers in implemented sections', leaked.join(', '));

if (/\*\*Not implemented\*\*|## Non-Goals/.test(readme) && /DESIGNED|design only/i.test(readme)) {
  pass('README labels designed-only material and states non-implementations');
} else {
  fail('README labels designed-only material and states non-implementations');
}

/* -------------------------------------------------------------------------- */
/* Report                                                                     */
/* -------------------------------------------------------------------------- */

const width = Math.max(...results.map(r => r.name.length));
console.log(`verifying ${path.relative(ROOT, ARTIFACT)} (v${version})\n`);
for (const r of results) {
  console.log(`[${r.level}] ${r.name.padEnd(width)}  ${r.note}`);
}
const failures = results.filter(r => r.level === 'FAIL').length;
const defects = results.filter(r => r.level === 'DEFECT').length;
console.log(`\n${results.filter(r => r.level === 'PASS').length} passed, ${failures} failed, ${defects} known defect(s)`);
process.exit(failures === 0 ? 0 : 1);
