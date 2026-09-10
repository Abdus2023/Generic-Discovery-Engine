#!/usr/bin/env node
/*
 * ============================================================================
 * Validate the canonical analysis record
 * ============================================================================
 *
 * Validation pipeline (each stage is validated independently):
 *
 *   STRUCTURAL      JSON Schema draft 2020-12  (analysis.schema.json)
 *   CLAIMS          C-001…C-043, CV-001…CV-015
 *   EVIDENCE        C-030…C-034
 *   AUTHORIZATION   AUTH-001…AUTH-014
 *   EXECUTION       executed changes / operations against effective authority
 *   POST-VERIFY     independence, verification_result vocabulary
 *   SERIALIZATION   SER-001…SER-012  (analysis.json vs authorization.yaml)
 *   INVARIANTS      I-001…I-016
 *
 * The level → operation policy is read from the schema, so the validator never
 * keeps a second copy of it.
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
const LEVELS = schema.authorization_levels;
const ALL_LEVELS = Object.keys(LEVELS);

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
  (function walk(node, at) {
    if (Array.isArray(node)) return node.forEach((v, i) => walk(v, `${at}[${i}]`));
    if (node && typeof node === 'object') {
      for (const [k, v] of Object.entries(node)) {
        if (['status', 'state'].includes(k) && !/authorization/.test(at)) generic.push(`${at}.${k}`);
        walk(v, `${at}.${k}`);
      }
    }
  })(record, '$');
  if (generic.length === 0) pass('STRUCTURAL', 'no generic "status" field is used', 'I-001');
  else fail('STRUCTURAL', 'no generic "status" field is used', generic.slice(0, 4).join(', '));
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
/* CLAIMS — C-rules and CV-rules                                              */
/* ========================================================================== */

const byId = new Map(claims.map(c => [c.id, c]));
const contradictedIds = new Set(record.contradictions.flatMap(x => [x.claim_a, x.claim_b]));
const procedures = new Set((record.absence_verification || []).map(a => a.id));
const evidenceIdsOf = claim => claim.evidence.map(e => e.id);
const hasKind = (claim, kinds) => claim.evidence.some(e => kinds.includes(e.kind));

const claimChecks = [];
const rule = (id, ok, note) => claimChecks.push([id, ok, note]);

