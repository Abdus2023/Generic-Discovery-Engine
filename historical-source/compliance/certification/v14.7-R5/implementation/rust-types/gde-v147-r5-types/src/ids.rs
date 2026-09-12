macro_rules! identifier { ($name:ident) => { #[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)] pub struct $name(pub String); }; }
identifier!(RequirementId);
identifier!(ProfileId);
identifier!(PredicateId);
identifier!(EvaluationId);
identifier!(ValidationId);
identifier!(EvidenceId);
identifier!(CertificateId);
identifier!(ReleaseId);
identifier!(DecisionId);
identifier!(EventId);
identifier!(ImplementationId);
identifier!(AuthorityId);
identifier!(SnapshotId);
identifier!(DecisionBasisId);
