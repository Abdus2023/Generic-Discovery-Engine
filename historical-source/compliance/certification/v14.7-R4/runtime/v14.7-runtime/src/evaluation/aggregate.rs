use crate::domain::evaluation::{EmptyMandatoryAction, EvaluationValue};
use super::EvaluationError;
pub fn aggregate(results: &[EvaluationValue], empty: EmptyMandatoryAction) -> Result<EvaluationValue, EvaluationError> {
    if results.is_empty() { return Ok(match empty { EmptyMandatoryAction::Allow => EvaluationValue::True, EmptyMandatoryAction::Deny => EvaluationValue::False, EmptyMandatoryAction::Block => EvaluationValue::Blocked, EmptyMandatoryAction::Unknown => EvaluationValue::Unknown }); }
    if results.contains(&EvaluationValue::Invalid) { return Err(EvaluationError::InvalidPredicate); }
    if results.contains(&EvaluationValue::False) { return Ok(EvaluationValue::False); }
    if results.contains(&EvaluationValue::Blocked) { return Ok(EvaluationValue::Blocked); }
    if results.contains(&EvaluationValue::Unknown) { return Ok(EvaluationValue::Unknown); }
    Ok(EvaluationValue::True)
}
