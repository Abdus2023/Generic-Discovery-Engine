class Discovery {
    constructor({
        candidate,
        observation,
        kind,
        confidence = 0.5,
        data = {}
    }) {
        this.id = makeId('discovery');

        this.candidateId = candidate.id;
        this.observationId = observation.id;

        this.kind = kind;
        this.confidence = confidence;

        this.data = data;

        this.provenance = {
            origin: candidate.origin,
            parent: candidate.parent
        };

        this.createdAt = now();
    }
}
