use super::ValidationError;
pub fn validate(requested: &[String], granted: &[String]) -> Result<(), ValidationError> {
    if requested.iter().all(|item| granted.contains(item)) { Ok(()) } else { Err(ValidationError::Scope("out of scope".into())) }
}
