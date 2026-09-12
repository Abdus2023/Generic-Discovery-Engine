class ScanSession {
    constructor(domain, options = {}) {
        this.id = makeId('scan');

        this.domainId = domain.id;

        this.goalId =
            options.goalId || null;

        // ...
    }
}
