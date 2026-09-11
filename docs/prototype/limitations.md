# Prototype Scope and Limitations

> **Status:** CURRENT
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** What the prototype deliberately does and does not implement, and what a browser prototype can guarantee.

## Contents

- **What changed — 3. The actual scope is now explicit** — `Userscript Discovery Prototype.md` L4784–4807
- **v0.7 — 6. One remaining architectural limitation** — `Continue Architecture Planning.md` L54418–54471
- **v0.30 — What the userscript should and should not become** — `Continue Architecture Planning.md` L85024–85066
- **v0.33 — 33.30 What the browser prototype can guarantee** — `Continue Architecture Planning.md` L90113–90152
- **v0.34 — 34.29 Prototype Boundary** — `Continue Architecture Planning.md` L91859–91905

## Related Documents

- [Prototype Overview](overview.md)
- [Userscript Development Narrative](userscript.md)
- [Concept Overview](../concepts/overview.md)
- [Coordination, Consistency and Transport](../architecture/coordination.md)

---

<!-- source: Userscript Discovery Prototype.md L4784–4807 | turn 15 | version ? -->
### What changed — 3. The actual scope is now explicit

**3. The actual scope is now explicit.**

This script is **not** implementing DVB blind scanning. It implements the _algorithmic pattern_:

> search → probe → recognize → discover → expand → schedule

against web resources.

The correspondence is architectural:

```
DVB                         Prototype

frequency candidate    →   URL candidate
RF detection            →   HTTP acquisition
demodulator lock        →   response recognition
PSI/SI                  →   content metadata
NIT                     →   metadata-derived candidates
multiplex discovery     →   resource discovery
scan database           →   knowledge base
```

It intentionally does **not** claim that HTTP discovery is equivalent to RF discovery. The useful research question here is whether the **blind-scan control architecture** generalizes beyond DVB—and this prototype gives you a concrete testbed for that idea.

<!-- source: Continue Architecture Planning.md L54418–54471 | turn 27 | version 0.7 -->
## v0.7 — 6. One remaining architectural limitation

There is still an important boundary:

```
Decision replay
       │
       ├── deterministic
       │
       ▼
Acquisition
       │
       └── nondeterministic external world
```

For example:

```
2026-09-10
GET /api/catalog
→ HTTP 200
→ 400 KB
→ fingerprint ABC123
```

A future execution could produce:

```
2026-09-11
GET /api/catalog
→ HTTP 200
→ 430 KB
→ fingerprint DEF456
```

Therefore the ledger should eventually support two explicit modes:

```
REPLAY MODE
────────────────────────────
Replay policy/decision graph
without touching network.

ACQUISITION MODE
────────────────────────────
Execute plans against the
current external world.
```

That separation prevents a common mistake:

> treating an acquisition log as though it were a deterministic execution trace.

---

<!-- source: Continue Architecture Planning.md L85024–85066 | turn 73 | version 0.30 -->
## v0.30 — What the userscript should and should not become

The architecture is now considerably larger than a sensible userscript.

That is a useful stopping point.

The **Generic Discovery Engine userscript should remain a prototype of the execution model**, not attempt to implement the entire theoretical system inside one browser script.

A practical implementation boundary is:

```
                 Generic Discovery Engine
                         userscript
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
     Sources            Acquisition        Recognition
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                      Frontier Runtime
                            │
                            ▼
                     Evidence / Graph
```

The deeper components can subsequently migrate into a proper runtime:

```
userscript
    ↓
browser prototype
    ↓
Rust discovery runtime
    ↓
WASM/plugin ecosystem
    ↓
agent/document acquisition platform
```

That is the natural convergence path with your broader **Rust + capability + evidence + provenance** architecture.

---

<!-- source: Continue Architecture Planning.md L90113–90152 | turn 81 | version 0.33 -->
## v0.33 — 33.30 What the browser prototype can guarantee

A single browser profile may reasonably provide:

```
same storage
+
atomic persistence operations
+
claim records
+
leases
```

This can support:

```
multiple tabs
multiple workers
```

within a shared persistence domain, subject to browser storage/concurrency semantics.

It cannot magically guarantee:

```
global distributed consensus
```

across:

```
different devices
different browsers
different storage systems
```

That requires a real coordination service or distributed database.

---

<!-- source: Continue Architecture Planning.md L91859–91905 | turn 83 | version 0.34 -->
## v0.34 — 34.29 Prototype Boundary

For the userscript, a realistic implementation should initially support:

```
single browser profile
        │
        ├── multiple tabs
        │
        ├── shared durable store
        │
        ├── worker identities
        │
        ├── leases
        │
        ├── fencing epochs
        │
        ├── optimistic versions
        │
        └── conflict records
```

But should explicitly label:

```
BROWSER PROFILE COORDINATION
```

rather than claiming:

```
DISTRIBUTED CONSENSUS
```

Across:

```
device A
device B
device C
```

you would need an actual shared authoritative coordination service or equivalent protocol.

That boundary should remain explicit.

---
