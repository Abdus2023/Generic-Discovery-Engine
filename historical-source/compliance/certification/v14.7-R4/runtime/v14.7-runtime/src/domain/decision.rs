use super::release::{ReleaseId, ReuseResult};
use crate::identity::hashing::ContentHash;
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct DecisionId(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum DecisionStatus { Approved, Rejected, Blocked, Deferred }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DecisionBasis {
    pub release_id: ReleaseId, pub artifact_hash: String, pub implementation_id: String,
    pub specification_hash: String, pub audit_snapshot_hash: String, pub certificate_id: String,
    pub gate_hash: String, pub policy_hash: String, pub environment_hash: String, pub evidence_hash: String,
    pub authority_context_hash: String, pub waiver_hash: String, pub security_context_hash: String,
    pub compatibility_context_hash: String, pub temporal_context: String, pub content_hash: ContentHash,
}
pub fn check_decision_reuse(old_basis: &DecisionBasis, new_basis: &DecisionBasis, constraints_valid: bool) -> ReuseResult {
    if !constraints_valid { ReuseResult::Blocked }
    else if old_basis.content_hash == new_basis.content_hash { ReuseResult::Reusable }
    else { ReuseResult::NotReusable }
}
