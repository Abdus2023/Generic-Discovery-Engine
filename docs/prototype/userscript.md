# Userscript Development Narrative

> **Status:** CURRENT
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** The change notes recorded alongside each userscript iteration, in conversation order.

## Source Sections

- **v0.3 — What changed from v0.2.0** — `CAP-005` — `Continue Architecture Planning.md` L2647–2671
- **v0.4 — Notable v0.4.0 behavior** — `CAP-011` — `Continue Architecture Planning.md` L7124–7148
- *Turn lead-in* — `CAP-014` — `Continue Architecture Planning.md` L13454–13472
- **v0.4 — What changed from v0.3.0** — `CAP-017` — `Continue Architecture Planning.md` L18267–18282
- **v0.5 architecture** — `CAP-022` — `Continue Architecture Planning.md` L23095–23126
- **v0.5 — What v0.6 changes architecturally** — `CAP-025` — `Continue Architecture Planning.md` L29352–29424
- **v0.5 — What v0.5.0 changes architecturally** — `CAP-028` — `Continue Architecture Planning.md` L34706–34740
- **v0.6.0's main architectural additions** — `CAP-031` — `Continue Architecture Planning.md` L43129–43181
- **v0.6 — What changed in v0.6** — `CAP-034` — `Continue Architecture Planning.md` L48362–48376
- *Turn lead-in* — `CAP-044` — `Continue Architecture Planning.md` L54115–54115
- **v0.7 — What v0.7.1 actually changes** — `CAP-045` — `Continue Architecture Planning.md` L54117–54121
- **v0.7 — Before** — `CAP-046` — `Continue Architecture Planning.md` L54123–54133
- **v0.7 — Now** — `CAP-047` — `Continue Architecture Planning.md` L54135–54163
- **v0.7 — 4. Candidate state machine** — `CAP-050` — `Continue Architecture Planning.md` L54270–54328

## Related Documents

- [Prototype Overview](overview.md)
- [Prototype Version Artifacts](versions/README.md)
- [Configuration](configuration.md)
- [Prototype Scope and Limitations](limitations.md)

---

<!-- CAP-005 | Continue Architecture Planning.md L2647–2671 | turn 3 | version 0.3 -->
### v0.3 — What changed from v0.2.0

> **Source sections:** `CAP-005`

The most important correction is **URL resolution**. In v0.2.0, parsing fetched HTML with `DOMParser` and then using `element.href` can resolve relative URLs against the parser-created document rather than reliably against the URL that was actually fetched. v0.3.0 explicitly resolves attributes against `observation.http.finalUrl`.

I also changed the discovery model so HTML can now discover:

* links
* scripts
* stylesheets
* images
* iframes/frames
* media
* tracks
* objects/embeds
* forms
* canonical URLs
* OpenGraph URLs
* meta-refresh destinations
* URLs embedded in HTML text

The concurrency model from v0.2.0 is retained: **candidate ownership is established synchronously before any `await`**, so multiple workers cannot claim the same candidate.

The state persistence deliberately **doesn't persist response bodies or observations**, since those can become enormous. It persists visited keys and bounded discovery results instead.

One design choice remains intentionally conservative: `sameOriginOnly: true`. That prevents this generic scanner from turning every discovered third-party URL into an unrestricted cross-origin crawler. You can change it to `false` when you explicitly want cross-origin discovery and your userscript environment permits those requests.

<!-- CAP-011 | Continue Architecture Planning.md L7124–7148 | turn 7 | version 0.4 -->
### v0.4 — Notable v0.4.0 behavior

> **Source sections:** `CAP-011`

The new **passive network observer** is deliberately different from the active scanner. When the page itself calls `fetch()` or XHR, the engine records that URL as a high-confidence candidate. It doesn't generate requests merely to create those observations.

The provenance graph now lets an export represent relationships such as:

```
initial page
   │
   └── HTML discovery
          │
          ├── /api/config
          │      │
          │      └── JSON discovery
          │             │
          │             └── /api/products
          │
          └── /static/app.js
                 │
                 └── text/CSS discovery
```

