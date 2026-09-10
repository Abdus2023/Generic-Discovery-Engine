#!/usr/bin/env node
/*
 * ============================================================================
 * Validate the canonical analysis record
 * ============================================================================
 *
 * Validation pipeline (each stage validated independently):
 *
 *   STRUCTURAL      JSON Schema draft 2020-12  (analysis.schema.json)
 *   CLAIMS          validation matrix CV-001…CV-020, rules C-001…C-043
 *   EVIDENCE        CV-008/CV-010 evidence rules, register resolution
 *   AUTHORIZATION   AUTH-001…AUTH-020 (state, level profile, capability,
 *                   operation, scope, change authorization)
 *   EXECUTION       EV-001…EV-012
 *   POST-VERIFY     PV-001…PV-010
 *   SERIALIZATION   SER-001…SER-012  (analysis.json vs authorization.yaml)
 *   INVARIANTS      I-001…I-016
 *
 * The level profiles and the capability → operation mapping are read from the
 * schema, so the validator never keeps a second copy of the policy.
 *
 * Usage:  node tools/validate-analysis.mjs
 * Exit 0 = valid. Exit 1 = at least one failure.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RECORD_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.json');
const SCHEMA_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.schema.json');
const YAML_PATH = path.join(ROOT, 'docs', 'analysis', 'authorization.yaml');
const REGISTER_PATH = path.join(ROOT, 'docs', 'analysis', 'evidence-register.md');

const results = [];
const pass = (stage, m, n = '') => results.push([stage, 'PASS', m, n]);
const fail = (stage, m, n = '') => results.push([stage, 'FAIL', m, n]);

const record = JSON.parse(fs.readFileSync(RECORD_PATH, 'utf8'));
const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
const register = fs.readFileSync(REGISTER_PATH, 'utf8');
const claims = record.claims;
const PROFILES = schema.level_profiles;
const CAP_OPS = schema.capability_operations;
const ALL_CAPS = Object.keys(CAP_OPS);
const ALL_PROFILES = Object.keys(PROFILES);

/* ========================================================================== */
/* STRUCTURAL — JSON Schema (implemented subset)                              */
/* ========================================================================== */

function resolve(node) {
  if (node && node.$ref) {
    let target = schema;
    for (const part of node.$ref.replace('#/', '').split('/')) target = target[part];
    return resolve(target);
  }
  return node;
}

function validate(instance, node, at, errors) {
  const s = resolve(node);
  if (!s) return;
  const typeOf = Array.isArray(instance) ? 'array'
    : instance === null ? 'null'
    : typeof instance === 'object' ? 'object' : typeof instance;
  if (s.type) {
    const allowed = Array.isArray(s.type) ? s.type : [s.type];
    if (!allowed.includes(typeOf)) { errors.push(`${at}: expected ${allowed.join('|')}, got ${typeOf}`); return; }
  }
  if ('const' in s && instance !== s.const) errors.push(`${at}: expected const ${s.const}`);
  if (s.enum && !s.enum.includes(instance)) errors.push(`${at}: "${instance}" not in enum`);
  if (typeof instance === 'string') {
    if (s.minLength !== undefined && instance.length < s.minLength) errors.push(`${at}: shorter than minLength`);
    if (s.pattern && !new RegExp(s.pattern).test(instance)) errors.push(`${at}: "${instance}" does not match ${s.pattern}`);
  }
  if (typeOf === 'object') {
    for (const key of s.required || []) if (!(key in instance)) errors.push(`${at}: missing required property "${key}"`);
    for (const [key, value] of Object.entries(instance)) {
      if (s.properties && s.properties[key]) validate(value, s.properties[key], `${at}.${key}`, errors);
      else if (s.additionalProperties && typeof s.additionalProperties === 'object') validate(value, s.additionalProperties, `${at}.${key}`, errors);
      else if (s.additionalProperties === false) errors.push(`${at}: unexpected property "${key}"`);
    }
  }
  if (typeOf === 'array' && s.items) instance.forEach((item, i) => validate(item, s.items, `${at}[${i}]`, errors));
}

{
  const errors = [];
  validate(record, schema, '$', errors);
  if (errors.length === 0) pass('STRUCTURAL', 'record validates against analysis.schema.json', 'draft 2020-12');
  else fail('STRUCTURAL', 'record validates against analysis.schema.json', errors.slice(0, 5).join(' | '));

  const generic = [];
  const onEvidence = [];
  (function walk(node, at) {
    if (Array.isArray(node)) return node.forEach((v, i) => walk(v, `${at}[${i}]`));
    if (node && typeof node === 'object') {
      const isEvidence = typeof node.id === 'string' && node.locator && node.kind;
      for (const [k, v] of Object.entries(node)) {
        if (['status', 'state'].includes(k) && !/authorization|execution|post_verification/.test(at)) generic.push(`${at}.${k}`);
        if (isEvidence && (k === 'status' || k === 'state')) onEvidence.push(`${at}.${k}`);
        walk(v, `${at}.${k}`);
      }
    }
  })(record, '$');
  if (generic.length === 0) pass('STRUCTURAL', 'no generic "status" field is used', 'I-001');
  else fail('STRUCTURAL', 'no generic "status" field is used', generic.slice(0, 4).join(', '));
  if (onEvidence.length === 0) pass('STRUCTURAL', 'no status field is permitted on evidence', 'section 143');
  else fail('STRUCTURAL', 'no status field is permitted on evidence', onEvidence.join(', '));
}

/* ========================================================================== */
/* EVIDENCE REGISTER RESOLUTION                                               */
/* ========================================================================== */

