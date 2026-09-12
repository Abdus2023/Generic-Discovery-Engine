const MergePolicy = Object.freeze({
    REJECT_STALE: 'reject-stale',
    FIELD_MERGE: 'field-merge',
    APPEND_ONLY: 'append-only',
    MAX_VALID_VERSION: 'max-valid-version',
    UNION_IF_DISJOINT: 'union-if-disjoint',
    PRESERVE_CONFLICT: 'preserve-conflict',
    EXPLICIT_RESOLUTION: 'explicit-resolution'
});
