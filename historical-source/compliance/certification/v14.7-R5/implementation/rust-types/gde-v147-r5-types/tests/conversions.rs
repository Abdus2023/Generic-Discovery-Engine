use gde_v147_r5_types::conversions::validation_to_evaluation_eligibility;
use gde_v147_r5_types::enums::ValidationStatus;
#[test] fn only_valid_is_evaluation_eligible() { assert!(validation_to_evaluation_eligibility(ValidationStatus::Valid).is_ok()); assert!(validation_to_evaluation_eligibility(ValidationStatus::Unknown).is_err()); }
