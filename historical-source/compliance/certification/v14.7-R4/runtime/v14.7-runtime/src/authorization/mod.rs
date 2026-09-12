pub mod authorize;
pub mod qualification;
pub mod threshold;
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorizationResult { Authorized, Denied, Blocked, Unknown, Invalid }
