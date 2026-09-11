# Scheduling

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`; `Userscript Discovery Prototype.md`
>
> **Purpose:** Scheduling: priority, retry and backoff, fairness, aging, starvation and arbitration decisions.

## Contents

- **11. Don't immediately discard failed candidates** — `Userscript Discovery Prototype.md` L573–615
- **12. Adaptive retry** — `Userscript Discovery Prototype.md` L617–646
- **13. Scheduling becomes important** — `Userscript Discovery Prototype.md` L648–676
- **39. A practical scheduler** — `Userscript Discovery Prototype.md` L1802–1829
- **v0.13 — 2. Two schedulers, not one** — `Continue Architecture Planning.md` L59548–59596
- **v0.13 — 10. Source scheduling** — `Continue Architecture Planning.md` L59914–59948
- **v0.13 — 11. Fairness** — `Continue Architecture Planning.md` L59950–59994
- **v0.15 — 11. WorkScheduler** — `Continue Architecture Planning.md` L62530–62568
- **v0.15 — 12. Priority starvation** — `Continue Architecture Planning.md` L62570–62597
- **v0.15 — 13. Priority aging** — `Continue Architecture Planning.md` L62599–62640
- **v0.15 — 27. Scheduled work** — `Continue Architecture Planning.md` L63182–63219

## Related Documents

- [Work Items and Frontier Arbitration](work-and-frontier.md)
- [Candidate Model](candidate-model.md)
- [Concurrency](concurrency.md)
- [Resource and Cost Ledger](resource-budget.md)

---

<!-- source: Userscript Discovery Prototype.md L573–615 | turn 5 | version ? -->
## 11. Don't immediately discard failed candidates

A failed demodulation attempt can mean several things:

```
Candidate
   │
   ├── wrong frequency
   ├── wrong bandwidth
   ├── wrong symbol rate
   ├── wrong modulation
   ├── wrong delivery system
   ├── insufficient signal
   └── valid signal but acquisition timeout
```

Those failures have different meanings.

Therefore record the reason:

```
AttemptResult {
    candidate
    elapsed_time
    signal_present
    lock_state
    failure_reason
}
```

This allows the scheduler to make better decisions.

For example, repeated:

```
signal_present = true
carrier_lock = true
FEC_lock = false
```

suggests that the frequency is probably interesting, but the current physical-layer hypothesis is wrong.

---

<!-- source: Userscript Discovery Prototype.md L617–646 | turn 5 | version ? -->
## 12. Adaptive retry

The scanner can then expand locally:

```
candidate failed
       │
       ▼
Was there RF energy?
       │
   ┌───┴───┐
   no      yes
   │        │
   ▼        ▼
discard   generate neighboring hypotheses
```

For example, conceptually:

```
failed symbol-rate hypothesis
        │
        ├── test nearby SR values
        ├── test alternative modulation
        └── test alternative DVB mode
```

This is better than globally trying every combination.

---

<!-- source: Userscript Discovery Prototype.md L648–676 | turn 5 | version ? -->
## 13. Scheduling becomes important

You can give every pending candidate a priority:

$$priority(c) = P(\text{valid}\mid c) \times value(c) \div cost(c)$$

Where:

* **probability** = how likely the candidate is to contain a valid multiplex
* **value** = how useful discovering it is
* **cost** = expected acquisition time

A candidate learned from an NIT would normally receive a much higher probability than an arbitrary point in the spectrum.

So your queues might look like:

```
Priority queue

1. NIT-derived candidate
2. Previously successful neighboring frequency
3. Strong RF candidate
4. Weak RF candidate
5. Uncharacterized spectrum
```

This turns blind scanning into an **active search algorithm**.

---

<!-- source: Userscript Discovery Prototype.md L1802–1829 | turn 11 | version ? -->
## 39. A practical scheduler

The scheduler can maintain three collections:

```
READY
    candidates eligible for acquisition

DEFERRED
    candidates worth testing later

DONE
    candidates sufficiently investigated
```

And each candidate has a priority:

```
priority =
    discovery_probability
    × information_value
    × freshness
    ÷ acquisition_cost
```

That gives you a principled way to choose the next candidate.

---

<!-- source: Continue Architecture Planning.md L59548–59596 | turn 39 | version 0.13 -->
## v0.13 — 2. Two schedulers, not one

This is an important distinction.

The system now has:

```
Discovery Scheduler
    ↓
Which source should inspect evidence?

