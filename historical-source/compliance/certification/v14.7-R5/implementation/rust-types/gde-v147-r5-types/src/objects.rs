use crate::enums::*;
use crate::ids::*;
#[derive(Clone, Debug, Eq, PartialEq)] pub struct ValidationResult { pub validation_id: ValidationId, pub subject_ref: String, pub status: ValidationStatus, pub content_hash: [u8; 32] }
#[derive(Clone, Debug, Eq, PartialEq)] pub struct ConformanceResult { pub requirement_ref: RequirementId, pub status: ConformanceStatus, pub evaluation_refs: Vec<EvaluationId>, pub evidence_refs: Vec<EvidenceId>, pub content_hash: [u8; 32] }
#[derive(Clone, Debug, Eq, PartialEq)] pub struct AuthorizationResult { pub authority_ref: AuthorityId, pub release_ref: ReleaseId, pub status: AuthorizationStatus, pub content_hash: [u8; 32] }
