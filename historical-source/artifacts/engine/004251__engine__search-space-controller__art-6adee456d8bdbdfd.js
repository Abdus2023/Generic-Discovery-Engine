class SearchSpaceController {
    constructor(options = {}) {
        this.strategies =
            options.strategies || [];

        this.partitions =
            new Map();

        this.proposals =
            new Map();
    }

    registerPartition(partition) {
        this.partitions.set(
            partition.id,
            partition
        );

        return partition;
    }

    selectStrategy(partition, context) {
        return this.strategies
            .filter(strategy =>
                strategy.canExplore(
                    partition,
                    context
                )
            )
            .sort(
                (a, b) =>
                    b.priority() -
                    a.priority()
            )[0] || null;
    }
}
