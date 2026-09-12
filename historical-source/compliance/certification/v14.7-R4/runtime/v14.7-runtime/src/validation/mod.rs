pub mod authority;
pub mod freshness;
pub mod integrity;
pub mod policy;
pub mod reference;
pub mod scope;
pub mod structural;
pub mod temporal;

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ValidationError {
    Structural(String), Reference(String), Integrity(String), Temporal(String), Scope(String),
    Policy(String), Authority(String), Evidence(String), Freshness(String),
}
