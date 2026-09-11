# Review Notes

> **Status:** OPEN
>
> **Source:** `Userscript Discovery Prototype.md`; `Continue Architecture Planning.md`
>
> **Purpose:** Unresolved issues recorded during the mechanical split. Nothing here has been resolved, reconciled or rewritten.

Identifiers (`C-nn`, `D-nn`) are referenced from [Source Map](SOURCE-MAP.md) and from the generated documents.

## Contradictions

### C-01 — Prototype version numbering is not monotonic

**Source A** — turn 9 and turn 17 of `Continue Architecture Planning.md` produce complete **v0.5.0** and **v0.6.0** scripts.  
> // @version      0.5.0 … // @version      0.6.0

**Source B** — turn 11 produces "the complete **v0.4.0** userscript" and turn 19 produces "the **complete v0.5.0**, implementing the architecture changes".  
> // @version      0.4.0 … // @version      0.5.0

**Why they appear inconsistent:** The conversation revisits earlier version numbers instead of only incrementing them; the artifacts differ, so they are not copies.

**Required decision:** Decide whether the artifacts are alternative branches to keep, abandoned drafts to archive, or one intended line with mislabelled versions.

**Sections:** `CAP-013`, `CAP-016`, `CAP-024`, `CAP-027`

### C-02 — The discovery pipeline is described with two different step sets

**Source A** — v0.1.0 header comment  
> candidate ↓ observation ↓ validation ↓ discovery ↓ new candidates ↓ scheduler

**Source B** — "What changed" (v0.2.0) and every later version  
> the acquisition layer produces an observation, and a protocol/content-specific provider decides whether that observation is meaningful

**Why they appear inconsistent:** v0.1.0 has no acquisition object and no provider layer; it *validates* an observation. From v0.2.0 onward the step is *recognition* performed by a provider. Section 31 "Define the core objects" defines `LockResult`, which has no counterpart in the later object models.

**Required decision:** Decide whether validation and recognition are the same step renamed, two different steps, or a step that changed responsibility; and whether `LockResult` is still a core object.

**Sections:** `USP-053`, `USP-010`

### C-03 — Candidate claiming: single-thread assumption versus distributed claiming

**Source A** — v0.2.0 `claimNextCandidate`  
> JavaScript executes this synchronous section without another worker being able to interleave an `await` … This prevents two concurrent workers from claiming the same candidate.

**Source B** — v0.33 (leases, fencing, heartbeats) and v0.34 (optimistic concurrency)  
> The userscript still needs a concrete persistence/coordination substrate capable of providing these atomic semantics. … A Tampermonkey prototype using `GM_setValue`, `localStorage`, `IndexedDB`, `BroadcastChannel` does **not automatically become a distributed transaction system**.

**Why they appear inconsistent:** The prototype argument relies on synchronous execution in one JavaScript context; the later design requires atomicity across workers, tabs and storage.

**Required decision:** State explicitly what the current prototype guarantees, and whether the v0.33/v0.34 contracts target the userscript or a non-browser runtime.

**Sections:** `CAP-1084`, `CAP-1085`, `CAP-1121`, `CAP-1157`

### C-04 — Resource identity: canonical URL versus identity resolution

**Source A** — v0.5.0 architecture note  
> resource identity is now the canonical URL, while the _way it was discovered_ is provenance

**Source B** — v0.17 §4 "Why not simply canonicalize everything?"  
> Canonicalization is deterministic string normalization. Identity resolution is an **inference problem**. … Canonicalization ≠ Identity Resolution.

**Why they appear inconsistent:** v0.5.0 makes the canonical URL the resource identity; v0.17 demotes canonicalization to the first step of an inference problem.

**Required decision:** Decide whether the canonical URL is an identity or an identity input.

**Sections:** `CAP-022`, `CAP-376`

### C-05 — Coverage: preferred metric, later heavily qualified

**Source A** — §19 "Coverage is a better metric than elapsed time"  
> Coverage is a better metric than elapsed time.

**Source B** — v0.22 §22.14 and v0.28 §28.24  
> Coverage cannot necessarily be monotonically interpreted … unique candidates = 100 doesn't establish coverage = 100%

