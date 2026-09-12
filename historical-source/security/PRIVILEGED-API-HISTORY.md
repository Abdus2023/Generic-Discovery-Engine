# Privileged API Boundary History

Permissions, callers, outbound data, inbound data, and error crossings are separate. Platform semantics were not historically executed.

| Snapshot | API | Caller | Permission | Outbound | Inbound | Errors |
|---|---|---|---|---|---|---|
| snapshot-0001 | GM_xmlhttpRequest | HttpAcquisitionAdapter.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0001 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0001 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0001 | fetch | HttpAcquisitionAdapter.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0001 | localStorage | KnowledgeBase.persist | BROWSER_AMBIENT | storage key/value | persisted value | throw/catch path |
| snapshot-0003 | GM_xmlhttpRequest | HttpAcquisitionAdapter.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0003 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0003 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0003 | fetch | HttpAcquisitionAdapter.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0003 | localStorage | KnowledgeBase.persist | BROWSER_AMBIENT | storage key/value | persisted value | throw/catch path |
| snapshot-0005 | GM_xmlhttpRequest | HttpAcquisitionAdapter.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0005 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0005 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0005 | fetch | HttpAcquisitionAdapter.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0005 | localStorage | KnowledgeBase.persist | BROWSER_AMBIENT | storage key/value | persisted value | throw/catch path |
| snapshot-0006 | GM_xmlhttpRequest | HttpAcquisitionAdapter.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0006 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0006 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0006 | fetch | HttpAcquisitionAdapter.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0006 | localStorage | KnowledgeBase.persist | BROWSER_AMBIENT | storage key/value | persisted value | throw/catch path |
| snapshot-0008 | GM_xmlhttpRequest | HttpAcquisitionAdapter.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0008 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0008 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0008 | fetch | HttpAcquisitionAdapter.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0008 | localStorage | KnowledgeBase.persist | BROWSER_AMBIENT | storage key/value | persisted value | throw/catch path |
| snapshot-0007 | GM_xmlhttpRequest | HttpAcquisitionAdapter.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0007 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0007 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0007 | fetch | HttpAcquisitionAdapter.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0007 | localStorage | KnowledgeBase.persist | BROWSER_AMBIENT | storage key/value | persisted value | throw/catch path |
| snapshot-0009 | GM_xmlhttpRequest | HttpAcquisition.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0009 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0009 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0009 | fetch | HttpAcquisition.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0011 | GM_xmlhttpRequest | HttpAcquisitionAdapter.acquire | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0011 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0011 | GM_setValue | KnowledgeBase.persistNow | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0011 | fetch | HttpAcquisitionAdapter.acquireFetch | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0010 | GM_xmlhttpRequest | HttpAcquisition.acquire | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0010 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0010 | GM_setValue | KnowledgeBase.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0010 | fetch | HttpAcquisition.fetchRequest | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0012 | GM_xmlhttpRequest | HttpAcquisitionAdapter.acquire | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0012 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0012 | GM_setValue | KnowledgeBase.persistNow | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0012 | fetch | HttpAcquisitionAdapter.acquireFetch | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0013 | GM_xmlhttpRequest | TOP_LEVEL.gmRequest | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0013 | GM_getValue | KnowledgeBase.load | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0013 | GM_setValue | KnowledgeBase.persistSoon | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0013 | fetch | TOP_LEVEL.fetchRequest | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
| snapshot-0014 | GM_xmlhttpRequest | Acquisition.request | EXPLICIT_GRANT | network request metadata/body | response/status/headers/body | callback or rejection |
| snapshot-0014 | GM_getValue | GenericDiscoveryEngine.restore | EXPLICIT_GRANT | storage key/default | persisted value | throw/catch path |
| snapshot-0014 | GM_setValue | GenericDiscoveryEngine.persist | EXPLICIT_GRANT | storage key/serialized state | storage side effect | throw/catch path |
| snapshot-0014 | fetch | Acquisition.request | BROWSER_AMBIENT | URL/request options | Response object/body | Promise rejection |
