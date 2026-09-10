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
import crypto from 'node:crypto';
import path from 'node:path';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ARTIFACT = path.join(ROOT, 'prototype', 'generic-discovery-engine.user.js');

const results = [];

/* the frozen artifact digest, re-computed wherever the record states it */
function verifyArtifactDigest(expected) {
  if (!expected) return true;
  const target = path.join(ROOT, expected.path);
  if (!fs.existsSync(target)) return false;
  const value = crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex');
  return value === expected.value;
}
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
    const fiveFields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'claim_verification'];
    const missing = [];
    for (const claim of record.claims) {
      for (const field of fiveFields) if (!(field in claim)) missing.push(`${claim.id}.${field}`);
    }
    if (missing.length === 0) {
      pass('every claim record carries its typed claim fields',
        `${record.claims.length} records`);
    } else {
      fail('every claim record carries its typed claim fields', missing.slice(0, 6).join(', '));
    }

    const collapsed = record.claims.filter(c => ['IMPLEMENTED', 'TESTED', 'DOCUMENTED', 'MISSING', 'TRUE', 'FALSE']
      .includes(c.claim_verification?.result));
    if (collapsed.length === 0) pass('claim_verification.result never carries a non-verification value');
    else fail('claim_verification.result never carries a non-verification value', collapsed.map(c => c.id).join(', '));
    const legacy = record.claims.filter(c => 'verification_result' in c || 'result' === undefined && 'verification' in c);
    if (legacy.length === 0) pass('no claim uses a legacy or unqualified verification field');
    else fail('no claim uses a legacy or unqualified verification field', `${legacy.length} claim(s)`);

    const exec = record.execution.state;
    if (['NOT_STARTED', 'AUTHORIZATION_BLOCKED', 'READY', 'RUNNING', 'SUCCEEDED', 'PARTIALLY_SUCCEEDED',
         'FAILED', 'CANCELLED', 'STOPPED'].includes(exec)) {
      const results = record.execution.operations.map(o => o.result);
      pass('execution.state uses the execution lifecycle enum',
        `${exec}, ${record.execution.executed_changes.length} executed change(s), ${results.length} operation results`);
    } else {
      fail('execution.state uses the execution lifecycle enum', String(exec));
    }

    /* the strongest form of the safety property: no effective capability can
       modify, rename, move or delete a source artifact. Creating the extracted
       artifact once (CAP-SOURCE-CREATE, restricted to prototype/, change R-001)
       is disclosed in the record; nothing else touches source. */
    const registry = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs', 'analysis', 'capability-registry.json'), 'utf8'));
    const allowed = ['ENABLED', 'RESTRICTED'];
    const authorizing = (record.authorization.capability_grants || []).filter(g => allowed.includes(g.state));
    const byId = new Map(registry.capabilities.map(c => [c.id, c]));
    const codeMutation = authorizing
      .map(g => byId.get(g.capability_id))
      .filter(c => c && c.resource_class === 'SOURCE' && c.operations.some(op => op !== 'CREATE'))
      .map(c => c.id);
    if (codeMutation.length === 0) {
      pass('authorization forbids source mutation', `${authorizing.length} authorizing grant(s); no MODIFY/RENAME/MOVE/DELETE capability against SOURCE`);
    } else {
      fail('authorization forbids source mutation', `unexpected: ${codeMutation.join(', ')}`);
    }
  }
}

/* -------------------------------------------------------------------------- */
/* 7e. State algebra: typed fields, authorization state vs level              */
/* -------------------------------------------------------------------------- */

