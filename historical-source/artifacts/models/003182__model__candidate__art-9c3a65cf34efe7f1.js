const candidate =
    this.db.claimNextCandidate();

if (!candidate) {
    // no work currently available
    ...
}

const plan =
    this.policy.plan(candidate);

this.db.recordDiagnostic(
    'acquisition-plan',
    plan.serialize()
);

if (!plan.allowed) {
    this.db.markSkipped(
        candidate,
        plan.reason
    );

    continue;
}

if (!this.reserveRequestSlot()) {
    this.db.requeue(candidate);
    break;
}

await this.executePlan(plan);
