    class ResourceRecord {
        constructor(url) {
            this.id =
                stableId(
                    'resource',
                    url
                );

            this.url =
                url;

            this.types =
                new Set();

            this.mechanisms =
                new Set();

            this.parents =
                new Set();

            this.candidateIds =
                new Set();

            this.observationIds =
                new Set();

            this.discoveryIds =
                new Set();

            this.firstSeenAt =
                now();

            this.lastSeenAt =
                now();

            this.status =
                'known';

            this.fingerprint =
                null;

            this.finalUrl =
                null;

            this.redirectTo =
                null;

            this.duplicateFingerprint =
                null;
        }

        mergeCandidate(candidate) {
            this.types.add(
                candidate.type
            );

            this.mechanisms.add(
                candidate.origin
            );

            if (candidate.parent) {
                this.parents.add(
                    candidate.parent
                );
            }

            this.candidateIds.add(
                candidate.id
            );

            this.lastSeenAt =
                now();
        }

        mergeObservation(observation) {
            this.observationIds.add(
                observation.id
            );

            if (
                observation.status ===
                'failed'
            ) {
                this.status =
                    'failed';
            } else if (
                observation.status ===
                'skipped'
            ) {
                this.status =
                    'skipped';
            } else if (
                observation.status ===
                'reused'
            ) {
                this.status =
                    'acquired';
            } else {
                this.status =
                    'acquired';
            }

            if (observation.fingerprint) {
                this.fingerprint =
                    observation.fingerprint;
            }

            if (
                observation.http?.finalUrl
            ) {
                this.finalUrl =
                    observation.http.finalUrl;

                if (
                    observation.http.finalUrl !==
                    this.url
                ) {
                    this.redirectTo =
                        observation.http.finalUrl;
                }
            }

            this.lastSeenAt =
                now();
        }

        mergeDiscovery(discovery) {
            this.discoveryIds.add(
                discovery.id
            );

            this.lastSeenAt =
                now();
        }

        toJSON() {
            return {
                id: this.id,
                url: this.url,

                types: [
                    ...this.types
                ],

                mechanisms: [
                    ...this.mechanisms
                ],

                parents: [
                    ...this.parents
                ],

                candidateIds: [
                    ...this.candidateIds
                ],

                observationIds: [
                    ...this.observationIds
                ],

                discoveryIds: [
                    ...this.discoveryIds
                ],

                firstSeenAt:
                    this.firstSeenAt,

                lastSeenAt:
                    this.lastSeenAt,

                status:
                    this.status,

                fingerprint:
                    this.fingerprint,

                finalUrl:
                    this.finalUrl,

                redirectTo:
                    this.redirectTo,

                duplicateFingerprint:
                    this.duplicateFingerprint
            };
        }

        static fromJSON(value) {
            const record =
                new ResourceRecord(
                    value.url
                );

            record.id =
                value.id ||
                record.id;

            record.types =
                new Set(
                    safeArray(
                        value.types
                    )
                );

            record.mechanisms =
                new Set(
                    safeArray(
                        value.mechanisms
                    )
                );

            record.parents =
                new Set(
                    safeArray(
                        value.parents
                    )
                );

            record.candidateIds =
                new Set(
                    safeArray(
                        value.candidateIds
                    )
                );

            record.observationIds =
                new Set(
                    safeArray(
                        value.observationIds
                    )
                );

            record.discoveryIds =
                new Set(
                    safeArray(
                        value.discoveryIds
                    )
                );

            record.firstSeenAt =
                value.firstSeenAt ||
                record.firstSeenAt;

            record.lastSeenAt =
                value.lastSeenAt ||
                record.lastSeenAt;

            record.status =
                value.status ||
                'known';

            record.fingerprint =
                value.fingerprint ||
                null;

            record.finalUrl =
                value.finalUrl ||
                null;

            record.redirectTo =
                value.redirectTo ||
                null;

            record.duplicateFingerprint =
                value.duplicateFingerprint ||
                null;

            return record;
        }
    }
