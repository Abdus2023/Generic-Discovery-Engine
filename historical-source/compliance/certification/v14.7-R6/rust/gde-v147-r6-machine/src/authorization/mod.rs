#[derive(Clone,Debug,Eq,PartialEq)] pub enum AuthorizationError { InvalidEligibility,AuthorityNotQualified,ScopeInvalid,ExpiredAuthority,PolicyUnavailable }
