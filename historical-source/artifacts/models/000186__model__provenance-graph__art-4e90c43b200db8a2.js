    class ProvenanceGraph {
        constructor() {
            this.nodes =
                new Map();

            this.edges =
                new Map();
        }

        addNode(node) {
            if (
                !node ||
                !node.id
            ) {
                return;
            }

            if (
                this.nodes.size >=
                CONFIG.maxGraphNodes
            ) {
                return;
            }

            this.nodes.set(
                node.id,
                node
            );
        }

        addEdge({
            from,
            to,
            relation,
            confidence = 0.5,
            mechanism = null
        }) {
            if (
                !from ||
                !to
            ) {
                return;
            }

            if (
                this.edges.size >=
                CONFIG.maxGraphEdges
            ) {
                return;
            }

            const id =
                makeId(
                    'edge'
                );

            this.edges.set(
                id,
                {
                    id,
                    from,
                    to,
                    relation,
                    confidence,
                    mechanism,
                    createdAt:
                        now()
                }
            );
        }

        addCandidate(candidate) {
            this.addNode({
                id:
                    candidate.id,

                type:
                    'candidate',

                candidateType:
                    candidate.type,

                target:
                    candidate.target,

                depth:
                    candidate.depth
            });

            if (
                candidate.parent
            ) {
                this.addEdge({
                    from:
                        candidate.parent,

                    to:
                        candidate.id,

                    relation:
                        'generated',

                    confidence:
                        candidate.priority,

                    mechanism:
                        candidate.origin
                });
            }
        }

        addDiscovery(discovery) {
            this.addNode({
                id:
                    discovery.id,

                type:
                    'discovery',

                kind:
                    discovery.kind,

                target:
                    discovery.data?.url ||
                    discovery.provenance
                        ?.target ||
                    null,

                confidence:
                    discovery.confidence,

                mechanism:
                    discovery.mechanism
            });

            if (
                discovery.candidateId
            ) {
                this.addEdge({
                    from:
                        discovery.candidateId,

                    to:
                        discovery.id,

                    relation:
                        'observed',

                    confidence:
                        discovery.confidence,

                    mechanism:
                        discovery.mechanism
                });
            }

            if (
                discovery.provenance.parent
            ) {
                this.addEdge({
                    from:
                        discovery.provenance.parent,

                    to:
                        discovery.id,

                    relation:
                        'produced',

                    confidence:
                        discovery.confidence,

                    mechanism:
                        discovery.mechanism
                });
            }
        }

        addPassiveObservation({
            url,
            mechanism,
            status,
            contentType
        }) {
            const id =
                makeId(
                    'passive'
                );

            this.addNode({
                id,

                type:
                    'passive-observation',

                target:
                    url,

                mechanism,

                status,
                contentType
            });

            return id;
        }

        serialize() {
            return {
                nodes:
                    [
                        ...this.nodes.values()
                    ],

                edges:
                    [
                        ...this.edges.values()
                    ]
            };
        }

        clear() {
            this.nodes.clear();
            this.edges.clear();
        }
    }
