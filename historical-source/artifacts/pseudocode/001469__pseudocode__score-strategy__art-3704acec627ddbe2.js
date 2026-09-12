function scoreStrategy(strategy, performance, context) {
    const attempts =
        Math.max(1, performance?.attempts || 0);

    const yieldRate =
        (performance?.newResources || 0) / attempts;

    const failureRate =
        (performance?.failures || 0) / attempts;

    const novelty =
        context.partition?.status === 'unexplored'
            ? 0.20
            : 0;

    return (
        strategy.priority() +
        yieldRate +
        novelty -
        failureRate * 0.5
    );
}
