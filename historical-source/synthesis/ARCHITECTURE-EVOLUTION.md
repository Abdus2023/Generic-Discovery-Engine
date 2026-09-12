# Architecture Evolution

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

## Historical architecture (recovered snapshots)

The diagrams below are source-local structural interpretations, not source code and not proof of runtime behavior.

### v0.1.0

```text
Seed/DOM
  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine
  -> Web acquisition -> Observation -> Recognizer/Provider set
  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state
```

Occurrences: `snapshot-0001` (mechanically-composed; LIKELY_EXECUTABLE). Providers/recognizers: mechanically-composed: HtmlRecognizer.

| Branch occurrence | Variant | Recovered model nodes | Provider count | Policy/ledger | Failure rows | Bound rows |
|---|---|---|---|---|---|---|
| snapshot-0001 | mechanically-composed | Candidate, Observation, Discovery, KnowledgeBase, Scheduler | 1 | not scanned | 9 | 4 |

### v0.2.0

```text
Seed/DOM
  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine
  -> Web acquisition -> Observation -> Recognizer/Provider set
  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state
```

Occurrences: `snapshot-0003` (mechanically-composed; LIKELY_EXECUTABLE). Providers/recognizers: mechanically-composed: HtmlProvider, JsonProvider, ResponseProvider, TextProvider.

| Branch occurrence | Variant | Recovered model nodes | Provider count | Policy/ledger | Failure rows | Bound rows |
|---|---|---|---|---|---|---|
| snapshot-0003 | mechanically-composed | Candidate, Observation, Discovery, KnowledgeBase, Scheduler | 4 | not scanned | 11 | 4 |

### v0.3.0

```text
Seed/DOM
  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine
  -> Web acquisition -> Observation -> Recognizer/Provider set
  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state
```

Occurrences: `snapshot-0005` (only-evidenced-complete-occurrence; LIKELY_EXECUTABLE). Providers/recognizers: only-evidenced-complete-occurrence: HtmlProvider, JsonProvider, ResponseProvider, TextProvider.

| Branch occurrence | Variant | Recovered model nodes | Provider count | Policy/ledger | Failure rows | Bound rows |
|---|---|---|---|---|---|---|
| snapshot-0005 | only-evidenced-complete-occurrence | Candidate, Observation, Discovery, KnowledgeBase, Scheduler | 4 | not scanned | 12 | 6 |

### v0.4.0

```text
Seed/DOM
  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine
  -> Web acquisition -> Observation -> Recognizer/Provider set
  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state
```

Occurrences: `snapshot-0006` (variant-a; LIKELY_EXECUTABLE), `snapshot-0008` (variant-b; LIKELY_EXECUTABLE). Providers/recognizers: variant-a: HtmlProvider, JsonProvider, ManifestProvider, ResponseProvider, TextProvider, XmlProvider; variant-b: CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider.

| Branch occurrence | Variant | Recovered model nodes | Provider count | Policy/ledger | Failure rows | Bound rows |
|---|---|---|---|---|---|---|
| snapshot-0006 | variant-a | Candidate, Observation, Discovery, KnowledgeBase, Scheduler | 6 | not scanned | 18 | 7 |
| snapshot-0008 | variant-b | Candidate, Observation, Discovery, KnowledgeBase, Scheduler | 8 | not scanned | 22 | 9 |

### v0.5.0

```text
Seed/DOM
  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine
  -> Web acquisition -> Observation -> Recognizer/Provider set
  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state
```

Occurrences: `snapshot-0007` (variant-a; LIKELY_EXECUTABLE), `snapshot-0009` (variant-b; NON_EXECUTABLE), `snapshot-0011` (variant-c; LIKELY_EXECUTABLE). Providers/recognizers: variant-a: ApiDescriptionProvider, HtmlProvider, JsonProvider, ManifestProvider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider; variant-b: CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, RobotsProvider, TextProvider, XmlProvider; variant-c: BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider.

