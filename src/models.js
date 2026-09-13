// src/models.js — Candidate, Observation, Discovery, ResourceRecord
    class Candidate {
        constructor(data = {}) {
            this.id =
                data.id || makeId('candidate');

            this.target =
                canonicalizeUrl(data.target) ||
                data.target ||
                '';

            this.type =
                data.type || 'unknown';

            this.origin =
                data.origin ||
                originOf(this.target);

            this.parent =
                data.parent || null;

            this.priority =
                Number.isFinite(data.priority)
                    ? data.priority
                    : 0;

            this.hints =
                data.hints || {};

            this.depth =
                Number.isFinite(data.depth)
                    ? data.depth
                    : 0;

            this.createdAt =
                data.createdAt || now();

            this.attempts =
                Number.isFinite(data.attempts)
                    ? data.attempts
                    : 0;

            this.status =
                data.status || 'discovered';

            this.nextAttemptAt =
                data.nextAttemptAt || 0;

            this.discoveredAt =
                data.discoveredAt || now();

            this.queuedAt =
                data.queuedAt || null;

            this.claimedAt =
                data.claimedAt || null;

            this.plannedAt =
                data.plannedAt || null;

            this.acquiringAt =
                data.acquiringAt || null;

            this.observedAt =
                data.observedAt || null;

            this.recognizedAt =
                data.recognizedAt || null;

            this.expandedAt =
                data.expandedAt || null;

            this.completedAt =
                data.completedAt || null;

            this.failedAt =
                data.failedAt || null;

            this.skippedAt =
                data.skippedAt || null;

            this.alternateTypes =
                safeArray(data.alternateTypes);

            this.alternateOrigins =
                safeArray(data.alternateOrigins);

            this.alternateParents =
                safeArray(data.alternateParents);
        }

        identityKey() {
            return `${this.type}:${this.target}`;
        }

        effectivePriority() {
            const typeWeight =
                CONFIG.typePriority[this.type] ??
                CONFIG.typePriority.unknown;

            const confidence =
                Number(this.hints.confidence || 0);

            const retryPenalty =
                this.attempts *
                CONFIG.priority.retryPenalty;

            return (
                this.priority +
                typeWeight * 0.20 +
                confidence *
                    CONFIG.priority.confidenceBoost -
                this.depth *
                    CONFIG.priority.depthPenalty -
                retryPenalty
            );
        }

        serialize() {
            return {
                ...this,
                alternateTypes:
                    [...this.alternateTypes],
                alternateOrigins:
                    [...this.alternateOrigins],
                alternateParents:
                    [...this.alternateParents]
            };
        }
    }

    /*
     * ============================================================
     * OBSERVATION
     * ============================================================
     */

    class Observation {
        constructor(data = {}) {
            this.id =
                data.id || makeId('obs');

            this.candidateId =
                data.candidateId || null;

            this.planId =
                data.planId || null;

            this.target =
                data.target || '';

            this.requestedUrl =
                data.requestedUrl || this.target;

            this.startedAt =
                data.startedAt || now();

            this.completedAt =
                data.completedAt || null;

            this.status =
                data.status || 'unknown';

            this.reason =
                data.reason || null;

            this.signalPresent =
                Boolean(data.signalPresent);

            this.http =
                data.http || {
                    status: 0,
                    contentType: '',
                    contentLength: null,
                    finalUrl: this.requestedUrl
                };

            this.body =
                data.body || '';

            this.bodyTruncated =
                Boolean(data.bodyTruncated);

            this.errors =
                safeArray(data.errors);

            this.network =
                safeArray(data.network);

            this.fingerprint =
                data.fingerprint || null;
        }

        serialize() {
            return {
                id: this.id,
                candidateId: this.candidateId,
                planId: this.planId,
                target: this.target,
                requestedUrl: this.requestedUrl,
                startedAt: this.startedAt,
                completedAt: this.completedAt,
                status: this.status,
                reason: this.reason,
                signalPresent: this.signalPresent,
                http: this.http,
                bodyTruncated: this.bodyTruncated,
                errors: this.errors,
                network: this.network,
                fingerprint: this.fingerprint
            };
        }
    }

    /*
     * ============================================================
     * DISCOVERY
     * ============================================================
     */

    class Discovery {
        constructor(data = {}) {
            this.id =
                data.id || makeId('discovery');

            this.candidateId =
                data.candidateId || null;

            this.observationId =
                data.observationId || null;

            this.kind =
                data.kind || 'url';

            this.confidence =
                Number.isFinite(data.confidence)
                    ? data.confidence
                    : 0.5;

            this.mechanism =
                data.mechanism || 'unknown';

            this.data =
                data.data || {};

            this.provenance =
                data.provenance || {};

            this.createdAt =
                data.createdAt || now();
        }

        targetUrl() {
            return (
                this.data.url ||
                this.data.target ||
                this.provenance.candidateTarget ||
                null
            );
        }

        serialize() {
            return { ...this };
        }
    }

    /*
     * ============================================================
     * RESOURCE
     * ============================================================
     */

    class ResourceRecord {
        constructor(data = {}) {
            this.url =
                data.url || '';

            this.types =
                safeArray(data.types);

            this.mechanisms =
                safeArray(data.mechanisms);

            this.parents =
                safeArray(data.parents);

            this.candidateIds =
                safeArray(data.candidateIds);

            this.observationIds =
                safeArray(data.observationIds);

            this.discoveryIds =
                safeArray(data.discoveryIds);

            this.networkEventIds =
                safeArray(data.networkEventIds);

            this.createdAt =
                data.createdAt || now();

            this.updatedAt =
                data.updatedAt || now();

            this.status =
                data.status || 'known';

            this.fingerprint =
                data.fingerprint || null;

            this.finalUrl =
                data.finalUrl || null;

            this.skipReason =
                data.skipReason || null;
        }

        merge(data = {}) {
            this.updatedAt = now();
            const maxRel = CONFIG.retention?.resources?.maxRelationsPerResource
                ?? CONFIG.runtimeBudget?.maxRelationsPerResource
                ?? 100;

            if (data.type) {
                this.types.push(data.type);
                this.types = unique(this.types).slice(-maxRel);
            }

            if (data.mechanism) {
                this.mechanisms.push(data.mechanism);
                this.mechanisms =
                    unique(this.mechanisms).slice(-maxRel);
            }

            for (const field of [
                'parents',
                'candidateIds',
                'observationIds',
                'discoveryIds',
                'networkEventIds'
            ]) {
                if (data[field]) {
                    this[field] = unique([
                        ...this[field],
                        ...data[field]
                    ]).slice(-maxRel);
                }
            }

            if (data.status) {
                this.status = data.status;
            }

            if (data.fingerprint) {
                this.fingerprint =
                    data.fingerprint;
            }

            if (data.finalUrl) {
                this.finalUrl =
                    data.finalUrl;
            }

            if (data.skipReason) {
                this.skipReason =
                    data.skipReason;
            }
        }

        serialize() {
            return { ...this };
        }
    }

    /*
     * ============================================================
     * KNOWLEDGE BASE
     * ============================================================
     */

