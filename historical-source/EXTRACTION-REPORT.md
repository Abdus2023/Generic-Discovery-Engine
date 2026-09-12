# Historical Source Extraction Report

## Completion

**HISTORICAL SOURCE EXTRACTION COMPLETE**

This is an evidence-preserving extraction. It does not modernize, repair, merge, or execute historical source.

## Documents examined

- `Userscript Discovery Prototype.md`
- `Continue Architecture Planning.md`
- Exact renamed archive copies and archive-banner revisions on fetched remote branches

Historical document blob revisions examined: **4**  
Code-bearing revisions: **4**  
Git revision events affecting these documents: **3**  
Tags found: **0**

Unchanged commit/path occurrences (including an exact rename to `archive/` on another branch) are mapped to their content-addressed blob revision. They are not miscounted as new byte revisions; their paths and commits remain in provenance.

## Artifacts

Original extracted artifacts: **5644**  
Reconstructed artifacts: **2**

- Userscripts: **28**
- Engines: **56**
- Models: **274**
- Providers: **312**
- Schedulers: **100**
- Acquisition: **126**
- Concurrency-bearing artifacts (overlapping category): **486**
- UI: **14**
- Tests: **0**
- Configurations: **26**
- Schemas: **0**
- Patches/diffs: **0**
- Pseudocode-classified: **4650**
- Fragments: **26**

## Userscript versions

The original (non-banner) document revisions contain 14 userscript representations. Archive-banner revisions retain another 14 exact code copies. Explicit version labels and distinct represented-byte variants in the original revisions:

- `v0.1.0`: 2 byte-distinct representation(s)
- `v0.2.0`: 2 byte-distinct representation(s)
- `v0.3.0`: 1 byte-distinct representation(s)
- `v0.4.0`: 2 byte-distinct representation(s)
- `v0.5.0`: 3 byte-distinct representation(s)
- `v0.6.0`: 3 byte-distinct representation(s)
- `v0.7.1`: 1 byte-distinct representation(s)

The v0.4.0, v0.5.0, and v0.6.0 labels each occur on multiple byte-distinct scripts. They are not merged.

### Chronological source-position index

| Order | Version | Source | Artifact | Classification | Bytes | SHA-256 |
|---:|---|---|---|---|---:|---|
| 103 | `0.1.0` | Userscript Discovery Prototype.md:1942 | `art-5ff41289b5f1c428` | `PARTIAL_IMPLEMENTATION` | 23425 | `6cc3c2b1b9e092c874f1d3ffe11fa46201f332476cd87353b49c6293fc655d21` |
| 117 | `0.2.0` | Userscript Discovery Prototype.md:3047 | `art-b7850a391eddeb86` | `PARTIAL_IMPLEMENTATION` | 36880 | `3d350c6ff67ee21b0b4c5b1cca25d8869da3d73288b7631d3bf688cab1c50bac` |
| 140 | `0.1.0` | Continue Architecture Planning.md:3 | `art-f14be66e164996ad` | `PARTIAL_IMPLEMENTATION` | 22412 | `1a00b194b86a3bf86b4ff90680f6858bb00b15b3a90d856613e17cbc58c1648f` |
| 141 | `0.2.0` | Continue Architecture Planning.md:11 | `art-e69de36ddbc7cb3b` | `PARTIAL_IMPLEMENTATION` | 35214 | `4f1a849896f318a16b7614f5f572f1cd830ed03f7dc41d42e462f8d865956df4` |
| 142 | `0.3.0` | Continue Architecture Planning.md:53 | `art-44eb3694339abdcb` | `IMPLEMENTED` | 70490 | `f52fccf69f9d89c5d4269de784479657e1c2baaca3d1ff5d7d4b07887ad156e3` |
| 161 | `0.4.0` | Continue Architecture Planning.md:2792 | `art-deb961ea9f622d3a` | `IMPLEMENTED` | 112382 | `9239a85bf7e040427adf93d4380d9ed28ceaf908b36201c7ca171150f94256b8` |
| 181 | `0.5.0` | Continue Architecture Planning.md:7178 | `art-2c6f74909f301798` | `IMPLEMENTED` | 164144 | `a55a835ef0b1274db71e4019616b8ac8b12f67a3b96d050e42bc3d8eca9ed0ab` |
| 203 | `0.4.0` | Continue Architecture Planning.md:13487 | `art-c19ebb3956fba19c` | `IMPLEMENTED` | 129500 | `c60c3278d160ed1ba6e8b4254d26cab291a3df64a4e986234cfc1fa7f897b783` |
| 229 | `0.5.0` | Continue Architecture Planning.md:18379 | `art-fbebfdf9a3874c18` | `IMPLEMENTED` | 127904 | `f71b190c334069da6e4ae82a8e8d27383826b5e333de4ca3cb1f72de19d9b1cd` |
| 251 | `0.6.0` | Continue Architecture Planning.md:23141 | `art-b1368ed9b372a6a6` | `IMPLEMENTED` | 168304 | `3a3aa26747ff5105ce52578133e8c8932edb2ec0c54246853ea0b8938ba3118c` |
| 276 | `0.5.0` | Continue Architecture Planning.md:29439 | `art-f019277e6c28e8f5` | `IMPLEMENTED` | 160026 | `644e9cf006441cf81e407e47f4b37b8ff12d91a65e738595de5eabadee6ec390` |
| 302 | `0.6.0` | Continue Architecture Planning.md:34755 | `art-3680c60f0bc39673` | `IMPLEMENTED` | 226645 | `414ad2bfc4df241d85b20367a4c8764187155f9cfdf8daacd5fb7e773477eed1` |
| 330 | `0.6.0` | Continue Architecture Planning.md:43196 | `art-33fa8de51e13e087` | `IMPLEMENTED` | 150359 | `8b0987792f6182090942ff5959eb8ae1e5cbf5386c45632c08b1f31742bf14d3` |
| 376 | `0.7.1` | Continue Architecture Planning.md:48949 | `art-e0789bc8f62176cb` | `IMPLEMENTED` | 145734 | `00c676fabe2d0b6c0e469e03171e00971a7291c7da404b624751fa86c19d39bb` |

