use super::transition::{CurrentState, StateTransitionEvent, TransitionError, ValidatedTransition};
pub fn guard_transition(current: &CurrentState, event: StateTransitionEvent) -> Result<ValidatedTransition, TransitionError> {
    if !event.evidence_valid { return Err(TransitionError::InvalidEvidence); }
    if !event.authority_valid { return Err(TransitionError::InvalidAuthority); }
    if !event.scope_valid { return Err(TransitionError::InvalidScope); }
    if !event.temporal_valid { return Err(TransitionError::InvalidTemporalContext); }
    if event.predecessor != current.last_event { return Err(TransitionError::InvalidPredecessor); }
    if !current.allowed_events.contains(&event.event_type) { return Err(TransitionError::IllegalTransition); }
    Ok(ValidatedTransition(event))
}
