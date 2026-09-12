use super::ValidationError;
pub fn validate(fresh: bool) -> Result<(), ValidationError> { if fresh { Ok(()) } else { Err(ValidationError::Freshness("stale evidence".into())) } }
