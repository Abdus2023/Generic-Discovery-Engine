    class ResourceRecord {
        constructor(url) {
            this.url =
                canonicalizeUrl(
                    url
                ) || url;

            this.id =
                'resource:' +
                this.url;

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

            this.status =
                'known';

            this.firstSeenAt =
                now();

            this.lastSeenAt =
                now();

            this.fingerprint =
                null;

            this.finalUrl =
                null;

            this.acquisitionCount =
                0;
        }

        mergeCandidate(
            candidate
        ) {
            this.types.add(
                candidate.type
            );

            this.mechanisms.add(
                candidate.origin
            );

            if (
                candidate.parent
            ) {
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

        mergeObservation(
            observation
        ) {
            this.observationIds.add(
                observation.id
            );

            this.status =
                observation.status ===
                'observed'
                    ? 'acquired'
                    : observation.status;

            if (
                observation.http
                    ?.finalUrl
            ) {
                this.finalUrl =
                    observation.http.finalUrl;
            }

            if (
                observation.fingerprint
            ) {
                this.fingerprint =
                    observation.fingerprint;
            }

            this.acquisitionCount++;

            this.lastSeenAt =
                now();
        }

        mergeDiscovery(
            discovery
        ) {
            this.discoveryIds.add(
                discovery.id
            );

            this.lastSeenAt =
                now();
        }

        toJSON() {
            return {
                url:
                    this.url,

                id:
                    this.id,

                types:
                    [...this.types],

                mechanisms:
                    [...this.mechanisms],

                parents:
                    [...this.parents],

                candidateIds:
                    [...this.candidateIds],

                observationIds:
                    [...this.observationIds],

                discoveryIds:
                    [...this.discoveryIds],

                status:
                    this.status,

                firstSeenAt:
                    this.firstSeenAt,

                lastSeenAt:
                    this.lastSeenAt,

                fingerprint:
                    this.fingerprint,

                finalUrl:
                    this.finalUrl,

                acquisitionCount:
                    this.acquisitionCount
            };
        }

        static fromJSON(
            value
        ) {
            const resource =
                new ResourceRecord(
                    value.url
                );

            resource.id =
                value.id ||
                resource.id;

            resource.types =
                new Set(
                    value.types || []
                );

            resource.mechanisms =
                new Set(
                    value.mechanisms || []
                );

            resource.parents =
                new Set(
                    value.parents || []
                );

            resource.candidateIds =
                new Set(
                    value.candidateIds ||
                        []
                );

            resource.observationIds =
                new Set(
                    value.observationIds ||
                        []
                );

            resource.discoveryIds =
                new Set(
                    value.discoveryIds ||
                        []
                );

            resource.status =
                value.status ||
                'known';

            resource.firstSeenAt =
                value.firstSeenAt ||
                now();

            resource.lastSeenAt =
                value.lastSeenAt ||
                resource.firstSeenAt;

            resource.fingerprint =
                value.fingerprint ||
                null;

            resource.finalUrl =
                value.finalUrl ||
                null;

            resource.acquisitionCount =
                value.acquisitionCount ||
                0;

            return resource;
        }
    }
