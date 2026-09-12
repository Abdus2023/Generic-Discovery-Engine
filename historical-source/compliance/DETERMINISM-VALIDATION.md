# Protocol-v12 Determinism Validation

**Status:** `PASS`
**Result:** 52/52 generator-owned deliverables byte-identical

Regeneration used an isolated temporary copy of every declared input with `PYTHONHASHSEED=577215`; unknown audit timestamps remain explicit deterministic sentinels.

| Path | Identical | SHA-256 |
|---|---|---|
| INPUT-CONTRACT.yaml | true | `9d31c5fd320ab79d51038bf946c33b6dde2f6839539e1ef2ede811665b2f5fb4` |
| AUDIT.yaml | true | `eefad16cdc9c6d7f02b2bc14ee0d92fe4e280a00e5e33b8bda438e3016b52ea3` |
| AUDIT-SCOPE.yaml | true | `67068512765b61790af99aa28a1b8cf653abec259570e53642e0ee72bff56d27` |
| IMPLEMENTATION-ARTIFACTS.yaml | true | `27b377ebfd2738522ba55e56006b782ab94e583b26951b875314cb43cdfd836c` |
| IMPLEMENTATION-EVIDENCE.yaml | true | `68e51fa22d0caf62bc9e1a38991c5b15433f9454e29b51ff5611e1f37f947cea` |
| IMPLEMENTATION-CLAIMS.yaml | true | `6d7edd685bb72b02f678c771558aebd8988c8180981680fa2c1bc097d120b5f2` |
| REQUIREMENT-MAPPINGS.yaml | true | `b68807a74981ee5fb102275fd37fe23af053a719d77b861ac008fad92fac1099` |
| EVIDENCE-RECORDS.yaml | true | `3e9351cac003581f369fca86084d76269e1f1869154e671cb825b29ae7f36eea` |
| VERIFICATION-EXECUTIONS.yaml | true | `b3b19612df200d893e513b648426405e59a445247669188873e4772cf7381575` |
| ENVIRONMENTS.yaml | true | `c36766f9b611037f8b3b617d5e71496b302f21ee3e552a8efad3a0c3c9f0d3d0` |
| COMPLIANCE-DECISIONS.yaml | true | `efeb8d1ad841e2c0c92705fc120e4c719657d69d8d4a7c6e7b5fc430639ca15a` |
| FINDINGS.yaml | true | `371fb7bc19ec277d5487c2450d14397659540a4bd3de26ce907cccbfc01836b9` |
| NONCONFORMANCES.yaml | true | `9fefe947631db99a5dfaa5ed52af3904f17586ce1601a988116cb883e09d4f85` |
| WAIVERS.yaml | true | `2088d1170b5b5f66aca83d9356443ee79d92d847c070437eebf8d9ec0ee58fa1` |
| REMEDIATIONS.yaml | true | `5047dca3404fb89055940831c0c7d1adbb70f0509c28b62c98712be348d466ad` |
| REMEDIATION-ACTIONS.yaml | true | `3376a1152276b9a2d3398a6e15f55abf3c38c5a06402dfcb08601cbdfd996e61` |
| AUDIT-RUNS.yaml | true | `2c50ddac78f1398a2401dc21efcab5b9dc319992d5375adb163643943c41bf4d` |
| AUDIT-CERTIFICATE.yaml | true | `3a51057a36b36abb568d024eb7b3e2cd4409c083c3430d915e2f4cb9e77c7d80` |
| IMPLEMENTATION-GRAPH.yaml | true | `96c55e069bba99b9a12648470d40660d94d6881552db0f79621784bf91bc52cc` |
| CONFORMANCE-GRAPH.yaml | true | `7165fc139d561463570d9350d3bc9bf80ed960ceea6b8b8575459cdfbe61a921` |
| FINDING-GRAPH.yaml | true | `c4f8345d87988a03138caadafba26b406ccfa6ae43de46b51d22b0e4c7d88403` |
| AUDIT-EVIDENCE-GRAPH.yaml | true | `b20f76abc255e42c71eeb9b680805b7981f98bdb11e97d5f6747a664b8e1ecbe` |
| COMPLIANCE-MATRIX.yaml | true | `f89e02c6049f0021d276bb4076c48a7f4b27c306825115410f9be5895f76e15a` |
| COMPLIANCE-AGGREGATION.yaml | true | `03257bcdd3fa44c064ffc91286fc40fae82deeeac2ab169f24b62a1e6898c623` |
| RELEASE-GATE.yaml | true | `bcb82730210ddb31d65d0c21ee31df0b06faf785d5b2a1a9e396749ebc8867da` |
| SCHEMA/audit.schema.yaml | true | `e8dc53c9ba11e7e76ee4fb3603fc7521337557a7b8de7272ef2a79c7e0949d76` |
| SCHEMA/audit-scope.schema.yaml | true | `0cabe3080a3ce40e68a6ef5ec75e8fffe08d28ea05bed0fc1231b90d851de815` |
| SCHEMA/implementation-artifact.schema.yaml | true | `ac1ed568416467057e7c793efdb4533ae5200a1dbfd478cf6a0a3f152d546052` |
| SCHEMA/implementation-evidence.schema.yaml | true | `cb8ca7418551fd25c867e7b10dcc817ce7b3c37cd61578b727b6dc498a503e9a` |
| SCHEMA/implementation-claim.schema.yaml | true | `2300e0069a0a7b997973d005bd9c7946e6b99ffbbfeb77faa8bd5c59eb1d22a9` |
| SCHEMA/requirement-mapping.schema.yaml | true | `82013103bfc1605f34b9d1b54c5855b20e22a8554c18ebb2613c1b567dfb26b9` |
| SCHEMA/evidence-record.schema.yaml | true | `54cae5db50b19d9a0b3a69afd615603d884bcbc0ae2c157943de9eff430ee981` |
| SCHEMA/verification-execution.schema.yaml | true | `154b8ff037bb976fee22ceeac126ade2e13b452d3aea78489256497fca01a3ef` |
| SCHEMA/environment.schema.yaml | true | `4e115d9d7841e4c436457d8d632f956c68b53f80559083122b64de7fae96b10c` |
| SCHEMA/compliance-decision.schema.yaml | true | `eb06d1ef00400725eae3e7c3700cee5afe45d6f842924943391442c91ed391b7` |
| SCHEMA/finding.schema.yaml | true | `cd41770296320086adac7fc0aee684facedcaf5d797757305777a7342ce4f6d4` |
| SCHEMA/nonconformance.schema.yaml | true | `b110b1848314ece95c715d5cc64684887080c1a55be258899295d5e7db8ce6d0` |
| SCHEMA/waiver.schema.yaml | true | `69fd000822de311d3b055c61ddd7b95b864c90d28944b7db688013506cce5560` |
| SCHEMA/remediation.schema.yaml | true | `c16d15f9bebe277d4bed142a29e04901b3c4634c3b767e1c01e651f4e8fc4670` |
| SCHEMA/remediation-action.schema.yaml | true | `12807d7af12479f0494dd99572387c4f96a4aa48f053f1190457c12a502ed784` |
| SCHEMA/audit-run.schema.yaml | true | `e08498de93171ec08bd61d56899613089e699fb340a1d78dc0308dcac5e5005a` |
| SCHEMA/audit-certificate.schema.yaml | true | `9216fa14523677ed20c224209f4f146c3c6e6af6c68d0923992c6487204a3a8f` |
| REPORTS/COMPLIANCE-MATRIX.md | true | `ea6bb23da213e4638e49da00a73c44e763cb7b2baf00a6d274226b1e7c3ec2ad` |
| REPORTS/NONCONFORMANCES.md | true | `4c98ddf8677577565fa4c0d42d728eb38b299ca95841bdbd42c7867f86f8f9a7` |
| REPORTS/FINDINGS.md | true | `6d8619fd897598fae6339231ef04ca44fe1041fa25e5f010edeff46904ed4ee5` |
| REPORTS/REMEDIATION-PLAN.md | true | `99a32aabf6c7adf302d44335e637d7ebfb44aa02be45321cc9e5222d1bf9bc95` |
| REPORTS/REGRESSION-REPORT.md | true | `2e3eb25aba9fc6fc4adeb962154ccc4ee3b4be81e63d849567c98f854175f7b2` |
| REPORTS/SECURITY-AUDIT.md | true | `08e03ddde612db7f59f4123575ad1280c9b2635a7904b55bd9bbd9134cd66612` |
| REPORTS/COMPATIBILITY-AUDIT.md | true | `8101e52cc697c6ee6c0b07d0e28ed8d3ea155b0ffefd6110d65749522c8e1b30` |
| REPORTS/TEMPORAL-AUDIT.md | true | `52b3b26d00e926187cf58f4e414f6c4ae338e9b4485d784743d7fb5b73e6bec8` |
| REPORTS/TRACEABILITY-AUDIT.md | true | `85a486b9c2c4964840df444588d15a678d2cb250ede2afc351a41747498affeb` |
| REPORTS/FINAL-COMPLIANCE-REPORT.md | true | `bf7474683d5d143ffea1d9949afbb0ce7cd19cdb3a52d0219026e00234527bcd` |
