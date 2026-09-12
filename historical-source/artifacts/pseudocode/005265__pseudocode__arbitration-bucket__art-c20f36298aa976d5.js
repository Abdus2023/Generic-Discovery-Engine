class ArbitrationBucket {
    constructor(workClass, weight = 1) {
        this.workClass = workClass;
        this.weight = weight;
        this.deficit = 0;
    }

    accrue(quantum) {
        this.deficit +=
            this.weight * quantum;
    }

    consume(cost) {
        this.deficit -= cost;
    }
}
