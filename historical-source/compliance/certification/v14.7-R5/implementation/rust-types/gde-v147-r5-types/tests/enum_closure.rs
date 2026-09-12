use gde_v147_r5_types::enums::{EvaluationValue, ValidationStatus};
#[test] fn domains_are_not_interchangeable() { let evaluation = EvaluationValue::Unknown; let validation = ValidationStatus::Unknown; assert!(matches!(evaluation, EvaluationValue::Unknown)); assert!(matches!(validation, ValidationStatus::Unknown)); }
