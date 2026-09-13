# Deep Verification — v1.5 Second-Pass Audit (B1→B3)

> Linked artifact: `dist/generic-discovery-engine.user.js` v1.5.0 `6453 lines` `204882B` `sha 508e3e…` (built from `src/` 7 modules)

## Summary

Yes — this link is important because it points to the actual generated distribution artifact, not merely the source tree.

I checked the branch and the `dist/generic-discovery-engine.user.js` artifact. The artifact is now v1.5.0, and its own embedded changelog explicitly describes the hardening work that followed the v1.4 audit.

### What changed since the previous audit

| Previous finding | v1.5 status |
|---|---|
| Production coverage measured incorrectly | Fixed in design |
| tsc pipeline could mask failure | Fixed |
| ESLint wasn't actually invoked | Fixed |
| Discovery/resource maps unbounded | Addressed with FIFO limits |
| Bodies could accumulate in memory | Addressed with maxBodiesInMemory |
| networkEvents cap bypass | Fixed |
| Redirect could cross origin | Fixed with `redirect: "error"` |
| @connect * excessive | Fixed; wildcard commented |
| Dead health branch | Fixed |
| Provider metrics ambiguous | Fixed |
| Adaptive concurrency terminology misleading | Clarified as target, not active worker resizing |

These are not merely documentation claims: the distributed artifact itself contains the v1.5 patch notes, so the published userscript and the stated fixes are at least synchronized at the artifact level.

There is also a meaningful change in the source architecture. KnowledgeBase still explicitly separates candidates, observations, discoveries, resources, graph edges, network events, fingerprints, patterns, clusters and diagnostics rather than collapsing everything into one state structure.

### One thing I would not conclude yet

I would not yet call v1.5 independently verified simply because the artifact says the fixes are present.

The artifact says:

> “Verification Hardening + Runtime Bounds”

but that is an implementation assertion.

The next verification step should be artifact ↔ source ↔ build-system consistency, specifically:

```
src/
  ↓
deterministic build
  ↓
dist/generic-discovery-engine.user.js
  ↓
hash / line count / metadata
  ↓
runtime execution
  ↓
invariant tests
```

The critical question is now:

> Did v1.5 actually implement the claimed bounds and security changes correctly, or did it merely update the generated artifact/changelog?

That is a stronger question than the v1.4 audit.

I would therefore treat this linked file as the v1.5 verification target and perform a second-pass audit against the source and build machinery, with special attention to:

1. FIFO eviction correctness — whether eviction also cleans every secondary index.
2. Body accounting — whether maxBodiesInMemory=150 actually bounds retained body bytes, not merely object count.
3. Discovery/resource eviction — whether graph edges, fingerprints, patterns and clusters can still grow after node eviction.
4. Candidate historical retention — whether completed candidates and candidateKeys still accumulate.
5. Redirect enforcement — whether every acquisition path, including GM_xmlhttpRequest, has equivalent origin/redirect semantics.
6. Coverage integrity — whether c8 now instruments production src/, rather than merely declaring that it does.
7. Build identity — whether the linked dist is reproducibly generated from the current src.
8. Runtime stress — whether the bounds survive a long-running, highly connected SPA rather than only synthetic unit tests.

So my updated position is:

- v1.4: architecture strong, verification incomplete.
- v1.5: the project appears to have directly attacked the audit findings; now the interesting problem is proving that the fixes are semantically complete, not merely present.

The linked artifact is therefore the right object for the next audit.

---

## v1.5 Deep Verification: The Runtime-Bound Claim Is Still Incomplete

The important distinction is now:

```
v1.5
                   │
        ┌──────────┴──────────┐
        │                     │
   bounded containers     unbounded contents
        │                     │
 discoveries ≤ 2000       ResourceRecord arrays
 resources ≤ 2000         fingerprintIndex Sets
 observations ≤ 800       visited Set
 graphEdges ≤ 5000       candidateKeys / candidates
 networkEvents ≤ 1000     patternIndex / clusterIndex
 diagnostics ≤ 500
```

So v1.5 does improve retention substantially, but it has not yet established a true global runtime-memory bound.

### 1. The biggest remaining bug: ResourceRecord is internally unbounded

`ensureResource()` now evicts old resource records when the resource map reaches 2,000 entries.

But each ResourceRecord contains:

- parents
- candidateIds
- observationIds
- discoveryIds
- networkEventIds
- types
- mechanisms

and `merge()` continually expands those arrays using:

