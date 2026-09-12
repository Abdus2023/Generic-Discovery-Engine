class AdaptiveDiscoveryController {
    constructor(options = {}) {
        this.strategies =
            options.strategies || [];

        this.performance =
            new Map();

        this.explorationRatio =
            options.explorationRatio ?? 0.2;
    }

    eligibleStrategies(partition, context) {
        return this.strategies.filter(
            strategy =>
                strategy.canExplore(
                    partition,
                    context
                )
        );
    }

    select(partition, context) {
        const eligible =
            this.eligibleStrategies(
                partition,
                context
            );

        if (!eligible.length) {
            return null;
        }

        // Deterministic scoring would occur here.
        return eligible
            .map(strategy => ({
                strategy,
                score: this.score(
                    strategy,
                    partition,
                    context
                )
            }))
            .sort((a, b) =>
                b.score - a.score
            )[0].strategy;
    }

    score(strategy, partition, context) {
        const key =
            performanceKey(
                strategy.describe().id,
                {
                    partitionKind:
                        partition.kind
                }
            );

        const history =
            this.performance.get(key);

        return (
            strategy.priority() +
            this.historyScore(history)
        );
    }

    historyScore(history) {
        if (!history) {
            return 0;
        }

        const attempts =
            Math.max(1, history.attempts);

        const yieldRate =
            history.newResources /
            attempts;

        const failures =
            history.failures /
            attempts;

        return yieldRate -
            failures * 0.5;
    }
}
