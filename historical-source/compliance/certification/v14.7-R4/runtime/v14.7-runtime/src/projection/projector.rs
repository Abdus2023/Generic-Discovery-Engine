use std::collections::BTreeMap;
use crate::events::{event::CommittedEvent, ordering::ordered};
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CurrentState(pub BTreeMap<String, String>);
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ProjectionError { InvalidHistory }
pub fn project(history: &[CommittedEvent], _profile_ref: &str) -> Result<CurrentState, ProjectionError> {
    let mut state = BTreeMap::new();
    for committed in ordered(history) { state.insert(committed.event.transition.0.event_type.clone(), committed.event.transition.0.event_id.clone()); }
    Ok(CurrentState(state))
}
