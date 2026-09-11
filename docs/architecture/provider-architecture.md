# Provider Architecture

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** The provider layer: capability-driven adapters, acquisition providers, provider selection and provider failure.

## Source Sections

- **32. Use capability-driven adapters** — `USP-055` — `Userscript Discovery Prototype.md` L1547–1584
- **v0.9 — Acquisition Provider Architecture** — `CAP-080` — `Continue Architecture Planning.md` L55633–55639
- **v0.9 — 1. AcquisitionProvider contract** — `CAP-083` — `Continue Architecture Planning.md` L55732–55779
- **v0.9 — 2. Provider capabilities** — `CAP-084` — `Continue Architecture Planning.md` L55781–55807
- **v0.9 — 3. Provider selection** — `CAP-085` — `Continue Architecture Planning.md` L55809–55860
- **v0.9 — 4. GM-XHR becomes a component** — `CAP-086` — `Continue Architecture Planning.md` L55862–55906
- **v0.9 — 6. Provider failure ≠ acquisition denial** — `CAP-088` — `Continue Architecture Planning.md` L55963–55965
- **v0.9 — Policy denial** — `CAP-089` — `Continue Architecture Planning.md` L55967–55989
- **v0.9 — Provider failure** — `CAP-090` — `Continue Architecture Planning.md` L55991–56016
- **v0.9 — 7. Provider selection itself becomes an event** — `CAP-091` — `Continue Architecture Planning.md` L56018–56069
- **v0.9 — Cache provider** — `CAP-093` — `Continue Architecture Planning.md` L56089–56099
- **v0.9 — Replay provider** — `CAP-094` — `Continue Architecture Planning.md` L56101–56113
- **v0.9 — 9. The engine is now approaching a general resource runtime** — `CAP-095` — `Continue Architecture Planning.md` L56115–56191

## Related Documents

- [Acquisition Model](../acquisition/acquisition-model.md)
- [Response Recognition](../acquisition/response-recognition.md)
- [Providers Overview](../providers/overview.md)
- [Capability Model](capability-model.md)

---

<!-- USP-055 | Userscript Discovery Prototype.md L1547–1584 | turn 11 | version ? -->
## 32. Use capability-driven adapters

> **Source sections:** `USP-055`

The generic engine shouldn't know how to tune a specific chipset.

Instead:

```
DiscoveryEngine
      │
      ▼
AcquisitionAdapter
      │
      ├── DVB-S/S2 adapter
      ├── DVB-T/T2 adapter
      └── DVB-C adapter
```

An adapter exposes operations conceptually like:

```
probe(candidate)
acquire(candidate)
measure()
read_stream()
release()
```

The engine doesn't care whether the underlying implementation is:

* a hardware tuner,
* an SDR,
* a kernel driver,
* a networked tuner,
* or a simulator.

That is a major architectural advantage.

---

<!-- CAP-080 | Continue Architecture Planning.md L55633–55639 | turn 31 | version 0.9 -->
## v0.9 — Acquisition Provider Architecture

> **Source sections:** `CAP-080`

The next boundary is cleanly defined:

> **The discovery engine should decide _what_ may be acquired; an acquisition provider decides _how_ it is acquired.**

This removes the remaining hard dependency between the scheduler and `GM_xmlhttpRequest`.

<!-- CAP-083 | Continue Architecture Planning.md L55732–55779 | turn 31 | version 0.9 -->
## v0.9 — 1. AcquisitionProvider contract

> **Source sections:** `CAP-083`

The contract should be deliberately small:

```JavaScript
class AcquisitionProvider {
    capabilities() {
        return [];
    }

    canExecute(plan) {
        return false;
    }

    async execute(plan) {
        throw new Error('Not implemented');
    }

    describe() {
        return {
            id: 'unknown',
            name: 'Unknown Acquisition Provider'
        };
    }
}
```

The provider does **not** decide whether acquisition is permitted.

That decision already belongs to:

```
AcquisitionPolicy
```

Instead:

```
Policy
    → "this plan is authorized"

Provider
    → "I can execute this authorized plan"
```

This distinction matters.

---

<!-- CAP-084 | Continue Architecture Planning.md L55781–55807 | turn 31 | version 0.9 -->
## v0.9 — 2. Provider capabilities

> **Source sections:** `CAP-084`

A provider advertises capabilities:

```JavaScript
[
    'network.http',
    'network.get',
    'same-origin',
    'text-response',
    'binary-response'
]
```

For example:

| Provider | GET | Same-origin | Cross-origin | POST | Browser context |
| --- | --- | --- | --- | --- | --- |
| GM-XHR | yes | yes | configurable | no | no |
| Fetch | yes | yes | limited | no | yes* |
| Browser | yes | yes | browser-dependent | potentially | yes |

`*` “capable” does not mean “authorized”.

That distinction must remain explicit.

---

<!-- CAP-085 | Continue Architecture Planning.md L55809–55860 | turn 31 | version 0.9 -->
## v0.9 — 3. Provider selection

> **Source sections:** `CAP-085`

The resolver becomes:

```
AcquisitionPlan
       │
       ▼
required capabilities
       │
       ▼
provider registry
       │
       ├── provider A ── missing capability
       │
       ├── provider B ── can execute
       │
       └── provider C ── policy incompatible
                         │
                         ▼
                   select provider
```

A useful contract is:

