#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct AuthorityId(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorityQualification { Qualified, Unqualified, Blocked, Unknown, Invalid }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Authority {
    pub authority_id: AuthorityId,
    pub active: bool,
    pub operations: Vec<String>,
    pub scopes: Vec<String>,
    pub not_before: u64,
    pub not_after: Option<u64>,
    pub threshold: usize,
}
