#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct RequirementId(pub String);
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ConditionRef(pub String);
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum NormativeStrength { Must, MustNot, Should, ShouldNot, May }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Requirement {
    pub requirement_id: RequirementId,
    pub statement: String,
    pub strength: NormativeStrength,
    pub acceptance_criteria: Vec<ConditionRef>,
}
