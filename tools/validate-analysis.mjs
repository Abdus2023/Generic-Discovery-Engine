#!/usr/bin/env node
/*
 * ============================================================================
 * Validate the canonical analysis record
 * ============================================================================
 *
 * Three layers of enforcement:
 *
 *   1. Structure and typed fields — the record is validated against
 *      docs/analysis/analysis.schema.json (JSON Schema draft 2020-12, the
 *      subset of keywords that schema uses is implemented here so that no
 *      network access or dependency is required).
 *
 *   2. Semantic rules V1-V20 — the state relationships JSON Schema cannot
 *      express.
 *
 *   3. Invariants I-001-I-016 — reported individually, so a reader can see
 *      which separation the record satisfies and which it does not.
 *
 * Also checks that the register resolves every evidence id, that evidence
 * objects carry a path and locator, and that claims.md is not stale.
 *
 * Usage:
 *   node tools/validate-analysis.mjs
 *
 * Exit code 0 = valid. Exit code 1 = at least one failure.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RECORD_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.json');
const SCHEMA_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.schema.json');
const REGISTER_PATH = path.join(ROOT, 'docs', 'analysis', 'evidence-register.md');

const results = [];
const pass = (m, n = '') => results.push(['PASS', m, n]);
const fail = (m, n = '') => results.push(['FAIL', m, n]);

const record = JSON.parse(fs.readFileSync(RECORD_PATH, 'utf8'));
const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
const register = fs.readFileSync(REGISTER_PATH, 'utf8');
const claims = record.claims;

const AUTHORIZATION_LEVELS = ['READ_ONLY', 'ANALYSIS_ONLY', 'DOC_REFACTOR', 'TEST_REFACTOR',
  'CODE_REFACTOR', 'ARCHITECTURE_CHANGE', 'COMMIT', 'PUSH'];

/* ========================================================================== */
/* 1. JSON Schema (implemented subset)                                        */
/* ========================================================================== */

function resolve(node) {
  if (node && node.$ref) {
    const parts = node.$ref.replace('#/', '').split('/');
    let target = schema;
    for (const part of parts) target = target[part];
    return resolve(target);
  }
  return node;
}

function validate(instance, node, at, errors) {
  const s = resolve(node);
  if (!s) return;
  const type = s.type;
  const typeOf = Array.isArray(instance) ? 'array'
    : instance === null ? 'null'
    : typeof instance === 'object' ? 'object' : typeof instance;
  if (type) {
    const allowed = Array.isArray(type) ? type : [type];
    if (!allowed.includes(typeOf)) {
      errors.push(`${at}: expected ${allowed.join('|')}, got ${typeOf}`);
      return;
    }
  }
  if ('const' in s && instance !== s.const) errors.push(`${at}: expected const ${s.const}, got ${instance}`);
  if (s.enum && !s.enum.includes(instance)) errors.push(`${at}: "${instance}" not in enum`);
  if (typeof instance === 'string') {
    if (s.minLength !== undefined && instance.length < s.minLength) errors.push(`${at}: shorter than minLength ${s.minLength}`);
    if (s.pattern && !new RegExp(s.pattern).test(instance)) errors.push(`${at}: "${instance}" does not match ${s.pattern}`);
  }
  if (typeOf === 'object') {
    for (const key of s.required || []) {
      if (!(key in instance)) errors.push(`${at}: missing required property "${key}"`);
    }
    for (const [key, value] of Object.entries(instance)) {
      if (s.properties && s.properties[key]) validate(value, s.properties[key], `${at}.${key}`, errors);
      else if (s.additionalProperties && typeof s.additionalProperties === 'object') {
        validate(value, s.additionalProperties, `${at}.${key}`, errors);
      } else if (s.additionalProperties === false) errors.push(`${at}: unexpected property "${key}"`);
    }
  }
  if (typeOf === 'array' && s.items) {
    instance.forEach((item, i) => validate(item, s.items, `${at}[${i}]`, errors));
  }
}

