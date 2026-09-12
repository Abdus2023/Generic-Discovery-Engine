class PartitionExpansionProvider {

    canExpand(evidence, context) {
        return false;
    }

    expand(evidence, context) {
        return [];
    }

    describe() {
        return {
            id: 'unknown-expander',
            name: 'Unknown Partition Expansion Provider'
        };
    }
}
