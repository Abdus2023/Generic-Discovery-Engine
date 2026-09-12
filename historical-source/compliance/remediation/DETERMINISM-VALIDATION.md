# Protocol-v13 Determinism Validation

**Status:** `PASS`
**Result:** 43/43 generator-owned deliverables byte-identical

The isolated build preserved the hash-bound v12.1 package and used `PYTHONHASHSEED=577215`.

| Path | Identical | SHA-256 |
|---|---|---|
| remediation/ACCOUNTABILITY-CHAIN.yaml | true | `c88424388e6289c5385db7fc4251cd9ec164a4f566f341ace72f3e61f88453c0` |
| remediation/CERTIFICATE-LINEAGE.yaml | true | `85ef5b0872bc4675a68ccbd8a3897e0b28f2cf2ebda659dc7c786cfe15afae6b` |
| remediation/CERTIFICATE-REVISIONS.yaml | true | `10c33e199c78301a469f367be0212d8925e390962871f186686a4c75b0638977` |
| remediation/CHANGE-SETS.yaml | true | `7acb1cee9975652301553e0b487f5adee9af5ca215bb50f2c343a086eee06ea7` |
| remediation/CLOSURE-DECISIONS.yaml | true | `5d57fe53e7b0a16b095e85be361fc22e014abca09bc9bab3d898fd0aa3f084ba` |
| remediation/CLOSURE-INVARIANTS.yaml | true | `269ed82d6e331aec51a7dcaae47d53bdb88b868e20167665619f624c246640ad` |
| remediation/CLOSURE-PREDICATE.yaml | true | `af7d3a819ed6dea28707f09832765059e651be28f40cc868a25441a14095bd40` |
| remediation/DECISION-FUNCTION.yaml | true | `22e90c0eba1193638348323feddd154acbc98962c3f35b8617ae07b550f8c669` |
| remediation/IMPACT-ASSESSMENTS.yaml | true | `f45564525c8c462a3cfda786a14774947460b014ef3865e2d23bdcbbd9ce830d` |
| remediation/IMPACT-RULES.yaml | true | `b89d2828c36f665ab69b6f41d52282d7e44190c81d517ac1379833f67211fc1a` |
| remediation/OBJECT-REGISTRY.yaml | true | `84f7fa0c9c63935579032ef2581f2aa462430801e8106cfd5386ef8d60cd0666` |
| remediation/PRIOR-AUDIT-INTEGRITY.yaml | true | `0e682748be0f91795f841bdaf9bd3eb597d67ab92aaf9e2877a34cc26af37706` |
| remediation/REGRESSION-SCOPES.yaml | true | `86880f3e0502180e5183a55d2cbfc1b90934869d3664282169905e13b03276da` |
| remediation/REMEDIATION-ACTIONS.yaml | true | `f7631c6c3abfcf5aab8f5b1ea837319d00e2175dcefae6784d0697566f5e0875` |
| remediation/REMEDIATION-DEPENDENCY-GRAPH.yaml | true | `3150d383427b4248d55722f34bd53b103acbd874a22a126f5ee25f65f4863c6f` |
| remediation/REMEDIATION-PROGRAMS.yaml | true | `be316509aae44d3dff7bff22175e73874b29cb35cae05f5b14651d53e8eb6db5` |
| remediation/REMEDIATION-STATE-MACHINE.yaml | true | `d0ffcea488ea45df0712b8bcedb735e7e1857bc54438d04d02a183c202791c22` |
| remediation/RESIDUAL-RISKS.yaml | true | `280acbd2f0498f046efb71c608940d004b88b09d34fcb79e677cd4dbbbf4e659` |
| remediation/REVERIFICATION-EXECUTIONS.yaml | true | `0817393c04087a4c323c251a46f4a23331d4cb2e4808e870bb633c1474a66873` |
| remediation/REVERIFICATION-PLANS.yaml | true | `c4a709635736423e1c4ab7e5d583ddf5af064bc308c0f007b1c4dd18e960c845` |
| remediation/REVERIFICATION-RULES.yaml | true | `63f0d30b4da330bef543b1514048e2c4db957bc9dbdf12d7e4af95d5b0e76eab` |
| remediation/ROOT-CAUSES.yaml | true | `83815f839d341f6f7d91ad3008230f44e809b3c9ad612a7b41f28796f344a0b0` |
| remediation/SCHEMA-REGISTRY.yaml | true | `e6752cb0b60b669d396f622d423d7018c398823573655d1fd2d7ba309acd7e38` |
| remediation/VALIDATION-ERRORS.yaml | true | `9eadec5fb25b35156b0ce60a72fe8d2e835d48499f03fac4d49a201074fcfc54` |
| remediation/VALIDATION-PIPELINE.yaml | true | `0a87ce3fe2eb5394132d2b54978127d16f76f14b5f10de3eade6ba6e1e9efc09` |
| remediation/VALIDATION-REPORT.yaml | true | `fd4dc7335f41a9939fc1efa8713a18ddb721165ed3c9a8d0559b65776cc843bb` |
| remediation/WAIVER-REVIEWS.yaml | true | `fb5e08143ee096e0ecbc54e15db2c2499766970e65a30bdccc37b4ec68e3a6c8` |
| schema/remediation-program.schema.yaml | true | `7a7a32a68bab70c04642cc2b78bef0c5f0c606e7295e906e6b18a28c306eb49f` |
| schema/root-cause.schema.yaml | true | `2a7199fd4ed897a759acf99a8821c3df966db670c2a6a1a6f0dfe20194151d9f` |
| schema/remediation-action.schema.yaml | true | `0376fe8f7f7e4944891b3b40c39e8dfddcd9d9aa818cb445316cd5e5d3f452bc` |
| schema/change-set.schema.yaml | true | `3ec2a21f59bbe22e81b392f966a9330a3ab4fa63c26de98b0b99a0b32b283377` |
| schema/impact-assessment.schema.yaml | true | `65bb97fe3410485cac8827056931701bc136e899aaecfb7d3874fd32a613d392` |
| schema/reverification-plan.schema.yaml | true | `2eb1cd811aebcd26ea67e68a15b3783a6f50f995f27f8c1f1c71704c8b7b2f44` |
| schema/reverification-execution.schema.yaml | true | `2f7e3d404f236672a199087c6754d0399e4460046417f781e2462c1b3afe499a` |
| schema/regression-scope.schema.yaml | true | `27a2933200deb7ed030d1bfde70aa5bc2c20152675e193e2ef908957c12c8a2f` |
| schema/closure-decision.schema.yaml | true | `9bc7d3a1f6647385b8dd13cac0faf8931bf14e3eb251583e418b08bdf0701b2f` |
| schema/waiver-review.schema.yaml | true | `3417970eca47d9f17524b541642de9cfbd8b952180894c5d76c26f8efb9cf579` |
| schema/residual-risk.schema.yaml | true | `71815cf5977d0578fc6f5a44942d0729ead549562a9fd6b247a314d8c1d633f7` |
| schema/certificate-revision.schema.yaml | true | `b6a45db682cf0cebfd81207c4af60ebe42bb7f213b6cb8f917d082f1d17a59cf` |
| reports/CLOSURE-REPORT.yaml | true | `5f3cb28734defb0eb03c3316c8c72bfc13e0296141389fbc44a81656251d6ab5` |
| reports/REGRESSION-REPORT.yaml | true | `4f1467d1e71d232c8c8929868054bcc9307c66a5bb08a7c871796ab25eecb007` |
| reports/REMEDIATION-STATUS.yaml | true | `81dd03b63aa8d76fd73bb909ca50348458488738c9b55e56017e6e50d8f5de6a` |
| reports/REVERIFICATION-REPORT.yaml | true | `5776b2b58b0d72be3e969134f1248ace892ecf342b992013066890f6a57a743c` |
