    class KnowledgeBase {
        constructor() {
            this.candidates = new Map();
            this.observations = new Map();
            this.discoveries = new Map();
            this.resources = new Map();

            this.visited = new Set();
            this.claimed = new Set();

            this.edges = [];

            this.networkEvents = new Map();

            this.fingerprintIndex = new Map();

            this.diagnostics = [];

            this.stats = {
                candidatesDiscovered: 0,
                candidatesQueued: 0,
                candidatesCompleted: 0,
                candidatesFailed: 0,

                requestsStarted: 0,
                requestsSucceeded: 0,
                requestsFailed: 0,

                policySkips: 0,
                originBudgetSkips: 0,

                discoveries: 0,
                resources: 0,

                duplicateContent: 0,

                networkEvents: 0,
                graphEdges: 0
            };

            this.persistenceTimer = null;

            this.load();
        }

        recordDiagnostic(type, data = {}) {
            this.diagnostics.push({
                id: makeId('diag'),
                type,
                data,
                timestamp: now()
            });

            while (this.diagnostics.length > CONFIG.maxDiagnostics) {
                this.diagnostics.shift();
            }
        }

        ensureResource(url, type = null, mechanism = null) {
            const canonical = canonicalizeUrl(url);

            if (!canonical) {
                return null;
            }

            let resource = this.resources.get(canonical);

            if (!resource) {
                resource = new ResourceRecord({
                    url: canonical
                });

                this.resources.set(canonical, resource);
                this.stats.resources++;
            }

            if (type) resource.addType(type);
            if (mechanism) resource.addMechanism(mechanism);

            resource.lastSeenAt = now();

            return resource;
        }

        addCandidate(input) {
            const candidate = input instanceof Candidate
                ? input
                : new Candidate(input);

            candidate.target = canonicalizeUrl(candidate.target);

            if (!candidate.target || !isAllowedUrl(candidate.target)) {
                return null;
            }

            if (candidate.depth > CONFIG.maxDepth) {
                this.recordDiagnostic('candidate-depth-limit', {
                    target: candidate.target,
                    depth: candidate.depth
                });

                return null;
            }

            const resource = this.ensureResource(
                candidate.target,
                candidate.type,
                candidate.hints.mechanism || 'candidate'
            );

            if (!resource) {
                return null;
            }

            resource.candidateIds.add(candidate.id);

            if (candidate.parent) {
                resource.parents.add(candidate.parent);
            }

            this.recordCandidateEdge(candidate);

            const existing = this.candidates.get(candidate.key());

            if (existing) {
                existing.priority = Math.max(
                    existing.priority,
                    candidate.priority
                );

                existing.hints = {
                    ...existing.hints,
                    ...candidate.hints
                };

                existing.alternateOrigins.add(candidate.origin);

                if (candidate.parent) {
                    existing.alternateParents.add(candidate.parent);
                }

                if (candidate.type !== existing.type) {
                    existing.alternateTypes.add(candidate.type);
                }

                return existing;
            }

            if (this.candidates.size >= CONFIG.maxCandidates) {
                this.recordDiagnostic('candidate-limit', {
                    target: candidate.target
                });

                return null;
            }

            candidate.mark('queued');

            this.candidates.set(candidate.key(), candidate);

            this.stats.candidatesDiscovered++;
            this.stats.candidatesQueued++;

            this.persistSoon();

            return candidate;
        }

        recordCandidateEdge(candidate) {
            if (this.edges.length >= CONFIG.maxGraphEdges) {
                return;
            }

            this.edges.push({
                id: makeId('edge'),
                from: candidate.parent || location.href,
                to: candidate.target,
                kind: 'candidate',
                mechanism: candidate.hints.mechanism || 'candidate',
                candidateType: candidate.type,
                confidence: candidate.hints.confidence ?? null,
                priority: candidate.priority,
                depth: candidate.depth,
                createdAt: now()
            });

            this.stats.graphEdges = this.edges.length;
        }

        claimNextCandidate() {
            const timestamp = now();

            const candidates = [...this.candidates.values()]
                .filter(candidate =>
                    candidate.status === 'queued' &&
                    candidate.nextAttemptAt <= timestamp
                )
                .sort((a, b) =>
                    b.effectivePriority() - a.effectivePriority()
                );

            for (const candidate of candidates) {
                candidate.mark('claimed');
                this.claimed.add(candidate.id);

                return candidate;
            }

            return null;
        }

        requeue(candidate) {
            if (!candidate) return;

            candidate.mark('queued');
            candidate.nextAttemptAt = 0;

            this.claimed.delete(candidate.id);
        }

        addObservation(observation) {
            this.observations.set(
                observation.id,
                observation
            );

            const resource = this.ensureResource(
                observation.requestedUrl || observation.target
            );

            if (resource) {
                resource.observationIds.add(observation.id);

                if (observation.http.finalUrl) {
                    resource.finalUrl = observation.http.finalUrl;
                }

                if (observation.fingerprint) {
                    this.indexFingerprint(
                        resource,
                        observation.fingerprint
                    );
                }

                resource.status =
                    observation.status === 'skipped'
                        ? 'skipped'
                        : observation.status === 'error'
                            ? 'failed'
                            : 'acquired';
            }

            this.persistSoon();
        }

        indexFingerprint(resource, fingerprint) {
            if (!resource || !fingerprint) {
                return;
            }

            resource.fingerprint = fingerprint;

            let urls = this.fingerprintIndex.get(fingerprint);

            if (!urls) {
                urls = new Set();
                this.fingerprintIndex.set(fingerprint, urls);
            }

            if (!urls.has(resource.url)) {
                if (urls.size > 0) {
                    this.stats.duplicateContent++;

                    this.recordDiagnostic(
                        'duplicate-content',
                        {
                            fingerprint,
                            url: resource.url,
                            existingUrls: [...urls]
                        }
                    );
                }

                urls.add(resource.url);
            }
        }

        addDiscovery(discovery) {
            this.discoveries.set(
                discovery.id,
                discovery
            );

            this.stats.discoveries++;

            if (discovery.candidateId) {
                const candidate =
                    [...this.candidates.values()]
                        .find(c => c.id === discovery.candidateId);

                if (candidate) {
                    const resource = this.ensureResource(
                        candidate.target,
                        candidate.type,
                        discovery.mechanism
                    );

                    if (resource) {
                        resource.discoveryIds.add(discovery.id);
                    }
                }
            }

            this.persistSoon();
        }

        addNetworkEvent(event) {
            this.networkEvents.set(event.id, event);

            while (
                this.networkEvents.size >
                CONFIG.maxNetworkEvents
            ) {
                const first = this.networkEvents.keys().next().value;
                this.networkEvents.delete(first);
            }

            this.stats.networkEvents = this.networkEvents.size;

            if (event.url) {
                const type = classifyNetworkType(event);

                const resource = this.ensureResource(
                    event.url,
                    type,
                    `network:${event.api}`
                );

                if (resource) {
                    resource.networkEventIds.add(event.id);

                    if (event.finalUrl) {
                        resource.finalUrl = event.finalUrl;
                    }

                    if (event.status >= 200 && event.status < 400) {
                        resource.status =
                            resource.status === 'acquired'
                                ? 'acquired'
                                : 'observed';
                    }
                }
            }

            this.persistSoon();
        }

        completeCandidate(candidate) {
            candidate.mark('completed');

            this.claimed.delete(candidate.id);
            this.visited.add(candidate.target);

            this.stats.candidatesCompleted++;

            this.persistSoon();
        }

        failCandidate(candidate, error) {
            candidate.attempts++;
            candidate.failedAt = now();

            if (
                candidate.attempts <= CONFIG.retry.maxRetries &&
                !engine.stopRequested
            ) {
                const delay = Math.min(
                    CONFIG.retry.maxDelay,
                    CONFIG.retry.baseDelay *
                    Math.pow(2, candidate.attempts - 1)
                );

                candidate.nextAttemptAt = now() + delay;
                candidate.status = 'queued';

                this.recordDiagnostic('candidate-retry', {
                    candidateId: candidate.id,
                    target: candidate.target,
                    attempt: candidate.attempts,
                    delay,
                    error: String(error || '')
                });
            } else {
                candidate.status = 'failed';
                this.stats.candidatesFailed++;

                this.recordDiagnostic('candidate-failed', {
                    candidateId: candidate.id,
                    target: candidate.target,
                    attempts: candidate.attempts,
                    error: String(error || '')
                });
            }

            this.claimed.delete(candidate.id);

            this.persistSoon();
        }

        markSkipped(candidate, reason) {
            candidate.mark('completed');

            this.claimed.delete(candidate.id);
            this.visited.add(candidate.target);

            const resource = this.ensureResource(
                candidate.target,
                candidate.type,
                'policy'
            );

            if (resource) {
                resource.status = 'skipped';
                resource.skipReason = reason;
            }

            this.stats.policySkips++;

            if (reason === 'origin-budget') {
                this.stats.originBudgetSkips++;
            }

            const observation = new Observation({
                candidateId: candidate.id,
                target: candidate.target,
                requestedUrl: candidate.target,
                startedAt: now(),
                completedAt: now(),
                status: 'skipped',
                reason
            });

            this.addObservation(observation);

            this.recordDiagnostic('candidate-skipped', {
                candidateId: candidate.id,
                target: candidate.target,
                reason
            });

            this.persistSoon();
        }

        recordRedirect(from, to) {
            if (!from || !to || from === to) {
                return;
            }

            if (this.edges.length >= CONFIG.maxGraphEdges) {
                return;
            }

            this.edges.push({
                id: makeId('edge'),
                from,
                to,
                kind: 'redirect',
                createdAt: now()
            });

            this.stats.graphEdges = this.edges.length;
        }

        serializePersistence() {
            return {
                version: 6,
                visited: [...this.visited],

                resources: [...this.resources.values()]
                    .slice(-CONFIG.persistedResources)
                    .map(resource => resource.serialize()),

                discoveries: [...this.discoveries.values()]
                    .slice(-CONFIG.persistedDiscoveries)
                    .map(discovery => discovery.serialize()),

                edges: this.edges
                    .slice(-CONFIG.persistedEdges)
            };
        }

        persistSoon() {
            if (!CONFIG.persistence) {
                return;
            }

            clearTimeout(this.persistenceTimer);

            this.persistenceTimer = setTimeout(() => {
                try {
                    GM_setValue(
                        'gde-state',
                        JSON.stringify(this.serializePersistence())
                    );
                } catch (error) {
                    warn('Persistence failed', error);
                }
            }, CONFIG.persistenceDebounce);
        }

        load() {
            if (!CONFIG.persistence) {
                return;
            }

            try {
                const raw = GM_getValue('gde-state', '');

                if (!raw) {
                    return;
                }

                const data = JSON.parse(raw);

                if (
                    !data ||
                    ![5, 6].includes(data.version)
                ) {
                    return;
                }

                for (const target of safeArray(data.visited)) {
                    this.visited.add(target);
                }

                for (const item of safeArray(data.resources)) {
                    const resource =
                        new ResourceRecord(item);

                    this.resources.set(
                        resource.url,
                        resource
                    );

                    if (resource.fingerprint) {
                        let group =
                            this.fingerprintIndex.get(
                                resource.fingerprint
                            );

                        if (!group) {
                            group = new Set();
                            this.fingerprintIndex.set(
                                resource.fingerprint,
                                group
                            );
                        }

                        group.add(resource.url);
                    }
                }

                for (const item of safeArray(data.discoveries)) {
                    const discovery =
                        new Discovery(item);

                    this.discoveries.set(
                        discovery.id,
                        discovery
                    );
                }

                this.edges = safeArray(data.edges)
                    .slice(-CONFIG.persistedEdges);

                this.stats.resources =
                    this.resources.size;

                this.stats.discoveries =
                    this.discoveries.size;

                this.stats.graphEdges =
                    this.edges.length;

                log(
                    'Loaded persistent state',
                    data.version
                );
            } catch (error) {
                warn('State load failed', error);
            }
        }

        clear() {
            this.candidates.clear();
            this.observations.clear();
            this.discoveries.clear();
            this.resources.clear();
            this.visited.clear();
            this.claimed.clear();
            this.edges = [];
            this.networkEvents.clear();
            this.fingerprintIndex.clear();
            this.diagnostics = [];

            for (const key of Object.keys(this.stats)) {
                this.stats[key] = 0;
            }

            if (CONFIG.persistence) {
                try {
                    GM_setValue(
                        'gde-state',
                        ''
                    );
                } catch {
                    // Ignore persistence errors during clear.
                }
            }
        }
    }
