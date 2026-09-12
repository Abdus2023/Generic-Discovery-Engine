#[derive(Clone, Debug, Eq, PartialEq)]
pub struct TestVector { pub test_id: String, pub profile_ref: String, pub requirement_refs: Vec<String>, pub operation: String, pub expected: String }
