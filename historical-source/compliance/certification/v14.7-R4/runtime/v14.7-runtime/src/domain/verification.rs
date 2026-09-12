#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct VerificationId(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum VerificationStatus { Verified, Failed, Blocked, Unknown }
