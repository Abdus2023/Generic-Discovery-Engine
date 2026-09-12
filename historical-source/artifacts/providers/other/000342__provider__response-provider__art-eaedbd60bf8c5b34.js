    class ResponseProvider extends Provider {
        constructor() {
            super('response');
            this.exclusive = false;
        }

        recognize(observation) {
            if (
                observation.status === 'success' ||
                observation.status === 'http-error'
            ) {
                return {
                    recognized: true,
                    confidence: 0.30
                };
            }

            return {
                recognized: false,
                confidence: 0
            };
        }

        discover(observation) {
            return [];
        }
    }
