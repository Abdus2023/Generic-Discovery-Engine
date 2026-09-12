#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Predicate { AlwaysTrue, AlwaysFalse, Unknown, Blocked }
