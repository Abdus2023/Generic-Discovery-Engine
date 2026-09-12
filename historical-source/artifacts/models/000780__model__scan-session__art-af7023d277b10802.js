class ScanSession {
    constructor(domain) {
        this.id = makeId('scan');

        this.domainId =
            domain.id;

        this.status =
            'created';

        this.startedAt =
            null;

        this.completedAt =
            null;

        this.reason =
            null;

        this.stats = {
            seeds: 0,
            candidates: 0,
            discoveries: 0,
            acquisitions: 0,
            observations: 0,
            recognitions: 0,
            errors: 0
        };

        this.createdAt =
            now();
    }
}
