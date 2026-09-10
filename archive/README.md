# Archive

These files are the unedited source material of the project: two conversation
transcripts, copied without modification.

| File | Content | Line count |
| --- | --- | --- |
| `Userscript Discovery Prototype.md` | 41 numbered design notes: DVB blind scan as a generic algorithm, candidate generation, coarse-to-fine search, confidence, retry, scheduling, the discovery database, provenance, the first userscript pastes (v0.1.0, v0.2.0) | 4,805 |
| `Continue Architecture Planning.md` | the full design and implementation log: complete userscripts v0.3.0 … v0.7.1, then the design series v0.8 … v0.35 and the final formulation | 92,274 |

## Status: non-normative

Nothing in this directory is a specification, and nothing here describes what the
code does. The transcripts contain:

* abandoned designs and superseded implementations;
* conversational filler and repeated "Continue" sections;
* design material presented as if implemented;
* at least one syntactically invalid script version (v0.5.0 paste at lines
  18378–23093).

**Canonical material lives elsewhere:**

| Need | Read instead |
| --- | --- |
| What exists, verified | `README.md`, `docs/prototype/userscript.md` |
| Architecture of the current system | `docs/architecture/` |
| Scope and non-goals | `docs/prototype/scope.md` |
| Known defects | `docs/prototype/limitations.md` |
| DVB analogy and its boundary | `docs/research/dvb-blind-scan-inspiration.md` |
| Designed future layers | `docs/roadmap/future-architecture.md` |
| Terminology | `docs/glossary.md` |

## Why keep them

The design series is the only record of the reasoning behind decisions that are
not visible in the code — why recognition is separate from acquisition, why
candidates are hypotheses, why coverage requires its own object. Removing it
would make several current design choices unexplainable. It is archived rather
than deleted so that:

1. design claims in `docs/roadmap/` can be traced back to their source;
2. the evolution of the prototype (v0.3.0 → v0.7.1) remains auditable;
3. rejected alternatives stay available for review.

## Extracting code from the archive

The userscript versions are fenced blocks whose lines are separated by blank
lines in the transcript. The extraction that produced
`prototype/generic-discovery-engine.user.js` is described in
`docs/prototype/userscript.md`.
