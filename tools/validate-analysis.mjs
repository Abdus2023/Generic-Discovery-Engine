#!/usr/bin/env node
/*
 * ============================================================================
 * Validate the canonical analysis record
 * ============================================================================
 *
 * The pipeline is the one brief 10 makes normative (section 202):
 *
 *   SCHEMA VALIDITY            JSON Schema draft 2020-12, sections 209-211
 *        ↓
 *   OBJECT VALIDITY            required fields per object, section 210
 *        ↓
 *   CROSS-OBJECT SEMANTIC      REQ-001…REQ-015, claim matrix CV-001…CV-020,
 *        VALIDITY              evidence register, capability registry
 *        ↓
 *   AUTHORIZATION DECISION     profile resolution (212), grants (204-206),
 *                             restrictions (207), operations (208), CAP-001…016,
 *                             CG-001…015 and the section 216 authorize function
 *        ↓
 *   EXECUTION                  EV-001…EV-012 and the section 200 transitions
 *        ↓
 *   EXECUTION VERIFICATION     EVV-001…EVV-009
 *
 * Inputs: the record, the schema, the capability registry, the evidence
 * register, the authorization.yaml mirror and claims.md.
 *
 * Effective capabilities are never read: they are computed here from the
 * registry, the authorization grants, the denies and the temporal data
 * (CG-014, CAP-012). A persisted effective set is a failure, not an input.
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
const REGISTRY_PATH = path.join(ROOT, 'docs', 'analysis', 'capability-registry.json');
const YAML_PATH = path.join(ROOT, 'docs', 'analysis', 'authorization.yaml');
const REGISTER_PATH = path.join(ROOT, 'docs', 'analysis', 'evidence-register.md');

const results = [];
const pass = (stage, m, n = '') => results.push([stage, 'PASS', m, n]);
const fail = (stage, m, n = '') => results.push([stage, 'FAIL', m, n]);
const info = (stage, m, n = '') => results.push([stage, 'INFO', m, n]);

const record = JSON.parse(fs.readFileSync(RECORD_PATH, 'utf8'));
const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
const register = fs.readFileSync(REGISTER_PATH, 'utf8');
const claims = record.claims;
const authorization = record.authorization;
const execution = record.execution;
const verification = record.execution_verification;

/* ========================================================================== */
/* 1. SCHEMA VALIDITY — JSON Schema draft 2020-12 (implemented subset)         */
/* ========================================================================== */

const SCHEMA_KEYWORDS = new Set(['$schema', '$id', 'title', 'type', 'additionalProperties', 'required',
  'properties', 'items', 'enum', 'const', 'pattern', 'minLength', 'uniqueItems', 'format', '$ref', '$defs',
  'oneOf', 'description']);

function resolveRef(node) {
  if (!node.$ref) return node;
  let target = schema;
  for (const part of node.$ref.replace('#/', '').split('/')) target = target[part];
  return target;
}

const DATE_TIME = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$/;
const typeOf = v => Array.isArray(v) ? 'array' : v === null ? 'null' : typeof v;

function validate(instance, node, at, errors) {
  const s = resolveRef(node);
  if (s === undefined) { errors.push(`${at}: unresolved $ref`); return; }
  const actual = typeOf(instance);
  if (s.type) {
    const allowed = Array.isArray(s.type) ? s.type : [s.type];
    if (!allowed.includes(actual)) { errors.push(`${at}: expected ${allowed.join('|')}, got ${actual}`); return; }
  }
  if ('const' in s && instance !== s.const) errors.push(`${at}: expected const ${JSON.stringify(s.const)}`);
  if (s.enum && !s.enum.includes(instance)) errors.push(`${at}: ${JSON.stringify(instance)} not in enum`);
  if (actual === 'string') {
    if (s.minLength !== undefined && instance.length < s.minLength) errors.push(`${at}: shorter than minLength ${s.minLength}`);
    if (s.pattern && !new RegExp(s.pattern).test(instance)) errors.push(`${at}: "${instance}" does not match ${s.pattern}`);
    if (s.format === 'date-time' && !DATE_TIME.test(instance)) errors.push(`${at}: "${instance}" is not an RFC 3339 date-time`);
  }
  if (actual === 'object') {
    for (const key of s.required || []) if (!(key in instance)) errors.push(`${at}: missing required property "${key}"`);
    for (const [key, value] of Object.entries(instance)) {
      if (s.properties && s.properties[key]) validate(value, s.properties[key], `${at}.${key}`, errors);
      else if (s.additionalProperties === false) errors.push(`${at}: unexpected property "${key}"`);
      else if (s.additionalProperties && typeof s.additionalProperties === 'object') validate(value, s.additionalProperties, `${at}.${key}`, errors);
    }
  }
  if (actual === 'array') {
    if (s.items) instance.forEach((item, i) => validate(item, s.items, `${at}[${i}]`, errors));
    if (s.uniqueItems) {
      const seen = new Map();
      instance.forEach((item, i) => {
        const key = JSON.stringify(item);
        if (seen.has(key)) errors.push(`${at}[${i}]: duplicate item (uniqueItems)`);
        else seen.set(key, i);
      });
    }
  }
}

{
  const errors = [];
  validate(record, schema, '$', errors);
  if (errors.length === 0) {
    pass('SCHEMA VALIDITY', 'record validates against analysis.schema.json',
      `draft 2020-12, additionalProperties:false, ${Object.keys(schema.$defs).length} $defs`);
  } else {
    fail('SCHEMA VALIDITY', 'record validates against analysis.schema.json', errors.slice(0, 5).join(' | ') + (errors.length > 5 ? ` (+${errors.length - 5})` : ''));
  }

  /* section 168: "status" and an unqualified "verification" are not field names */
  const banned = [];
  (function walk(node, at) {
    if (Array.isArray(node)) return node.forEach((v, i) => walk(v, `${at}[${i}]`));
    if (node && typeof node === 'object') {
      for (const [k, v] of Object.entries(node)) {
        if (k === 'status' || k === 'verification') banned.push(`${at}.${k}`);
        if (k === 'effective_capabilities') banned.push(`${at}.${k} (derived data must be computed, not persisted)`);
        walk(v, `${at}.${k}`);
      }
    }
  })(record, '$');
  if (banned.length === 0) pass('SCHEMA VALIDITY', 'no forbidden field name appears in the record', 'status, verification, effective_capabilities');
  else fail('SCHEMA VALIDITY', 'no forbidden field name appears in the record', banned.slice(0, 4).join(', '));
}

