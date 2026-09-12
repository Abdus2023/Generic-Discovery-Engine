#[derive(Clone,Debug,Eq,PartialEq)] pub enum ValidationError { Structural,Reference,Integrity,Temporal,Scope,Policy,Authority,Evidence,Freshness }
