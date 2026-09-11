# Review Notes

> **Status:** OPEN
>
> **Source:** `Userscript Discovery Prototype.md`; `Continue Architecture Planning.md`
>
> **Purpose:** Contradictions, ambiguities and documentation defects found during the mechanical split, preserved without resolution.

These notes were produced by the mechanical split described in [Source Map](SOURCE-MAP.md).

Nothing here has been resolved, reconciled or rewritten. Each entry records two (or more)
statements from the source documents, why they appear inconsistent, and the decision that a
human or a later architectural pass must make. Where a statement belongs to the working
prototype, the current design, or a speculative future version, that is stated explicitly
instead of being inferred from tone.

Status vocabulary used below: **CURRENT** (implemented in a prototype artifact),
**DESIGNED** (planned/designed in the conversation), **FUTURE** (explicitly marked as a next
boundary or open problem), **UNVERIFIED** (the sources do not establish the status).

---

## Contradictions

### 1. Prototype version numbering is not monotonic

**Source A** — `Continue Architecture Planning.md`, turn 9 produces a complete **v0.5.0** script,
and turn 17 produces a complete **v0.6.0** script.

**Source B** — `Continue Architecture Planning.md`, turn 11 (after v0.5.0) produces "the
complete **v0.4.0** userscript", and turn 19 (after v0.6.0) produces "the **complete v0.5.0**,
implementing the architecture changes".

**Why they appear inconsistent:** the conversation revisits earlier version numbers instead of
only incrementing them. The artifacts differ, so they are not copies.

**Decision required:** decide whether the artifacts are (a) alternative branches to keep,
(b) abandoned drafts to archive, or (c) a single intended line with mislabelled versions.

**Preserved as:** [prototype/versions/06-v0.5.0.md](prototype/versions/06-v0.5.0.md),
[prototype/versions/07-v0.4.0-second-iteration.md](prototype/versions/07-v0.4.0-second-iteration.md),
[prototype/versions/10-v0.6.0.md](prototype/versions/10-v0.6.0.md),
[prototype/versions/11-v0.5.0-third-iteration.md](prototype/versions/11-v0.5.0-third-iteration.md).
Status of all four artifacts: **CURRENT** (each is a delivered script); relative ordering
**UNVERIFIED**.

---

### 2. The discovery pipeline is described with two different step sets

**Source A** — `Userscript Discovery Prototype.md` L1958–1975, v0.1.0 header comment:

```
candidate
    ↓
observation
    ↓
validation
    ↓
discovery
    ↓
new candidates
    ↓
scheduler
```

**Source B** — `Userscript Discovery Prototype.md` L4715–4805 ("What changed") and every later
version: acquisition and *recognition* replace *validation*: "the acquisition layer produces an
observation, and a protocol/content-specific provider decides whether that observation is
meaningful."

**Why they appear inconsistent:** v0.1.0 has no acquisition object and no provider layer; it
"validates" an observation. From v0.2.0 onward the step is "recognition" performed by a provider.
`Userscript Discovery Prototype.md` §31 "Define the core objects" defines
`Candidate / Observation / LockResult / Discovery` — `LockResult` has no counterpart in the later
object models, and no acquisition object is defined at that point.

**Decision required:** decide whether "validation" and "recognition" are the same step renamed,
two different steps, or a step that changed responsibility; and whether `LockResult` is still a
core object.

**Preserved as:** [concepts/discovery-loop.md](concepts/discovery-loop.md),
[acquisition/response-recognition.md](acquisition/response-recognition.md),
[architecture/system-model.md](architecture/system-model.md).

---

### 3. Candidate claiming: single-thread assumption versus distributed claiming

**Source A** — `Userscript Discovery Prototype.md` L3258–3300 (v0.2.0, `claimNextCandidate`):

> "JavaScript executes this synchronous section without another worker being able to interleave
> an `await` … This prevents two concurrent workers from claiming the same candidate."

**Source B** — `Continue Architecture Planning.md` v0.33 (leases, fencing tokens, heartbeats,
worker death) and v0.34 (optimistic concurrency control, conflict records, fencing). v0.34 §34.28
states as **OPEN**:

> "The userscript still needs a concrete persistence/coordination substrate capable of providing
> these atomic semantics. … A Tampermonkey prototype using `GM_setValue`, `localStorage`,
> `IndexedDB`, `BroadcastChannel` does **not automatically become a distributed transaction
> system**. The v0.34 contracts are therefore stronger than the browser substrate currently
> available."

**Why they appear inconsistent:** the prototype's atomicity argument relies on synchronous
execution in one JavaScript context; the later design requires atomicity across workers, tabs
and storage, which synchronous execution alone does not provide.

**Decision required:** state explicitly what the current prototype actually guarantees, and
whether the v0.33/v0.34 contracts are requirements for the userscript or for a non-browser
runtime.

**Preserved as:** [architecture/concurrency.md](architecture/concurrency.md),
[architecture/coordination.md](architecture/coordination.md),
[validation/verification.md](validation/verification.md),
[prototype/limitations.md](prototype/limitations.md).
Status: prototype behaviour **CURRENT**; v0.33/v0.34 contracts **DESIGNED**; browser substrate
support **OPEN** (as stated by the source).