## Major implementation families

- Early source-split v0.1.0 and v0.2.0 userscripts
- Flattened v0.1.0/v0.2.0 paste representations
- Complete fenced v0.3.0 through v0.7.1 userscript family, including repeated-version branches
- Post-v0.7.1 architecture contracts and pseudocode through v0.35
- Exact archive-banner revision copies

## Discovery-engine evolution

| Version | Source | Engine artifacts |
|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | DiscoveryEngine: `art-957cabb060c4971f` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | DiscoveryEngine: `art-0648d1c473e7e354` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.3.0` | Continue Architecture Planning.md:53 | DiscoveryEngine: `art-ac4fd8cb35fea58c` |
| `0.4.0` | Continue Architecture Planning.md:2792 | DiscoveryEngine: `art-13b13af920da2ed5` |
| `0.5.0` | Continue Architecture Planning.md:7178 | DiscoveryEngine: `art-d500fa45cd83c2a6` |
| `0.4.0` | Continue Architecture Planning.md:13487 | DiscoveryEngine: `art-ac5abfdb7f384b28` |
| `0.5.0` | Continue Architecture Planning.md:18379 | DiscoveryEngine: `art-a427aad1847339ed` |
| `0.6.0` | Continue Architecture Planning.md:23141 | DiscoveryEngine: `art-15c3e3774edd630b` |
| `0.5.0` | Continue Architecture Planning.md:29439 | DiscoveryEngine: `art-af39d6ff7d65774d`<br>EngineUI: `art-ffe4faa458896290` |
| `0.6.0` | Continue Architecture Planning.md:34755 | DiscoveryEngine: `art-68499ced63f8b578`<br>EngineUI: `art-d4f30d29136802d4` |
| `0.6.0` | Continue Architecture Planning.md:43196 | OriginController: `art-199c065db6335f33`<br>GenericDiscoveryEngine: `art-c0e3f5d0000c699d` |
| `0.7.1` | Continue Architecture Planning.md:48949 | OriginController: `art-d7b2931dbf30f2eb`<br>GenericDiscoveryEngine: `art-9d84514d82ede0da` |

Rows report exact nested engine-class slices where boundaries were mechanically recoverable. Absence in this table does not mean the concept is absent from a flattened whole-script artifact.

## Scheduler evolution

| Version | Source | Scheduler artifacts |
|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | Scheduler: `art-3422b29e8ab8a7fa` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | Scheduler: `art-78ba6027187052a4` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.3.0` | Continue Architecture Planning.md:53 | Scheduler: `art-5be25a9f15ac75d8` |
| `0.4.0` | Continue Architecture Planning.md:2792 | Scheduler: `art-85d2eddbc38d0f60` |
| `0.5.0` | Continue Architecture Planning.md:7178 | Scheduler: `art-1b3c321a87c6c31e` |
| `0.4.0` | Continue Architecture Planning.md:13487 | Scheduler: `art-ae6fd68a68a44db3` |
| `0.5.0` | Continue Architecture Planning.md:18379 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.6.0` | Continue Architecture Planning.md:23141 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.5.0` | Continue Architecture Planning.md:29439 | Scheduler: `art-205c035d169908a1` |
| `0.6.0` | Continue Architecture Planning.md:34755 | Scheduler: `art-a3eb762e56e8cfc9` |
| `0.6.0` | Continue Architecture Planning.md:43196 | AdaptiveScheduler: `art-3263e66c44f4c579` |
| `0.7.1` | Continue Architecture Planning.md:48949 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |

Scheduler classes and scheduler-oriented code blocks remain independent artifacts. No scheduler implementation was merged into a later representation.

## Candidate model evolution

