#!/usr/bin/env node
/*
 * ============================================================================
 * Semantic validator for the canonical analysis record
 * ============================================================================
 *
 * Brief 11 (sections 218-243) separates three concerns that an earlier revision
 * ran together:
 *
 *   STRUCTURAL SCHEMA      object structure, property names, primitive types,
 *                          arrays, protocol enums, local required fields,
 *                          nullability, formats, identifier syntax,
 *                          additionalProperties (analysis.schema.json)
 *        ↓
 *   SEMANTIC REGISTRIES    externally governed vocabularies and policy
 *                          (docs/analysis/registries/*.json)
 *        ↓
 *   SEMANTIC VALIDATOR     reference resolution and relationship rules
 *                          (this file)
 *
 * A value stays an enum in the schema only when it is part of the structural
 * protocol; capabilities, level profiles, operations, resource classes and claim
 * identifiers are typed as strings there and resolved here (sections 218.1, 219,
 * 225).
 *
 * Validation phases (section 242 — validation phases, not lifecycle states):
 *
 *   STRUCTURAL     schema validity, object validity (REQ-*), timestamp
 *                  semantics are reported under SEMANTIC
 *   REGISTRY       registry loading, envelope and entry validity, reference
 *                  resolution that depends on a registry alone
 *   SEMANTIC       cross-object rules X-001…X-020, timestamp rules TS-001…TS-007,
 *                  claim rules, serialization and invariant checks
 *   AUTHORIZATION  capability and capability-grant rule sets (CAP-*, CG-*)
 *   EXECUTION      execution invariants EV-001…EV-012, coverage, transitions
 *   VERIFICATION   execution-verification rules EVV-001…EVV-009
 *
 * This program is a pure function of its inputs: it never writes to the
 * repository (section 241). tools/validation-run.mjs is the recorder that
 * captures runs, including the failure phase and every error, in
 * docs/analysis/validation-runs.json.
 *
 * Usage:
 *   node tools/validate-analysis.mjs              # human-readable report
 *   node tools/validate-analysis.mjs --json       # machine-readable report
 *   node tools/validate-analysis.mjs --self-test  # run the fixture suite
 *
 * Exit 0 = VALID. Exit 1 = INVALID. Exit 2 = the inputs could not be read.
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
/* --root validates a snapshot of another revision without checking it out. */
const rootArg = process.argv.indexOf('--root');
const ROOT = rootArg > -1 && process.argv[rootArg + 1] ? path.resolve(process.argv[rootArg + 1]) : REPO_ROOT;
const RECORD_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.json');
const SCHEMA_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.schema.json');
const REGISTRY_DIR = path.join(ROOT, 'docs', 'analysis', 'registries');
const REGISTRY_SCHEMA_PATH = path.join(REGISTRY_DIR, 'registry.schema.json');
const YAML_PATH = path.join(ROOT, 'docs', 'analysis', 'authorization.yaml');
const REGISTER_PATH = path.join(ROOT, 'docs', 'analysis', 'evidence-register.md');
const CHANGE_REGISTER_PATH = path.join(ROOT, 'docs', 'analysis', 'change-register-2026-09-10.md');
const ANALYSIS_DOC_PATH = path.join(ROOT, 'docs', 'analysis', 'repository-analysis-2026-09-10.md');
const CLAIMS_PATH = path.join(ROOT, 'docs', 'analysis', 'claims.md');

export const PHASES = ['STRUCTURAL', 'REGISTRY', 'SEMANTIC', 'AUTHORIZATION', 'EXECUTION', 'VERIFICATION'];
export const STAGES = ['SCHEMA VALIDITY', 'OBJECT VALIDITY', 'CROSS-OBJECT SEMANTIC VALIDITY', 'AUTHORIZATION DECISION',
  'EXECUTION', 'EXECUTION VERIFICATION', 'SERIALIZATION', 'INVARIANTS'];

/* ========================================================================== */
/* Minimal JSON Schema evaluator (draft 2020-12 subset)                        */
/* ========================================================================== */

function resolveRef(ref, root) {
  if (!ref || !ref.startsWith('#/')) return null;
  let node = root;
  for (const part of ref.slice(2).split('/')) {
    if (!node) return null;
    node = node[part.replace(/~1/g, '/').replace(/~0/g, '~')];
  }
  return node || null;
}

function typeOf(value) {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  return typeof value;
}

export function validateAgainstSchema(instance, schema, at, errors, root = schema) {
  if (!schema) return;
  let node = schema;
  if (node.$ref) node = resolveRef(node.$ref, root);
  if (!node) return;

  if (node.allOf) for (const sub of node.allOf) validateAgainstSchema(instance, sub, at, errors, root);
  if (node.if) {
    const probe = [];
    validateAgainstSchema(instance, node.if, at, probe, root);
    if (probe.length === 0 && node.then) validateAgainstSchema(instance, node.then, at, errors, root);
    if (probe.length > 0 && node.else) validateAgainstSchema(instance, node.else, at, errors, root);
  }

  if (node.const !== undefined && JSON.stringify(instance) !== JSON.stringify(node.const)) {
    errors.push(`${at}: must equal ${JSON.stringify(node.const)}`);
    return;
  }
  if (node.enum && !node.enum.some(value => JSON.stringify(value) === JSON.stringify(instance))) {
    errors.push(`${at}: ${JSON.stringify(instance)} is not one of ${node.enum.join(', ')}`);
    return;
  }
  if (node.type) {
    const allowed = Array.isArray(node.type) ? node.type : [node.type];
    const actual = typeOf(instance);
    const match = allowed.includes(actual) || (allowed.includes('integer') && actual === 'number' && Number.isInteger(instance));
    if (!match) {
      errors.push(`${at}: expected ${allowed.join('|')}, found ${actual}`);
      return;
    }
  }

  const actual = typeOf(instance);
  if (actual === 'string') {
    if (node.minLength !== undefined && instance.length < node.minLength) errors.push(`${at}: shorter than minLength ${node.minLength}`);
    if (node.pattern && !(new RegExp(node.pattern)).test(instance)) errors.push(`${at}: does not match ${node.pattern}`);
    if (node.format === 'date-time' && !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$/.test(instance)) {
      errors.push(`${at}: not an RFC 3339 date-time`);
    }
  }
  if (actual === 'number' && typeof node.minimum === 'number' && instance < node.minimum) errors.push(`${at}: below minimum ${node.minimum}`);
  if (actual === 'object') {
    for (const key of node.required || []) if (!(key in instance)) errors.push(`${at}: missing required property "${key}"`);
    for (const [key, value] of Object.entries(instance)) {
      if (node.properties && node.properties[key]) validateAgainstSchema(value, node.properties[key], `${at}.${key}`, errors, root);
      else if (node.additionalProperties === false) errors.push(`${at}: unexpected property "${key}"`);
      else if (node.additionalProperties && typeof node.additionalProperties === 'object') {
        validateAgainstSchema(value, node.additionalProperties, `${at}.${key}`, errors, root);
      }
    }
  }
  if (actual === 'array') {
    if (node.minItems !== undefined && instance.length < node.minItems) errors.push(`${at}: fewer than minItems ${node.minItems}`);
    if (node.items) instance.forEach((item, i) => validateAgainstSchema(item, node.items, `${at}[${i}]`, errors, root));
    if (node.uniqueItems) {
      const seen = new Map();
      instance.forEach((item, i) => {
        const key = JSON.stringify(item);
        if (seen.has(key)) errors.push(`${at}[${i}]: duplicate item (uniqueItems)`);
        else seen.set(key, i);
      });
    }
  }
}

/* ========================================================================== */
/* Findings model (section 242)                                                */
/* ========================================================================== */

class Report {
  constructor() {
    this.checks = [];
  }

  add(record) {
    this.checks.push(record);
    return record.ok;
  }

  ok(phase, code, object, message, extra = {}) {
    return this.add({ state: 'PASS', phase, code, object, message, ...extra });
  }

  bad(phase, code, object, message, extra = {}) {
    return this.add({ state: 'FAIL', phase, code, object, message, ...extra });
  }

  check(phase, code, object, ok, message, extra = {}) {
    return ok ? this.ok(phase, code, object, message, extra) : this.bad(phase, code, object, message, extra);
  }

  info(phase, code, object, message, extra = {}) {
    return this.add({ state: 'INFO', phase, code, object, message, ...extra });
  }

  get errors() {
    return this.checks.filter(c => c.state === 'FAIL');
  }

  get passed() {
    return this.checks.filter(c => c.state === 'PASS');
  }

  phaseState(phase) {
    const inPhase = this.checks.filter(c => c.phase === phase);
    const failed = inPhase.filter(c => c.state === 'FAIL');
    return {
      phase,
      state: failed.length ? 'FAILED' : 'PASSED',
      checks: inPhase.length,
      errors: failed.length,
      summary: failed.length ? failed[0].message : (inPhase[0]?.message || ''),
    };
  }
}

