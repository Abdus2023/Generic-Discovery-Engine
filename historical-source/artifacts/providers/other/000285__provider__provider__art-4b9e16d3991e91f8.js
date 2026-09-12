    class Provider {
        constructor(name, exclusive = true) {
            this.name = name;
            this.exclusive = exclusive;
        }

        matches() {
            return false;
        }

        recognize() {
            return [];
        }

        candidates() {
            return [];
        }
    }
