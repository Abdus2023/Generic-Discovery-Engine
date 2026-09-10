# Generic Discovery Engine

A browser userscript that explores a web origin as an *unknown search space*:
it proposes candidates, acquires them, recognizes what came back, and uses the
result to propose more candidates.

The architecture is inspired by **DVB blind scanning** — a receiver searching an
unknown spectrum, locking onto carriers, reading metadata, and using that
metadata to discover further services. The inspiration is structural only.
**This project contains no DVB, RF, tuner, or demodulation code and is not
DVB-compatible.** See [docs/research/dvb-blind-scan-inspiration.md](docs/research/dvb-blind-scan-inspiration.md).

## What It Is

Blind discovery is a control loop over incomplete knowledge:

```
Candidate → Acquisition → Observation → Recognition → Discovery → Candidate Expansion → Scheduler ↺
```

A *candidate* is a hypothesis ("this is worth investigating"), not a fact. An
*observation* is what acquisition actually produced, including failures. A
*discovery* is an interpretation of an observation. Discoveries generate new
candidates, which is what makes the search space grow while it is being searched.

## Current Status

| Item | State |
| --- | --- |
| Working prototype | **Yes** — one userscript, `prototype/generic-discovery-engine.user.js` (v0.7.1) |
| Verified behaviour | claiming, acquisition, recognition, expansion, persistence, export (see [docs/prototype/userscript.md](docs/prototype/userscript.md)) |
| Known defects | 9 documented defects (D1–D9) in the prototype — see [docs/prototype/limitations.md](docs/prototype/limitations.md) |
| Architecture beyond v0.7.1 | **Design only** — v0.8 … v0.35 exist as prose, with no implementation |
| Verification | `tools/verify.mjs` (static), `tools/checks.mjs` (behavioural invariants), `tools/simulate.mjs` (headless harness) |

Nothing in this repository is a production crawler, and no version after
v0.7.1 exists as code.

## Current Prototype

`prototype/generic-discovery-engine.user.js` is a single Tampermonkey /
Greasemonkey userscript (v0.7.1, ~4.3k lines) that:

- seeds the frontier with the current page URL and with DOM links/scripts/frames
- observes page network activity (fetch/XHR bridge + PerformanceObserver)
- canonicalizes and deduplicates candidate URLs
- schedules candidates by weighted priority
- claims a candidate atomically *before* any `await`
- acquires candidates over HTTP with timeouts, per-origin limits and a global request budget
- recognizes responses with seven providers: HTML, JSON, XML, CSS, JavaScript, text, binary
- converts recognized URLs into new candidates (bounded by depth and candidate caps)
- records candidates, observations, discoveries, resources and an append-only decision ledger
- persists state through `GM_setValue`/`GM_getValue` (or `localStorage`) with size caps
- exports a JSON snapshot and shows a small on-page control panel

## Core Architecture

Three planes exist in the prototype. Only the first two are implemented as
interfaces; candidate sources are currently methods on the engine.

```
                     ┌─────────────────────┐
                     │  Discovery Engine   │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │      Scheduler      │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │      Candidate      │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │  Acquisition (HTTP) │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │     Observation     │
                     └──────────┬──────────┘
                                │
                     ┌──────────▼──────────┐
                     │  Provider Registry  │
                     └──────────┬──────────┘
                                │
          ┌──────────┬──────────┼──────────┬──────────┐
          ▼          ▼          ▼          ▼          ▼
        HTML       JSON       XML/CSS      JS        Text
          │          │          │          │          │
          └──────────┴──────────┼──────────┴──────────┘
                                ▼
                           Discovery
                                │
                        Candidate Expansion
                                │
                                └────────────► Scheduler
```

Responsibilities, boundaries and failure modes are specified in
[docs/architecture/](docs/architecture/discovery-model.md).

## Discovery Loop

```
initialize search space
while a candidate is claimable:
    candidate   ← scheduler.claim()          synchronous ownership transition
    plan        ← policy.plan(candidate)     may deny (non-GET, depth, type)
    observation ← acquisition.execute(plan)  network, non-deterministic
    discovery[] ← provider.recognize(...)    interpretation, deterministic
    enqueue candidates derived from discovery
    mark candidate completed / retried / failed
```

The loop is real but bounded: the prototype stops when no candidate is
*currently* eligible, when the request budget is exhausted, or when stopped
manually. Design-only material about coverage, completeness, and adaptive
strategy lives in [docs/roadmap/future-architecture.md](docs/roadmap/future-architecture.md).