| Version | Source | Artifact | Mechanically observed fields |
|---|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | `art-6d420309da1b4bb7` | `attempts`, `createdAt`, `hints`, `id`, `origin`, `parent`, `priority`, `status`, `target`, `type` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | `art-5c3e8f1c4e3fcae5` | `attempts`, `createdAt`, `hints`, `id`, `origin`, `parent`, `priority`, `status`, `target`, `type` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.3.0` | Continue Architecture Planning.md:53 | `art-f52789eef20c179d` | `attempts`, `createdAt`, `hints`, `id`, `origin`, `parent`, `priority`, `status`, `target`, `type` |
| `0.4.0` | Continue Architecture Planning.md:2792 | `art-c59c9caae171cd46` | `attempts`, `createdAt`, `depth`, `hints`, `id`, `nextAttemptAt`, `origin`, `parent`, `priority`, `status`, `target`, `type` |
| `0.5.0` | Continue Architecture Planning.md:7178 | `art-7658c21799c264ae` | `attempts`, `createdAt`, `depth`, `hints`, `id`, `nextAttemptAt`, `origin`, `parent`, `priority`, `status`, `target`, `type` |
| `0.4.0` | Continue Architecture Planning.md:13487 | `art-a7e23401a50e698f` | `attempts`, `createdAt`, `depth`, `hints`, `id`, `nextAttemptAt`, `origin`, `parent`, `priority`, `status`, `target`, `type` |
| `0.5.0` | Continue Architecture Planning.md:18379 | `art-cb0533a61ff3ade7` | `attempts`, `createdAt`, `depth`, `hints`, `id`, `lastError`, `nextAttemptAt`, `origin`, `parent`, `priority`, `status`, `target`, `type` |
| `0.6.0` | Continue Architecture Planning.md:23141 | `art-75bed90a2bdbfbaf` | `acquiringAt`, `attempts`, `claimedAt`, `completedAt`, `createdAt`, `depth`, `expandedAt`, `failedAt`, `hints`, `id`, `lastError`, `nextAttemptAt`, `observedAt`, `origin`, `parent`, `priority`, `queuedAt`, `recognizedAt`, `status`, `target`, `type` |
| `0.5.0` | Continue Architecture Planning.md:29439 | `art-4bcdef425e8bda9b` | `acquiringAt`, `alternateOrigins`, `alternateTypes`, `attempts`, `claimedAt`, `completedAt`, `createdAt`, `depth`, `expandedAt`, `failedAt`, `hints`, `id`, `nextAttemptAt`, `observedAt`, `origin`, `parent`, `parents`, `priority`, `queuedAt`, `recognizedAt`, `status`, `target`, `type` |
| `0.6.0` | Continue Architecture Planning.md:34755 | `art-eee0d6ac4f5f54ac` | `acquiringAt`, `alternateOrigins`, `alternateTypes`, `attempts`, `claimedAt`, `completedAt`, `createdAt`, `depth`, `expandedAt`, `failedAt`, `hints`, `id`, `nextAttemptAt`, `observedAt`, `origin`, `parent`, `parents`, `priority`, `queuedAt`, `recognizedAt`, `skippedAt`, `status`, `target`, `type` |
| `0.6.0` | Continue Architecture Planning.md:43196 | `art-da15dee66827cf8c` | `acquiringAt`, `alternateOrigins`, `alternateParents`, `alternateTypes`, `attempts`, `claimedAt`, `completedAt`, `createdAt`, `depth`, `discoveredAt`, `expandedAt`, `failedAt`, `hints`, `id`, `nextAttemptAt`, `observedAt`, `origin`, `parent`, `priority`, `queuedAt`, `recognizedAt`, `status`, `target`, `type` |
| `0.7.1` | Continue Architecture Planning.md:48949 | `art-a99ebc49a4254f07` | `acquiringAt`, `alternateOrigins`, `alternateParents`, `alternateTypes`, `attempts`, `claimedAt`, `completedAt`, `createdAt`, `depth`, `discoveredAt`, `expandedAt`, `failedAt`, `hints`, `id`, `nextAttemptAt`, `observedAt`, `origin`, `parent`, `plannedAt`, `priority`, `queuedAt`, `recognizedAt`, `skippedAt`, `status`, `target`, `type` |

## Observation model evolution

| Version | Source | Artifact | Mechanically observed fields |
|---|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | `art-538cc6a7a7b8b4d6` | `candidateId`, `completedAt`, `errors`, `features`, `http`, `id`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | `art-756466d45f355acc` | `body`, `candidateId`, `completedAt`, `errors`, `http`, `id`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.3.0` | Continue Architecture Planning.md:53 | `art-3fb6fd6d55e078b1` | `body`, `candidateId`, `completedAt`, `errors`, `http`, `id`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.4.0` | Continue Architecture Planning.md:2792 | `art-92f49788f0e46f5e` | `body`, `candidateId`, `completedAt`, `errors`, `http`, `id`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.5.0` | Continue Architecture Planning.md:7178 | `art-89a1e78cce30332a` | `body`, `bodyTruncated`, `candidateId`, `completedAt`, `errors`, `http`, `id`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.4.0` | Continue Architecture Planning.md:13487 | `art-38e1267ff7742f1f` | `body`, `candidateId`, `completedAt`, `errors`, `http`, `id`, `network`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.5.0` | Continue Architecture Planning.md:18379 | `art-b844d07af7682d56` | `body`, `candidateId`, `completedAt`, `errors`, `fingerprint`, `http`, `id`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.6.0` | Continue Architecture Planning.md:23141 | `art-16ccd6bf6ce57e54` | `body`, `candidateId`, `completedAt`, `errors`, `fingerprint`, `http`, `id`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.5.0` | Continue Architecture Planning.md:29439 | `art-427d31dbfe025c9e` | `body`, `candidateId`, `completedAt`, `errors`, `fingerprint`, `http`, `id`, `network`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.6.0` | Continue Architecture Planning.md:34755 | `art-dca138c09325c970` | `body`, `candidateId`, `completedAt`, `errors`, `fingerprint`, `http`, `id`, `network`, `reason`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.6.0` | Continue Architecture Planning.md:43196 | `art-5bb815a8798f901f` | `body`, `candidateId`, `completedAt`, `errors`, `fingerprint`, `http`, `id`, `network`, `reason`, `requestedUrl`, `signalPresent`, `startedAt`, `status`, `target` |
| `0.7.1` | Continue Architecture Planning.md:48949 | `art-e98ef71f3937a5f2` | `body`, `bodyTruncated`, `candidateId`, `completedAt`, `errors`, `fingerprint`, `http`, `id`, `network`, `planId`, `reason`, `requestedUrl`, `signalPresent`, `startedAt`, `status`, `target` |

