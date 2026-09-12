use gde_v147_r6_machine::domain::enums::CertificateLifecycle;
use gde_v147_r6_machine::events::{certificate_transition,TransitionContext};
#[test] fn issued_is_not_validity(){let c=TransitionContext{structural:true,reference:true,integrity:true,temporal:true,scope:true,authority:true};assert!(certificate_transition(CertificateLifecycle::Draft,CertificateLifecycle::Issued,&c).is_ok());assert!(certificate_transition(CertificateLifecycle::Draft,CertificateLifecycle::Expired,&c).is_err());}
