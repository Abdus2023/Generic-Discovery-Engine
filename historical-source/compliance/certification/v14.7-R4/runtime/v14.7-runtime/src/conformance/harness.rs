use super::{oracle::{compare, OracleResult}, vectors::TestVector};
pub fn run_conformance<F>(vectors: &[TestVector], operation: F) -> Vec<OracleResult> where F: Fn(&TestVector) -> String { vectors.iter().map(|vector| compare(vector, operation(vector))).collect() }
