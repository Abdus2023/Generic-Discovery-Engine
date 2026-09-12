# Essential vs Accidental Architecture

> **Input status: INPUT_CONTRACT_FAILED.** Protocol-v1 source integrity fails and required Protocol-v4 through Protocol-v7 artifacts are missing. This is a structurally validated, downgraded source-local corpus—not an accepted complete v10.1 synthesis. Missing evidence is not evidence of absence.

| Element | Semantic effect | Rule |
|---|---|---|
| Candidate | Changes behavior | PRESERVE_SEMANTICS_ONLY |
| Observation | Changes behavior | PRESERVE_SEMANTICS_ONLY |
| Provider role | Changes behavior | PRESERVE_SEMANTICS_ONLY |
| Scheduler lifecycle | Changes behavior | PRESERVE_SEMANTICS_ONLY |
| Knowledge accumulation | Changes behavior | PRESERVE_SEMANTICS_ONLY |
| Provenance associations | Changes behavior | PRESERVE_SEMANTICS_ONLY |
| Persistence/export representation | Representation or conditional compatibility | REMOVE_WITH_MIGRATION |
| UI presentation | Representation or conditional compatibility | OPTIONAL |
| Map/Set/function/module layout | Representation or conditional compatibility | HISTORICAL_ONLY |

## Allowed refactoring
worker loop → actor; class → trait; function → service; in-memory queue → persistent queue, only with equivalent contracts.

## Forbidden refactoring
failure → silent skip; provenance → discard; Observation → raw body only; provider failure → scheduler failure; bounded pool → unbounded spawning.