---

### 4. Resource identity: canonical URL versus identity resolution

**Source A** — `Continue Architecture Planning.md` L23097 (v0.5.0):

> "The important change is that **resource identity is now the canonical URL**, while the _way it
> was discovered_ is provenance."

**Source B** — `Continue Architecture Planning.md` L65431 (v0.17 §4 "Why not simply canonicalize
everything?"):

> "Canonicalization is deterministic string normalization. Identity resolution is an **inference
> problem** … Canonicalization ≠ Identity Resolution. Canonicalization happens first. Identity
> resolution happens afterward."

**Why they appear inconsistent:** v0.5.0 makes the canonical URL *the* resource identity; v0.17
makes canonicalization only the first step of an inference problem.

**Decision required:** decide whether canonical URL is an identity or an identity *input*, and
which statement is current.

**Preserved as:** [architecture/resource-model.md](architecture/resource-model.md),
[prototype/userscript.md](prototype/userscript.md).

---

### 5. Coverage: metric of choice, but qualified later

**Source A** — `Userscript Discovery Prototype.md` §19:

> "Coverage is a better metric than elapsed time."

**Source B** — `Continue Architecture Planning.md` v0.22 §22.14 "Coverage cannot necessarily be
monotonically interpreted" (a later session can reduce measured coverage when the universe is
revised), and v0.28 §28.24 "Candidate count is not coverage":
"unique candidates = 100 doesn't establish coverage = 100%".

**Why they appear inconsistent:** not necessarily a contradiction, but the later sections qualify
"coverage" heavily enough that the earlier claim cannot be read unqualified.

**Decision required:** define what "coverage" means before it is used as the primary success
metric.

**Preserved as:** [architecture/coverage-and-absence.md](architecture/coverage-and-absence.md),
[concepts/discovery-loop.md](concepts/discovery-loop.md).

---

### 6. Confidence: one score versus no single global score

**Source A** — `Userscript Discovery Prototype.md` §10 "Confidence rather than binary decisions",
and the `Discovery` object in §31 carrying a single `confidence` field.

**Source B** — `Continue Architecture Planning.md` v0.18 §18.12 "Do Not Use One Global Confidence
Score":

> "Avoid `confidence: 0.93` as the sole representation of classification certainty."

with a structured assertion (`confidence`, `evidenceIds`, `classifier`, `classifierVersion`,
`status`, `contradictions`).

**Why they appear inconsistent:** a single numeric confidence field versus an explicit prohibition
on a single global confidence score.

**Decision required:** decide whether discovery confidence and classification confidence are
different objects, and whether `Discovery.confidence` is superseded.

**Preserved as:** [architecture/discovery-model.md](architecture/discovery-model.md),
[architecture/classification.md](architecture/classification.md).

---

### 7. Resource → artifact model revised

**Source A** — `Continue Architecture Planning.md` v0.17 models resources with content
fingerprints and revisions (§§10, 24).

**Source B** — `Continue Architecture Planning.md` v0.19 §19.2 "Why Resource → Artifact Is Wrong":

> "A tempting model is `resource.fingerprint = sha256(bytes);`. That creates several problems."

**Why they appear inconsistent:** v0.19 explicitly rejects a modelling shortcut that v0.17 uses.
This is an explicit revision rather than an outright contradiction.

**Decision required:** mark the v0.17 resource model as superseded (or not) once the intended
target version is chosen.

**Preserved as:** [architecture/resource-model.md](architecture/resource-model.md).

---

### 8. Replay: decisions deterministic, network not

**Source A** — `Continue Architecture Planning.md` v0.7.1 is titled "Replayable Acquisition
Decisions + Deterministic Event Ledger", and the v0.7.1 script header states:

> "Decision replay is supported. Network replay is NOT guaranteed."

**Source B** — v0.7.1 §6 "One remaining architectural limitation" asks for two explicit modes
(`REPLAY MODE`, `ACQUISITION MODE`) to avoid "treating an acquisition log as though it were a
deterministic execution trace".

**Why they appear inconsistent:** not a contradiction, but the term "replayable" is scoped to
decisions while the surrounding language can be read as full replay. The source itself flags the
ambiguity.

**Decision required:** keep the decision/network replay distinction explicit wherever "replay" is
used.

**Preserved as:** [prototype/versions/14-v0.7.1.md](prototype/versions/14-v0.7.1.md),
[architecture/provenance.md](architecture/provenance.md),
[prototype/limitations.md](prototype/limitations.md).

---

### 9. Termination models

**Source A** — `Userscript Discovery Prototype.md` §18 lists four termination modes: exhaustive
scan, confidence-based scan, time-bounded scan, hybrid.

**Source B** — `Continue Architecture Planning.md` v0.14 §11 enumerates eight termination
conditions (frontier exhaustion, candidate limit, acquisition limit, discovery-task limit,
proposal limit, depth limit, time limit, external stop) and §13 states "Limit reached ≠
successful completion".

