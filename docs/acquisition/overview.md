# Acquisition Overview

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Why acquisition is separated from discovery, and what acquisition is and is not responsible for.

## Source Sections

- **3. Detection should precede expensive decoding** — `USP-009` — `Userscript Discovery Prototype.md` L211–248
- **v0.9 — The important separation** — `CAP-082` — `Continue Architecture Planning.md` L55699–55730
- **v0.9 — 8. A deeper consequence: acquisition becomes replaceable** — `CAP-092` — `Continue Architecture Planning.md` L56071–56087

## Related Documents

- [Acquisition Model](acquisition-model.md)
- [Acquisition Runtime](runtime.md)
- [Response Recognition](response-recognition.md)
- [Provider Architecture](../architecture/provider-architecture.md)

---

<!-- USP-009 | Userscript Discovery Prototype.md L211–248 | turn 3 | version ? -->
## 3. Detection should precede expensive decoding

> **Source sections:** `USP-009`

A naïve blind scanner tries every possible demodulator configuration. That can become extremely expensive.

A better pipeline is:

```
RF energy?
   │
   ├── no → next candidate
   │
   └── yes
        │
        ▼
rough signal characterization
        │
        ▼
candidate parameter ranking
        │
        ▼
demodulation attempts
```

So instead of testing 100 possible symbol rates equally, you can estimate a likely symbol rate or occupied bandwidth and test the most probable candidates first.

Conceptually:

```
score(candidate) =
    w1 × signal_strength
  + w2 × bandwidth_match
  + w3 × timing_consistency
  + w4 × synchronization_score
```

Then attempt candidates in descending score order.

---

<!-- CAP-082 | Continue Architecture Planning.md L55699–55730 | turn 31 | version 0.9 -->
### v0.9 — The important separation

> **Source sections:** `CAP-082`
>
> **Note:** explicit override

There are now **two different provider systems**:

```
Acquisition Providers
    = obtain bytes / response metadata

Recognition Providers
    = interpret obtained bytes
```

For example:

```
candidate
   │
   ├── acquisition provider
   │       └── GM-XHR
   │             └── HTTP response
   │
   └── recognition provider
           └── HTML provider
                 ├── links
                 ├── scripts
                 ├── manifests
                 └── API endpoints
```

This prevents a common architectural mistake: treating "HTTP client" and "HTML parser" as the same kind of provider.

---

<!-- CAP-092 | Continue Architecture Planning.md L56071–56087 | turn 31 | version 0.9 -->
## v0.9 — 8. A deeper consequence: acquisition becomes replaceable

> **Source sections:** `CAP-092`
>
> **Note:** explicit override

The engine can eventually run with:

```
Generic Discovery Engine
│
├── GM-XHR Provider
├── Fetch Provider
├── Browser Provider
├── Archive Provider
├── Local File Provider
├── Cache Provider
└── Replay Provider
```

The last two are particularly important.
