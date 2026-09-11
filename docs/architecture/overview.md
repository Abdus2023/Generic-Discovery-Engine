# Architecture Overview

> **Status:** DESIGNED
>
> **Source:** `Userscript Discovery Prototype.md`
>
> **Purpose:** Whole-architecture overviews as they were recorded in the planning conversation.

## Source Sections

- **41. The resulting architecture** — `USP-064` — `Userscript Discovery Prototype.md` L1877–1922

## Related Documents

- [README.md](../README.md)
- [System Model](system-model.md)
- [Concept Overview](../concepts/overview.md)
- [Acquisition Model](../acquisition/acquisition-model.md)
- [Providers Overview](../providers/overview.md)
- [Prototype Overview](../prototype/overview.md)

---

<!-- USP-064 | Userscript Discovery Prototype.md L1877–1922 | turn 11 | version ? -->
## 41. The resulting architecture

> **Source sections:** `USP-064`

You end up with something like:

```
                         ┌──────────────────┐
                         │  Discovery API   │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │ Discovery Engine │
                         └────────┬─────────┘
                                  │
               ┌──────────────────┼──────────────────┐
               ▼                  ▼                  ▼
        ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
        │  Scheduler  │    │  Knowledge  │    │  Event Bus  │
        │             │    │    Base     │    │             │
        └──────┬──────┘    └─────────────┘    └─────────────┘
               │
               ▼
        ┌─────────────┐
        │ Acquisition │
        │   Adapter   │
        └──────┬──────┘
               │
       ┌───────┴────────┐
       ▼                ▼
    DVB-S/S2          DVB-T/T2
       │                │
       └───────┬────────┘
               ▼
        ┌─────────────┐
        │   Metadata  │
        │   Parsers   │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │ Discoveries │
        └─────────────┘
```

At this point, **blind scanning is just one strategy plugged into a general discovery engine**.

The really interesting consequence is that the same engine can support **continuous spectrum discovery**: initial blind scan → network-guided expansion → periodic verification → change detection → incremental rescan.