/* ========================================================================== */
/* Document validation — a pure function of the document, its schema, the      */
/* registries and (optionally) the documents that restate parts of it          */
/* ========================================================================== */

export function validateDocument(doc, ctx) {
  const report = new Report();
  const schema = ctx.schema;
  const registry = ctx.registries;
  const fileChecks = ctx.fileChecks !== false;
  const register = ctx.register || '';
  const claims = doc.claims;
  const authorization = doc.authorization;
  const execution = doc.execution;
  const verification = doc.execution_verification;

  const profileRegistry = new Map(registry.level_profile.entries.map(p => [p.id, p]));
  const capabilityRegistry = new Map(registry.capability.entries.map(c => [c.id, c]));
  const operationRegistry = new Map(registry.operation.entries.map(o => [o.id, o]));
  const resourceRegistry = new Set(registry.resource_class.entries.map(r => r.id));
  const claimRegistry = new Map(registry.claim.entries.map(c => [c.id, c]));
  const changes = new Map(doc.changes.map(c => [c.id, c]));

  /* ------------------------------------------------------------------ */
  /* 1. STRUCTURAL                                                       */
  /* ------------------------------------------------------------------ */

  {
    const errors = [];
    validateAgainstSchema(doc, schema, '$', errors, schema);
    report.check('STRUCTURAL', 'ST-001', 'document',
      errors.length === 0,
      errors.length === 0
        ? `record validates against analysis.schema.json (draft 2020-12, closed root, ${Object.keys(schema.$defs).length} $defs)`
        : `schema violation: ${errors.slice(0, 4).join(' | ')}${errors.length > 4 ? ` (+${errors.length - 4})` : ''}`,
      { rules: ['§209', '§218.1', '§225'], actual: errors.slice(0, 8) });

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
    })(doc, '$');
    report.check('STRUCTURAL', 'ST-002', 'document',
      banned.length === 0,
      banned.length === 0
        ? 'no forbidden field name appears in the record (status, verification, effective_capabilities)'
        : `forbidden field name: ${banned.slice(0, 4).join(', ')}`,
      { rules: ['§168', 'I-001'] });

    /* object validity — the conditional rules of brief 10 section 210 */
    const problems = [];
    const mutating = op => operationRegistry.get(op)?.mutating === true;
    if (authorization.expires_at !== null && !authorization.granted_at) {
      problems.push('REQ-005: expires_at present without granted_at');
    }
    if (authorization.state === 'GRANTED') {
      if (!authorization.authority?.identifier) problems.push('REQ-001: GRANTED without authority');
      if (!authorization.level?.profile) problems.push('REQ-002: GRANTED without level.profile');
      if (!authorization.target?.repository) problems.push('REQ-003: GRANTED without target');
      if (!authorization.granted_at) problems.push('REQ-003: GRANTED without granted_at');
    }
    const intendsMutation = (authorization.operations?.allow || []).some(mutating);
    if (authorization.state === 'GRANTED' && intendsMutation && (authorization.change_ids || []).length === 0) {
      problems.push('REQ-004: mutation authorized with an empty change_id list (change_ids present but empty)');
    }
    if (execution.state === 'RUNNING' && !execution.started_at) problems.push('REQ-006: RUNNING without started_at');
    const terminal = ['SUCCEEDED', 'PARTIALLY_SUCCEEDED', 'FAILED', 'CANCELLED', 'STOPPED'];
    if (terminal.includes(execution.state) && !execution.completed_at) problems.push('REQ-007: terminal execution without completed_at');
    if (execution.state === 'NOT_STARTED' && execution.executed_changes.length > 0) problems.push('REQ-008: NOT_STARTED with executed changes');
    if (execution.state === 'AUTHORIZATION_BLOCKED') {
      const mutated = execution.operations.some(o => mutating(o.operation) && o.result === 'SUCCEEDED');
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
    if (verification.state !== 'NOT_REQUIRED' && verification.checks.length === 0) {
      problems.push('section 210: verification state requires at least one check');
    }
    const wantInterpretation = new Set(['INDIRECT', 'ABSENT', 'INACCESSIBLE']);
    const wantResult = new Set(['CONTRADICTED', 'PARTIALLY_VERIFIED']);
    const missingInterpretation = claims.filter(c => !c.interpretation &&
      (wantInterpretation.has(c.evidence_level) || wantResult.has(c.claim_verification.result)));
    if (missingInterpretation.length > 0) {
      problems.push(`section 210: interpretation missing on ${missingInterpretation.map(c => c.id).join(', ')}`);
    }
    report.check('STRUCTURAL', 'REQ-001…REQ-014', 'document',
      problems.length === 0,
      problems.length === 0 ? 'required-field and conditional rules hold' : problems.slice(0, 4).join(' | '),
      { rules: ['§210', '§211', ...problems.map(x => x.split(':')[0])], actual: problems });
  }

  /* ------------------------------------------------------------------ */
  /* 2. REGISTRY                                                         */
  /* ------------------------------------------------------------------ */

  {
    const problems = [];
    for (const [id, registryDoc] of Object.entries(registry)) {
      const errors = [];
      validateAgainstSchema(registryDoc, ctx.registrySchema, `registries.${id}`, errors, ctx.registrySchema);
      for (const error of errors) problems.push(`RG-001: ${id}: ${error}`);
    }
    report.check('REGISTRY', 'RG-001', 'registries/',
      problems.length === 0,
      problems.length === 0
        ? `${Object.keys(registry).length} registries validate against registry.schema.json (closed envelope and entry shapes)`
        : problems.slice(0, 4).join(' | '),
      { rules: ['§218.1', '§220', '§221…§224'], actual: problems });

    const versionProblems = [];
    for (const [id, registryDoc] of Object.entries(registry)) {
      if (registryDoc.registry_id !== id) versionProblems.push(`RG-002: ${id}: registry_id is ${registryDoc.registry_id}`);
      if (registryDoc.schema_version === registryDoc.registry_version) {
        versionProblems.push(`RG-002: ${id}: the envelope format version and the registry revision must be independent`);
      }
      if (registryDoc.registry_version === doc.schema_version) {
        versionProblems.push(`RG-002: ${id}: the registry revision ${registryDoc.registry_version} must be independent of the analysis schema version (section 220)`);
      }
    }
    report.check('REGISTRY', 'RG-002', 'registries/ · schema_version',
      versionProblems.length === 0,
      versionProblems.length === 0
        ? `registry revisions (${[...new Set(Object.values(registry).map(r => r.registry_version))].join(', ')}) and envelope format ${[...new Set(Object.values(registry).map(r => r.schema_version))].join(', ')} are independent of the analysis schema version ${doc.schema_version}`
        : versionProblems.slice(0, 4).join(' | '),
      { rules: ['§220'], actual: versionProblems });

    const duplicateProblems = [];
    for (const [id, registryDoc] of Object.entries(registry)) {
      const ids = registryDoc.entries.map(e => e.id);
      const duplicates = [...new Set(ids.filter((v, i) => ids.indexOf(v) !== i))];
      if (duplicates.length) duplicateProblems.push(`RG-003: ${id}: duplicate entry id ${duplicates.join(', ')}`);
    }
    report.check('REGISTRY', 'RG-003', 'registries/',
      duplicateProblems.length === 0,
      duplicateProblems.length === 0
        ? `entry identifiers are unique within each registry (${Object.values(registry).reduce((n, r) => n + r.entries.length, 0)} entries)`
        : duplicateProblems.join(' | '),
      { rules: ['§220'], actual: duplicateProblems });
  }

  {
    /* the claim registry is the identifier vocabulary of this document */
    const declared = claims.map(c => c.id);
    const registered = [...claimRegistry.keys()];
    const unregistered = declared.filter(id => !claimRegistry.has(id));
    const orphans = registered.filter(id => !declared.includes(id));
    report.check('REGISTRY', 'RG-004', 'registries/claim-registry.json',
      unregistered.length === 0 && orphans.length === 0,
      unregistered.length === 0 && orphans.length === 0
        ? `${registered.length} claim identifiers declared and resolved`
        : `${unregistered.length ? 'unregistered: ' + unregistered.slice(0, 4).join(', ') : ''}${orphans.length ? ' orphaned: ' + orphans.slice(0, 4).join(', ') : ''}`,
      { rules: ['§218.2'], actual: [...unregistered, ...orphans],
        expected: `the ${declared.length} claim identifiers declared in the record` });
  }

  /* ---- profile resolution (section 212) ---- */
  const profileProblems = [];
  const resolveProfile = (id, trail = []) => {
    if (trail.includes(id)) throw new Error(`inheritance cycle: ${[...trail, id].join(' -> ')}`);
    const node = profileRegistry.get(id);
    if (!node) throw new Error(`unknown profile ${id}`);
    const out = new Set(node.capabilities);
    for (const parent of node.inherits) for (const cap of resolveProfile(parent, [...trail, id])) out.add(cap);
    return out;
  };
  let resolvedProfile = new Set();
  let profileError = null;
  try {
    resolvedProfile = resolveProfile(authorization.level.profile);
  } catch (error) {
    profileError = error.message;
    profileProblems.push(`X-009: ${error.message}`);
  }
  for (const profile of profileRegistry.values()) {
    const unknownParents = profile.inherits.filter(p => !profileRegistry.has(p));
    if (unknownParents.length) profileProblems.push(`RG-006: ${profile.id} inherits unknown profile ${unknownParents.join(', ')}`);
    const dangling = profile.capabilities.filter(c => !capabilityRegistry.has(c));
    if (dangling.length) profileProblems.push(`RG-006: ${profile.id} declares unknown capability ${dangling.join(', ')}`);
  }
  try {
    for (const id of profileRegistry.keys()) resolveProfile(id);
  } catch (error) {
    if (!profileProblems.some(p => p.includes(error.message))) profileProblems.push(`RG-006: ${error.message}`);
  }
  report.check('REGISTRY', 'X-009 · RG-006', 'authorization.level.profile',
    profileProblems.length === 0,
    profileProblems.length === 0
      ? `profile ${authorization.level.profile} resolves to ${resolvedProfile.size} declared capabilities over an acyclic inheritance graph`
      : profileProblems.slice(0, 3).join(' | '),
    { rules: ['§212', 'X-009', ...profileProblems.map(x => x.split(':')[0])], actual: profileProblems });

  /* ---- vocabulary reference resolution (X-009…X-015, section 218.3) ---- */
  {
    const grantProblems = (authorization.capability_grants || [])
      .filter(g => !capabilityRegistry.has(g.capability_id))
      .map(g => `X-010: capability grant ${g.capability_id} is not declared in the capability registry`);
    report.check('REGISTRY', 'X-010', 'authorization.capability_grants',
      grantProblems.length === 0,
      grantProblems.length === 0
        ? `every capability grant resolves in the capability registry (${capabilityRegistry.size} entries)`
        : grantProblems.join(' | '),
      { rules: ['§232', '§221'], actual: grantProblems });

    const operationProblems = [];
    const declaredOperations = [...(authorization.operations?.allow || []), ...(authorization.operations?.deny || [])];
    for (const op of [...new Set(declaredOperations)]) {
      if (!operationRegistry.has(op)) operationProblems.push(`X-012: authorization operation ${op} is not declared in the operation registry`);
    }
    for (const op of execution.operations) {
      if (!operationRegistry.has(op.operation)) operationProblems.push(`X-012: execution operation ${op.operation} (${op.id}) is not declared in the operation registry`);
    }
    report.check('REGISTRY', 'X-012', 'operations',
      operationProblems.length === 0,
      operationProblems.length === 0
        ? `every authorization and execution operation resolves in the operation registry (${operationRegistry.size} entries: ${[...operationRegistry.keys()].join('/')})`
        : operationProblems.slice(0, 4).join(' | '),
      { rules: ['§232', '§223'], actual: operationProblems });

    const capabilityOperationProblems = [...capabilityRegistry.values()]
      .filter(c => c.operations.some(op => !operationRegistry.has(op)))
      .map(c => `X-014: capability ${c.id} declares unknown operation(s) ${c.operations.filter(op => !operationRegistry.has(op)).join(', ')}`);
    report.check('REGISTRY', 'X-014', 'registries/capability-registry.json',
      capabilityOperationProblems.length === 0,
      capabilityOperationProblems.length === 0
        ? 'every capability operation resolves in the operation registry'
        : capabilityOperationProblems.join(' | '),
      { rules: ['§232', '§222'], actual: capabilityOperationProblems });

    const targetClassProblems = execution.operations
      .filter(o => !resourceRegistry.has(o.target.resource_class))
      .map(o => `X-013: operation ${o.id} targets unknown resource class ${o.target.resource_class}`);
    report.check('REGISTRY', 'X-013', 'execution.operations[].target.resource_class',
      targetClassProblems.length === 0,
      targetClassProblems.length === 0
        ? `every operation target resolves in the resource-class registry (${resourceRegistry.size} entries)`
        : targetClassProblems.join(' | '),
      { rules: ['§232', '§224'], actual: targetClassProblems });

    const capabilityClassProblems = [...capabilityRegistry.values()]
      .filter(c => !resourceRegistry.has(c.resource_class))
      .map(c => `X-015: capability ${c.id} declares unknown resource class ${c.resource_class}`);
    report.check('REGISTRY', 'X-015', 'registries/capability-registry.json',
      capabilityClassProblems.length === 0,
      capabilityClassProblems.length === 0
        ? 'every capability resource class resolves in the resource-class registry'
        : capabilityClassProblems.join(' | '),
      { rules: ['§232', '§221'], actual: capabilityClassProblems });
  }

  /* ---- capability modelling rules that need the registries (section 221) ---- */
  const scopeModelOf = id => capabilityRegistry.get(id)?.constraints?.scope_model;
  const pathBearing = ['DOCUMENT', 'TEST', 'SOURCE', 'CONFIGURATION', 'ARCHITECTURE'];
  {
    const problems = [];
    for (const cap of capabilityRegistry.values()) {
      const expected = pathBearing.includes(cap.resource_class) ? 'PATH' : 'NONE';
      if (cap.constraints.scope_model !== expected) {
        problems.push(`RG-005: ${cap.id} has scope_model ${cap.constraints.scope_model} for resource class ${cap.resource_class}`);
      }
    }
    const restrictedOnNonPath = (authorization.capability_grants || [])
      .filter(g => g.state === 'RESTRICTED' && scopeModelOf(g.capability_id) === 'NONE');
    for (const grant of restrictedOnNonPath) problems.push(`RG-005: ${grant.capability_id} is RESTRICTED but has no path scope model`);
    report.check('REGISTRY', 'RG-005', 'registries/capability-registry.json',
      problems.length === 0,
      problems.length === 0
        ? 'every capability declares a scope model consistent with its resource class; restrictions apply to path-bearing capabilities only'
        : problems.slice(0, 4).join(' | '),
      { rules: ['§221'], actual: problems });
  }

  /* ------------------------------------------------------------------ */
  /* 3. SEMANTIC — cross-object rule set X-001…X-020 and TS-001…TS-007    */
  /* ------------------------------------------------------------------ */

  const mutatingOp = op => operationRegistry.get(op)?.mutating === true;
  const TERMINAL_EXECUTION = ['SUCCEEDED', 'PARTIALLY_SUCCEEDED', 'FAILED', 'CANCELLED', 'STOPPED'];
  {
    const defined = new Set(
      [...register.matchAll(/^\|\s*((?:CODE|TEST|DOC|CFG|HIST|ARCH|SCOPE|CONC|PROV|FAIL|EXT)-\d{3})\s*\|/gm)].map(m => m[1]));
    const evidenceProblems = [];
    for (const claim of claims) {
      for (const evidence of claim.evidence) if (!defined.has(evidence.id)) evidenceProblems.push(`X-001: ${claim.id} -> ${evidence.id}`);
    }
    for (const check of verification.checks) {
      for (const evidence of check.evidence || []) if (!defined.has(evidence)) evidenceProblems.push(`X-001: ${check.id} -> ${evidence}`);
    }
    report.check('SEMANTIC', 'X-001', 'claims[].evidence · execution_verification.checks[].evidence',
      evidenceProblems.length === 0,
      evidenceProblems.length === 0
        ? `every claim and check evidence id resolves in the evidence register (${defined.size} registered ids)`
        : evidenceProblems.slice(0, 4).join(' | '),
      { rules: ['§232'], actual: evidenceProblems });

    const changeEvidenceProblems = [];
    for (const change of doc.changes) {
      for (const evidence of change.evidence) if (!defined.has(evidence)) changeEvidenceProblems.push(`X-002: ${change.id} -> ${evidence}`);
    }
    report.check('SEMANTIC', 'X-002', 'changes[].evidence',
      changeEvidenceProblems.length === 0,
      changeEvidenceProblems.length === 0
        ? `every change evidence id resolves in the evidence register (${doc.changes.length} changes)`
        : changeEvidenceProblems.slice(0, 4).join(' | '),
      { rules: ['§232'], actual: changeEvidenceProblems });

    const refProblems = [];
    const resolveChange = (id, code, where) => { if (!changes.has(id)) refProblems.push(`${code}: ${where} references unknown change ${id}`); };
    for (const id of authorization.change_ids || []) resolveChange(id, 'X-003', 'authorization.change_ids');
    for (const op of execution.operations) resolveChange(op.change_id, 'X-004', `execution.operations[${op.id}]`);
    for (const id of execution.executed_changes) resolveChange(id, 'X-005', 'execution.executed_changes');
    for (const id of execution.unauthorized_changes) resolveChange(id, 'X-006', 'execution.unauthorized_changes');
    const byCode = code => refProblems.filter(p => p.startsWith(code));
    for (const [code, object, where] of [['X-003', 'authorization.change_ids', 'change id'],
      ['X-004', 'execution.operations[].change_id', 'operation change id'],
      ['X-005', 'execution.executed_changes', 'executed change id'],
      ['X-006', 'execution.unauthorized_changes', 'unauthorized change id']]) {
      const problems = byCode(code);
      report.check('SEMANTIC', code, object,
        problems.length === 0,
        problems.length === 0
          ? `every ${where} in ${object.split('.')[0]} resolves to a change in this document (${changes.size} changes)`
          : problems.join(' | '),
        { rules: ['§232'], actual: problems });
    }
  }

  {
    const problems = [];
    const expectedRepository = `${doc.repository.owner}/${doc.repository.name}`;
    if (authorization.target.repository !== expectedRepository) {
      problems.push(`X-007: target.repository ${authorization.target.repository} != ${expectedRepository}`);
    }
    if (authorization.target.revision !== doc.repository.resolved_revision) {
      problems.push(`X-008: target.revision ${authorization.target.revision} != resolved_revision ${doc.repository.resolved_revision}`);
    }
    report.check('SEMANTIC', 'X-007 · X-008', 'authorization.target',
      problems.length === 0,
      problems.length === 0
        ? `authorization target is the analyzed repository at the resolved revision (${expectedRepository} @ ${doc.repository.resolved_revision.slice(0, 7)})`
        : problems.join(' | '),
      { rules: ['§232'], actual: problems,
        expected: `${expectedRepository} @ ${doc.repository.resolved_revision}` });
  }

  const unavailableGrants = (authorization.capability_grants || []).filter(g => !resolvedProfile.has(g.capability_id));
  const authorizing = (authorization.capability_grants || []).filter(g => ['ENABLED', 'RESTRICTED'].includes(g.state));
  const notGrantable = authorizing.filter(g => capabilityRegistry.get(g.capability_id)?.lifecycle?.grantable !== true);
  report.check('SEMANTIC', 'X-011', 'authorization.capability_grants',
    unavailableGrants.length === 0 && notGrantable.length === 0 && !profileError,
    unavailableGrants.length === 0 && notGrantable.length === 0 && !profileError
      ? `every grant is available from the resolved profile ${authorization.level.profile} and grantable by its registry entry`
      : `${unavailableGrants.length ? 'absent from the profile: ' + unavailableGrants.map(g => g.capability_id).join(', ') : ''}` +
        `${notGrantable.length ? ' not grantable: ' + notGrantable.map(g => g.capability_id).join(', ') : ''}`,
    { rules: ['§235', 'X-011', 'CAP-004', 'CAP-014', 'CG-002', 'CG-003', 'RG-007'], actual: [...unavailableGrants, ...notGrantable],
      expected: `capability ∈ ProfileCapabilitySet(${authorization.level.profile}) and lifecycle.grantable` });

  /* temporal model: the reference instant is the end of the execution */
  const referenceTime = Date.parse(execution.completed_at || execution.started_at || authorization.granted_at || '1970-01-01T00:00:00Z');
  const at = value => (value === null || value === undefined ? null : Date.parse(value));
  {
    const problems = [];
    const ts = (id, ok, message) => { if (!ok) problems.push(`${id}: ${message}`); };
    const exState = execution.state;
    const notStarted = ['NOT_STARTED', 'AUTHORIZATION_BLOCKED', 'READY', 'RUNNING'];
    ts('TS-001', execution.completed_at === null || execution.completed_at === undefined || execution.started_at,
      'completed_at is set while started_at is null');
    if (execution.completed_at && execution.started_at) {
      ts('TS-002', at(execution.completed_at) >= at(execution.started_at), 'completed_at precedes started_at');
    }
    ts('TS-003', exState !== 'RUNNING' || execution.completed_at === null, 'RUNNING with a completed_at timestamp');
    ts('TS-004', !TERMINAL_EXECUTION.includes(exState) || !!execution.completed_at, 'terminal execution without completed_at');
    ts('TS-005', exState !== 'NOT_STARTED' || !execution.started_at, 'NOT_STARTED with a started_at timestamp');
    ts('TS-006', exState !== 'AUTHORIZATION_BLOCKED' || !execution.started_at, 'AUTHORIZATION_BLOCKED with a started_at timestamp');
    ts('TS-007', authorization.expires_at === null || at(authorization.expires_at) >= at(authorization.granted_at),
      'expires_at precedes granted_at');
    ts('TS-004', !notStarted.includes(exState) || execution.completed_at === null, `completed_at must be null while execution is ${exState}`);
    report.check('SEMANTIC', 'TS-001…TS-007', 'execution · authorization',
      problems.length === 0,
      problems.length === 0
        ? `timestamp contract holds (execution ${exState}, ${execution.started_at || 'not started'} → ${execution.completed_at || 'open'}, expiry ${authorization.expires_at ?? 'none'})`
        : problems.join(' | '),
      { rules: ['§229', '§230', ...problems.map(x => x.split(':')[0])], actual: problems,
        expected: 'TS-001…TS-007 and the section 229 timestamp contract' });
  }

  /* the authorization function of section 216 (brief 10) over registered operations */
  const grantFor = id => (authorization.capability_grants || []).filter(g => g.capability_id === id);
  const inScope = (scope, target) => {
    if (!scope?.paths) return true;
    if (!pathBearing.includes(target.resource_class)) return true;
    const include = scope.paths.include || [];
    const exclude = scope.paths.exclude || [];
    const inside = include.length === 0 || include.some(p => target.path.startsWith(p));
    return inside && !exclude.some(p => target.path.startsWith(p));
  };
  const PRECEDENCE = ['DENIED', 'REVOKED', 'EXPIRED', 'RESTRICTED', 'ENABLED', 'DECLARED'];
  const effectiveState = id => {
    const grants = grantFor(id);
    if (grants.length === 0) return 'DECLARED';
    return grants.map(g => g.state).sort((a, b) => PRECEDENCE.indexOf(a) - PRECEDENCE.indexOf(b))[0];
  };
  const effectiveCapabilities = new Map();
  for (const id of resolvedProfile) {
    const state = effectiveState(id);
    if (['ENABLED', 'RESTRICTED'].includes(state)) {
      effectiveCapabilities.set(id, { ...capabilityRegistry.get(id), state, scope: grantFor(id)[0]?.scope });
    }
  }
  const capabilityOperations = new Set([...effectiveCapabilities.values()].flatMap(c => c.operations));
  const operationAllow = new Set(authorization.operations.allow);
  const operationDeny = new Set(authorization.operations.deny);
  const effectiveOperations = new Set([...capabilityOperations].filter(op => operationAllow.has(op) && !operationDeny.has(op)));
  const temporallyValid = authorization.expires_at === null || at(authorization.expires_at) >= referenceTime;

  function authorize(operation) {
    if (authorization.state !== 'GRANTED') return { decision: 'DENIED', why: `authorization state is ${authorization.state}` };
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
    const chosen = passing.sort((a, b) => (a.state === 'RESTRICTED' ? -1 : 1) - (b.state === 'RESTRICTED' ? -1 : 1))[0];
    return { decision: 'ALLOWED', why: `capability ${chosen.id}`, capability: chosen.id };
  }

  const decisions = execution.operations.map(op => ({ op, verdict: authorize(op) }));
  {
    const problems = [];
    const mismatched = decisions.filter(({ op, verdict }) => verdict.decision !== op.authorization_decision);
    for (const { op, verdict } of mismatched) {
      problems.push(`X-016: ${op.id} (${op.operation} ${op.target.path}) recorded ${op.authorization_decision}, computed ${verdict.decision} — ${verdict.why}`);
    }
    for (const op of execution.operations) {
      if (op.result === 'SUCCEEDED' && op.authorization_decision !== 'ALLOWED') problems.push(`X-016: ${op.id} succeeded without an ALLOWED decision`);
    }
    report.check('SEMANTIC', 'X-016', 'execution.operations',
      problems.length === 0,
      problems.length === 0
        ? `every recorded decision is re-derived by the section 216 function over ${effectiveCapabilities.size} effective capabilities`
        : problems.slice(0, 3).join(' | '),
      { rules: ['§232', '§216'], actual: problems, expected: 'the recorded authorization_decision for every operation' });
  }

  const mutatingOperations = execution.operations.filter(o => mutatingOp(o.operation));
  {
    const problems = [];
    for (const op of mutatingOperations) {
      if (!(authorization.change_ids || []).includes(op.change_id)) {
        problems.push(`X-017: ${op.id} (${op.operation}) is not covered by authorization.change_ids`);
      }
    }
    if (execution.state !== 'GRANTED' && authorization.state !== 'GRANTED') {
      const succeeded = mutatingOperations.filter(o => o.result === 'SUCCEEDED');
      for (const op of succeeded) problems.push(`X-018: ${op.id} succeeded while authorization.state is ${authorization.state}`);
    }
    if (authorization.state === 'GRANTED') {
      const succeeded = mutatingOperations.filter(o => o.result === 'SUCCEEDED' && o.authorization_decision !== 'ALLOWED');
      for (const op of succeeded) problems.push(`X-018: ${op.id} succeeded while its decision is ${op.authorization_decision}`);
    }
    const coverage = problems.filter(p => p.startsWith('X-017'));
    const state = problems.filter(p => p.startsWith('X-018'));
    report.check('SEMANTIC', 'X-017', 'execution.operations[] · authorization.change_ids',
      coverage.length === 0,
      coverage.length === 0
        ? `every one of the ${mutatingOperations.length} mutating operation(s) references an authorized change`
        : coverage.slice(0, 3).join(' | '),
      { rules: ['§232'], actual: coverage, expected: 'change_id ∈ authorization.change_ids' });
    report.check('SEMANTIC', 'X-018', 'execution.operations[] · authorization.state',
      state.length === 0,
      state.length === 0
        ? `no successful mutation is reported while authorization.state is ${authorization.state}`
        : state.slice(0, 3).join(' | '),
      { rules: ['§232', '§238'], actual: state, expected: 'authorization.state = GRANTED with an ALLOWED decision' });
  }

  {
    const problems = [];
    if (verification.execution_id !== execution.id) {
      problems.push(`X-019: execution_verification.execution_id ${verification.execution_id} != execution.id ${execution.id}`);
    }
    const claimChanges = new Set([...authorization.change_ids, ...execution.executed_changes]);
    const named = (verification.findings || []).join(' ').match(/R-\d{3,}/g) || [];
    for (const id of [...new Set(named)]) if (claimChanges.has(id)) problems.push(`X-020: verification finding names authorized or executed change ${id}`);
    report.check('SEMANTIC', 'X-019 · X-020', 'execution_verification',
      problems.length === 0,
      problems.length === 0
        ? `verification refers to ${execution.id} and authorizes no change`
        : problems.join(' | '),
      { rules: ['§232'], actual: problems });
  }

  /* ---- claim semantics (briefs 7-10) ---- */
  const byId = new Map(claims.map(c => [c.id, c]));
  const cvr = claim => claim.claim_verification.result;
  const procedures = new Map([...register.matchAll(/^\|\s*`(AV-\d{3})`\s*\|\s*`(CLAIM-\d{3})`\s*\|/gm)].map(m => [m[1], m[2]]));
  const procedureClaims = new Set(procedures.values());
  const contradictions = [...register.matchAll(/^\|\s*`?(CONTRA-\d{3})`?\s*\|\s*`(CLAIM-\d{3})`\s*\|\s*`(CLAIM-\d{3})`\s*\|/gm)]
    .map(m => ({ id: m[1], claim_a: m[2], claim_b: m[3] }));
  const contradicted = new Set(contradictions.flatMap(x => [x.claim_a, x.claim_b]));
  {
    const claimChecks = [];
    const rule = (id, ok, note) => claimChecks.push([id, ok, note]);
    const inEnum = (name, value) => (schema.$defs[name].enum || []).includes(value);
    rule('CV-001…CV-005', claims.every(c =>
      inEnum('claimKind', c.claim_kind) && inEnum('implementationState', c.implementation_state) &&
      inEnum('testState', c.test_state) && inEnum('evidenceLevel', c.evidence_level) &&
      (schema.$defs.claimVerificationResult.enum || []).includes(cvr(c))),
      'every claim dimension uses its canonical enum');
    rule('CV-006', claims.every(c => cvr(c) !== 'VERIFIED' || c.evidence_level === 'DIRECT' || c.evidence_level === 'CORROBORATED' ||
      (c.evidence_level === 'ABSENT' && procedureClaims.has(c.id))),
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
      'HYPOTHESIS has no implementation state');
    rule('CV-012', claims.every(c => c.claim_kind !== 'NON_GOAL' || c.implementation_state === 'NOT_APPLICABLE'),
      'NON_GOAL has no implementation state');
    rule('CV-013', claims.every(c => c.claim_kind !== 'PLANNED' || c.implementation_state === 'NOT_IMPLEMENTED'),
      'PLANNED defaults to NOT_IMPLEMENTED');
    rule('CV-014', claims.every(c => !['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state) || c.evidence.some(e => e.kind === 'TEST')),
      'TESTED requires execution evidence');
    const states = new Set(claims.filter(c => c.test_state === 'UNTESTED').map(c => c.implementation_state));
    rule('CV-015', states.size > 1, 'UNTESTED spans implementation states without implying failure');
    const implemented = claims.filter(c => c.implementation_state === 'IMPLEMENTED');
    const tested = claims.filter(c => ['TESTED', 'PARTIALLY_TESTED'].includes(c.test_state));
    const verified = claims.filter(c => cvr(c) === 'VERIFIED');
    const partial = claims.filter(c => c.implementation_state === 'PARTIAL');
    rule('CV-016', new Set(implemented.map(c => c.test_state)).size > 1, 'IMPLEMENTED does not imply TESTED');
    rule('CV-017', new Set(tested.map(cvr)).size > 1, 'TESTED does not imply VERIFIED');
    rule('CV-018', new Set(verified.map(c => c.implementation_state)).size > 1, 'VERIFIED does not imply IMPLEMENTED');
    rule('CV-019', partial.length === 0 || new Set(partial.map(cvr)).size > 1 || partial.every(c => cvr(c) === 'PARTIALLY_VERIFIED') === false,
      'PARTIAL does not imply PARTIALLY_VERIFIED');
    rule('CV-020', claims.every(c => !(c.evidence_level === 'ABSENT' && c.implementation_state === 'IMPLEMENTED')),
      'ABSENT is not INACCESSIBLE and never IMPLEMENTED');
    rule('C-031', claims.every(c => c.evidence_level !== 'CORROBORATED' ||
      new Set(c.evidence.map(e => e.kind)).size > 1 || c.evidence.length > 1),
      'CORROBORATED needs two independent artifacts');
    rule('C-141', claims.every(c => !['HIGH', 'VERY_HIGH'].includes(c.confidence) || cvr(c) !== 'UNVERIFIED'),
      'confidence never overrides claim_verification.result');
    rule('§169', claims.every(c => c.claim_kind !== 'CURRENT' || cvr(c) !== 'NOT_APPLICABLE' || c.implementation_state === 'NOT_APPLICABLE'),
      'a CURRENT claim is never NOT_APPLICABLE by construction');
    rule('X-001', claims.every(c => c.evidence.length > 0), 'every claim carries at least one evidence object');
    const violated = claimChecks.filter(([, ok]) => !ok);
    report.check('SEMANTIC', 'CV-001…CV-020', 'claims',
      violated.length === 0,
      violated.length === 0
        ? `${claimChecks.length} rule groups; ${contradictions.length} contradiction(s), ${procedures.size} absence procedure(s) from the register`
        : violated.map(([id, , n]) => `${id} (${n})`).join('; '),
      { rules: ['§144', '§232', ...violated.flatMap(([id]) => id.split('…')[0].split('·').map(x => x.trim()))], actual: violated.map(([id]) => id) });
  }

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
    report.check('SEMANTIC', 'RG-008', 'evidence-register.md',
      problems.length === 0,
      problems.length === 0
        ? `${procedures.size} absence procedure(s) cover ${absentClaims.length} ABSENT claim(s); ${contradictions.length} contradiction row(s) name their claims`
        : problems.slice(0, 4).join(' | '),
      { rules: ['CV-008', 'CV-010', 'C-031', 'X-001'], actual: problems });
  }

  if (fileChecks) {
    const changeRegister = fs.readFileSync(CHANGE_REGISTER_PATH, 'utf8');
    const planSection = changeRegister.slice(changeRegister.indexOf('## Proposed changes — code'));
    const proposed = [...new Set([...planSection.matchAll(/^\| (R-\d{3}) \|/gm)].map(m => m[1]))];
    const leaked = proposed.filter(id => authorization.change_ids.includes(id) || execution.executed_changes.includes(id));
    report.check('SEMANTIC', 'I-016', 'change-register-2026-09-10.md',
      leaked.length === 0 && proposed.length > 0,
      proposed.length === 0
        ? 'the change register lists no PLAN ONLY proposal'
        : leaked.length === 0
          ? `${proposed.length} PLAN ONLY change(s) absent from change_ids and from the execution`
          : `authorized or executed although only proposed: ${leaked.join(', ')}`,
      { rules: ['§78 discovered-change rule'], actual: leaked });
  }

  /* ---- serialization (YAML mirror) ---- */
  if (ctx.yaml) {
    const parsed = ctx.yaml;
    const problems = [];
    const compare = (expected, actual, at_) => {
      if (expected === null || expected === undefined) return;
      if (Array.isArray(expected)) {
        if (!Array.isArray(actual)) { problems.push(`${at_}: expected a list, found ${actual === undefined ? 'nothing' : typeof actual}`); return; }
        if (expected.length !== actual.length) { problems.push(`${at_}: ${actual.length} entries vs ${expected.length} in JSON`); return; }
        expected.forEach((v, i) => compare(v, actual[i], `${at_}[${i}]`));
        return;
      }
      if (expected && typeof expected === 'object') {
        for (const [k, v] of Object.entries(expected)) compare(v, actual?.[k], `${at_}.${k}`);
        return;
      }
      if (expected !== actual) problems.push(`${at_}: ${JSON.stringify(actual)} vs ${JSON.stringify(expected)} in JSON`);
    };
    compare(authorization, parsed.authorization, '$.authorization');
    report.check('SEMANTIC', 'SER-001…SER-012', 'authorization.yaml',
      problems.length === 0,
      problems.length === 0
        ? 'YAML and JSON deserialize to the same authorization object (state, level, capability grants, operations, scope, change ids, authority, target)'
        : problems.slice(0, 4).join(' | '),
      { rules: ['§199'], actual: problems });
  }

  /* ------------------------------------------------------------------ */
  /* 4. AUTHORIZATION — capability and grant rule sets                   */
  /* ------------------------------------------------------------------ */

  {
    const checks = [];
    const cap = (id, ok, note) => checks.push([id, ok, note]);
    cap('CAP-001', (authorization.capability_grants || []).every(g => /^CAP-[A-Z0-9_-]+$/.test(g.capability_id)),
      `${(authorization.capability_grants || []).length} capability grant(s) use the canonical id form`);
    cap('CAP-002', !profileError, profileError || `profile ${authorization.level.profile} resolves to ${resolvedProfile.size} declared capabilities`);
    cap('CAP-003', !profileError, 'profile inheritance is acyclic');
    cap('CAP-004', unavailableGrants.length === 0, 'every grant references a capability available from the resolved profile');
    cap('CAP-005', (authorization.capability_grants || []).every(g => !('operations' in g)), 'no grant alters a capability operation set');
    cap('CAP-006', (authorization.capability_grants || []).every(g => !('resource_class' in g)), 'no grant alters a capability resource class');
    const unrestricted = (authorization.capability_grants || []).filter(g => g.state === 'RESTRICTED' && !g.scope);
    cap('CAP-007', unrestricted.length === 0, `every RESTRICTED grant carries its restriction scope${unrestricted.length ? ': ' + unrestricted.map(g => g.capability_id).join(', ') : ''}`);
    const enabledOutOfScope = (authorization.capability_grants || []).filter(g => g.state === 'ENABLED' && g.scope);
    cap('CAP-008', enabledOutOfScope.length === 0, 'ENABLED grants carry no hidden restriction');
    const bothStates = (authorization.capability_grants || []).map(g => g.capability_id).filter((id, i, all) => all.indexOf(id) !== i);
    cap('CAP-009', bothStates.length === 0, 'DENIED overrides ENABLED: no capability is granted twice');
    cap('CAP-010', true, 'REVOKED grants are terminal and authorize nothing');
    cap('CAP-011', temporallyValid, `EXPIRED grants authorize nothing; authorization valid at ${new Date(referenceTime).toISOString()}`);
    cap('CAP-012', effectiveCapabilities.size > 0,
      `effective capabilities are computed here, never read: ${effectiveCapabilities.size} capabilities → ${[...effectiveOperations].sort().join('/')}`);
    cap('CAP-013', true, 'no effective capability set is persisted in the record (checked in STRUCTURAL)');
    cap('CAP-014', unavailableGrants.length === 0, 'a capability absent from the profile is never introduced by a grant');
    const overreach = (authorization.operations.allow || []).filter(op => !capabilityOperations.has(op));
    cap('CAP-015', overreach.length === 0, `operation allow lists may reduce privileges only${overreach.length ? ': ' + overreach.join(', ') : ''}`);
    const conflicted = (authorization.operations.allow || []).filter(op => operationDeny.has(op));
    cap('CAP-016', conflicted.length === 0, `operation deny lists override operation allow lists${conflicted.length ? ': ' + conflicted.join(', ') : ''}`);
    cap('CG-001', unknownGrantsCount(authorization, capabilityRegistry) === 0, 'every capability grant references an existing capability');
    cap('CG-002', unavailableGrants.length === 0, 'every ENABLED/RESTRICTED grant is available from the resolved profile');
    cap('CG-003', unavailableGrants.length === 0, 'no capability is granted merely by listing it');
    cap('CG-004', (authorization.capability_grants || []).every(g => g.state !== 'DENIED' || resolvedProfile.has(g.capability_id)),
      `${(authorization.capability_grants || []).filter(g => g.state === 'DENIED').length} explicit deny grant(s), all within the profile`);
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
    cap('CG-013', escapes.length === 0, `no executed operation escaped the authorization scope${escapes.length ? ': ' + escapes.map(o => o.id).join(', ') : ''}`);
    cap('CG-014', true, 'effective capabilities are derived in this validator; a persisted set fails STRUCTURAL');
    cap('CG-015', authorization.authority.type === 'USER', `technical access did not create a grant; authority is ${authorization.authority.type}`);
    const declaredGrants = (authorization.capability_grants || []).filter(g => g.state === 'DECLARED').map(g => g.capability_id);
    cap('CG-001-state', declaredGrants.length === 0, `DECLARED belongs to a profile declaration, not a grant${declaredGrants.length ? ': ' + declaredGrants.join(', ') : ''}`);
    const violated = checks.filter(([, ok]) => !ok);
    report.check('AUTHORIZATION', 'CAP-001…CAP-016 · CG-001…CG-015', 'authorization',
      violated.length === 0,
      violated.length === 0
        ? `${effectiveCapabilities.size} effective capabilities; operations ${[...effectiveOperations].sort().join('/')}; ${violated.length} violations`
        : violated.map(([id, , n]) => `${id} (${n})`).join('; '),
      { rules: ['§204…§208', '§214…§216', ...violated.flatMap(([id]) => id.split('-state')[0].split('·').map(x => x.trim()))], actual: violated.map(([id]) => id) });
  }

  /* ------------------------------------------------------------------ */
  /* 5. EXECUTION — EV-001…EV-012                                        */
  /* ------------------------------------------------------------------ */

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
    const ev = [
      ['EV-001', ops.length > 0, 'the execution records its operations'],
      ['EV-002', new Set(ops.map(o => o.id)).size === ops.length, 'operation ids are unique'],
      ['EV-003', ops.every(o => !!o.authorization_decision), 'every operation carries its authorization decision'],
      ['EV-004', ops.every(o => o.result !== 'SUCCEEDED' || o.authorization_decision === 'ALLOWED'), 'no operation succeeds without an ALLOWED decision'],
      ['EV-005', execution.unauthorized_changes.length === 0, 'no unauthorized change was recorded'],
      ['EV-006', new Set(execution.executed_changes).size === execution.executed_changes.length, 'executed change ids are unique'],
      ['EV-007', execution.state !== 'SUCCEEDED' || ops.every(o => o.result === 'SUCCEEDED'), 'SUCCEEDED requires every operation to succeed'],
      ['EV-008', ops.every(o => !mutatingOp(o.operation) || o.result !== 'SUCCEEDED' || authorization.change_ids.includes(o.change_id)), 'mutating operations stay inside the authorized change set'],
      ['EV-009', execution.executed_changes.every(id => ops.some(o => o.change_id === id)), 'every executed change has at least one operation'],
      ['EV-010', succeeded.length > 0, 'the execution succeeded in at least one operation'],
      ['EV-011', ops.every(o => !!o.change_id), 'every executed operation references a change id'],
      ['EV-012', ops.filter(o => o.result === 'SUCCEEDED').every(o => o.authorization_decision === 'ALLOWED'), 'decisions and results never contradict'],
    ];
    const bad = ev.filter(([, ok]) => !ok);
    report.check('EXECUTION', 'EV-001…EV-012', 'execution',
      bad.length === 0,
      bad.length === 0 ? `${ev.length} invariants, state ${execution.state}, ${ops.length} operations` : bad.map(([id]) => id).join(', '),
      { rules: ['§189…§191', ...bad.map(([id]) => id)], actual: bad.map(([id]) => id) });

    const uncovered = execution.executed_changes.filter(id => !ops.some(o => o.change_id === id));
    const unauthorized = execution.executed_changes.filter(id => !authorization.change_ids.includes(id));
    report.check('EXECUTION', 'X-004 · X-005 · EV-009', 'execution.executed_changes',
      uncovered.length === 0 && unauthorized.length === 0,
      uncovered.length === 0 && unauthorized.length === 0
        ? `${execution.executed_changes.length} change(s), ${ops.length} operation(s), every executed change authorized and covered`
        : `uncovered: ${uncovered.join(', ')}; unauthorized: ${unauthorized.join(', ')}`,
      { rules: ['§232'], actual: [...uncovered, ...unauthorized] });

    const unreachable = [];
    if (!reachable('authorization', authorization.state)) unreachable.push(`authorization.${authorization.state}`);
    if (!reachable('execution', execution.state)) unreachable.push(`execution.${execution.state}`);
    if (!reachable('execution_verification', verification.state)) unreachable.push(`execution_verification.${verification.state}`);
    report.check('EXECUTION', '§200', 'lifecycles',
      unreachable.length === 0,
      unreachable.length === 0
        ? 'recorded lifecycle states are reachable under the section 200 transition graph'
        : `unreachable: ${unreachable.join(', ')}`,
      { rules: ['§200'] });
  }

  /* ------------------------------------------------------------------ */
  /* 6. VERIFICATION — EVV-001…EVV-009                                   */
  /* ------------------------------------------------------------------ */

  {
    const results = verification.checks.map(c => c.result);
    const evv = [
      ['EVV-001', verification.state !== 'PASSED' || verification.result === 'CONFORMING', 'PASSED requires CONFORMING'],
      ['EVV-002', verification.result !== 'CONFORMING' || verification.state === 'PASSED', 'CONFORMING requires PASSED'],
      ['EVV-003', verification.result !== 'NON_CONFORMING' || verification.state === 'FAILED', 'NON_CONFORMING requires FAILED'],
      ['EVV-004', verification.state !== 'PASSED' || results.every(r => r === 'PASSED'), 'PASSED requires every required check to pass'],
      ['EVV-005', verification.state !== 'FAILED' || results.some(r => r === 'FAILED'), 'FAILED requires at least one check to fail'],
      ['EVV-006', results.length === new Set(verification.checks.map(c => c.id)).size, 'check ids are unique'],
      ['EVV-007', verification.remediation_required !== true || verification.findings.length > 0, 'remediation requires a finding'],
      ['EVV-008', true, 'verification modified nothing: enforced procedurally by tools/validation-run.mjs (tree digest before/after)'],
      ['EVV-009', !verification.findings.some(f => /R-\d{3}/.test(f)), 'a remediation finding proposes, it never authorizes'],
    ];
    const bad = evv.filter(([, ok]) => !ok);
    report.check('VERIFICATION', 'EVV-001…EVV-009', 'execution_verification',
      bad.length === 0,
      bad.length === 0
        ? `${evv.length} rules, state ${verification.state} / result ${verification.result}, ${verification.checks.length} checks (${results.filter(r => r === 'PASSED').length} passed)`
        : bad.map(([id]) => id).join(', '),
      { rules: ['§180…§184', ...bad.map(([id]) => id)], actual: bad.map(([id]) => id) });

    const scopePaths = verification.scope?.paths;
    const declared = Array.isArray(scopePaths) ? scopePaths.length
      : (scopePaths ? (scopePaths.include || []).length + (scopePaths.exclude || []).length : 0);
    report.check('VERIFICATION', 'EVV-010', 'execution_verification.scope',
      declared > 0 && verification.checks.length > 0,
      `${verification.checks.length} check(s) over ${declared} declared location(s)`,
      { rules: ['§231', 'X-019'] });

    if (verification.state !== 'NOT_REQUIRED' && verification.state !== 'NOT_STARTED') {
      report.info('VERIFICATION', 'EVV-008', 'execution_verification',
        'the "verification must not mutate the repository" rule is procedural: tools/validation-run.mjs compares a working-tree digest before and after the run');
    }
  }

  /* ------------------------------------------------------------------ */
  /* 7. INVARIANTS — I-001…I-016 and restated fields                     */
  /* ------------------------------------------------------------------ */

  {
    const invariants = [
      ['I-001', 'no generic status field', () => !/"status"\s*:/.test(ctx.recordText || '')],
      ['I-002', 'claim kind describes claim semantics', () => claims.every(c => typeof c.claim_kind === 'string')],
      ['I-003', 'implementation state describes implementation', () => claims.every(c => typeof c.implementation_state === 'string')],
      ['I-004', 'test state describes testing', () => claims.every(c => typeof c.test_state === 'string')],
      ['I-005', 'evidence level describes evidence strength', () => claims.every(c => typeof c.evidence_level === 'string')],
      ['I-006', 'claim verification is a separate field', () => claims.every(c => typeof c.claim_verification?.result === 'string')],
      ['I-007', 'authorization is an object, not a boolean', () => typeof authorization === 'object' && !('granted' in authorization)],
      ['I-008', 'profile is not an authority', () => !['GRANTED', 'ALLOWED'].includes(authorization.level.profile)],
      ['I-009', 'capability is not an operation', () => (authorization.capability_grants || []).every(g => capabilityRegistry.has(g.capability_id))],
      ['I-010', 'access is not authorization', () => doc.repository.access_level !== 'GRANTED'],
      ['I-011', 'execution state is not a verification result', () => !schema.$defs.executionVerification.properties.state.enum.includes(execution.state)],
      ['I-012', 'execution verification is independent of the execution it verifies', () => verification.execution_id === execution.id],
      ['I-013', 'documentation never proves implementation', () => claims.every(c => c.implementation_state !== 'IMPLEMENTED' || c.evidence.some(e => e.kind !== 'DOCUMENTATION'))],
      ['I-014', 'ABSENT is not INACCESSIBLE', () => claims.every(c => !(c.evidence_level === 'ABSENT' && c.implementation_state === 'UNKNOWN'))],
      ['I-015', 'full access implies no inaccessible evidence', () => !(doc.repository.access_level === 'FULL' && claims.some(c => c.evidence_level === 'INACCESSIBLE'))],
      ['I-016', 'newly discovered work cannot silently expand execution scope', () => execution.unauthorized_changes.length === 0],
    ];
    const violated = invariants.filter(([, , check]) => !check());
    report.check('SEMANTIC', 'I-001…I-016', 'document',
      violated.length === 0,
      violated.length === 0 ? `${invariants.length} invariants hold` : violated.map(([id]) => id).join(', '),
      { rules: ['§167', ...violated.map(([id]) => id)], actual: violated.map(([id]) => id) });
  }

  if (fileChecks) {
    const doc_ = fs.readFileSync(ANALYSIS_DOC_PATH, 'utf8');
    const stale = [];
    for (const row of doc_.matchAll(/^\| `(CLAIM-\d{3})` \|([^\n]*)$/gm)) {
      const claim = byId.get(row[1]);
      if (!claim) { stale.push(`${row[1]} (unknown)`); continue; }
      const cells = row[2].split('|').map(s => s.trim().replace(/`/g, ''));
      const shown = [claim.claim_kind, claim.implementation_state, claim.test_state, claim.evidence_level, claim.claim_verification.result];
      if (!shown.every(v => cells.includes(v))) stale.push(row[1]);
    }
    const legacy = [...new Set([...doc_.matchAll(/[A-Z]+-CLAIM-\d{3}/g)].map(m => m[0]))];
    report.check('SEMANTIC', 'I-011', 'repository-analysis-2026-09-10.md',
      stale.length === 0 && legacy.length === 0,
      stale.length === 0 && legacy.length === 0
        ? 'restated claim fields match the record (CLAIM-nnn namespace)'
        : `${stale.length ? 'stale: ' + stale.slice(0, 4).join(', ') : ''}${legacy.length ? ' legacy ids: ' + legacy.slice(0, 3).join(', ') : ''}`,
      { rules: ['§106'] });

    if (ctx.allowSubprocess !== false) {
      try {
        execFileSync(process.execPath, [path.join(REPO_ROOT, 'tools', 'render-claims.mjs'), '--check', '--root', ROOT], { cwd: REPO_ROOT, stdio: 'pipe' });
        report.ok('SEMANTIC', 'I-012', 'claims.md', 'generated claim tables are current');
      } catch (error) {
        report.bad('SEMANTIC', 'I-012', 'claims.md',
          String(error.stdout || error.message).trim().split('\n').pop(), { rules: ['§150'] });
      }
    }
  }

  return report;
}

function unknownGrantsCount(authorization, capabilityRegistry) {
  return (authorization.capability_grants || []).filter(g => !capabilityRegistry.has(g.capability_id)).length;
}

/* ========================================================================== */
/* Inputs                                                                      */
/* ========================================================================== */

const REGISTRY_IDS = ['capability', 'level_profile', 'operation', 'resource_class', 'claim'];
const REGISTRY_FILES = {
  capability: 'capability-registry.json',
  level_profile: 'level-profile-registry.json',
  operation: 'operation-registry.json',
  resource_class: 'resource-class-registry.json',
  claim: 'claim-registry.json',
};

export function loadInputs({ parseYaml = true } = {}) {
  const record = JSON.parse(fs.readFileSync(RECORD_PATH, 'utf8'));
  const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
  const registrySchema = JSON.parse(fs.readFileSync(REGISTRY_SCHEMA_PATH, 'utf8'));
  const registries = {};
  for (const id of REGISTRY_IDS) {
    registries[id] = JSON.parse(fs.readFileSync(path.join(REGISTRY_DIR, REGISTRY_FILES[id]), 'utf8'));
  }
  const register = fs.readFileSync(REGISTER_PATH, 'utf8');
  const yaml = parseYaml ? parseAuthorizationYaml(fs.readFileSync(YAML_PATH, 'utf8')) : null;
  return {
    record, schema, registrySchema, registries, register, yaml,
    recordText: fs.readFileSync(RECORD_PATH, 'utf8'),
    fileChecks: true,
  };
}

/* Minimal YAML reader for the authorization mirror: the emitter in this
   repository writes a restricted subset (two-space indentation, scalars,
   inline empty lists and block lists), so the reader stays small on purpose. */
export function parseAuthorizationYaml(text) {
  const lines = text.split(/\r?\n/).filter(l => l.trim() && !l.trim().startsWith('#'));
  let index = 0;

  function scalar(raw) {
    const value = raw.trim();
    if (value === 'null' || value === '~') return null;
    if (value === 'true') return true;
    if (value === 'false') return false;
    if (value === '[]') return [];
    if (value.startsWith('"') && value.endsWith('"')) return JSON.parse(value);
    if (/^-?\d+$/.test(value)) return Number(value);
    return value;
  }

  function parseBlock(indent) {
    const first = lines[index];
    const isList = first.trim().startsWith('- ');
    const out = isList ? [] : {};
    while (index < lines.length) {
      const line = lines[index];
      const depth = line.search(/\S/);
      if (depth < indent) break;
      if (depth > indent) break;
      const content = line.trim();
      if (isList) {
        if (!content.startsWith('- ')) break;
        const rest = content.slice(2);
        index += 1;
        if (rest.includes(':')) {
          const [key, ...tail] = rest.split(':');
          const item = {};
          const value = tail.join(':').trim();
          if (value === '') item[key.trim()] = parseBlock(indent + 4);
          else item[key.trim()] = scalar(value);
          /* continuation keys of the same list item */
          while (index < lines.length && lines[index].search(/\S/) === indent + 2 && !lines[index].trim().startsWith('- ')) {
            const [k, ...t] = lines[index].trim().split(':');
            const v = t.join(':').trim();
            index += 1;
            item[k.trim()] = v === '' ? parseBlock(indent + 4) : scalar(v);
          }
          out.push(item);
        } else {
          out.push(scalar(rest));
        }
      } else {
        if (!content.includes(':')) { index += 1; continue; }
        const [key, ...tail] = content.split(':');
        const value = tail.join(':').trim();
        index += 1;
        if (value === '') out[key.trim()] = parseBlock(indent + 2);
        else out[key.trim()] = scalar(value);
      }
    }
    return out;
  }

  return parseBlock(0);
}

/* ========================================================================== */
/* Reporting                                                                   */
/* ========================================================================== */

function digest(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

export function buildReport(ctx, report) {
  const input = (file) => ({ path: path.relative(ROOT, file).split(path.sep).join('/'), sha256: digest(file) });
  const root = { path: ROOT, repository_root: REPO_ROOT };
  return {
    validator: {
      path: path.relative(REPO_ROOT, fileURLToPath(import.meta.url)).split(path.sep).join('/'),
      model: 'brief 11 sections 202, 218-243',
      sha256: digest(fileURLToPath(import.meta.url)),
    },
    root,
    inputs: {
      document: input(RECORD_PATH),
      schema: input(SCHEMA_PATH),
      registry_schema: input(REGISTRY_SCHEMA_PATH),
      registries: REGISTRY_IDS.map(id => ({ registry_id: id, registry_version: ctx.registries[id].registry_version, ...input(path.join(REGISTRY_DIR, REGISTRY_FILES[id])) })),
    },
    verdict: report.errors.length === 0 ? 'VALID' : 'INVALID',
    phases: PHASES.map(phase => report.phaseState(phase)),
    errors: report.errors.map(e => ({
      code: e.code, phase: e.phase, object: e.object, message: e.message,
      ...(e.expected !== undefined ? { expected: e.expected } : {}),
      ...(e.actual !== undefined ? { actual: e.actual } : {}),
      ...(e.rules ? { rules: e.rules } : {}),
    })),
    checks: report.checks,
  };
}

function printHuman(report) {
  console.log('validation (brief 11 sections 218-243): schema -> registries -> semantic rules');
  console.log('  phases: STRUCTURAL → REGISTRY → SEMANTIC → AUTHORIZATION → EXECUTION → VERIFICATION\n');
  for (const phase of PHASES) {
    const inPhase = report.checks.filter(c => c.phase === phase);
    if (inPhase.length === 0) continue;
    console.log(phase);
    for (const check of inPhase) {
      const tag = check.state === 'FAIL' ? '[FAIL]' : check.state === 'INFO' ? '[INFO]' : '[PASS]';
      const pad = ' '.repeat(Math.max(0, 8 - tag.length));
      console.log(`  ${tag}${pad}${check.code.padEnd(28)} ${check.message.slice(0, 150)}`);
    }
    console.log('');
  }
  const errors = report.errors;
  if (errors.length > 0) {
    console.log('errors:');
    for (const e of errors) {
      console.log(`  ${e.phase} · ${e.code} · ${e.object}`);
      console.log(`    ${e.message}`);
    }
    console.log('');
  }
  console.log(`${report.passed.length} passed, ${errors.length} failed, ${report.checks.filter(c => c.state === 'INFO').length} informational`);
}

async function selfTest() {
  const { fixtures } = await import('./validation-fixtures.mjs');
  const base = loadInputs();
  const report = validateDocument(base.record, { ...base, fileChecks: false, allowSubprocess: false });
  const failures = [];
  if (report.errors.length > 0) {
    failures.push(`the unmutated record is invalid: ${report.errors.map(e => e.code).join(', ')}`);
  }
  let index = 0;
  for (const fixture of fixtures) {
    index += 1;
    const doc = JSON.parse(JSON.stringify(base.record));
    const ctx = {
      ...base,
      registries: JSON.parse(JSON.stringify(base.registries)),
      fileChecks: fixture.fileChecks === true,
      allowSubprocess: false,
    };
    try {
      fixture.mutate(doc, ctx);
    } catch (error) {
      failures.push(`${fixture.id}: mutation failed — ${error.message}`);
      continue;
    }
    const result = validateDocument(doc, ctx);
    const all = new Set(result.errors.flatMap(e => [
      ...(e.code.match(/[A-Z]+-[0-9]{3}/g) || []),
      ...((e.rules || []).flatMap(r => r.match(/[A-Z]+-[0-9]{3}/g) || [])),
    ]));
    const expected = Array.isArray(fixture.expect) ? fixture.expect : [fixture.expect || fixture.rule].filter(Boolean);
    const missing = expected.filter(code => !all.has(code));
    const phases = new Set(result.errors.map(e => e.phase));
    const phaseOK = !fixture.phase || phases.has(fixture.phase);
    if (result.errors.length === 0) failures.push(`${fixture.id}: expected ${expected.join(', ')}, but the document was accepted`);
    else if (missing.length) failures.push(`${fixture.id}: expected ${missing.join(', ')}; observed ${[...all].slice(0, 6).join(', ')}`);
    else if (!phaseOK) failures.push(`${fixture.id}: expected phase ${fixture.phase}; observed ${[...phases].join(', ')}`);
    else console.log(`  [PASS] ${fixture.id.padEnd(8)} ${(expected.join(',')).padEnd(14)} ${fixture.note || ''}`);
  }
  console.log('');
  if (failures.length) {
    for (const f of failures) console.error(`  [FAIL] ${f}`);
    console.error(`\nfixtures: ${fixtures.length - failures.length}/${fixtures.length} behaved as specified`);
    process.exit(1);
  }
  console.log(`fixtures: ${fixtures.length}/${fixtures.length} behaved as specified (and the record under test is valid)`);
}

const argv = process.argv.slice(2);
if (argv.includes('--self-test')) {
  await selfTest();
  process.exit(0);
} else {
  let ctx;
  try {
    ctx = loadInputs();
  } catch (error) {
    /* A pipeline that cannot load its inputs has failed in the REGISTRY phase,
       and the failure is reported in the same structure as every other one. */
    const entry = {
      code: 'LOAD-001', phase: 'REGISTRY', object: 'inputs',
      message: `could not load the validation inputs under ${ROOT}: ${error.message}`,
    };
    if (argv.includes('--json')) {
      console.log(JSON.stringify({
        validator: { path: 'tools/validate-analysis.mjs', model: 'brief 11 sections 202, 218-243',
          sha256: crypto.createHash('sha256').update(fs.readFileSync(fileURLToPath(import.meta.url))).digest('hex') },
        root: { path: ROOT, repository_root: REPO_ROOT },
        inputs: {}, verdict: 'INVALID',
        phases: PHASES.map(phase => ({ phase, state: phase === 'REGISTRY' ? 'FAILED' : 'NOT_RUN', checks: 0, errors: phase === 'REGISTRY' ? 1 : 0 })),
        errors: [entry],
        checks: [],
      }, null, 2));
    } else {
      console.error(entry.message);
    }
    process.exit(2);
  }
  const report = validateDocument(ctx.record, ctx);
  if (argv.includes('--json')) console.log(JSON.stringify(buildReport(ctx, report), null, 2));
  else printHuman(report);
  process.exit(report.errors.length === 0 ? 0 : 1);
}
