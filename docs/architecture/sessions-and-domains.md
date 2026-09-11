# Domains, Sessions and Termination

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Discovery domains, scan sessions, seeds, session lifecycle and termination conditions.

## Source Sections

- **v0.14 — DiscoveryDomain + ScanSession** — `CAP-223` — `Continue Architecture Planning.md` L60556–60588
- **v0.14 — 1. The conceptual split** — `CAP-224` — `Continue Architecture Planning.md` L60590–60610
- **v0.14 — DiscoveryDomain** — `CAP-226` — `Continue Architecture Planning.md` L60629–60633
- **v0.14 — ScanSession** — `CAP-227` — `Continue Architecture Planning.md` L60635–60647
- **v0.14 — 3. DiscoveryDomain** — `CAP-229` — `Continue Architecture Planning.md` L60691–60748
- **v0.14 — 4. Domain vs policy** — `CAP-230` — `Continue Architecture Planning.md` L60750–60798
- **v0.14 — 5. Domain membership** — `CAP-231` — `Continue Architecture Planning.md` L60800–60878
- **v0.14 — 6. Explicit seeds** — `CAP-232` — `Continue Architecture Planning.md` L60880–60932
- **v0.14 — 7. Seed ≠ Candidate** — `CAP-233` — `Continue Architecture Planning.md` L60934–60972
- **v0.14 — 9. ScanSession** — `CAP-235` — `Continue Architecture Planning.md` L61039–61102
- **v0.14 — 10. Session lifecycle** — `CAP-236` — `Continue Architecture Planning.md` L61104–61147
- **v0.14 — 11. Termination becomes explicit** — `CAP-237` — `Continue Architecture Planning.md` L61149–61153
- **v0.14 — Frontier exhaustion** — `CAP-238` — `Continue Architecture Planning.md` L61155–61165
- **v0.14 — Candidate limit** — `CAP-239` — `Continue Architecture Planning.md` L61167–61171
- **v0.14 — Acquisition limit** — `CAP-240` — `Continue Architecture Planning.md` L61173–61177
- **v0.14 — Discovery-task limit** — `CAP-241` — `Continue Architecture Planning.md` L61179–61183
- **v0.14 — Proposal limit** — `CAP-242` — `Continue Architecture Planning.md` L61185–61189
- **v0.14 — Depth limit** — `CAP-243` — `Continue Architecture Planning.md` L61191–61195
- **v0.14 — Time limit** — `CAP-244` — `Continue Architecture Planning.md` L61197–61201
- **v0.14 — External stop** — `CAP-245` — `Continue Architecture Planning.md` L61203–61209
- **v0.14 — 12. Termination evaluator** — `CAP-246` — `Continue Architecture Planning.md` L61211–61265
- **v0.14 — 13. Limit reached ≠ successful completion** — `CAP-247` — `Continue Architecture Planning.md` L61267–61306
- **v0.14 — 14. The session snapshot** — `CAP-248` — `Continue Architecture Planning.md` L61308–61352
- **v0.14 — 15. Resumability** — `CAP-249` — `Continue Architecture Planning.md` L61354–61413
- **v0.14 — 17. Session ownership** — `CAP-251` — `Continue Architecture Planning.md` L61463–61501
- **v0.14 — 18. Scan vs engine knowledge** — `CAP-252` — `Continue Architecture Planning.md` L61503–61557
- **v0.14 — 19. Domain snapshot vs mutable domain** — `CAP-253` — `Continue Architecture Planning.md` L61559–61615
- **v0.14 — 20. Domain identity** — `CAP-254` — `Continue Architecture Planning.md` L61617–61666
- **v0.14 — 21. Search frontier vs knowledge graph** — `CAP-255` — `Continue Architecture Planning.md` L61668–61695
- **v0.14 — 23. Four distinct scopes** — `CAP-257` — `Continue Architecture Planning.md` L61774–61787
- **v0.14 — 26. What v0.14 changes conceptually** — `CAP-269` — `Continue Architecture Planning.md` L61886–61918

## Related Documents

