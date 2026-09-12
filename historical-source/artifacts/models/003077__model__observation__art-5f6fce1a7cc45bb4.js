    class Observation {
        constructor(candidate) {
            this.id =
                makeId('observation');

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
                status:
                    null,

                contentType:
                    '',

                contentLength:
                    null,

                finalUrl:
                    candidate.target
            };

            this.fingerprint =
                null;

            this.body =
                '';

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