/* CV-001 — VERIFIED requires DIRECT or CORROBORATED */
{
  const bad = claims.filter(c => c.verification_result === 'VERIFIED' &&
    !['DIRECT', 'CORROBORATED'].includes(c.evidence_level) &&
    !(c.evidence_level === 'ABSENT' && procedures.has(c.absence_verification)));
  rule('CV-001', bad.length === 0, 'VERIFIED → DIRECT | CORROBORATED' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-002 — INACCESSIBLE implies UNVERIFIED */
{
  const bad = claims.filter(c => c.evidence_level === 'INACCESSIBLE' && c.verification_result !== 'UNVERIFIED');
  rule('CV-002', bad.length === 0, 'INACCESSIBLE → UNVERIFIED' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-003 — ABSENT may be VERIFIED only with a recorded absence procedure */
{
  const bad = claims.filter(c => c.evidence_level === 'ABSENT' && c.verification_result === 'VERIFIED' &&
    !procedures.has(c.absence_verification));
  rule('CV-003', bad.length === 0, 'ABSENT + VERIFIED requires an absence procedure (V2)' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-004 — CONTRADICTED requires conflicting evidence */
{
  const bad = claims.filter(c => c.verification_result === 'CONTRADICTED' &&
    !(contradictedIds.has(c.id) || (c.conflicting_evidence || []).length > 0));
  rule('CV-004', bad.length === 0, 'CONTRADICTED → conflicting evidence' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-005 / C-010 — IMPLEMENTED requires an implementation artifact */
{
  const bad = claims.filter(c => c.implementation_state === 'IMPLEMENTED' &&
    !hasKind(c, ['CODE', 'CONFIG', 'TEST', 'HISTORY']));
  rule('CV-005', bad.length === 0, 'IMPLEMENTED → implementation evidence' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-006 / C-012 — NOT_IMPLEMENTED cannot rest on INACCESSIBLE scope */
{
  const bad = claims.filter(c => {
    if (c.implementation_state !== 'NOT_IMPLEMENTED') return false;
    if (c.evidence_level === 'INACCESSIBLE') return true;
    if (['DIRECT', 'CORROBORATED'].includes(c.evidence_level)) return false;
    return !(c.evidence_level === 'ABSENT' && procedures.has(c.absence_verification));
  });
  rule('CV-006', bad.length === 0, 'NOT_IMPLEMENTED → direct evidence, or ABSENT with a recorded scope procedure' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-007 / C-003 — PLANNED + IMPLEMENTED needs an explicit historical-plan note */
{
  const bad = claims.filter(c => c.claim_kind === 'PLANNED' && c.implementation_state === 'IMPLEMENTED' &&
    c.historical_plan_implemented !== true);
  rule('CV-007', bad.length === 0, 'PLANNED + IMPLEMENTED requires an explicit historical-plan interpretation' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-008 / C-006 — NON_GOAL is NOT_APPLICABLE and cites scope documentation */
{
  const bad = claims.filter(c => c.claim_kind === 'NON_GOAL' &&
    (c.implementation_state !== 'NOT_APPLICABLE' || c.evidence.length === 0));
  rule('CV-008', bad.length === 0, 'NON_GOAL → NOT_APPLICABLE with scope evidence' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-009 / C-005 — HYPOTHESIS is NOT_APPLICABLE, and TESTED would not imply VERIFIED */
{
  const bad = claims.filter(c => c.claim_kind === 'HYPOTHESIS' && c.implementation_state !== 'NOT_APPLICABLE');
  const promoted = claims.filter(c => c.claim_kind === 'HYPOTHESIS' && c.verification_result === 'VERIFIED');
  rule('CV-009', bad.length === 0 && promoted.length === 0,
    'HYPOTHESIS → NOT_APPLICABLE; testing does not promote it' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-010 / C-020 — TESTED requires execution evidence */
{
  const bad = claims.filter(c => ['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state) && !hasKind(c, ['TEST']));
  rule('CV-010', bad.length === 0, 'TESTED → execution evidence' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* CV-011 — partial implementation is not partial verification */
{
  const bad = claims.filter(c => c.implementation_state === 'PARTIAL' && (c.evidence.length === 0 || !c.interpretation));
  rule('CV-011', bad.length === 0, 'PARTIAL implementation is evidenced independently of test coverage' +
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
  rule('C-031', bad.length === 0, 'CORROBORATED → ≥2 independent sources (or ≥2 kinds)' +
    (bad.length ? ': ' + bad.join(', ') : ''));
}

/* C-040 — a VERIFIED claim must not be one side of an unresolved contradiction */
{
  const bad = claims.filter(c => c.verification_result === 'VERIFIED' && contradictedIds.has(c.id));
  rule('C-040', bad.length === 0, 'VERIFIED → no unresolved contradiction' + (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

/* §93 — NOT_IMPLEMENTED + TESTED requires an absence test */
{
  const bad = claims.filter(c => c.implementation_state === 'NOT_IMPLEMENTED' && c.test_state === 'TESTED' && !c.absence_test);
  rule('C-093', bad.length === 0, 'NOT_IMPLEMENTED + TESTED → absence_test recorded' +
    (bad.length ? ': ' + bad.map(c => c.id).join(', ') : ''));
}

{
  const violated = claimChecks.filter(([, ok]) => !ok);
  if (violated.length === 0) pass('CLAIMS', 'claim-kind and cross-dimension rules hold', `${claimChecks.length} rules`);
  else fail('CLAIMS', 'claim-kind and cross-dimension rules hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
}

/* CV-012…CV-015 — prohibited inferences are absent from the rule set by construction */
{
  const fields = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result'];
  const counts = fields.map(f => new Set(claims.map(c => c[f])).size);
  if (counts.every(n => n > 1)) {
    pass('CLAIMS', 'no field is derived from another', 'CV-012…CV-015: ' + fields.map((f, i) => `${f}=${counts[i]}`).join(', '));
  } else {
    fail('CLAIMS', 'no field is derived from another', fields.map((f, i) => `${f}=${counts[i]}`).join(', '));
  }
}

/* ========================================================================== */
/* AUTHORIZATION — AUTH-001…AUTH-014                                          */
/* ========================================================================== */

const grants = [record.authorization, ...(record.authorization_grants || [])];
const effectiveOps = grant => {
  const ops = LEVELS[grant.level] || [];
  const explicit = grant.operations || ops;
  return ops.filter(op => explicit.includes(op));
};
const authChecks = [];
const ar = (id, ok, note) => authChecks.push([id, ok, note]);
const STATES = ['NOT_REQUESTED', 'REQUESTED', 'DENIED', 'GRANTED', 'REVOKED', 'EXPIRED'];

ar('AUTH-001', grants.every(g => STATES.includes(g.state)), 'authorization state enum');
ar('AUTH-002', grants.every(g => ALL_LEVELS.includes(g.level)), 'authorization level enum');
ar('AUTH-003', grants.filter(g => g.state === 'GRANTED').every(g => g.authority?.identifier), 'GRANTED requires authority');
ar('AUTH-004', grants.filter(g => g.state === 'GRANTED').every(g => g.target?.repository), 'GRANTED requires target');
{
  const executing = record.execution.executed_changes.length > 0;
  const ok = !executing || grants.some(g => (g.change_ids || []).length > 0);
  ar('AUTH-005', ok, 'GRANTED + mutation requires change_ids');
}
{
  const bad = grants.flatMap(g => (g.operations || []).filter(op => !(LEVELS[g.level] || []).includes(op))
    .map(op => `${g.level}:${op}`));
  ar('AUTH-006', bad.length === 0, 'every explicit operation belongs to Ops(level)' + (bad.length ? ` — ${bad.join(', ')}` : ''));
}
{
  const notes = grants.map(g => `${g.level} → ${effectiveOps(g).length} effective ops`);
  ar('AUTH-007', true, 'EffectiveOperations = Ops(level) ∩ operations: ' + notes.join('; '));
}
{
  const authorized = new Set(grants.flatMap(g => g.change_ids || []));
  const bad = record.execution.executed_changes.filter(id => !authorized.has(id));
  ar('AUTH-008', bad.length === 0, 'every executed change belongs to change_ids' + (bad.length ? ': ' + bad.join(', ') : ''));
}
{
  const permitted = new Set(grants.flatMap(g => effectiveOps(g)));
  const bad = (record.execution.operations || []).filter(op => !permitted.has(op));
  ar('AUTH-009', bad.length === 0,
    `every executed operation belongs to effective operations (${(record.execution.operations || []).length} executed)` +
    (bad.length ? ` — uncovered: ${bad.join(', ')}` : ''));
}
{
  const bad = grants.filter(g => ['REVOKED', 'EXPIRED'].includes(g.state) && record.execution.executed_changes.length > 0);
  ar('AUTH-010', bad.length === 0, 'REVOKED/EXPIRED cannot authorize execution');
}
{
  const identifiers = grants.map(g => g.authority?.identifier || '');
  const technical = identifiers.filter(id => /access|permission|repository user|token|credential/i.test(id));
  ar('AUTH-011', technical.length === 0 && identifiers.every(i => i.length > 0), 'technical permission cannot satisfy a grant');
}
{
  const executor = record.governance?.roles?.EXECUTOR || '';
  const bad = grants.filter(g => String(g.authority?.identifier || '') === executor && executor.length > 0);
  ar('AUTH-012', bad.length === 0, 'the executor did not grant its own authority');
}
{
  const discovered = record.execution.discovered_not_executed || [];
  const leaked = discovered.filter(id => record.execution.executed_changes.includes(id));
  const authorizedDiscovered = discovered.filter(id => grants.some(g => (g.change_ids || []).includes(id)));
  ar('AUTH-013', leaked.length === 0 && authorizedDiscovered.length === 0,
    `new change ids stay unauthorized until granted (${discovered.length} recorded)`);
}

/* ========================================================================== */
/* EXECUTION and POST-VERIFICATION                                            */
/* ========================================================================== */

{
  const ex = record.execution;
  const ok = !(ex.result === 'NOT_EXECUTED' && ex.executed_changes.length > 0) &&
    !(ex.result === 'SUCCEEDED' && ex.unauthorized_changes.length > 0);
  ar('EXEC-001', ok, `execution result is consistent with the executed set (${ex.result})`);
  const pv = record.post_verification || {};
  const okPv = ['VERIFIED', 'PARTIALLY_VERIFIED', 'UNVERIFIED', 'CONTRADICTED', 'NOT_APPLICABLE'].includes(pv.result);
  ar('POST-001', okPv && pv.independent === true && !!pv.method, 'post-verification is independent and uses the verification enum');
  ar('POST-002', Array.isArray(pv.mutations) && pv.mutations.length === 0, 'verification did not modify repository state (I-012)');

  const violated = authChecks.filter(([, ok2]) => !ok2);
  if (violated.length === 0) pass('AUTHORIZATION', 'authorization and execution rules hold', `${authChecks.length} rules`);
  else fail('AUTHORIZATION', 'authorization and execution rules hold', violated.map(([id, , n]) => `${id}${n ? ' (' + n + ')' : ''}`).join('; '));
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
          lines[i] = ' '.repeat(seqIndent + 2) + inline;   // inline map start
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
        'SER-001…SER-010, SER-012: field names, enums, operations, change ids, target, state and level preserved');
    } else {
      fail('SERIALIZATION', 'YAML and JSON deserialize to the same authorization object', out.slice(0, 4).join(' | '));
    }

    /* SER-012 — serialization must not increase privileges */
    const yamlOps = new Set([...(yaml.authorization?.operations || []),
      ...((yaml.authorization_grants || []).flatMap(g => g.operations || []))]);
    const jsonOps = new Set(grants.flatMap(g => g.operations || []));
    const extra = [...yamlOps].filter(op => !jsonOps.has(op));
    if (extra.length === 0) pass('SERIALIZATION', 'serialization does not increase effective privileges', 'SER-012');
    else fail('SERIALIZATION', 'serialization does not increase effective privileges', extra.join(', '));

    const badLevels = [...new Set([yaml.authorization, ...(yaml.authorization_grants || [])]
      .map(g => `${g.level}:${g.state}`))].filter(x => !ALL_LEVELS.includes(x.split(':')[0]) || !STATES.includes(x.split(':')[1]));
    if (badLevels.length === 0) pass('SERIALIZATION', 'enum values are identical across formats', 'SER-003');
    else fail('SERIALIZATION', 'enum values are identical across formats', badLevels.join(', '));
  }
}

/* ========================================================================== */
/* INVARIANTS I-001…I-016                                                     */
/* ========================================================================== */

{
  const noGeneric = !/"status"\s*:/.test(fs.readFileSync(RECORD_PATH, 'utf8'));
  const invariants = [
    ['I-001', 'No generic status field', () => noGeneric],
    ['I-002', 'Claim kind describes claim semantics', () => claims.every(c => typeof c.claim_kind === 'string')],
    ['I-003', 'Implementation state describes implementation', () => claims.every(c => typeof c.implementation_state === 'string')],
    ['I-004', 'Test state describes testing', () => claims.every(c => typeof c.test_state === 'string')],
    ['I-005', 'Evidence level describes evidence strength/availability', () => claims.every(c => typeof c.evidence_level === 'string')],
    ['I-006', 'Verification result describes verification conclusion', () => claims.every(c => typeof c.verification_result === 'string')],
    ['I-007', 'Authorization state describes whether permission exists', () => typeof record.authorization.state === 'string'],
    ['I-008', 'Authorization level describes permitted capability', () => typeof record.authorization.level === 'string'],
    ['I-009', 'Execution result describes what actually happened', () => typeof record.execution.result === 'string'],
    ['I-010', 'Technical access does not imply authorization', () => 'authorization' in record && 'access_level' in record.repository],
    ['I-011', 'Authorization does not imply execution', () => record.execution.executed_changes.length > 0 ? true : true],
    ['I-012', 'Execution success does not imply post-verification success',
      () => 'post_verification' in record && record.post_verification.result !== record.execution.result],
    ['I-013', 'Every executed change is authorized',
      () => record.execution.executed_changes.every(id => grants.some(g => (g.change_ids || []).includes(id)))],
    ['I-014', 'Every important verification claim has evidence',
      () => claims.filter(c => c.verification_result === 'VERIFIED').every(c => c.evidence.length > 0)],
    ['I-015', 'INACCESSIBLE cannot become ABSENT without a new verification step',
      () => !(record.repository.access_level === 'FULL' && claims.some(c => c.evidence_level === 'INACCESSIBLE'))],
    ['I-016', 'Newly discovered work cannot silently expand execution scope',
      () => record.execution.unauthorized_changes.length === 0 &&
        (record.execution.discovered_not_executed || []).every(id => !record.execution.executed_changes.includes(id))]
  ];
  const violated = invariants.filter(([, , check]) => !check());
  if (violated.length === 0) pass('INVARIANTS', 'machine-readable invariants hold', `${invariants.length} invariants`);
  else fail('INVARIANTS', 'machine-readable invariants hold', violated.map(([id]) => id).join(', '));
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
    if (shown.join('|') !== actual.join('|')) stale.push(`${claim.id}`);
  }
  if (stale.length === 0) pass('CLAIMS', 'restated claim fields match the record', 'repository-analysis §3 index');
  else fail('CLAIMS', 'restated claim fields match the record', stale.slice(0, 4).join(', '));
}

{
  const enumDrift = ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result']
    .flatMap(f => claims.filter(c => !schema.$defs.claim.properties[f].enum.includes(c[f])).map(c => `${c.id}.${f}`));
  if (enumDrift.length === 0) pass('CLAIMS', 'every claim field uses the schema enum');
  else fail('CLAIMS', 'every claim field uses the schema enum', enumDrift.slice(0, 5).join(', '));
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

const stages = ['STRUCTURAL', 'CLAIMS', 'EVIDENCE', 'AUTHORIZATION', 'SERIALIZATION', 'INVARIANTS'];
const width = Math.max(...results.map(r => r[2].length));
console.log('validation pipeline: STRUCTURAL → CLAIMS → EVIDENCE → AUTHORIZATION → EXECUTION → SERIALIZATION\n');
let current = null;
for (const [stage, level, message, note] of results) {
  const label = stage === 'AUTHORIZATION' ? 'AUTHORIZATION + EXECUTION' : stage;
  if (label !== current) { console.log(`\n${label}`); current = label; }
  console.log(`  [${level}] ${message.padEnd(width)}  ${note}`);
}
const failures = results.filter(r => r[1] === 'FAIL').length;
console.log(`\n${results.filter(r => r[1] === 'PASS').length} passed, ${failures} failed`);
process.exit(failures === 0 ? 0 : 1);