**Why they appear inconsistent:** The later sections qualify coverage enough that the earlier claim cannot be read unqualified.

**Required decision:** Define "coverage" before using it as the primary success metric.

**Sections:** `USP-034`, `CAP-615`, `CAP-894`

### C-06 — Confidence: one score versus no single global score

**Source A** — §10 and the `Discovery` object (§31)  
> Confidence rather than binary decisions … `confidence` field on `Discovery`

**Source B** — v0.18 §18.12  
> Avoid `confidence: 0.93` as the sole representation of classification certainty.

**Why they appear inconsistent:** A single numeric confidence field versus an explicit prohibition on a single global confidence score.

**Required decision:** Decide whether discovery confidence and classification confidence are different objects, and whether `Discovery.confidence` is superseded.

**Sections:** `USP-019`, `CAP-436`

### C-07 — Resource → artifact model revised

**Source A** — v0.17 (fingerprints and revisions on the resource)  
> resource.fingerprint = sha256(bytes);

**Source B** — v0.19 §19.2  
> Why Resource → Artifact Is Wrong

**Why they appear inconsistent:** v0.19 explicitly rejects a modelling shortcut that v0.17 uses. An explicit revision rather than an outright contradiction.

**Required decision:** Mark the v0.17 resource model as superseded (or not) once the target version is chosen.

**Sections:** `CAP-329`, `CAP-465`

### C-08 — Replay: decisions deterministic, network not

**Source A** — v0.7.1 title and script header  
> Decision replay is supported. Network replay is NOT guaranteed.

**Source B** — v0.7.1 §6  
> treating an acquisition log as though it were a deterministic execution trace

**Why they appear inconsistent:** The word "replayable" is scoped to decisions while surrounding language can be read as full replay; the source itself flags the ambiguity.

**Required decision:** Keep the decision/network replay distinction explicit wherever "replay" is used.

**Sections:** `CAP-052`

### C-09 — Two termination taxonomies

**Source A** — §18 "Termination"  
> Exhaustive scan / Confidence-based scan / Time-bounded scan / Hybrid

**Source B** — v0.14 §§11–13  
> frontier exhaustion, candidate limit, acquisition limit, discovery-task limit, proposal limit, depth limit, time limit, external stop … Limit reached ≠ successful completion

**Why they appear inconsistent:** Different taxonomies at different layers (scan-level versus session-level).

**Required decision:** Decide whether the four scan modes and the eight session limits are two layers of one model or competing models.

**Sections:** `USP-029`, `CAP-237`, `CAP-247`

### C-10 — Knowledge store naming

**Source A** — §14 "Discovery database" and the `KnowledgeBase` class  
> Discovery database … class KnowledgeBase

**Source B** — v0.6 change note and v0.14 §18  
> candidates are no longer the resource database … Scan vs engine knowledge

**Why they appear inconsistent:** The store is variously a database, a knowledge base, a resource graph and a domain/session pair.

**Required decision:** Fix the vocabulary, or state explicitly that these are different objects.

**Sections:** `USP-023`, `CAP-252`

### C-11 — Same-origin default versus cross-origin capability

**Source A** — prototype configuration (`sameOriginOnly: true`)  
> sameOriginOnly: true … deliberately conservative

**Source B** — the same scripts (`@connect *`, `GM_xmlhttpRequest`) and v0.6 per-origin budgets  
> @connect      *

**Why they appear inconsistent:** The safety boundary is a default setting, not an enforced constraint.

**Required decision:** Decide whether same-origin is a policy default or an invariant.

**Sections:** `CAP-115`, `CAP-476`

## Ambiguous Sections

Sections whose assignment involved judgement rather than a mechanical rule. None of them were discarded.

