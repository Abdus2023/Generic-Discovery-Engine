# ADR 029 — Health Metrics (observability + status)

**Status:** accepted (v1.4.0)  
**Transcript:** 1.4 observability — health check + export  
**Code:** `src/config.js` `health {enabled,maxRecentErrors,slowProviderMs}` `src/engine.js` `getHealthMetrics` `exportData().health` `getCoverageMetrics` `providerMetrics`, `tests/health-concurrent.test.js` 4 cases

## Context
v1.3.0 stabilized at 13 providers `6344` `bb0453…` 150/150 with lazy/bundle/ESM. No health endpoint: `getCoverageMetrics` had `providerInstances`/`providerMetrics` but no `status` (`healthy`/`degraded`/`unhealthy`/`disabled`), no `frontierPressure`/`requestPressure`/`ledgerPressure`, no `recentErrors` truncation. Operators cannot assert `health.status==='healthy'` in CI or `exportData().health` for dashboards. Provider slow threshold was implicit (no `CONFIG.health.slowProviderMs`), `recentErrors` unbounded. Need `npm test` health invariants and `verify:build` health gates.

## Decision
- **Config** `src/config.js` adds `health: {enabled:true, maxRecentErrors:20, slowProviderMs:50}` — `enabled false` → `status 'disabled'` (bypass), `slowProviderMs 50` → `avgMs > 50` → `slowProviders`, `maxRecentErrors 20` → `recentDiagnostics`/`recentLedgerErrors` slice.
- **Engine** `src/engine.js` adds `getHealthMetrics()` — calls `getCoverageMetrics()` → `providerMetrics`, computes `slowProviders` via `Object.entries(providerMetrics).filter(m.avgMs > slowThreshold).map({name,avgMs,calls,matches})` sorted desc, `recentDiagnostics` `db.diagnostics.slice(-maxRecentErrors)`, `recentLedgerErrors` `ledger.events.filter(/error|illegal|failed|bridge/i).slice(-5)`, pressures `frontierPressure = frontierSize / maxCandidates`, `requestPressure = requestsUsed / maxRequests`, `ledgerPressure = ledgerSize / 5000` (3 decimals), `status` logic: `healthy` default, `degraded` if `slowProviders>2 || frontierPressure>0.9 || requestPressure>0.9 || observations>750`, `unhealthy` if `slowProviders.some(avgMs>100) || liveCount>=maxCandidates || recentDiagnostics.length>maxRecentErrors`, `disabled` if `!health.enabled`, try/catch → `unknown`. Returns `{status, timestamp, coverage, providerHealth {slowProviders,totalProviders,slowThresholdMs,slowCount}, system {frontierPressure,requestPressure,ledgerPressure,concurrency,adaptive,healthEnabled}, recentErrors: [...ledgerErrors,...diagnostics].slice(-5)}` O(13) ~0.01 ms.
- **Export** `exportData()` adds `health: this.getHealthMetrics()` alongside `coverage/inference/providers` (schema stays `gde-export-v8.0` additive). `providers` now also includes `concurrent` flag. `getCoverageMetrics` unchanged but `health` consumes it.
- **Tests** `tests/health-concurrent.test.js` 4 health cases: `healthy` when no slow/low pressure, `degraded` when 3 slow `>50`, `unhealthy` when `liveCount==750`, `disabled` when `enabled:false`. `npm test` 160/160 42 suites (150+10) vs 150/150.

## Consequences
- **+** `engine.getHealthMetrics()` provides single-call observability for UI/dashboards (`status` triage, `slowProviders` top N, `system` pressures 0–1, `recentErrors` 5). `exportData().health` JSON-stable for `verify:build` health gate or external monitors. `slowProviderMs` tunable (e.g. `30` for stricter). `maxRecentErrors` caps diagnostics growth (500 → 20 recent).
- **+** Zero runtime overhead when `health.enabled false` (`status disabled` fast path); otherwise O(13) ~0.01 ms per call (UI `_doUpdateUI` could call `getHealthMetrics` without thrash). Additive, `CONFIG` v8 compatible, `STORAGE_KEY v8` unchanged.
- **−** `health` adds `~50` lines + export `+health` JSON ~1kB per export; negligible at 200k dist. `slowProviders` threshold `50ms` is heuristic (provider `matches` normally 0.01 ms, `recognize` 0.05 ms, so 50 captures only pathological regex/CPU).

## Links
- Code: `src/config.js` `health`, `src/engine.js` `getHealthMetrics` `exportData().health`, `tests/health-concurrent.test.js`.
- Prior: ADR 028 ESM, ADR 027 wellKnown/manifest, `VERIFICATION_SUPPLEMENT_v1.3.0.md`.
