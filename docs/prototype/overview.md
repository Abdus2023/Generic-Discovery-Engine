# Prototype Overview

> **Status:** CURRENT
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** What the browser userscript prototype is, where it came from and how its iterations are organised.

## Contents

- *Turn lead-in* — `Userscript Discovery Prototype.md` L2967–3007
- *Turn lead-in* — `Continue Architecture Planning.md` L21–38

## Related Documents

- [Userscript Development Narrative](userscript.md)
- [Configuration](configuration.md)
- [Prototype Scope and Limitations](limitations.md)
- [Prototype Version Artifacts](versions/README.md)
- [Concept Overview](../concepts/overview.md)

---

<!-- source: Userscript Discovery Prototype.md L2967–3007 | turn 13 | ChatGPT turn lead-in -->
The important part is that this **isn't really a “web crawler” disguised as a DVB scanner**. Its architecture deliberately follows the model we developed:

```
                    ┌─────────────────┐
                    │ Search Space    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Scheduler     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Candidate    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Acquisition   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Observation   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Recognizer    │
                    └────────┬────────┘
                             │
                       ┌─────┴─────┐
                       ▼           ▼
                  rejected     Discovery
                                   │
                                   ▼
                            New Candidates
                                   │
                                   └──────► Scheduler
```

<!-- source: Continue Architecture Planning.md L21–38 | turn 1 | ChatGPT turn lead-in -->
I see you’ve provided **two versions of the same userscript**:

* **v0.1.0** — basic discovery engine with HTML recognition.
* **v0.2.0** — more structured version with provider abstraction, JSON/text providers, and—most importantly—an atomic candidate-claim mechanism for concurrent workers.

If your goal is to improve this code, **v0.2.0 is clearly the better foundation**. I can help with any of these:

1. **Compare v0.1 vs v0.2** — identify exactly what improved and what remains broken.
2. **Debug/fix the script** — including syntax, concurrency, persistence, URL handling, and userscript compatibility.
3. **Produce a clean v0.3.0** — refactored, robust, and ready to paste into Tampermonkey/Violentmonkey.
4. **Add discovery capabilities** — JSON endpoints, `fetch()`/XHR interception, forms, sitemaps, robots.txt, manifests, embedded URLs, CSS URLs, etc.
5. **Improve the scheduler** — retries, backoff, priorities, deduplication, rate limiting, and cancellation.
6. **Improve the UI/export** — live progress, discovered-resource browser, filtering, JSON/CSV export.
7. **Review the architecture** against the DVB blind-scan analogy and make the candidate → observation → recognition → discovery → candidate loop more rigorous.

One immediate issue: **as pasted, both versions contain stray backtick delimiters around the JavaScript body**, so they aren't directly valid JavaScript. If those backticks are merely an artifact of how you pasted the code, then that can be ignored.

If you want, I can take **v0.2.0 and return a complete corrected v0.3.0 userscript** rather than just discussing the changes.
