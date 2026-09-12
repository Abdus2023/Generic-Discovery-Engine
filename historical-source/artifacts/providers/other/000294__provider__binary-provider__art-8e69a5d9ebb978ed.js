    class BinaryProvider extends Provider {
        constructor() {
            super('binary', true);
        }

        matches(candidate, observation) {
            const type =
                normalizeContentType(
                    observation.http.contentType
                );

            if (!type) {
                return false;
            }

            return !(
                isHtmlContentType(type) ||
                isJsonContentType(type) ||
                isXmlContentType(type) ||
                isCssContentType(type) ||
                isJavaScriptContentType(type) ||
                isTextContentType(type)
            );
        }

        recognize(candidate, observation) {
            return [
                new Discovery({
                    candidateId: candidate.id,
                    observationId: observation.id,
                    kind: 'binary-resource',
                    confidence: 0.80,
                    mechanism: 'content-type-recognition',
                    data: {
                        url: candidate.target,
                        finalUrl:
                            observation.http.finalUrl,
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
