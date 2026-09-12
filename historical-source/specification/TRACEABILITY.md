# Forward and Reverse Traceability

> **Derivation gate: CLOSED — REJECTED_INVALID_OBLIGATION_PACKAGE.** The v10.1 input contract failed, no source obligation is `VERIFIED`, epistemic `UNKNOWN` records remain, and four obligation conflicts are unresolved. Protocol-v11 therefore emits no normative requirements. This is a validated rejection/audit package, not a normative implementation specification.

The graph retains 304 source/evidence/property/obligation nodes and 322 forward edges, plus exact reverse edges. Traversal intentionally terminates at obligation because the derivation gate is closed.

```text
SOURCE → EVIDENCE → PROPERTY → OBLIGATION ┤ CLOSED GATE
REQUIREMENT → RULE → CRITERION → ORACLE → TEST → RESULT  (not instantiated)
```
