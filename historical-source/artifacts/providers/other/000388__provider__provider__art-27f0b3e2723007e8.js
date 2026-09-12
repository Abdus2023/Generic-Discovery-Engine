    class Provider {
        constructor(name) {
            this.name = name;
        }

        matches() {
            return false;
        }

        async recognize() {
            return [];
        }
    }