```JavaScript
class AcquisitionProviderRegistry {
    constructor() {
        this.providers = [];
    }

    register(provider) {
        this.providers.push(provider);
        return this;
    }

    select(plan) {
        return this.providers.find(
            provider =>
                provider.canExecute(plan)
        ) || null;
    }

    describe() {
        return this.providers.map(
            provider => provider.describe()
        );
    }
}
```

---

<!-- CAP-086 | Continue Architecture Planning.md L55862–55906 | turn 31 | version 0.9 -->
## v0.9 — 4. GM-XHR becomes a component

> **Source sections:** `CAP-086`

Instead of:

```JavaScript
GM_xmlhttpRequest(...)
```

being scattered through the engine, it becomes:

```JavaScript
class GMXHRProvider extends AcquisitionProvider {
    capabilities() {
        return [
            'network.http',
            'network.get',
            'same-origin',
            'text-response',
            'binary-response'
        ];
    }

    canExecute(plan) {
        return (
            plan.method === 'GET' &&
            plan.target.startsWith(location.origin)
        );
    }

    async execute(plan) {
        // GM_xmlhttpRequest implementation
    }

    describe() {
        return {
            id: 'gm-xhr',
            name: 'GM XMLHttpRequest'
        };
    }
}
```

Now the rest of the engine doesn't care whether the request was performed by GM-XHR.

---

<!-- CAP-088 | Continue Architecture Planning.md L55963–55965 | turn 31 | version 0.9 -->
## v0.9 — 6. Provider failure ≠ acquisition denial

> **Source sections:** `CAP-088`

This gives us another important state distinction.

<!-- CAP-089 | Continue Architecture Planning.md L55967–55989 | turn 31 | version 0.9 -->
### v0.9 — Policy denial

> **Source sections:** `CAP-089`
>
> [DOCUMENTATION REVIEW] Contradiction **C-11** ([Review Notes](../REVIEW-NOTES.md#c-11--))

```
candidate
   ↓
plan
   ↓
POLICY DENIED
```

Example:

```
POST /api/order
```

Result:

```
discovered
represented
policy-denied
```

<!-- CAP-090 | Continue Architecture Planning.md L55991–56016 | turn 31 | version 0.9 -->
### v0.9 — Provider failure

> **Source sections:** `CAP-090`

```
candidate
   ↓
plan
   ↓
provider selected
   ↓
NETWORK FAILURE
```

Result:

```
discovered
planned
provider-selected
acquiring
failed
retry
```

These must never collapse into the same status.

---

<!-- CAP-091 | Continue Architecture Planning.md L56018–56069 | turn 31 | version 0.9 -->
## v0.9 — 7. Provider selection itself becomes an event

> **Source sections:** `CAP-091`

The v0.7 event ledger now gains:

```
acquisition-provider-selected
acquisition-provider-rejected
acquisition-provider-failed
```

Full chain:

```
candidate-discovered
        │
        ▼
candidate-claimed
        │
        ▼
acquisition-planned
        │
        ▼
provider-selection
        │
        ├── no provider
        │      └── acquisition-unavailable
        │
        ▼
provider-selected
        │
        ▼
slot-granted
        │
        ▼
request-started
        │
        ▼
request-completed
        │
        ▼
observation-recorded
        │
        ▼
provider-recognized
        │
        ▼
discovery-emitted
```

This makes the decision trail much more useful.

---

<!-- CAP-093 | Continue Architecture Planning.md L56089–56099 | turn 31 | version 0.9 -->
### v0.9 — Cache provider

> **Source sections:** `CAP-093`

```
candidate
   ↓
cache lookup
   ↓
existing observation
```

No network request.

<!-- CAP-094 | Continue Architecture Planning.md L56101–56113 | turn 31 | version 0.9 -->
### v0.9 — Replay provider

> **Source sections:** `CAP-094`
>
> [DOCUMENTATION REVIEW] Contradiction **C-08** ([Review Notes](../REVIEW-NOTES.md#c-08--))

```
candidate
   ↓
recorded acquisition
   ↓
historical observation
```

This enables deterministic testing without pretending that network replay is equivalent to live acquisition.

---

<!-- CAP-095 | Continue Architecture Planning.md L56115–56191 | turn 31 | version 0.9 -->
## v0.9 — 9. The engine is now approaching a general resource runtime

> **Source sections:** `CAP-095`

The architecture has evolved:

```
v0.1
Discovery

v0.2
Discovery + scheduling

v0.3
typed discovery

v0.4
resource identity

v0.5
observation + recognition

v0.6
resource graph + persistence

v0.7
acquisition plans + decision ledger

v0.8
capability-aware acquisition

v0.9
pluggable acquisition providers
```

The resulting abstraction is:

```
                 RESOURCE
                    │
                    ▼
              REPRESENTATION
                    │
                    ▼
              REQUIREMENTS
                    │
                    ▼
              CAPABILITIES
                    │
                    ▼
                 POLICY
                    │
                    ▼
                  PLAN
                    │
                    ▼
                PROVIDER
                    │
                    ▼
              ACQUISITION
                    │
                    ▼
               OBSERVATION
                    │
                    ▼
              RECOGNITION
                    │
                    ▼
               DISCOVERY
                    │
                    └───────────────┐
                                    │
                                    ▼
                              NEW RESOURCE
```

That is considerably closer to a **generic discovery runtime** than a web crawler.

---
