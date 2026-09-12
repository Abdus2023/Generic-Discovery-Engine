#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct EvidenceId(pub String);
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Evidence {
    pub evidence_id: EvidenceId,
    pub subject_ref: String,
    pub observation: String,
    pub integrity_valid: bool,
}