## Discovery model evolution

| Version | Source | Artifact | Mechanically observed fields |
|---|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | `art-c8174278dc5c3cd2` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `observationId`, `provenance` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | `art-79c92578ae130589` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `observationId`, `provenance` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.3.0` | Continue Architecture Planning.md:53 | `art-d556d5eb848af542` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `observationId`, `provenance` |
| `0.4.0` | Continue Architecture Planning.md:2792 | `art-8267c4e2e0748d7e` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `mechanism`, `observationId`, `provenance` |
| `0.5.0` | Continue Architecture Planning.md:7178 | `art-e765b0cddd9bde04` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `mechanism`, `observationId`, `provenance` |
| `0.4.0` | Continue Architecture Planning.md:13487 | `art-11fedee43a51499d` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `observationId`, `provenance` |
| `0.5.0` | Continue Architecture Planning.md:18379 | `art-690c74cbd36aec9e` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `observationId`, `provenance` |
| `0.6.0` | Continue Architecture Planning.md:23141 | `art-fa108f051a086874` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `mechanism`, `observationId`, `provenance` |
| `0.5.0` | Continue Architecture Planning.md:29439 | `art-3ec453a391b13904` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `mechanism`, `observationId`, `provenance` |
| `0.6.0` | Continue Architecture Planning.md:34755 | `art-32a3d0a3e9d729d8` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `mechanism`, `observationId`, `provenance` |
| `0.6.0` | Continue Architecture Planning.md:43196 | `art-bf0e5de651e02a37` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `mechanism`, `observationId`, `provenance` |
| `0.7.1` | Continue Architecture Planning.md:48949 | `art-d37432fd888e46a7` | `candidateId`, `confidence`, `createdAt`, `data`, `id`, `kind`, `mechanism`, `observationId`, `provenance` |

`FIELD-HISTORY.yaml` compares `this.<field> =` assignment sets only along source-supported userscript lineage edges. It does not infer field renames, types, or semantic equivalence. KnowledgeBase, provenance, resource, budget, session, domain, claim, and related definitions remain separately indexed.

## Provider evolution

| Version | Source | Provider artifacts/symbols |
|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | HtmlRecognizer: `art-b20c916d3bc67731` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | ResponseProvider: `art-913df2f28f1cbf0c`<br>HtmlProvider: `art-0f607231cf25f140`<br>JsonProvider: `art-1bac5b8c6517a341`<br>TextProvider: `art-efe7d5a26da111e8`<br>ProviderRegistry: `art-69ac5c503cd96ef3` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.3.0` | Continue Architecture Planning.md:53 | ResponseProvider: `art-7b99eaffeeacf062`<br>HtmlProvider: `art-3c6788f51b8e56e9`<br>JsonProvider: `art-e8de0c5603edb2c3`<br>TextProvider: `art-e50a705e297aedcd`<br>ProviderRegistry: `art-23fff9a666ffbb94` |
| `0.4.0` | Continue Architecture Planning.md:2792 | ResponseProvider: `art-13ad4bff3157d279`<br>HtmlProvider: `art-800f49c60b025b0d`<br>JsonProvider: `art-de8d70149815c779`<br>TextProvider: `art-6fd8276874ec982e`<br>XmlProvider: `art-edf852e8bc97d40e`<br>ManifestProvider: `art-af4a4cc2d1d14559`<br>ProviderRegistry: `art-2848991adbd8e86c` |
| `0.5.0` | Continue Architecture Planning.md:7178 | ResponseProvider: `art-e808501271914f60`<br>HtmlProvider: `art-9d3a764e67bc86f2`<br>JsonProvider: `art-6fb45dfb05559117`<br>ManifestProvider: `art-cec722c63e35f525`<br>XmlProvider: `art-76f5452f850736af`<br>RobotsProvider: `art-b91fb712da955d6f`<br>ApiDescriptionProvider: `art-a7ef02959dc212aa`<br>TextProvider: `art-8398cd9fae4935ab`<br>ProviderRegistry: `art-12071dbde2a640a0` |
| `0.4.0` | Continue Architecture Planning.md:13487 | ResponseProvider: `art-3520a600c15d7b5b`<br>HtmlProvider: `art-94afff5b50f72476`<br>JsonProvider: `art-782fd944e04d91e8`<br>XmlProvider: `art-3a802eb7bb7000c0`<br>CssProvider: `art-17fb393a93d26d2a`<br>JavaScriptProvider: `art-63edc11faa5fe3c7`<br>RobotsProvider: `art-bf4ad78b2bd5353d`<br>TextProvider: `art-c1cf7d787263ae3b`<br>ProviderRegistry: `art-f9e0998a63fbbcd9` |
| `0.5.0` | Continue Architecture Planning.md:18379 | Provider: `art-7bb9692626761003`<br>HtmlProvider: `art-5c6d187eccc84371`<br>JsonProvider: `art-3850b4f7191e9e8d`<br>XmlProvider: `art-a40cf30beb3ee014`<br>CssProvider: `art-da647b30bf8fdae5`<br>JavaScriptProvider: `art-400e55d470b07f97`<br>RobotsProvider: `art-bb7481225b62dffa`<br>TextProvider: `art-ef8c738040a40412`<br>ProviderRegistry: `art-b9d78dec2a3df19f` |
| `0.6.0` | Continue Architecture Planning.md:23141 | Provider: `art-f113bba51210501c`<br>HtmlProvider: `art-399f1f6e83d29aae`<br>JsonProvider: `art-f4b1508c378ef160`<br>XmlProvider: `art-48e7f8ec53e013ea`<br>CssProvider: `art-ecc299c1b923769e`<br>JavaScriptProvider: `art-a0bc2591240b92d5`<br>RobotsProvider: `art-a2879a23dfd46920`<br>TextProvider: `art-957acc4c6b63ab76`<br>BinaryProvider: `art-6d32814b6d4831e7`<br>ProviderRegistry: `art-fbc0419d248c98cf` |
| `0.5.0` | Continue Architecture Planning.md:29439 | Provider: `art-4b9e16d3991e91f8`<br>ResponseProvider: `art-c70f4a225e4a415e`<br>HtmlProvider: `art-b7fe8dd8893a8416`<br>JsonProvider: `art-2ad42dc41eac49c7`<br>XmlProvider: `art-f53353cbf95ba206`<br>CssProvider: `art-b7c4660ebee379c1`<br>JavaScriptProvider: `art-d372fcc07db72b56`<br>RobotsProvider: `art-304df2b3537b1e49`<br>TextProvider: `art-1da54951dda4eb47`<br>BinaryProvider: `art-8e69a5d9ebb978ed`<br>ProviderRegistry: `art-b5266fd26e94091c` |
| `0.6.0` | Continue Architecture Planning.md:34755 | Provider: `art-4ab7b2e055dbb5c4`<br>ResponseProvider: `art-f5eda70fbf7f8e4d`<br>HtmlProvider: `art-a454a0af38b41ff3`<br>JsonProvider: `art-5a5a535a77953ca6`<br>XmlProvider: `art-a97beef5e45a73b8`<br>CssProvider: `art-9af6624989df58fb`<br>JavaScriptProvider: `art-83476917f66259b3`<br>RobotsProvider: `art-9d18c980b76ce263`<br>TextProvider: `art-fcded9f9e6eb1369`<br>BinaryProvider: `art-075d27c3451f7757`<br>ProviderRegistry: `art-a71198de2aeb0112` |
| `0.6.0` | Continue Architecture Planning.md:43196 | Provider: `art-43b7c8bfed361ba8`<br>ResponseProvider: `art-eaedbd60bf8c5b34`<br>HtmlProvider: `art-736f0001827c8db2`<br>JsonProvider: `art-ce36cdf543670046`<br>XmlProvider: `art-6e22157fe9fe7865`<br>CssProvider: `art-9bce464708b823c1`<br>JavaScriptProvider: `art-d5690dcdc03032b7`<br>RobotsProvider: `art-59545e34a1e499ed`<br>TextProvider: `art-8b873fe8af0d8904`<br>BinaryProvider: `art-3ab458e706d42dba`<br>ProviderRegistry: `art-6af8bbe905287db1` |
| `0.7.1` | Continue Architecture Planning.md:48949 | Provider: `art-27f0b3e2723007e8`<br>HtmlProvider: `art-60cab60faf66779a`<br>JsonProvider: `art-250f9bf6f718e9ec`<br>XmlProvider: `art-4f1dc13b1f744857`<br>CssProvider: `art-3d02a531157339a6`<br>JavaScriptProvider: `art-ba0d74b46d7cbff6`<br>TextProvider: `art-a9f5079497c574de`<br>BinaryProvider: `art-1856f3b918b71c9f`<br>ProviderRegistry: `art-d0ad5943c4779fb2` |

