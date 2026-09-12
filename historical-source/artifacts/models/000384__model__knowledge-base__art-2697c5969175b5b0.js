    class KnowledgeBase {
        constructor() {
            this.candidates = new Map();
            this.candidateKeys = new Map();

            this.observations = new Map();
            this.discoveries = new Map();
            this.resources = new Map();

            this.visited = new Set();
            this.claimed = new Set();

            this.graphEdges = [];

            this.networkEvents = new Map();

            this.fingerprintIndex = new Map();

            this.diagnostics = [];

            this.stats = {
                discovered: 0,
                queued: 0,
                claimed: 0,
                planned: 0,
                acquired: 0,
                recognized: 0,
                expanded: 0,
                completed: 0,
                skipped: 0,
                failed: 0,
                retried: 0
            };
        }

        addCandidate(candidate, discovery = null) {
            if (!(candidate instanceof Candidate)) {
                candidate =
                    new Candidate(candidate);
            }

            const canonical =
                canonicalizeUrl(candidate.target);

            if (!canonical) {
                return null;
            }

            candidate.target = canonical;

            if (!isAllowedUrl(candidate.target)) {
                return null;
            }

            const key =
                candidate.identityKey();

            const existingId =
                this.candidateKeys.get(key);

            if (existingId) {
                const existing =
                    this.candidates.get(existingId);

                if (existing) {
                    existing.alternateTypes =
                        unique([
                            ...existing.alternateTypes,
                            candidate.type
                        ]);

                    if (candidate.parent) {
                        existing.alternateParents =
                            unique([
                                ...existing.alternateParents,
                                candidate.parent
                            ]);
                    }

                    existing.priority =
                        Math.max(
                            existing.priority,
                            candidate.priority
                        );

                    return existing;
                }
            }

            if (
                this.candidates.size >=
                CONFIG.maxCandidates
            ) {
                this.recordDiagnostic(
                    'candidate-cap-reached',
                    {
                        target: candidate.target
                    }
                );

                return null;
            }

            this.candidates.set(
                candidate.id,
                candidate
            );

            this.candidateKeys.set(
                key,
                candidate.id
            );

            this.stats.discovered++;

            if (discovery) {
                this.addEdge(
                    discovery.candidateId,
                    candidate.id,
                    discovery.mechanism
                );
            }

            return candidate;
        }

        queueCandidate(candidate) {
            if (!candidate) return;

            if (
                candidate.status ===
                    'completed' ||
                candidate.status ===
                    'skipped'
            ) {
                return;
            }

            candidate.status = 'queued';
            candidate.queuedAt = now();

            this.stats.queued++;
        }

        claimNextCandidate() {
            const eligible = [];

            for (const candidate of this.candidates.values()) {
                if (
                    candidate.status !== 'queued' &&
                    candidate.status !== 'failed'
                ) {
                    continue;
                }

                if (
                    candidate.nextAttemptAt &&
                    candidate.nextAttemptAt > now()
                ) {
                    continue;
                }

                eligible.push(candidate);
            }

            eligible.sort(
                (a, b) =>
                    b.effectivePriority() -
                    a.effectivePriority()
            );

            const candidate = eligible[0];

            if (!candidate) {
                return null;
            }

            candidate.status = 'claimed';
            candidate.claimedAt = now();

            this.claimed.add(candidate.id);
            this.stats.claimed++;

            return candidate;
        }

        markPlanned(candidate) {
            candidate.status = 'planned';
            candidate.plannedAt = now();
            this.stats.planned++;
        }

        markAcquiring(candidate) {
            candidate.status = 'acquiring';
            candidate.acquiringAt = now();
        }

        markObserved(candidate) {
            candidate.status = 'observed';
            candidate.observedAt = now();
        }

        markRecognized(candidate) {
            candidate.status = 'recognized';
            candidate.recognizedAt = now();
            this.stats.recognized++;
        }

        markExpanded(candidate) {
            candidate.status = 'expanded';
            candidate.expandedAt = now();
            this.stats.expanded++;
        }

        markCompleted(candidate) {
            candidate.status = 'completed';
            candidate.completedAt = now();
            this.visited.add(candidate.target);
            this.stats.completed++;
        }

        markSkipped(candidate, reason) {
            candidate.status = 'skipped';
            candidate.skippedAt = now();

            const resource =
                this.ensureResource(candidate.target);

            resource.merge({
                status: 'skipped',
                skipReason: reason,
                candidateIds: [candidate.id]
            });

            this.stats.skipped++;
        }

        markFailed(candidate) {
            candidate.status = 'failed';
            candidate.failedAt = now();
            this.stats.failed++;
        }

        retryCandidate(candidate, reason) {
            candidate.attempts++;

            if (
                candidate.attempts >
                CONFIG.retry.maxRetries
            ) {
                this.markFailed(candidate);
                return false;
            }

            const delay = Math.min(
                CONFIG.retry.maxDelay,
                CONFIG.retry.baseDelay *
                    Math.pow(
                        2,
                        candidate.attempts - 1
                    )
            );

            candidate.nextAttemptAt =
                now() + delay;

            candidate.status = 'queued';

            this.stats.retried++;

            return true;
        }

        recordObservation(observation) {
            this.observations.set(
                observation.id,
                observation
            );

            const resource =
                this.ensureResource(
                    observation.requestedUrl
                );

            resource.merge({
                observationIds: [
                    observation.id
                ],
                candidateIds: [
                    observation.candidateId
                ],
                status:
                    observation.status ===
                    'success'
                        ? 'acquired'
                        : 'observed',
                fingerprint:
                    observation.fingerprint,
                finalUrl:
                    observation.http?.finalUrl
            });

            if (observation.fingerprint) {
                const hash =
                    observation.fingerprint.hash;

                if (!this.fingerprintIndex.has(hash)) {
                    this.fingerprintIndex.set(
                        hash,
                        new Set()
                    );
                }

                this.fingerprintIndex
                    .get(hash)
                    .add(observation.requestedUrl);
            }
        }

        addDiscovery(discovery) {
            this.discoveries.set(
                discovery.id,
                discovery
            );

            const target =
                discovery.targetUrl();

            if (target) {
                const canonical =
                    canonicalizeUrl(target);

                if (canonical) {
                    const resource =
                        this.ensureResource(canonical);

                    resource.merge({
                        mechanisms: [
                            discovery.mechanism
                        ],
                        discoveryIds: [
                            discovery.id
                        ]
                    });
                }
            }
        }

        ensureResource(url) {
            const canonical =
                canonicalizeUrl(url);

            if (!canonical) {
                return null;
            }

            let resource =
                this.resources.get(canonical);

            if (!resource) {
                resource =
                    new ResourceRecord({
                        url: canonical
                    });

                this.resources.set(
                    canonical,
                    resource
                );
            }

            return resource;
        }

        addEdge(from, to, relation) {
            if (!from || !to) return;

            if (
                this.graphEdges.length >=
                CONFIG.maxGraphEdges
            ) {
                return;
            }

            this.graphEdges.push({
                id: makeId('edge'),
                from,
                to,
                relation,
                createdAt: now()
            });
        }

        recordDiagnostic(type, data = {}) {
            this.diagnostics.push({
                id: makeId('diag'),
                type,
                timestamp: now(),
                data
            });

            if (
                this.diagnostics.length >
                CONFIG.maxDiagnostics
            ) {
                this.diagnostics.shift();
            }
        }

        shouldAcquireResource(url) {
            const resource =
                this.resources.get(
                    canonicalizeUrl(url)
                );

            return !resource ||
                resource.status !== 'acquired';
        }

        serialize() {
            return {
                version: CONFIG.version,

                candidates: [
                    ...this.candidates.values()
                ].map(c => c.serialize()),

                observations: [
                    ...this.observations.values()
                ].map(o => o.serialize()),

                discoveries: [
                    ...this.discoveries.values()
                ]
                    .slice(-CONFIG.persistedDiscoveries)
                    .map(d => d.serialize()),

                resources: [
                    ...this.resources.values()
                ]
                    .slice(-CONFIG.persistedResources)
                    .map(r => r.serialize()),

                visited: [
                    ...this.visited
                ],

                graphEdges:
                    this.graphEdges.slice(
                        -CONFIG.persistedEdges
                    ),

                stats: {
                    ...this.stats
                }
            };
        }

        restore(data) {
            if (!data) return;

            for (const raw of safeArray(
                data.candidates
            )) {
                const candidate =
                    new Candidate(raw);

                this.candidates.set(
                    candidate.id,
                    candidate
                );

                this.candidateKeys.set(
                    candidate.identityKey(),
                    candidate.id
                );
            }

            for (const raw of safeArray(
                data.observations
            )) {
                const observation =
                    new Observation(raw);

                this.observations.set(
                    observation.id,
                    observation
                );
            }

            for (const raw of safeArray(
                data.discoveries
            )) {
                const discovery =
                    new Discovery(raw);

                this.discoveries.set(
                    discovery.id,
                    discovery
                );
            }

            for (const raw of safeArray(
                data.resources
            )) {
                const resource =
                    new ResourceRecord(raw);

                this.resources.set(
                    resource.url,
                    resource
                );
            }

            this.visited =
                new Set(
                    safeArray(data.visited)
                );

            this.graphEdges =
                safeArray(data.graphEdges);

            for (const resource of this.resources.values()) {
                if (resource.fingerprint?.hash) {
                    const hash =
                        resource.fingerprint.hash;

                    if (
                        !this.fingerprintIndex.has(hash)
                    ) {
                        this.fingerprintIndex.set(
                            hash,
                            new Set()
                        );
                    }

                    this.fingerprintIndex
                        .get(hash)
                        .add(resource.url);
                }
            }
        }
    }
