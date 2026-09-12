use std::collections::BTreeSet;
pub fn distinct_valid(approvals: &[(String, bool)]) -> usize { approvals.iter().filter(|(_, valid)| *valid).map(|(id, _)| id).collect::<BTreeSet<_>>().len() }