Provider symbols mechanically identified across all artifacts include:

- `AcquisitionProvider`
- `AcquisitionProviderRegistry`
- `ApiDescriptionProvider`
- `BinaryProvider`
- `CandidateSource`
- `CandidateSourceRegistry`
- `CssProvider`
- `DiscoveryProvider`
- `GMXHRProvider`
- `HtmlProvider`
- `HtmlRecognizer`
- `JavaScriptProvider`
- `JsonProvider`
- `ManifestProvider`
- `PartitionExpansionProvider`
- `Provider`
- `ProviderRegistry`
- `QueryExpansionProvider`
- `RecognitionProvider`
- `ResponseProvider`
- `RobotsProvider`
- `TextProvider`
- `XmlProvider`

Provider dependencies are token observations, not runtime verification.

## Acquisition evolution

| Version | Source | Acquisition artifacts/symbols |
|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | HttpAcquisitionAdapter: `art-af20498245caa757` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | HttpAcquisitionAdapter: `art-d51f79dc85eafa18` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.3.0` | Continue Architecture Planning.md:53 | HttpAcquisitionAdapter: `art-ca595abccf7757e7` |
| `0.4.0` | Continue Architecture Planning.md:2792 | HttpAcquisitionAdapter: `art-7af22df3afb2b4f2` |
| `0.5.0` | Continue Architecture Planning.md:7178 | HttpAcquisitionAdapter: `art-33c3d7fadc839ba5` |
| `0.4.0` | Continue Architecture Planning.md:13487 | HttpAcquisitionAdapter: `art-77da573ca3cd4a4a` |
| `0.5.0` | Continue Architecture Planning.md:18379 | HttpAcquisition: `art-4754960bb5cd2fec` |
| `0.6.0` | Continue Architecture Planning.md:23141 | HttpAcquisition: `art-d3ab8a8aa9d1f5e4` |
| `0.5.0` | Continue Architecture Planning.md:29439 | HttpAcquisitionAdapter: `art-8efa7661fa5d5181` |
| `0.6.0` | Continue Architecture Planning.md:34755 | HttpAcquisitionAdapter: `art-894c54a8c7851457`<br>AcquisitionPolicy: `art-69e18868ec91f495` |
| `0.6.0` | Continue Architecture Planning.md:43196 | AcquisitionPolicy: `art-0cb69f13a4606beb` |
| `0.7.1` | Continue Architecture Planning.md:48949 | AcquisitionPlan: `art-5af7d0c912f183ca`<br>AcquisitionPolicy: `art-1ac18c50c963764b`<br>Acquisition: `art-344f6a75939b2571` |

Acquisition classes and contracts are separately classified where source boundaries permit. Historical `fetch`, XHR, and `GM_xmlhttpRequest` implementations remain independent.

## Concurrency evolution

| Version | Source | Model | Worker count | Ownership/duplicate-prevention observation |
|---|---|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | async worker pool, shared queue/frontier | `3` | visited state/set; duplicate prevention: visited state/set |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | async worker pool, shared queue/frontier | `3` | claimNextCandidate, claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.1.0` | Continue Architecture Planning.md:3 | async worker pool, shared queue/frontier | `3` | visited state/set; duplicate prevention: visited state/set |
| `0.2.0` | Continue Architecture Planning.md:11 | async worker pool, shared queue/frontier | `3` | claimNextCandidate, claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.3.0` | Continue Architecture Planning.md:53 | async worker pool, shared queue/frontier | `3` | claimNextCandidate, claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.4.0` | Continue Architecture Planning.md:2792 | async worker pool, shared queue/frontier | `3` | claimNextCandidate, claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.5.0` | Continue Architecture Planning.md:7178 | async worker pool, shared queue/frontier | `4` | claimNextCandidate, claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.4.0` | Continue Architecture Planning.md:13487 | async worker pool, shared queue/frontier | `4` | claimNextCandidate, claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.5.0` | Continue Architecture Planning.md:18379 | async worker pool, shared queue/frontier | `4` | claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.6.0` | Continue Architecture Planning.md:23141 | async worker pool, shared queue/frontier | `4` | claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.5.0` | Continue Architecture Planning.md:29439 | async worker pool, shared queue/frontier | `4` | claimNextCandidate, claimed state/set, visited state/set; duplicate prevention: claimed state/set, visited state/set |
| `0.6.0` | Continue Architecture Planning.md:34755 | async worker pool, shared queue/frontier, lease-based ownership | `5` | claimNextCandidate, claimed state/set, visited state/set, lease; duplicate prevention: claimed state/set, visited state/set, lease |
| `0.6.0` | Continue Architecture Planning.md:43196 | async worker pool, shared queue/frontier, lease-based ownership | `4` | claimNextCandidate, claimed state/set, visited state/set, lease; duplicate prevention: claimed state/set, visited state/set, lease |
| `0.7.1` | Continue Architecture Planning.md:48949 | async worker pool, shared queue/frontier, lease-based ownership | `4` | claimNextCandidate, claimed state/set, visited state/set, lease; duplicate prevention: claimed state/set, visited state/set, lease |

Manifest `concurrency` records also retain claim points, async boundaries, cancellation tokens, and error-isolation syntax. These observations do **not** establish concurrency safety; every safety conclusion remains `UNKNOWN` and verification remains `UNVERIFIED`.

## Configuration evolution

| Version | Source | Configuration artifact | Worker count observation |
|---|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | CONFIG: `art-5be67443de03368a` | `3` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | CONFIG: `art-578d78a8386f184b` | `3` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` | `3` |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` | `3` |
| `0.3.0` | Continue Architecture Planning.md:53 | CONFIG: `art-bddb23e6ba12e6ee` | `3` |
| `0.4.0` | Continue Architecture Planning.md:2792 | CONFIG: `art-4a4cf840a16b987a` | `3` |
| `0.5.0` | Continue Architecture Planning.md:7178 | CONFIG: `art-6687f5a4980390d3` | `4` |
| `0.4.0` | Continue Architecture Planning.md:13487 | CONFIG: `art-ceebb6f2fec6494f` | `4` |
| `0.5.0` | Continue Architecture Planning.md:18379 | CONFIG: `art-7647fc0582cb8481` | `4` |
| `0.6.0` | Continue Architecture Planning.md:23141 | CONFIG: `art-ec98490a90192697` | `4` |
| `0.5.0` | Continue Architecture Planning.md:29439 | CONFIG: `art-f149d4d94aec65cd` | `4` |
| `0.6.0` | Continue Architecture Planning.md:34755 | CONFIG: `art-f6af84ef31d0a77f` | `5` |
| `0.6.0` | Continue Architecture Planning.md:43196 | CONFIG: `art-6a380a786e7f33e9` | `4` |
| `0.7.1` | Continue Architecture Planning.md:48949 | CONFIG: `art-8b378236b04ceef4` | `4` |

Configuration files preserve exact historical literals. `CHANGES.yaml` compares mechanically observed simple literals without evaluating JavaScript.

## Storage evolution

| Version | Source | Artifact | Mechanically observed fields |
|---|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | `art-f79bedb8ba7febed` | `candidates`, `discoveries`, `observations`, `visited` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | `art-8df8f9bb24a6f4ac` | `candidates`, `claimed`, `discoveries`, `observations`, `visited` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_RECOVERABLE_FROM_FLATTENED_REPRESENTATION` | — |
| `0.3.0` | Continue Architecture Planning.md:53 | `art-1a8a80a2eace5b4f` | `candidates`, `claimed`, `discoveries`, `observations`, `visited` |
| `0.4.0` | Continue Architecture Planning.md:2792 | `art-4fb30cb408283e41` | `candidates`, `claimed`, `discoveries`, `graph`, `observations`, `visited` |
| `0.5.0` | Continue Architecture Planning.md:7178 | `art-3c357e1fce63e052` | `candidates`, `claimed`, `discoveries`, `graph`, `observations`, `visited` |
| `0.4.0` | Continue Architecture Planning.md:13487 | `art-f3bf233dfcd8c882` | `candidates`, `claimed`, `discoveries`, `observations`, `visited` |
| `0.5.0` | Continue Architecture Planning.md:18379 | `art-b9ef2487d49ea940` | `candidates`, `claimed`, `discoveries`, `networkEvents`, `observations`, `visited` |
| `0.6.0` | Continue Architecture Planning.md:23141 | `art-774852ff67b40e5e` | `candidates`, `claimed`, `discoveries`, `edges`, `engine`, `networkEvents`, `networkRequests`, `observations`, `persistTimer`, `resources`, `visited` |
| `0.5.0` | Continue Architecture Planning.md:29439 | `art-60e1efcb69393e27` | `candidates`, `claimed`, `discoveries`, `edgeRecords`, `observations`, `persistTimer`, `queue`, `resources`, `statistics`, `visited` |
| `0.6.0` | Continue Architecture Planning.md:34755 | `art-fbd2c2852d622a92` | `candidates`, `claimed`, `discoveries`, `edgeRecords`, `fingerprintIndex`, `observations`, `persistTimer`, `queue`, `resources`, `statistics`, `visited` |
| `0.6.0` | Continue Architecture Planning.md:43196 | `art-a77939f7530f26f9` | `candidates`, `claimed`, `diagnostics`, `discoveries`, `edges`, `fingerprintIndex`, `networkEvents`, `observations`, `persistenceTimer`, `resources`, `stats`, `visited` |
| `0.7.1` | Continue Architecture Planning.md:48949 | `art-2697c5969175b5b0` | `candidateKeys`, `candidates`, `claimed`, `diagnostics`, `discoveries`, `fingerprintIndex`, `graphEdges`, `networkEvents`, `observations`, `resources`, `stats`, `visited` |

