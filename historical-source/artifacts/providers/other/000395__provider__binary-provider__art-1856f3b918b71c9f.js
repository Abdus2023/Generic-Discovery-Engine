    class BinaryProvider extends Provider {
        constructor() {
            super('binary');
        }

        matches(observation) {
            return looksLikeBinary(
                observation.http?.contentType
            );
        }

        async recognize() {
            /*
             * Binary resources are observed but not parsed.
             *
             * Future providers may add PDF, ZIP, image metadata,
             * archive manifests, etc.
             */
            return [];
        }
    }
