    class BinaryProvider extends Provider {
        constructor() {
            super('binary');
            this.exclusive = true;
        }

        recognize(observation) {
            if (
                isBinaryContentType(
                    observation.http.contentType
                )
            ) {
                return {
                    recognized: true,
                    confidence: 0.90
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover() {
            return [];
        }
    }