Storage API token deltas (`GM_getValue`, `GM_setValue`, `localStorage`, and `IndexedDB`) are recorded under `cross_version_dimensions.storage_tokens` in `CHANGES.yaml`; no persistence behavior is inferred.

## UI evolution

| Version | Source | UI artifacts |
|---|---|---|
| `0.1.0` | Userscript Discovery Prototype.md:1942 | UI: `art-4839bf9d50ffb56e` |
| `0.2.0` | Userscript Discovery Prototype.md:3047 | UI: `art-42a3fd253461d2c5` |
| `0.1.0` | Continue Architecture Planning.md:3 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.2.0` | Continue Architecture Planning.md:11 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.3.0` | Continue Architecture Planning.md:53 | UI: `art-bffc725e58dfc65d` |
| `0.4.0` | Continue Architecture Planning.md:2792 | UI: `art-396941e4cfd827b1` |
| `0.5.0` | Continue Architecture Planning.md:7178 | UI: `art-7817b108f4dec9d2` |
| `0.4.0` | Continue Architecture Planning.md:13487 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.5.0` | Continue Architecture Planning.md:18379 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.6.0` | Continue Architecture Planning.md:23141 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.5.0` | Continue Architecture Planning.md:29439 | UI: `art-b6afabe847891691` |
| `0.6.0` | Continue Architecture Planning.md:34755 | UI: `art-7157df224e7225cf` |
| `0.6.0` | Continue Architecture Planning.md:43196 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |
| `0.7.1` | Continue Architecture Planning.md:48949 | `NOT_SEPARATELY_RECOVERABLE_OR_NOT_PRESENT` |

Clearly marked UI source sections inside complete userscripts are extracted as exact nested byte ranges. Flattened scripts were not split because their original component whitespace/boundaries are not recoverable.

## Tests and validation code

No fenced block met the conservative test criterion (a test-labeled section with assertion/test calls). Validation/invariant architecture snippets remain pseudocode rather than being relabeled as executed tests.

## Duplication and lineage

Exact duplicate groups: **2782**  
Near-duplicate observations: **97**  
Evolution groups: **32**  
Change records: **156**

Duplicates are retained. `DUPLICATES.yaml` chooses a canonical identifier solely by earliest chronology/provenance index. `NEAR-DUPLICATES.yaml` records mechanical line similarity without asserting semantic identity. `evolved_from` is used only where source prose supports the transition; ambiguous edges are `unknown_relation`.

Every `CHANGES.yaml` record contains mechanical comparisons for API symbols, assigned data fields, control-flow tokens, scheduler/concurrency/acquisition/discovery tokens, provider symbols, UI/storage/error/security tokens, and simple configuration literals. `behavior_changes` remains empty because no execution or semantic verification was performed.

## Superseded implementations

Artifacts explicitly classified `SUPERSEDED_IMPLEMENTATION`: **0**.

The documents use revised/continuing language that supports selected `evolved_from` edges, but they do not reliably establish one current winner among repeated v0.4.0, v0.5.0, or v0.6.0 scripts. The extraction therefore does not silently mark those variants superseded.

## Missing/incomplete source

Incomplete/anomalous original artifacts: **50**

The early split/flattened scripts are preserved exactly. Missing original whitespace in flattened lines is `NOT_RECOVERABLE`; it was not inferred. There were **0** extraction failures. Lexical component-boundary uncertainties, if any, are listed in `UNCERTAINTIES.md`.

## Contradictions and uncertainties

Contradictions: **4**  
Uncertainties: **8**

Repeated/regressing versions and source formatting conflicts are registered, not resolved.

## Reconstruction candidates and results

Two optional v0.1.0/v0.2.0 reconstructions mechanically concatenate explicit source ranges after removing Markdown fence delimiter lines. They remain under `reconstructed/`, are marked `derived: true`, `semantic_inference: false`, and `authoritative: false`. They are **not** authentic raw artifacts. Flattened paste representations were not reconstructed.

## Validation

- Source coverage: **PASS** — 5184/5184 detected source regions represented
- Provenance coverage: **PASS** — 5646/5646 artifacts have required provenance; reconstructed artifacts use composite provenance
- Hash coverage: **PASS** — 5646/5646 artifact files match SHA-256
- Lineage consistency: **PASS** — 3488 relationships; 0 broken references
- Reconstruction labeling: **PASS** — 2 reconstructed artifacts explicitly non-authoritative
- Semantic preservation: **PASS** — 5644/5644 original artifacts equal their source byte ranges
- Empty artifacts: **PASS** — 0 empty artifacts

Overall: **PASS**

## Final distinction

- **EXTRACTED:** exact bytes selected from pinned historical Git blobs; authoritative for what those Markdown revisions contain.
- **RECONSTRUCTED:** separately labeled mechanical concatenations; non-authoritative derivatives.
- **INFERRED:** language, role, context version, similarity, and some chronology metadata only; never presented as authentic source bytes.
