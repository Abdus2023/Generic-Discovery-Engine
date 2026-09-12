use super::oracle::OracleResult;
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ConformanceReport { pub profile_id: String, pub implementation_id: String, pub vector_identity: String, pub results: Vec<OracleResult>, pub executed_at: String, pub harness_version: String }
