# Algorithm and Scheduler Evolution

> **Acceptance: PROVISIONAL_ONLY_UPSTREAM_BLOCKED.** Protocol-v1 raw/range validation fails and Protocol-v4 through Protocol-v7 outputs are absent. `SUPPORTED` in this report is source-local and does not mean the full v1→v9 chain is verified. Missing dimensions remain `UNKNOWN`.

## Workflow by occurrence

| Snapshot | Version | Candidate | Acquire | Observe | Recognize | Expand | Repeat | Retry | Static execution |
|---|---|---|---|---|---|---|---|---|---|
| snapshot-0001 | v0.1.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0003 | v0.2.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0005 | v0.3.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0006 | v0.4.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0008 | v0.4.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0007 | v0.5.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0009 | v0.5.0 | yes | yes | yes | yes | yes | yes | yes | NON_EXECUTABLE |
| snapshot-0011 | v0.5.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0010 | v0.6.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0012 | v0.6.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0013 | v0.6.0 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |
| snapshot-0014 | v0.7.1 | yes | yes | yes | yes | yes | yes | yes | LIKELY_EXECUTABLE |

## Scheduler state transitions

```text
pending -> running/claimed -> done
                    \-> failure -> retry/requeue when represented -> terminal failure
```

The diagram is a union interpretation, not a claim that every variant has identical transitions. Candidate status and queue/knowledge state occur from v0.1.0. `claimNextCandidate` is explicit from v0.2.0. Attempts/requeue/backoff become explicit in later occurrences. Cancellation signals appear, but stop guarantees remain unproved.

## Boundedness and convergence

Resource mechanisms include worker limits, retry/attempt limits, depth/body/frontier controls, timeouts, and per-origin controls in varying combinations. They bound particular operations; they do not prove global termination, exhaustive coverage, fairness, or convergence. Duplicate suppression is stateful but not proved atomic in every variant.

## Complexity and stability

Provider and model counts increase, but variants make growth non-monotonic. No composite maturity score is computed: execution, validation, contracts, security, and algorithmic closure remain independent.
