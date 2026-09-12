# Discovery Closure Analysis

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

| Snapshot | Version | Expansion mechanism | Repeating scheduler | Closure classification | Exhaustive? |
|---|---|---|---|---|---|
| snapshot-0001 | v0.1.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0003 | v0.2.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0005 | v0.3.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0006 | v0.4.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0008 | v0.4.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0007 | v0.5.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0009 | v0.5.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0011 | v0.5.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0010 | v0.6.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0012 | v0.6.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0013 | v0.6.0 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |
| snapshot-0014 | v0.7.1 | present | present | STATIC_RECURSIVE_CLOSURE_SUPPORTED | NO |

**Closure means:** a discovery can yield candidate work that re-enters scheduler/knowledge state. It does not mean exhaustive crawling. Convergence depends on duplicate identity, depth/frontier/body/time/retry budgets, provider behavior, asynchronous additions, and origin policy. Termination remains conditional. Snapshot-0009 is structurally exact but statically non-executable; its represented closure cannot be upgraded to runnable closure.
