# Domains, Sessions and Termination

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Discovery domains, scan sessions, seeds, session lifecycle and termination conditions.

## Contents

- **v0.14 — DiscoveryDomain + ScanSession** — `Continue Architecture Planning.md` L60556–60588
- **v0.14 — 1. The conceptual split** — `Continue Architecture Planning.md` L60590–60610
- **v0.14 — DiscoveryDomain** — `Continue Architecture Planning.md` L60629–60633
- **v0.14 — ScanSession** — `Continue Architecture Planning.md` L60635–60647
- **v0.14 — 3. DiscoveryDomain** — `Continue Architecture Planning.md` L60691–60748
- **v0.14 — 4. Domain vs policy** — `Continue Architecture Planning.md` L60750–60798
- **v0.14 — 5. Domain membership** — `Continue Architecture Planning.md` L60800–60878
- **v0.14 — 6. Explicit seeds** — `Continue Architecture Planning.md` L60880–60932
- **v0.14 — 7. Seed ≠ Candidate** — `Continue Architecture Planning.md` L60934–60972
- **v0.14 — 9. ScanSession** — `Continue Architecture Planning.md` L61039–61102
- **v0.14 — 10. Session lifecycle** — `Continue Architecture Planning.md` L61104–61147
- **v0.14 — 11. Termination becomes explicit** — `Continue Architecture Planning.md` L61149–61153
- **v0.14 — Frontier exhaustion** — `Continue Architecture Planning.md` L61155–61165
- **v0.14 — Candidate limit** — `Continue Architecture Planning.md` L61167–61171
- **v0.14 — Acquisition limit** — `Continue Architecture Planning.md` L61173–61177
- **v0.14 — Discovery-task limit** — `Continue Architecture Planning.md` L61179–61183
- **v0.14 — Proposal limit** — `Continue Architecture Planning.md` L61185–61189
- **v0.14 — Depth limit** — `Continue Architecture Planning.md` L61191–61195
- **v0.14 — Time limit** — `Continue Architecture Planning.md` L61197–61201
- **v0.14 — External stop** — `Continue Architecture Planning.md` L61203–61209
- **v0.14 — 12. Termination evaluator** — `Continue Architecture Planning.md` L61211–61265
- **v0.14 — 13. Limit reached ≠ successful completion** — `Continue Architecture Planning.md` L61267–61306
- **v0.14 — 14. The session snapshot** — `Continue Architecture Planning.md` L61308–61352
- **v0.14 — 15. Resumability** — `Continue Architecture Planning.md` L61354–61413
- **v0.14 — 17. Session ownership** — `Continue Architecture Planning.md` L61463–61501
- **v0.14 — 18. Scan vs engine knowledge** — `Continue Architecture Planning.md` L61503–61557
- **v0.14 — 19. Domain snapshot vs mutable domain** — `Continue Architecture Planning.md` L61559–61615
- **v0.14 — 20. Domain identity** — `Continue Architecture Planning.md` L61617–61666
- **v0.14 — 21. Search frontier vs knowledge graph** — `Continue Architecture Planning.md` L61668–61695
- **v0.14 — 23. Four distinct scopes** — `Continue Architecture Planning.md` L61774–61787
- **v0.14 — 26. What v0.14 changes conceptually** — `Continue Architecture Planning.md` L61886–61918

## Related Documents

- [Search Space](search-space.md)
- [Persistence and Crash Recovery](persistence-and-recovery.md)
- [Work Items and Frontier Arbitration](work-and-frontier.md)
- [System Model](system-model.md)

---

<!-- source: Continue Architecture Planning.md L60556–60588 | turn 41 | version 0.14 -->
## v0.14 — DiscoveryDomain + ScanSession

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

<!-- source: Continue Architecture Planning.md L60590–60610 | turn 41 | version 0.14 -->
## v0.14 — 1. The conceptual split

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

<!-- source: Continue Architecture Planning.md L60629–60633 | turn 41 | version 0.14 -->
### v0.14 — DiscoveryDomain

The domain defines:

> **Where and what are we allowed to search?**

<!-- source: Continue Architecture Planning.md L60635–60647 | turn 41 | version 0.14 -->
### v0.14 — ScanSession

The session defines:

> **What particular execution of that domain are we currently performing?**

Therefore:

```
Engine ≠ Domain ≠ Session
```

---

<!-- source: Continue Architecture Planning.md L60691–60748 | turn 41 | version 0.14 -->
## v0.14 — 3. DiscoveryDomain

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

<!-- source: Continue Architecture Planning.md L60750–60798 | turn 41 | version 0.14 -->
## v0.14 — 4. Domain vs policy

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

