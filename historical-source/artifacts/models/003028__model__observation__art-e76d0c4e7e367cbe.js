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
                'unknown';

            this.signalPresent =
                false;

            this.http = {
                status: null,
                contentType: null,
                contentLength: null,
                finalUrl: null
            };

            this.body =
                null;

            this.errors =
                [];

            this.network =
                candidate.type ===
                    'network'
                    ? {
                          observed: true,
                          mechanism:
                              candidate
                                  .hints
                                  ?.mechanism ||
                              null
                      }
                    : null;
        }

        complete(status) {
            this.completedAt =
                now();

            this.status =
                status;
        }
    }
