# Reconstructed Version Graph

Arrows are evidence-backed `evolved_from` directions. Dotted/unknown relations are not treated as source bases. Repeated semantic versions are preserved as alternatives.

```text
v0.1 composed ───────────────▶ v0.2 composed
v0.1 flattened - - unknown - ▶ v0.2 flattened ─▶ v0.3
                                                   ├─▶ v0.4 variant-a ─▶ v0.5 variant-a
                                                   └─▶ v0.4 variant-b ─▶ v0.5 variant-b ─▶ v0.6 variant-a

v0.5 variant-c (parent ambiguous) ─▶ v0.6 variant-b ─▶ v0.6 variant-c ─▶ v0.7.1

v0.7.0, v0.8 … v0.35: design/pseudocode evidence only; no source snapshot created
```

This graph is not a release graph: all embedded versions share document-level Git commits, tags are absent, and repeated versions are not collapsed.
