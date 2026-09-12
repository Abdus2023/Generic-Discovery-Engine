#[derive(Clone,Debug,Eq,PartialEq)] pub enum ProjectionError { InvalidHistory,MissingEvent,DuplicateSequence,CorruptEvent }
pub trait Projector<History,Profile,State>{fn project(&self,history:&History,profile:&Profile)->Result<State,ProjectionError>;}
