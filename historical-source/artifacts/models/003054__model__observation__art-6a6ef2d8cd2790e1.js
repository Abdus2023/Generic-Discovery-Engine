    class Observation {
        constructor(candidate) {
            this.id =
                id('observation');

            this.candidateId =
                candidate.id;

            this.target =
                candidate.target;

            this.startedAt =
                now();

            this.completedAt =
                null;

            this.status =
                'acquiring';

            this.signalPresent =
                false;

            this.http = {
                status: null,
                contentType: '',
                contentLength: null,
                finalUrl:
                    candidate.target
            };

            this.fingerprint = {
                length: null,
                sha256: null
            };

            this.body =
                null;

            this.errors =
                [];
        }

        complete(status) {
            this.status =
                status;

            this.completedAt =
                now();
        }
    }