## Candidate Lifecycle

```
discovered → queued → claimed → planned → acquiring → observed
                                                       │
                          recognized → expanded → completed
                          (otherwise)  skipped | failed → (retry) → queued
```

`claimed` is an ownership transition, not a claim about the resource. Full
state table and bounds: [docs/architecture/candidate-model.md](docs/architecture/candidate-model.md).

## Concurrency Invariant

> A candidate may have at most one active owner.

The claim operation is synchronous — it marks a candidate `claimed` before the
worker performs any `await` — so the browser event loop cannot interleave two
claims for the same candidate. This is *not* a distributed lock; it is safe only
because JavaScript runs to completion between awaits, and only within one
execution context.

**The end-to-end invariant does not hold in v0.7.1.** Re-discovering a URL that
is still in flight re-queues the existing candidate, so the same candidate can be
acquired twice. This is reproduced deterministically by `tools/simulate.mjs`.
Details: [docs/architecture/concurrency.md](docs/architecture/concurrency.md),
evidence and severity: [docs/prototype/limitations.md](docs/prototype/limitations.md).

## Provider Model

Providers interpret an observation; they do not perform I/O, schedule work, or
enqueue candidates.

| Provider | Recognizes | Emits candidate kinds |
| --- | --- | --- |
| `HtmlProvider` | HTML documents | links, frames, scripts, media, form actions, metadata URLs |
| `JsonProvider` | JSON bodies | URL-like string values |
| `XmlProvider` | XML bodies | `loc`/location values |
| `CssProvider` | CSS bodies | `url(...)` references |
| `JavaScriptProvider` | script bodies | string-literal URLs |
| `TextProvider` | `text/*` or an empty content type | HTTP(S) and relative URLs |
| `BinaryProvider` | binary content types | nothing (recognizes, emits no candidates) |

Several providers can match one observation (`text/html` matches both HTML and text), so one body may be interpreted twice by design. Contract: `matches(observation)` and `recognize(candidate, observation) → Discovery[]`.
Candidate expansion is performed by the engine from `Discovery.data.url`, which is
why providers stay replaceable. See [docs/architecture/provider-model.md](docs/architecture/provider-model.md).

## Provenance

Every candidate records why it exists (`parent`, `mechanism`, `depth`, `hints`),
every discovery records the candidate and observation it came from, and the
decision ledger keeps a sequenced trace of intake, planning, budget decisions,
requests, observations, recognition and completion. Content fingerprints are
computed but not yet used (**D8**). Details and limits:
[docs/architecture/provenance.md](docs/architecture/provenance.md).

## Scope

**Implemented** — URL candidate generation, deduplication, priority scheduling,
single-context candidate claiming, HTTP GET acquisition, timeouts, response
recognition (HTML/JSON/XML/CSS/JS/text/binary), candidate expansion, depth and
budget limits, provenance records, persistence, JSON export, control panel.

**Not implemented** — RF spectrum scanning, SDR or tuner control, DVB-S/S2,
DVB-T/T2 or DVB-C demodulation, carrier synchronization, symbol-rate estimation,
FEC decoding, MPEG transport-stream decoding, DVB PSI/SI parsing, NIT-based
discovery.

**Designed but not implemented** — capability-aware acquisition, work items and
frontier arbitration, evidence graph, resource identity resolution, coverage and
completeness claims, negative evidence, adaptive strategy learning, leases and
fencing, multi-context coordination, transactional persistence.

## Non-Goals

- a general-purpose web crawler clone, or an unrestricted Internet crawler
- a browser automation framework
- an RF/DVB scanner implemented in JavaScript
- a replacement for specialized DVB software
- a system that claims completeness of the open web

## Repository Structure

```
README.md                     ← you are here (concept, status, scope, index)
prototype/
  generic-discovery-engine.user.js   the only implementation artifact (v0.7.1)
docs/
  glossary.md                 canonical terminology
  architecture/               stable design: discovery model, candidates, scheduler,
                              providers, provenance, concurrency, search space
  prototype/                  artifact guide, strict scope, limitations + failure modes
  research/                   DVB blind-scan inspiration and analogy boundary
  roadmap/                    DESIGNED / CONJECTURE layers (v0.8 … v0.35)
  analysis/                   repository review: evidence register, claim records,
                              scope & authorization, change register
archive/
  Userscript Discovery Prototype.md   raw design conversation (non-normative)
  Continue Architecture Planning.md   raw design conversation (non-normative)
tools/
  verify.mjs                  static checks: artifact vs documentation, scope, governance
  validate-analysis.mjs       schema validation, rules V1–V20, invariants I-001–I-016
  render-claims.mjs           renders claims.md from analysis.json
  checks.mjs                  behaviour checks: dedup, providers, provenance, persistence
  simulate.mjs                headless harness that executes the shipped artifact
```

