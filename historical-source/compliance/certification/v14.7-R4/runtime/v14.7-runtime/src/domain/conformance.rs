use super::evidence::EvidenceId;
use crate::identity::hashing::ContentHash;
use super::evaluation::EvaluationId;
use super::requirement::{ConditionRef, RequirementId};
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ConformanceStatus { Conformant, PartiallyConformant, NonConformant, Unverified, Blocked, NotApplicable, Unknown }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ConformanceResult {
    pub requirement_ref: RequirementId,
    pub status: ConformanceStatus,
    pub evaluation_refs: Vec<EvaluationId>,
    pub evidence_refs: Vec<EvidenceId>,
    pub violated_conditions: Vec<ConditionRef>,
    pub rationale_codes: Vec<String>,
    pub content_hash: ContentHash,
}
