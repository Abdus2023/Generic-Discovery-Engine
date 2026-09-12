use crate::domain::objects::{EvaluationContext,EvaluationResult,EvaluatorIdentity,Predicate};
use crate::domain::typestate::ValidatedSubject;
#[derive(Clone,Copy,Debug,Eq,PartialEq)] pub enum EvaluationErrorCode { InvalidPredicate,InvalidSubject,InvalidContext,ValidationRequired,ValidationFailed,UnsupportedPredicate,EvaluatorFailure,EvaluatorTimeout,EvaluatorResourceFailure,EvaluatorInternalFailure,OutputInvalid,EvaluatorDependencyUnavailable }
#[derive(Clone,Copy,Debug,Eq,PartialEq)] pub enum ErrorSeverity { Recoverable,Terminal }
#[derive(Clone,Debug,Eq,PartialEq)] pub struct EvaluationError { pub code:EvaluationErrorCode, pub severity:ErrorSeverity, pub retry:bool, pub message:String, pub cause_ref:Option<String> }
pub trait Evaluator { fn identity(&self)->EvaluatorIdentity; fn evaluate(&self,predicate:&Predicate,subject:&ValidatedSubject,context:&EvaluationContext)->Result<EvaluationResult,EvaluationError>; }
