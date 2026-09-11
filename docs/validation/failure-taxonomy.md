# Failure Taxonomy

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Every failure taxonomy recorded in the planning conversation, grouped by the version that introduced it.

## Contents

- **v0.11 — 12. Recognition failure taxonomy** — `Continue Architecture Planning.md` L57893–57897
- **v0.13 — 18. Discovery failure taxonomy** — `Continue Architecture Planning.md` L60260–60288
- **v0.14 — 25. Failure taxonomy** — `Continue Architecture Planning.md` L61852–61884
- **v0.16 — 35. Failure taxonomy** — `Continue Architecture Planning.md` L65054–65084
- **v0.17 — 29. Failure taxonomy** — `Continue Architecture Planning.md` L66422–66448
- **v0.18 — 18.22 Failure Taxonomy** — `Continue Architecture Planning.md` L67939–67964
- **v0.19 — 19.26 Failure Modes** — `Continue Architecture Planning.md` L69544–69567
- **v0.20 — 20.28 Failure Modes** — `Continue Architecture Planning.md` L70944–70971
- **v0.21 — 21.28 Failure Taxonomy** — `Continue Architecture Planning.md` L72430–72450
- **v0.22 — 22.23 Failure taxonomy** — `Continue Architecture Planning.md` L73809–73854
- **v0.23 — 23.8 Failure → evidence mapping** — `Continue Architecture Planning.md` L74449–74481
- **v0.26 — 26.20 Failure taxonomy** — `Continue Architecture Planning.md` L79582–79584
- **v0.28 — 28.31 Failure taxonomy** — `Continue Architecture Planning.md` L82948–82989
- **v0.30 — 30.24 Failure taxonomy** — `Continue Architecture Planning.md` L86282–86305
- **v0.32 — 32.33 Failure taxonomy** — `Continue Architecture Planning.md` L88935–88959
- **v0.33 — 33.28 Multi-worker failure modes** — `Continue Architecture Planning.md` L90062–90083
- **v0.34 — 34.25 Failure Taxonomy** — `Continue Architecture Planning.md` L91624–91666

## Related Documents

- [Invariants](invariants.md)
- [Response Recognition](../acquisition/response-recognition.md)
- [Discovery Model](../architecture/discovery-model.md)
- [Persistence and Crash Recovery](../architecture/persistence-and-recovery.md)

---

<!-- source: Continue Architecture Planning.md L57893–57897 | turn 35 | version 0.11 -->
## v0.11 — 12. Recognition failure taxonomy

This becomes important for diagnostics.

These are different:

<!-- source: Continue Architecture Planning.md L60260–60288 | turn 39 | version 0.13 -->
## v0.13 — 18. Discovery failure taxonomy

v0.13 should distinguish:

| Failure | Meaning |
| --- | --- |
| `source-disabled` | Source is configured off |
| `source-ineligible` | Context unsuitable |
| `source-budget-exhausted` | Source quota consumed |
| `task-budget-exhausted` | Global discovery quota consumed |
| `depth-limit` | Expansion depth exceeded |
| `proposal-limit` | Task generated too many proposals |
| `invalid-proposal` | Proposal malformed |
| `normalization-failed` | Target couldn't be normalized |
| `policy-rejected` | Candidate violates discovery policy |
| `duplicate-candidate` | Existing identity |
| `source-error` | Source itself failed |

And:

```
duplicate-candidate
```

is **not an error**.

It is a normal convergence event.

---

<!-- source: Continue Architecture Planning.md L61852–61884 | turn 41 | version 0.14 -->
## v0.14 — 25. Failure taxonomy

v0.14 adds another layer to the failure model.

| Failure | Meaning |
| --- | --- |
| `domain-rejected` | Candidate outside search domain |
| `seed-invalid` | Seed cannot be normalized |
| `seed-out-of-domain` | Seed is valid but outside domain |
| `session-cancelled` | User/system cancelled scan |
| `session-stopped` | Explicit stop |
| `candidate-limit` | Search truncated by candidate budget |
| `acquisition-limit` | Search truncated by acquisition budget |
| `discovery-limit` | Discovery task budget exhausted |
| `proposal-limit` | Proposal budget exhausted |
| `depth-limit` | Search reached allowed depth |
| `frontier-exhausted` | Natural completion |
| `lease-expired` | Previous worker/session lost ownership |
| `recovery-requeued` | Work safely returned to frontier |