```js
this[field] = unique([
    ...this[field],
    ...data[field]
]);
```

There is no per-resource bound.

Therefore:

```
2000 resources
   ×
unbounded relationship arrays
   =
still-unbounded retained graph metadata
```

This is the most important remaining runtime issue.

The resource-map cap bounds the number of resource objects, not the size of the resource graph.

### 2. Observation-body bound is not actually implemented

This is particularly interesting.

The configuration says:

```js
runtimeBudget.maxBodiesInMemory = 150
```

and the v1.5 changelog claims:

> “maxBodiesInMemory 150”

But `recordObservation()` still only bounds the number of observations:

```js
maxObservationsInMemory = 800
```

It deletes the oldest observation object when that map reaches the limit.

And Observation itself retains:

```js
this.body = data.body || '';
```

with a per-response truncation of:

```js
maxBodyChars = 2_000_000
```

So the theoretical retained body payload can still approach:

```
800 × 2,000,000 characters
≈ 1.6 billion JS characters
```

before considering object overhead, strings, provider parsing, temporary copies, etc.

The actual average may be much smaller, but the stated `maxBodiesInMemory: 150` is not the mechanism enforcing that bound.

This is a concrete v1.5 verification failure.

### 3. Evicting observations does not remove their references elsewhere

This follows directly from the previous two findings.

When an observation is evicted:

```js
observations.delete(firstKey)
```

but its ID can remain inside:

```js
ResourceRecord.observationIds
```

and its fingerprint URL can remain inside:

```js
fingerprintIndex
```

The resource relationship arrays are never garbage-collected by the knowledge model.

Thus:

```
Observation
    │
    ├── observations Map ──[EVicted]
    │
    └── ResourceRecord ── observationIds ──[RETAINED]
```

This is a classic retention-reference problem.

The object itself may disappear, while its identity and associated metadata remain indefinitely.

### 4. visited is still unbounded

`markCompleted()` does:

```js
this.visited.add(candidate.identityKey());
```

and `markSkipped()` does the same.

There is no `maxVisited`.

That means a sufficiently long-lived engine can accumulate:

```
visited:
  url:A
  url:B
  url:C
  ...
  url:N
```

indefinitely.

This is actually important to the GDE architecture because `visited` is not merely telemetry. It is part of the search state.

Therefore you cannot simply discard it without changing semantics.

You need a deliberate policy such as:

```
VisitedRetentionPolicy
├── session
├── bounded
├── persistent
└── probabilistic
```

or a compact identity structure.

### 5. candidateKeys has a similar lifetime problem

A completed candidate remains in:

- candidates
- candidateKeys
- visited

There is no candidate-history eviction.

The v1.5 change improved the live candidate cap:

```js
liveCount =
  candidates excluding completed/skipped
```

but that is different from bounding the candidate database itself.

So the semantics are:

```
maxCandidates = maximum active frontier
```

not:

```
maxCandidates = maximum candidate state retained
```

That's a valid design, but it needs to be named honestly.

### 6. Inference indexes remain historical accumulators

`recordPattern()` increments:

- patternIndex
- clusterIndex

but nothing removes entries when candidates/resources disappear.

Likewise:

```js
fingerprintIndex
```

accumulates URL sets by fingerprint.

So the actual state topology is:

```
             Candidate
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
    candidateKeys visited patternIndex
                           │
                           ▼
                       clusterIndex

             Observation
                 │
        ┌────────┴────────┐
        ▼                 ▼
     Resource       fingerprintIndex
        │
        ├── observationIds
        ├── candidateIds
        ├── discoveryIds
        └── networkEventIds
```

Only some of these nodes/edges have retention limits.

That means the system is currently partially bounded, not globally bounded.

### 7. The acquisition security improvement is real

There is nevertheless a significant v1.5 success.

The Fetch fallback now uses:

```js
redirect:
    CONFIG.sameOriginOnly ? 'error' : 'follow'
```

instead of unconditional `follow`.

That is the correct direction for a hard same-origin boundary.

The important security property becomes:

```
candidate
   │
   ▼
isAllowedUrl()
   │
   ▼
AcquisitionPolicy
   │
   ▼
fetch()
   │
   └── redirect:error
```

rather than:

```
same-origin candidate
       │
       ▼
fetch
       │
       ▼
arbitrary redirect
       │
       ▼
different origin
```

So I would upgrade the previous assessment of the Fetch path from PARTIAL → substantially hardened.

However, the `GM_xmlhttpRequest` path still needs an explicit redirect-boundary test. Its code records `response.finalUrl`, but the request invocation itself does not show an explicit redirect rejection policy.

