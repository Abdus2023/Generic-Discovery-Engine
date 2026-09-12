# Concurrency Safety History

`DERIVED SECURITY MODEL — NOT HISTORICAL SOURCE`

Synchronous JavaScript claim mutation is event-loop-local. Await boundaries, callbacks, threads, processes, and distributed workers are not covered.

| Snapshot | Claim | Atomicity | Ownership | Processing | Completion | Failure | Requeue |
|---|---|---|---|---|---|---|---|
| snapshot-0001 | NOT_EVIDENCED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | NOT_EVIDENCED |
| snapshot-0003 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | NOT_EVIDENCED |
| snapshot-0005 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | IMPLEMENTED |
| snapshot-0006 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | IMPLEMENTED |
| snapshot-0008 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | IMPLEMENTED |
| snapshot-0007 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | IMPLEMENTED |
| snapshot-0009 | KnowledgeBase.claimNext | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.complete | KnowledgeBase.fail | IMPLEMENTED |
| snapshot-0011 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | IMPLEMENTED |
| snapshot-0010 | KnowledgeBase.claimNext | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.complete | KnowledgeBase.fail | IMPLEMENTED |
| snapshot-0012 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | IMPLEMENTED |
| snapshot-0013 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | KnowledgeBase.completeCandidate | KnowledgeBase.failCandidate | IMPLEMENTED |
| snapshot-0014 | KnowledgeBase.claimNextCandidate | SYNCHRONOUS_EVENT_LOOP_LOCAL_SEQUENCE | SUPPORTED_LOCAL_CLAIM_SET_OR_QUEUE_REMOVAL | SUPPORTED_FOR_RECOVERED_WORKER_PATH | UNKNOWN | UNKNOWN | CONFIGURED_WITHOUT_COMPLETE_PATH_PROOF |
