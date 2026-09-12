// src/knowledge.js — KnowledgeBase
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

            this.patternIndex = new Map();
            this.clusterIndex = new Map();

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

            if (this.visited.has(key)) {
                this.recordDiagnostic(
                    'candidate-visited',
                    {
                        key,
                        target: candidate.target
                    }
                );

                return null;
            }

            // P0-1 FIX: count live only (exclude completed/skipped)
            const liveCount = [...this.candidates.values()].filter(
                c =>
                    !['completed', 'skipped'].includes(
                        c.status
                    )
            ).length;

            if (
                liveCount >= CONFIG.maxCandidates
            ) {
                this.recordDiagnostic(
                    'candidate-cap-reached',
                    {
                        target: candidate.target,
                        liveCount,
                        cap: CONFIG.maxCandidates
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

            this.recordPattern(candidate);

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
            this._validateTransition(candidate, 'queued');

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

                if (
                    CONFIG.candidateTTL > 0 &&
                    candidate.createdAt &&
                    now() - candidate.createdAt > CONFIG.candidateTTL
                ) {
                    this.markSkipped(candidate, 'ttl-expired');
                    this.recordDiagnostic('candidate-ttl-expired', {
                        id: candidate.id,
                        target: candidate.target,
                        age: now() - candidate.createdAt,
                        ttl: CONFIG.candidateTTL
                    });
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

            this._validateTransition(candidate, 'claimed');
            candidate.status = 'claimed';
            candidate.claimedAt = now();

            this.claimed.add(candidate.id);
            this.stats.claimed++;

            return candidate;
        }

        markPlanned(candidate) {
            this._validateTransition(candidate, 'planned');
            candidate.status = 'planned';
            candidate.plannedAt = now();
            this.stats.planned++;
        }

        markAcquiring(candidate) {
            this._validateTransition(candidate, 'acquiring');
            candidate.status = 'acquiring';
            candidate.acquiringAt = now();
        }

        markObserved(candidate) {
            this._validateTransition(candidate, 'observed');
            candidate.status = 'observed';
            candidate.observedAt = now();
        }

        markRecognized(candidate) {
            this._validateTransition(candidate, 'recognized');
            candidate.status = 'recognized';
            candidate.recognizedAt = now();
            this.stats.recognized++;
        }

        markExpanded(candidate) {
            this._validateTransition(candidate, 'expanded');
            candidate.status = 'expanded';
            candidate.expandedAt = now();
            this.stats.expanded++;
        }

        markCompleted(candidate) {
            this._validateTransition(candidate, 'completed');
            candidate.status = 'completed';
            candidate.completedAt = now();
            this.visited.add(candidate.identityKey());
            this.stats.completed++;
        }

        markSkipped(candidate, reason) {
            this._validateTransition(candidate, 'skipped');
            candidate.status = 'skipped';
            candidate.skippedAt = now();
            this.visited.add(candidate.identityKey());

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
            this._validateTransition(candidate, 'failed');
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

            this._validateTransition(candidate, 'queued');
            candidate.status = 'queued';

            this.stats.retried++;

            return true;
        }

        recordObservation(observation) {
            // P0-3: cap in-memory observations (FIFO) to avoid unbounded heap
            if (
                this.observations.size >=
                CONFIG.maxObservationsInMemory
            ) {
                const firstKey = this.observations.keys().next().value;
                if (firstKey) this.observations.delete(firstKey);
                this.recordDiagnostic('observation-evicted', {
                    max: CONFIG.maxObservationsInMemory
                });
            }

            this.observations.set(
                observation.id,
                observation
            );

            const _oldHash = (() => {
                try {
                    const prev = this.resources.get(
                        canonicalizeUrl(observation.requestedUrl) ||
                            observation.requestedUrl
                    );
                    return prev?.fingerprint?.hash || null;
                } catch {
                    return null;
                }
            })();

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

                if (
                    CONFIG.changeDetection &&
                    _oldHash &&
                    hash !== _oldHash
                ) {
                    this.recordDiagnostic('resource-changed', {
                        target: observation.requestedUrl,
                        oldHash: _oldHash,
                        newHash: hash
                    });
                    // mark resource as changed (overwrites acquired)
                    try {
                        const res = this.resources.get(
                            canonicalizeUrl(observation.requestedUrl) ||
                                observation.requestedUrl
                        );
                        if (res) res.status = 'changed';
                    } catch {}
                }
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

        _validateTransition(candidate, to) {
            const from = candidate.status;
            if (from === to) return true;
            const allowed = {
                discovered: ['queued'],
                queued: ['claimed', 'skipped', 'failed'],
                claimed: ['planned', 'skipped'],
                planned: ['acquiring', 'completed', 'skipped'],
                acquiring: ['observed'],
                observed: ['recognized', 'completed', 'queued', 'failed'],
                recognized: ['expanded'],
                expanded: ['completed'],
                completed: [],
                skipped: [],
                failed: ['queued']
            };
            const ok = (allowed[from] || []).includes(to);
            if (!ok) {
                this.recordDiagnostic('lifecycle-illegal-transition', {
                    id: candidate.id,
                    target: candidate.target,
                    from,
                    to,
                    allowed: allowed[from] || []
                });
                if (CONFIG.lifecycle && CONFIG.lifecycle.strict) {
                    throw new Error(`lifecycle illegal: ${from} -> ${to}`);
                }
            }
            return ok || !(CONFIG.lifecycle && CONFIG.lifecycle.strict);
        }

        recordPattern(candidate) {
            if (!CONFIG.inference || !CONFIG.inference.patternInference) return;
            try {
                const pattern = extractUrlPattern(candidate.target);
                this.patternIndex.set(pattern, (this.patternIndex.get(pattern) || 0) + 1);
                if (CONFIG.inference.clustering) {
                    const key = clusterKeyForCandidate(candidate);
                    this.clusterIndex.set(key, (this.clusterIndex.get(key) || 0) + 1);
                }
            } catch {}
        }

        getPatternMetrics() {
            const sorted = [...this.patternIndex.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20);
            return { size: this.patternIndex.size, top: sorted, total: [...this.patternIndex.values()].reduce((a, b) => a + b, 0) };
        }

        getClusterMetrics() {
            const sorted = [...this.clusterIndex.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20);
            return { size: this.clusterIndex.size, top: sorted, total: [...this.clusterIndex.values()].reduce((a, b) => a + b, 0) };
        }

        suggestPatternCandidates(limit = CONFIG.patternGuided?.maxSuggestions || 5) {
            if (!CONFIG.patternGuided?.enabled || !CONFIG.inference?.patternInference) return [];
            const metrics = this.getPatternMetrics();
            const suggestions = [];
            for (const [pattern, count] of metrics.top) {
                if (count < (CONFIG.inference.minPatternFreq || 3)) continue;
                if (!pattern.includes('{int}') && !pattern.includes('{hash}') && !pattern.includes('{uuid}')) continue;
                let suggestion = pattern;
                // deterministic replacements
                suggestion = suggestion.replace('{int}', '0');
                suggestion = suggestion.replace('{hash}', '0'.repeat(32));
                suggestion = suggestion.replace('{uuid}', '00000000-0000-4000-a000-000000000000');
                // handle query patterns like ?id={int}
                suggestion = suggestion.replace('={int}', '=0').replace('={hash}', '='+'0'.repeat(32)).replace('={uuid}', '=00000000-0000-4000-a000-000000000000');
                const key = `url:${suggestion}`;
                if (this.visited.has(key) || this.candidateKeys.has(key)) continue;
                // also need isAllowedUrl check (sameOriginOnly)
                try { if (!isAllowedUrl(suggestion)) continue; } catch { continue; }
                suggestions.push({ pattern, count, suggestion });
                if (suggestions.length >= limit) break;
            }
            return suggestions;
        }

        getChangedResources() {
            return [...this.resources.values()].filter(r => r.status === 'changed');
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

    /*
     * ============================================================
     * ACQUISITION POLICY
     * ============================================================
     */

