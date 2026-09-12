use crate::domain::{authority::AuthorityQualification, release::ReleaseEligibility};
use super::AuthorizationResult;
pub fn authorize(eligibility: ReleaseEligibility, authority: AuthorityQualification, policy_valid: bool, scope_valid: bool, credential_valid: bool, temporal_valid: bool, threshold_valid: bool) -> AuthorizationResult {
    if eligibility == ReleaseEligibility::Eligible && authority == AuthorityQualification::Qualified && policy_valid && scope_valid && credential_valid && temporal_valid && threshold_valid { AuthorizationResult::Authorized } else if eligibility == ReleaseEligibility::Ineligible { AuthorizationResult::Denied } else { AuthorizationResult::Blocked }
}
