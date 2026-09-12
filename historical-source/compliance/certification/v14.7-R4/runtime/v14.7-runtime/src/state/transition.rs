#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CurrentState { pub state: String, pub last_event: Option<String>, pub allowed_events: Vec<String> }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct StateTransitionEvent { pub event_id: String, pub event_type: String, pub predecessor: Option<String>, pub evidence_valid: bool, pub authority_valid: bool, pub scope_valid: bool, pub temporal_valid: bool }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidatedTransition(pub(crate) StateTransitionEvent);
impl ValidatedTransition { pub fn event(&self) -> &StateTransitionEvent { &self.0 } }
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum TransitionError { InvalidEvidence, InvalidAuthority, InvalidScope, InvalidTemporalContext, InvalidPredecessor, IllegalTransition }
