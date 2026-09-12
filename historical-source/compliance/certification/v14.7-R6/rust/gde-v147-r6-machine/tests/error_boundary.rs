use gde_v147_r6_machine::evaluation::{ErrorSeverity,EvaluationError,EvaluationErrorCode};
#[test] fn error_is_not_result(){let e=EvaluationError{code:EvaluationErrorCode::EvaluatorFailure,severity:ErrorSeverity::Terminal,retry:false,message:String::new(),cause_ref:None};assert_eq!(e.code,EvaluationErrorCode::EvaluatorFailure);}
