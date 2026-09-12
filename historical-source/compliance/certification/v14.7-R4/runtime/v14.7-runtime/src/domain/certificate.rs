#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct CertificateId(pub String);
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Certificate { pub certificate_id: CertificateId, pub subject_hash: String, pub valid: bool }
