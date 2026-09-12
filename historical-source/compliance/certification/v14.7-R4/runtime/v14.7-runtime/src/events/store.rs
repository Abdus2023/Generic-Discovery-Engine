use std::collections::BTreeSet;
use std::sync::Mutex;
use super::event::{CommittedEvent, ValidatedEvent};
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum EventStoreError { SequenceCollision, Poisoned }
pub trait EventStore { fn append(&self, event: ValidatedEvent) -> Result<CommittedEvent, EventStoreError>; }
pub struct InMemoryEventStore { inner: Mutex<(BTreeSet<(String, u64)>, Vec<CommittedEvent>)> }
impl InMemoryEventStore { pub fn new() -> Self { Self { inner: Mutex::new((BTreeSet::new(), vec![])) } } }
impl Default for InMemoryEventStore { fn default() -> Self { Self::new() } }
impl EventStore for InMemoryEventStore {
    fn append(&self, event: ValidatedEvent) -> Result<CommittedEvent, EventStoreError> {
        let mut guard = self.inner.lock().map_err(|_| EventStoreError::Poisoned)?;
        let key = (event.stream_id.clone(), event.sequence_no);
        if !guard.0.insert(key) { return Err(EventStoreError::SequenceCollision); }
        let committed = CommittedEvent { event, commit_index: guard.1.len() as u64 };
        guard.1.push(committed.clone()); Ok(committed)
    }
}
