use v14_7_runtime::domain::evaluation::{EmptyMandatoryAction, EvaluationValue};
use v14_7_runtime::evaluation::aggregate::aggregate;
#[test] fn false_dominates_true() { assert_eq!(aggregate(&[EvaluationValue::True, EvaluationValue::False], EmptyMandatoryAction::Deny).unwrap(), EvaluationValue::False); }
#[test] fn empty_action_is_explicit() { assert_eq!(aggregate(&[], EmptyMandatoryAction::Deny).unwrap(), EvaluationValue::False); }
