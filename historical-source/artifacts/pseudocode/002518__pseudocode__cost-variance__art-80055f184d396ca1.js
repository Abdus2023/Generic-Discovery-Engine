class CostVariance {
    constructor(data = {}) {
        this.dimension = data.dimension;
        this.estimated = data.estimated ?? 0;
        this.actual = data.actual ?? 0;

        this.delta =
            this.actual - this.estimated;

        this.ratio =
            this.estimated > 0
                ? this.actual / this.estimated
                : null;
    }
}
