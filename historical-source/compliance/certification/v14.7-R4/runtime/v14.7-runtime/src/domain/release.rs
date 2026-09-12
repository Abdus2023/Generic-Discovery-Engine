#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ReleaseId(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ReleaseEligibility { Eligible, Ineligible, Blocked, Unknown }
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ReuseResult { Reusable, NotReusable, Blocked, Unknown, Invalid }
