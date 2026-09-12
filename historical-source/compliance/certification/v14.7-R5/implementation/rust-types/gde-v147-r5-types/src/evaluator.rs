use crate::enums::EvaluationValue;
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EvaluatorError { InvalidPredicate, InvalidSubject, InvalidContext, ValidationRequired, ValidationFailed, UnsupportedPredicate, EvaluatorFailure, EvaluatorTimeout, EvaluatorResourceFailure, EvaluatorInternalFailure, OutputInvalid, EvaluatorDependencyUnavailable }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EvaluationResult { pub evaluation_id: crate::ids::EvaluationId, pub predicate_ref: crate::ids::PredicateId, pub value: EvaluationValue, pub content_hash: [u8; 32] }
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum EvaluationCompletion { Result(EvaluationResult), Error(EvaluatorError) }
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ErrorDisposition { EvaluationFailure, Unknown, Blocked, Invalid }
pub fn default_disposition(_error: EvaluatorError) -> ErrorDisposition { ErrorDisposition::EvaluationFailure }