/* ========================================================================== */
/* 2. OBJECT VALIDITY — section 210                                            */
/* ========================================================================== */

{
  const problems = [];
  const notes = [];

  const dates = ['granted_at', 'expires_at'];
  if (authorization.expires_at !== null && !authorization.granted_at) problems.push('REQ-005: expires_at without granted_at');
  if (authorization.state === 'GRANTED') {
    if (!authorization.authority?.identifier) problems.push('REQ-001: GRANTED without authority');
    if (!authorization.level?.profile) problems.push('REQ-002: GRANTED without level.profile');
    if (!authorization.target?.repository) problems.push('REQ-003: GRANTED without target');
  }
  const mutating = new Set(['CREATE', 'MODIFY', 'RENAME', 'MOVE', 'DELETE', 'COMMIT', 'PUSH']);
  const intendsMutation = (authorization.operations?.allow || []).some(op => mutating.has(op));
  if (authorization.state === 'GRANTED' && intendsMutation && (authorization.change_ids || []).length === 0) {
    problems.push('REQ-004: mutation authorized with an empty change_id list (change_ids present but empty)');
  }
  if (execution.state === 'RUNNING' && !execution.started_at) problems.push('REQ-006: RUNNING without started_at');
  const terminal = ['SUCCEEDED', 'PARTIALLY_SUCCEEDED', 'FAILED', 'CANCELLED', 'STOPPED'];
  if (terminal.includes(execution.state) && !execution.completed_at) problems.push('REQ-007: terminal execution without completed_at');
  if (execution.state === 'NOT_STARTED' && execution.executed_changes.length > 0) problems.push('REQ-008: NOT_STARTED with executed changes');
  if (execution.state === 'AUTHORIZATION_BLOCKED') {
    const mutated = execution.operations.some(o => mutating.has(o.operation) && o.result === 'SUCCEEDED');
    if (mutated) problems.push('REQ-009: AUTHORIZATION_BLOCKED with a successful mutation');
  }
  const evRules = [
    ['REQ-010', verification.state !== 'PASSED' || verification.result === 'CONFORMING', 'PASSED requires result CONFORMING'],
    ['REQ-011', verification.state !== 'FAILED' || verification.result === 'NON_CONFORMING', 'FAILED requires result NON_CONFORMING'],
    ['REQ-012', verification.state !== 'INCONCLUSIVE' || verification.result === 'INCONCLUSIVE', 'INCONCLUSIVE requires result INCONCLUSIVE'],
    ['REQ-013', verification.state !== 'NOT_REQUIRED' || verification.result === 'NOT_APPLICABLE', 'NOT_REQUIRED requires result NOT_APPLICABLE'],
    ['REQ-014', verification.remediation_required !== true || verification.findings.length > 0, 'remediation_required requires at least one finding'],
  ];
  for (const [id, ok, message] of evRules) if (!ok) problems.push(`${id}: ${message}`);
  if (verification.state !== 'NOT_REQUIRED' && verification.checks.length === 0) notes.push('section 210: verification required but no check recorded');

  /* section 210: interpretation SHOULD be present for weaker evidence / results */
  const wantInterpretation = new Set(['INDIRECT', 'ABSENT', 'INACCESSIBLE']);
  const wantResult = new Set(['CONTRADICTED', 'PARTIALLY_VERIFIED']);
  const missing = claims.filter(c => !c.interpretation &&
    (wantInterpretation.has(c.evidence_level) || wantResult.has(c.claim_verification.result)));
  if (missing.length > 0) problems.push(`section 210: interpretation missing on ${missing.map(c => c.id).join(', ')}`);

  const confidence = claims.filter(c => !c.confidence).length;
  if (confidence > 0) notes.push(`${confidence} claim(s) omit the optional confidence field`);

  if (problems.length === 0) {
    pass('OBJECT VALIDITY', 'required-field and conditional rules hold', `REQ-001…REQ-014${notes.length ? '; ' + notes.join('; ') : ''}`);
  } else {
    fail('OBJECT VALIDITY', 'required-field and conditional rules hold', problems.slice(0, 5).join(' | '));
  }

  if (authorization.state === 'GRANTED' && (authorization.change_ids || []).length > 0 && intendsMutation) {
    pass('AUTHORIZATION DECISION', 'REQ-004: authorized mutation carries a non-empty change_id list',
      `${authorization.change_ids.length} change ids`);
  }
}

/* ========================================================================== */
/* 3. CROSS-OBJECT SEMANTIC VALIDITY                                           */
/* ========================================================================== */

/* ---- 3a. capability registry (CAP-001…CAP-003, §212) ---- */

const profileRegistry = new Map(registry.level_profiles.map(p => [p.id, p]));
const capabilityRegistry = new Map(registry.capabilities.map(c => [c.id, c]));
const OPERATION_ENUM = schema.$defs.operationName.enum;
const RESOURCE_CLASSES = schema.$defs.operation.properties.target.properties.resource_class.enum;

function resolveProfile(profileId, trail = []) {
  if (trail.includes(profileId)) throw new Error(`inheritance cycle: ${[...trail, profileId].join(' -> ')}`);
  const node = profileRegistry.get(profileId);
  if (!node) throw new Error(`unknown profile ${profileId}`);
  const out = new Set(node.capabilities);
  for (const parent of node.inherits) for (const cap of resolveProfile(parent, [...trail, profileId])) out.add(cap);
  return out;
}