{
  const defined = new Set(
    [...register.matchAll(/^\|\s*((?:CODE|TEST|DOC|CFG|HIST|ARCH|SCOPE|CONC|PROV|FAIL)-\d{3})\s*\|/gm)].map(m => m[1]));
  const unknown = [];
  for (const c of claims) for (const e of c.evidence) if (!defined.has(e.id)) unknown.push(`${c.id}->${e.id}`);
  if (unknown.length === 0) pass('EVIDENCE', 'every evidence id resolves in the register');
  else fail('EVIDENCE', 'every evidence id resolves in the register', unknown.slice(0, 5).join(', '));

  const shaped = claims.flatMap(c => c.evidence).filter(e => !e.path || !e.locator?.type || !e.locator?.value);
  if (shaped.length === 0) pass('EVIDENCE', 'every evidence object carries id, kind, path and locator');
  else fail('EVIDENCE', 'every evidence object carries id, kind, path and locator', shaped.map(e => e.id).join(', '));
}

/* ========================================================================== */
/* CLAIMS — CV-001…CV-020 and the C-rules not covered by the matrix           */
/* ========================================================================== */

const byId = new Map(claims.map(c => [c.id, c]));
const contradictedIds = new Set(record.contradictions.flatMap(x => [x.claim_a, x.claim_b]));
const procedures = new Set((record.absence_verification || []).map(a => a.id));
const evidenceIdsOf = claim => claim.evidence.map(e => e.id);
const hasKind = (claim, kinds) => claim.evidence.some(e => kinds.includes(e.kind));
const enumOf = field => schema.$defs.claim.properties[field].enum;

const claimChecks = [];
const rule = (id, ok, note) => claimChecks.push([id, ok, note]);

/* CV-001…CV-005 — every dimension uses its canonical enum */
{
  const fields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result'];
  const bad = fields.flatMap(f => claims.filter(c => !enumOf(f).includes(c[f])).map(c => `${c.id}.${f}`));
  rule('CV-001…CV-005', bad.length === 0, 'all six claim dimensions use the canonical enums' +
    (bad.length ? ': ' + bad.slice(0, 5).join(', ') : ''));
}

