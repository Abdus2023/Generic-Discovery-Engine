use std::collections::BTreeMap;
use v14_7_runtime::identity::canonical::CanonicalSerialize;
#[test] fn canonical_order_is_deterministic() { let mut left = BTreeMap::new(); left.insert("b".into(), "2".into()); left.insert("a".into(), "1".into()); let mut right = BTreeMap::new(); right.insert("a".into(), "1".into()); right.insert("b".into(), "2".into()); assert_eq!(left.canonical_bytes().unwrap(), right.canonical_bytes().unwrap()); }
