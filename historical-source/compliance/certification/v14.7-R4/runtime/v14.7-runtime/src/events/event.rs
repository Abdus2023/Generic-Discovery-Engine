use crate::state::transition::ValidatedTransition;
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct EventId(pub String);
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidatedEvent { pub(crate) stream_id: String, pub(crate) sequence_no: u64, pub(crate) transition: ValidatedTransition }
impl ValidatedEvent {
    pub fn from_transition(stream_id: String, sequence_no: u64, transition: ValidatedTransition) -> Self { Self { stream_id, sequence_no, transition } }
    pub fn stream_id(&self) -> &str { &self.stream_id }
    pub fn sequence_no(&self) -> u64 { self.sequence_no }
    pub fn transition(&self) -> &ValidatedTransition { &self.transition }
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CommittedEvent { pub event: ValidatedEvent, pub commit_index: u64 }
