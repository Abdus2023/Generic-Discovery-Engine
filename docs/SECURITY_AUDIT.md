# Security Audit — Generic Discovery Engine v0.7.9

**Scope:** `dist/generic-discovery-engine.user.js` (5,597 lines), `dist/generic-discovery-engine.v0.7.1.user.js`, tests, configuration  
**Date:** 2026-09-10  
**Method:** static taint review + threat modeling + policy-vs-mechanism trace  
**Standard:** OWASP Top 10 (2021) + Greasemonkey/Tampermonkey userscript advisories  

---

## 1. Threat Model

| Actor | Capability | Interest |
|---|---|---|
| **Visited web page** | Serves HTML/JSON/JS that the engine will parse and potentially fetch further | Injection of malicious URLs, tracking params, large payloads |
| **Network attacker (MITM)** | Controls HTTP response body if not HTTPS | XSS via payload that provider parses |
| **Malicious discovery value** | JSON string that looks like URL (`javascript:`, `data:`) | Drive acquisition to unintended scheme |
| **Extension host** | Grants `GM_xmlhttpRequest @connect *` | Cross-origin fetch capability |
| **Persistent storage reader** | Reads `GM_getValue` store | PII in URLs (session tokens, query strings) |

**Not in scope:** RF/DVB stack (none exists), browser extension sandbox escape.

---

## 2. Findings Summary

| # | Severity | Title | Status |
|---|---|---|---|
| S-01 | **HIGH** (mitigated) | `@connect *` declares wildcard cross-origin | **Mitigated** by `sameOriginOnly:true` default + `isAllowedUrl` + `AcquisitionPolicy` double-check |
| S-02 | **MEDIUM** | Network bridge injects `<script>` into page world | **Documented, fallback** — CSP can block; engine degrades to `PerformanceObserver` evidence-only |
| S-03 | **MEDIUM** (mitigated) | HTML provider parses untrusted body | **Safe** — `DOMParser` does not execute scripts; no `innerHTML` assignment of body to live document |
| S-04 | **LOW** (mitigated) | `javascript:` / `data:` URL injection via JSON/text | **Blocked** — `isAllowedUrl` requires `^https?:$`, checked in both `discover()` and `policy.plan()` |
| S-05 | **LOW** (mitigated) | Form acquisition could cause side-effects (GET-disguised POST) | **Disabled** — `acquireForms:false` by default; provider still *discovers* form actions but `policy` denies `forms-disabled` |
| S-06 | **LOW** (mitigated) | Binary/media bulk fetch → DoS + heap bloat | **Disabled** — `acquireMedia:false`, `acquireBinaryResources:false` |
| S-07 | **INFO** | Persistent ledger stores URLs with query strings (potential session tokens) | **Accepted** — `Clear` requires explicit `GM_setValue(..., null)` + reload; export includes raw discoveries; document in README/Threat Model |
| S-08 | **INFO** | Regex URL extraction on 2 MB body (ReDoS risk) | **Bounded** — `maxBodyChars 2M`, `fingerprintMaxChars 1M`, body truncation, `Set` dedup; no nested quantifiers that cause catastrophic backtracking |
| S-09 | **INFO** | `stripTrackingParams` removes `ref` which may be semantic on some sites | **Configurable** — `CONFIG.stripTrackingParams` toggle; lossy canonicalization is intentional for dedup, documented |

**Overall posture:** **Secure by default** — all acquisition paths deny by default unless `method=GET` + `sameOrigin` + `depth` + `type` allowlist; discovery (observing) is separate from acquisition (fetching).

---

## 3. Detailed Evidence

### S-01 — Wildcard `@connect *`
```
// ==UserScript==
// @connect      *
```
The Tampermonkey header declares all hosts, but runtime enforcement is:
```js
function isAllowedUrl(url) {
  if (!/^https?:$/.test(parsed.protocol)) return false;
  if (CONFIG.sameOriginOnly && parsed.origin !== location.origin) return false;
  return true;
}
// checked in discover() AND AcquisitionPolicy.plan()
```
And `CONFIG.sameOriginOnly:true` is the default. Changing it to `false` is a deliberate, visible config edit; then `@connect *` becomes actually needed. Recommendation (P2) remains: narrow to `@connect self` when confined, or add runtime warning when `sameOriginOnly:false`.