The scheduler also now tracks **depth**, so discovery doesn't grow indefinitely through recursive links. `maxDepth: 8` and `maxRequests: 150` provide two independent bounds.

One caveat with the network observer: because this is a userscript, whether it can observe page JavaScript's `fetch`/XHR depends on the userscript manager's execution-world/isolation behavior. The active acquisition path remains independent of that observer, so the scanner still functions when passive interception isn't available.

<!-- CAP-014 | Continue Architecture Planning.md L13454–13472 | turn 9 | ChatGPT turn lead-in -->
> **Source sections:** `CAP-014`

One important architectural change in v0.5.0 is that **network observation is now a first-class observation source**, rather than merely another URL extractor. The resulting graph can distinguish:

```
page
 ├─ HTML
 │   └─ /api/config
 │
 ├─ performance-resource
 │   └─ /assets/app.js
 │
 ├─ fetch-response
 │   └─ /api/products
 │
 └─ robots.txt
     └─ /sitemap.xml
          └─ /products/123
```

The next logical step would be **v0.6.0**, where the engine can evolve from a URL crawler into a genuine **resource inference engine**: endpoint templates, parameter relationships, API schemas, authentication/session boundaries, content fingerprints, and graph-based prioritization.

<!-- CAP-017 | Continue Architecture Planning.md L18267–18282 | turn 11 | version 0.4 -->
### v0.4 — What changed from v0.3.0

> **Source sections:** `CAP-017`

* **Network discovery:** observes page-context `fetch()` and `XMLHttpRequest` activity without capturing response bodies.
* **Passive network discovery:** watches `PerformanceResourceTiming` entries as another source of URLs.
* **Depth-aware graph:** candidates now carry discovery depth and are capped by `maxDepth`.
* **Smarter scheduler:** priority is adjusted by depth, and failed candidates use exponential retry backoff.
* **More providers:** HTML, JSON, XML/sitemaps, CSS, JavaScript, robots.txt, and generic text.
* **Well-known discovery:** seeds `/robots.txt` and `/sitemap.xml`.
* **Manifest discovery:** follows `<link rel="manifest">`.
* **Richer HTML discovery:** canonical URLs, OpenGraph/Twitter URLs, meta refreshes, forms, media, SVG resources, etc.
* **Safer persistence:** raw JSON response bodies are no longer persisted.
* **Graph export:** discoveries now retain mechanism, parent, candidate type, and depth, producing a usable provenance graph.
* **Network candidates are deduplicated** separately from ordinary candidate processing.
* **Retry workers no longer exit prematurely** when candidates are waiting for backoff.

One limitation is intentional: the page-context `fetch`/XHR bridge observes **URLs and metadata, not response bodies**. The normal acquisition pipeline subsequently fetches discovered URLs itself, subject to the configured same-origin and request limits.

<!-- CAP-022 | Continue Architecture Planning.md L23095–23126 | turn 15 | version 0.5 -->
### v0.5 architecture

> **Source sections:** `CAP-022`
>
> **Note:** explicit override

The important change is that **resource identity is now the canonical URL**, while the _way it was discovered_ is provenance:

```
                    ┌── HTML link ────────┐
                    │                     │
page ───────────────┼── CSS reference ───┼──► /api/products
                    │                     │
                    ├── JavaScript ───────┤
                    │                     │
                    └── network fetch ────┘
```

So `/api/products` can be discovered four different ways but acquired only once.

The exported graph now conceptually looks like:

```
root
 ├── html-document
 │    ├── html-links ──────────► /products
 │    ├── html-resources ──────► /app.js
 │    └── html-resources ──────► /style.css
 │
 ├── network-observation ─────► /api/session
 │
 └── robots-document
      └── sitemap ─────────────► /sitemap.xml
```

One deliberate boundary remains: **observed POST/PUT/PATCH/DELETE requests are recorded but are not replayed by default**. That prevents the discovery engine from turning page observation into unintended state-changing requests.

<!-- CAP-025 | Continue Architecture Planning.md L29352–29424 | turn 17 | version 0.5 -->
### v0.5 — What v0.6 changes architecturally