<!-- source: Continue Architecture Planning.md L60800–60878 | turn 41 | version 0.14 -->
## v0.14 — 5. Domain membership

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

<!-- source: Continue Architecture Planning.md L60880–60932 | turn 41 | version 0.14 -->
## v0.14 — 6. Explicit seeds

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

<!-- source: Continue Architecture Planning.md L60934–60972 | turn 41 | version 0.14 -->
## v0.14 — 7. Seed ≠ Candidate

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

<!-- source: Continue Architecture Planning.md L61039–61102 | turn 41 | version 0.14 -->
## v0.14 — 9. ScanSession

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

<!-- source: Continue Architecture Planning.md L61104–61147 | turn 41 | version 0.14 -->
## v0.14 — 10. Session lifecycle

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

<!-- source: Continue Architecture Planning.md L61149–61153 | turn 41 | version 0.14 -->
## v0.14 — 11. Termination becomes explicit

A blind scan needs a stopping rule.

The generic engine should therefore support several termination conditions.

<!-- source: Continue Architecture Planning.md L61155–61165 | turn 41 | version 0.14 -->
### v0.14 — Frontier exhaustion

```
no queued discovery tasks
AND
no queued acquisition candidates
AND
no active operations
```

This is the natural completion condition.

<!-- source: Continue Architecture Planning.md L61167–61171 | turn 41 | version 0.14 -->
### v0.14 — Candidate limit

```
candidateCount >= maxCandidates
```

<!-- source: Continue Architecture Planning.md L61173–61177 | turn 41 | version 0.14 -->
### v0.14 — Acquisition limit

```
acquisitionCount >= maxAcquisitions
```

<!-- source: Continue Architecture Planning.md L61179–61183 | turn 41 | version 0.14 -->
### v0.14 — Discovery-task limit

```
discoveryTaskCount >= maxDiscoveryTasks
```

<!-- source: Continue Architecture Planning.md L61185–61189 | turn 41 | version 0.14 -->
### v0.14 — Proposal limit

```
proposalCount >= maxProposals
```

<!-- source: Continue Architecture Planning.md L61191–61195 | turn 41 | version 0.14 -->
### v0.14 — Depth limit

```
candidate.depth > maxDepth
```

<!-- source: Continue Architecture Planning.md L61197–61201 | turn 41 | version 0.14 -->
### v0.14 — Time limit

```
elapsed >= maxDuration
```

<!-- source: Continue Architecture Planning.md L61203–61209 | turn 41 | version 0.14 -->
### v0.14 — External stop

```
user → Stop
```

---

<!-- source: Continue Architecture Planning.md L61211–61265 | turn 41 | version 0.14 -->
## v0.14 — 12. Termination evaluator

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

<!-- source: Continue Architecture Planning.md L61267–61306 | turn 41 | version 0.14 -->
## v0.14 — 13. Limit reached ≠ successful completion

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

<!-- source: Continue Architecture Planning.md L61308–61352 | turn 41 | version 0.14 -->
## v0.14 — 14. The session snapshot

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

<!-- source: Continue Architecture Planning.md L61354–61413 | turn 41 | version 0.14 -->
## v0.14 — 15. Resumability

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

<!-- source: Continue Architecture Planning.md L61463–61501 | turn 41 | version 0.14 -->
## v0.14 — 17. Session ownership

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

<!-- source: Continue Architecture Planning.md L61503–61557 | turn 41 | version 0.14 -->
## v0.14 — 18. Scan vs engine knowledge

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

<!-- source: Continue Architecture Planning.md L61559–61615 | turn 41 | version 0.14 -->
## v0.14 — 19. Domain snapshot vs mutable domain

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

<!-- source: Continue Architecture Planning.md L61617–61666 | turn 41 | version 0.14 -->
## v0.14 — 20. Domain identity

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

<!-- source: Continue Architecture Planning.md L61668–61695 | turn 41 | version 0.14 -->
## v0.14 — 21. Search frontier vs knowledge graph

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

<!-- source: Continue Architecture Planning.md L61774–61787 | turn 41 | version 0.14 -->
## v0.14 — 23. Four distinct scopes

At this point the architecture has four clean scopes:

| Scope | Question | Owner |
| --- | --- | --- |
| Engine | How does discovery work? | Engine |
| Domain | What may be searched? | DiscoveryDomain |
| Session | What scan is running? | ScanSession |
| Resource | What have we learned? | KnowledgeBase |

This is a significant architectural boundary.

---

<!-- source: Continue Architecture Planning.md L61886–61918 | turn 41 | version 0.14 -->
## v0.14 — 26. What v0.14 changes conceptually

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
