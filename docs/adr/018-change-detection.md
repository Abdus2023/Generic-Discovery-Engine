# ADR 018 — Change Detection (fingerprint diff → resource-changed)

**Status:** accepted (v0.8.0)  
**Transcript:** Phase 3 “change detection” + Phase 1 “historical knowledge”  
**Code:** `CONFIG.changeDetection`, `KnowledgeBase.recordObservation` `_oldHash` capture + `fingerprint` diff + `recordDiagnostic('resource-changed')`, `ResourceRecord.status='changed'`

## Context
`KnowledgeBase` stored `ResourceRecord` with `fingerprint` and `fingerprintIndex: Map<hash,Set<url>>` but never compared current vs previous hash for the same target. A page that changed from `hash:aaa` to `hash:bbb` was still marked `acquired`, hiding that the resource is stale and should be re-expanded. The transcript listed “change detection” as future, and verification noted no test for fingerprint diff.

## Decision
- Add `CONFIG.changeDetection: true` (on by default).
- In `KnowledgeBase.recordObservation(observation)`:
  1. Capture `_oldHash` **before** `ensureResource` + `merge` via `this.resources.get(canonical)?.fingerprint?.hash` (try/catch, canonicalized URL).
  2. After `fingerprintIndex` update, if `CONFIG.changeDetection && _oldHash && hash !== _oldHash`, emit `recordDiagnostic('resource-changed', {target, oldHash, newHash})` and set `resource.status='changed'` (overwrites `acquired`).
  - Cost O(1) Map lookup + hash compare, ~0.01 ms; no extra network.
  - No auto-requeue yet; `changed` status is observable via `exportData` and `getCoverageMetrics` future.

## Consequences
- **+** Operators see `resource-changed` in `ledger/diagnostics` and `exportData`, enabling polling or `onChange` callback future.
- **+** Deterministic: same body → same hash → no diagnostic; different body → diagnostic (proven by `provider-robots-headers.test.js` change detection 3 cases).
- **−** `changed` status is informational only; scheduler does not yet re-queue `changed` resources (would need `candidateTTL` or explicit `revisit`) — documented as residual.

## Links
- Tests: `tests/provider-robots-headers.test.js` “change detection” (3 cases: source contains, diff emits, same no diagnostic).
- Code: `KnowledgeBase.recordObservation` `_oldHash`, `CONFIG.changeDetection`.
