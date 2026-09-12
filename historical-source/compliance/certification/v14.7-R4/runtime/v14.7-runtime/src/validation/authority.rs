use super::ValidationError;
pub fn validate(valid: bool) -> Result<(), ValidationError> { if valid { Ok(()) } else { Err(ValidationError::Authority("invalid authority".into())) } }
