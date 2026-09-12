use super::event::CommittedEvent;
pub fn ordered(history: &[CommittedEvent]) -> Vec<&CommittedEvent> {
    let mut items: Vec<_> = history.iter().collect();
    items.sort_by(|left, right| left.event.stream_id.cmp(&right.event.stream_id)
        .then(left.event.sequence_no.cmp(&right.event.sequence_no))
        .then(left.commit_index.cmp(&right.commit_index)));
    items
}