That should be tested independently.

### 8. The architecture is now revealing its real abstraction

This audit exposes something deeper.

GDE doesn't actually have one budget.

It has at least four different resource classes:

```
GDE Resource Governance

                       ┌─────────────┐
                       │   POLICY    │
                       └──────┬──────┘
                              │
        ┌─────────────────────┼──────────────────────┐
        ▼                     ▼                      ▼
   Search Budget         Execution Budget       Retention Budget
        │                     │                      │
 maxCandidates            maxRequests         observations
 maxDepth                 concurrency          resources
 candidate TTL            per-origin           discoveries
 retry                     timeout              bodies
                                                   indexes
                                                   graph metadata
                                                        │
                                                        ▼
                                               Persistence Budget
                                                        │
                                                persistedResources
                                                persistedDiscoveries
                                                persistedEdges
```

The project already distinguishes search budget from persistence budget.

v1.5 partially introduces runtime retention budget.

The missing piece is making retention compositional.

### 9. The next architectural fix should not be “add more caps”

I would avoid adding random:

```
maxX
maxY
maxZ
```

configuration fields.

Instead introduce an explicit:

```
RetentionPolicy
```

with ownership semantics.

For example:

```
RetentionPolicy
├── observations
│   ├── maxEntries
│   └── maxBodyBytes
│
├── discoveries
│   └── maxEntries
│
├── resources
│   ├── maxEntries
│   └── maxRelationsPerResource
│
├── candidates
│   └── maxHistoricalEntries
│
├── visited
│   └── maxEntries
│
├── fingerprints
│   ├── maxHashes
│   └── maxUrlsPerHash
│
├── inference
│   ├── maxPatterns
│   └── maxClusters
│
└── diagnostics
    └── maxEntries
```

Then every collection gets one invariant:

> No retention structure may grow beyond its declared bound.

That becomes testable.

### 10. The stronger invariant

The project originally had invariants such as:

```
requestsReserved <= maxRequests
liveCandidates <= maxCandidates
graphEdges <= maxGraphEdges
observations <= maxObservations
```

v1.5 should evolve that into:

```
∀ state collection C:
    size(C) ≤ bound(C)
```

and, crucially:

```
∀ relation R:
    cardinality(R) ≤ bound(R)
```

and for payloads:

```
retainedBodyBytes ≤ maxBodyBytes
```

That is much stronger than counting objects.

### Current v1.5 Verdict

| Area | Verdict |
|---|---|
| Search frontier | PASS |
| Candidate ownership | PASS |
| Acquisition policy | PASS |
| Fetch redirect boundary | PASS / hardened |
| GM-XHR redirect boundary | OPEN |
| Observation count | PASS |
| Discovery count | PASS |
| Resource count | PASS |
| Resource relationship size | FAIL |
| Body retention bound | FAIL |
| Visited retention | FAIL |
| Candidate history | FAIL |
| Fingerprint retention | FAIL |
| Pattern/cluster retention | FAIL |
| Graph-edge count | PASS |
| Diagnostic count | PASS |
| Global runtime-memory bound | FAIL |

The key conclusion: **v1.5 fixed the containers, but not the state topology.**

That's the distinction I would carry into the next revision.

The engine is becoming something more interesting than a userscript: a bounded discovery state machine. But to make that claim rigorous, every persistent relationship and every historical index needs an explicit retention contract.

And there is one especially concrete correction to make immediately:

> `runtimeBudget.maxBodiesInMemory: 150` is currently configuration without corresponding enforcement.

That should be the first v1.5.x fix, followed by bounded relationship arrays and bounded indexes.

---

## Next Layer: v1.5 Has a Retention Model, But Eviction Is Not Referentially Coherent

The core problem is not simply that some maps are unbounded.

It is that GDE has evolved into a multi-index knowledge graph, while eviction is currently implemented as local FIFO deletion.

That distinction matters.

### 1. The knowledge base is a graph, not a collection of independent caches

The current KnowledgeBase maintains:

- candidates
- candidateKeys
- observations
- discoveries
- resources
- visited
- claimed
- graphEdges
- networkEvents
- fingerprintIndex
- patternIndex
- clusterIndex
- diagnostics

These structures reference one another.

For example:

```
Candidate
   │
   ├───────────────┐
   ▼               ▼
Observation      Discovery
   │               │
   └──────┬────────┘
          ▼
      Resource
          │
          ├── candidateIds
          ├── observationIds
          ├── discoveryIds
          └── networkEventIds
```

