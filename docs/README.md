# Generic Discovery Engine — Documentation

> **Status:** CURRENT
>
> **Source:** `Userscript Discovery Prototype.md`; `Continue Architecture Planning.md`
>
> **Purpose:** Index of the documentation tree produced by the deterministic mechanical split of the two original planning documents.

This tree was produced by a **mechanical split**. It answers *where the existing knowledge should live*; it does not answer *what the architecture should become*. Material was moved, grouped, given stable identifiers and cross-referenced. No architecture, algorithm, interface, requirement or example was added, removed, rewritten or resolved.

Both source documents are retained verbatim under [`archive/`](../archive/) and are marked as archived source documents.

## Reading order

1. [Concept Overview](concepts/overview.md) — what the project is.
2. [Prototype Overview](prototype/overview.md) — the working browser userscript.
3. [Architecture Overview](architecture/overview.md) and [System Model](architecture/system-model.md) — the designed architecture.
4. [Invariants](validation/invariants.md) — every invariant in one place.
5. [Future Work](roadmap/future-work.md) — everything the sources mark as a next boundary, still missing, or open.
6. [Source Map](SOURCE-MAP.md) — `USP-nnn` / `CAP-nnn` section identifiers and their destinations.
7. [Review Notes](REVIEW-NOTES.md) — contradictions, defects and unverified claims.

## Concepts

- [Concept Overview](concepts/overview.md)
- [Generic Discovery](concepts/generic-discovery.md)
- [The Discovery Loop](concepts/discovery-loop.md)

## Architecture

- [Architecture Overview](architecture/overview.md)
- [System Model](architecture/system-model.md)
- [Candidate Model](architecture/candidate-model.md)
- [Observation Model](architecture/observation-model.md)
- [Discovery Model](architecture/discovery-model.md)
- [Provenance](architecture/provenance.md)
- [Scheduling](architecture/scheduler.md)
- [Concurrency](architecture/concurrency.md)
- [Provider Architecture](architecture/provider-architecture.md)
- [Capability Model](architecture/capability-model.md)
- [Resource, Representation and Revision Model](architecture/resource-model.md)
- [Evidence Model](architecture/evidence-model.md)
- [Resource Type System and Classification](architecture/classification.md)
- [Search Space](architecture/search-space.md)
- [Strategies, Query Planning and Enumeration](architecture/strategy-and-planning.md)
- [Goal-Constrained Discovery and Query Planning](architecture/goal-and-query.md)
- [Coverage, Completeness and Absence](architecture/coverage-and-absence.md)
- [Domains, Sessions and Termination](architecture/sessions-and-domains.md)
- [Work Items and Frontier Arbitration](architecture/work-and-frontier.md)
- [Resource and Cost Ledger](architecture/resource-budget.md)
- [Persistence and Crash Recovery](architecture/persistence-and-recovery.md)
- [Coordination, Consistency and Transport](architecture/coordination.md)

## Acquisition

- [Acquisition Overview](acquisition/overview.md)
- [Acquisition Model](acquisition/acquisition-model.md)
- [Response Recognition](acquisition/response-recognition.md)
- [Acquisition Runtime](acquisition/runtime.md)

## Providers

- [Providers Overview](providers/overview.md)
- [HTML Provider](providers/html.md)
- [JSON Provider](providers/json.md)
- [Text Provider](providers/text.md)
- [Candidate Sources](providers/candidate-sources.md)

## Prototype

- [Prototype Overview](prototype/overview.md)
- [Userscript Development Narrative](prototype/userscript.md)
- [Configuration](prototype/configuration.md)
- [Prototype Scope and Limitations](prototype/limitations.md)
- [Prototype Version Artifacts](prototype/versions/README.md)

## Research

- [DVB Blind Scan](research/dvb-blind-scan.md)

## Validation

- [Invariants](validation/invariants.md)
- [Verification](validation/verification.md)
- [Failure Taxonomy](validation/failure-taxonomy.md)

## Roadmap

- [Future Work](roadmap/future-work.md)

## Traceability

- [Source Map](SOURCE-MAP.md) — 1,244 identified sections with destination, action, status and anchors
- [Split Manifest](SPLIT-MANIFEST.yaml) — machine-readable source of truth: one record per section with heading path and content hash, the allocation list, and the conceptual diff
- [Review Notes](REVIEW-NOTES.md) — contradictions `C-01`…`C-11`, defects `D-01`…`D-05`
- [Archived source documents](../archive/)

