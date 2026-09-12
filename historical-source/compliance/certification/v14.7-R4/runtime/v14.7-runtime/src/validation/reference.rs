use super::ValidationError;
pub fn validate(exists: bool) -> Result<(), ValidationError> { if exists { Ok(()) } else { Err(ValidationError::Reference("missing reference".into())) } }