> **Source sections:** `CAP-025`

The key improvement is that **candidates are no longer the resource database**.

```
                 ┌── HTML
                 ├── CSS
                 ├── JavaScript
                 ├── JSON
                 └── network
                       │
                       ▼
                ResourceRecord
                /api/data
                       │
              ┌────────┴────────┐
              ▼                 ▼
        observations        provenance
              │                 │
              ▼                 ▼
        fingerprints          edges
```

That means one canonical resource can accumulate:

```
/api/data

types:
  api
  network

mechanisms:
  json-parser
  network-fetch
  performance-observer
  javascript-parser

observations:
  observation-1

discoveries:
  discovery-1
  discovery-2

acquisitionCount:
  1
```

even if five different parts of the page lead to it.

The network bridge also now assigns a **request ID**, so the logical relationship is:

```
fetch request
    │
    │ requestId = fetch-123
    ▼
network event
    │
    │ requestId = fetch-123
    ▼
fetch response
    │
    ├── status
    ├── content-type
    ├── final URL
    └── duration
```

rather than treating the request and response as unrelated observations.

The next natural step for **v0.7** would be to turn the scheduler into a more formal **work-queue engine**: separate candidate queues by class, dynamic prioritization based on observed provider yield, redirect-aware depth, negative-result caching, and incremental graph streaming instead of constructing the graph only at export time.

<!-- CAP-028 | Continue Architecture Planning.md L34706–34740 | turn 19 | version 0.5 -->
### v0.5 — What v0.5.0 changes architecturally

> **Source sections:** `CAP-028`

The important shift is that **URLs and resources are now separate from candidates**.

A single resource can therefore be discovered through:

```
HTML link ───────┐
CSS url() ───────┤
JavaScript ──────┼──→ https://example.com/api/data
Network fetch ───┤
Performance API ─┘
```

…but the scheduler performs only **one actual acquisition** for that canonical URL.

The exported graph preserves those separate discovery edges even when acquisition is deduplicated.

It also now records:

* candidate lifecycle transitions
* request/response network events
* GET-only network replay
* API-oriented priority
* provider confidence
* resource fingerprints
* redirects
* resource-level status
* multiple provenance mechanisms
* performance-resource observations
* bounded persistence
* graph nodes and edges
* acquisition observations without exporting raw response bodies

One deliberate safety/semantics change is that observed `POST`, `PUT`, `PATCH`, `DELETE`, etc. requests are **recorded but never automatically replayed**. Only observed `GET` traffic can become an acquisition candidate.

<!-- CAP-031 | Continue Architecture Planning.md L43129–43181 | turn 21 | version 0.6 -->
### v0.6.0's main architectural additions

> **Source sections:** `CAP-031`
>
> **Note:** explicit override

The scheduler is now effectively:

```
                 ┌──────────────┐
candidate ──────►│ policy gate  │
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │ origin budget│
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │ adaptive     │
                 │ concurrency  │
                 └──────┬───────┘
                        │
                 ┌──────▼───────┐
                 │ acquisition  │
                 └──────┬───────┘
                        │
                    observation
                        │
                 ┌──────▼───────┐
                 │ recognition  │
                 └──────┬───────┘
                        │
                    discovery
                        │
                 ┌──────▼───────┐
                 │ new candidate│
                 └──────────────┘
```

Notable changes:

* **Forms are discovered but not fetched by default.**
* **Images/media are discovered but not fetched by default.**
* **Non-GET network traffic is observed but never replayed.**
* **Per-origin request budgets** prevent one site from consuming the entire scan.
* **Per-origin concurrency** defaults to 2.
* **Minimum request spacing** defaults to 150 ms.
* **Adaptive concurrency** backs off after repeated acquisition failures and recovers after successful acquisitions.
* **Tracking parameters** such as `utm_*`, `fbclid`, and `gclid` can be stripped during canonicalization.
* **Redirects become explicit graph edges.**
* **Identical acquired representations are grouped by fingerprint**, while their URLs remain separate resources.
* **Pause / Resume / Stop** are now scheduler controls rather than merely UI decoration.
* **Policy-skipped resources remain represented in the knowledge graph**, instead of disappearing.
* **Origin accounting and duplicate-content groups are exported.**
* Persistence has been advanced to **state version 6**.

