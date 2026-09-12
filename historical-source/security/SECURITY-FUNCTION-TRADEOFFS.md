# Security / Function Tradeoffs

Controls can bound authority or work while reducing discovery completeness. No effect was measured and no generic superiority score is assigned.

| Snapshot | Control | Safety effect | Discovery effect | Measured |
|---|---|---|---|---|
| snapshot-0001 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0001 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0001 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0001 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0003 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0003 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0003 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0003 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0005 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0005 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0005 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0005 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0006 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0006 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0006 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0006 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0006 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0008 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0008 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0008 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0008 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0008 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0007 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0007 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0007 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0007 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0007 | maxResponseBytes | bounded response retention/parsing | truncation can hide late content | NOT_MEASURED |
| snapshot-0007 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0007 | maxUrlsPerDiscovery | bounded per-discovery fanout | additional URLs can be omitted | NOT_MEASURED |
| snapshot-0009 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0009 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0009 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0009 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0009 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0011 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0011 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0011 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0011 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0011 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0010 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0010 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0010 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0010 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0010 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0012 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0012 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0012 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0012 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0012 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0012 | maxRequestsPerOrigin | bounded per-origin authority/use | origin coverage can be capped | NOT_MEASURED |
| snapshot-0012 | minRequestInterval | reduced request pressure | scan takes longer | NOT_MEASURED |
| snapshot-0013 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0013 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0013 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0013 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0013 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0013 | maxRequestsPerOrigin | bounded per-origin authority/use | origin coverage can be capped | NOT_MEASURED |
| snapshot-0013 | minRequestInterval | reduced request pressure | scan takes longer | NOT_MEASURED |
| snapshot-0014 | maxCandidates | bounded candidate memory/work | candidate discoveries beyond the cap may be rejected | NOT_MEASURED |
| snapshot-0014 | maxRequests | bounded acquisition work | scan completeness is capped | NOT_MEASURED |
| snapshot-0014 | concurrency | bounded concurrent workers | lower parallelism can increase completion time | NOT_MEASURED |
| snapshot-0014 | requestTimeout | bounded request wait | slow resources may be classified as failure | NOT_MEASURED |
| snapshot-0014 | maxBodyChars | bounded response retention/parsing | truncation can hide late content | NOT_MEASURED |
| snapshot-0014 | maxDepth | bounded recursive expansion | deeper discoveries can be omitted | NOT_MEASURED |
| snapshot-0014 | maxRequestsPerOrigin | bounded per-origin authority/use | origin coverage can be capped | NOT_MEASURED |
| snapshot-0014 | minRequestInterval | reduced request pressure | scan takes longer | NOT_MEASURED |
| snapshot-0001 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0003 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0005 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0006 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0008 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0007 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0009 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0011 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0010 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0012 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0013 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
| snapshot-0014 | sameOriginOnly | restricts default cross-origin acquisition scope | cross-origin discoveries may not be acquired | NOT_MEASURED |
