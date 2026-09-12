use crate::domain::authority::{Authority, AuthorityQualification};
use super::threshold::distinct_valid;
pub fn qualify(authority: &Authority, operation: &str, scope: &str, now: u64, approvals: &[(String, bool)]) -> AuthorityQualification {
    if !authority.active || !authority.operations.iter().any(|item| item == operation) || !authority.scopes.iter().any(|item| item == scope) { return AuthorityQualification::Unqualified; }
    if now < authority.not_before || authority.not_after.map(|end| now >= end).unwrap_or(false) { return AuthorityQualification::Unqualified; }
    if distinct_valid(approvals) < authority.threshold { return AuthorityQualification::Blocked; }
    AuthorityQualification::Qualified
}