The conceptual direction for the next version would be to move toward a true **evidence/fusion layer**: instead of treating every provider discovery equally, multiple independent observations of the same resource could accumulate evidence and produce a single confidence score before the scheduler decides what to explore next.

<!-- CAP-034 | Continue Architecture Planning.md L48362–48376 | turn 23 | version 0.6 -->
### v0.6 — What changed in v0.6

> **Source sections:** `CAP-034`

* **Acquisition policy layer:** forms/media/binary resources are discovered but not automatically fetched by default.
* **Per-origin budgets:** request count, minimum spacing, and concurrent requests are controlled independently for each origin.
* **Adaptive concurrency:** repeated failures/timeouts reduce concurrency; sustained success restores it.
* **Pause / Resume / Stop:** stopping prevents new requests while allowing already-running requests to finish.
* **Canonicalization:** fragments, default ports, and common tracking parameters are normalized away.
* **Content fingerprints:** identical response bodies are grouped as duplicate content without collapsing the distinct URLs.
* **Redirect graph edges:** requested → final URLs are explicitly represented.
* **Dynamic DOM discovery:** newly inserted links/scripts/forms/resources are discovered through `MutationObserver`.
* **Bounded diagnostics:** scheduler decisions, retries, skips, failures, and duplicate-content events are retained.
* **Persistence upgraded to v6:** existing v5 state can still be loaded.
* **Hard request reservation:** the global request budget is reserved synchronously before an acquisition starts, preventing concurrency races from exceeding `maxRequests`.

One deliberate safety/semantic change is important: **a discovered form action is now represented in the knowledge graph but is not automatically requested**. That keeps discovery separate from performing potentially state-changing web actions.

<!-- CAP-044 | Continue Architecture Planning.md L54115–54115 | turn 27 | ChatGPT turn lead-in -->
> **Source sections:** `CAP-044`

---

<!-- CAP-045 | Continue Architecture Planning.md L54117–54121 | turn 27 | version 0.7 -->
## v0.7 — What v0.7.1 actually changes

> **Source sections:** `CAP-045`

The important change is not the provider code.

It is the **control-plane contract**.

<!-- CAP-046 | Continue Architecture Planning.md L54123–54133 | turn 27 | version 0.7 -->
### v0.7 — Before

> **Source sections:** `CAP-046`

```
Candidate
   │
   └──────► Acquisition
```

The implicit question was:

> “Can I fetch this candidate?”

<!-- CAP-047 | Continue Architecture Planning.md L54135–54163 | turn 27 | version 0.7 -->
### v0.7 — Now

> **Source sections:** `CAP-047`

```
Candidate
   │
   ▼
AcquisitionPolicy
   │
   ▼
AcquisitionPlan
   │
   ├── allowed=false
   │       └── reason
   │
   └── allowed=true
           │
           ▼
       Budget
           │
           ▼
       Origin Slot
           │
           ▼
       Acquisition
```

That makes the acquisition boundary explicit.

---

<!-- CAP-050 | Continue Architecture Planning.md L54270–54328 | turn 27 | version 0.7 -->
## v0.7 — 4. Candidate state machine

> **Source sections:** `CAP-050`

The lifecycle is now explicit:

```
                    ┌───────────────┐
                    │   discovered  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    queued     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    claimed    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    planned    │
                    └───────┬───────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
             denied                  allowed
                │                       │
                ▼                       ▼
             skipped                acquiring
                                        │
                                        ▼
                                   observed
                                        │
                                        ▼
                                  recognized
                                        │
                                        ▼
                                    expanded
                                        │
                                        ▼
                                   completed
```

Failure creates:

```
acquiring
    │
    ▼
 failed
    │
    ├── retry allowed → queued
    │
    └── retry exhausted → failed
```

---
