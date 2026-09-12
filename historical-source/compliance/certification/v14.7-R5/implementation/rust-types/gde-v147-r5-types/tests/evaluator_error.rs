use gde_v147_r5_types::evaluator::{default_disposition, ErrorDisposition, EvaluatorError};
#[test] fn evaluator_error_defaults_to_failure() { assert_eq!(default_disposition(EvaluatorError::EvaluatorTimeout), ErrorDisposition::EvaluationFailure); }