- [Search Space](search-space.md)
- [Persistence and Crash Recovery](persistence-and-recovery.md)
- [Work Items and Frontier Arbitration](work-and-frontier.md)
- [System Model](system-model.md)

---

<!-- CAP-223 | Continue Architecture Planning.md L60556–60588 | turn 41 | version 0.14 -->
## v0.14 — DiscoveryDomain + ScanSession

> **Source sections:** `CAP-223`

The missing abstraction is the **search space**.

Up to v0.13, the engine has increasingly well-defined components:

```
CandidateSource
       ↓
DiscoveryController
       ↓
Candidate
       ↓
AcquisitionPlan
       ↓
AcquisitionRuntime
       ↓
Observation
       ↓
RecognitionRuntime
       ↓
Evidence
       ↓
CandidateSource
```

But there is still no explicit answer to:

> **What exactly is this scan allowed to explore, and when is this particular scan finished?**

That is what `DiscoveryDomain` and `ScanSession` establish.

---

<!-- CAP-224 | Continue Architecture Planning.md L60590–60610 | turn 41 | version 0.14 -->
## v0.14 — 1. The conceptual split

> **Source sections:** `CAP-224`

There are now three different things:

```
DISCOVERY ENGINE
    │
    │ reusable machinery
    ▼
DISCOVERY DOMAIN
    │
    │ defines the search space
    ▼
SCAN SESSION
    │
    │ executes one bounded exploration
    ▼
RESULTS / EVIDENCE / LEDGER
```

This distinction is important.

<!-- CAP-226 | Continue Architecture Planning.md L60629–60633 | turn 41 | version 0.14 -->
### v0.14 — DiscoveryDomain

> **Source sections:** `CAP-226`

The domain defines:

> **Where and what are we allowed to search?**

<!-- CAP-227 | Continue Architecture Planning.md L60635–60647 | turn 41 | version 0.14 -->
### v0.14 — ScanSession

> **Source sections:** `CAP-227`

The session defines:

> **What particular execution of that domain are we currently performing?**

Therefore:

```
Engine ≠ Domain ≠ Session
```

---

<!-- CAP-229 | Continue Architecture Planning.md L60691–60748 | turn 41 | version 0.14 -->
## v0.14 — 3. DiscoveryDomain

> **Source sections:** `CAP-229`

A first conceptual model:

```JavaScript
class DiscoveryDomain {
    constructor(data = {}) {
        this.id = data.id || makeId('domain');

        this.schemes =
            data.schemes || ['https'];

        this.origins =
            data.origins || [];

        this.resourceTypes =
            data.resourceTypes || [];

        this.seeds =
            data.seeds || [];

        this.sources =
            data.sources || [];

        this.maxDepth =
            data.maxDepth ?? 5;

        this.budgets = {
            maxCandidates:
                data.budgets?.maxCandidates ?? 750,

            maxDiscoveryTasks:
                data.budgets?.maxDiscoveryTasks ?? 1000,

            maxProposals:
                data.budgets?.maxProposals ?? 2000,

            maxAcquisitions:
                data.budgets?.maxAcquisitions ?? 150
        };

        this.policy =
            data.policy || {};

        this.termination =
            data.termination || {};

        this.createdAt =
            data.createdAt || now();
    }
}
```

But this should **not** become a giant configuration object.

The domain should answer only questions about the search space.

---

<!-- CAP-230 | Continue Architecture Planning.md L60750–60798 | turn 41 | version 0.14 -->
## v0.14 — 4. Domain vs policy

