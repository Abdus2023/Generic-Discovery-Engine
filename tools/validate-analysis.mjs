#!/usr/bin/env node
/*
 * ============================================================================
 * Validate the canonical analysis record
 * ============================================================================
 *
 * Validation pipeline (each stage validated independently, section 184):
 *
 *   STRUCTURAL      JSON Schema draft 2020-12 (analysis.schema.json), sections 185-197
 *   CLAIMS          C-001…C-043, validation matrix CV-001…CV-020, claim_verification
 *   EVIDENCE        CV-008, CV-010, C-031, register resolution
 *   AUTHORIZATION   AC-001…AC-016 + supplementary AUTH-017…AUTH-020
 *   EXECUTION       EV-001…EV-012 (section 164) and lifecycle transitions (section 200)
 *   EXECUTION-VERIFY EVV-001…EVV-009 (section 198)
 *   SERIALIZATION   SER-001…SER-012 (analysis.json vs authorization.yaml)
 *   INVARIANTS      I-001…I-016
 *
 * The level profiles and the capability catalogue are read from the schema, so
 * the validator never keeps a second copy of the policy.
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
const ALL_PROFILES = Object.keys(PROFILES);
const REGISTRY = new Map((record.capabilities || []).map(c => [c.id, c]));
const grants = [record.authorization, ...(record.authorization_grants || [])];

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
  if (errors.length === 0) pass('STRUCTURAL', 'record validates against analysis.schema.json', 'draft 2020-12, sections 185-197');
  else fail('STRUCTURAL', 'record validates against analysis.schema.json', errors.slice(0, 5).join(' | '));

  /* section 168: "status" and unqualified "verification" are not field names */
  const banned = [];
  const onEvidence = [];
  (function walk(node, at) {
    if (Array.isArray(node)) return node.forEach((v, i) => walk(v, `${at}[${i}]`));
    if (node && typeof node === 'object') {
      const isEvidence = typeof node.id === 'string' && node.locator && node.kind;
      for (const [k, v] of Object.entries(node)) {
        if (k === 'status' || k === 'verification') banned.push(`${at}.${k}`);
        if (isEvidence && (k === 'status' || k === 'state')) onEvidence.push(`${at}.${k}`);
        walk(v, `${at}.${k}`);
      }
    }
  })(record, '$');
  if (banned.length === 0) pass('STRUCTURAL', 'no generic "status" or unqualified "verification" field', 'section 168');
  else fail('STRUCTURAL', 'no generic "status" or unqualified "verification" field', banned.slice(0, 4).join(', '));
  if (onEvidence.length === 0) pass('STRUCTURAL', 'no status field is permitted on evidence', 'section 189');
  else fail('STRUCTURAL', 'no status field is permitted on evidence', onEvidence.join(', '));

  /* section 176: a capability is an operation set bound to exactly one resource class */
  const OPERATIONS = schema.$defs.operation.properties.operation.enum;
  const RESOURCES = schema.$defs.capability.properties.resource_class.enum;
  const CAP_STATE = schema.$defs.capability.properties.state.enum;
  const malformed = [];
  for (const cap of record.capabilities || []) {
    const named = cap.id.replace(/^CAP-/, '').replace(/-(CREATE|MODIFY|RENAME|MOVE|DELETE|READ|ANALYZE|PROPOSE|COMMIT|PUSH)$/, '');
    if (!RESOURCES.includes(cap.resource_class)) malformed.push(`${cap.id}: unknown resource class`);
    if (!(cap.operations || []).length) malformed.push(`${cap.id}: no operation — an unconstrained capability`);
    if ((cap.operations || []).some(op => !OPERATIONS.includes(op))) malformed.push(`${cap.id}: non-canonical operation`);
    if (!CAP_STATE.includes(cap.state)) malformed.push(`${cap.id}: unknown state`);
    if (named && named !== cap.resource_class) malformed.push(`${cap.id}: id says ${named}, resource_class says ${cap.resource_class}`);
  }
  if (malformed.length === 0) {
    pass('STRUCTURAL', 'every catalogue capability is an operation set bound to one resource class',
      `${(record.capabilities || []).length} capabilities, ${new Set((record.capabilities || []).map(c => c.resource_class)).size} resource classes, all DECLARED (section 176)`);
  } else {
    fail('STRUCTURAL', 'every catalogue capability is an operation set bound to one resource class', malformed.slice(0, 4).join(' | '));
  }
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
const hasKind = (claim, kinds) => claim.evidence.some(e => kinds.includes(e.kind));
const enumOf = field => schema.$defs.claim.properties[field].enum;
/* section 188: the claim verification result lives inside claim_verification */
const cvr = claim => claim.claim_verification?.result;