| Sections | Ambiguity | Resolution applied |
| --- | --- | --- |
| all `prototype/versions/04-v0.4.0-plan.md`, `prototype/versions/08-v0.5.0-plan.md` sections | A plan is future work at the time it was written, but a later artifact implements it | status `FUTURE`, with the delivered sibling artifact linked from the version index |
| all sections of v0.8 and later versions | One version can cover several topics; per-section routing would scatter it | kept with the version's own topic document, cross-referenced from the topic indexes |
| `prototype/versions/01-v0.1.0.md`, `prototype/versions/02-v0.2.0.md`, `prototype/versions/00-v0.1.0-and-v0.2.0-paste.md` | near-duplicate with conflicting bytes | both kept, difference recorded (see [Duplicates](#duplicates-and-near-duplicates)) |
| the 44 conversation-marker turns | no classifiable content | disposition `ARCHIVE`, retained in the archived source documents |

## Unverified Claims

Claims that exist in the sources but that repository evidence does not establish.

1. **No implementation files exist in this repository.** The repository contains only the two planning documents (now under `archive/`) and the documentation tree. Under specification section 8, `CURRENT` means *verified in repository implementation*, so **no section is classified `CURRENT`**: all 36 prototype sections that the sources present as the delivered userscript are classified `UNVERIFIED`, with the source’s claim recorded in the section note and in the file header of every document under `prototype/`. The prototype/design distinction is carried by the destination directory (`prototype/` versus `architecture/`, `acquisition/`, `providers/`) instead of by the status field, so that no unsupported implementation claim is introduced.
2. **Claim-atomicity claim** (`C-03`): “JavaScript executes this synchronous section without another worker being able to interleave an `await`” is asserted by the prototype comment; no test or implementation file in this repository verifies it.
3. **Substrate claim** (`C-03`): v0.34 §34.28 itself declares the required persistence/coordination substrate `OPEN`.
4. **Prototype capability claims** listed in the root `README.md` (concurrent acquisition, provenance, deduplication, persistence, export) are documented as implemented by the userscript, but no userscript file is present in the repository to verify them against.

## Orphaned Material

None. Every extracted section has a destination, a category and a status; the accounting check reports **0 unaccounted** sections. The only content not carried into the tree is the 44 conversation continuation markers, recorded with disposition `ARCHIVE` in [Source Map](SOURCE-MAP.md) and preserved in the archived source documents.

## Duplicates and near-duplicates

Handled per specification sections 12–13. Full record in [Source Map → Duplicates](SOURCE-MAP.md#duplicates).

| | Sections | Content |
| --- | --- | --- |
| A | `USP-065`, `USP-066`, `USP-069`, `USP-070` | v0.1.0 and v0.2.0 with line breaks and indentation intact |
| B | `CAP-001` | the same two scripts, flattened into single lines, with the undamaged `@match *://*/*` directive |
| A ∩ B | — | the script bodies |
| A − B | — | line breaks, indentation |
| B − A | — | `*://*/*` versus `_://_/*` in the `@match` directive |

Both copies are kept because they express conflicting bytes for the same script (specification section 13: “If conflicting: KEEP BOTH + FLAG CONFLICT”). The unique information of each copy is recorded in the destination files themselves and here; nothing was deleted on the assumption that one copy is obsolete.

## Source Document Defects

Defects of the source documents, preserved rather than repaired (except for Markdown fence boundaries, which are structural).

| ID | Defect | Document | Detail |
| --- | --- | --- | --- |
| D-01 | Flattened code paste | `Continue Architecture Planning.md` | `Continue Architecture Planning.md` L3–16 contains the v0.1.0 and v0.2.0 userscripts with all internal line breaks and backticks lost (lines of 22,001 and 34,769 characters). Preserved verbatim in `prototype/versions/00-v0.1.0-and-v0.2.0-paste.md`. |
| D-02 | Mangled match pattern | `Userscript Discovery Prototype.md` | `Userscript Discovery Prototype.md` L1947 and L3052 read `// @match _://_/*`; the same scripts pasted into `Continue Architecture Planning.md` read `// @match *://*/*`. One export replaced `*` with `_`. This affects installability of the pasted script. |
| D-03 | Broken code fences | `Userscript Discovery Prototype.md` | Both userscript blocks in `Userscript Discovery Prototype.md` open a fence part-way through the userscript header and close it before the final `})();`. The split moved the fence boundaries to the real start and end of each block; the code text itself is unchanged. |
| D-04 | Export artifacts | `Userscript Discovery Prototype.md` | A stray `::` sequence follows `})();` in several script exports, and the final user prompt reads "Conclued". Both are treated as conversational/export artifacts. |
| D-05 | Conversation markers | both | 44 turns consist only of "Continue" / "Conclude" / "Conclued". They are removed from the tree and recorded with disposition `ARCHIVE` in [Source Map](SOURCE-MAP.md). |

## Classification Decisions

Decisions taken by the split that a later pass may revisit.

1. **Extended destination tree.** The canonical map in specification section 10 is used as the spine; every canonical file exists and owns its concept. Eleven additional topic documents were created because the source contains ~2.36 MB of design material and collapsing it into the canonical files would produce single documents of several hundred kilobytes (for example `architecture/system-model.md` would absorb 20 version architectures). The additional files are: `architecture/capability-model.md`, `resource-model.md`, `evidence-model.md`, `classification.md`, `search-space.md`, `strategy-and-planning.md`, `goal-and-query.md`, `coverage-and-absence.md`, `sessions-and-domains.md`, `work-and-frontier.md`, `resource-budget.md`, `persistence-and-recovery.md`, `coordination.md`, `acquisition/runtime.md`, `providers/candidate-sources.md`, `validation/failure-taxonomy.md`, `prototype/configuration.md` (the prototype configuration block has no home in the canonical map) and `prototype/versions/*` for the complete script artifacts. No canonical ownership from section 11 was moved into them — every concept in the ownership table still lives in its canonical file.
2. **Version-scoped grouping.** For v0.8 and later, a version's sections stay with that version's topic document; for v0.7 and v0.13–v0.17 sections are routed individually by topic. This is a navigation decision only.
3. **Script artifacts are not split.** Each complete userscript stays in one file (`prototype/versions/`), because a code block must not be split across files (specification section 6).
4. **Provider code extracts.** `providers/html.md`, `json.md`, `text.md` and `prototype/configuration.md` contain reference extracts of code that also appears in `prototype/versions/14-v0.7.1.md`. The extracts are labelled as extracts and link to the complete artifact.
5. **Heading prefix.** Sections from `Continue Architecture Planning.md` carry a `v0.nn — ` prefix; recorded per section in [Source Map → Section records](SOURCE-MAP.md#section-records).
6. **Status convention** (specification section 8). `DESIGNED` = intentional architecture/specification; `FUTURE` = explicitly proposed next work; `OPEN` = the source itself marks the question unresolved; `UNVERIFIED` = a claim the repository cannot verify, or no claim at all. `CURRENT` is **not used**: it is defined as *verified in repository implementation*, and this repository contains no implementation files. Prototype material therefore lands in `prototype/` (destination semantics: what the sources say exists today) with status `UNVERIFIED` plus an explicit note, which keeps the prototype/design separation of specification section 25 without asserting an implementation that cannot be checked.

## Possible Future Refactoring

Suggestions for the subsequent architecture-verification phase. **None of these were performed by this split.**

1. Resolve `C-01`…`C-11`, starting with `C-01` (version numbering) because it determines which artifact is authoritative.
2. Repair the source-document defects `D-01`…`D-04` in a code pass, in particular the `// @match _://_/*` mangling, which makes the pasted script uninstallable.
3. Decide the canonical implementation target: extract one userscript into a real source file, or declare the prototype documentation-only.
4. Normalize the vocabulary identified in `C-02` and `C-10` (validation/recognition, database/knowledge base/resource graph).
5. Split `validation/invariants.md` by owning subsystem once the target version is chosen; today it is a chronological invariant register.
6. Promote the version artifacts to dated, individually named files if the version numbering question (`C-01`) is resolved.

## Related Documents

- [Source Map](SOURCE-MAP.md)
- [Split Manifest](SPLIT-MANIFEST.yaml)
- [Documentation index](README.md)
- [Prototype Overview](prototype/overview.md)
- [Architecture Overview](architecture/overview.md)
- [Future Work](roadmap/future-work.md)