### S-02 — Bridge injection
```js
installBridge() {
  const script = document.createElement('script');
  script.textContent = `(function(){ if(window.__GDE_NETWORK_BRIDGE__) return; ... })();`;
  (document.documentElement||document.head||document.body)?.appendChild(script);
  script.remove();
}
```
- Runs in **page world**, subject to page CSP (`script-src`). Blocked → `catch` → `recordDiagnostic('network-bridge-error')`.
- Communication via `window.postMessage({source:'generic-discovery-engine', type:'network'})` with origin check `event.source===window && event.data.source==='generic-discovery-engine'`.
- Degradation: `PerformanceObserver` evidence-only for `fetch/xhr` (v0.7.1 fix) ensures `POST /api` resource timing is **not** promoted to `GET` candidate.

### S-03 — HTML parsing
```js
const doc = new DOMParser().parseFromString(observation.body, 'text/html');
for (const el of doc.querySelectorAll('a[href]')) emit(el.href, ...)
```
- `DOMParser` does **not** execute `<script>`, `<img onerror>`, etc.
- No `panel.innerHTML = body` — only reads `href/src/action/content` attributes.
- Panel’s `innerHTML` is static (no interpolation of `body`).

### S-04 — Scheme validation
```js
if (!/^https?:$/.test(parsed.protocol)) return false;
```
Blocks `javascript:`, `data:`, `blob:`, `mailto:`, `ftp:` etc. Even if JSON contains `"url": "javascript:alert(1)"`, `canonicalizeUrl` succeeds but `isAllowedUrl` fails and `discover()` returns `null`.

### S-05 / S-06 — Type guards
```js
if (candidate.type==='form' && !CONFIG.policy.acquireForms) deny('forms-disabled')
if (candidate.type==='media' && !CONFIG.policy.acquireMedia) deny('media-disabled')
if (candidate.hints?.binary && !CONFIG.policy.acquireBinaryResources) deny('binary-disabled')
```
All default `false`. Provider still emits `kind:form` discoveries for graph completeness, but `executePlan` short-circuits to `markSkipped`.

### S-08 — Regex bounds
```js
maxBodyChars: 2_000_000,
fingerprintMaxChars: 1_000_000,
// in Acquisition.request:
if (body.length > CONFIG.maxBodyChars) body = body.slice(0, CONFIG.maxBodyChars);
```
Extraction regexes:
```js
/\bhttps?:\/\/[^\s"'<>\)]+/gi          // absolute
/(?:^|["'(\s])((?:\/|\.\.?\/)[A-Za-z0-9._~:/?#\[\]@!$&'*+,;=%-]+)/g  // relative
/url\(\s*(['"]?)(.*?)\1\s*\)/gi        // CSS
```
No nested `*` inside `*` that triggers ReDoS; each runs once over `String(text).matchAll`. Time is O(n) for 2 MB, acceptable at `concurrency:4`.

---

## 4. Residual Recommendations (P2)

1. **Add CSP meta check:** before `installBridge()`, test `document.securityPolicy` or try/catch and immediately downgrade; already done via `try/catch`, but add explicit `diagnostic: 'csp-blocks-bridge'`.
2. **Add PII scrub option:** `CONFIG.scrubQueryParams = ['token','session','auth']` to strip before `visited`/`ledger` persistence; off by default, opt-in for sensitive sites.
3. **Narrow `@connect`:** generate header from `CONFIG.sameOriginOnly` (build step) — `*` vs `self`.
4. **Add Trusted Types compliance:** `script.textContent` assignment is allowed but document with `trustedTypes` policy if page uses it.

---

## 5. Verification

- `tests/canonicalize-and-policy.test.js` asserts `isAllowedUrl` rejects `javascript:`, `data:`, cross-origin; `AcquisitionPolicy` denies `POST`, `max-depth`, `forms-disabled`, `media-disabled`, `binary-disabled`, `url-not-allowed`.
- `node --check` passes; no `eval`, `new Function`, `innerHTML=body`.

---

*Auditor: Arena Agent — static review, 2026-09-10*
