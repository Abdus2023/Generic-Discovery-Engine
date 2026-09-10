# DVB Blind Scan as Inspiration

```
claim_kind:           NON_GOAL for the physical layer · CURRENT for the analogy itself
implementation_state: NOT_IMPLEMENTED (no DVB/RF code exists in the inspected scope)
test_state:           NOT_APPLICABLE
evidence_level:       ABSENT (inspected, not found) · INDIRECT for the analogy's origin
verification_result:  VERIFIED as absent for DVB behaviour; the analogy itself is reasoning,
                      not evidence
```

Status: research note. Normative only for what the analogy may and may not be
used to claim.

## Why the analogy exists

A DVB receiver has no complete service list at start-up. It searches a parameter
space, detects energy, attempts to lock, validates what it receives, extracts
metadata, and uses that metadata to find more services. The generic property is
*discovery under incomplete knowledge with a feedback loop*, and that property
is domain-independent.

## The DVB blind scan process

```
sweep a frequency range
  → detect energy above the noise floor
  → try plausible bandwidths / symbol rates / modulation parameters
  → attempt carrier synchronization and demodulation
  → validate the transport stream
  → parse PSI/SI tables (network, transport stream, services)
  → deduplicate and continue until the range is covered
```

Each step narrows uncertainty and is only meaningful in the physical layer that
the next step assumes. **None of this is implemented here.**

## Analogy matrix

| DVB concept | Generic abstraction | Prototype implementation | Status |
| --- | --- | --- | --- |
| frequency candidate | candidate | URL + type, keyed `type:target` | implemented |
| RF observation | acquisition observation | `Observation` (status, HTTP metadata, body, errors) | implemented |
| carrier / signal detection | response availability | HTTP status and transport success/failure | implemented (remote) |
| demodulator lock | recognition | provider `matches()` | implemented (analogy only — no demodulation) |
| PSI/SI metadata | resource metadata | recognized URLs, forms, metadata URLs, resource records | implemented |
| NIT / network discovery | candidate expansion | `Discovery` → new candidates | implemented |
| scan database | knowledge base | `KnowledgeBase` + decision ledger + persistence | implemented (ephemeral semantics differ) |
| coverage of the frequency range | search-space coverage | none | **not implemented** (DESIGNED v0.22) |
| signal absence below noise floor | negative evidence | none | **not implemented** (DESIGNED v0.23) |
| blind vs guided scan | adaptive strategy | static priority table only | **not implemented** (DESIGNED v0.21) |
| multi-receiver coordination | multi-context claims | none | **not implemented** (DESIGNED v0.33) |

Rows marked *analogy only* exist to explain the architecture; they are not
equivalences.

## The boundary

| DVB | Generic | Evidence |
| --- | --- | --- |
| RF front end, tuner, demodulator, FEC, transport stream, PSI/SI | no corresponding implementation was found in the inspected scope (ABSENCE_VERIFIED, [EVID:SCOPE-001]) | `tools/verify.mjs` scans the artifact for DVB symbols and fails if any appear |
| carrier lock as a physical condition | a provider matching a content type is **not** a lock | provider code has no notion of physical validity |
| exhaustive spectrum coverage as a physical guarantee | no equivalent guarantee exists for the web | coverage is DESIGNED, not implemented |

Absence discipline: because the implementation is a single file that was read in
full and scanned mechanically, absence claims about it are marked
ABSENCE_VERIFIED rather than assumed from a partial search. Absence claims about
artifacts that were never present in the repository are recorded as NOT_FOUND.

Two claims must never be made:

1. that this project implements, emulates or interoperates with DVB;
2. that HTTP probing is technically equivalent to RF demodulation. The analogy
   maps *control structure*, not physics. A 200 response is not a carrier, and a
   provider match is not a lock.

## Where the analogy helps

* it explains why **recognition is separate from acquisition** — detection and
  decoding are distinct jobs in both domains;
* it explains why **metadata expands the search space** — the DVB service list is
  discovered from the stream, not from the scan plan;
* it explains why **observations are evidence, including negative ones** — an
  empty frequency is a datum, and a failed request is an observation;
* it motivates **binding work by budget** (spectrum sweeps are time-bounded).

## Where the analogy misleads

* **Termination.** A blind scan has a finite grid and can be complete. The web
  has no finite grid; "no eligible candidate" is not "nothing else exists".
* **Cost symmetry.** Every frequency step costs roughly the same; a URL can be
  free, slow, or destructive.
* **Authority.** A tuner owns the medium. A userscript shares a browser with the
  page it observes and is subject to CORS, grants and rate limits.
* **Determinism.** Demodulation is deterministic given parameters; responses
  change between runs.

These differences are why `docs/roadmap/future-architecture.md` treats coverage,
absence and completeness as explicit, separately designed objects rather than as
properties inherited from the analogy.

## Source

The analogy was developed in `archive/Userscript Discovery Prototype.md`
(41 numbered design notes: coarse-to-fine search, confidence instead of binary
decisions, retrying failed candidates, coverage as a metric, caching knowledge
between scans, avoiding unbounded candidate generation). Those notes are the
origin of many later design decisions; the transcript is archived unedited and is
**non-normative**.
