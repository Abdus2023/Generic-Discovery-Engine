# Future Architecture (DESIGNED — no implementation)

Claim state: `PLANNED` (or `HYPOTHESIS` where marked). Evidence state: `INDIRECT`
(design prose in the archive). Verification state: `VERIFIED` **as planned** —
the fact that these layers are designed and unimplemented is verified; their
existence is not implied.

Everything in this document is **design prose**. None of it exists in code.
The prototype is v0.7.1; the design series runs from v0.8 to v0.35 and lives in
`archive/Continue Architecture Planning.md` (non-normative transcript).

Legend:

| Label | Meaning |
| --- | --- |
| DESIGNED | a boundary, contract or object has been specified in prose |
| CONJECTURE | plausible direction, not specified |
| OPEN | a question that requires implementation or research to answer |

## Progression

| Version | Boundary introduced | Core idea | Label |
| --- | --- | --- | --- |
| v0.8 | Capability-aware acquisition runtime | capability lattice, candidate requirements, four-level authorization, three graphs (discovery/acquisition/evidence) | DESIGNED |
| v0.9 | Acquisition provider architecture | providers perform I/O under a runtime: provider selection, capability contracts, provider failure ≠ denial | DESIGNED |
| v0.10 | Acquisition runtime | admission control, budget reservation before execution, cancellation, runtime-owned timeout and retry, plan ≠ attempt | DESIGNED |
| v0.11 | Response recognition runtime | recognition providers answer "what did I obtain?", response router, provider priority, recognition evidence and failure taxonomy, providers must not enqueue candidates | DESIGNED |
| v0.12 | Candidate source architecture | a source *proposes* resources and never acquires them; three independent provider planes | DESIGNED |
| v0.13 | Discovery controller | orchestration so that sources do not become independent mini-crawlers | DESIGNED |
| v0.14 | `DiscoveryDomain` + `ScanSession` | explicit search space, seeds ≠ candidates, termination evaluator, session snapshots, lease-based claims | DESIGNED |
| v0.15 | `WorkItem` + frontier runtime | work as a first-class object with lifecycle, leases, priority aging, dependencies, generic retry | DESIGNED |
| v0.16 | `EvidenceGraph` + provenance | observation ≠ evidence ≠ assertion; evidence strength, independence, immutability, conflict | DESIGNED |
| v0.17 | `ResourceGraph` + identity resolution | locator vs resource, redirect chains, fingerprints, no destructive merges | DESIGNED |
| v0.18 | Resource type system | four orthogonal type axes, classification assertions with per-axis evidence, recognition ≠ classification | DESIGNED |
| v0.19 | Representation / artifact / revision | logical resource ≠ bytes observed at a time; identity chain | DESIGNED |
| v0.20 | Partitions + discovery strategies | search-space partitioning, strategy as an object, probe cost | DESIGNED |
| v0.21 | Adaptive strategy learning | learn which partitions/strategies yield discoveries | DESIGNED |
| v0.22 | Coverage claims | what part of the search space was explored; completeness is claimed, never assumed | DESIGNED |
| v0.23 | Negative evidence / absence reasoning | absence assertions backed by coverage, not by failure | DESIGNED |
| v0.24 | Goal-constrained discovery | relevance with respect to a goal | DESIGNED |
| v0.25 | Discovery query planner | goals → query plans → tactics | DESIGNED |
| v0.26 | Search tactic runtime | tactic as a bounded unit of work | DESIGNED |
| v0.27 | Enumeration runtime | systematic enumeration as a distinct work kind | DESIGNED |
| v0.28 | Search-space reconciliation | one resource reachable by many paths; frontier dedup | DESIGNED |
| v0.29 | Dynamic search-space expansion | regions discovered after the scan started | DESIGNED |
| v0.30 | Unified frontier arbitration | one arbiter across discovery, acquisition and enumeration work | DESIGNED |
| v0.31 | Unified resource & cost ledger | reservation → allocation → consumption → actual cost | DESIGNED |
| v0.32 | Transactional persistence & crash recovery | durable frontier, checkpoints, recovery after a crash | DESIGNED |
| v0.33 | Multi-worker coordination | worker identity, claim tokens, leases, heartbeats, fencing epochs, duplicate-execution semantics | DESIGNED |
| v0.34 | Distributed consistency | optimistic concurrency, versions, conflict records, deterministic resolution, provenance-preserving merges | DESIGNED |
| v0.35 | Cross-context event transport | replication of events/state between execution contexts | CONJECTURE |

Earlier prototypes v0.3.0 – v0.6.0 exist as code only inside the archived
transcript; they are superseded by v0.7.1 and are not maintained.

## The separation the series converged on

| Layer | Question | Implemented today |
| --- | --- | --- |
| Goal | What am I looking for? | no |
| Domain | Where am I allowed to search? | partially (`sameOriginOnly`) |
| Search space | How is the universe partitioned? | no (implicit) |
| Query plan / tactic / strategy | How should a region be explored? | no |
| Candidate | What might exist? | yes |
| Acquisition | Can I obtain it? | yes (HTTP GET) |
| Observation | What did I actually observe? | yes |
| Recognition | What is the observation? | yes (content providers) |
| Evidence | Why do I believe that interpretation? | no |
| Resource / artifact / revision | What logical entity, which bytes, which version? | URL-level only |
| Classification | What kind of resource is it? | type labels only |
| Relevance | Does it satisfy the goal? | no |
| Coverage / absence / completeness | What was explored, what is legitimately absent, what may be claimed? | no |
| Frontier | What remains to be done? | implicit in candidate status |
| Coordination / consistency | Which worker owns it; how do concurrent updates converge? | single-context claim only |

## Prototype boundary stated by the design series itself

The series states its own limits; keep these when reading it:

* deterministic **replay** of decisions is separable from **acquisition** against
  a changing world — an acquisition log is not a deterministic execution trace;
* a browser profile can offer shared storage, claim records and leases across
  tabs, but that is **profile coordination**, not distributed consensus;
* a userscript cannot prove completeness of the open web; it can only report
  enumerated partitions, exhausted cursors, acquired artifacts, digests,
  evidence-backed classifications, inaccessible regions, attempted strategies and
  consumed budgets.

## Open questions (OPEN)

| Question | Why it matters |
| --- | --- |
| What is the terminating condition of a scan? | without it, "finished" and "idle" are indistinguishable |
| What should deduplicate: candidate identity, resource identity, or observed artifact? | three different identities exist in the design series, one in the code |
| How is a confidence produced and compared across providers? | today confidences are provider-local constants |
| When is a negative observation evidence of absence? | requires coverage accounting first |
| How should the frontier survive a crash without overclaiming durability? | v0.32 assumes transactional storage that browsers do not offer uniformly |
| How much coordination is safe inside one browser profile? | v0.33/v0.34 assume atomic storage operations that are not guaranteed |

## Migration constraints (if this is ever implemented)

1. Do not replace the working prototype to introduce a designed layer; layer it.
2. Preserve the provider purity rules — they are the part of the design that the
   current code already satisfies.
3. Fix the ownership invariant (D1) and terminal-failure semantics (D3) before
   adding leases or coordination, otherwise the design inherits an unsound
   baseline.
4. Keep the DVB analogy at the level of control structure: no physical-layer
   claims, no coverage claims inherited by metaphor.
