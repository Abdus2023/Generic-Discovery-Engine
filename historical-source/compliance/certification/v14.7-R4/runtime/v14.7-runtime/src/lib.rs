#![forbid(unsafe_code)]
//! Reference domain model for the frozen v14.7-R4 realization profile.

pub mod authorization;
pub mod conformance;
pub mod domain;
pub mod evaluation;
pub mod events;
pub mod identity;
pub mod projection;
pub mod state;
pub mod validation;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RawSubject {
    pub subject_ref: String,
    pub payload: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidatedSubject {
    subject_ref: String,
    payload: String,
}

impl ValidatedSubject {
    pub(crate) fn new(raw: RawSubject) -> Self {
        Self { subject_ref: raw.subject_ref, payload: raw.payload }
    }
    pub fn subject_ref(&self) -> &str { &self.subject_ref }
    pub fn payload(&self) -> &str { &self.payload }
}
