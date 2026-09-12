use super::canonical::{CanonicalSerialize, CanonicalizationError};
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct ContentHash(pub [u8; 32]);
impl ContentHash { pub fn zero() -> Self { Self([0; 32]) } }
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DomainSeparatedInput(pub Vec<u8>);
pub fn hash_input<T: CanonicalSerialize>(domain_tag: &str, value: &T) -> Result<DomainSeparatedInput, CanonicalizationError> {
    let mut input = domain_tag.as_bytes().to_vec(); input.push(b':'); input.extend(value.canonical_bytes()?); Ok(DomainSeparatedInput(input))
}
