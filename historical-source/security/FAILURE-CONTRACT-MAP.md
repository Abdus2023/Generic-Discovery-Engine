# Failure → Contract Map

A failure path maps to a contract requirement and local enforcement; every test column remains UNVERIFIED where no historical test evidence exists.

| Failure | Contract requirement | Enforcement | Test |
|---|---|---|---|
| VALIDATION_FAILURE | validation_failure handling semantics | CATCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| NETWORK_FAILURE | acquisition error semantics | CATCH, ERROR_CALLBACK, PROMISE_REJECT | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| TIMEOUT | timeout/cancellation semantics | CATCH, PROMISE_REJECT, TIMEOUT_CALLBACK | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| HTTP_FAILURE | HTTP result-state semantics | STATUS_BRANCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| PARSING_FAILURE | parser failure representation | CATCH, PARSER_RESULT_CHECK | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| RECOGNITION_FAILURE | recognition_failure handling semantics | CATCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| PROVIDER_FAILURE | provider failure isolation | CATCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| DISCOVERY_FAILURE | discovery_failure handling semantics | CATCH, THROW | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| SCHEDULER_FAILURE | candidate failure ownership and progress | CATCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| PERSISTENCE_FAILURE | persistence integrity and observability | CATCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| UI_FAILURE | ui_failure handling semantics | CATCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
| UNKNOWN_FAILURE | unknown_failure handling semantics | CATCH | UNVERIFIED_NO_HISTORICAL_TEST_EVIDENCE |