Again:

```
frontier-exhausted
```

is fundamentally different from:

```
candidate-limit
```

---

<!-- source: Continue Architecture Planning.md L65054–65084 | turn 45 | version 0.16 -->
## v0.16 — 35. Failure taxonomy

v0.16 adds epistemic failures.

| Failure | Meaning |
| --- | --- |
| `evidence-missing-source` | Evidence has no valid provenance |
| `locator-invalid` | Evidence locator cannot identify its source |
| `extraction-error` | Parser failed |
| `unrecognized-observation` | Observation has no recognized interpretation |
| `claim-unsupported` | Claim has no supporting evidence |
| `evidence-conflict` | Evidence contradicts another observation |
| `fingerprint-unavailable` | Bytes could not be fingerprinted |
| `resource-identity-ambiguous` | Identity cannot safely be resolved |
| `provenance-incomplete` | Historical chain is incomplete |

Again, not every one of these is an operational failure.

For example:

```
unrecognized-observation
```

can simply mean:

> We successfully acquired something that the current recognizers do not understand.

That is valuable information.

---

<!-- source: Continue Architecture Planning.md L66422–66448 | turn 47 | version 0.17 -->
## v0.17 — 29. Failure taxonomy

v0.17 introduces identity failures.

| Condition | Interpretation |
| --- | --- |
| `canonicalization-conflict` | normalization rules produce incompatible identities |
| `redirect-cycle` | redirect chain cycles |
| `identity-ambiguous` | insufficient evidence |
| `identity-conflict` | evidence supports incompatible relationships |
| `fingerprint-conflict` | expected identical content differs |
| `relation-unsupported` | resolver cannot justify relation |
| `invalid-locator` | locator cannot be represented safely |
| `destructive-merge-blocked` | attempted unsafe identity merge |
| `provenance-missing` | relation lacks supporting evidence |

Again:

```
identity-ambiguous
```

is not necessarily an error.

It is often the correct result.

---

<!-- source: Continue Architecture Planning.md L67939–67964 | turn 49 | version 0.18 -->
## v0.18 — 18.22 Failure Taxonomy

v0.18 should explicitly distinguish:

| Failure | Meaning |
| --- | --- |
| `classifier-unavailable` | No classifier can handle resource |
| `classification-error` | Classifier failed |
| `insufficient-evidence` | Evidence exists but is inadequate |
| `classification-ambiguous` | Multiple plausible classes |
| `classification-conflict` | Evidence supports incompatible classes |
| `type-unknown` | No useful classification |
| `type-registry-missing` | Assertion refers to unknown type |
| `invalid-classification` | Classifier produced malformed assertion |
| `classifier-version-mismatch` | Historical classifier unavailable |
| `classification-superseded` | Newer classification replaces interpretation |

And importantly:

```
unknown ≠ failure
```

An unknown resource is still useful knowledge.

---

<!-- source: Continue Architecture Planning.md L69544–69567 | turn 51 | version 0.19 -->
## v0.19 — 19.26 Failure Modes

| Failure | Interpretation |
| --- | --- |
| `artifact-hash-failed` | Bytes could not be hashed |
| `artifact-incomplete` | Acquisition did not produce complete bytes |
| `artifact-corrupted` | Stored bytes fail integrity validation |
| `representation-conflict` | Evidence disagrees about representation |
| `revision-ambiguous` | Change detected but revision meaning unclear |
| `revision-order-conflict` | Temporal ordering cannot be established |
| `artifact-unavailable` | Metadata exists but bytes are unavailable |
| `resource-identity-conflict` | Artifact evidence conflicts with resource identity |
| `representation-unresolved` | Logical representation cannot be determined |
| `storage-failed` | Artifact exists conceptually but persistence failed |

Again:

```
unknown revision
≠
failed acquisition
```

---

<!-- source: Continue Architecture Planning.md L70944–70971 | turn 53 | version 0.20 -->
## v0.20 — 20.28 Failure Modes

| Failure | Meaning |
| --- | --- |
| `partition-invalid` | malformed partition definition |
| `partition-outside-domain` | partition violates domain |
| `partition-overlap` | partition overlaps existing region |
| `strategy-unavailable` | no strategy can explore it |
| `strategy-failed` | exploration strategy failed |
| `partition-budget-exhausted` | local budget reached |
| `global-budget-exhausted` | scan-wide budget reached |
| `partition-saturated` | exploration has low marginal yield |
| `partition-exhausted` | strategy completed its defined exploration |
| `partition-starved` | partition waited too long |
| `partition-split-rejected` | proposed subdivision denied |
| `coverage-unknown` | completeness cannot be established |