The two files in `archive/` are the unedited source conversations. They are
**historical evidence, not specifications**; everything normative lives in
`docs/` and `prototype/`.

## Verification

```bash
node tools/verify.mjs             # static: artifact vs documentation, scope, links, governance
node tools/validate-analysis.mjs  # schema: typed fields, enums, authorization/execution rules
node tools/checks.mjs             # behaviour: dedup, provider selection, provenance, persistence
node tools/simulate.mjs           # dynamic: runs the artifact under a browser shim
node tools/render-claims.mjs --check   # claims.md is generated from analysis.json
```

`tools/verify.mjs` exits non-zero when documentation and code disagree, when a
`[EVID:…]` citation does not resolve to the [evidence register](docs/analysis/evidence-register.md),
or when a register row points at a path that does not exist. Known prototype
defects are reported separately as `[DEFECT]` entries and do not fail the run.

Results and the audit trail:

| Document | Content |
| --- | --- |
| [repository-analysis-2026-09-10.md](docs/analysis/repository-analysis-2026-09-10.md) | full review (18 sections) |
| [evidence-register.md](docs/analysis/evidence-register.md) | the audit index: every `[EVID:…]` id with path and locator, `evidence_level` values, absence procedures, frozen artifact digest |
| [claims.md](docs/analysis/claims.md) | 41 claim records rendered from [analysis.json](docs/analysis/analysis.json): `claim_kind` · `implementation_state` · `test_state` · `evidence_level` · `verification_result` |
| [analysis.schema.json](docs/analysis/analysis.schema.json) | the normative machine-readable schema (JSON Schema draft 2020-12) the record is validated against |
| [scope-and-authorization.md](docs/analysis/scope-and-authorization.md) | scope boundary, six ownership roles, authorization contract, pre/post-execution checks |
| [change-register-2026-09-10.md](docs/analysis/change-register-2026-09-10.md) | executed changes R-001…R-017; code changes R-101…R-112 (PLAN ONLY) |

Status in this repository is never a single word. Five typed fields are reported
separately for every claim — `claim_kind`, `implementation_state`, `test_state`,
`evidence_level`, `verification_result`. Repository mutation is a separate algebra:
`authorization.state` (whether permission exists) is not `authorization.level`
(what it permits), and neither is `execution.result` (what actually happened) or
`post_verification.result` (what the independent re-run established). No field
answers two questions, and no field is substituted for another.
`tools/validate-analysis.mjs` enforces this — against
[docs/analysis/analysis.schema.json](docs/analysis/analysis.schema.json), plus the
semantic rules `V1`–`V20` and invariants `I-001`–`I-016`.

## Roadmap

| Stage | Content | Status |
| --- | --- | --- |
| v0.7.1 | acquisition planning, decision ledger, seven providers, persistence | implemented |
| v0.8 – v0.13 | capabilities, acquisition runtime, recognition runtime, candidate sources, discovery controller | design only |
| v0.14 – v0.19 | search domain, sessions, work items, evidence graph, resource identity, classification | design only |
| v0.20 – v0.27 | partitioning, strategy learning, coverage, absence, query planning, tactics, enumeration | design only |
| v0.28 – v0.35 | reconciliation, frontier arbitration, cost ledger, crash recovery, multi-context coordination | design only |

Do not read the roadmap as a description of the current system. Each stage is
labelled DESIGNED, CONJECTURE or OPEN in
[docs/roadmap/future-architecture.md](docs/roadmap/future-architecture.md).

## DVB Inspiration

Blind scanning supplies the control pattern — search unknown space, detect,
acquire, validate, read metadata, discover more — not the physical layer. The
analogy matrix and its limits are owned by
[docs/research/dvb-blind-scan-inspiration.md](docs/research/dvb-blind-scan-inspiration.md).

**DVB-inspired, not DVB-compatible.** No RF, tuner, demodulator, FEC,
transport-stream or PSI/SI implementation was found in the inspected repository
scope (ABSENCE_VERIFIED — the entire implementation is one 4,290-line file, read
in full and scanned mechanically; [EVID:SCOPE-001]). `tools/verify.mjs` fails if
such a symbol is ever introduced.
