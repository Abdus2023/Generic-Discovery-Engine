# Provider and Acquisition Evolution

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

| Snapshot | Version | Variant | Providers / recognizers | Acquisition coupling |
|---|---|---|---|---|
| snapshot-0001 | v0.1.0 | mechanically-composed | HtmlRecognizer | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0003 | v0.2.0 | mechanically-composed | HtmlProvider, JsonProvider, ResponseProvider, TextProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0005 | v0.3.0 | only-evidenced-complete-occurrence | HtmlProvider, JsonProvider, ResponseProvider, TextProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0006 | v0.4.0 | variant-a | HtmlProvider, JsonProvider, ManifestProvider, ResponseProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0008 | v0.4.0 | variant-b | CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0007 | v0.5.0 | variant-a | ApiDescriptionProvider, HtmlProvider, JsonProvider, ManifestProvider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0009 | v0.5.0 | variant-b | CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, RobotsProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0011 | v0.5.0 | variant-c | BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0010 | v0.6.0 | variant-a | BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, RobotsProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0012 | v0.6.0 | variant-b | BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0013 | v0.6.0 | variant-c | BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, ResponseProvider, RobotsProvider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |
| snapshot-0014 | v0.7.1 | only-evidenced-complete-occurrence | BinaryProvider, CssProvider, HtmlProvider, JavaScriptProvider, JsonProvider, Provider, TextProvider, XmlProvider | Web URL + GM/fetch/HTTP-shaped |

## Interpretation

- v0.1.0 uses a concrete `HtmlRecognizer`; it demonstrates separable recognition but not the later reusable provider family.
- v0.2.0 introduces multiple response provider occurrences. Later versions broaden media/protocol recognition names. Names do not prove lineage.
- v0.4-v0.6 alternatives diverge in provider sets and failure handling; no canonical branch is selected.
- v0.7.1 makes policy/plan/decision structures explicit. Provider ownership and candidate expansion must be interpreted per occurrence, not assumed stable.
- Error-containment mechanisms (whole-item catches and, where directly evidenced, narrower catches or settled aggregation) improve continuation behavior, but neither complete provider isolation nor integrity is guaranteed.
- Historical acquisition remains HTTP/browser/userscript coupled. Current protocol-independent acquisition is a separate target.
