# Verification

> **Status:** DESIGNED
>
> **Source:** `Continue Architecture Planning.md`
>
> **Purpose:** Verification levels, assurance levels and the claims the architecture states as proved, argued or open.

## Contents

- **v0.16 — 23. Verification** — `Continue Architecture Planning.md` L64514–64555
- **v0.19 — 19.20 Verification Levels** — `Continue Architecture Planning.md` L69183–69220
- **v0.22 — 22.19 Assurance levels** — `Continue Architecture Planning.md` L73665–73697
- **v0.34 — 34.28 What v0.34 Actually Proves** — `Continue Architecture Planning.md` L91800–91800
- **v0.34 — PROVED by the architecture** — `Continue Architecture Planning.md` L91802–91832
- **v0.34 — ARGUMENT** — `Continue Architecture Planning.md` L91834–91836
- **v0.34 — OPEN** — `Continue Architecture Planning.md` L91838–91857

## Related Documents

- [Invariants](invariants.md)
- [Evidence Model](../architecture/evidence-model.md)
- [Coverage, Completeness and Absence](../architecture/coverage-and-absence.md)
- [Prototype Scope and Limitations](../prototype/limitations.md)

---

<!-- source: Continue Architecture Planning.md L64514–64555 | turn 45 | version 0.16 -->
## v0.16 — 23. Verification

v0.16 also introduces a useful distinction:

```
DISCOVERY
```

versus:

```
VERIFICATION
```

Discovery says:

> I found a reference to this resource.

Verification asks:

> Does the resource actually exist and does it match what the evidence suggests?

Example:

```
HTML:
manual.pdf
    ↓
DISCOVERY
    ↓
Candidate
    ↓
GET
    ↓
HTTP 200 + %PDF-
    ↓
VERIFICATION EVIDENCE
```

This produces stronger evidence.

---

<!-- source: Continue Architecture Planning.md L69183–69220 | turn 51 | version 0.19 -->
## v0.19 — 19.20 Verification Levels

We should also avoid a binary:

```
verified / unverified
```

Instead:

```
artifact observed
       ↓
hash computed
       ↓
integrity verified
       ↓
representation recognized
       ↓
semantic classification verified
       ↓
human verified
```

Potential evidence levels:

```
L0 = locator observed
L1 = response observed
L2 = artifact hashed
L3 = representation recognized
L4 = semantic classification supported
L5 = independently verified
```

These are not necessarily universal truth levels; they describe **what evidence exists**.

---

<!-- source: Continue Architecture Planning.md L73665–73697 | turn 57 | version 0.22 -->
## v0.22 — 22.19 Assurance levels

A practical assurance ladder:

```
A0 — NO ASSURANCE
     Nothing meaningful established.

A1 — STRATEGY-RELATIVE
     Exhaustive only relative to one strategy.

A2 — MULTI-STRATEGY
     Multiple independent discovery mechanisms exhausted.

A3 — ENUMERATOR-BOUNDED
     A finite enumerator defines the search universe.

A4 — VERIFIED ENUMERATION
     Enumerator completeness itself has supporting evidence.

A5 — EXTERNALLY VERIFIED
     Independent authoritative evidence confirms completeness.
```

Important:

```
A1 ≠ A3
```

A crawler that followed every link is not equivalent to a verified finite manifest.

---

<!-- source: Continue Architecture Planning.md L91800–91800 | turn 83 | version 0.34 -->
## v0.34 — 34.28 What v0.34 Actually Proves



<!-- source: Continue Architecture Planning.md L91802–91832 | turn 83 | version 0.34 -->
### v0.34 — PROVED by the architecture

```
stale state can be detected
```

through expected versions.

```
stale workers can be fenced
```

through epochs/leases.

```
silent last-write-wins can be avoided
```

through explicit mutation policies.

```
conflicts can become durable objects
```

through ConflictRecord.

```
materialized state can be reconstructed
```

through the event journal.

<!-- source: Continue Architecture Planning.md L91834–91836 | turn 83 | version 0.34 -->
### v0.34 — ARGUMENT

Append-only epistemic structures make concurrent discovery significantly easier to reconcile than mutable shared facts.

<!-- source: Continue Architecture Planning.md L91838–91857 | turn 83 | version 0.34 -->
### v0.34 — OPEN

The userscript still needs a concrete persistence/coordination substrate capable of providing these atomic semantics.

That is a major distinction.

A Tampermonkey prototype using:

```
GM_setValue
localStorage
IndexedDB
BroadcastChannel
```

does **not automatically become a distributed transaction system**.

The v0.34 contracts are therefore stronger than the browser substrate currently available.

---
