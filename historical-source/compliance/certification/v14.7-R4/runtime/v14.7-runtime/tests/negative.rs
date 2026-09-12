use v14_7_runtime::RawSubject;
use v14_7_runtime::validation::structural::validate;
#[test] fn empty_subject_is_rejected() { assert!(validate(RawSubject { subject_ref: String::new(), payload: String::new() }).is_err()); }
