use super::evidence::EvidenceId;
use crate::identity::hashing::ContentHash;
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct PredicateId(pub String);
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct EvaluationId(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EvaluationValue { True, False, Unknown, Blocked, Invalid }
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EmptyMandatoryAction { Allow, Deny, Block, Unknown }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EvaluationResult {
    pub evaluation_id: EvaluationId,
    pub subject_ref: String,
    pub predicate_ref: PredicateId,
    pub result: EvaluationValue,
    pub reason_codes: Vec<String>,
    pub evidence_refs: Vec<EvidenceId>,
    pub input_refs: Vec<String>,
    pub evaluator_id: String,
    pub evaluator_version: String,
    pub scope_ref: String,
    pub freshness: String,
    pub integrity: String,
    pub evaluated_at: String,
    pub sequence_no: u64,
    pub content_hash: ContentHash,
}
