# Security → Architecture Map

Chronological correlation is not causality. No boundary is claimed to have been caused by a concern unless explicit motivation evidence exists.

| Concern | Mechanism | Boundary | Causality | Explicit motivation |
|---|---|---|---|---|
| provider failures | ProviderRegistry catch path | provider boundary | CORRELATED | NOT_EVIDENCED |
| resource exhaustion | configured/enforced limits | scheduler/acquisition boundary | CORRELATED | NOT_EVIDENCED |
| duplicate processing | key/visited/claimed state | KnowledgeBase/scheduler boundary | CORRELATED | NOT_EVIDENCED |
| untrusted remote data | acquisition then parser/provider | acquisition/provider data boundary | CORRELATED | NOT_EVIDENCED |
| persistence failure | local persistence catch | storage boundary | CORRELATED | NOT_EVIDENCED |

## Comparative security-boundary migration

Movement is comparative; parentage and security consequence remain UNKNOWN.

| Operation | Before | After | Boundary before | Boundary after | Classification |
|---|---|---|---|---|---|
| candidate claim | snapshot-0006 | snapshot-0009 | KnowledgeBase.claimNextCandidate | KnowledgeBase.claimNext | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate claim | snapshot-0008 | snapshot-0009 | KnowledgeBase.claimNextCandidate | KnowledgeBase.claimNext | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate claim | snapshot-0007 | snapshot-0010 | KnowledgeBase.claimNextCandidate | KnowledgeBase.claimNext | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate claim | snapshot-0009 | snapshot-0012 | KnowledgeBase.claimNext | KnowledgeBase.claimNextCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate claim | snapshot-0009 | snapshot-0013 | KnowledgeBase.claimNext | KnowledgeBase.claimNextCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate claim | snapshot-0011 | snapshot-0010 | KnowledgeBase.claimNextCandidate | KnowledgeBase.claimNext | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate claim | snapshot-0010 | snapshot-0014 | KnowledgeBase.claimNext | KnowledgeBase.claimNextCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate insertion | snapshot-0005 | snapshot-0006 | KnowledgeBase.addCandidate | ProvenanceGraph.addCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate insertion | snapshot-0006 | snapshot-0009 | ProvenanceGraph.addCandidate | KnowledgeBase.addCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate insertion | snapshot-0006 | snapshot-0011 | ProvenanceGraph.addCandidate | KnowledgeBase.addCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate insertion | snapshot-0008 | snapshot-0007 | KnowledgeBase.addCandidate | ProvenanceGraph.addCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate insertion | snapshot-0007 | snapshot-0010 | ProvenanceGraph.addCandidate | KnowledgeBase.addCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate insertion | snapshot-0007 | snapshot-0012 | ProvenanceGraph.addCandidate | KnowledgeBase.addCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| candidate insertion | snapshot-0007 | snapshot-0013 | ProvenanceGraph.addCandidate | KnowledgeBase.addCandidate | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0006 | snapshot-0009 | HttpAcquisitionAdapter.request | HttpAcquisition.request | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0006 | snapshot-0011 | HttpAcquisitionAdapter.request | HttpAcquisitionAdapter.acquire | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0008 | snapshot-0009 | HttpAcquisitionAdapter.request | HttpAcquisition.request | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0008 | snapshot-0011 | HttpAcquisitionAdapter.request | HttpAcquisitionAdapter.acquire | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0007 | snapshot-0010 | HttpAcquisitionAdapter.request | HttpAcquisition.acquire | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0007 | snapshot-0012 | HttpAcquisitionAdapter.request | HttpAcquisitionAdapter.acquire | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0007 | snapshot-0013 | HttpAcquisitionAdapter.request | TOP_LEVEL.gmRequest | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0009 | snapshot-0010 | HttpAcquisition.request | HttpAcquisition.acquire | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0009 | snapshot-0012 | HttpAcquisition.request | HttpAcquisitionAdapter.acquire | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0009 | snapshot-0013 | HttpAcquisition.request | TOP_LEVEL.gmRequest | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0011 | snapshot-0010 | HttpAcquisitionAdapter.acquire | HttpAcquisition.acquire | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0011 | snapshot-0013 | HttpAcquisitionAdapter.acquire | TOP_LEVEL.gmRequest | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0010 | snapshot-0014 | HttpAcquisition.acquire | Acquisition.request | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0012 | snapshot-0014 | HttpAcquisitionAdapter.acquire | Acquisition.request | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
| network request | snapshot-0013 | snapshot-0014 | TOP_LEVEL.gmRequest | Acquisition.request | COMPARATIVE_MOVEMENT_NOT_PROVED_LINEAGE |