But the v1.5 eviction operations mostly look like:

```js
oldest = map.keys().next()
map.delete(oldest)
```

That is sufficient for a cache.

It is not sufficient for a graph.

### 2. Example: discovery eviction creates dangling references

Suppose:

```
Discovery D17
      │
      ▼
Resource R42
      │
      └── discoveryIds = [D17]
```

When the discovery limit is reached, v1.5 deletes D17:

```js
discoveries.delete(D17)
```

but the resource still contains:

```js
R42.discoveryIds = [D17]
```

because `ResourceRecord.merge()` only adds and deduplicates relationship IDs. It does not perform reverse-reference cleanup.

Now the state is:

```
R42 ──discoveryIds──> D17
                         X
                    no longer exists
```

That's a dangling reference.

It may not immediately crash anything, but it destroys an important property:

> Every persisted relationship should resolve to a retained object, or explicitly be classified as historical evidence.

GDE currently has neither guarantee.

### 3. Observation eviction has the same problem

The code evicts observations when:

```js
observations.size >= maxObservationsInMemory
```

But the observation ID is also inserted into the corresponding resource:

```js
resource.merge({
    observationIds: [observation.id]
});
```

So:

```
observations
    └── O123  ← deleted

resources
    └── Rabc
         └── observationIds
              └── O123  ← retained
```

Again, dangling.

### 4. This exposes a fundamental distinction: hot state vs evidence

I think this is the correct architectural direction for the project:

```
GDE STATE

        ┌──────────────────────────┐
        │       HOT STATE          │
        │ bounded / mutable / fast │
        └────────────┬─────────────┘
                     │
              promotion / eviction
                     │
                     ▼
        ┌──────────────────────────┐
        │      COLD EVIDENCE       │
        │ historical / persistent  │
        └──────────────────────────┘
```

Right now GDE is trying to use one structure for both.

That creates the conflict:

```
Need bounded RAM
        vs
Need complete provenance
```

You cannot satisfy both by merely deleting old objects.

### 5. Better solution: immutable evidence IDs

The graph should distinguish:

Live references

```js
ObservationRef {
    id,
    retained: true
}
```

from historical evidence:

```js
EvidenceRef {
    id,
    retained: false,
    persisted: true
}
```

Or even simpler:

```js
ResourceRecord
    observationIds[]
```

should become conceptually:

```js
ResourceRecord
    liveObservationIds[]
    historicalObservationIds[]
```

Then eviction means:

```
LIVE
 │
 │ retention pressure
 ▼
COLD
 │
 │ persistence policy
 ▼
ARCHIVED
```

rather than:

```
LIVE
 │
 ▼
DELETE
```

This is much more compatible with GDE's provenance objective.

### 6. The same problem exists with candidates

`candidateKeys` maps:

```
type:target → candidateId
```

while `candidates` stores the actual candidate.

If candidates are eventually evicted without updating `candidateKeys`, the lookup becomes:

```
candidateKeys
    key → old candidate ID

candidates
    old candidate ID → missing
```

The current `addCandidate()` already contains logic for precisely this situation:

```js
existingId = candidateKeys.get(key)
existing = candidates.get(existingId)
if (existing) {
    ...
}
```

That is an implicit acknowledgement that the two structures can become inconsistent.

The correct invariant should instead be explicit:

```
candidateKeys[k] = id
        ⇒
candidates.has(id)
```

or the index entry must be removed.

### 7. restore() introduces another important issue

This is arguably more serious.

`restore()` directly inserts persisted state:

```js
this.candidates.set(...)
this.candidateKeys.set(...)
this.observations.set(...)
this.discoveries.set(...)
this.resources.set(...)
```

and reconstructs `fingerprintIndex`.

But it does not apply the runtime retention limits during restoration.

So:

```
runtime:
    maxResourcesInMemory = 2000

persisted state:
    5000 resources

restore()
    ↓
5000 resources loaded
```

The runtime bound is therefore not necessarily a bound on the actual runtime state.

This is a major verification point.

Required invariant:

After every state-loading operation:

```js
restore(data)
```

must result in:

```
∀ C:
    size(C) ≤ retentionBound(C)
```

Otherwise the bound only applies to incremental insertion.

### 8. Persistence limits and runtime limits are currently different systems

The project has:

```js
maxDiscoveriesInMemory = 2000
maxResourcesInMemory = 2000
```

and separately:

```js
persistedDiscoveries = 1200
persistedResources = 1500
persistedEdges = 3000
```

That's actually a good distinction:

```
Runtime:
    "How much can I keep?"

Persistence:
    "How much do I save?"
```

But `restore()` needs a third rule:

```
Restoration:
    "How much am I allowed to load?"
```

So the model should become:

```
Retention

          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Runtime   Persistence  Restoration
          │          │          │
       2000       1500         ≤2000
```

### 9. There is also a semantic bug in visited

`visited` is serialized in its entirety:

```js
visited: [...this.visited]
```

while `candidates`/`discoveries`/`resources` have persistence slices.

So even if all object collections are bounded, `visited` can become the historical memory sink.

This is particularly subtle because `visited` is a correctness index, not merely telemetry.

If you evict it arbitrarily, GDE can rediscover things it previously processed.

Therefore:

```
visited
```

cannot be treated like:

```
diagnostics
```

It requires semantic retention.

### 10. This leads to a stronger GDE state taxonomy

I would now classify the state into four categories:

```
GDE Knowledge State
│
├── 1. Control State
│      candidates
│      claimed
│      lifecycle
│
├── 2. Search Memory
│      visited
│      candidateKeys
│      patternIndex
│      clusterIndex
│
├── 3. Evidence State
│      observations
│      discoveries
│      resources
│      graphEdges
│      networkEvents
│
└── 4. Derived Indexes
       fingerprintIndex
       candidateKeys
       patternIndex
       clusterIndex
```

Then each category gets a different retention policy.

This is substantially cleaner than applying FIFO independently to every Map.

### 11. The crucial invariant should become referential integrity

For the next version, I would introduce explicit verification invariants:

- **RI-1 — Candidate index:** `∀ k,id: candidateKeys[k]=id ⇒ candidates[id] exists`
- **RI-2 — Resource observations:** `∀ r,o: r.observationIds contains o ⇒ observation o exists OR o is explicitly historical`
- **RI-3 — Resource discoveries:** `r.discoveryIds contains d ⇒ d exists OR d is historical`
- **RI-4 — Resource candidates:** `r.candidateIds contains c ⇒ c exists OR c is historical`
- **RI-5 — Fingerprint index:** `fingerprintIndex[h] contains URL u ⇒ u has corresponding retained resource OR index explicitly permits historical URLs`
- **RI-6 — Graph edges:** `edge.from / edge.to` must have a defined interpretation if either endpoint is evicted.

This is especially important because the current edge array is bounded to 5,000 but does not appear to perform endpoint validation when nodes disappear.

### 12. This changes what “bounded memory” should mean

There are actually three levels:

| Level | Meaning | v1.5 |
|---|---|---|
| B1 | Individual containers have size limits | Mostly yes |
| B2 | Total payload memory has limits | No |
| B3 | Graph + indexes remain bounded and referentially coherent | No |

The project currently reaches approximately B1.

The engineering target should be B3.

And B3 is more interesting because it transforms GDE from:

> a discovery script with caches

into:

> a bounded knowledge-state machine with formally defined retention semantics.

### The next architectural move

I would not immediately patch every individual collection.

Instead, define:

```
RetentionManager
        │
        ├── CandidateStore
        ├── ObservationStore
        ├── DiscoveryStore
        ├── ResourceStore
        ├── EvidenceStore
        └── IndexStore

with one operation:

evict(entity)

whose contract is:

evict(x):
    1. remove x from primary store
    2. remove/update reverse indexes
    3. update relationship references
    4. preserve historical evidence if policy requires it
    5. emit deterministic ledger event
    6. re-check invariants
```

Then retention becomes a state transition, not a `Map.delete()`.

That is the point where the GDE architecture becomes much more rigorous.

### Current Assessment

v1.5 is a meaningful hardening release, but the audit now moves from “are there bounds?” to “are the bounds semantically correct?”

That is the right next problem for GDE.

The strongest next milestone would therefore be:

```
v1.5.x
  │
  ├── bounded body retention
  ├── bounded relationship cardinality
  ├── bounded indexes
  ├── bounded restoration
  └── referential-integrity invariant suite
          │
          ▼
      Bounded Knowledge Kernel
```

Once those invariants hold, the earlier DVB analogy becomes even stronger: the scanner isn't merely discovering candidates; it is maintaining a bounded, auditable discovery state machine.

---
*Saved from second-pass audit transcript — 2026-09-13 — branch `arena/01a08cd3-generic-discovery-engine` at v1.5.0 `508e3e…`.*
