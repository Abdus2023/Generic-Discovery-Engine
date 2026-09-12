class Observation {
    constructor(candidate) {
        this.id = makeId('observation');

        this.candidateId = candidate.id;
        this.target = candidate.target;

        this.startedAt = now();
        this.completedAt = null;

        this.signalPresent = false;

        this.status = 'unknown';

        this.http = {
            status: null,
            contentType: null,
            contentLength: null
        };

        this.features = {};
        this.errors = [];
    }

    complete(status = 'complete') {
        this.completedAt = now();
        this.status = status;
    }
}
