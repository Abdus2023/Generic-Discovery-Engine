use crate::domain::conformance::{ConformanceResult, ConformanceStatus};
use crate::domain::evidence::EvidenceId;
use crate::domain::evaluation::{EvaluationResult, EvaluationValue};
use crate::domain::requirement::Requirement;
use crate::identity::hashing::ContentHash;
use super::vectors::TestVector;
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ConformanceError { InvalidEvaluation, MissingAcceptanceCriterion }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct OracleResult { pub test_id: String, pub passed: bool, pub actual: String }
pub fn compare(vector: &TestVector, actual: String) -> OracleResult { OracleResult { test_id: vector.test_id.clone(), passed: actual == vector.expected, actual } }
pub fn assess_requirement(requirement: &Requirement, evaluations: &[EvaluationResult], evidence_refs: Vec<EvidenceId>) -> Result<ConformanceResult, ConformanceError> {
    if evaluations.iter().any(|item| item.result == EvaluationValue::Invalid) { return Err(ConformanceError::InvalidEvaluation); }
    if evidence_refs.is_empty() { return Ok(ConformanceResult { requirement_ref: requirement.requirement_id.clone(),
        status: ConformanceStatus::Unverified, evaluation_refs: evaluations.iter().map(|item| item.evaluation_id.clone()).collect(),
        evidence_refs, violated_conditions: vec![], rationale_codes: vec![], content_hash: ContentHash::zero() }); }
    let mut status = ConformanceStatus::Conformant;
    let mut violated_conditions = vec![];
    if evaluations.iter().any(|item| item.result == EvaluationValue::False) {
        let condition = requirement.acceptance_criteria.first().cloned().ok_or(ConformanceError::MissingAcceptanceCriterion)?;
        violated_conditions.push(condition); status = ConformanceStatus::NonConformant;
    } else if evaluations.iter().any(|item| item.result == EvaluationValue::Blocked) { status = ConformanceStatus::Blocked; }
    else if evaluations.iter().any(|item| item.result == EvaluationValue::Unknown) { status = ConformanceStatus::Unknown; }
    Ok(ConformanceResult { requirement_ref: requirement.requirement_id.clone(), status,
        evaluation_refs: evaluations.iter().map(|item| item.evaluation_id.clone()).collect(), evidence_refs,
        violated_conditions, rationale_codes: vec![], content_hash: ContentHash::zero() })
}
