#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ExecutionId(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ExecutionStatus { Succeeded, Failed, Blocked, Unknown }