| Branch occurrence | Variant | Recovered model nodes | Provider count | Policy/ledger | Failure rows | Bound rows |
|---|---|---|---|---|---|---|
| snapshot-0007 | variant-a | Candidate, Observation, Discovery, KnowledgeBase, Scheduler | 8 | not scanned | 28 | 11 |
| snapshot-0009 | variant-b | Candidate, Observation, Discovery, KnowledgeBase, Provider | 8 | not scanned | 19 | 10 |
| snapshot-0011 | variant-c | Candidate, Observation, Discovery, KnowledgeBase, Provider, Scheduler | 10 | not scanned | 23 | 14 |

### v0.6.0

```text
Seed/DOM
  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine
  -> Web acquisition -> Observation -> Recognizer/Provider set
  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state
```

Occurrences: `snapshot-0010` (variant-a; LIKELY_EXECUTABLE), `snapshot-0012` (variant-b; LIKELY_EXECUTABLE), `snapshot-0013` (variant-c; LIKELY_EXECUTABLE). Providers/recognizers: variant-a: BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, RobotsProvider, TextProvider, XmlProvider; variant-b: BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider; variant-c: BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider.

| Branch occurrence | Variant | Recovered model nodes | Provider count | Policy/ledger | Failure rows | Bound rows |
|---|---|---|---|---|---|---|
| snapshot-0010 | variant-a | Candidate, Observation, Discovery, KnowledgeBase, Provider | 9 | not scanned | 15 | 13 |
| snapshot-0012 | variant-b | Candidate, Observation, Discovery, KnowledgeBase, Provider, Scheduler | 10 | present | 24 | 16 |
| snapshot-0013 | variant-c | Candidate, Observation, Discovery, KnowledgeBase, Provider | 10 | present | 14 | 17 |

### v0.7.1

```text
Seed/DOM
  -> Candidate identity -> Scheduler/Knowledge state -> Worker/Engine
  -> Web acquisition -> Observation -> Recognizer/Provider set
  -> Discovery/provenance -> Candidate expansion -> Scheduler/Knowledge state
```

Occurrences: `snapshot-0014` (only-evidenced-complete-occurrence; LIKELY_EXECUTABLE). Providers/recognizers: only-evidenced-complete-occurrence: BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, TextProvider, XmlProvider.

| Branch occurrence | Variant | Recovered model nodes | Provider count | Policy/ledger | Failure rows | Bound rows |
|---|---|---|---|---|---|---|
| snapshot-0014 | only-evidenced-complete-occurrence | Candidate, Observation, Discovery, KnowledgeBase, Provider | 8 | present | 16 | 17 |

## Retrospective phase model

| Epoch | Range | Interpretive label | Evidence-bounded meaning |
|---|---|---|---|
| E1 | v0.1.0 | Candidate-centric closed recognition loop | The earliest recovered occurrence already contains Candidate, Observation, acquisition, recognition, Discovery, expansion, scheduling, and knowledge state. |
| E2 | v0.2.0-v0.3.0 | Providerized claimed pipeline | Multiple response providers and an explicit claim operation appear; retry/cancellation state becomes more explicit. |
| E3 | v0.4.0-v0.6.0 | Branching reliability, provenance, and observability experiments | Parallel alternatives add provider kinds, error-containment forms, origin/budget structures, and richer diagnostics without proving one linear lineage. |
| E4 | v0.7.1 | Policy/plan/ledger recomposition | Acquisition policy, plans, decisions, and ledger structures become explicit while provider interaction changes. |

These epoch boundaries are `INFERRED` analytical groupings. They do not assert source lineage. The prompt's hypothetical URL-only and structured-observation precursor phases are not recovered: v0.1.0 already has Candidate and Observation structures.

## Current architecture

Current planning adds protocol-independent acquisition, stronger contracts, capability policy, integrity, and security boundaries. Those are current targets, not backward evidence for v0.1-v0.7.1. See `CONTRACT-SECURITY-INTEGRATION.md`.
