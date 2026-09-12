use crate::ValidatedSubject;
use crate::domain::evaluation::{EvaluationId, EvaluationResult, EvaluationValue, PredicateId};
use crate::identity::hashing::ContentHash;
use super::{EvaluationError, predicate::Predicate};
pub trait Evaluator {
    fn identity(&self) -> (&str, &str);
    fn evaluate(&self, predicate: &Predicate, subject: &ValidatedSubject, context_ref: &str) -> Result<EvaluationResult, EvaluationError>;
}
pub struct ReferenceEvaluator;
impl Evaluator for ReferenceEvaluator {
    fn identity(&self) -> (&str, &str) { ("v14.7-reference", "14.7-R4") }
    fn evaluate(&self, predicate: &Predicate, subject: &ValidatedSubject, context_ref: &str) -> Result<EvaluationResult, EvaluationError> {
        if context_ref.is_empty() { return Err(EvaluationError::EvaluationContextInvalid); }
        let value = match predicate { Predicate::AlwaysTrue => EvaluationValue::True, Predicate::AlwaysFalse => EvaluationValue::False, Predicate::Unknown => EvaluationValue::Unknown, Predicate::Blocked => EvaluationValue::Blocked };
        Ok(EvaluationResult { evaluation_id: EvaluationId("reference".into()), subject_ref: subject.subject_ref().into(), predicate_ref: PredicateId("predicate".into()), result: value, reason_codes: vec![], evidence_refs: vec![], input_refs: vec![], evaluator_id: self.identity().0.into(), evaluator_version: self.identity().1.into(), scope_ref: context_ref.into(), freshness: "FRESH".into(), integrity: "VALID".into(), evaluated_at: "1970-01-01T00:00:00Z".into(), sequence_no: 0, content_hash: ContentHash::zero() })
    }
}
