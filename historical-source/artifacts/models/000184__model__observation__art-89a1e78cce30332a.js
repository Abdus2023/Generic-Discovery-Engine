    class Observation {
        constructor(candidate) {
            this.id =
                makeId(
                    'observation'
                );

            this.candidateId =
                candidate.id;

            this.target =
                candidate.target;

            this.startedAt =
                now();

            this.completedAt =
                null;

            this.status =
                'unknown';

            this.signalPresent =
                false;

            this.http = {
                status: null,
                statusClass:
                    'unknown',

                contentType: null,

                contentLength: null,

                finalUrl: null
            };

            this.body =
                null;

            this.bodyTruncated =
                false;

            this.errors =
                [];
        }

        complete(status) {
            this.completedAt =
                now();

            this.status =
                status;

            this.http.statusClass =
                classifyHttpStatus(
                    this.http.status
                );
        }
    }