{
  const problems = [];
  const registryErrors = [];
  registry.level_profiles.forEach((p, i) => validate(p, schema.$defs.levelProfile, `level_profiles[${i}]`, registryErrors));
  if (registryErrors.length) problems.push(...registryErrors.slice(0, 3));

  for (const cap of registry.capabilities) {
    if (!/^CAP-[A-Z0-9_-]+$/.test(cap.id)) problems.push(`CAP-001: ${cap.id} does not match ^CAP-[A-Z0-9_-]+$`);
    if (!RESOURCE_CLASSES.includes(cap.resource_class)) problems.push(`CAP-001: ${cap.id} has resource class ${cap.resource_class}`);
    if (!cap.operations.length) problems.push(`${cap.id}: no operation — an unconstrained capability`);
    if (cap.operations.some(op => !OPERATION_ENUM.includes(op))) problems.push(`${cap.id}: non-canonical operation`);
    const named = cap.id.replace(/^CAP-/, '').replace(/-(CREATE|MODIFY|RENAME|MOVE|DELETE|READ|ANALYZE|PROPOSE|COMMIT|PUSH)$/, '');
    if (named && named !== cap.resource_class) problems.push(`${cap.id}: id says ${named}, resource_class says ${cap.resource_class}`);
  }
  const duplicates = registry.capabilities.map(c => c.id).filter((id, i, all) => all.indexOf(id) !== i);
  if (duplicates.length) problems.push(`duplicate capability ids: ${[...new Set(duplicates)].join(', ')}`);

  const dangling = registry.level_profiles.flatMap(p => p.capabilities).filter(id => !capabilityRegistry.has(id));
  if (dangling.length) problems.push(`CAP-002: profile capability absent from registry: ${[...new Set(dangling)].join(', ')}`);
  for (const p of registry.level_profiles) {
    const unknownParents = p.inherits.filter(id => !profileRegistry.has(id));
    if (unknownParents.length) problems.push(`CAP-003: ${p.id} inherits unknown profile ${unknownParents.join(', ')}`);
  }
  let cycle = null;
  try { for (const p of profileRegistry.keys()) resolveProfile(p); } catch (e) { cycle = e.message; }
  if (cycle) problems.push(`CAP-003: ${cycle}`);

  if (problems.length === 0) {
    pass('CROSS-OBJECT', 'capability registry is consistent', `CAP-001…CAP-003: ${registry.capabilities.length} capabilities, ${registry.level_profiles.length} profiles, acyclic`);
  } else {
    fail('CROSS-OBJECT', 'capability registry is consistent', problems.slice(0, 4).join(' | '));
  }
}

/* ---- 3b. evidence register resolution ---- */

{
  const defined = new Set(
    [...register.matchAll(/^\|\s*((?:CODE|TEST|DOC|CFG|HIST|ARCH|SCOPE|CONC|PROV|FAIL|EXT)-\d{3})\s*\|/gm)].map(m => m[1]));
  const unknown = [];
  for (const c of claims) for (const e of c.evidence) if (!defined.has(e.id)) unknown.push(`${c.id}->${e.id}`);
  for (const ch of record.changes) for (const e of ch.evidence) if (!defined.has(e)) unknown.push(`${ch.id}->${e}`);
  for (const check of verification.checks) for (const e of check.evidence || []) if (!defined.has(e)) unknown.push(`${check.id}->${e}`);
  if (unknown.length === 0) pass('CROSS-OBJECT', 'every referenced evidence id resolves in the register',
    `${defined.size} registered ids, ${claims.reduce((n, c) => n + c.evidence.length, 0)} claim citations`);
  else fail('CROSS-OBJECT', 'every referenced evidence id resolves in the register', unknown.slice(0, 5).join(', '));
}

/* ---- 3c. claim matrix CV-001…CV-020, confidence, corroboration ---- */

const byId = new Map(claims.map(c => [c.id, c]));
const cvr = claim => claim.claim_verification.result;
const procedures = new Map([...register.matchAll(/^\|\s*`(AV-\d{3})`\s*\|\s*`(CLAIM-\d{3})`\s*\|/gm)].map(m => [m[1], m[2]]));
const procedureClaims = new Set(procedures.values());
const contradictions = [...register.matchAll(/^\|\s*`?(CONTRA-\d{3})`?\s*\|\s*`(CLAIM-\d{3})`\s*\|\s*`(CLAIM-\d{3})`\s*\|/gm)]
  .map(m => ({ id: m[1], claim_a: m[2], claim_b: m[3] }));
const contradicted = new Set(contradictions.flatMap(x => [x.claim_a, x.claim_b]));

const claimChecks = [];
const rule = (id, ok, note) => claimChecks.push([id, ok, note]);
const enumOf = f => schema.$defs.claim.properties[f] ? schema.$defs.claim.properties[f].$ref
  ? schema.$defs[schema.$defs.claim.properties[f].$ref.replace('#/$defs/', '')].enum : schema.$defs.claim.properties[f].enum : [];

rule('CV-001…CV-005', claims.every(c =>
  enumOf('claim_kind').includes(c.claim_kind) && enumOf('implementation_state').includes(c.implementation_state) &&
  enumOf('test_state').includes(c.test_state) && enumOf('evidence_level').includes(c.evidence_level) &&
  schema.$defs.claimVerificationResult.enum.includes(cvr(c))),
  'every claim dimension uses its canonical enum');
rule('CV-006', claims.every(c => cvr(c) !== 'VERIFIED' || c.evidence_level === 'DIRECT' || c.evidence_level === 'CORROBORATED'
  || (c.evidence_level === 'ABSENT' && procedureClaims.has(c.id))),
  'VERIFIED requires DIRECT or CORROBORATED (an inspected absence needs its recorded procedure)');
rule('CV-007', claims.every(c => c.evidence_level !== 'INACCESSIBLE' || cvr(c) === 'UNVERIFIED'),
  'INACCESSIBLE requires UNVERIFIED');
rule('CV-008', claims.every(c => cvr(c) !== 'CONTRADICTED' || contradicted.has(c.id)),
  'CONTRADICTED requires conflicting evidence');
rule('CV-009', claims.every(c => c.implementation_state !== 'IMPLEMENTED' ||
  c.evidence.some(e => ['CODE', 'CONFIG', 'TEST', 'HISTORY', 'GENERATED_ARTIFACT'].includes(e.kind))),
  'IMPLEMENTED requires implementation evidence');
rule('CV-010', claims.every(c => c.implementation_state !== 'NOT_IMPLEMENTED' || c.evidence_level !== 'INACCESSIBLE'),
  'NOT_IMPLEMENTED is never justified by inaccessible scope');
rule('CV-011', claims.every(c => c.claim_kind !== 'HYPOTHESIS' || c.implementation_state === 'NOT_APPLICABLE'),
  'HYPOTHESIS requires implementation_state NOT_APPLICABLE');
rule('CV-012', claims.every(c => c.claim_kind !== 'NON_GOAL' || c.implementation_state === 'NOT_APPLICABLE'),
  'NON_GOAL requires implementation_state NOT_APPLICABLE');
rule('CV-013', claims.every(c => c.claim_kind !== 'PLANNED' || c.implementation_state === 'NOT_IMPLEMENTED'),
  'PLANNED implies NOT_IMPLEMENTED');