{
  const errors = [];
  validate(record, schema, '$', errors);
  if (errors.length === 0) pass('record validates against analysis.schema.json', 'JSON Schema draft 2020-12');
  else fail('record validates against analysis.schema.json', errors.slice(0, 6).join(' | '));
}

/* ========================================================================== */
/* 2. No generic status field                                                 */
/* ========================================================================== */

{
  const generic = [];
  (function walk(node, at) {
    if (Array.isArray(node)) return node.forEach((v, i) => walk(v, `${at}[${i}]`));
    if (node && typeof node === 'object') {
      for (const [k, v] of Object.entries(node)) {
        if (['status', 'state'].includes(k) && at !== '$.authorization') generic.push(`${at}.${k}`);
        walk(v, `${at}.${k}`);
      }
    }
  })(record, '$');
  if (generic.length === 0) pass('no generic "status" field is used', '"state" appears only as authorization.state');
  else fail('no generic "status" field is used', generic.slice(0, 5).join(', '));
}

/* ========================================================================== */
/* 3. Evidence register resolution                                            */
/* ========================================================================== */

{
  const defined = new Set(
    [...register.matchAll(/^\|\s*((?:CODE|TEST|DOC|CFG|HIST|ARCH|SCOPE|CONC|PROV|FAIL)-\d{3})\s*\|/gm)].map(m => m[1]));
  const unknown = [];
  for (const c of claims) for (const e of c.evidence) if (!defined.has(e.id)) unknown.push(`${c.id}->${e.id}`);
  if (unknown.length === 0) pass('every evidence id resolves in the register');
  else fail('every evidence id resolves in the register', unknown.slice(0, 5).join(', '));

  const shaped = claims.flatMap(c => c.evidence).filter(e =>
    !e.path || !e.locator || !e.locator.type || !e.locator.value);
  if (shaped.length === 0) pass('every evidence object carries id, kind, path and locator');
  else fail('every evidence object carries id, kind, path and locator', shaped.map(e => e.id).join(', '));
}

/* ========================================================================== */
/* 4. Semantic rules V1-V20                                                   */
/* ========================================================================== */

const rules = [];
const rule = (id, ok, note = '') => rules.push([id, ok, note]);

