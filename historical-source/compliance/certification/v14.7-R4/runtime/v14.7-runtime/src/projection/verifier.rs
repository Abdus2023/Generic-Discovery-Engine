use super::projector::CurrentState;
pub fn verify(expected: &CurrentState, actual: &CurrentState) -> bool { expected == actual }
