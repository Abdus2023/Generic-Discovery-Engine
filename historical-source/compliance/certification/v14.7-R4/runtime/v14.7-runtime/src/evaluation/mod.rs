pub mod aggregate;
pub mod evaluator;
pub mod predicate;
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum EvaluationError { InvalidPredicate, MissingInput, EvaluatorUnavailable, EvaluationContextInvalid, EvidenceInvalid, InternalFailure }
