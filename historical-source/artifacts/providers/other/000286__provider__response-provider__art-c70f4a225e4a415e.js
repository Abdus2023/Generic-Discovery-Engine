    class ResponseProvider extends Provider {
        constructor() {
            super('response', false);
        }

        matches(candidate, observation) {
            return (
                !!candidate &&
                !!observation &&
                !!observation.http
            );
        }

        recognize(candidate, observation) {
            return [
                new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind: 'http-response',
                    confidence: 0.45,
                    mechanism: 'http-response',
                    data: {
                        url: candidate.target,
                        finalUrl:
                            observation.http.finalUrl,
                        status:
                            observation.http.status,
                        contentType:
                            observation.http.contentType,
                        contentLength:
                            observation.http.contentLength,
                        fingerprint:
                            observation.fingerprint
                    },
                    provenance: {
                        origin: candidate.origin,
                        parent: candidate.parent,
                        candidateTarget: candidate.target,
                        candidateType: candidate.type,
                        depth: candidate.depth
                    }
                })
            ];
        }
    }