Acquisition Scheduler
    ↓
Which candidate should be acquired?
```

They operate at different levels.

```
                    DISCOVERY LOOP

Observation
    ↓
Evidence
    ↓
Source Scheduler
    ↓
CandidateSource
    ↓
Proposal
    ↓
Candidate
    │
    └───────────────┐
                    ▼
             Acquisition Loop
```

Therefore:

```
source priority ≠ candidate priority
```

A high-priority source can produce low-priority candidates.

A low-priority source can produce an extremely valuable candidate.

---

<!-- source: Continue Architecture Planning.md L59914–59948 | turn 39 | version 0.13 -->
## v0.13 — 10. Source scheduling

The scheduler can score tasks:

```
score(task)
 =
 sourcePriority
 + evidenceConfidence
 + parentPriority
 - depthPenalty
 - retryPenalty
```

For example:

```JavaScript
function discoveryTaskPriority(task, source) {
    const meta = source.describe();

    return (
        (meta.priority || 0) +
        task.priority -
        task.depth * 0.05
    );
}
```

The exact scoring function should remain configurable.

The important architectural point is:

> **Discovery scheduling is a policy decision, not an accidental consequence of JavaScript callback order.**

---

<!-- source: Continue Architecture Planning.md L59950–59994 | turn 39 | version 0.13 -->
## v0.13 — 11. Fairness

Pure priority scheduling has a failure mode:

```
high-priority source
        ↓
always produces tasks
        ↓
low-priority source
        ↓
never executes
```

That is starvation.

A simple solution is aging:

```
effectivePriority =
    basePriority
    + ageBonus
```

So:

```
task A: priority 0.90, waiting 0s
task B: priority 0.50, waiting 30s
```

eventually B receives execution time.

Another option is weighted round-robin:

```
HTML       4
Network    3
Sitemap    2
Metadata   1
```

The controller can later support both.

---

<!-- source: Continue Architecture Planning.md L62530–62568 | turn 43 | version 0.15 -->
## v0.15 — 11. WorkScheduler

The scheduler can now operate over the common envelope.

```JavaScript
class WorkScheduler {
    constructor() {
        this.items = new Map();
    }

    enqueue(work) {
        this.items.set(work.id, work);
        return work;
    }

    eligible(nowValue = now()) {
        return [...this.items.values()]
            .filter(work =>
                work.status === 'queued' &&
                (
                    work.nextAttemptAt === null ||
                    work.nextAttemptAt <= nowValue
                )
            );
    }

    next(nowValue = now()) {
        return this.eligible(nowValue)
            .sort(
                (a, b) =>
                    b.priority - a.priority
            )[0] || null;
    }
}
```

But a pure priority queue introduces a problem.

---

<!-- source: Continue Architecture Planning.md L62570–62597 | turn 43 | version 0.15 -->
## v0.15 — 12. Priority starvation

Suppose:

```
Discovery A     priority 0.2
Discovery B     priority 0.2
Discovery C     priority 0.2
...
```

and new high-priority work continuously appears:

```
0.99
0.98
0.97
0.96
...
```

The low-priority work may never execute.

Therefore:

> Priority must not become starvation.

---

<!-- source: Continue Architecture Planning.md L62599–62640 | turn 43 | version 0.15 -->
## v0.15 — 13. Priority aging

One solution:

```
effectivePriority
    =
basePriority
+
agingFactor × waitingTime
```

For example:

```JavaScript
effectivePriority(work, currentTime) {
    const waiting =
        Math.max(
            0,
            currentTime -
            (work.queuedAt || work.createdAt)
        );

    return (
        work.priority +
        waiting * 0.0001
    );
}
```

The exact coefficient should be configuration, not hardcoded architecture.

Another option is weighted round-robin.

The important contract:

```
A continuously arriving higher-priority stream
must not make lower-priority work permanently unreachable.
```

---

<!-- source: Continue Architecture Planning.md L63182–63219 | turn 43 | version 0.15 -->
## v0.15 — 27. Scheduled work

Retries introduce another state:

```
DELAYED
```

Example:

```
attempt failed
      ↓
retry scheduled
      ↓
DELAYED
      ↓
nextAttemptAt
      ↓
QUEUED
```

Therefore the complete operational state is:

```
BLOCKED
QUEUED
CLAIMED
RUNNING
DELAYED
COMPLETED
FAILED
CANCELLED
```

This is much more expressive than the original candidate lifecycle.

---
