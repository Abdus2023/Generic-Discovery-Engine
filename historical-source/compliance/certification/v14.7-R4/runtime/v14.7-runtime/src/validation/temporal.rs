use super::ValidationError;
pub fn validate(now: u64, not_before: u64, not_after: Option<u64>) -> Result<(), ValidationError> {
    if now < not_before || not_after.map(|end| now >= end).unwrap_or(false) { Err(ValidationError::Temporal("outside interval".into())) } else { Ok(()) }
}