**Why they appear inconsistent:** different taxonomies of termination, at different layers
(scan-level versus session-level).

**Decision required:** decide whether the four scan modes and the eight session limits are two
layers of one model or competing models.

**Preserved as:** [concepts/discovery-loop.md](concepts/discovery-loop.md),
[architecture/sessions-and-domains.md](architecture/sessions-and-domains.md).

---

### 10. Knowledge store naming

**Source A** — `Userscript Discovery Prototype.md` §14 "Discovery database", and the prototype
class `KnowledgeBase` holding candidates, observations and discoveries.

**Source B** — `Continue Architecture Planning.md` v0.6: "candidates are no longer the resource
database"; v0.14 §18 "Scan vs engine knowledge" separates domain knowledge from session
knowledge.

**Why they appear inconsistent:** the store is variously a database, a knowledge base, a
resource graph and a domain/session pair.

**Decision required:** fix the vocabulary, or state explicitly that these are different objects.

**Preserved as:** [architecture/system-model.md](architecture/system-model.md),
[architecture/sessions-and-domains.md](architecture/sessions-and-domains.md),
[prototype/userscript.md](prototype/userscript.md).

---

### 11. Same-origin default versus cross-origin capability

**Source A** — prototype configuration keeps `sameOriginOnly: true`, described as "deliberately
conservative … That prevents this generic scanner from turning every discovered third-party URL
into an unrestricted cross-origin crawler."

**Source B** — the same scripts request `@connect *` and `GM_xmlhttpRequest` (cross-origin
capability), and v0.6.0 adds per-origin budgets and origin controllers, which only matter if
multiple origins are in play.

**Why they appear inconsistent:** not a contradiction, but the safety boundary is a default
setting rather than an enforced constraint.

**Decision required:** decide whether same-origin is a policy default or an invariant.

**Preserved as:** [prototype/configuration.md](prototype/configuration.md),
[prototype/limitations.md](prototype/limitations.md),
[acquisition/runtime.md](acquisition/runtime.md).

---

## Documentation defects in the source documents

These are defects of the source documents themselves. They are preserved, not repaired, except
where the Markdown structure was broken (see [Source Map](SOURCE-MAP.md)).

1. **Flattened code paste.** `Continue Architecture Planning.md` L3–16 contains the v0.1.0 and
   v0.2.0 userscripts with all internal line breaks and backticks lost (two lines of 22,001 and
   34,769 characters). The same two scripts are preserved with full formatting in
   `Userscript Discovery Prototype.md`. Both copies are retained:
   [prototype/versions/00-v0.1.0-and-v0.2.0-paste.md](prototype/versions/00-v0.1.0-and-v0.2.0-paste.md)
   (flattened) and
   [prototype/versions/01-v0.1.0.md](prototype/versions/01-v0.1.0.md) /
   [prototype/versions/02-v0.2.0.md](prototype/versions/02-v0.2.0.md) (formatted).
2. **Mangled match pattern.** `Userscript Discovery Prototype.md` L1947 and L3052 read
   `// @match _://_/*`, while the same scripts pasted into `Continue Architecture Planning.md`
   read `// @match *://*/*`. One of the two exports has replaced `*` with `_`. This affects
   installability of the pasted script and must be corrected by hand in any future code pass.
3. **Broken code fences.** Both userscript blocks in `Userscript Discovery Prototype.md` open a
   fence part-way through the userscript header and close it before the final `})();`. The split
   moved the fence boundaries to the real start and end of each block; the code text itself is
   unchanged.
4. **Export artifacts.** A stray `::` sequence follows `})();` in several script exports, and the
   final user prompt reads "Conclued". Both are treated as conversation/export artifacts.
5. **Conversation markers.** 44 turns consist only of "Continue" / "Conclude" / "Conclued". They
   are removed and recorded as `ARTIFACT` in [Source Map](SOURCE-MAP.md).

---

## Content that could not be classified unambiguously

1. **Version-scoped grouping.** From v0.8 onward, most sections of a version were kept together
   in that version's topic document (for example all of v0.27 in
   [architecture/strategy-and-planning.md](architecture/strategy-and-planning.md)), while for
   v0.7, v0.13–v0.17 sections were routed individually by topic. This is a navigation decision
   made by the split, not a statement about the architecture; the per-section mapping in
   [Source Map](SOURCE-MAP.md) is authoritative either way.
2. **Status of individual prototype artifacts.** Every complete script is tagged **CURRENT**
   because each was delivered as a working script. The sources never state which artifacts were
   abandoned, so relative status is **UNVERIFIED**.
3. **`archive/` copies.** The two original documents are retained verbatim under
   [`archive/`](../archive/) and are therefore the only place where the defects listed above can
   still be inspected in their original context.

---

## Related Documents

- [Source Map](SOURCE-MAP.md)
- [Documentation index](README.md)
- [Prototype Overview](prototype/overview.md)
- [Architecture Overview](architecture/overview.md)
- [Future Work](roadmap/future-work.md)