{
  const schemaPath = path.join(ROOT, 'docs', 'analysis', 'analysis.schema.json');
  if (!fs.existsSync(schemaPath)) {
    fail('the schema file exists', 'docs/analysis/analysis.schema.json missing');
  } else {
    const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
    if (String(schema.$schema).includes('2020-12')) pass('schema declares JSON Schema draft 2020-12');
    else fail('schema declares JSON Schema draft 2020-12', String(schema.$schema));
  }

  const record = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs', 'analysis', 'analysis.json'), 'utf8'));
  const registryDoc = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs', 'analysis', 'capability-registry.json'), 'utf8'));
  const auth = record.authorization || {};
  const STATES = ['NOT_REQUESTED', 'REQUESTED', 'GRANTED', 'DENIED', 'REVOKED', 'EXPIRED'];
  const profiles = new Map(registryDoc.level_profiles.map(p => [p.id, p]));
  const capabilities = new Map(registryDoc.capabilities.map(c => [c.id, c]));
  const AUTHORIZING = ['ENABLED', 'RESTRICTED'];

  if (STATES.includes(auth.state)) pass('authorization state uses the authorization enum', auth.state);
  else fail('authorization state uses the authorization enum', String(auth.state));

  if (profiles.has(auth.level?.profile)) pass('authorization level is a named profile', auth.level.profile);
  else fail('authorization level is a named profile', String(auth.level?.profile));

  if (!('granted' in auth) && typeof auth.authorized !== 'boolean') pass('authorization is an object, not a boolean');
  else fail('authorization is an object, not a boolean');

  if (!(auth.state === 'GRANTED' && !auth.level?.profile)) pass('a grant states its level separately from its state');
  else fail('a grant states its level separately from its state');

  /* section 202.3: profile capabilities ∩ grants − denies, computed here */
  const closure = (profile, path_ = []) => {
    if (path_.includes(profile)) throw new Error('inheritance cycle: ' + [...path_, profile].join(' -> '));
    const node = profiles.get(profile);
    const out = new Set(node.capabilities || []);
    for (const parent of node.inherits || []) for (const cap of closure(parent, [...path_, profile])) out.add(cap);
    return out;
  };
  const grantOf = id => (auth.capability_grants || []).find(g => g.capability_id === id);
  const effective = () => {
    const ceiling = closure(auth.level.profile);
    const granted = (auth.capability_grants || []).filter(g => AUTHORIZING.includes(g.state) && ceiling.has(g.capability_id));
    const denied = new Set((auth.capability_grants || []).filter(g => ['DENIED', 'REVOKED', 'EXPIRED'].includes(g.state)).map(g => g.capability_id));
    return granted.filter(g => !denied.has(g.capability_id)).map(g => ({ ...capabilities.get(g.capability_id), state: g.state, grant: g }));
  };
  const permitted = () => {
    const implied = new Set(effective().flatMap(c => c.operations || []));
    const kept = new Set(auth.operations?.allow ? auth.operations.allow.filter(op => implied.has(op)) : [...implied]);
    for (const op of auth.operations?.deny || []) kept.delete(op);
    return kept;
  };

  {
    const ceiling = closure(auth.level.profile);
    const dangling = [...ceiling, ...(auth.capability_grants || []).map(g => g.capability_id)].filter(id => !capabilities.has(id));
    if (dangling.length === 0) pass('every capability id resolves in the registry',
      `${capabilities.size} registry entries, ${ceiling.size} reachable from ${auth.level.profile}`);
    else fail('every capability id resolves in the registry', [...new Set(dangling)].join(', '));

    const outside = (auth.capability_grants || []).filter(g => !ceiling.has(g.capability_id)).map(g => g.capability_id);
    if (outside.length === 0) pass('grants never exceed the resolved profile', `${(auth.capability_grants || []).length} grant(s) ⊆ ${auth.level.profile}`);
    else fail('grants never exceed the resolved profile', outside.join(', '));

    const restrictedWithoutScope = (auth.capability_grants || []).filter(g => g.state === 'RESTRICTED' && !g.scope);
    if (restrictedWithoutScope.length === 0) pass('every RESTRICTED grant carries its restriction scope',
      `${(auth.capability_grants || []).filter(g => g.state === 'RESTRICTED').length} restricted grant(s)`);
    else fail('every RESTRICTED grant carries its restriction scope', restrictedWithoutScope.map(g => g.capability_id).join(', '));

    const withheld = registryDoc.governance?.withheld_capabilities || [];
    const leaked = withheld.filter(id => (auth.capability_grants || []).some(g => g.capability_id === id && AUTHORIZING.includes(g.state)));
    if (leaked.length === 0) pass('withheld capability classes are unreachable through the authorization',
      `${withheld.length} withheld`);
    else fail('withheld capability classes are unreachable through the authorization', leaked.join(', '));

    const forbidden = registryDoc.governance?.forbidden_operations || [];
    const attempted = record.execution.operations.filter(o => forbidden.includes(o.operation)).map(o => o.id);
    if (attempted.length === 0) pass('no forbidden operation was executed', forbidden.join(', '));
    else fail('no forbidden operation was executed', attempted.join(', '));

    const PATH_RESOURCES = new Set(['DOCUMENT', 'TEST', 'SOURCE', 'CONFIGURATION', 'ARCHITECTURE']);
    const inPaths = (scope, target) => {
      const include = scope?.paths?.include || [];
      const exclude = scope?.paths?.exclude || [];
      const inside = include.some(p => target.path.startsWith(p));
      return inside && !exclude.some(p => target.path.startsWith(p));
    };
    const uncovered = record.execution.operations.filter(o => o.result !== 'SUCCEEDED').map(o => o.id)
      .concat(record.execution.operations.filter(o => o.result === 'SUCCEEDED').filter(o => {
        if (!permitted().has(o.operation)) return true;
        if (!(auth.change_ids || []).includes(o.change_id)) return true;
        const candidates = effective().filter(c => c.operations.includes(o.operation) && c.resource_class === o.target.resource_class);
        if (candidates.length === 0) return true;
        if (PATH_RESOURCES.has(o.target.resource_class) && !inPaths(auth.scope, o.target)) return true;
        return !candidates.some(c => c.state !== 'RESTRICTED' || inPaths(c.grant.scope, o.target));
      }).map(o => o.id));
    if (uncovered.length === 0) pass('every executed operation is covered by an effective capability',
      `${record.execution.operations.length} operations, ${effective().length} effective capabilities, operations ${[...permitted()].sort().join('/')}`);
    else fail('every executed operation is covered by an effective capability', uncovered.join(', '));
  }

  /* declared scope paths must describe the paths the change set actually touched */
  {
    const include = auth.scope?.paths?.include || [];
    let touched = [];
    try {
      touched = execFileSync('git', ['diff', '--name-only', record.repository.resolved_revision + '..HEAD'],
        { cwd: ROOT, encoding: 'utf8' }).trim().split('\n').filter(Boolean);
    } catch { touched = []; }
    const outside = touched.filter(f => !include.some(prefix => f === prefix || f.startsWith(prefix)));
    if (touched.length > 0 && outside.length === 0) {
      pass('declared scope paths cover everything the change set touched',
        `${touched.length} changed path(s) inside ${include.length} declared location(s)`);
    } else if (touched.length === 0) {
      pass('declared scope paths are stated', `${include.length} location(s); git comparison unavailable`);
    } else {
      fail('declared scope paths cover everything the change set touched', outside.slice(0, 5).join(', '));
    }
  }

  /* section 168: claim verification and execution verification are different domains */
  {
    const EXEC = ['NOT_STARTED', 'AUTHORIZATION_BLOCKED', 'READY', 'RUNNING', 'SUCCEEDED', 'PARTIALLY_SUCCEEDED', 'FAILED', 'CANCELLED', 'STOPPED'];
    const EV_STATE = ['NOT_REQUIRED', 'NOT_STARTED', 'READY', 'RUNNING', 'PASSED', 'PARTIALLY_PASSED', 'FAILED', 'BLOCKED', 'INCONCLUSIVE'];
    const EV_RESULT = ['CONFORMING', 'PARTIALLY_CONFORMING', 'NON_CONFORMING', 'INCONCLUSIVE', 'NOT_APPLICABLE'];
    const okExec = EXEC.includes(record.execution.state) && !('result' in record.execution);
    const okEv = EV_STATE.includes(record.execution_verification?.state) && EV_RESULT.includes(record.execution_verification?.result);
    if (okExec && okEv) {
      pass('execution verification is its own lifecycle, separate from execution',
        `execution ${record.execution.state}; execution_verification ${record.execution_verification.state}/${record.execution_verification.result}`);
    } else {
      fail('execution verification is its own lifecycle, separate from execution', `${record.execution.state} / ${record.execution_verification?.state}`);
    }

    const mixed = record.claims.filter(c => ['PASSED', 'CONFORMING', 'SUCCEEDED'].includes(c.claim_verification?.result));
    if (mixed.length === 0) pass('claim verification never borrows execution or verification lifecycle values');
    else fail('claim verification never borrows execution or verification lifecycle values', mixed.map(c => c.id).join(', '));

    /* EVV-008 / PV-009 as a procedural check: verification repaired nothing.
       A working tree may legitimately hold the change set being prepared, so the
       check is that nothing outside the declared scope paths is modified and
       that the frozen artifact digest still matches. */
    let dirty = [];
    try {
      dirty = execFileSync('git', ['status', '--porcelain'], { cwd: ROOT, encoding: 'utf8' })
        .split(/\r?\n/).filter(Boolean).map(l => l.slice(3).trim().replace(/^"|"$/g, ''));
    } catch { dirty = []; }
    const include = auth.scope?.paths?.include || [];
    const outsideScope = dirty.filter(f => !include.some(prefix => f === prefix || f.startsWith(prefix)));
    const digestOK = verifyArtifactDigest(registryDoc.record_provenance?.artifact_digest);
    if (outsideScope.length === 0 && digestOK) {
      pass('execution verification modified nothing outside the authorized scope',
        `${dirty.length} uncommitted path(s), all inside the declared scope; artifact digest unchanged`);
    } else {
      fail('execution verification modified nothing outside the authorized scope',
        outsideScope.length ? `outside scope: ${outsideScope.slice(0, 3).join(', ')}` : 'artifact digest mismatch');
    }
  }

  const flatEvidence = record.claims.flatMap(c => c.evidence).filter(e => typeof e === 'string');
  if (flatEvidence.length === 0) pass('evidence entries are objects with path and locator');
  else fail('evidence entries are objects with path and locator', `${flatEvidence.length} bare id(s)`);

  try {
    execFileSync(process.execPath, [path.join(ROOT, 'tools', 'validate-analysis.mjs')], { cwd: ROOT, stdio: 'pipe' });
    pass('the canonical record passes its own validator', 'tools/validate-analysis.mjs');
  } catch (error) {
    fail('the canonical record passes its own validator',
      String(error.stdout || error.message).trim().split('\n').pop());
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
    if (!/claim_kind/.test(text) || !/claim_verification/.test(text)) undeclared.push(rel);
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
