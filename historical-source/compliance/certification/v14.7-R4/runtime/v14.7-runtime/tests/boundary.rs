use v14_7_runtime::RawSubject;
use v14_7_runtime::validation::structural::validate;
#[test] fn raw_requires_validation() { let validated = validate(RawSubject { subject_ref: "subject".into(), payload: "body".into() }).unwrap(); assert_eq!(validated.subject_ref(), "subject"); }
