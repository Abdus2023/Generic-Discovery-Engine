use super::evidence::EvidenceId;
use crate::identity::hashing::ContentHash;
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ValidationId(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ValidationStatus { Valid, Invalid, Blocked, Unknown }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidationResult {
    pub validation_id: ValidationId,
    pub subject_ref: String,
    pub status: ValidationStatus,
    pub failure_codes: Vec<String>,
    pub evidence_refs: Vec<EvidenceId>,
    pub validator_id: String,
    pub scope_ref: String,
    pub input_hash: ContentHash,
    pub validated_at: String,
    pub content_hash: ContentHash,
}