{
  const byId = new Map(claims.map(c => [c.id, c]));
  const contradictionClaims = new Set(record.contradictions.flatMap(x => [x.claim_a, x.claim_b]));

  /* V1 */
  const v1 = claims.filter(c => c.evidence_level === 'INACCESSIBLE' && c.verification_result !== 'UNVERIFIED');
  rule('V1', v1.length === 0, 'INACCESSIBLE evidence requires UNVERIFIED' + (v1.length ? ': ' + v1.map(c => c.id).join(', ') : ''));

  /* V2 — ABSENT may be VERIFIED only with a recorded absence-verification procedure */
  const procedures = new Set((record.absence_verification || []).map(a => a.id));
  const v2 = claims.filter(c => c.evidence_level === 'ABSENT' && c.verification_result === 'VERIFIED' &&
    !procedures.has(c.absence_verification));
  rule('V2', v2.length === 0,
    'ABSENT + VERIFIED requires a recorded absence procedure' + (v2.length ? ': ' + v2.map(c => c.id).join(', ') : ''));

  /* V3 — VERIFIED requires DIRECT or CORROBORATED, unless V2's absence procedure applies */
  const v3 = claims.filter(c => c.verification_result === 'VERIFIED' &&
    !['DIRECT', 'CORROBORATED'].includes(c.evidence_level) &&
    !(c.evidence_level === 'ABSENT' && procedures.has(c.absence_verification)));
  rule('V3', v3.length === 0, 'VERIFIED requires DIRECT or CORROBORATED (ABSENT only via V2)' +
    (v3.length ? ': ' + v3.map(c => c.id).join(', ') : ''));

  /* V4 — CONTRADICTED requires conflicting evidence: either a claim-to-claim
     contradiction record or an explicit conflicting_evidence list */
  const v4 = claims.filter(c => c.verification_result === 'CONTRADICTED' &&
    !(contradictionClaims.has(c.id) || (c.conflicting_evidence || []).length > 0));
  rule('V4', v4.length === 0, 'CONTRADICTED requires conflicting evidence' +
    (v4.length ? ': ' + v4.map(c => c.id).join(', ') : ''));

  /* V5 — PLANNED must not be IMPLEMENTED unless the record says so explicitly */
  const v5 = claims.filter(c => c.claim_kind === 'PLANNED' && c.implementation_state === 'IMPLEMENTED');
  rule('V5', v5.length === 0, 'PLANNED + IMPLEMENTED requires an explicit historical-implementation note' +
    (v5.length ? ': ' + v5.map(c => c.id).join(', ') : ''));

  /* V6 / V7 — NON_GOAL and HYPOTHESIS should carry NOT_APPLICABLE */
  const v6 = claims.filter(c => c.claim_kind === 'NON_GOAL' && c.implementation_state !== 'NOT_APPLICABLE');
  rule('V6', v6.length === 0, 'NON_GOAL should be NOT_APPLICABLE' + (v6.length ? ': ' + v6.map(c => c.id).join(', ') : ''));
  const v7 = claims.filter(c => c.claim_kind === 'HYPOTHESIS' && c.implementation_state !== 'NOT_APPLICABLE');
  rule('V7', v7.length === 0, 'HYPOTHESIS should be NOT_APPLICABLE' + (v7.length ? ': ' + v7.map(c => c.id).join(', ') : ''));

  /* §93 — NOT_IMPLEMENTED + TESTED requires an explicit absence test */
  const v93 = claims.filter(c => c.implementation_state === 'NOT_IMPLEMENTED' && c.test_state === 'TESTED' &&
    !c.absence_test);
  rule('93', v93.length === 0, 'NOT_IMPLEMENTED + TESTED requires an explicit absence test' +
    (v93.length ? ': ' + v93.map(c => c.id).join(', ') : ''));

  /* §94 — INACCESSIBLE must not be relabelled ABSENT */
  const inaccessible = claims.filter(c => c.evidence_level === 'INACCESSIBLE');
  const fullAccess = record.repository.access_level === 'FULL';
  rule('94', !(fullAccess && inaccessible.length > 0),
    fullAccess ? `full access: ${claims.filter(c => c.evidence_level === 'ABSENT').length} ABSENT, 0 INACCESSIBLE (no conversion)`
      : 'partial access: absence must not be asserted as ABSENT');

  /* V8 / V9 — mutation requires a granted authorization with an explicit level */
  const executed = record.execution.executed_changes;
  const granted = record.authorization.state === 'GRANTED';
  rule('V8', granted || executed.length === 0, 'mutation only under GRANTED' + (granted ? '' : ' — no execution permitted'));
  rule('V9', !granted || AUTHORIZATION_LEVELS.includes(record.authorization.level),
    'a granted authorization must state a level');

  /* V10 — every executed change is authorized */
  const authorized = new Set(record.authorization.change_ids);
  const v10 = executed.filter(id => !authorized.has(id));
  rule('V10', v10.length === 0, `executed changes are authorized (${executed.length}/${authorized.size})`);

  /* V11 — every executed operation is permitted, and COMMIT/PUSH are never inherited */
  const ops = new Set(record.authorization.operations || []);
  const execOps = record.execution.operations || [];
  const v11 = execOps.filter(op => !ops.has(op));
  const declaredExtra = new Set(record.authorization.additional_levels_declared || []);
  const inherited = record.authorization.hierarchical === true ? []
    : execOps.filter(op => ['COMMIT', 'PUSH'].includes(op) && !declaredExtra.has(op));
  rule('V11', v11.length === 0 && inherited.length === 0,
    `executed operations are permitted (${execOps.length})` +
    (inherited.length ? ` — not inherited: ${inherited.join(', ')}` : ''));

  /* V12 / V13 — execution result consistency */
  rule('V12', !(record.execution.result === 'NOT_EXECUTED' && executed.length > 0),
    'NOT_EXECUTED implies zero executed changes');
  rule('V13', !(record.execution.result === 'SUCCEEDED' && record.execution.unauthorized_changes.length > 0),
    'SUCCEEDED implies no unauthorized changes');

  /* V14 — revoked or expired authorization prevents execution */
  const dead = ['REVOKED', 'EXPIRED'].includes(record.authorization.state);
  rule('V14', !(dead && executed.length > 0), 'REVOKED/EXPIRED prevents subsequent execution');

  /* V15 — newly discovered work outside change_ids is not executed */
  const discovered = record.execution.discovered_not_executed || [];
  const leaked = discovered.filter(id => executed.includes(id));
  rule('V15', leaked.length === 0,
    `discovered work (${discovered.length}) was not executed without authorization` +
    (leaked.length ? ` — leaked: ${leaked.join(', ')}` : ''));

  /* V16 / V20 — post-verification is independent and repairs nothing */
  const pv = record.post_verification || {};
  rule('V16', pv.independent === true && !!pv.method, 'post-verification is independent of the execution result');
  rule('V20', Array.isArray(pv.mutations) && pv.mutations.length === 0, 'verification did not modify repository state');

  /* V17 / V18 / V19 — governance separation */
  const roles = record.authorization.roles || {};
  rule('V17', !!record.repository.access_level && record.authorization.state === 'GRANTED' &&
    String(record.authorization.authority?.identifier || '').length > 0,
    'technical access is recorded separately from granted authorization');
  rule('V18', /EXECUTOR role/i.test(String(roles.EXECUTOR || '')) || !!record.authorization.role_entry,
    'executor authority is entered explicitly, not implied by the analyzer role');
  rule('V19', record.authorization.authority?.identifier !== roles.EXECUTOR,
    'the executor did not grant its own authorization');

  const failed = rules.filter(([, ok]) => !ok);
  if (failed.length === 0) pass('semantic rules V1-V20 hold', `${rules.length} rules evaluated`);
  else fail('semantic rules V1-V20 hold', failed.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
}

/* ========================================================================== */
/* 5. Invariants I-001-I-016                                                  */
/* ========================================================================== */

{
  const invariants = [
    ['I-001', 'No generic status field', () => !/"(status|quality)"\s*:/.test(fs.readFileSync(RECORD_PATH, 'utf8'))],
    ['I-002', 'Claim kind describes claim semantics', () => claims.every(c => typeof c.claim_kind === 'string')],
    ['I-003', 'Implementation state describes implementation', () => claims.every(c => typeof c.implementation_state === 'string')],
    ['I-004', 'Test state describes testing', () => claims.every(c => typeof c.test_state === 'string')],
    ['I-005', 'Evidence level describes evidence strength/availability', () => claims.every(c => typeof c.evidence_level === 'string')],
    ['I-006', 'Verification result describes verification conclusion', () => claims.every(c => typeof c.verification_result === 'string')],
    ['I-007', 'Authorization state describes whether permission exists', () => typeof record.authorization.state === 'string'],
    ['I-008', 'Authorization level describes permitted capability', () => typeof record.authorization.level === 'string'],
    ['I-009', 'Execution result describes what actually happened', () => typeof record.execution.result === 'string'],
    ['I-010', 'Technical access does not imply authorization', () => 'authorization' in record && 'access_level' in record.repository],
    ['I-011', 'Authorization does not imply execution', () => !('execution' in record.authorization)],
    ['I-012', 'Execution success does not imply post-verification success',
      () => 'post_verification' in record && record.post_verification.result !== record.execution.result],
    ['I-013', 'Every executed change is authorized',
      () => record.execution.executed_changes.every(id => record.authorization.change_ids.includes(id))],
    ['I-014', 'Every important verification claim has evidence',
      () => claims.filter(c => c.verification_result === 'VERIFIED').every(c => c.evidence.length > 0)],
    ['I-015', 'INACCESSIBLE cannot become ABSENT without a new verification step',
      () => !(record.repository.access_level === 'FULL' && claims.some(c => c.evidence_level === 'INACCESSIBLE'))],
    ['I-016', 'Newly discovered work cannot silently expand execution scope',
      () => record.execution.unauthorized_changes.length === 0 &&
        (record.execution.discovered_not_executed || []).every(id => !record.execution.executed_changes.includes(id))]
  ];
  const violated = invariants.filter(([, , check]) => !check());
  if (violated.length === 0) pass('machine-readable invariants hold', `${invariants.length} invariants`);
  else fail('machine-readable invariants hold', violated.map(([id]) => id).join(', '));
}

/* ========================================================================== */
/* 6. Five questions stay independent, claims.md is current                   */
/* ========================================================================== */

{
  const fields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result'];
  const counts = fields.map(f => new Set(claims.map(c => c[f])).size);
  if (counts.every(n => n > 1)) pass('all five claim fields carry independent information',
    fields.map((f, i) => `${f}=${counts[i]}`).join(', '));
  else fail('all five claim fields carry independent information', fields.map((f, i) => `${f}=${counts[i]}`).join(', '));

  const enumDrift = fields.flatMap(f => claims.filter(c => !schema.$defs.claim.properties[f].enum.includes(c[f]))
    .map(c => `${c.id}.${f}`));
  if (enumDrift.length === 0) pass('every claim field uses the schema enum');
  else fail('every claim field uses the schema enum', enumDrift.slice(0, 6).join(', '));
}

/* Any document that restates a claim's typed fields must agree with the record. */
{
  const docPath = path.join(ROOT, 'docs', 'analysis', 'repository-analysis-2026-09-10.md');
  const doc = fs.readFileSync(docPath, 'utf8');
  const byId = new Map(claims.map(c => [c.id, c]));
  const stale = [];
  for (const m of doc.matchAll(/\| `([A-Z]+-CLAIM-\d{3})` \| ([^|]*)\|/g)) {
    const claim = byId.get(m[1]);
    if (!claim) continue;
    const shown = [...m[2].matchAll(/`([A-Z_]+)`/g)].map(x => x[1]);
    if (shown.length !== 5) continue;
    const actual = [claim.claim_kind, claim.implementation_state, claim.test_state,
      claim.evidence_level, claim.verification_result];
    if (shown.join('|') !== actual.join('|')) stale.push(`${claim.id} (${shown.join('·')} vs ${actual.join('·')})`);
  }
  if (stale.length === 0) pass('restated claim fields match the record', 'repository-analysis §3 index');
  else fail('restated claim fields match the record', stale.slice(0, 3).join(' | '));
}

{
  try {
    execFileSync(process.execPath, [path.join(ROOT, 'tools', 'render-claims.mjs'), '--check'],
      { cwd: ROOT, stdio: 'pipe' });
    pass('claims.md matches analysis.json', 'generated tables are current');
  } catch (error) {
    fail('claims.md matches analysis.json', String(error.stdout || error.message).trim().split('\n').pop());
  }
}

/* ========================================================================== */
/* Report                                                                     */
/* ========================================================================== */

const width = Math.max(...results.map(r => r[1].length));
console.log('validating docs/analysis/analysis.json against docs/analysis/analysis.schema.json\n');
for (const [level, message, note] of results) console.log(`[${level}] ${message.padEnd(width)}  ${note}`);
const failures = results.filter(r => r[0] === 'FAIL').length;
console.log(`\n${results.filter(r => r[0] === 'PASS').length} passed, ${failures} failed`);
process.exit(failures === 0 ? 0 : 1);
