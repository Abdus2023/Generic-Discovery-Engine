function performanceKey(strategyId, context) {
    return [
        strategyId,
        context.partitionKind || 'unknown',
        context.resourceClass || 'unknown'
    ].join(':');
}
