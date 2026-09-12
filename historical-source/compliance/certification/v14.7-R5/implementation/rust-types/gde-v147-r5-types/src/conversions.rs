use crate::enums::{AuthorizationStatus, ConformanceStatus, EvaluationValue, ReleaseEligibility, ValidationStatus};
#[derive(Clone, Copy, Debug, Eq, PartialEq)] pub struct EvaluationEligible;
#[derive(Clone, Copy, Debug, Eq, PartialEq)] pub struct PredicateOutcome(pub EvaluationValue);
#[derive(Clone, Copy, Debug, Eq, PartialEq)] pub struct AggregateEvaluation(pub EvaluationValue);
#[derive(Clone, Copy, Debug, Eq, PartialEq)] pub struct AuthorizationInput;
#[derive(Clone, Copy, Debug, Eq, PartialEq)] pub struct ReleaseDecisionInput;
#[derive(Clone, Copy, Debug, Eq, PartialEq)] pub enum ConversionError { InvalidSource, MissingEvidence, PolicyRequired }
pub fn validation_to_evaluation_eligibility(value: ValidationStatus) -> Result<EvaluationEligible, ConversionError> { match value { ValidationStatus::Valid => Ok(EvaluationEligible), _ => Err(ConversionError::InvalidSource) } }
pub fn evaluation_to_predicate_outcome(value: EvaluationValue) -> Result<PredicateOutcome, ConversionError> { if value == EvaluationValue::Invalid { Err(ConversionError::InvalidSource) } else { Ok(PredicateOutcome(value)) } }
pub fn predicate_outcome_to_aggregate(value: PredicateOutcome) -> AggregateEvaluation { AggregateEvaluation(value.0) }
pub fn aggregate_to_release_eligibility(value: AggregateEvaluation) -> Result<ReleaseEligibility, ConversionError> { match value.0 { EvaluationValue::True => Ok(ReleaseEligibility::Eligible), EvaluationValue::False => Ok(ReleaseEligibility::Ineligible), EvaluationValue::Blocked => Ok(ReleaseEligibility::Blocked), EvaluationValue::Unknown => Ok(ReleaseEligibility::Unknown), EvaluationValue::Invalid => Err(ConversionError::InvalidSource) } }
pub fn conformance_to_compliance(value: ConformanceStatus) -> ConformanceStatus { value }
pub fn release_eligibility_to_authorization_input(value: ReleaseEligibility) -> Result<AuthorizationInput, ConversionError> { if value == ReleaseEligibility::Eligible { Ok(AuthorizationInput) } else { Err(ConversionError::InvalidSource) } }
pub fn authorization_to_decision_input(value: AuthorizationStatus) -> Result<ReleaseDecisionInput, ConversionError> { if value == AuthorizationStatus::Authorized { Ok(ReleaseDecisionInput) } else { Err(ConversionError::InvalidSource) } }
