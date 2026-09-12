    class ResponseProvider {

        matches(/* observation */) {
            return false;
        }

        recognize(/* candidate, observation */) {
            return null;
        }

        candidates(/* discovery */) {
            return [];
        }
    }
