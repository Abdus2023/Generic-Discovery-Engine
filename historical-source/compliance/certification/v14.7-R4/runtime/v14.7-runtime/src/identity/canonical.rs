use std::collections::BTreeMap;
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CanonicalizationError { Unsupported }
pub trait CanonicalSerialize { fn canonical_bytes(&self) -> Result<Vec<u8>, CanonicalizationError>; }
impl CanonicalSerialize for BTreeMap<String, String> {
    fn canonical_bytes(&self) -> Result<Vec<u8>, CanonicalizationError> {
        let body = self.iter().map(|(key, value)| format!("{}:{}{}:{}", key.len(), key, value.len(), value)).collect::<Vec<_>>().join("|");
        Ok(body.into_bytes())
    }
}
