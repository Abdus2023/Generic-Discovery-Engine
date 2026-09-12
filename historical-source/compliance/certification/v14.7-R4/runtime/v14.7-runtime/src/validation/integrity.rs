use super::ValidationError;
pub fn validate(matches: bool) -> Result<(), ValidationError> { if matches { Ok(()) } else { Err(ValidationError::Integrity("hash mismatch".into())) } }
