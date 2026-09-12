use super::enums::*;
use super::ids::*;
#[derive(Clone,Debug,Eq,PartialEq)] pub struct Scope { pub scope_id:String, pub scope_expression:String }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct EvaluationResult { pub evaluation_id:EvaluationId, pub subject_ref:String, pub evaluator_id:String, pub result:EvaluationValue, pub reason_codes:Vec<String>, pub scope:Scope, pub content_hash:[u8;32] }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct ValidationResult { pub validation_id:ValidationId, pub subject_ref:String, pub status:ValidationStatus, pub content_hash:[u8;32] }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct ConformanceResult { pub requirement_ref:RequirementId, pub status:ConformanceStatus, pub evaluation_refs:Vec<EvaluationId>, pub evidence_refs:Vec<EvidenceId>, pub content_hash:[u8;32] }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct Predicate { pub predicate_id:PredicateId, pub expression:String }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct EvaluationContext { pub profile_ref:ProfileId, pub scope:Scope }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct EvaluatorIdentity { pub implementation_ref:ImplementationId, pub version:String, pub hash:[u8;32] }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct Observation { pub observation_id:ObservationId, pub subject_ref:String, pub value:String }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct Evidence { pub evidence_id:EvidenceId, pub observation_refs:Vec<ObservationId>, pub content_hash:[u8;32] }