The last one is particularly important.

For an open web:

```
coverage = unknown
```

is often the correct answer.

---

<!-- source: Continue Architecture Planning.md L72430–72450 | turn 55 | version 0.21 -->
## v0.21 — 21.28 Failure Taxonomy

v0.21 adds:

| Failure | Meaning |
| --- | --- |
| `strategy-no-match` | no strategy can handle partition |
| `strategy-ineligible` | strategy violates current constraints |
| `strategy-cold-start` | insufficient historical information |
| `strategy-starved` | strategy never receives exploration opportunity |
| `strategy-score-unstable` | scoring inputs changed during decision |
| `strategy-history-stale` | historical data too old |
| `strategy-temporary-failure` | transient execution problem |
| `strategy-structural-failure` | strategy cannot work in this context |
| `adaptive-budget-exhausted` | adaptation budget exhausted |
| `exploration-quota-exhausted` | exploration allocation consumed |
| `exploitation-starvation` | exploratory work dominates |
| `decision-nondeterministic` | decision cannot be replayed |
| `strategy-policy-conflict` | optimization conflicts with hard policy |

---

<!-- source: Continue Architecture Planning.md L73809–73854 | turn 57 | version 0.22 -->
## v0.22 — 22.23 Failure taxonomy

v0.22 introduces a new class of failures:

```
COVERAGE
├── coverage-undefined
├── denominator-unknown
├── snapshot-missing
├── snapshot-changed
├── coverage-estimate-invalid
├── coverage-method-unsupported
│
COMPLETENESS
├── completeness-not-established
├── completeness-evidence-missing
├── completeness-conflict
├── enumerator-incomplete
├── enumerator-invalid
├── enumeration-truncated
├── enumeration-pagination-unknown
│
ABSENCE
├── absence-not-provable
├── negative-evidence-weak
├── negative-evidence-conflict
│
SEARCH SPACE
├── inaccessible-partition
├── unsupported-partition
├── unknown-boundary
└── dynamic-universe
```

These are not necessarily execution failures.

Many mean:

```
the engine successfully searched
but cannot make the requested assurance claim.
```

That distinction matters.

---

<!-- source: Continue Architecture Planning.md L74449–74481 | turn 59 | version 0.23 -->
## v0.23 — 23.8 Failure → evidence mapping

A useful mapping:

| Event | Negative evidence? |
| --- | --- |
| Empty complete manifest | Yes |
| Empty verified directory enumeration | Yes |
| Search query returns zero | Weak |
| HTML crawl returns zero | Weak |
| 404 for exact immutable locator | Moderate/strong for that locator |
| 403 | No |
| Timeout | No |
| DNS failure | No |
| Parser failure | No |
| Unsupported format | No |
| Authentication required | No |
| Incomplete pagination | No |
| Truncated sitemap | No |

The distinction is:

```
NO MATCH
```

versus:

```
COULD NOT OBSERVE
```

---

<!-- source: Continue Architecture Planning.md L79582–79584 | turn 65 | version 0.26 -->
## v0.26 — 26.20 Failure taxonomy

v0.26 introduces tactic-specific failures.

<!-- source: Continue Architecture Planning.md L82948–82989 | turn 69 | version 0.28 -->
## v0.28 — 28.31 Failure taxonomy

v0.28 introduces:

```
identity-ambiguity
locator-equivalence-unknown
partition-overlap-unknown
coverage-union-unknown
duplicate-work
duplicate-observation
artifact-match-conflict
resource-merge-blocked
coverage-accounting-conflict
provenance-loss
independence-unknown
snapshot-incompatible
```

Most importantly:

```
UNKNOWN
```

must remain a valid answer.

The resolver should not force:

```
same
```

or:

```
different
```

when evidence is insufficient.

---

<!-- source: Continue Architecture Planning.md L86282–86305 | turn 75 | version 0.30 -->
## v0.30 — 30.24 Failure taxonomy

v0.30 adds:

| Failure | Meaning |
| --- | --- |
| `ineligible` | Work cannot currently execute |
| `dependency-blocked` | Required work incomplete |
| `budget-blocked` | Required budget unavailable |
| `capability-blocked` | Runtime lacks capability |
| `policy-blocked` | Policy forbids execution |
| `domain-blocked` | Outside search domain |
| `backpressured` | Downstream capacity unavailable |
| `class-starvation` | Work class receives insufficient service |
| `item-starvation` | Individual work waits excessively |
| `priority-inversion` | Dependency ordering prevents progress |
| `claim-conflict` | Another worker claimed work |
| `score-instability` | Ranking changes excessively |
| `cost-estimation-error` | Actual cost diverges substantially |
| `fairness-conflict` | Fairness and utility objectives conflict |
| `arbitration-nondeterministic` | Same state produced different decision |
| `frontier-monopolization` | One class consumes disproportionate capacity |

---

<!-- source: Continue Architecture Planning.md L88935–88959 | turn 79 | version 0.32 -->
## v0.32 — 32.33 Failure taxonomy

v0.32 adds:

| Failure | Meaning |
| --- | --- |
| `transaction-incomplete` | Durable transaction lacks commit |
| `write-failed` | Persistence operation failed |
| `schema-incompatible` | Stored state cannot be interpreted |
| `migration-failed` | Schema migration failed |
| `lease-expired` | Worker ownership expired |
| `reservation-orphaned` | Reservation has no valid owner |
| `settlement-orphaned` | Settlement has no valid reservation |
| `checkpoint-invalid` | Checkpoint cannot be trusted |
| `cursor-inconsistent` | Cursor conflicts with durable knowledge |
| `state-conflict` | Materialized state conflicts with ledger |
| `artifact-undurable` | Artifact reference exists without durable bytes |
| `observation-undurable` | Observation existed only in transient state |
| `recovery-uncertain` | Outcome cannot be determined |
| `recovery-partial` | Some state recovered, some unresolved |
| `snapshot-corrupt` | Snapshot integrity failure |
| `ledger-gap` | Durable event sequence has a gap |
| `reconciliation-conflict` | Recovery rules cannot resolve state safely |

---

<!-- source: Continue Architecture Planning.md L90062–90083 | turn 81 | version 0.33 -->
## v0.33 — 33.28 Multi-worker failure modes

| Failure | Meaning |
| --- | --- |
| `claim-conflict` | another worker won the claim |
| `lease-expired` | worker stopped renewing |
| `stale-worker` | worker continued after losing ownership |
| `fencing-rejected` | stale mutation rejected |
| `worker-disappeared` | worker no longer responsive |
| `heartbeat-failed` | lease renewal failed |
| `worker-overloaded` | worker capacity exhausted |
| `capability-mismatch` | worker cannot execute work |
| `reservation-conflict` | concurrent resource allocation conflict |
| `duplicate-execution` | same work executed more than once |
| `duplicate-observation` | repeated observation detected |
| `coordination-split-brain` | multiple contexts believe they own authority |
| `state-stale` | worker cache conflicts with durable state |
| `clock-skew` | time assumptions unreliable |
| `orphaned-claim` | ownership cannot be resolved |
| `orphaned-reservation` | resource allocation lacks valid owner |

---

<!-- source: Continue Architecture Planning.md L91624–91666 | turn 83 | version 0.34 -->
## v0.34 — 34.25 Failure Taxonomy

v0.34 adds:

```
STALE_STATE
EXPECTED_VERSION_MISMATCH
VERSION_GAP
VERSION_REGRESSION
CONFLICT_DETECTED
CONFLICT_UNCLASSIFIED
CONFLICT_UNRESOLVED
RESOLUTION_REJECTED
RESOLUTION_POLICY_MISSING
RESOLUTION_NONDETERMINISTIC
MERGE_LOSS
PROVENANCE_LOSS
CAUSALITY_AMBIGUOUS
CROSS_SCOPE_CONFLICT
ACCOUNTING_CONFLICT
SNAPSHOT_DIGEST_MISMATCH
MATERIALIZED_STATE_DIVERGENCE
EVENT_SEQUENCE_GAP
DUPLICATE_EVENT
INVALID_FENCING_EPOCH
STALE_WORKER_MUTATION
```

Important:

```
conflict ≠ failure
```

A conflict is often normal in a concurrent system.

The failure is:

```
conflict → silent corruption
```

---