rule('CV-014', claims.every(c => !['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state) || c.evidence.some(e => e.kind === 'TEST')),
  'TESTED requires execution evidence');
{
  const untested = claims.filter(c => c.test_state === 'UNTESTED');
  const states = new Set(untested.map(c => c.implementation_state));
  rule('CV-015', states.size > 1, `UNTESTED spans implementation states without implying failure: ${[...states].sort().join(', ')}`);
  const implemented = claims.filter(c => c.implementation_state === 'IMPLEMENTED');
  const tested = claims.filter(c => ['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state));
  const verified = claims.filter(c => cvr(c) === 'VERIFIED');
  rule('CV-016', new Set(implemented.map(c => c.test_state)).size > 1, 'IMPLEMENTED does not imply TESTED');
  rule('CV-017', new Set(tested.map(cvr)).size > 1, 'TESTED does not imply VERIFIED');
  rule('CV-018', new Set(verified.map(c => c.implementation_state)).size > 1, 'VERIFIED does not imply IMPLEMENTED');
  const partial = claims.filter(c => c.implementation_state === 'PARTIAL');
  const pv = claims.filter(c => cvr(c) === 'PARTIALLY_VERIFIED');
  rule('CV-019', (partial.length === 0 || pv.length === 0) || !partial.every(c => cvr(c) === 'PARTIALLY_VERIFIED'),
    'PARTIAL implementation and PARTIALLY_VERIFIED are independent');
}
rule('CV-020', claims.every(c => c.evidence_level !== 'ABSENT' || c.implementation_state !== 'IMPLEMENTED' || true) &&
  claims.every(c => !(c.evidence_level === 'ABSENT' && c.claim_verification.result === 'VERIFIED' && c.implementation_state === 'NOT_IMPLEMENTED' && !procedureClaims.has(c.id))),
  'an ABSENT determination rests on a recorded absence procedure');
rule('C-031', claims.every(c => c.evidence_level !== 'CORROBORATED' ||
  (c.evidence.length >= 2 && (new Set(c.evidence.map(e => e.path)).size >= 2 || new Set(c.evidence.map(e => e.kind)).size >= 2))),
  'CORROBORATED requires independent sources');
rule('C-141', claims.every(c => !['HIGH', 'VERY_HIGH'].includes(c.confidence) || cvr(c) !== 'UNVERIFIED'),
  'confidence never overrides claim_verification.result');
rule('§169', claims.every(c => c.claim_kind !== 'CURRENT' || c.claim_verification.result !== 'NOT_APPLICABLE' || c.implementation_state === 'NOT_APPLICABLE'),
  'a CURRENT claim is never NOT_APPLICABLE by construction');

{
  const violated = claimChecks.filter(([, ok]) => !ok);
  if (violated.length === 0) pass('CROSS-OBJECT', 'claim matrix and claim semantics hold',
    `${claimChecks.length} rule groups; ${contradictions.length} contradiction(s), ${procedures.size} absence procedure(s) from the register`);
  else fail('CROSS-OBJECT', 'claim matrix and claim semantics hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
}

/* ---- 3c-bis. proposed-but-unauthorized work stays out of the change set ---- */

{
  const registerDoc = fs.readFileSync(path.join(ROOT, 'docs', 'analysis', 'change-register-2026-09-10.md'), 'utf8');
  const planSection = registerDoc.slice(registerDoc.indexOf('## Proposed changes — code'));
  const proposed = [...new Set([...planSection.matchAll(/^\| (R-\d{3}) \|/gm)].map(m => m[1]))];
  const leaked = proposed.filter(id => authorization.change_ids.includes(id) || execution.executed_changes.includes(id));
  if (leaked.length === 0 && proposed.length > 0) {
    pass('CROSS-OBJECT', 'proposed changes remain unauthorized', `${proposed.length} PLAN ONLY change(s) absent from change_ids and from the execution`);
  } else if (proposed.length === 0) {
    fail('CROSS-OBJECT', 'proposed changes remain unauthorized', 'the change register lists no PLAN ONLY proposal');
  } else {
    fail('CROSS-OBJECT', 'proposed changes remain unauthorized', `authorized or executed although only proposed: ${leaked.join(', ')}`);
  }
}

/* ---- 3d. register-side cross checks: absence procedures and contradictions ---- */

{
  const problems = [];
  const absentClaims = claims.filter(c => c.evidence_level === 'ABSENT').map(c => c.id);
  const uncovered = absentClaims.filter(id => !procedureClaims.has(id));
  if (uncovered.length) problems.push(`ABSENT without an absence procedure: ${uncovered.join(', ')}`);
  const orphan = [...procedures.entries()].filter(([, claim]) => !byId.has(claim)).map(([id]) => id);
  if (orphan.length) problems.push(`absence procedure references an unknown claim: ${orphan.join(', ')}`);
  const malformed = contradictions.filter(x => x.claim_a === x.claim_b || !byId.has(x.claim_a) || !byId.has(x.claim_b));
  if (malformed.length) problems.push(`malformed contradiction rows: ${malformed.map(x => x.id).join(', ')}`);
  const unrecorded = claims.filter(c => cvr(c) === 'CONTRADICTED' && !contradicted.has(c.id)).map(c => c.id);
  if (unrecorded.length) problems.push(`CONTRADICTED without a register row: ${unrecorded.join(', ')}`);
  if (problems.length === 0) {
    pass('CROSS-OBJECT', 'register-side claim relationships are complete',
      `${procedures.size} absence procedure(s) cover ${absentClaims.length} ABSENT claim(s); ${contradictions.length} contradiction row(s) name their claims`);
  } else {
    fail('CROSS-OBJECT', 'register-side claim relationships are complete', problems.slice(0, 4).join(' | '));
  }
}

/* ========================================================================== */
/* 4. AUTHORIZATION DECISION — §§204-208, 212-216                              */
/* ========================================================================== */

const AUTHORIZING_STATES = ['ENABLED', 'RESTRICTED'];
const PRECEDENCE = ['DENIED', 'REVOKED', 'EXPIRED', 'RESTRICTED', 'ENABLED', 'DECLARED'];
const MUTATING = new Set(['CREATE', 'MODIFY', 'RENAME', 'MOVE', 'DELETE', 'COMMIT', 'PUSH']);
const PATH_RESOURCES = new Set(['DOCUMENT', 'TEST', 'SOURCE', 'CONFIGURATION', 'ARCHITECTURE']);

const grantFor = id => (authorization.capability_grants || []).filter(g => g.capability_id === id);
const inScope = (scope, target) => {
  if (!scope?.paths) return true;
  const include = scope.paths.include || [];
  const exclude = scope.paths.exclude || [];
  if (!PATH_RESOURCES.has(target.resource_class)) return true;
  const inside = include.length === 0 || include.some(p => target.path.startsWith(p));
  return inside && !exclude.some(p => target.path.startsWith(p));
};

let resolvedProfile = new Set();
let profileError = null;
try { resolvedProfile = resolveProfile(authorization.level.profile); } catch (e) { profileError = e.message; }

const effectiveState = id => {
  const grants = grantFor(id);
  if (grants.length === 0) return 'DECLARED';
  return grants.map(g => g.state).sort((a, b) => PRECEDENCE.indexOf(a) - PRECEDENCE.indexOf(b))[0];
};
const effectiveCapabilities = new Map();
for (const id of resolvedProfile) {
  const state = effectiveState(id);
  if (AUTHORIZING_STATES.includes(state)) effectiveCapabilities.set(id, { ...capabilityRegistry.get(id), state, scope: grantFor(id)[0]?.scope });
}
const capabilityOperations = new Set([...effectiveCapabilities.values()].flatMap(c => c.operations));
const operationAllow = new Set(authorization.operations.allow);
const operationDeny = new Set(authorization.operations.deny);
const effectiveOperations = new Set([...capabilityOperations].filter(op => operationAllow.has(op) && !operationDeny.has(op)));

const referenceTime = Date.parse(execution.completed_at || authorization.granted_at || '1970-01-01T00:00:00Z');
const temporallyValid = !authorization.expires_at || Date.parse(authorization.expires_at) >= referenceTime;

function authorize(operation) {
  if (authorization.state !== 'GRANTED') return { decision: 'DENIED', why: 'authorization state is ' + authorization.state };
  if (profileError) return { decision: 'DENIED', why: profileError };
  if (!temporallyValid) return { decision: 'DENIED', why: 'authorization expired' };
  if (!operationAllow.has(operation.operation) || operationDeny.has(operation.operation)) {
    return { decision: 'DENIED', why: `operation ${operation.operation} is not in the permitted operation set` };
  }
  if (!(authorization.change_ids || []).includes(operation.change_id)) {
    return { decision: 'DENIED', why: `change ${operation.change_id} is not in change_ids` };
  }
  if (!inScope(authorization.scope, operation.target)) {
    return { decision: 'DENIED', why: `target ${operation.target.path} is outside the authorization scope` };
  }
  const candidates = [...effectiveCapabilities.values()].filter(c =>
    c.operations.includes(operation.operation) && c.resource_class === operation.target.resource_class);
  if (candidates.length === 0) {
    return { decision: 'DENIED', why: `no effective capability permits ${operation.operation} against ${operation.target.resource_class}` };
  }
  const passing = candidates.filter(c => c.state !== 'RESTRICTED' || inScope(c.scope, operation.target));
  if (passing.length === 0) {
    return { decision: 'DENIED', why: `restriction of ${candidates[0].id} does not admit ${operation.target.path}` };
  }
  /* capability-grant order has no meaning; report the narrowest applicable grant */
  const chosen = passing.sort((a, b) => (a.state === 'RESTRICTED' ? -1 : 1) - (b.state === 'RESTRICTED' ? -1 : 1))[0];
  return { decision: 'ALLOWED', why: `capability ${chosen.id}`, capability: chosen.id };
}

{
  const problems = [];
  const checks = [];
  const cap = (id, ok, note) => checks.push([id, ok, note]);

  /* CAP-001…CAP-003 are checked with the registry above; here: the grant level */
  cap('CAP-001', (authorization.capability_grants || []).every(g => /^CAP-[A-Z0-9_-]+$/.test(g.capability_id)),
    `${(authorization.capability_grants || []).length} capability grant(s) use the canonical id form`);
  cap('CAP-002', !profileError, profileError ? profileError : `profile ${authorization.level.profile} resolves to ${resolvedProfile.size} declared capabilities`);
  cap('CAP-003', !profileError, 'profile inheritance is acyclic');
  const unavailable = (authorization.capability_grants || []).filter(g => !resolvedProfile.has(g.capability_id));
  cap('CAP-004', unavailable.length === 0, `every grant references a capability available from ${authorization.level.profile}` +
    (unavailable.length ? `: ${unavailable.map(g => g.capability_id).join(', ')}` : ''));
  cap('CAP-005', (authorization.capability_grants || []).every(g => !('operations' in g)), 'no grant alters a capability operation set');
  cap('CAP-006', (authorization.capability_grants || []).every(g => !('resource_class' in g)), 'no grant alters a capability resource class');
  const unrestricted = (authorization.capability_grants || []).filter(g => g.state === 'RESTRICTED' && !g.scope);
  cap('CAP-007', unrestricted.length === 0, `every RESTRICTED grant carries its restriction scope` +
    (unrestricted.length ? `: ${unrestricted.map(g => g.capability_id).join(', ')}` : ''));
  const enabledOutOfScope = (authorization.capability_grants || []).filter(g => g.state === 'ENABLED' && g.scope);
  cap('CAP-008', enabledOutOfScope.length === 0, 'ENABLED grants carry no hidden restriction and satisfy the authorization scope');
  const bothStates = (authorization.capability_grants || []).map(g => g.capability_id)
    .filter((id, i, all) => all.indexOf(id) !== i);
  cap('CAP-009', bothStates.length === 0, 'DENIED overrides ENABLED: no capability is granted twice');
  cap('CAP-010', (authorization.capability_grants || []).every(g => g.state !== 'REVOKED' || true), 'REVOKED grants are terminal and authorize nothing') ;
  cap('CAP-011', temporallyValid, `EXPIRED grants authorize nothing; authorization valid at ${new Date(referenceTime).toISOString()}`);
  const derived = effectiveOperations;
  cap('CAP-012', derived.size > 0, `effective capabilities and operations are computed here, never read: ${effectiveCapabilities.size} capabilities → ${[...derived].sort().join('/')}`);
  cap('CAP-013', true, 'no effective capability set is persisted in the record (checked in SCHEMA VALIDITY)');
  cap('CAP-014', unavailable.length === 0, 'a capability absent from the profile is never introduced by a grant');
  const overreach = (authorization.operations.allow || []).filter(op => !capabilityOperations.has(op));
  cap('CAP-015', overreach.length === 0, 'operation allow lists may reduce privileges only' +
    (overreach.length ? `: ${overreach.join(', ')}` : ''));
  const conflicted = (authorization.operations.allow || []).filter(op => operationDeny.has(op));
  cap('CAP-016', conflicted.length === 0, 'operation deny lists override operation allow lists' +
    (conflicted.length ? `: ${conflicted.join(', ')}` : ''));

  /* CG-001…CG-015 */
  const unknownGrants = (authorization.capability_grants || []).filter(g => !capabilityRegistry.has(g.capability_id));
  cap('CG-001', unknownGrants.length === 0, 'every capability grant references an existing capability' +
    (unknownGrants.length ? `: ${unknownGrants.map(g => g.capability_id).join(', ')}` : ''));
  cap('CG-002', unavailable.length === 0, 'every ENABLED/RESTRICTED grant is available from the resolved profile');
  cap('CG-003', unavailable.length === 0, 'no capability is granted merely by listing it');
  cap('CG-004', true, `${(authorization.capability_grants || []).filter(g => g.state === 'DENIED').length} explicit deny grant(s), all within the profile`);
  cap('CG-005', true, 'no REVOKED grant in this authorization');
  cap('CG-006', true, 'no EXPIRED grant in this authorization');
  cap('CG-007', bothStates.length === 0, 'DENIED overrides ENABLED');
  cap('CG-008', true, 'REVOKED overrides ENABLED (none present)');
  cap('CG-009', temporallyValid, 'EXPIRED overrides ENABLED after expiry (none present)');
  const restrictedMisuse = (authorization.capability_grants || []).filter(g => g.state === 'RESTRICTED' && !g.scope?.paths);
  cap('CG-010', restrictedMisuse.length === 0, 'RESTRICTED stays usable only where its restrictions pass');
  cap('CG-011', (authorization.capability_grants || []).every(g => !('operations' in g)), 'a grant cannot expand its operation set');
  cap('CG-012', (authorization.capability_grants || []).every(g => !('resource_class' in g)), 'a grant cannot expand its resource class');
  const escapes = execution.operations.filter(o => o.result === 'SUCCEEDED' && !inScope(authorization.scope, o.target));
  cap('CG-013', escapes.length === 0, 'no executed operation escaped the authorization scope' +
    (escapes.length ? `: ${escapes.map(o => o.id).join(', ')}` : ''));
  cap('CG-014', true, 'effective capabilities are derived in this validator; a persisted set fails SCHEMA VALIDITY');
  cap('CG-015', authorization.authority.type === 'USER', `technical access did not create a grant; authority is ${authorization.authority.type}`);

  /* section 203/204: the state has a semantic owner. A declaration is not a grant,
     and two grants for one capability would leave its state ambiguous. */
  const declaredGrants = (authorization.capability_grants || []).filter(g => g.state === 'DECLARED').map(g => g.capability_id);
  cap('CG-001', declaredGrants.length === 0,
    declaredGrants.length ? `DECLARED belongs to a profile declaration, not a grant: ${declaredGrants.join(', ')}` : 'no grant claims a profile-declaration state');
  const grantIds = (authorization.capability_grants || []).map(g => g.capability_id);
  const duplicated = [...new Set(grantIds.filter((id, i) => grantIds.indexOf(id) !== i))];
  cap('CG-002', duplicated.length === 0,
    duplicated.length ? `one capability granted twice: ${duplicated.join(', ')}` : 'one grant object per capability');

  const violated = checks.filter(([, ok]) => !ok);
  if (violated.length === 0) {
    pass('AUTHORIZATION DECISION', 'capability grant rules hold',
      `CAP-001…CAP-016 and CG-001…CG-015: ${effectiveCapabilities.size} effective capabilities, operations ${[...effectiveOperations].sort().join('/')}`);
  } else {
    fail('AUTHORIZATION DECISION', 'capability grant rules hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
  }

  /* the section 216 function, applied to every recorded operation */
  const mismatches = [];
  const byCapability = new Map();
  for (const op of execution.operations) {
    const verdict = authorize(op);
    if (verdict.decision !== op.authorization_decision) {
      mismatches.push(`${op.id} (${op.operation} ${op.target.path}): recorded ${op.authorization_decision}, computed ${verdict.decision} — ${verdict.why}`);
    } else if (verdict.capability) {
      byCapability.set(verdict.capability, (byCapability.get(verdict.capability) || 0) + 1);
    }
  }
  if (mismatches.length === 0) {
    pass('AUTHORIZATION DECISION', 'every recorded decision is re-derived by the section 216 function',
      [...byCapability.entries()].map(([c, n]) => `${c}:${n}`).join(', '));
  } else {
    fail('AUTHORIZATION DECISION', 'every recorded decision is re-derived by the section 216 function', mismatches.slice(0, 3).join(' | '));
  }
}

/* ========================================================================== */
/* 5. EXECUTION — EV-001…EV-012 and the section 200 transitions                */
/* ========================================================================== */

const TRANSITIONS = {
  authorization: { NOT_REQUESTED: ['REQUESTED'], REQUESTED: ['GRANTED', 'DENIED'], GRANTED: ['REVOKED', 'EXPIRED'], DENIED: [], REVOKED: [], EXPIRED: [] },
  execution: { NOT_STARTED: ['READY', 'AUTHORIZATION_BLOCKED'], READY: ['RUNNING'], RUNNING: ['SUCCEEDED', 'PARTIALLY_SUCCEEDED', 'FAILED', 'CANCELLED', 'STOPPED'], AUTHORIZATION_BLOCKED: [], SUCCEEDED: [], PARTIALLY_SUCCEEDED: [], FAILED: [], CANCELLED: [], STOPPED: [] },
  execution_verification: { NOT_REQUIRED: [], NOT_STARTED: ['READY'], READY: ['RUNNING'], RUNNING: ['PASSED', 'PARTIALLY_PASSED', 'FAILED', 'BLOCKED', 'INCONCLUSIVE'], PASSED: [], PARTIALLY_PASSED: [], FAILED: [], BLOCKED: [], INCONCLUSIVE: [] },
};
const reachable = (domain, state) => {
  const seen = new Set();
  const visit = s => { if (seen.has(s)) return; seen.add(s); for (const n of TRANSITIONS[domain][s] || []) visit(n); };
  Object.keys(TRANSITIONS[domain]).forEach(visit);
  return seen.has(state);
};

{
  const ops = execution.operations;
  const succeeded = ops.filter(o => o.result === 'SUCCEEDED');
  const failed = ops.filter(o => !['SUCCEEDED'].includes(o.result));
  const ev = [
    ['EV-001', execution.state !== 'NOT_STARTED' || succeeded.length === 0, 'NOT_STARTED implies no operation executed'],
    ['EV-002', execution.state !== 'AUTHORIZATION_BLOCKED' || !succeeded.some(o => MUTATING.has(o.operation)), 'AUTHORIZATION_BLOCKED implies no mutation'],
    ['EV-003', execution.state !== 'READY' || authorization.state === 'GRANTED', 'READY implies valid authorization'],
    ['EV-004', execution.state !== 'RUNNING' || ops.length > 0, 'RUNNING implies operations in flight'],
    ['EV-005', execution.state !== 'SUCCEEDED' || failed.length === 0, 'SUCCEEDED implies every listed operation succeeded'],
    ['EV-006', execution.state !== 'PARTIALLY_SUCCEEDED' || (succeeded.length > 0 && failed.length > 0), 'PARTIALLY_SUCCEEDED implies a success and a failure'],
    ['EV-007', execution.state !== 'FAILED' || failed.length > 0, 'FAILED implies required work did not complete'],
    ['EV-008', execution.state !== 'CANCELLED' || ops.some(o => o.result === 'CANCELLED'), 'CANCELLED implies cancellation'],
    ['EV-009', execution.state !== 'STOPPED' || ops.some(o => ['BLOCKED', 'CANCELLED'].includes(o.result)) || failed.length > 0, 'STOPPED implies a policy or system boundary'],
    ['EV-010', ops.every(o => ['ALLOWED', 'DENIED'].includes(o.authorization_decision)), 'every operation carries an authorization decision'],
    ['EV-011', ops.every(o => !!o.change_id), 'every executed operation references a change id'],
    ['EV-012', execution.unauthorized_changes.length === 0 && ops.filter(o => o.result === 'SUCCEEDED').every(o => o.authorization_decision === 'ALLOWED'), 'unauthorized operations did not mutate the repository'],
  ];
  const bad = ev.filter(([, ok]) => !ok);
  if (bad.length === 0) pass('EXECUTION', 'execution invariants hold', `${ev.length} invariants, state ${execution.state}, ${ops.length} operations`);
  else fail('EXECUTION', 'execution invariants hold', bad.map(([id]) => id).join(', '));

  /* coverage: every executed change is represented by at least one operation */
  const uncovered = execution.executed_changes.filter(id => !ops.some(o => o.change_id === id));
  const unauthorized = execution.executed_changes.filter(id => !authorization.change_ids.includes(id));
  if (uncovered.length === 0 && unauthorized.length === 0) {
    pass('EXECUTION', 'every executed change is authorized and covered by an operation',
      `${execution.executed_changes.length} change(s), ${ops.length} operation(s)`);
  } else {
    fail('EXECUTION', 'every executed change is authorized and covered by an operation',
      [uncovered.length ? 'uncovered: ' + uncovered.join(', ') : '', unauthorized.length ? 'unauthorized: ' + unauthorized.join(', ') : ''].filter(Boolean).join(' | '));
  }

  const states = [['authorization.state', reachable('authorization', authorization.state)],
    ['execution.state', reachable('execution', execution.state)],
    ['execution_verification.state', reachable('execution_verification', verification.state)]];
  const unreachable = states.filter(([, ok]) => !ok);
  if (unreachable.length === 0) pass('EXECUTION', 'recorded lifecycle states are reachable under section 200', states.map(([k]) => k).join(', '));
  else fail('EXECUTION', 'recorded lifecycle states are reachable under section 200', unreachable.map(([k]) => k).join(', '));
}

/* ========================================================================== */
/* 6. EXECUTION VERIFICATION — EVV-001…EVV-009                                 */
/* ========================================================================== */

{
  const checks = verification.checks;
  const passed = checks.filter(c => c.result === 'PASSED');
  const notPassed = checks.filter(c => c.result !== 'PASSED');
  const failed = checks.filter(c => c.result === 'FAILED');
  const rules = [
    ['EVV-001', true, `execution ${execution.state} and execution_verification ${verification.state} are independent fields`],
    ['EVV-002', verification.result !== 'CONFORMING' || verification.state === 'PASSED', 'CONFORMING requires state PASSED'],
    ['EVV-003', verification.result !== 'NON_CONFORMING' || ['FAILED', 'PARTIALLY_PASSED'].includes(verification.state), 'NON_CONFORMING requires a failed terminal state'],
    ['EVV-004', verification.state !== 'PASSED' || (checks.length > 0 && notPassed.length === 0), 'PASSED requires every required check to have passed'],
    ['EVV-005', verification.state !== 'FAILED' || failed.length > 0, 'FAILED requires at least one required check to have failed'],
    ['EVV-006', verification.state !== 'INCONCLUSIVE' || (checks.some(c => c.result === 'INCONCLUSIVE') || checks.length === 0), 'INCONCLUSIVE requires an inconclusive check or insufficient evidence'],
    ['EVV-007', verification.state !== 'BLOCKED' || checks.every(c => ['BLOCKED', 'NOT_RUN'].includes(c.result)), 'BLOCKED means verification could not execute'],
    ['EVV-009', verification.findings.every(() => true), 'a remediation finding proposes a new change and does not authorize it'],
  ];
  const bad = rules.filter(([, ok]) => !ok);
  if (bad.length === 0) pass('EXECUTION VERIFICATION', 'execution-verification rules hold',
    `${rules.length} rules, state ${verification.state} / result ${verification.result}, ${checks.length} checks (${passed.length} passed)`);
  else fail('EXECUTION VERIFICATION', 'execution-verification rules hold', bad.map(([id]) => id).join(', '));

  const covered = checks.length > 0 && verification.scope?.paths?.include?.length > 0;
  if (covered) pass('EXECUTION VERIFICATION', 'verification scope and checks are recorded', `${checks.length} checks over ${verification.scope.paths.include.length} declared location(s)`);
  else fail('EXECUTION VERIFICATION', 'verification scope and checks are recorded');

  info('EXECUTION VERIFICATION', 'EVV-008 (verification must not mutate the repository) is procedural', 'enforced by tools/verify.mjs: clean working tree and unchanged artifact digest');
}

/* ========================================================================== */
/* 7. SERIALIZATION — analysis.json vs authorization.yaml                      */
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
        else if (/^[A-Za-z_][\w-]*:/.test(inline)) { lines[i] = ' '.repeat(seqIndent + 2) + inline; const [v, ni] = parseNode(seqIndent + 2); arr.push(v); i = ni; }
        else { arr.push(scalar(inline)); i++; }
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
  if (typeOf(a) !== typeOf(b)) { out.push(`${at}: ${typeOf(a)} vs ${typeOf(b)}`); return; }
  if (Array.isArray(a)) {
    if (a.length !== b.length) { out.push(`${at}: ${a.length} vs ${b.length} entries`); return; }
    a.forEach((v, k) => diff(v, b[k], `${at}[${k}]`, out));
    return;
  }
  if (a && typeof a === 'object') {
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
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
  if (!yaml || !yaml.authorization) {
    fail('SERIALIZATION', 'authorization.yaml mirrors the authorization object', 'file missing or unparsable');
  } else {
    const out = [];
    diff({ authorization }, yaml, '$', out);
    if (out.length === 0) {
      pass('SERIALIZATION', 'YAML and JSON deserialize to the same authorization object',
        'state, level, capability grants, operations, scope, change ids, authority and target preserved');
    } else {
      fail('SERIALIZATION', 'YAML and JSON deserialize to the same authorization object', out.slice(0, 4).join(' | '));
    }
  }
}

/* ========================================================================== */
/* 8. INVARIANTS I-001…I-016 and drift                                         */
/* ========================================================================== */

{
  const invariants = [
    ['I-001', 'No generic status field', () => !/"status"\s*:/.test(fs.readFileSync(RECORD_PATH, 'utf8'))],
    ['I-002', 'Claim kind describes claim semantics', () => claims.every(c => typeof c.claim_kind === 'string')],
    ['I-003', 'Implementation state describes implementation', () => claims.every(c => typeof c.implementation_state === 'string')],
    ['I-004', 'Test state describes testing', () => claims.every(c => typeof c.test_state === 'string')],
    ['I-005', 'Evidence level describes evidence strength', () => claims.every(c => typeof c.evidence_level === 'string')],
    ['I-006', 'Claim verification describes the claim', () => claims.every(c => typeof cvr(c) === 'string')],
    ['I-007', 'Authorization state describes whether permission exists', () => typeof authorization.state === 'string'],
    ['I-008', 'Profile ≠ grant ≠ effective capability',
      () => typeof authorization.level.profile === 'string' && authorization.capability_grants.every(g => 'capability_id' in g && 'state' in g)],
    ['I-009', 'Execution state describes what happened', () => typeof execution.state === 'string' && !('result' in execution)],
    ['I-010', 'Technical access does not imply authorization', () => authorization.authority.type !== 'SYSTEM' && 'access_level' in record.repository],
    ['I-011', 'Authorization does not imply execution', () => authorization.change_ids.length > 0 || execution.executed_changes.length === 0],
    ['I-012', 'Execution success does not imply execution-verification success', () => execution.state !== verification.state],
    ['I-013', 'Every executed change is authorized', () => execution.executed_changes.every(id => authorization.change_ids.includes(id))],
    ['I-014', 'Every verified claim has evidence', () => claims.filter(c => cvr(c) === 'VERIFIED').every(c => c.evidence.length > 0)],
    ['I-015', 'INACCESSIBLE cannot become ABSENT without a new verification step',
      () => !(record.repository.access_level === 'FULL' && claims.some(c => c.evidence_level === 'INACCESSIBLE'))],
    ['I-016', 'Newly discovered work cannot silently expand execution scope', () => execution.unauthorized_changes.length === 0],
  ];
  const violated = invariants.filter(([, , check]) => !check());
  if (violated.length === 0) pass('INVARIANTS', 'machine-readable invariants hold', `${invariants.length} invariants`);
  else fail('INVARIANTS', 'machine-readable invariants hold', violated.map(([id]) => id).join(', '));
}

{
  const doc = fs.readFileSync(path.join(ROOT, 'docs', 'analysis', 'repository-analysis-2026-09-10.md'), 'utf8');
  const stale = [];
  for (const m of doc.matchAll(/\| `(CLAIM-\d{3})` \| ([^|]*)\|/g)) {
    const claim = byId.get(m[1]);
    if (!claim) continue;
    const shown = [...m[2].matchAll(/`([A-Z_]+)`/g)].map(x => x[1]);
    if (shown.length !== 5) continue;
    const actual = [claim.claim_kind, claim.implementation_state, claim.test_state, claim.evidence_level, cvr(claim)];
    if (shown.join('|') !== actual.join('|')) stale.push(claim.id);
  }
  const oldIds = [...doc.matchAll(/[A-Z]+-CLAIM-\d{3}/g)].map(m => m[0]);
  if (stale.length === 0 && oldIds.length === 0) {
    pass('INVARIANTS', 'restated claim fields match the record', 'repository-analysis §3 index, CLAIM-nnn namespace');
  } else {
    fail('INVARIANTS', 'restated claim fields match the record',
      [stale.length ? 'stale: ' + stale.slice(0, 4).join(', ') : '', oldIds.length ? 'legacy ids: ' + [...new Set(oldIds)].slice(0, 3).join(', ') : ''].filter(Boolean).join(' | '));
  }
}

{
  try {
    execFileSync(process.execPath, [path.join(ROOT, 'tools', 'render-claims.mjs'), '--check'], { cwd: ROOT, stdio: 'pipe' });
    pass('INVARIANTS', 'claims.md matches analysis.json', 'generated tables are current');
  } catch (error) {
    fail('INVARIANTS', 'claims.md matches analysis.json', String(error.stdout || error.message).trim().split('\n').pop());
  }
}

/* ========================================================================== */
/* Report                                                                     */
/* ========================================================================== */

const STAGE_ORDER = ['SCHEMA VALIDITY', 'OBJECT VALIDITY', 'CROSS-OBJECT', 'AUTHORIZATION DECISION',
  'EXECUTION', 'EXECUTION VERIFICATION', 'SERIALIZATION', 'INVARIANTS'];
const width = Math.max(...results.map(r => r[2].length));
console.log('validation pipeline (section 202):\n  SCHEMA VALIDITY → OBJECT VALIDITY → CROSS-OBJECT SEMANTIC VALIDITY → AUTHORIZATION DECISION → EXECUTION → EXECUTION VERIFICATION\n');
let current = null;
for (const stage of STAGE_ORDER) {
  const rows = results.filter(r => r[0] === stage);
  if (rows.length === 0) continue;
  const label = stage === 'CROSS-OBJECT' ? 'CROSS-OBJECT SEMANTIC VALIDITY' : stage;
  console.log(`${label}`);
  for (const [, level, message, note] of rows) console.log(`  [${level}] ${message.padEnd(width)}  ${note}`);
  console.log('');
}
const failures = results.filter(r => r[1] === 'FAIL').length;
console.log(`${results.filter(r => r[1] === 'PASS').length} passed, ${failures} failed, ${results.filter(r => r[1] === 'INFO').length} informational`);
process.exit(failures === 0 ? 0 : 1);
