use super::ids::*;
pub struct RawSubject { pub subject_ref:String }
pub struct ValidatedSubject { pub subject_ref:String, pub validation_id:ValidationId }
pub struct EligibleRelease { pub release_id:ReleaseId }
pub struct AuthorizedRelease { pub release_id:ReleaseId, pub authority_id:AuthorityId }
pub struct ApprovedRelease { pub release_id:ReleaseId, pub decision_id:DecisionId }
pub struct ExecutedRelease { pub release_id:ReleaseId }
