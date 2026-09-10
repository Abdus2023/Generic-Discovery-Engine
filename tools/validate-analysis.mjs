#!/usr/bin/env node
/*
 * ============================================================================
 * Validate the canonical analysis record
 * ============================================================================
 *
 * Enforces the canonical state model and the schema validation rules:
 *
 *   - no generic "status" field anywhere in the record
 *   - every claim uses the five typed fields with allowed enum values
 *   - claim_kind is never used as evidence strength, and so on
 *   - access_level, authorization.level, execution.result and
 *     post_verification.result each use their own enum
 *   - executed changes are a subset of authorized changes
 *   - no unauthorized change was executed
 *   - documentation-only evidence never establishes an implementation claim
 *   - ABSENT is not used where the scope was not actually inspected
 *     (i.e. INACCESSIBLE is not converted into ABSENT)
 *   - every evidence reference exists in the evidence register
 *   - claims.md is rendered from analysis.json and is not stale
 *
 * Usage:
 *   node tools/validate-analysis.mjs
 *
 * Exit code 0 = the record is valid. Exit code 1 = validation failed.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RECORD_PATH = path.join(ROOT, 'docs', 'analysis', 'analysis.json');
const REGISTER_PATH = path.join(ROOT, 'docs', 'analysis', 'evidence-register.md');

const results = [];
const pass = (m, n = '') => results.push(['PASS', m, n]);
const fail = (m, n = '') => results.push(['FAIL', m, n]);
const info = (m, n = '') => results.push(['INFO', m, n]);

const ENUMS = {
  claim_kind: ['CURRENT', 'SPECIFIED', 'PLANNED', 'HISTORICAL', 'HYPOTHESIS', 'NON_GOAL'],
  implementation_state: ['IMPLEMENTED', 'PARTIAL', 'NOT_IMPLEMENTED', 'NOT_APPLICABLE', 'UNKNOWN'],
  test_state: ['TESTED', 'PARTIALLY_TESTED', 'UNTESTED', 'NOT_APPLICABLE', 'UNKNOWN'],
  evidence_level: ['DIRECT', 'CORROBORATED', 'INDIRECT', 'ABSENT', 'INACCESSIBLE'],
  verification_result: ['VERIFIED', 'PARTIALLY_VERIFIED', 'UNVERIFIED', 'CONTRADICTED', 'NOT_APPLICABLE'],
  access_level: ['FULL', 'PARTIAL', 'DOCUMENT_ONLY', 'SEARCH_ONLY', 'NONE'],
  authorization_level: ['READ_ONLY', 'ANALYSIS_ONLY', 'DOC_REFACTOR', 'TEST_REFACTOR',
                        'CODE_REFACTOR', 'ARCHITECTURE_CHANGE', 'COMMIT', 'PUSH'],
  execution_result: ['NOT_EXECUTED', 'SUCCEEDED', 'PARTIALLY_SUCCEEDED', 'FAILED', 'STOPPED'],
  risk: ['LOW', 'MEDIUM', 'HIGH', 'ARCHITECTURAL']
};

/* Values that must never appear as a verification_result. */
const FORBIDDEN_VERIFICATION_VALUES = ['IMPLEMENTED', 'TESTED', 'DOCUMENTED', 'PLANNED', 'MISSING', 'TRUE', 'FALSE'];

const record = JSON.parse(fs.readFileSync(RECORD_PATH, 'utf8'));

/* -------------------------------------------------------------------------- */
/* 1. Schema shape                                                            */
/* -------------------------------------------------------------------------- */

{
  const missing = ['repository', 'scope', 'claims', 'changes', 'authorization', 'execution', 'post_verification']
    .filter(k => !(k in record));
  if (missing.length === 0) pass('record contains every required top-level block');
  else fail('record contains every required top-level block', missing.join(', '));

  const generic = [];
  (function walk(node, at) {
    if (Array.isArray(node)) return node.forEach((v, i) => walk(v, `${at}[${i}]`));
    if (node && typeof node === 'object') {
      for (const [k, v] of Object.entries(node)) {
        if (k === 'status' || k === 'state' || k === 'quality') generic.push(`${at}.${k}`);
        walk(v, `${at}.${k}`);
      }
    }
  })(record, '$');
  if (generic.length === 0) pass('no generic "status"/"state"/"quality" field is used');
  else fail('no generic "status"/"state"/"quality" field is used', generic.slice(0, 5).join(', '));
}

