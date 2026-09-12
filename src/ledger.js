// src/ledger.js — DecisionLedger
    class DecisionLedger {
        constructor() {
            this.sequence = 0;
            this.events = [];
        }

        append(type, data = {}) {
            const event = {
                seq: ++this.sequence,
                id: makeId('evt'),
                type,
                timestamp: now(),
                ...data
            };

            this.events.push(event);

            if (
                this.events.length >
                CONFIG.persistedLedgerEvents
            ) {
                this.events.splice(
                    0,
                    this.events.length -
                        CONFIG.persistedLedgerEvents
                );
            }

            return event;
        }

        recordCandidateDiscovered(candidate, discovery = null) {
            return this.append(
                'candidate-discovered',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    candidateType: candidate.type,
                    depth: candidate.depth,
                    priority: candidate.priority,
                    discoveryId:
                        discovery?.id || null
                }
            );
        }

        recordCandidateClaimed(candidate) {
            return this.append(
                'candidate-claimed',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    candidateType: candidate.type
                }
            );
        }

        recordPlan(plan) {
            return this.append(
                'acquisition-planned',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    target: plan.target,
                    method: plan.method,
                    allowed: plan.allowed,
                    reason: plan.reason,
                    priority: plan.priority,
                    expectedType: plan.expectedType,
                    policyVersion: plan.policyVersion
                }
            );
        }

        recordPolicyDenied(plan) {
            return this.append(
                'policy-denied',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    target: plan.target,
                    method: plan.method,
                    reason: plan.reason
                }
            );
        }

        recordBudgetDenied(candidate, reason) {
            return this.append(
                'budget-denied',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    reason
                }
            );
        }

        recordSlotGranted(plan) {
            return this.append(
                'slot-granted',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    origin: plan.origin
                }
            );
        }

        recordRequestStarted(plan) {
            return this.append(
                'request-started',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    target: plan.target,
                    method: plan.method
                }
            );
        }

        recordRequestCompleted(plan, observation) {
            return this.append(
                'request-completed',
                {
                    planId: plan.id,
                    candidateId: plan.candidateId,
                    observationId: observation.id,
                    status: observation.status,
                    httpStatus:
                        observation.http?.status || null
                }
            );
        }

        recordObservation(observation) {
            return this.append(
                'observation-recorded',
                {
                    observationId: observation.id,
                    candidateId: observation.candidateId,
                    target: observation.target,
                    status: observation.status,
                    fingerprint:
                        observation.fingerprint?.hash ||
                        null
                }
            );
        }

        recordRecognition(
            candidate,
            observation,
            provider
        ) {
            return this.append(
                'provider-recognized',
                {
                    candidateId: candidate.id,
                    observationId: observation.id,
                    provider
                }
            );
        }

        recordDiscovery(discovery) {
            return this.append(
                'discovery-emitted',
                {
                    discoveryId: discovery.id,
                    candidateId: discovery.candidateId,
                    observationId:
                        discovery.observationId,
                    kind: discovery.kind,
                    confidence: discovery.confidence,
                    mechanism: discovery.mechanism
                }
            );
        }

        recordCandidateEnqueued(candidate) {
            return this.append(
                'candidate-enqueued',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    candidateType: candidate.type,
                    priority: candidate.priority,
                    depth: candidate.depth
                }
            );
        }

        recordRetry(candidate, reason) {
            return this.append(
                'candidate-retried',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    attempt: candidate.attempts,
                    reason
                }
            );
        }

        recordCandidateCompleted(candidate) {
            return this.append(
                'candidate-completed',
                {
                    candidateId: candidate.id,
                    target: candidate.target
                }
            );
        }

        recordCandidateSkipped(candidate, reason) {
            return this.append(
                'candidate-skipped',
                {
                    candidateId: candidate.id,
                    target: candidate.target,
                    reason
                }
            );
        }

        recordDiagnostic(type, data = {}) {
            return this.append(
                `diagnostic:${type}`,
                data
            );
        }

        export() {
            return {
                version: 1,
                sequence: this.sequence,
                events: this.events.slice()
            };
        }

        restore(data) {
            if (!data || !Array.isArray(data.events)) {
                return;
            }

            this.events = data.events.slice(
                -CONFIG.persistedLedgerEvents
            );

            this.sequence =
                Number.isFinite(data.sequence)
                    ? data.sequence
                    : (
                        this.events.length
                            ? Math.max(
                                ...this.events.map(
                                    e => e.seq || 0
                                )
                            )
                            : 0
                    );
        }
    }

    /*
     * ============================================================
     * CANDIDATE
     * ============================================================
     */

