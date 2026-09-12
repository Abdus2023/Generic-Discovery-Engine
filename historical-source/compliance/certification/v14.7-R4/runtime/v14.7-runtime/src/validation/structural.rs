use crate::{RawSubject, ValidatedSubject};
use super::ValidationError;
pub fn validate(raw: RawSubject) -> Result<ValidatedSubject, ValidationError> {
    if raw.subject_ref.is_empty() { return Err(ValidationError::Structural("missing subject_ref".into())); }
    Ok(ValidatedSubject::new(raw))
}
