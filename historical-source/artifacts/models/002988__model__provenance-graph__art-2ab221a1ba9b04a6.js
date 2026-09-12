    class ProvenanceGraph {
        constructor() {
            this.nodes =
                new Map();

            this.edges =
                new Map();
        }

        addNode(node) {
            if (!node || !node.id) {
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
            confidence = 0.5
        }) {
            const id =
                makeId('edge');

            this.edges.set(
                id,
                {
                    id,
                    from,
                    to,
                    relation,
                    confidence,
                    createdAt: now()
                }
            );
        }

        addDiscovery(discovery) {
            this.addNode({
                id: discovery.id,
                type: 'discovery',
                kind: discovery.kind,
                target:
                    discovery.data.url ||
                    null,
                confidence:
                    discovery.confidence
            });

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
                        discovery.confidence
                });
            }
        }

        addCandidate(candidate) {
            this.addNode({
                id: candidate.id,
                type: 'candidate',
                candidateType:
                    candidate.type,
                target:
                    candidate.target,
                depth:
                    candidate.depth
            });

            if (candidate.parent) {
                this.addEdge({
                    from:
                        candidate.parent,
                    to:
                        candidate.id,
                    relation:
                        'generated',
                    confidence:
                        candidate.priority
                });
            }
        }

        serialize() {
            return {
                nodes: [
                    ...this.nodes.values()
                ],
                edges: [
                    ...this.edges.values()
                ]
            };
        }

        clear() {
            this.nodes.clear();
            this.edges.clear();
        }
    }
