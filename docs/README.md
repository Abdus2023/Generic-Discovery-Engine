# Generic Discovery Engine — Documentation

> **Status:** CURRENT
>
> **Source:** `Userscript Discovery Prototype.md`; `Continue Architecture Planning.md`
>
> **Purpose:** Index of the documentation tree produced by mechanically splitting the two original planning documents.

This documentation tree was produced by a **mechanical split** of two source documents:

- [`Userscript Discovery Prototype.md`](../archive/Userscript%20Discovery%20Prototype.md)
- [`Continue Architecture Planning.md`](../archive/Continue%20Architecture%20Planning.md)

The split moves, groups and cross-references existing material. It does not redesign the architecture, resolve contradictions, or add requirements. Contradictions and ambiguities found during the split are recorded in [Review Notes](REVIEW-NOTES.md) and left for a separate decision pass.

Both original documents are retained under [`archive/`](../archive/) for provenance.

## How to navigate

- Start with [Concept Overview](concepts/overview.md) for what the project is.
- [Prototype Overview](prototype/overview.md) covers the working browser userscript.
- [Architecture Overview](architecture/overview.md) and [System Model](architecture/system-model.md) cover the designed architecture.
- [Invariants](validation/invariants.md) collects every invariant in one place.
- [Future Work](roadmap/future-work.md) collects everything the sources mark as next boundary, still missing, or open.
- [Source Map](SOURCE-MAP.md) maps every extracted section to its destination.
- [Review Notes](REVIEW-NOTES.md) lists contradictions and defects found during the split.

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

- [Source Map](SOURCE-MAP.md)
- [Review Notes](REVIEW-NOTES.md)
- [Archived source documents](../archive/)

