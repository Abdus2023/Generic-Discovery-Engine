use super::evaluation::EmptyMandatoryAction;
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ProfileId(pub String);
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ImplementationId(pub String);
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Profile {
    pub profile_id: ProfileId,
    pub profile_version: String,
    pub specification_hash: String,
    pub empty_mandatory_action: EmptyMandatoryAction,
}