/* -------------------------------------------------------------------------- */
/* 2. Enum validation per field                                               */
/* -------------------------------------------------------------------------- */

{
  const bad = [];
  for (const c of record.claims) {
    for (const field of Object.keys(ENUMS).filter(f => f in c)) {
      if (!ENUMS[field].includes(c[field])) bad.push(`${c.id}.${field}=${c[field]}`);
    }
    if (FORBIDDEN_VERIFICATION_VALUES.includes(c.verification_result)) {
      bad.push(`${c.id}.verification_result=${c.verification_result}`);
    }
  }
  if (bad.length === 0) pass('every claim field uses its own canonical enum', `${record.claims.length} claims`);
  else fail('every claim field uses its own canonical enum', bad.slice(0, 8).join('; '));
}

{
  const r = record.repository;
  if (ENUMS.access_level.includes(r.access_level)) pass('repository.access_level uses the access enum', r.access_level);
  else fail('repository.access_level uses the access enum', r.access_level);

  if (ENUMS.authorization_level.includes(record.authorization.level)) {
    pass('authorization.level uses the authorization enum', record.authorization.level);
  } else {
    fail('authorization.level uses the authorization enum', record.authorization.level);
  }

  const extra = record.authorization.additional_levels_declared || [];
  const badExtra = extra.filter(l => !ENUMS.authorization_level.includes(l));
  if (badExtra.length === 0) pass('declared additional authorization levels are canonical',
    extra.join(', ') || '(none)');
  else fail('declared additional authorization levels are canonical', badExtra.join(', '));

  if (ENUMS.execution_result.includes(record.execution.result)) pass('execution.result uses the execution enum', record.execution.result);
  else fail('execution.result uses the execution enum', record.execution.result);

  if (ENUMS.verification_result.includes(record.post_verification.result)) {
    pass('post_verification.result reuses the verification enum', record.post_verification.result);
  } else {
    fail('post_verification.result reuses the verification enum', record.post_verification.result);
  }
}

/* -------------------------------------------------------------------------- */
/* 3. Evidence and absence discipline                                         */
/* -------------------------------------------------------------------------- */

{
  const register = fs.readFileSync(REGISTER_PATH, 'utf8');
  const defined = new Set(
    [...register.matchAll(/^\|\s*((?:CODE|TEST|DOC|CFG|HIST|ARCH|SCOPE|CONC|PROV|FAIL)-\d{3})\s*\|/gm)].map(m => m[1])
  );

  const unknown = [];
  for (const c of record.claims) {
    for (const id of c.evidence) if (!defined.has(id)) unknown.push(`${c.id}->${id}`);
  }
  if (unknown.length === 0) pass('every claim evidence reference exists in the register');
  else fail('every claim evidence reference exists in the register', unknown.join(', '));

  /* Documentation alone cannot establish an implementation claim. */
  const docOnly = record.claims.filter(c =>
    c.evidence.length > 0 &&
    c.evidence.every(id => id.startsWith('DOC-') || id.startsWith('HIST-')) &&
    (c.evidence_level === 'DIRECT' || c.evidence_level === 'CORROBORATED') &&
    c.implementation_state === 'IMPLEMENTED');
  if (docOnly.length === 0) pass('no implementation claim rests on documentation alone');
  else fail('no implementation claim rests on documentation alone', docOnly.map(c => c.id).join(', '));

  /* INACCESSIBLE must not be converted into ABSENT. */
  const access = record.repository.access_level;
  const inaccessible = record.claims.filter(c => c.evidence_level === 'INACCESSIBLE');
  const absent = record.claims.filter(c => c.evidence_level === 'ABSENT');
  if (access === 'FULL' && inaccessible.length > 0) {
    fail('INACCESSIBLE is not used when access was full', inaccessible.map(c => c.id).join(', '));
  } else if (access === 'FULL') {
    pass('absence claims are ABSENT, not INACCESSIBLE, because access was full',
      `${absent.length} absent, 0 inaccessible`);
  } else {
    fail('absence claims require full access to be labelled ABSENT',
      `access_level=${access}, ${absent.length} ABSENT claim(s)`);
  }

  const external = record.repository.external_sources_used;
  if (external === false) pass('no external source is used as repository evidence');
  else fail('no external source is used as repository evidence');
}