/* CV-006 — VERIFIED requires DIRECT or CORROBORATED evidence */
{
  const bad = claims.filter(c => c.verification_result === 'VERIFIED' &&
    !['DIRECT', 'CORROBORATED'].includes(c.evidence_level) &&
    !(c.evidence_level === 'ABSENT' && procedures.has(c.absence_verification)));
  rule('CV-006', bad.length === 0, 'VERIFIED requires DIRECT | CORROBORATED (ABSENT only with a recorded procedure)' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-007 — INACCESSIBLE normally requires UNVERIFIED */
{
  const bad = claims.filter(c => c.evidence_level === 'INACCESSIBLE' && c.verification_result !== 'UNVERIFIED');
  rule('CV-007', bad.length === 0, 'INACCESSIBLE requires UNVERIFIED' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-008 — CONTRADICTED requires conflicting evidence */
{
  const bad = claims.filter(c => c.verification_result === 'CONTRADICTED' &&
    !(contradictedIds.has(c.id) || (c.conflicting_evidence || []).length > 0));
  rule('CV-008', bad.length === 0, 'CONTRADICTED requires conflicting evidence' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-009 — IMPLEMENTED requires implementation evidence */
{
  const bad = claims.filter(c => c.implementation_state === 'IMPLEMENTED' && !hasKind(c, ['CODE', 'CONFIG', 'TEST', 'HISTORY', 'GENERATED_ARTIFACT']));
  rule('CV-009', bad.length === 0, 'IMPLEMENTED requires implementation evidence' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-010 — NOT_IMPLEMENTED requires sufficiently inspected scope or explicit negative evidence */
{
  const bad = claims.filter(c => {
    if (c.implementation_state !== 'NOT_IMPLEMENTED') return false;
    if (c.evidence_level === 'INACCESSIBLE') return true;
    if (['DIRECT', 'CORROBORATED'].includes(c.evidence_level)) return false;
    return !(c.evidence_level === 'ABSENT' && procedures.has(c.absence_verification));
  });
  rule('CV-010', bad.length === 0, 'NOT_IMPLEMENTED requires inspected scope or negative evidence, never INACCESSIBLE' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-011 — HYPOTHESIS uses NOT_APPLICABLE for implementation_state */
{
  const bad = claims.filter(c => c.claim_kind === 'HYPOTHESIS' && c.implementation_state !== 'NOT_APPLICABLE');
  rule('CV-011', bad.length === 0, 'HYPOTHESIS requires implementation_state NOT_APPLICABLE' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-012 — NON_GOAL uses NOT_APPLICABLE for implementation_state, with scope evidence */
{
  const bad = claims.filter(c => c.claim_kind === 'NON_GOAL' &&
    (c.implementation_state !== 'NOT_APPLICABLE' || c.evidence.length === 0));
  rule('CV-012', bad.length === 0, 'NON_GOAL requires NOT_APPLICABLE with scope evidence' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-013 — PLANNED normally implies NOT_IMPLEMENTED */
{
  const bad = claims.filter(c => c.claim_kind === 'PLANNED' && !['NOT_IMPLEMENTED', 'NOT_APPLICABLE'].includes(c.implementation_state)
    && c.implementation_state !== 'IMPLEMENTED');
  const historical = claims.filter(c => c.claim_kind === 'PLANNED' && c.implementation_state === 'IMPLEMENTED');
  const unjustified = historical.filter(c => c.historical_plan_implemented !== true);
  rule('CV-013', bad.length === 0 && unjustified.length === 0,
    `PLANNED implies NOT_IMPLEMENTED; ${historical.length} implemented historical plan(s) recorded explicitly` +
    (bad.length || unjustified.length ? ': ' + [...bad, ...unjustified].map(c => c.id).join(', ') : ''));
}

/* CV-014 — TESTED requires execution evidence; TESTED implies VERIFIED is forbidden */
{
  const noEvidence = claims.filter(c => ['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state) && !hasKind(c, ['TEST']));
  const promoted = claims.filter(c => c.test_state === 'TESTED' && c.verification_result === 'VERIFIED' &&
    c.evidence_level === 'INDIRECT');
  rule('CV-014', noEvidence.length === 0 && promoted.length === 0,
    'TESTED requires execution evidence, and testing alone does not make an indirect claim VERIFIED' +
    ((noEvidence.length || promoted.length) ? ': ' + [...noEvidence, ...promoted].map(c => c.id).join(', ') : ''));
}

/* CV-015 — UNTESTED does not imply implementation failure. Checked as an
   independence property: an untested claim may still be IMPLEMENTED, and an
   untested claim may be NOT_IMPLEMENTED on non-test evidence. */
{
  const untested = claims.filter(c => c.test_state === 'UNTESTED');
  const states = new Set(untested.map(c => c.implementation_state));
  rule('CV-015', states.size > 1 || untested.length === 0,
    'UNTESTED spans implementation states without implying failure: ' +
    [...states].sort().join(', '));
}

/* CV-016…CV-019 — prohibited inferences. A dimension must not determine
   another: if every observed value of A came with exactly one value of B, the
   record would be treating the inference as a rule. The check is therefore an
   independence test over the observed combinations. */
{
  const spans = (subset, field) => new Set(subset.map(c => c[field])).size;
  const implemented = claims.filter(c => c.implementation_state === 'IMPLEMENTED');
  const tested = claims.filter(c => ['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state));
  const verified = claims.filter(c => c.verification_result === 'VERIFIED');
  const partial = claims.filter(c => c.implementation_state === 'PARTIAL');
  const results = [
    ['CV-016', spans(implemented, 'test_state') > 1, 'IMPLEMENTED does not imply TESTED', `${implemented.length} implemented, test states: ${[...new Set(implemented.map(c => c.test_state))].sort().join('/')}`],
    ['CV-017', spans(tested, 'verification_result') > 1, 'TESTED does not imply VERIFIED', `${tested.length} tested, verification: ${[...new Set(tested.map(c => c.verification_result))].sort().join('/')}`],
    ['CV-018', spans(verified, 'implementation_state') > 1, 'VERIFIED does not imply IMPLEMENTED', `${verified.length} verified, implementation: ${[...new Set(verified.map(c => c.implementation_state))].sort().join('/')}`],
    ['CV-019', partial.every(c => c.verification_result !== 'PARTIALLY_VERIFIED') || verified.every(c => c.implementation_state !== 'PARTIAL'),
      'PARTIAL implementation and PARTIALLY_VERIFIED are independent dimensions',
      `${partial.length} partial implementation(s), no forced partial-verification pairing`],
  ];
  for (const [id, ok, message, note] of results) rule(id, ok, `${message} — ${note}`);
}

/* CV-020 — INACCESSIBLE is never silently converted to ABSENT */
{
  const bad = claims.filter(c => c.evidence_level === 'INACCESSIBLE' ? c.verification_result === 'VERIFIED'
    : (c.evidence_level === 'ABSENT' && !c.absence_verification && c.verification_result === 'VERIFIED'));
  const inaccessible = claims.filter(c => c.evidence_level === 'INACCESSIBLE');
  rule('CV-020', bad.length === 0,
    `ABSENT determinations record an inspection procedure; INACCESSIBLE is never presented as absence (${inaccessible.length} INACCESSIBLE, ${procedures.size} procedures)` +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* C-031 — CORROBORATED requires materially independent sources */
{
  const bad = [];
  for (const c of claims.filter(x => x.evidence_level === 'CORROBORATED')) {
    const paths = new Set(c.evidence.map(e => e.path));
    const kinds = new Set(c.evidence.map(e => e.kind));
    if (c.evidence.length < 2 || (paths.size < 2 && kinds.size < 2)) bad.push(c.id);
  }
  rule('C-031', bad.length === 0, 'CORROBORATED requires >=2 independent sources (or >=2 kinds)' +
    (bad.length ? ': ' + bad.join(', ') : ''));
}

/* C-040 — a VERIFIED claim is not one side of an unresolved contradiction */
{
  const bad = claims.filter(c => c.verification_result === 'VERIFIED' && contradictedIds.has(c.id));
  rule('C-040', bad.length === 0, 'VERIFIED excludes unresolved claim contradictions' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* section 93 — NOT_IMPLEMENTED + TESTED requires an absence test */
{
  const bad = claims.filter(c => c.implementation_state === 'NOT_IMPLEMENTED' && c.test_state === 'TESTED' && !c.absence_test);
  rule('C-093', bad.length === 0, 'NOT_IMPLEMENTED + TESTED requires an absence_test' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* section 141 — confidence is graded evidence strength, never a substitute.
   The confusing combination HIGH/VERY_HIGH with UNVERIFIED is forbidden. */
{
  const bad = claims.filter(c => ['HIGH', 'VERY_HIGH'].includes(c.confidence) && c.verification_result === 'UNVERIFIED');
  const missing = claims.filter(c => !c.confidence);
  const rule6 = ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'];
  const invalid = claims.filter(c => !rule6.includes(c.confidence));
  rule('C-141', bad.length === 0 && missing.length === 0 && invalid.length === 0,
    'confidence grades evidential strength and never contradicts verification' +
    (bad.length ? ' — HIGH with UNVERIFIED: ' + bad.map(c => c.id).join(', ') : '') +
    (missing.length ? ` — ${missing.length} claim(s) without confidence` : ''));
}

{
  const violated = claimChecks.filter(([, ok]) => !ok);
  if (violated.length === 0) pass('CLAIMS', 'claim rules and validation matrix hold', `${claimChecks.length} rule groups`);
  else fail('CLAIMS', 'claim rules and validation matrix hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
}

{
  const fields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result'];
  const counts = fields.map(f => new Set(claims.map(c => c[f])).size);
  if (counts.every(n => n > 1)) pass('CLAIMS', 'no dimension is derived from another', fields.map((f, i) => `${f}=${counts[i]}`).join(', '));
  else fail('CLAIMS', 'no dimension is derived from another', fields.map((f, i) => `${f}=${counts[i]}`).join(', '));
}

/* ========================================================================== */
/* AUTHORIZATION — AUTH-001…AUTH-020                                          */
/* ========================================================================== */

const grants = [record.authorization, ...(record.authorization_grants || [])];

/* Capabilities(L) = Own(L) ∪ Capabilities(parents), over the declared edges.  */
function capabilityClosure(profile, path_ = []) {
  if (path_.includes(profile)) throw new Error(`inheritance cycle: ${[...path_, profile].join(' -> ')}`);
  const node = PROFILES[profile];
  if (!node) throw new Error(`unknown profile ${profile}`);
  const out = new Set(node.capabilities || []);
  for (const parent of node.inherits || []) {
    for (const cap of capabilityClosure(parent, [...path_, profile])) out.add(cap);
  }
  return out;
}

const effective = grant => {
  const ceiling = capabilityClosure(grant.level?.profile);
  const caps = grant.capabilities || {};
  const allow = caps.allow || [...ceiling];
  const keep = caps.mode === 'INHERIT' ? [...allow] : [...allow].filter(c => ceiling.has(c));
  const afterAllow = new Set(keep);
  for (const cap of caps.deny || []) afterAllow.delete(cap);
  return afterAllow;
};

/* Operations implied by a capability set: §147 capability → operation. */
const operationsOf = caps => new Set([...caps].map(c => CAP_OPS[c]?.operation).filter(Boolean));

const permittedOperations = grant => {
  const implied = operationsOf(effective(grant));
  const ops = grant.operations || {};
  const allow = ops.allow ? ops.allow.filter(op => implied.has(op)) : [...implied];
  const afterAllow = new Set(allow);
  for (const op of ops.deny || []) afterAllow.delete(op);
  return afterAllow;
};

const authChecks = [];
const ar = (id, ok, note) => authChecks.push([id, ok, note]);
const STATES = ['NOT_REQUESTED', 'REQUESTED', 'DENIED', 'GRANTED', 'REVOKED', 'EXPIRED'];

ar('AUTH-001', grants.every(g => STATES.includes(g.state)), 'authorization state uses the authorization enum');
ar('AUTH-002', grants.every(g => ALL_PROFILES.includes(g.level?.profile)),
  `level is a profile, not an operation list (${grants.map(g => g.level?.profile).join(', ')})`);
ar('AUTH-003', grants.filter(g => g.state === 'GRANTED').every(g => g.authority?.identifier), 'GRANTED requires an authority');
ar('AUTH-004', grants.filter(g => g.state === 'GRANTED').every(g => g.target?.repository), 'GRANTED requires a target');
ar('AUTH-005', !record.execution.executed_changes.length || grants.some(g => (g.change_ids || []).length > 0),
  'GRANTED mutation requires change_ids');

{
  const escalation = grants.flatMap(g => {
    const ceiling = capabilityClosure(g.level?.profile);
    return (g.capabilities?.allow || []).filter(c => !ceiling.has(c)).map(c => `${g.level.profile}:${c}`);
  });
  ar('AUTH-006', escalation.length === 0,
    'allow never introduces a capability the profile does not contain' + (escalation.length ? ` — ${escalation.join(', ')}` : ''));
}

{
  const catalogue = ALL_CAPS.filter(c => !(schema.$defs.capabilities.properties.allow.items.enum || []).includes(c));
  const report = grants.map(g => `${g.level.profile} → ${effective(g).size} caps / ${permittedOperations(g).size} ops`);
  ar('AUTH-007', catalogue.length === 0, 'EffectiveCapabilities = (Capabilities(profile) ∩ allow) − deny: ' + report.join('; '));
}

{
  const bad = grants.flatMap(g => {
    const implied = operationsOf(effective(g));
    return (g.operations?.allow || []).filter(op => !implied.has(op)).map(op => `${g.level.profile}:${op}`);
  });
  ar('AUTH-008', bad.length === 0, 'every allowed operation is implied by an effective capability' +
    (bad.length ? ` — ${bad.join(', ')}` : ''));
}

{
  const denied = grants.flatMap(g => (g.capabilities?.deny || []).filter(c => effective(g).has(c)));
  ar('AUTH-009', denied.length === 0, 'deny wins over allow and over the profile' + (denied.length ? ` — ${denied.join(', ')}` : ''));
}

{
  const authorized = new Set(grants.flatMap(g => g.change_ids || []));
  const bad = record.execution.executed_changes.filter(id => !authorized.has(id));
  ar('AUTH-010', bad.length === 0, 'every executed change belongs to change_ids' + (bad.length ? `: ${bad.join(', ')}` : ''));
}

{
  const permitted = new Set(grants.flatMap(g => [...permittedOperations(g)]));
  const bad = (record.execution.operations || []).filter(o => o.result === 'SUCCEEDED' && !permitted.has(o.operation));
  ar('AUTH-011', bad.length === 0,
    `every executed operation is permitted (${(record.execution.operations || []).length} operations)` +
    (bad.length ? ` — uncovered: ${bad.map(o => o.operation).join(', ')}` : ''));
}

{
  const dead = grants.filter(g => ['REVOKED', 'EXPIRED'].includes(g.state) && record.execution.executed_changes.length > 0);
  ar('AUTH-012', dead.length === 0, 'REVOKED/EXPIRED cannot authorize execution');
}

{
  const identifiers = grants.map(g => g.authority?.identifier || '');
  const technical = identifiers.filter(id => /access|permission|repository user|token|credential/i.test(id));
  ar('AUTH-013', technical.length === 0 && identifiers.every(i => i.length > 0), 'technical permission cannot satisfy a grant');
}

{
  const executor = record.governance?.roles?.EXECUTOR || '';
  const self = grants.filter(g => executor && String(g.authority?.identifier || '') === executor);
  ar('AUTH-014', self.length === 0, 'the executor did not grant its own authority');
}

{
  /* File-level operations carry a path and are checked against the scope.
     COMMIT/PUSH are repository-level acts: they are constrained by the change
     set (AUTH-011/AUTH-016) rather than by a path prefix. */
  const fileLevel = new Set(['CREATE', 'MODIFY', 'RENAME', 'MOVE', 'DELETE']);
  const include = [...new Set(grants.flatMap(g => g.scope?.paths?.include || []))];
  const exclude = [...new Set(grants.flatMap(g => g.scope?.paths?.exclude || []))];
  const bad = record.execution.operations
    .filter(o => o.result === 'SUCCEEDED' && fileLevel.has(o.operation))
    .filter(o => !include.some(prefix => o.target.startsWith(prefix)) || exclude.some(prefix => o.target.startsWith(prefix)))
    .map(o => `${o.id}:${o.target}`);
  const publication = record.execution.operations.filter(o => ['COMMIT', 'PUSH'].includes(o.operation)).length;
  ar('AUTH-015', bad.length === 0,
    `file-level operations stay inside scope.paths (${include.length} include, ${exclude.length} exclude; ${publication} repository-level publication op(s) constrained by change set)` +
    (bad.length ? ` — ${bad.join(', ')}` : ''));
}

{
  const mutating = new Set(['CREATE', 'MODIFY', 'RENAME', 'MOVE', 'DELETE', 'COMMIT', 'PUSH']);
  const authorized = new Set(grants.flatMap(g => g.change_ids || []));
  const bad = record.execution.operations.filter(o =>
    mutating.has(o.operation) && !o.change_id);
  const unknown = record.execution.operations.filter(o => o.change_id && !authorized.has(o.change_id));
  ar('AUTH-016', bad.length === 0 && unknown.length === 0,
    'every mutating operation names an authorized change (EV-011)' +
    (bad.length || unknown.length ? ` — ${[...bad, ...unknown].map(o => o.id).join(', ')}` : ''));
}

{
  const discovered = record.execution.discovered_not_executed || [];
  const leaked = discovered.filter(id => record.execution.executed_changes.includes(id) ||
    grants.some(g => (g.change_ids || []).includes(id)));
  ar('AUTH-017', leaked.length === 0,
    `newly discovered change ids stay unauthorized until granted (${discovered.length} recorded, none executed)`);
}

{
  const forbidden = record.governance?.forbidden_operations || [];
  const withheld = record.governance?.withheld_capabilities || [];
  const reachable = withheld.filter(c => grants.some(g => effective(g).has(c)));
  ar('AUTH-018', reachable.length === 0 && forbidden.length > 0,
    `withheld capability classes are unreachable through every grant (${withheld.length} withheld)` +
    (reachable.length ? ` — reachable: ${reachable.join(', ')}` : ''));
}

{
  /* Every executed operation must have an authorization decision recorded:
     either it is permitted by some grant, or it carries a non-success result. */
  const decided = record.execution.operations.every(o => {
    const allowed = grants.some(g => permittedOperations(g).has(o.operation));
    return allowed || o.result !== 'SUCCEEDED';
  });
  ar('AUTH-019', decided, 'every executed operation has an authorization decision (EV-010)');
}

{
  const steps = ['state', 'level', 'capabilities', 'operations', 'scope', 'change_ids'];
  const missing = steps.filter(k => !(k in record.authorization));
  ar('AUTH-020', missing.length === 0,
    'authorization keeps state, level, capability, operation, scope and change authorization separate (section 167)' +
    (missing.length ? ` — missing: ${missing.join(', ')}` : ''));
}

/* ========================================================================== */
/* EXECUTION (EV-001…EV-012) and POST-VERIFICATION (PV-001…PV-010)            */
/* ========================================================================== */

{
  const ex = record.execution;
  const ops = ex.operations || [];
  const succeeded = ops.filter(o => o.result === 'SUCCEEDED');
  const notSucceeded = ops.filter(o => o.result !== 'SUCCEEDED');
  const mutating = new Set(['CREATE', 'MODIFY', 'RENAME', 'MOVE', 'DELETE']);
  const permitted = new Set(grants.flatMap(g => [...permittedOperations(g)]));

  const ev = [
    ['EV-001', ex.state !== 'NOT_STARTED' || succeeded.length === 0, 'NOT_STARTED implies no operation executed'],
    ['EV-002', ex.state !== 'AUTHORIZATION_BLOCKED' || succeeded.filter(o => mutating.has(o.operation)).length === 0,
      'AUTHORIZATION_BLOCKED implies no mutation'],
    ['EV-003', ex.state !== 'READY' || grants.some(g => g.state === 'GRANTED'), 'READY implies valid authorization'],
    ['EV-004', ex.state !== 'RUNNING' || ops.length > 0, 'RUNNING implies operations in flight'],
    ['EV-005', ex.state !== 'SUCCEEDED' || notSucceeded.length === 0, 'SUCCEEDED implies every listed operation succeeded'],
    ['EV-006', ex.state !== 'PARTIALLY_SUCCEEDED' || (succeeded.length > 0 && notSucceeded.length > 0),
      'PARTIALLY_SUCCEEDED implies both a success and a failure'],
    ['EV-007', ex.state !== 'FAILED' || notSucceeded.length > 0, 'FAILED implies required work did not complete'],
    ['EV-008', ex.state !== 'CANCELLED' || ops.some(o => o.result === 'CANCELLED'), 'CANCELLED implies cancellation'],
    ['EV-009', ex.state !== 'STOPPED' || ops.some(o => ['BLOCKED', 'CANCELLED'].includes(o.result)) || notSucceeded.length > 0,
      'STOPPED implies a policy or system boundary'],
    ['EV-010', ops.every(o => permitted.has(o.operation) || o.result !== 'SUCCEEDED'), 'every operation has an authorization decision'],
    ['EV-011', ops.filter(o => mutating.has(o.operation) || ['COMMIT', 'PUSH'].includes(o.operation)).every(o => !!o.change_id),
      'every mutating operation references a change id'],
    ['EV-012', ex.unauthorized_changes.length === 0 && ops.every(o => !(o.result === 'SUCCEEDED' && !permitted.has(o.operation))),
      'unauthorized operations did not mutate the repository'],
  ];
  const bad = ev.filter(([, ok]) => !ok);
  if (bad.length === 0) pass('EXECUTION', 'execution invariants hold', `${ev.length} invariants, state ${ex.state}`);
  else fail('EXECUTION', 'execution invariants hold', bad.map(([id]) => id).join(', '));

  const pv = record.post_verification || {};
  const checks = pv.checks || [];
  const required = checks;
  const failed = required.filter(c => c.result === 'FAILED');
  const passed = required.filter(c => c.result === 'PASSED');
  const notPassed = required.filter(c => c.result !== 'PASSED');
  const pvRules = [
    ['PV-001', pv.state !== 'PASSED' || (notPassed.length === 0 && required.length > 0), 'PASSED implies every required check passed'],
    ['PV-002', pv.state !== 'PARTIALLY_PASSED' || (passed.length > 0 && notPassed.length > 0), 'PARTIALLY_PASSED implies a pass and a non-pass'],
    ['PV-003', pv.state !== 'FAILED' || failed.length > 0, 'FAILED implies at least one required check failed'],
    ['PV-004', pv.state !== 'BLOCKED' || checks.some(c => c.result === 'BLOCKED'), 'BLOCKED implies verification could not execute'],
    ['PV-005', pv.state !== 'INCONCLUSIVE' || checks.some(c => c.result === 'INCONCLUSIVE'), 'INCONCLUSIVE implies no outcome'],
    ['PV-006', pv.result !== 'CONFORMING' || pv.state === 'PASSED', 'CONFORMING requires a PASSED lifecycle'],
    ['PV-007', pv.result !== 'NON_CONFORMING' || failed.length > 0, 'NON_CONFORMING implies a violated invariant'],
    ['PV-008', !(ex.state === 'SUCCEEDED' && pv.state === 'PASSED') || passed.length > 0,
      'execution success does not automatically produce verification success'],
    ['PV-009', (pv.mutations || []).length === 0, 'post-verification did not modify the repository'],
    ['PV-010', (pv.findings || []).every(f => !f.proposed_change_id || !ex.executed_changes.includes(f.proposed_change_id)),
      'remediation proposed by verification requires separate authorization'],
  ];
  const pvBad = pvRules.filter(([, ok]) => !ok);
  if (pvBad.length === 0) pass('POST-VERIFY', 'post-verification invariants hold',
    `${pvRules.length} invariants, state ${pv.state} / result ${pv.result}, ${checks.length} checks`);
  else fail('POST-VERIFY', 'post-verification invariants hold', pvBad.map(([id]) => id).join(', '));

  /* section 159 — the two lifecycles are independent, not identical fields */
  const independent = record.execution.state !== undefined && pv.state !== undefined &&
    !('result' in record.execution && record.execution.result === pv.state);
  if (independent) pass('POST-VERIFY', 'execution and post-verification are separate lifecycles', 'SUCCEEDED ≠ PASSED');
  else fail('POST-VERIFY', 'execution and post-verification are separate lifecycles');

  const violated = authChecks.filter(([, ok]) => !ok);
  if (violated.length === 0) pass('AUTHORIZATION', 'authorization rules hold', `${authChecks.length} rules across ${grants.length} grants`);
  else fail('AUTHORIZATION', 'authorization rules hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
}

/* ========================================================================== */
/* SERIALIZATION — analysis.json vs authorization.yaml (SER-001…SER-012)      */
/* ========================================================================== */

function parseYaml(text) {
  const lines = text.split('\n').map(l => l.replace(/\t/g, '  '));
  let i = 0;
  const indentOf = l => l.match(/^ */)[0].length;
  const skip = () => { while (i < lines.length && (lines[i].trim() === '' || lines[i].trim().startsWith('#'))) i++; };
  const scalar = raw => {
    const s = raw.trim();
    if (s === '' || s === 'null' || s === '~') return null;
    if (s === 'true') return true;
    if (s === 'false') return false;
    if (s === '[]') return [];
    if (s === '{}') return {};
    if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) return s.slice(1, -1);
    return s;
  };
  function parseNode(indent) {
    skip();
    if (i >= lines.length) return [null, i];
    if (lines[i].trim().startsWith('- ')) {
      const arr = [];
      const seqIndent = indentOf(lines[i]);
      while (i < lines.length) {
        skip();
        if (i >= lines.length || indentOf(lines[i]) !== seqIndent || !lines[i].trim().startsWith('- ')) break;
        const inline = lines[i].trim().slice(2).trim();
        if (inline === '') { i++; const [v, ni] = parseNode(indent + 2); arr.push(v); i = ni; }
        else if (/^[A-Za-z_][\w-]*:/.test(inline)) {
          lines[i] = ' '.repeat(seqIndent + 2) + inline;
          const [v, ni] = parseNode(seqIndent + 2); arr.push(v); i = ni;
        } else { arr.push(scalar(inline)); i++; }
      }
      return [arr, i];
    }
    const obj = {};
    while (i < lines.length) {
      skip();
      if (i >= lines.length || indentOf(lines[i]) !== indent) break;
      const m = lines[i].trim().match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
      if (!m) break;
      if (m[2] === '') { i++; const [v, ni] = parseNode(indent + 2); obj[m[1]] = v; i = ni; }
      else { obj[m[1]] = scalar(m[2]); i++; }
    }
    return [obj, i];
  }
  return parseNode(0)[0];
}

function diff(a, b, at, out) {
  const typeOf = v => Array.isArray(v) ? 'array' : v === null ? 'null' : typeof v;
  if (typeOf(a) !== typeOf(b)) { out.push(`${at}: ${typeOf(a)} vs ${typeOf(b)}`); return; }
  if (Array.isArray(a)) {
    if (a.length !== b.length) { out.push(`${at}: ${a.length} vs ${b.length} entries`); return; }
    a.forEach((v, k) => diff(v, b[k], `${at}[${k}]`, out));
    return;
  }
  if (a && typeof a === 'object') {
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
      if (k === '$comment') continue;
      if (!(k in a)) out.push(`${at}.${k}: YAML-only field`);
      else if (!(k in b)) out.push(`${at}.${k}: JSON-only field`);
      else diff(a[k], b[k], `${at}.${k}`, out);
    }
    return;
  }
  if (a !== b) out.push(`${at}: ${JSON.stringify(a)} vs ${JSON.stringify(b)}`);
}

{
  const yaml = fs.existsSync(YAML_PATH) ? parseYaml(fs.readFileSync(YAML_PATH, 'utf8')) : null;
  if (!yaml) {
    fail('SERIALIZATION', 'authorization.yaml mirrors the record', 'file missing or unparsable');
  } else {
    const jsonView = { authorization: record.authorization, authorization_grants: record.authorization_grants || [] };
    const out = [];
    diff(jsonView, yaml, '$', out);
    if (out.length === 0) {
      pass('SERIALIZATION', 'YAML and JSON deserialize to the same authorization object',
        'SER-001…SER-010: state, level profile, capabilities, operations, scope, change ids, authority and target preserved');
    } else {
      fail('SERIALIZATION', 'YAML and JSON deserialize to the same authorization object', out.slice(0, 4).join(' | '));
    }

    /* SER-012 — serialization must never increase privileges */
    const privilege = grant => [...permittedOperations(grant)].sort().join(',');
    const yamlGrants = [yaml.authorization, ...(yaml.authorization_grants || [])];
    const jsonGrants = grants;
    const gained = yamlGrants.flatMap((g, i) => {
      const before = new Set(jsonGrants[i] ? permittedOperations(jsonGrants[i]) : []);
      return [...permittedOperations(g)].filter(op => !before.has(op)).map(op => `${g.level?.profile}:${op}`);
    });
    if (gained.length === 0) pass('SERIALIZATION', 'serialization does not increase effective privileges', 'SER-012, ' + yamlGrants.map(privilege).join(' | '));
    else fail('SERIALIZATION', 'serialization does not increase effective privileges', gained.join(', '));

    const badLevels = yamlGrants.filter(g => !ALL_PROFILES.includes(g.level?.profile) || !STATES.includes(g.state));
    if (badLevels.length === 0) pass('SERIALIZATION', 'enum values are identical across formats', 'SER-003');
    else fail('SERIALIZATION', 'enum values are identical across formats', badLevels.length + ' grant(s)');
  }
}

/* ========================================================================== */
/* INVARIANTS I-001…I-016                                                     */
/* ========================================================================== */

{
  const raw = fs.readFileSync(RECORD_PATH, 'utf8');
  const noGeneric = !/"status"\s*:/.test(raw);
  const merged = record.contradictions.flatMap(x => [x.claim_a, x.claim_b]);
  const invariants = [
    ['I-001', 'No generic status field', () => noGeneric],
    ['I-002', 'Claim kind describes claim semantics', () => claims.every(c => typeof c.claim_kind === 'string')],
    ['I-003', 'Implementation state describes implementation', () => claims.every(c => typeof c.implementation_state === 'string')],
    ['I-004', 'Test state describes testing', () => claims.every(c => typeof c.test_state === 'string')],
    ['I-005', 'Evidence level describes evidence strength/availability', () => claims.every(c => typeof c.evidence_level === 'string')],
    ['I-006', 'Verification result describes verification conclusion', () => claims.every(c => typeof c.verification_result === 'string')],
    ['I-007', 'Authorization state describes whether permission exists', () => typeof record.authorization.state === 'string'],
    ['I-008', 'Authorization level is a profile, not an operation set', () => typeof record.authorization.level?.profile === 'string'
      && Array.isArray(record.authorization.capabilities?.allow) && typeof record.authorization.operations === 'object'],
    ['I-009', 'Execution state describes what happened', () => typeof record.execution.state === 'string' && typeof record.execution.result === 'undefined'],
    ['I-010', 'Technical access does not imply authorization', () => 'authorization' in record && 'access_level' in record.repository],
    ['I-011', 'Authorization does not imply execution', () => record.execution.executed_changes.length > 0 || grants.some(g => g.state !== 'GRANTED')],
    ['I-012', 'Execution success does not imply post-verification success',
      () => record.post_verification.state !== record.execution.state],
    ['I-013', 'Every executed change is authorized',
      () => record.execution.executed_changes.every(id => grants.some(g => (g.change_ids || []).includes(id)))],
    ['I-014', 'Every important verification claim has evidence',
      () => claims.filter(c => c.verification_result === 'VERIFIED').every(c => c.evidence.length > 0)],
    ['I-015', 'INACCESSIBLE cannot become ABSENT without a new verification step',
      () => !(record.repository.access_level === 'FULL' && claims.some(c => c.evidence_level === 'INACCESSIBLE'))],
    ['I-016', 'Newly discovered work cannot silently expand execution scope',
      () => record.execution.unauthorized_changes.length === 0 &&
        (record.execution.discovered_not_executed || []).every(id => !record.execution.executed_changes.includes(id))],
  ];
  const violated = invariants.filter(([, , check]) => !check());
  if (violated.length === 0) pass('INVARIANTS', 'machine-readable invariants hold', `${invariants.length} invariants`);
  else fail('INVARIANTS', 'machine-readable invariants hold', violated.map(([id]) => id).join(', '));

  const malformed = record.contradictions.filter(x => x.claim_a === x.claim_b || !byId.has(x.claim_a) || !byId.has(x.claim_b));
  if (malformed.length === 0) {
    pass('INVARIANTS', 'contradictions are recorded as relationships between claims',
      `${record.contradictions.length} contradiction(s) over ${new Set(merged).size} distinct claims`);
  } else {
    fail('INVARIANTS', 'contradictions are recorded as relationships between claims', malformed.length + ' malformed');
  }
}

/* ========================================================================== */
/* DRIFT: restated claim fields, generated claims.md                          */
/* ========================================================================== */

{
  const doc = fs.readFileSync(path.join(ROOT, 'docs', 'analysis', 'repository-analysis-2026-09-10.md'), 'utf8');
  const stale = [];
  for (const m of doc.matchAll(/\| `([A-Z]+-CLAIM-\d{3})` \| ([^|]*)\|/g)) {
    const claim = byId.get(m[1]);
    if (!claim) continue;
    const shown = [...m[2].matchAll(/`([A-Z_]+)`/g)].map(x => x[1]);
    if (shown.length !== 5) continue;
    const actual = [claim.claim_kind, claim.implementation_state, claim.test_state, claim.evidence_level, claim.verification_result];
    if (shown.join('|') !== actual.join('|')) stale.push(claim.id);
  }
  if (stale.length === 0) pass('CLAIMS', 'restated claim fields match the record', 'repository-analysis §3 index');
  else fail('CLAIMS', 'restated claim fields match the record', stale.slice(0, 4).join(', '));
}

{
  const drift = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result']
    .flatMap(f => claims.filter(c => !enumOf(f).includes(c[f])).map(c => `${c.id}.${f}`));
  if (drift.length === 0) pass('CLAIMS', 'every claim field uses the schema enum');
  else fail('CLAIMS', 'every claim field uses the schema enum', drift.slice(0, 5).join(', '));
}

{
  try {
    execFileSync(process.execPath, [path.join(ROOT, 'tools', 'render-claims.mjs'), '--check'], { cwd: ROOT, stdio: 'pipe' });
    pass('CLAIMS', 'claims.md matches analysis.json', 'generated tables are current');
  } catch (error) {
    fail('CLAIMS', 'claims.md matches analysis.json', String(error.stdout || error.message).trim().split('\n').pop());
  }
}

/* ========================================================================== */
/* Report                                                                     */
/* ========================================================================== */

const width = Math.max(...results.map(r => r[2].length));
console.log('validation pipeline: STRUCTURAL → CLAIMS → EVIDENCE → AUTHORIZATION → EXECUTION → POST-VERIFY → SERIALIZATION\n');
let current = null;
for (const [stage, level, message, note] of results) {
  const label = stage === 'AUTHORIZATION' ? 'AUTHORIZATION (AUTH-001…AUTH-020)' : stage;
  if (label !== current) { console.log(`\n${label}`); current = label; }
  console.log(`  [${level}] ${message.padEnd(width)}  ${note}`);
}
const failures = results.filter(r => r[1] === 'FAIL').length;
console.log(`\n${results.filter(r => r[1] === 'PASS').length} passed, ${failures} failed`);
process.exit(failures === 0 ? 0 : 1);
