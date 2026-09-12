# Protocol-v14.1 Independent Certificate-State Validation

**Overall:** `STRUCTURAL_PASS_CURRENT_CERTIFICATION_NOT_APPLICABLE`
**Acceptance:** `BLOCKED`
**Checks:** 82 PASS / 0 FAIL / 1 BLOCKED (83 total)

Structural validity does not create a certificate candidate, eligibility decision, issuance action, certificate, or release authorization.

| ID | Category | Result | Description | Detail |
|---|---|---|---|---|
| I01 | inventory | PASS | all 72 generator-owned v14.1 deliverables exist |  |
| I02 | syntax | PASS | all v14.1 YAML is JSON-compatible and parseable | [] |
| S01 | schemas | PASS | all 21 schemas have unique stable IDs |  |
| S02 | schemas | PASS | all object schemas reject undeclared fields |  |
| S03 | schemas | PASS | schema registry resolves all 21 schemas with exact hashes | [] |
| S04 | schemas | PASS | all applicable production and synthetic objects satisfy schemas | [] |
| M01 | separation | PASS | lifecycle, eligibility, validity, and release are independent |  |
| M02 | reconciliation | PASS | v14 is preserved while VALID and INVALID move to derived validity |  |
| M03 | lifecycle | PASS | normative lifecycle contains exactly five states and excludes validity terms |  |
| T01 | state-machine | PASS | six permitted lifecycle transitions are exact |  |
| T02 | state-machine | PASS | all terminal states prohibit outgoing transitions |  |
| T03 | state-machine | PASS | complete 5x5 transition matrix reproduces |  |
| T04 | test-vectors | PASS | all 25 lifecycle transition vectors reproduce |  |
| T05 | history | PASS | all lifecycle history projections reproduce without skipping malformed events | [] |
| T06 | revocation | PASS | revocation requires reason, authority, evidence, and timestamp |  |
| T07 | supersession | PASS | replacement requires new identity and preserves old certificate |  |
| T08 | expiration | PASS | expiration derives deterministically from valid-until, policy, and explicit evaluation time |  |
| T09 | terminal-actions | PASS | revocation completeness and supersession identity are executable |  |
| E01 | eligibility | PASS | exact four eligibility outcomes retain blocked/unknown distinction |  |
| E02 | eligibility | PASS | all twelve mandatory predicates expose four predicate outcomes |  |
| E03 | precedence | PASS | invalid/false dominates blocked and blocked dominates unknown |  |
| E04 | test-vectors | PASS | all nine deterministic eligibility vectors reproduce | [] |
| E05 | hashes | PASS | eligibility inputs and immutable decisions have canonical hashes | [] |
| E06 | precedence | PASS | proven ineligibility dominates blocked mechanically |  |
| E07 | precedence | PASS | blocked dominates semantic unknown mechanically |  |
| E08 | unknown | PASS | unknown remains UNKNOWN rather than INELIGIBLE |  |
| E09 | history | PASS | INELIGIBLE→BLOCKED→ELIGIBLE remains three immutable decisions |  |
| E10 | policy | PASS | certification policy hash and precedence reproduce |  |
| E11 | policy | PASS | certificate type explicitly maps to aggregate without changing aggregate truth | [] |
| E12 | waiver | PASS | waiver validity influences eligibility without changing aggregate truth | [] |
| U01 | issuance | PASS | issuance requires eligibility, authority, payload, seal, action, and draft |  |
| U02 | test-vectors | PASS | all six issuance vectors reproduce independently | [] |
| U03 | hashes | PASS | issuance authority, action, and result records have canonical hashes | [] |
| U04 | non-implication | PASS | ELIGIBLE without issuance action remains DRAFT |  |
| V01 | validity | PASS | seven validity outcomes are derived outside lifecycle |  |
| V02 | validity | PASS | eleven ordered validity checks are explicit and deterministic |  |
| V03 | test-vectors | PASS | all eighteen derived validity vectors reproduce independently | [] |
| V04 | hashes | PASS | all validity result hashes reproduce | [] |
| V05 | derived-status | PASS | issued certificate may derive INVALID without lifecycle transition |  |
| V06 | terminal-status | PASS | terminal lifecycle state remains authoritative while all failures are reported |  |
| V07 | validity | PASS | NOT_YET_VALID and interval expiration derive from explicit evaluated_at |  |
| V08 | precedence | PASS | multiple validity failures report all while integrity selects INVALID |  |
| R01 | release | PASS | release consumes ISSUED plus VALID and never substitutes eligibility |  |
| R02 | test-vectors | PASS | all seven release-certificate vectors reproduce | [] |
| R03 | release | PASS | current eligibility is not used as substitute for issued certificate validity |  |
| R04 | hashes | PASS | release-certificate evaluation hashes reproduce | [] |
| N00 | non-implication | PASS | all eight critical non-implications are executable |  |
| N01 | invariants | PASS | CERT-021 through CERT-040 have exact stable IDs and checks |  |
| CERT-021 | certificate-invariant | PASS | VALID MUST NOT be represented as a certificate lifecycle state. |  |
| CERT-022 | certificate-invariant | PASS | Eligibility MUST be represented independently of certificate lifecycle. |  |
| CERT-023 | certificate-invariant | PASS | Validity MUST be derived independently of issuance state. |  |
| CERT-024 | certificate-invariant | PASS | ELIGIBLE MUST NOT imply ISSUED. |  |
| CERT-025 | certificate-invariant | PASS | ISSUED MUST NOT imply currently VALID. |  |
| CERT-026 | certificate-invariant | PASS | Certificate eligibility MUST be evaluated before issuance. |  |
| CERT-027 | certificate-invariant | PASS | A proven mandatory eligibility failure dominates BLOCKED. |  |
| CERT-028 | certificate-invariant | PASS | BLOCKED dominates UNKNOWN when evaluation is concretely blocked. |  |
| CERT-029 | certificate-invariant | PASS | UNKNOWN MUST NOT be interpreted as INELIGIBLE. |  |
| CERT-030 | certificate-invariant | PASS | Invalid required input produces INELIGIBLE. |  |
| CERT-031 | certificate-invariant | PASS | Historical eligibility decisions MUST remain immutable. |  |
| CERT-032 | certificate-invariant | PASS | Certificate lifecycle transitions MUST be validated. |  |
| CERT-033 | certificate-invariant | PASS | Terminal certificate states MUST NOT return to ISSUED. |  |
| CERT-034 | certificate-invariant | PASS | A replacement certificate MUST have a new certificate identity. |  |
| CERT-035 | certificate-invariant | PASS | Certificate validity MUST be independently recomputable. |  |
| CERT-036 | certificate-invariant | PASS | Release authorization MUST NOT use eligibility as a substitute for validity. |  |
| CERT-037 | certificate-invariant | PASS | A valid signature MUST NOT establish aggregate conformance. |  |
| CERT-038 | certificate-invariant | PASS | A waiver MUST NOT change the underlying aggregate result. |  |
| CERT-039 | certificate-invariant | PASS | Certification policy MUST explicitly define which aggregate results are eligible for each certificate type. |  |
| CERT-040 | certificate-invariant | PASS | Certificate eligibility MUST expose the predicates responsible for ELIGIBLE, INELIGIBLE, BLOCKED, or UNKNOWN outcomes. |  |
| C01 | current | PASS | current upstream truth remains blocked at SPEC_INVALID with no aggregate |  |
| C02 | non-invention | PASS | no current candidate, certificate, history, eligibility decision, or issuance action is invented |  |
| C03 | current | PASS | current no-certificate projection preserves independent dimensions |  |
| C04 | current | PASS | release remains not evaluated |  |
| O01 | registry | PASS | two v14.1 current normative object IDs are unique |  |
| O02 | registry | PASS | v14.1 object IDs are globally unique from predecessors |  |
| O03 | references | PASS | predecessor registry references resolve with exact hashes |  |
| P01 | append-only | PASS | all 364 predecessor compliance artifacts remain byte-identical | [] |
| P02 | append-only | PASS | v14 builder refuses to erase v14.1 extension |  |
| Q01 | determinism | PASS | all 72 generator outputs reproduce byte-for-byte |  |
| Q02 | regression | PASS | v10.1 through v14 regressions and append guards pass |  |
| Q03 | hygiene | PASS | no Python cache artifacts exist |  |
| Q04 | tools | PASS | generic and pinned v14.1 builders and validators exist |  |
| G01 | reports | PASS | four reports preserve lifecycle, eligibility, validity, and release separation |  |
| GATE-V141 | acceptance | BLOCKED | current certification and release | The v14.1 protocol validates structurally; current v13.3 specification validation remains blocked, no certificate candidate or certificate exists, eligibility is not applicable, validity is UNKNOWN, and release is not evaluated. |