/* -------------------------------------------------------------------------- */
/* 4. Authorization, change set and execution consistency                     */
/* -------------------------------------------------------------------------- */

{
  const authorized = new Set(record.authorization.authorized_changes);
  const changes = new Map(record.changes.map(c => [c.id, c]));

  const unknownAuthorized = [...authorized].filter(id => !changes.has(id));
  if (unknownAuthorized.length === 0) pass('every authorized change ID exists in the change list');
  else fail('every authorized change ID exists in the change list', unknownAuthorized.join(', '));

  const executedNotAuthorized = record.execution.executed_changes.filter(id => !authorized.has(id));
  if (executedNotAuthorized.length === 0) {
    pass('executed changes are a subset of authorized changes',
      `${record.execution.executed_changes.length}/${authorized.size}`);
  } else {
    fail('executed changes are a subset of authorized changes', executedNotAuthorized.join(', '));
  }

  const declaredUnauthorized = record.execution.unauthorized_changes || [];
  if (declaredUnauthorized.length === 0) pass('no unauthorized change was executed');
  else fail('no unauthorized change was executed', declaredUnauthorized.join(', '));

  const markedExecuted = record.changes.filter(c => c.executed === true).map(c => c.id);
  const mismatch = markedExecuted.filter(id => !record.execution.executed_changes.includes(id));
  if (mismatch.length === 0) pass('change flags agree with the execution record');
  else fail('change flags agree with the execution record', mismatch.join(', '));

  const forbidden = new Set(record.authorization.forbidden_operations);
  if (forbidden.has('MODIFY_SOURCE_CODE')) {
    const codeChanges = record.changes.filter(c => c.executed === true &&
      ['CODE_FIX', 'CODE_REFACTOR', 'ARCHITECTURE_CHANGE'].includes(c.category));
    if (codeChanges.length === 0) pass('no code change was executed while code mutation was forbidden');
    else fail('no code change was executed while code mutation was forbidden', codeChanges.map(c => c.id).join(', '));
  }

  const badCategory = record.changes.filter(c => !/^(DOC_|CODE_|TEST_|RENAME|REMOVAL|ARCHITECTURE_)/.test(c.category));
  if (badCategory.length === 0) pass('change categories are canonical');
  else fail('change categories are canonical', badCategory.map(c => c.id).join(', '));

  const badRisk = record.changes.filter(c => !ENUMS.risk.includes(c.risk));
  if (badRisk.length === 0) pass('change risks use the risk enum');
  else fail('change risks use the risk enum', badRisk.map(c => c.id).join(', '));
}

/* -------------------------------------------------------------------------- */
/* 5. Generated claims table is current                                       */
/* -------------------------------------------------------------------------- */

{
  try {
    execFileSync(process.execPath, [path.join(ROOT, 'tools', 'render-claims.mjs'), '--check'],
      { cwd: ROOT, stdio: 'pipe' });
    pass('claims.md matches analysis.json', 'generated tables are current');
  } catch (error) {
    fail('claims.md matches analysis.json',
      String(error.stdout || error.message).trim().split('\n').pop());
  }
}

/* -------------------------------------------------------------------------- */
/* 6. Five questions remain independently answerable                          */
/* -------------------------------------------------------------------------- */

{
  const counts = {};
  for (const field of ['claim_kind', 'implementation_state', 'test_state', 'evidence_level', 'verification_result']) {
    counts[field] = new Set(record.claims.map(c => c[field])).size;
  }
  const used = Object.values(counts).filter(n => n > 1).length;
  if (used === Object.keys(counts).length) {
    pass('all five claim fields carry independent information',
      Object.entries(counts).map(([k, v]) => `${k}=${v} values`).join(', '));
  } else {
    fail('all five claim fields carry independent information',
      Object.entries(counts).map(([k, v]) => `${k}=${v} values`).join(', '));
  }
}

/* -------------------------------------------------------------------------- */
/* Report                                                                     */
/* -------------------------------------------------------------------------- */

const width = Math.max(...results.map(r => r[1].length));
console.log('validating docs/analysis/analysis.json against the canonical schema\n');
for (const [level, message, note] of results) {
  console.log(`[${level}] ${message.padEnd(width)}  ${note}`);
}
const failures = results.filter(r => r[0] === 'FAIL').length;
console.log(`\n${results.filter(r => r[0] === 'PASS').length} passed, ${failures} failed`);
process.exit(failures === 0 ? 0 : 1);