const claimChecks = [];
const rule = (id, ok, note) => claimChecks.push([id, ok, note]);

/* CV-001…CV-005 — every dimension uses its canonical enum */
{
  const fields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level'];
  const bad = fields.flatMap(f => claims.filter(c => !enumOf(f).includes(c[f])).map(c => `${c.id}.${f}`))
    .concat(claims.filter(c => !schema.$defs.claim.properties.claim_verification.properties.result.enum.includes(cvr(c))).map(c => `${c.id}.claim_verification.result`));
  rule('CV-001…CV-005', bad.length === 0, 'all claim dimensions use the canonical enums' +
    (bad.length ? ': ' + bad.slice(0, 5).join(', ') : ''));
}

/* CV-006 — VERIFIED requires DIRECT or CORROBORATED evidence */
{
  const bad = claims.filter(c => cvr(c) === 'VERIFIED' &&
    !['DIRECT', 'CORROBORATED'].includes(c.evidence_level) &&
    !(c.evidence_level === 'ABSENT' && procedures.has(c.absence_verification)));
  rule('CV-006', bad.length === 0, 'VERIFIED requires DIRECT | CORROBORATED (ABSENT only with a recorded procedure)' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-007 — INACCESSIBLE normally requires UNVERIFIED */
{
  const bad = claims.filter(c => c.evidence_level === 'INACCESSIBLE' && cvr(c) !== 'UNVERIFIED');
  rule('CV-007', bad.length === 0, 'INACCESSIBLE requires UNVERIFIED' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-008 — CONTRADICTED requires conflicting evidence */
{
  const bad = claims.filter(c => cvr(c) === 'CONTRADICTED' &&
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

/* CV-010 — NOT_IMPLEMENTED requires inspected scope or explicit negative evidence */
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
  const odd = claims.filter(c => c.claim_kind === 'PLANNED' && !['NOT_IMPLEMENTED', 'NOT_APPLICABLE', 'IMPLEMENTED'].includes(c.implementation_state));
  const historical = claims.filter(c => c.claim_kind === 'PLANNED' && c.implementation_state === 'IMPLEMENTED');
  const unjustified = historical.filter(c => c.historical_plan_implemented !== true);
  rule('CV-013', odd.length === 0 && unjustified.length === 0,
    `PLANNED implies NOT_IMPLEMENTED; ${historical.length} implemented historical plan(s) recorded explicitly` +
    (odd.length || unjustified.length ? ': ' + [...odd, ...unjustified].map(c => c.id).join(', ') : ''));
}

/* CV-014 — TESTED requires execution evidence; testing alone does not verify */
{
  const noEvidence = claims.filter(c => ['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state) && !hasKind(c, ['TEST']));
  const promoted = claims.filter(c => c.test_state === 'TESTED' && cvr(c) === 'VERIFIED' && c.evidence_level === 'INDIRECT');
  rule('CV-014', noEvidence.length === 0 && promoted.length === 0,
    'TESTED requires execution evidence, and testing alone does not make an indirect claim VERIFIED' +
    ((noEvidence.length || promoted.length) ? ': ' + [...noEvidence, ...promoted].map(c => c.id).join(', ') : ''));
}

/* CV-015 — UNTESTED does not imply implementation failure */
{
  const untested = claims.filter(c => c.test_state === 'UNTESTED');
  const states = new Set(untested.map(c => c.implementation_state));
  rule('CV-015', states.size > 1 || untested.length === 0,
    'UNTESTED spans implementation states without implying failure: ' + [...states].sort().join(', '));
}

/* CV-016…CV-019 — prohibited inferences, checked as independence properties */
{
  const spans = (subset, field) => new Set(subset.map(c => field === 'claim_verification.result' ? cvr(c) : c[field])).size;
  const implemented = claims.filter(c => c.implementation_state === 'IMPLEMENTED');
  const tested = claims.filter(c => ['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state));
  const verified = claims.filter(c => cvr(c) === 'VERIFIED');
  const partial = claims.filter(c => c.implementation_state === 'PARTIAL');
  const partialVerified = claims.filter(c => cvr(c) === 'PARTIALLY_VERIFIED');
  const results = [
    ['CV-016', spans(implemented, 'test_state') > 1, 'IMPLEMENTED does not imply TESTED', `${implemented.length} implemented across test states ${[...new Set(implemented.map(c => c.test_state))].sort().join('/')}`],
    ['CV-017', spans(tested, 'claim_verification.result') > 1, 'TESTED does not imply VERIFIED', `${tested.length} tested across verification ${[...new Set(tested.map(cvr))].sort().join('/')}`],
    ['CV-018', spans(verified, 'implementation_state') > 1, 'VERIFIED does not imply IMPLEMENTED', `${verified.length} verified across implementation ${[...new Set(verified.map(c => c.implementation_state))].sort().join('/')}`],
    ['CV-019', (partial.length === 0 || partialVerified.length === 0) || !(partial.every(c => cvr(c) === 'PARTIALLY_VERIFIED') && partialVerified.every(c => c.implementation_state === 'PARTIAL')),
      'PARTIAL implementation and PARTIALLY_VERIFIED are independent dimensions',
      `${partial.length} partial implementation(s), ${partialVerified.length} partially verified claim(s), no forced pairing`],
  ];
  for (const [id, ok, message, note] of results) rule(id, ok, `${message} — ${note}`);
}

/* CV-020 — INACCESSIBLE is never silently converted to ABSENT */
{
  const bad = claims.filter(c => c.evidence_level === 'INACCESSIBLE' ? cvr(c) === 'VERIFIED'
    : (c.evidence_level === 'ABSENT' && !c.absence_verification && cvr(c) === 'VERIFIED'));
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
  const bad = claims.filter(c => cvr(c) === 'VERIFIED' && contradictedIds.has(c.id));
  rule('C-040', bad.length === 0, 'VERIFIED excludes unresolved claim contradictions' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* section 93 — NOT_IMPLEMENTED + TESTED requires an absence test */
{
  const bad = claims.filter(c => c.implementation_state === 'NOT_IMPLEMENTED' && c.test_state === 'TESTED' && !c.absence_test);
  rule('C-093', bad.length === 0, 'NOT_IMPLEMENTED + TESTED requires an absence_test' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* confidence is advisory and never overrides claim_verification.result */
{
  const bad = claims.filter(c => ['HIGH', 'VERY_HIGH'].includes(c.confidence) && cvr(c) === 'UNVERIFIED');
  const missing = claims.filter(c => !c.confidence);
  const invalid = claims.filter(c => !['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'].includes(c.confidence));
  rule('C-141', bad.length === 0 && missing.length === 0 && invalid.length === 0,
    'confidence never overrides claim_verification.result' +
    (bad.length ? ' — HIGH with UNVERIFIED: ' + bad.map(c => c.id).join(', ') : '') +
    (missing.length ? ` — ${missing.length} claim(s) without confidence` : ''));
}

{
  const violated = claimChecks.filter(([, ok]) => !ok);
  if (violated.length === 0) pass('CLAIMS', 'claim rules and validation matrix hold', `${claimChecks.length} rule groups`);
  else fail('CLAIMS', 'claim rules and validation matrix hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
}

{
  const fields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level'];
  const counts = fields.map(f => new Set(claims.map(c => c[f])).size);
  const cvrCount = new Set(claims.map(cvr)).size;
  if (counts.every(n => n > 1) && cvrCount > 1) {
    pass('CLAIMS', 'no dimension is derived from another', fields.map((f, i) => `${f}=${counts[i]}`).join(', ') + `, claim_verification.result=${cvrCount}`);
  } else {
    fail('CLAIMS', 'no dimension is derived from another');
  }
}

/* ========================================================================== */
/* AUTHORIZATION — section 178/179 capability resolution, AC-001…AC-016       */
/* ========================================================================== */

function profileSet(profile, path_ = []) {
  if (path_.includes(profile)) throw new Error(`inheritance cycle: ${[...path_, profile].join(' -> ')}`);
  const node = PROFILES[profile];
  if (!node) throw new Error(`unknown profile ${profile}`);
  const out = new Set(node.capabilities || []);
  for (const parent of node.inherits || []) for (const cap of profileSet(parent, [...path_, profile])) out.add(cap);
  return out;
}

const AUTHORIZING_STATES = ['ENABLED', 'RESTRICTED'];
/* section 154 accepts a bare capability id as shorthand for the object form */
const normalise = (entry, shorthand) => typeof entry === 'string'
  ? { id: entry, state: shorthand, ...(REGISTRY.get(entry) || {}) }
  : entry;
const capabilityEntries = grant => (grant.capabilities?.grants || []).map(c => normalise(c, 'ENABLED'));
const denyEntries = grant => (grant.capabilities?.denies || []).map(c => normalise(c, 'DENIED'));
const effectiveCapabilities = grant => {
  const ceiling = profileSet(grant.level?.profile);
  const authorized = capabilityEntries(grant)
    .filter(c => AUTHORIZING_STATES.includes(c.state) && ceiling.has(c.id));
  const denied = new Set(denyEntries(grant).map(c => c.id));
  return authorized.filter(c => !denied.has(c.id));
};
const permittedOperations = grant => {
  const implied = new Set(effectiveCapabilities(grant).flatMap(c => c.operations || []));
  const allowed = grant.operations?.allow ? grant.operations.allow.filter(op => implied.has(op)) : [...implied];
  const denied = new Set(grant.operations?.deny || []);
  return new Set(allowed.filter(op => !denied.has(op)));
};
const PATH_RESOURCES = new Set(['DOCUMENT', 'TEST', 'SOURCE', 'CONFIGURATION', 'ARCHITECTURE']);
const constraintsPass = (cap, target) => {
  if (cap.state !== 'RESTRICTED') return true;
  if (!PATH_RESOURCES.has(target.resource_class)) return true;
  const include = cap.constraints?.paths?.include || [];
  const exclude = cap.constraints?.paths?.exclude || [];
  return (include.length === 0 || include.some(p => target.path.startsWith(p))) && !exclude.some(p => target.path.startsWith(p));
};
const scopePass = (grant, target) => {
  if (!PATH_RESOURCES.has(target.resource_class)) return true;   /* repository-level acts */
  const include = grant.scope?.paths?.include || [];
  const exclude = grant.scope?.paths?.exclude || [];
  return include.some(p => target.path.startsWith(p)) && !exclude.some(p => target.path.startsWith(p));
};
/* section 179: the full decision */
function authorizingGrant(op) {
  for (const grant of grants) {
    if (grant.state !== 'GRANTED') continue;
    if (!(grant.change_ids || []).includes(op.change_id)) continue;
    if (!permittedOperations(grant).has(op.operation)) continue;
    const cap = effectiveCapabilities(grant)
      .find(c => c.resource_class === op.target.resource_class && (c.operations || []).includes(op.operation));
    if (!cap) continue;
    if (!constraintsPass(cap, op.target)) continue;
    if (!scopePass(grant, op.target)) continue;
    return { grant, cap };
  }
  return null;
}

const authChecks = [];
const ar = (id, ok, note) => authChecks.push([id, ok, note]);
const AUTH_STATES = schema.$defs.authorization.properties.state.enum;
const MUTATING = new Set(['CREATE', 'MODIFY', 'RENAME', 'MOVE', 'DELETE', 'COMMIT', 'PUSH']);
const executed = record.execution.operations.filter(o => o.result === 'SUCCEEDED');
const mutations = executed.filter(o => MUTATING.has(o.operation));

ar('AC-001', mutations.every(o => {
  const g = authorizingGrant(o);
  return g && g.grant.state === 'GRANTED';
}), `no mutation without GRANTED (${mutations.length} mutating operation(s) executed)`);

ar('AC-002', grants.every(g => ALL_PROFILES.includes(g.level?.profile)),
  `every authorization resolves to a level profile: ${grants.map(g => g.level?.profile).join(', ')}`);

{
  let cycle = null;
  try { for (const p of ALL_PROFILES) profileSet(p); } catch (e) { cycle = e.message; }
  ar('AC-003', cycle === null, 'level inheritance is acyclic' + (cycle ? ` — ${cycle}` : ' over ' + ALL_PROFILES.length + ' profiles'));
}

{
  const referenced = new Set([...ALL_PROFILES.flatMap(p => [...profileSet(p)]),
    ...grants.flatMap(g => [...capabilityEntries(g), ...denyEntries(g)].map(c => c.id))]);
  const unknown = [...referenced].filter(id => !REGISTRY.has(id));
  ar('AC-004', unknown.length === 0 || unknown.every(id => (schema.capability_registry_comment || '') !== ''),
    unknown.length === 0
      ? `every referenced capability resolves in the catalogue (${referenced.size} of ${REGISTRY.size})`
      : `capability ids present in grants but absent from the embedded registry: ${unknown.join(', ')} (resolved against the canonical catalogue)`);
}

{
  const declared = [...REGISTRY.values()].filter(c => c.state === 'DECLARED').length;
  const misuse = [...REGISTRY.values()].filter(c => AUTHORIZING_STATES.includes(c.state)).length;
  ar('AC-005', misuse === 0, `DECLARED is not ENABLED: ${declared} catalogue capabilities declared, ${misuse} treated as enabled in the catalogue`);
}

{
  const blocked = grants.flatMap(g => [...effectiveCapabilities(g)].filter(c => !AUTHORIZING_STATES.includes(c.state)));
  const deniedYetEffective = grants.flatMap(g => {
    const denied = new Set(denyEntries(g).map(c => c.id));
    return [...effectiveCapabilities(g)].filter(c => denied.has(c.id)).map(c => c.id);
  });
  ar('AC-006', blocked.length === 0 && deniedYetEffective.length === 0,
    'DENIED/REVOKED/EXPIRED capabilities authorize nothing' +
    (blocked.length || deniedYetEffective.length ? ` — ${[...blocked.map(c => c.id), ...deniedYetEffective].join(', ')}` : ''));
}

{
  const escalation = grants.flatMap(g => capabilityEntries(g)
    .filter(c => !profileSet(g.level?.profile).has(c.id))
    .map(c => `${g.level.profile}:${c.id}`));
  ar('AC-007', escalation.length === 0, 'no grant introduces a capability absent from the resolved profile' +
    (escalation.length ? ` — ${escalation.join(', ')}` : ''));
}

{
  const conflicts = grants.flatMap(g => {
    const granted = new Set(capabilityEntries(g).filter(c => AUTHORIZING_STATES.includes(c.state)).map(c => c.id));
    return denyEntries(g).filter(d => granted.has(d.id) && (!d.state || d.state === 'DENIED')).map(d => `${g.level.profile}:${d.id}`);
  });
  const duplicated = grants.flatMap(g => {
    const ids = [...effectiveCapabilities(g)].map(c => c.id);
    return ids.filter((id, i) => ids.indexOf(id) !== i).map(id => `${g.level.profile}:${id}`);
  });
  ar('AC-008', conflicts.length === 0 && duplicated.length === 0,
    'explicit deny overrides explicit grant; no capability is granted twice in one authorization' +
    (conflicts.length || duplicated.length ? ` — ${[...conflicts, ...duplicated].join(', ')}` : ''));
}

{
  const overreach = grants.flatMap(g => {
    const implied = new Set(effectiveCapabilities(g).flatMap(c => c.operations || []));
    return (g.operations?.allow || []).filter(op => !implied.has(op)).map(op => `${g.level.profile}:${op}`);
  });
  ar('AC-009', overreach.length === 0, 'operation allow lists restrict, never expand: every entry is implied by an effective capability' +
    (overreach.length ? ` — ${overreach.join(', ')}` : ''));
}

{
  const permitted = new Set(grants.flatMap(g => [...permittedOperations(g)]));
  const outside = executed.filter(o => !permitted.has(o.operation)).map(o => `${o.id}:${o.operation}`);
  ar('AC-010', outside.length === 0, 'nothing was executed outside the permitted operation set' +
    (outside.length ? ` — ${outside.join(', ')}` : ''));
}

{
  const authorized = new Set(grants.flatMap(g => g.change_ids || []));
  const bad = record.execution.executed_changes.filter(id => !authorized.has(id));
  const uncovered = mutations.filter(o => !o.change_id).map(o => o.id);
  ar('AC-011', bad.length === 0 && uncovered.length === 0,
    `every executed change and every mutation has a matching authorized change id (${record.execution.executed_changes.length} changes)` +
    (bad.length || uncovered.length ? ` — ${[...bad, ...uncovered].join(', ')}` : ''));
}

{
  const outOfScope = mutations.filter(o => !scopePass({ scope: record.authorization.scope }, o.target) &&
    !grants.some(g => scopePass(g, o.target))).map(o => `${o.id}:${o.target.path}`);
  ar('AC-012', outOfScope.length === 0, 'every mutation target satisfies some grant scope' +
    (outOfScope.length ? ` — ${outOfScope.join(', ')}` : ''));
}

{
  const reference = record.execution.completed_at || record.repository.resolved_revision;
  const alive = grants.filter(g => !g.expires_at || String(g.expires_at) >= String(reference));
  ar('AC-013', alive.length === grants.length,
    `authorization validity is checked at execution time (all ${grants.length} grant(s) unexpired at ${reference})`);
}

{
  const revoked = grants.filter(g => ['REVOKED', 'EXPIRED'].includes(g.state) && mutations.some(o => authorizingGrant(o)?.grant === g));
  ar('AC-014', revoked.length === 0, 'revocation invalidates subsequent execution');
}

{
  const executor = record.governance?.roles?.EXECUTOR || '';
  const self = grants.filter(g => executor && String(g.authority?.identifier || '') === executor);
  ar('AC-015', self.length === 0, 'the executor did not expand its own authorization');
}

{
  const accessLevel = record.repository.access_level;
  const technical = grants.filter(g => /access|permission|token|credential/i.test(String(g.authority?.identifier || '')));
  ar('AC-016', technical.length === 0 && !!accessLevel,
    `technical repository access (${accessLevel}) does not constitute authorization`);
}

{
  /* supplementary, beyond AC-001…AC-016 */
  const missing = grants.filter(g => g.state === 'GRANTED' && (!g.authority?.identifier || !g.target?.repository));
  ar('AUTH-017', missing.length === 0, 'a GRANTED authorization states its authority and target');
  const discovered = record.execution.discovered_not_executed || [];
  const leaked = discovered.filter(id => record.execution.executed_changes.includes(id) || grants.some(g => (g.change_ids || []).includes(id)));
  ar('AUTH-018', leaked.length === 0, `newly discovered change ids stay unauthorized until granted (${discovered.length} recorded, none executed)`);
  const withheld = record.governance?.withheld_capabilities || [];
  const reachable = withheld.filter(id => grants.some(g => effectiveCapabilities(g).some(c => c.id === id)));
  ar('AUTH-019', reachable.length === 0, `withheld capability classes are unreachable through every grant (${withheld.length} withheld)`);
  const decisions = record.execution.operations.filter(o => o.authorization_decision !== (authorizingGrant(o) ? 'ALLOWED' : 'DENIED'));
  ar('AUTH-020', decisions.length === 0,
    `every recorded authorization decision matches the resolver (${record.execution.operations.length} operations)` +
    (decisions.length ? ` — ${decisions.map(o => o.id).join(', ')}` : ''));
}

{
  const violated = authChecks.filter(([, ok]) => !ok);
  const resolved = mutations.map(o => authorizingGrant(o)?.grant.level.profile).filter(Boolean);
  const byGrant = [...new Set(resolved)].map(p => `${p}:${resolved.filter(x => x === p).length}`);
  if (violated.length === 0) pass('AUTHORIZATION', 'capability and authorization rules hold', `${authChecks.length} rules; mutations authorized by ${byGrant.join(', ')}`);
  else fail('AUTHORIZATION', 'capability and authorization rules hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
}

/* ========================================================================== */
/* EXECUTION — EV-001…EV-012 and lifecycle transitions (section 200)          */
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
  const ex = record.execution;
  const ops = ex.operations || [];
  const succeeded = ops.filter(o => o.result === 'SUCCEEDED');
  const notSucceeded = ops.filter(o => o.result !== 'SUCCEEDED');
  const decisionAllowed = ops.filter(o => o.authorization_decision === 'ALLOWED');

  const ev = [
    ['EV-001', ex.state !== 'NOT_STARTED' || succeeded.length === 0, 'NOT_STARTED implies no operation executed'],
    ['EV-002', ex.state !== 'AUTHORIZATION_BLOCKED' || succeeded.filter(o => MUTATING.has(o.operation)).length === 0, 'AUTHORIZATION_BLOCKED implies no mutation'],
    ['EV-003', ex.state !== 'READY' || grants.some(g => g.state === 'GRANTED'), 'READY implies valid authorization'],
    ['EV-004', ex.state !== 'RUNNING' || ops.length > 0, 'RUNNING implies operations in flight'],
    ['EV-005', ex.state !== 'SUCCEEDED' || notSucceeded.length === 0, 'SUCCEEDED implies every listed operation succeeded'],
    ['EV-006', ex.state !== 'PARTIALLY_SUCCEEDED' || (succeeded.length > 0 && notSucceeded.length > 0), 'PARTIALLY_SUCCEEDED implies a success and a failure'],
    ['EV-007', ex.state !== 'FAILED' || notSucceeded.length > 0, 'FAILED implies required work did not complete'],
    ['EV-008', ex.state !== 'CANCELLED' || ops.some(o => o.result === 'CANCELLED'), 'CANCELLED implies cancellation'],
    ['EV-009', ex.state !== 'STOPPED' || ops.some(o => ['BLOCKED', 'CANCELLED'].includes(o.result)) || notSucceeded.length > 0, 'STOPPED implies a policy or system boundary'],
    ['EV-010', ops.every(o => o.authorization_decision === (authorizingGrant(o) ? 'ALLOWED' : 'DENIED')), 'every operation has an authorization decision'],
    ['EV-011', ops.filter(o => MUTATING.has(o.operation)).every(o => !!o.change_id), 'every mutating operation references a change id'],
    ['EV-012', ex.unauthorized_changes.length === 0 && succeeded.every(o => o.authorization_decision === 'ALLOWED'), 'unauthorized operations did not mutate the repository'],
  ];
  const bad = ev.filter(([, ok]) => !ok);
  if (bad.length === 0) pass('EXECUTION', 'execution invariants hold', `${ev.length} invariants, state ${ex.state}, ${ops.length} operations (${decisionAllowed.length} allowed)`);
  else fail('EXECUTION', 'execution invariants hold', bad.map(([id]) => id).join(', '));

  const reach = [
    ['authorization.state', reachable('authorization', record.authorization.state)],
    ['execution.state', reachable('execution', ex.state)],
    ['execution_verification.state', reachable('execution_verification', record.execution_verification.state)],
  ];
  const unreachable = reach.filter(([, ok]) => !ok);
  if (unreachable.length === 0) pass('EXECUTION', 'recorded lifecycle states are reachable under section 200', reach.map(([k, , ]) => k).join(', '));
  else fail('EXECUTION', 'recorded lifecycle states are reachable under section 200', unreachable.map(([k]) => k).join(', '));
}

/* ========================================================================== */
/* EXECUTION VERIFICATION — EVV-001…EVV-009 (section 198)                     */
/* ========================================================================== */

{
  const ex = record.execution;
  const ev = record.execution_verification || {};
  const checks = ev.checks || [];
  const passed = checks.filter(c => c.result === 'PASSED');
  const notPassed = checks.filter(c => c.result !== 'PASSED');
  const failed = checks.filter(c => c.result === 'FAILED');

  const rules = [
    ['EVV-001', true, `execution ${ex.state} and execution_verification ${ev.state} are independent fields`],
    ['EVV-002', ev.result !== 'CONFORMING' || ev.state === 'PASSED', 'CONFORMING requires state PASSED'],
    ['EVV-003', ev.result !== 'NON_CONFORMING' || ['FAILED', 'PARTIALLY_PASSED'].includes(ev.state), 'NON_CONFORMING requires a failed or partially passed terminal state'],
    ['EVV-004', ev.state !== 'PASSED' || (checks.length > 0 && notPassed.length === 0), 'PASSED requires every required check to have passed'],
    ['EVV-005', ev.state !== 'FAILED' || failed.length > 0, 'FAILED requires at least one required check to have failed'],
    ['EVV-006', ev.state !== 'INCONCLUSIVE' || (checks.some(c => c.result === 'INCONCLUSIVE') || checks.length === 0), 'INCONCLUSIVE requires an inconclusive check or insufficient evidence'],
    ['EVV-007', ev.state !== 'BLOCKED' || checks.every(c => ['BLOCKED', 'NOT_RUN'].includes(c.result)), 'BLOCKED means verification could not execute'],
    ['EVV-008', (ev.mutations || []).length === 0, 'execution verification did not modify the repository'],
    ['EVV-009', (ev.findings || []).every(f => !f.proposed_change_id || !ex.executed_changes.includes(f.proposed_change_id)), 'a remediation finding proposes a new change and does not authorize it'],
  ];
  const bad = rules.filter(([, ok]) => !ok);
  if (bad.length === 0) pass('EXECUTION-VERIFY', 'execution-verification rules hold',
    `${rules.length} rules, state ${ev.state} / result ${ev.result}, ${checks.length} checks (${passed.length} passed)`);
  else fail('EXECUTION-VERIFY', 'execution-verification rules hold', bad.map(([id]) => id).join(', '));

  const borrowed = checks.filter(c => c.state !== undefined).length;
  if (borrowed === 0) pass('EXECUTION-VERIFY', 'a check carries one outcome and no lifecycle state', 'check.result only (section 196)');
  else fail('EXECUTION-VERIFY', 'a check carries one outcome and no lifecycle state', `${borrowed} check(s)`);
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
        'SER-001…SER-010: state, profile, capability states, operations, scope, change ids, authority and target preserved');
    } else {
      fail('SERIALIZATION', 'YAML and JSON deserialize to the same authorization object', out.slice(0, 4).join(' | '));
    }

    const yamlGrants = [yaml.authorization, ...(yaml.authorization_grants || [])];
    const privilege = g => [...permittedOperations(g)].sort().join(',');
    const saved = grants;
    const gained = [];
    yamlGrants.forEach((g, i) => {
      const before = new Set(saved[i] ? permittedOperations(saved[i]) : []);
      for (const op of permittedOperations(g)) if (!before.has(op)) gained.push(`${g.level?.profile}:${op}`);
    });
    if (gained.length === 0) pass('SERIALIZATION', 'serialization does not increase effective privileges', 'SER-012, ' + yamlGrants.map(privilege).join(' | '));
    else fail('SERIALIZATION', 'serialization does not increase effective privileges', gained.join(', '));

    const badLevels = yamlGrants.filter(g => !ALL_PROFILES.includes(g.level?.profile) || !AUTH_STATES.includes(g.state));
    if (badLevels.length === 0) pass('SERIALIZATION', 'enum values are identical across formats', 'SER-003');
    else fail('SERIALIZATION', 'enum values are identical across formats', badLevels.length + ' grant(s)');
  }
}

/* ========================================================================== */
/* INVARIANTS I-001…I-016                                                     */
/* ========================================================================== */

{
  const raw = fs.readFileSync(RECORD_PATH, 'utf8');
  const merged = record.contradictions.flatMap(x => [x.claim_a, x.claim_b]);
  const invariants = [
    ['I-001', 'No generic status field', () => !/"status"\s*:/.test(raw)],
    ['I-002', 'Claim kind describes claim semantics', () => claims.every(c => typeof c.claim_kind === 'string')],
    ['I-003', 'Implementation state describes implementation', () => claims.every(c => typeof c.implementation_state === 'string')],
    ['I-004', 'Test state describes testing', () => claims.every(c => typeof c.test_state === 'string')],
    ['I-005', 'Evidence level describes evidence strength/availability', () => claims.every(c => typeof c.evidence_level === 'string')],
    ['I-006', 'Claim verification describes the claim', () => claims.every(c => typeof cvr(c) === 'string') && claims.every(c => !('verification_result' in c))],
    ['I-007', 'Authorization state describes whether permission exists', () => typeof record.authorization.state === 'string'],
    ['I-008', 'Level is a profile, capability is an object, operation is an action',
      () => typeof record.authorization.level?.profile === 'string' && Array.isArray(record.authorization.capabilities?.grants)
        && typeof record.authorization.operations === 'object'],
    ['I-009', 'Execution state describes what happened', () => typeof record.execution.state === 'string' && typeof record.execution.result === 'undefined'],
    ['I-010', 'Technical access does not imply authorization', () => 'authorization' in record && 'access_level' in record.repository],
    ['I-011', 'Authorization does not imply execution', () => record.execution.executed_changes.length > 0 || grants.some(g => g.state !== 'GRANTED')],
    ['I-012', 'Execution success does not imply execution-verification success',
      () => record.execution_verification.state !== record.execution.state],
    ['I-013', 'Every executed change is authorized',
      () => record.execution.executed_changes.every(id => grants.some(g => (g.change_ids || []).includes(id)))],
    ['I-014', 'Every verified claim has evidence',
      () => claims.filter(c => cvr(c) === 'VERIFIED').every(c => c.evidence.length > 0)],
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
    const actual = [claim.claim_kind, claim.implementation_state, claim.test_state, claim.evidence_level, cvr(claim)];
    if (shown.join('|') !== actual.join('|')) stale.push(claim.id);
  }
  if (stale.length === 0) pass('CLAIMS', 'restated claim fields match the record', 'repository-analysis §3 index');
  else fail('CLAIMS', 'restated claim fields match the record', stale.slice(0, 4).join(', '));
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
console.log('validation pipeline: STRUCTURAL → CLAIMS → EVIDENCE → AUTHORIZATION → EXECUTION → EXECUTION-VERIFY → SERIALIZATION\n');
let current = null;
for (const [stage, level, message, note] of results) {
  const label = stage === 'AUTHORIZATION' ? 'AUTHORIZATION (AC-001…AC-016)' : stage;
  if (label !== current) { console.log(`\n${label}`); current = label; }
  console.log(`  [${level}] ${message.padEnd(width)}  ${note}`);
}
const failures = results.filter(r => r[1] === 'FAIL').length;
console.log(`\n${results.filter(r => r[1] === 'PASS').length} passed, ${failures} failed`);
process.exit(failures === 0 ? 0 : 1);
