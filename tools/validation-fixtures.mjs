/*
 * ============================================================================
 * Validation fixtures — the rule sets of brief 11, executed
 * ============================================================================
 *
 * A rule that is never exercised is a claim, not an enforcement. Each fixture
 * below mutates the canonical record (or the registries) into a state that one
 * rule forbids, and `node tools/validate-analysis.mjs --self-test` fails unless
 * the validator rejects it with the expected code in the expected phase.
 *
 * Section references point at the brief that states the rule; the section 233-240
 * examples are reproduced here as fixtures, and the remaining cases are the
 * minimal mutation that isolates a rule.
 *
 * `mutate(document, context)` receives a deep copy of the record and of the
 * registries, so a fixture never touches the repository.
 */

const firstClaim = document => document.claims[0];
const firstGrant = document => document.authorization.capability_grants[0];

export const fixtures = [
  {
    id: 'FX-001', rule: 'X-003', code: 'X-003', phase: 'SEMANTIC',
    note: 'section 234 — authorization.change_ids references an unknown change',
    mutate: document => { document.authorization.change_ids.push('R-999'); },
  },
  {
    id: 'FX-002', rule: 'X-011', code: 'X-011', phase: 'SEMANTIC',
    note: 'section 235 — a grant for a capability no profile declares (anti-escalation)',
    mutate: (document, context) => {
      context.registries.capability.entries.push({
        id: 'CAP-ORBIT-CHANGE', resource_class: 'REPOSITORY', operations: ['PROPOSE'],
        constraints: { scope_model: 'NONE' }, lifecycle: { grantable: true },
      });
      document.authorization.capability_grants.push({ capability_id: 'CAP-ORBIT-CHANGE', state: 'ENABLED' });
    },
  },
  {
    id: 'FX-003', rule: 'X-010', code: 'X-010', phase: 'REGISTRY',
    note: 'section 235 — a grant for a capability the registry does not contain',
    mutate: document => {
      document.authorization.capability_grants[0] = { capability_id: 'CAP-DOCUMENT-TELEPORT', state: 'ENABLED' };
    },
  },
  {
    id: 'FX-004', rule: 'X-012', code: 'X-012', phase: 'REGISTRY',
    note: 'an operation the operation registry does not recognize',
    mutate: document => { document.authorization.operations.allow.push('TELEPORT'); },
  },
  {
    id: 'FX-005', rule: 'X-013', code: 'X-013', phase: 'REGISTRY',
    note: 'a target resource class the resource-class registry does not recognize',
    mutate: document => { document.execution.operations[1].target.resource_class = 'BLOCKCHAIN'; },
  },
  {
    id: 'FX-006', rule: 'X-016', code: 'X-016', phase: 'SEMANTIC',
    note: 'section 237 — a recorded operation that the narrowed restriction no longer admits',
    mutate: document => {
      const grant = document.authorization.capability_grants.find(g => g.capability_id === 'CAP-DOCUMENT-MODIFY');
      grant.scope = { paths: { include: ['docs/architecture/'], exclude: [] } };
    },
  },
  {
    id: 'FX-007', rule: 'X-018', code: 'X-018', phase: 'SEMANTIC',
    note: 'section 238 — successful mutations while authorization.state is DENIED',
    mutate: document => { document.authorization.state = 'DENIED'; },
  },
  {
    id: 'FX-008', rule: 'X-019', code: 'X-019', phase: 'SEMANTIC',
    note: 'verification that refers to an execution the document does not contain',
    mutate: document => { document.execution_verification.execution_id = 'EXEC-999'; },
  },
  {
    id: 'FX-009', rule: 'EVV-001', code: 'EVV-001', phase: 'VERIFICATION',
    note: 'section 239 — PASSED with result NON_CONFORMING',
    mutate: document => { document.execution_verification.result = 'NON_CONFORMING'; },
  },
  {
    id: 'FX-010', rule: 'TS-001', code: 'TS-001', phase: 'SEMANTIC',
    note: 'section 240 — completed_at set while started_at is null',
    mutate: document => { document.execution.started_at = null; },
  },
  {
    id: 'FX-011', rule: 'REQ-003', code: 'REQ-003', phase: 'STRUCTURAL',
    note: 'section 240 — GRANTED authorization without granted_at',
    mutate: document => { delete document.authorization.granted_at; },
  },
  {
    id: 'FX-012', rule: 'ST-001', code: 'ST-001', phase: 'STRUCTURAL',
    note: 'section 227 — a required-but-nullable field may be null, but not absent',
    mutate: document => { delete document.authorization.expires_at; },
  },
  {
    id: 'FX-013', rule: 'CAP-015', code: 'CAP-015', phase: 'AUTHORIZATION',
    note: 'section 236 — an operation allow-list cannot create authority',
    mutate: document => {
      document.authorization.operations.allow.push('DELETE');
      document.authorization.operations.deny = [];
    },
  },
  {
    id: 'FX-014', rule: 'X-020', code: 'X-020', phase: 'SEMANTIC',
    note: 'a verification finding names an authorized change (verification cannot authorize)',
    mutate: document => {
      document.execution_verification.findings = ['remediation: change R-021 was applied incorrectly'];
    },
  },
  {
    id: 'FX-015', rule: 'X-001', code: 'X-001', phase: 'SEMANTIC',
    note: 'a claim evidence id that no register row defines',
    mutate: document => { firstClaim(document).evidence[0].id = 'DOC-999'; },
  },
  {
    id: 'FX-016', rule: 'X-004', code: 'X-004', phase: 'SEMANTIC',
    note: 'an operation that references an unknown change',
    mutate: document => { document.execution.operations[0].change_id = 'R-999'; },
  },
  {
    id: 'FX-017', rule: 'X-007', code: 'X-007', phase: 'SEMANTIC',
    note: 'section 232 — authorization target is not the analyzed repository',
    mutate: document => { document.authorization.target.repository = 'someone/other-repository'; },
  },
  {
    id: 'FX-018', rule: 'X-008', code: 'X-008', phase: 'SEMANTIC',
    note: 'section 232 — authorization target revision is not the resolved revision',
    mutate: document => { document.authorization.target.revision = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeef'; },
  },
  {
    id: 'FX-019', rule: 'CV-006', code: 'CV-006', phase: 'SEMANTIC',
    note: 'VERIFIED carried by INDIRECT evidence',
    mutate: document => { firstClaim(document).evidence_level = 'INDIRECT'; },
  },
  {
    id: 'FX-020', rule: 'RG-004', code: 'RG-004', phase: 'REGISTRY',
    note: 'a claim the claim registry does not declare',
    mutate: (document, context) => {
      context.registries.claim.entries = context.registries.claim.entries.filter(e => e.id !== firstClaim(document).id);
    },
  },
  {
    id: 'FX-021', rule: 'X-006', code: 'X-006', phase: 'SEMANTIC',
    note: 'an unauthorized-list entry that resolves to nothing',
    mutate: document => { document.execution.unauthorized_changes = ['R-999']; },
  },
  {
    id: 'FX-022', rule: 'RG-005', code: 'RG-005', phase: 'REGISTRY',
    note: 'a capability whose scope model contradicts its resource class',
    mutate: (document, context) => {
      const entry = context.registries.capability.entries.find(c => c.id === 'CAP-DOCUMENT-MODIFY');
      entry.constraints.scope_model = 'NONE';
    },
  },
  {
    id: 'FX-023', rule: 'X-014', code: 'X-014', phase: 'REGISTRY',
    note: 'a capability that declares an operation the operation registry does not contain',
    mutate: (document, context) => {
      context.registries.capability.entries.find(c => c.id === 'CAP-DOCUMENT-MODIFY').operations.push('TRANSMUTE');
    },
  },
  {
    id: 'FX-024', rule: 'X-015', code: 'X-015', phase: 'REGISTRY',
    note: 'a capability whose resource class the resource-class registry does not contain',
    mutate: (document, context) => {
      context.registries.capability.entries.find(c => c.id === 'CAP-DOCUMENT-MODIFY').resource_class = 'BLOCKCHAIN';
    },
  },
  {
    id: 'FX-025', rule: 'RG-002', code: 'RG-002', phase: 'REGISTRY',
    note: 'section 220 — a registry revision tied to the analysis schema version',
    mutate: (document, context) => { context.registries.capability.registry_version = document.schema_version; },
  },
  {
    id: 'FX-026', rule: 'TS-005', code: 'TS-005', phase: 'SEMANTIC',
    note: 'NOT_STARTED with a started_at timestamp',
    mutate: document => {
      document.execution.state = 'NOT_STARTED';
      document.execution.completed_at = null;
    },
  },
  {
    id: 'FX-027', rule: 'EV-009', code: 'EV-009', phase: 'EXECUTION',
    note: 'an executed change with no operation to account for it',
    mutate: document => { document.execution.executed_changes.push('R-109'); },
  },
  {
    id: 'FX-031', rule: 'I-016', code: 'I-016', phase: 'SEMANTIC', fileChecks: true,
    note: 'a PLAN ONLY proposal that has entered the execution (change register cross-check)',
    mutate: document => { document.execution.executed_changes.push('R-109'); },
  },
  {
    id: 'FX-028', rule: 'SER-001', code: 'SER', phase: 'SEMANTIC',
    note: 'the YAML mirror and the record disagree',
    mutate: (document, context) => { context.yaml = { authorization: { ...context.yaml?.authorization, state: 'DENIED' } }; },
  },
  {
    id: 'FX-029', rule: 'RG-001', code: 'RG-001', phase: 'REGISTRY',
    note: 'a registry entry that loses a field the envelope schema requires',
    mutate: (document, context) => { delete context.registries.operation.entries[0].mutating; },
  },
  {
    id: 'FX-030', rule: 'EV-004', code: 'EV-004', phase: 'EXECUTION',
    note: 'an operation that succeeded without an ALLOWED decision',
    mutate: document => { document.execution.operations[1].authorization_decision = 'DENIED'; },
  },
];

export default fixtures;
