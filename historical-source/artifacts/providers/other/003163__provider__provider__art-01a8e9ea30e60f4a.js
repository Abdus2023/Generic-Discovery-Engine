    class Provider {
        constructor(name) {
            this.name = name;
            this.exclusive = false;
        }

        recognize(observation) {
            return {
                recognized: false,
                confidence: 0
            };
        }

        discover() {
            return [];
        }
    }
