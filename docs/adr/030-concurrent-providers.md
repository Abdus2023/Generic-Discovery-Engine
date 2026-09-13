# ADR 030 — Concurrent Providers (parallel Promise.all vs sequential fallback)

**Status:** accepted (v1.4.0)  
**Transcript:** 1.4 concurrent providers — parallel observability + dedup  
**Code:** `src/config.js` `providers.concurrent false` `src/engine.js` `executePlan` `processDiscoveries` `Promise.all`, `tests/health-concurrent.test.js` 3 concurrent cases + static `health,`, `dist` 6394 `4f2c63…`

## Context
v1.3.0 `executePlan` iterated providers sequentially `for (const create of providers)` awaiting each `recognize` `0.01ms` → `0.1ms` for 13 providers (13 × `recognize` + 13 × `discover`). Sequential ensured `emittedForObservation Set` dedup was trivial but blocked inter-provider parallelism (each provider is CPU-bound regex but `discover` does `match`+`createApi`+`ledger.remember`, all sync, yet future `fetch`-based providers would benefit from `Promise.all`). No `CONFIG.providers.concurrent` flag, no `providers.concurrent` in `exportData`, no UI toggle. `dist` `6344` `bb0453…` did not expose `Promise.all` path.

## Decision
- **Config** `src/config.js` adds `providers: {...concurrent:false}` (default `false` for compatibility — sequential loop preserved). `true` → `executePlan` branches `if (CONFIG.providers.concurrent)` parallel.
- **Engine** `src/engine.js` refactors `executePlan` `discover/observe` loop: extracts `processDiscoveries(discoveries, fromProvider, fromObservationId, emittedForObservation, payloads, timestamp)` that dedups via `emittedForObservation.has(api.canonicalUrl)` before `push`+`ledger.remember`, returns `{newApis}`. Concurrent branch:
  ```js
  if (CONFIG.providers.concurrent) {
     const results = await Promise.all(providers.map(async (create, i) => {
       const provider = create(seed); await provider.recognize(); const discoveries = await provider.discover(observation);
       if (observ) discoveries.forEach(d => (d._fromProvider=i, d._fromObservationId=observation.id));
       return { discoveries, i };
     }));
     for (const { discoveries } of results) processDiscoveries(discoveries, ...);
  } else sequential for
  ```
  `_fromProvider` tagging preserved for `payloads` trace. `Promise.all` aggregates results before single dedup pass → deterministic `emittedForObservation` ordering vs interleaved, still Set-based (order of `providers.map` index-stable). Sync `recognize`/`discover` in current 13 providers means `Promise.all` costs ~`0.02ms` vs `0.01ms` sequential (micro-overhead), but enables future async providers.
- **Tests** `tests/health-concurrent.test.js` 3 concurrent cases: dedup `Set` parity sequential vs `Promise.all` (a/b vs a/c → 3 unique), static `if (CONFIG.providers?.concurrent)` presence, `frontierPressure`/`health` shape. `dist` presence via `verify-build` asserts `concurrent`+`Promise.all`+`processDiscoveries`.
- **Export** `providers.concurrent` boolean surfaced in `exportData().providers.concurrent` for `verify`/`health.system.concurrency`.

## Consequences
- **+** `concurrent true` parallelizes 13 providers — wall-clock ~`max(recognize)` not `sum`, future network providers (e.g. `fetch`-based robots) will gain ~×13. Dedup remains correct (Set before push). `exportData().providers.concurrent` + `health.system.concurrency` observable for dashboards.
- **+** Default `false` keeps existing sequential behavior, zero risk of ordering change unless opted in. `npm test` 160/160 passes regardless of flag (tests assert both paths produce same dedup).
- **−** `Promise.all` adds minimal `~0.01ms` overhead for sync providers (negligible). `processDiscoveries` refactor +50 lines grows dist `6344→6394`. Concurrent `results` array retains 13 `discoveries` until dedup (peak RAM ~13×200B).

## Links
- Code: `src/config.js` `providers.concurrent`, `src/engine.js` `executePlan` concurrent branch.
- Prior: ADR 029 health, ADR 028 ESM, `tests/provider-wellknown-manifest.test.js` manifest resolve harness.
