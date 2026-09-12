    class Observation {
        constructor({
            candidateId,
            target,
            status = 'acquired',
            reason = null
        }) {
            this.id =
                makeId('observation');

            this.candidateId =
                candidateId;

            this.target =
                target;

            this.startedAt =
                now();

            this.completedAt =
                null;

            this.status =
                status;

            this.reason =
                reason;

            this.signalPresent =
                false;

            this.http = {
                status: null,
                contentType: '',
                contentLength: null,
                finalUrl: null
            };

            this.body = '';

            this.errors = [];

            this.network = null;

            this.fingerprint = null;
        }
    }
