# Provenance

Status: **CURRENT (partial)**; DESIGNED extensions are labelled.

## The four questions

| Question | Answered by | Implemented |
| --- | --- | --- |
| Why was this target investigated? | `Candidate.parent`, `hints`, `mechanism`, `depth` | yes |
| What did acquisition actually observe? | `Observation` (+ ledger `request-*`, `observation` events) | yes |
| What interpretation was derived? | `Discovery` (`kind`, `data`, `confidence`, `mechanism`) | yes |
| Which observation/discovery caused this candidate to exist? | `Discovery.provenance` → graph edge `parent → child` | yes, partially |

The prototype keeps these four as separate records. It does **not** build an
evidence graph, does not model competing interpretations, and does not treat an
observation as proof.

## Recorded provenance

```
Discovery {
    candidateId          candidate that was acquired
    observationId        observation that was interpreted
    kind                 interpretation kind (url / api / resource / metadata / ...)
    confidence           0..1, provider-supplied
    mechanism            e.g. html-link, json-url, css-url, network-get, dom-observer-link
    data                 { url, ... }
    provenance {
        origin, parent, candidateTarget, candidateType, mechanism, depth, hints
    }
}
```

```
Observation.fingerprint    { algorithm: 'fnv1a32', hash, length, sampledLength }
                          whitespace-normalized sample, first 1,000,000 chars
Candidate.parent          id of the candidate whose discovery produced this one
Candidate.alternateParents / alternateOrigins / alternateTypes   merge history
KnowledgeBase.graphEdges  { from, to, relation }, capped at 5000
DecisionLedger.events     append-only, sequenced, capped at 5000
ResourceRecord            merges type, mechanism, status, candidateIds,
                          networkEventIds, fingerprint
```

The ledger is the closest thing to a causal trace: every intake, claim, plan,
denial, reservation, request, observation, discovery, retry and completion is
appended with an increasing `seq`.

## Walk-through

```
current page (root, depth 0)
    │  acquire → observation
    ▼
HTML provider → discovery(html-link, mechanism=html-link, confidence=0.7)
    │  emitDiscovery() → discover(url, type, { parent: candidateId, depth+1 })
    ▼
candidate (parent = root candidate id, hints.confidence = 0.7)
    │  graphEdges: parent → child
    ▼
JSON provider → discovery(json-url)
    │
    ▼
candidate (parent = second candidate id)
```

Answering "why does this URL exist?" means walking `parent` links or `graphEdges`
back to a root whose `mechanism` is `current-page`, `dom-observer-link`,
`network-get` or `performance-*`.

## Limits

| Limit | Consequence |
| --- | --- |
| Re-discovery returns the **existing** candidate and merges `alternate*` fields instead of creating a new record | the first discovery remains the `parent`; later origins are visible only in `alternateParents` / `alternateOrigins` |
| Expansion depth is derived from `discovery.provenance.depth + 1`, falling back to 1 | a discovery without provenance depth restarts the depth count at 1 |
| Observations are mutable in practice (stored in a `Map`, serialized on persistence) | "what was observed" is not immutable evidence; a later write could change it |
| Ledger and edge lists are capped (5000 / 5000) and truncated from the front | long scans lose the earliest causal history |
| No claim/evidence objects, no independent-evidence tracking, no conflict records | competing interpretations of one observation cannot be reconciled (DESIGNED: v0.16, v0.34) |
| `Discovery.confidence` is provider-specific | cross-provider comparison of confidences is meaningless |
| Content fingerprints are **indexed but never consulted** | `KnowledgeBase.fingerprintIndex` (hash → URLs) is written on observation and restore, but no code reads it, so identical bytes behind different URLs are never recognized as the same content (**D8**) |
| The ledger is persisted but is not a query interface | events can be read back in order; there is no lookup by candidate, target or time |

## DESIGNED

| Design | Version | Purpose |
| --- | --- | --- |
| `EvidenceGraph` + `Provenance` + `Claim` | v0.16 | separate observation, evidence, assertion; keep independence |
| Resource identity resolution and locator model | v0.17 | identity is relational, no destructive merges |
| Classification assertions with per-axis evidence | v0.18 | multiple assertions may coexist |
| Representation / artifact / revision identity | v0.19 | bytes observed at a time ≠ logical resource |
| Provenance-preserving conflict resolution | v0.34 | resolution must not erase origin |

See [../roadmap/future-architecture.md](../roadmap/future-architecture.md).
These are design documents; no code exists for them.