> **Source sections:** `CAP-230`
>
> [DOCUMENTATION REVIEW] Contradiction **C-11** ([Review Notes](../REVIEW-NOTES.md#c-11--))

This distinction matters.

Consider:

```
https://example.com/manual.pdf
```

The domain may say:

```
origin allowed
scheme allowed
type allowed
```

The acquisition policy may say:

```
GET allowed
binary response allowed
```

The runtime may then say:

```
provider available
budget available
origin slot available
```

So:

```
DOMAIN
"What belongs to the search universe?"

POLICY
"What is authorized?"

RUNTIME
"What can execute right now?"
```

These must not collapse into one mechanism.

---

<!-- CAP-231 | Continue Architecture Planning.md L60800–60878 | turn 41 | version 0.14 -->
## v0.14 — 5. Domain membership

> **Source sections:** `CAP-231`

A domain needs an explicit predicate:

```JavaScript
domain.contains(candidate)
```

Conceptually:

```
contains(candidate)
    │
    ├── scheme allowed?
    ├── origin allowed?
    ├── resource type allowed?
    ├── depth allowed?
    └── domain-specific constraints?
```

Example:

```JavaScript
contains(candidate) {
    const url = new URL(candidate.target);

    if (!this.schemes.includes(url.protocol.replace(':', ''))) {
        return false;
    }

    if (
        this.origins.length &&
        !this.origins.includes(url.origin)
    ) {
        return false;
    }

    if (
        this.resourceTypes.length &&
        !this.resourceTypes.includes(candidate.type)
    ) {
        return false;
    }

    if (candidate.depth > this.maxDepth) {
        return false;
    }

    return true;
}
```

This is more fundamental than `sameOriginOnly`.

`sameOriginOnly` is a policy/configuration convenience.

A domain can express:

```
example.com only
```

or:

```
example.com
docs.example.com
cdn.example.com
```

or potentially:

```
all HTTPS origins discovered from a seed
```

without changing the engine itself.

---

<!-- CAP-232 | Continue Architecture Planning.md L60880–60932 | turn 41 | version 0.14 -->
## v0.14 — 6. Explicit seeds

> **Source sections:** `CAP-232`

The domain should have explicit seeds.

For example:

```JavaScript
const domain = new DiscoveryDomain({
    schemes: ['https'],

    origins: [
        'https://example.com'
    ],

    seeds: [
        {
            target: 'https://example.com/',
            type: 'page'
        },

        {
            target: 'https://example.com/robots.txt',
            type: 'robots'
        }
    ]
});
```

This is better than implicitly assuming:

```
location.href
```

is always the scan seed.

The userscript may still provide:

```
Current Page
```

as a convenient seed source.

But that becomes:

```
User Seed Source
```

rather than a hidden assumption inside the engine.

---

<!-- CAP-233 | Continue Architecture Planning.md L60934–60972 | turn 41 | version 0.14 -->
## v0.14 — 7. Seed ≠ Candidate

> **Source sections:** `CAP-233`

This distinction should remain explicit.

```
Seed
  ↓
CandidateProposal
  ↓
CandidateNormalizer
  ↓
Candidate
```

A seed is an instruction to initialize the search frontier.

A candidate is an entity in the discovery graph.

Therefore:

```
seed
    ≠
candidate
```

A seed can also be rejected:

```
Seed
 ↓
Domain validation
 ↓
Rejected
```

without creating a candidate.

---

<!-- CAP-235 | Continue Architecture Planning.md L61039–61102 | turn 41 | version 0.14 -->
## v0.14 — 9. ScanSession

> **Source sections:** `CAP-235`

A session represents one execution.

```JavaScript
class ScanSession {
    constructor(domain) {
        this.id = makeId('scan');

        this.domainId =
            domain.id;

        this.status =
            'created';

        this.startedAt =
            null;

        this.completedAt =
            null;

        this.reason =
            null;

        this.stats = {
            seeds: 0,
            candidates: 0,
            discoveries: 0,
            acquisitions: 0,
            observations: 0,
            recognitions: 0,
            errors: 0
        };

        this.createdAt =
            now();
    }
}
```

Possible lifecycle:

```
CREATED
   ↓
INITIALIZING
   ↓
RUNNING
   ↓
DRAINING
   ↓
COMPLETED
```

With alternate terminal states:

```
STOPPED
LIMIT_REACHED
FAILED
CANCELLED
```

---

<!-- CAP-236 | Continue Architecture Planning.md L61104–61147 | turn 41 | version 0.14 -->
## v0.14 — 10. Session lifecycle

> **Source sections:** `CAP-236`

A more precise state machine:

```
                    ┌───────────────┐
                    │    CREATED    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ INITIALIZING  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
              ┌────▶│    RUNNING    │◀─────┐
              │     └───────┬───────┘      │
              │             │              │
              │             ▼              │
              │     ┌───────────────┐      │
              │     │    DRAINING   │──────┘
              │     └───────┬───────┘
              │             │
              │             ▼
              │     ┌───────────────┐
              └─────│   COMPLETED   │
                    └───────────────┘

RUNNING ──→ STOPPED
RUNNING ──→ CANCELLED
RUNNING ──→ FAILED
RUNNING ──→ LIMIT_REACHED
```

`DRAINING` is useful.

It means:

> No new work will be admitted, but already-running operations are allowed to settle.

This addresses one of the weaknesses in the earlier `Stop` implementation.

---

<!-- CAP-237 | Continue Architecture Planning.md L61149–61153 | turn 41 | version 0.14 -->
## v0.14 — 11. Termination becomes explicit

> **Source sections:** `CAP-237`
>
> [DOCUMENTATION REVIEW] Contradiction **C-09** ([Review Notes](../REVIEW-NOTES.md#c-09--))

A blind scan needs a stopping rule.

The generic engine should therefore support several termination conditions.

<!-- CAP-238 | Continue Architecture Planning.md L61155–61165 | turn 41 | version 0.14 -->
### v0.14 — Frontier exhaustion

> **Source sections:** `CAP-238`
>
> **Note:** explicit override

```
no queued discovery tasks
AND
no queued acquisition candidates
AND
no active operations
```

This is the natural completion condition.

<!-- CAP-239 | Continue Architecture Planning.md L61167–61171 | turn 41 | version 0.14 -->
### v0.14 — Candidate limit

> **Source sections:** `CAP-239`
>
> **Note:** explicit override

```
candidateCount >= maxCandidates
```

<!-- CAP-240 | Continue Architecture Planning.md L61173–61177 | turn 41 | version 0.14 -->
### v0.14 — Acquisition limit

> **Source sections:** `CAP-240`
>
> **Note:** explicit override

```
acquisitionCount >= maxAcquisitions
```

<!-- CAP-241 | Continue Architecture Planning.md L61179–61183 | turn 41 | version 0.14 -->
### v0.14 — Discovery-task limit

> **Source sections:** `CAP-241`
>
> **Note:** explicit override

```
discoveryTaskCount >= maxDiscoveryTasks
```

<!-- CAP-242 | Continue Architecture Planning.md L61185–61189 | turn 41 | version 0.14 -->
### v0.14 — Proposal limit

> **Source sections:** `CAP-242`

```
proposalCount >= maxProposals
```

<!-- CAP-243 | Continue Architecture Planning.md L61191–61195 | turn 41 | version 0.14 -->
### v0.14 — Depth limit

> **Source sections:** `CAP-243`

```
candidate.depth > maxDepth
```

<!-- CAP-244 | Continue Architecture Planning.md L61197–61201 | turn 41 | version 0.14 -->
### v0.14 — Time limit

> **Source sections:** `CAP-244`

```
elapsed >= maxDuration
```

<!-- CAP-245 | Continue Architecture Planning.md L61203–61209 | turn 41 | version 0.14 -->
### v0.14 — External stop

> **Source sections:** `CAP-245`

```
user → Stop
```

---

<!-- CAP-246 | Continue Architecture Planning.md L61211–61265 | turn 41 | version 0.14 -->
## v0.14 — 12. Termination evaluator

> **Source sections:** `CAP-246`
>
> [DOCUMENTATION REVIEW] Contradiction **C-09** ([Review Notes](../REVIEW-NOTES.md#c-09--))

Instead of scattering termination checks throughout the code:

```JavaScript
class TerminationController {
    constructor(domain, session) {
        this.domain = domain;
        this.session = session;
    }

    evaluate(state) {
        const limits =
            this.domain.budgets;

        if (
            state.candidates >=
            limits.maxCandidates
        ) {
            return {
                terminate: true,
                reason: 'candidate-limit'
            };
        }

        if (
            state.acquisitions >=
            limits.maxAcquisitions
        ) {
            return {
                terminate: true,
                reason: 'acquisition-limit'
            };
        }

        if (
            state.discoveryTasks >=
            limits.maxDiscoveryTasks
        ) {
            return {
                terminate: true,
                reason: 'discovery-task-limit'
            };
        }

        return {
            terminate: false
        };
    }
}
```

But there is a subtle issue.

---

<!-- CAP-247 | Continue Architecture Planning.md L61267–61306 | turn 41 | version 0.14 -->
## v0.14 — 13. Limit reached ≠ successful completion

> **Source sections:** `CAP-247`

This distinction should be preserved.

```
FRONTIER EXHAUSTED
        ↓
COMPLETED
```

means:

> The bounded search space was exhausted.

Whereas:

```
CANDIDATE LIMIT
        ↓
LIMIT_REACHED
```

means:

> The scan was deliberately truncated.

Those are not equivalent.

A result should therefore expose:

```JavaScript
{
    status: 'limit-reached',
    reason: 'candidate-limit'
}
```

rather than pretending the scan completed naturally.

---

<!-- CAP-248 | Continue Architecture Planning.md L61308–61352 | turn 41 | version 0.14 -->
## v0.14 — 14. The session snapshot

> **Source sections:** `CAP-248`

A session should have a reproducible state snapshot.

For example:

```JavaScript
{
    sessionId: 'scan-...',
    domainId: 'domain-...',

    status: 'running',

    startedAt: 1757500000000,

    frontier: {
        discoveryQueued: 12,
        discoveryRunning: 2,
        acquisitionQueued: 43,
        acquisitionRunning: 3
    },

    counters: {
        candidates: 181,
        proposals: 427,
        discoveryTasks: 198,
        acquisitions: 104,
        observations: 101
    },

    budgets: {
        candidatesRemaining: 569,
        acquisitionsRemaining: 46
    },

    termination: {
        terminate: false,
        reason: null
    }
}
```

This becomes the basis for resumability.

---

<!-- CAP-249 | Continue Architecture Planning.md L61354–61413 | turn 41 | version 0.14 -->
## v0.14 — 15. Resumability

> **Source sections:** `CAP-249`

This is where `ScanSession` becomes substantially more useful than simply having a `running` boolean.

A session should be persistable.

Conceptually:

```
ScanSession
├── domain snapshot
├── scheduler state
├── discovery frontier
├── acquisition frontier
├── budgets
├── counters
├── knowledge graph
└── event ledger
```

Then:

```
SAVE
 ↓
CLOSE TAB
 ↓
RELOAD
 ↓
RESTORE SESSION
 ↓
RECONSTRUCT FRONTIERS
 ↓
CONTINUE
```

But there is an important design constraint:

> Do not persist transient "running" claims as if they were still active.

For example:

```
CLAIMED
RUNNING
```

at the moment the browser disappears cannot safely be assumed to still be executing.

On recovery:

```
RUNNING
   ↓
RECOVERY
   ↓
REQUEUE OR ABANDON
```

---

<!-- CAP-251 | Continue Architecture Planning.md L61463–61501 | turn 41 | version 0.14 -->
## v0.14 — 17. Session ownership

> **Source sections:** `CAP-251`

The session becomes the top-level execution identity.

```
ScanSession
     │
     ├── DiscoveryTask
     │
     ├── Candidate
     │
     ├── AcquisitionPlan
     │
     ├── Attempt
     │
     ├── Observation
     │
     └── Event
```

Every major event can carry:

```JavaScript
{
    sessionId,
    domainId,
    ...
}
```

This allows the event ledger to answer:

> What happened during this particular scan?

rather than merely:

> What has this engine ever seen?

---

<!-- CAP-252 | Continue Architecture Planning.md L61503–61557 | turn 41 | version 0.14 -->
## v0.14 — 18. Scan vs engine knowledge

> **Source sections:** `CAP-252`
>
> [DOCUMENTATION REVIEW] Contradiction **C-10** ([Review Notes](../REVIEW-NOTES.md#c-10--))

This produces another important distinction.

The KnowledgeBase may contain information from multiple scans.

```
KNOWLEDGE BASE
├── Scan A
├── Scan B
├── Scan C
└── Scan D
```

A candidate might have:

```JavaScript
candidate.discoverySessions = [
    'scan-001',
    'scan-017'
];
```

Likewise:

```
Observation
   ↓
sessionId
```

and:

```
Discovery
   ↓
sessionId
```

The underlying resource identity remains global.

The observation is session-specific.

This allows:

```
Resource
  ├── discovered in Scan A
  ├── observed in Scan B
  └── changed in Scan C
```

That becomes extremely useful for revision detection later.

---

<!-- CAP-253 | Continue Architecture Planning.md L61559–61615 | turn 41 | version 0.14 -->
## v0.14 — 19. Domain snapshot vs mutable domain

> **Source sections:** `CAP-253`

A subtle but important rule:

A running session should not silently change underneath itself.

Bad:

```
Session A
   ↓
Domain
   ↓
user modifies domain
   ↓
Session A behaves differently
```

Better:

```
Domain Definition
       ↓
Session Initialization
       ↓
Domain Snapshot
       ↓
Session
```

So:

```JavaScript
session.domainSnapshot = deepFreeze(
    domain.serialize()
);
```

Conceptually:

> **A scan is reproducible against the domain definition it started with.**

If the user changes the domain:

```
Domain v1
    ↓
Scan A

Domain v2
    ↓
Scan B
```

rather than mutating Scan A.

---

<!-- CAP-254 | Continue Architecture Planning.md L61617–61666 | turn 41 | version 0.14 -->
## v0.14 — 20. Domain identity

> **Source sections:** `CAP-254`
>
> [DOCUMENTATION REVIEW] Contradiction **C-04** ([Review Notes](../REVIEW-NOTES.md#c-04--))

A useful next step is deterministic domain identity.

Instead of:

```
domain-123
```

only, calculate:

```
DomainDefinition
       ↓
canonical serialization
       ↓
hash
       ↓
domain fingerprint
```

For example:

```JavaScript
{
    schemes: ['https'],
    origins: ['https://example.com'],
    resourceTypes: ['page', 'document'],
    maxDepth: 5,
    sources: ['html-link', 'robots', 'sitemap']
}
```

could produce:

```
domainFingerprint = SHA-256(...)
```

Now a session can state:

```
domainId: domain-123
domainFingerprint: 9c8...
```

This is much stronger for reproducibility.

---

<!-- CAP-255 | Continue Architecture Planning.md L61668–61695 | turn 41 | version 0.14 -->
## v0.14 — 21. Search frontier vs knowledge graph

> **Source sections:** `CAP-255`
>
> [DOCUMENTATION REVIEW] Contradiction **C-10** ([Review Notes](../REVIEW-NOTES.md#c-10--))

Do not confuse them.

```
KNOWLEDGE GRAPH
"What do we know?"

FRONTIER
"What remains to explore?"
```

A candidate can remain in the graph forever while no longer being frontier work.

For example:

```
Candidate
status = completed
```

doesn't mean it disappears.

It remains evidence.

The frontier contains only active work.

---

<!-- CAP-257 | Continue Architecture Planning.md L61774–61787 | turn 41 | version 0.14 -->
## v0.14 — 23. Four distinct scopes

> **Source sections:** `CAP-257`

At this point the architecture has four clean scopes:

| Scope | Question | Owner |
| --- | --- | --- |
| Engine | How does discovery work? | Engine |
| Domain | What may be searched? | DiscoveryDomain |
| Session | What scan is running? | ScanSession |
| Resource | What have we learned? | KnowledgeBase |

This is a significant architectural boundary.

---

<!-- CAP-269 | Continue Architecture Planning.md L61886–61918 | turn 41 | version 0.14 -->
## v0.14 — 26. What v0.14 changes conceptually

> **Source sections:** `CAP-269`

Before:

```
Current page
    ↓
discover things
    ↓
keep scanning
```

After:

```
Domain
  ↓
Session
  ↓
Initialize frontier
  ↓
Explore bounded search space
  ↓
Terminate explicitly
  ↓
Persist result
```

This is the point where the project stops being merely a sophisticated userscript crawler.

It becomes a **bounded generic discovery runtime**.

---
