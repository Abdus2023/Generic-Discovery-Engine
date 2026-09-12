    class KnowledgeBase {
        constructor() {
            this.queue = [];

            this.candidates =
                new Map();

            this.observations =
                new Map();

            this.discoveries =
                new Map();

            this.resources =
                new Map();

            this.visited =
                new Set();

            this.claimed =
                new Set();

            this.edgeRecords =
                [];

            this.fingerprintIndex =
                new Map();

            this.persistTimer =
                null;

            this.statistics = this.makeStatistics();

            this.load();
        }

        makeStatistics() {
            return {
                candidatesCreated: 0,
                candidatesMerged: 0,
                candidatesRejected: 0,
                maxDepthReached: 0,

                requests: 0,
                observations: 0,
                discoveries: 0,

                retries: 0,
                failures: 0,

                cacheSkips: 0,

                policySkips: 0,
                originBudgetSkips: 0,

                networkEvents: 0,
                networkCandidates: 0,
                performanceCandidates: 0,

                providerMatches: 0,

                duplicateContent: 0,

                redirects: 0,

                successes: 0,

                pauses: 0,
                resumes: 0,

                adaptiveConcurrencyChanges: 0
            };
        }

        ensureResource(target) {
            if (!target) {
                return null;
            }

            let record =
                this.resources.get(
                    target
                );

            if (!record) {
                record =
                    new ResourceRecord(
                        target
                    );

                this.resources.set(
                    target,
                    record
                );
            }

            return record;
        }

        getResource(target) {
            return this.resources.get(
                target
            ) || null;
        }

        resourceAlreadyAcquired(target) {
            const record =
                this.getResource(
                    target
                );

            return !!(
                record &&
                record.status ===
                    'acquired' &&
                record.fingerprint
            );
        }

        addCandidate(candidate) {
            if (!(candidate instanceof Candidate)) {
                return false;
            }

            const canonical =
                canonicalizeUrl(
                    candidate.target
                );

            if (
                !canonical ||
                !isAllowedUrl(canonical)
            ) {
                this.statistics
                    .candidatesRejected++;

                return false;
            }

            candidate.target =
                canonical;

            if (
                candidate.depth >
                CONFIG.maxDepth
            ) {
                this.statistics
                    .maxDepthReached++;

                this.statistics
                    .candidatesRejected++;

                return false;
            }

            const resource =
                this.ensureResource(
                    candidate.target
                );

            resource.mergeCandidate(
                candidate
            );

            this.recordCandidateEdge(
                candidate
            );

            const key =
                candidate.key();

            const existing =
                this.candidates.get(
                    key
                );

            if (existing) {
                existing.merge(
                    candidate
                );

                this.statistics
                    .candidatesMerged++;

                return false;
            }

            if (this.visited.has(key)) {
                this.statistics
                    .candidatesMerged++;

                return false;
            }

            if (this.claimed.has(key)) {
                this.statistics
                    .candidatesMerged++;

                return false;
            }

            if (
                this.resourceAlreadyAcquired(
                    candidate.target
                )
            ) {
                this.visited.add(key);

                this.statistics
                    .cacheSkips++;

                return false;
            }

            if (
                this.queue.length >=
                CONFIG.maxCandidates
            ) {
                this.statistics
                    .candidatesRejected++;

                return false;
            }

            candidate.transition(
                'queued'
            );

            this.candidates.set(
                key,
                candidate
            );

            this.queue.push(
                candidate
            );

            this.statistics
                .candidatesCreated++;

            this.schedulePersist();

            return true;
        }

        recordCandidateEdge(candidate) {
            if (
                this.edgeRecords.length >=
                CONFIG.maxGraphEdges
            ) {
                return;
            }

            const source =
                candidate.parent ||
                null;

            const duplicate =
                this.edgeRecords.some(
                    edge =>
                        edge.fromDiscoveryId ===
                            source &&
                        edge.target ===
                            candidate.target &&
                        edge.mechanism ===
                            candidate.origin &&
                        edge.candidateType ===
                            candidate.type
                );

            if (duplicate) {
                return;
            }

            this.edgeRecords.push({
                id:
                    makeId('edge'),

                fromDiscoveryId:
                    source,

                target:
                    candidate.target,

                mechanism:
                    candidate.origin,

                candidateType:
                    candidate.type,

                confidence:
                    Number(
                        candidate.hints.confidence ||
                        0.5
                    ),

                priority:
                    candidate.priority,

                depth:
                    candidate.depth,

                createdAt:
                    now()
            });
        }

        claimNextCandidate() {
            const timestamp =
                now();

            const ready =
                this.queue.filter(
                    candidate =>
                        candidate.nextAttemptAt <=
                        timestamp
                );

            if (!ready.length) {
                return null;
            }

            ready.sort(
                (a, b) => {
                    const priority =
                        b.effectivePriority() -
                        a.effectivePriority();

                    if (priority !== 0) {
                        return priority;
                    }

                    return (
                        a.createdAt -
                        b.createdAt
                    );
                }
            );

            const candidate =
                ready[0];

            const index =
                this.queue.indexOf(
                    candidate
                );

            if (index >= 0) {
                this.queue.splice(
                    index,
                    1
                );
            }

            const key =
                candidate.key();

            this.candidates.delete(
                key
            );

            this.claimed.add(
                key
            );

            candidate.transition(
                'claimed'
            );

            return candidate;
        }

        nextReadyDelay() {
            if (!this.queue.length) {
                return null;
            }

            const timestamp =
                now();

            let earliest =
                Infinity;

            for (
                const candidate of
                this.queue
            ) {
                earliest =
                    Math.min(
                        earliest,
                        candidate.nextAttemptAt ||
                            timestamp
                    );
            }

            return Math.max(
                0,
                earliest - timestamp
            );
        }

        addObservation(observation) {
            this.observations.set(
                observation.id,
                observation
            );

            const resource =
                this.ensureResource(
                    observation.target
                );

            resource.mergeObservation(
                observation
            );

            this.statistics
                .observations++;

            this.schedulePersist();
        }

        addDiscovery(discovery) {
            this.discoveries.set(
                discovery.id,
                discovery
            );

            const target =
                discovery.targetUrl();

            if (target) {
                const resource =
                    this.ensureResource(
                        target
                    );

                resource.mergeDiscovery(
                    discovery
                );
            }

            this.statistics
                .discoveries++;

            this.statistics
                .providerMatches++;

            this.schedulePersist();
        }

        markDuplicateContent(
            resource,
            fingerprint
        ) {
            if (
                !CONFIG.detectDuplicateContent ||
                !fingerprint?.bodyHash
            ) {
                return;
            }

            const hash =
                fingerprint.bodyHash;

            let group =
                this.fingerprintIndex.get(
                    hash
                );

            if (!group) {
                group = new Set();

                this.fingerprintIndex.set(
                    hash,
                    group
                );
            }

            if (
                group.has(
                    resource.url
                )
            ) {
                return;
            }

            if (group.size > 0) {
                this.statistics
                    .duplicateContent++;

                resource.duplicateFingerprint =
                    hash;
            }

            group.add(
                resource.url
            );

            while (
                this.fingerprintIndex.size >
                CONFIG.maxDuplicateGroups
            ) {
                const oldest =
                    this.fingerprintIndex.keys()
                        .next()
                        .value;

                if (!oldest) {
                    break;
                }

                this.fingerprintIndex.delete(
                    oldest
                );
            }
        }

        markResourceAcquired(
            requestedUrl,
            observation
        ) {
            const resource =
                this.ensureResource(
                    requestedUrl
                );

            resource.status =
                'acquired';

            resource.fingerprint =
                observation.fingerprint;

            resource.finalUrl =
                observation.http.finalUrl ||
                requestedUrl;

            if (
                resource.finalUrl !==
                requestedUrl
            ) {
                resource.redirectTo =
                    resource.finalUrl;

                this.statistics
                    .redirects++;

                this.ensureResource(
                    resource.finalUrl
                );
            }

            this.markDuplicateContent(
                resource,
                observation.fingerprint
            );
        }

        completeCandidate(candidate) {
            candidate.transition(
                'completed'
            );

            this.claimed.delete(
                candidate.key()
            );

            this.visited.add(
                candidate.key()
            );

            this.statistics.successes++;

            this.schedulePersist();
        }

        skipCandidate(
            candidate,
            reason
        ) {
            candidate.hints.skipReason =
                reason;

            candidate.transition(
                'skipped'
            );

            this.claimed.delete(
                candidate.key()
            );

            this.visited.add(
                candidate.key()
            );

            const resource =
                this.ensureResource(
                    candidate.target
                );

            resource.status =
                'skipped';

            this.statistics.policySkips++;

            this.schedulePersist();
        }

        failCandidate(
            candidate,
            error
        ) {
            candidate.attempts++;

            candidate.hints.lastError =
                String(
                    error?.message ||
                    error ||
                    'unknown error'
                );

            if (
                candidate.attempts <=
                CONFIG.maxRetries
            ) {
                const delay =
                    Math.min(
                        CONFIG.retryMaxDelay,
                        CONFIG.retryBaseDelay *
                            Math.pow(
                                2,
                                candidate.attempts - 1
                            )
                    );

                candidate.nextAttemptAt =
                    now() + delay;

                candidate.transition(
                    'queued'
                );

                this.queue.push(
                    candidate
                );

                this.claimed.delete(
                    candidate.key()
                );

                this.statistics
                    .retries++;

                this.schedulePersist();

                return 'retry';
            }

            candidate.transition(
                'failed'
            );

            this.claimed.delete(
                candidate.key()
            );

            this.visited.add(
                candidate.key()
            );

            const resource =
                this.ensureResource(
                    candidate.target
                );

            resource.status =
                'failed';

            this.statistics
                .failures++;

            this.schedulePersist();

            return 'failed';
        }

        schedulePersist() {
            if (!CONFIG.persistState) {
                return;
            }

            clearTimeout(
                this.persistTimer
            );

            this.persistTimer =
                setTimeout(
                    () => this.persistNow(),
                    CONFIG.persistDebounceMs
                );
        }

        persistNow() {
            if (!CONFIG.persistState) {
                return;
            }

            try {
                const resources =
                    [
                        ...this.resources.values()
                    ].slice(
                        -CONFIG.maxPersistedResources
                    );

                const discoveries =
                    [
                        ...this.discoveries.values()
                    ].slice(
                        -CONFIG.maxPersistedDiscoveries
                    );

                const edges =
                    this.edgeRecords.slice(
                        -CONFIG.maxPersistedEdges
                    );

                GM_setValue(
                    'genericDiscoveryState',
                    {
                        version: 6,

                        savedAt:
                            now(),

                        visited:
                            [
                                ...this.visited
                            ].slice(-3000),

                        discoveries,

                        resources:
                            resources.map(
                                resource =>
                                    resource.toJSON()
                            ),

                        edges,

                        fingerprintGroups:
                            [
                                ...this.fingerprintIndex
                            ]
                                .slice(
                                    -CONFIG.maxDuplicateGroups
                                )
                                .map(
                                    ([hash, urls]) => [
                                        hash,
                                        [
                                            ...urls
                                        ]
                                    ]
                                )
                    }
                );
            } catch (error) {
                warn(
                    'Persistence failed:',
                    error
                );
            }
        }

        load() {
            if (!CONFIG.persistState) {
                return;
            }

            try {
                const state =
                    GM_getValue(
                        'genericDiscoveryState',
                        null
                    );

                if (!state) {
                    return;
                }

                this.visited =
                    new Set(
                        safeArray(
                            state.visited
                        )
                    );

                for (
                    const discovery of
                    safeArray(
                        state.discoveries
                    )
                ) {
                    if (!discovery?.id) {
                        continue;
                    }

                    this.discoveries.set(
                        discovery.id,
                        discovery
                    );
                }

                for (
                    const raw of
                    safeArray(
                        state.resources
                    )
                ) {
                    if (!raw?.url) {
                        continue;
                    }

                    this.resources.set(
                        raw.url,
                        ResourceRecord.fromJSON(
                            raw
                        )
                    );
                }

                this.edgeRecords =
                    safeArray(
                        state.edges
                    ).slice(
                        -CONFIG.maxPersistedEdges
                    );

                for (
                    const [
                        hash,
                        urls
                    ] of
                    safeArray(
                        state.fingerprintGroups
                    )
                ) {
                    this.fingerprintIndex.set(
                        hash,
                        new Set(
                            safeArray(urls)
                        )
                    );
                }

                /*
                 * Compatibility with v0.4/v0.5 persistence:
                 * reconstruct resource knowledge from discoveries.
                 */
                for (
                    const discovery of
                    this.discoveries.values()
                ) {
                    const target =
                        discovery?.provenance
                            ?.candidateTarget ||
                        discovery?.data?.url ||
                        null;

                    const canonical =
                        canonicalizeUrl(
                            target
                        );

                    if (!canonical) {
                        continue;
                    }

                    const resource =
                        this.ensureResource(
                            canonical
                        );

                    resource.discoveryIds.add(
                        discovery.id
                    );
                }

                /*
                 * Rebuild the fingerprint index if it was not persisted.
                 */
                if (
                    this.fingerprintIndex.size === 0
                ) {
                    for (
                        const resource of
                        this.resources.values()
                    ) {
                        const hash =
                            resource
                                .fingerprint
                                ?.bodyHash;

                        if (!hash) {
                            continue;
                        }

                        if (
                            !this.fingerprintIndex.has(
                                hash
                            )
                        ) {
                            this.fingerprintIndex.set(
                                hash,
                                new Set()
                            );
                        }

                        this.fingerprintIndex
                            .get(hash)
                            .add(
                                resource.url
                            );
                    }
                }

                log(
                    'Restored state:',
                    this.resources.size,
                    'resources,',
                    this.discoveries.size,
                    'discoveries'
                );
            } catch (error) {
                warn(
                    'State restore failed:',
                    error
                );
            }
        }

        clear() {
            clearTimeout(
                this.persistTimer
            );

            this.queue.length = 0;

            this.candidates.clear();
            this.observations.clear();
            this.discoveries.clear();
            this.resources.clear();

            this.visited.clear();
            this.claimed.clear();

            this.edgeRecords.length = 0;
            this.fingerprintIndex.clear();

            this.statistics =
                this.makeStatistics();

            try {
                if (CONFIG.persistState) {
                    GM_setValue(
                        'genericDiscoveryState',
                        null
                    );
                }
            } catch (error) {
                warn(
                    'Could not clear persisted state:',
                    error
                );
            }
        }
    }
