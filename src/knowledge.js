// src/knowledge.js — KnowledgeBase — Bounded Knowledge Kernel v1.6
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

        // ---- Retention helpers ----
        _retention(path, fallback) {
            try {
                const parts = path.split('.');
                let cur = CONFIG.retention;
                for (const p of parts) {
                    if (cur == null || !(p in cur)) return fallback;
                    cur = cur[p];
                }
                return cur ?? fallback;
            } catch { return fallback; }
        }
        _maxVisited() { return this._retention('visited.maxEntries', 2000); }
        _maxCandidateKeys() { return this._retention('candidateKeys.maxEntries', 2000); }
        _maxCandidateHistory() { return this._retention('candidateHistory.maxEntries', 2000); }
        _maxObservations() { return this._retention('observations.maxEntries', CONFIG.maxObservationsInMemory ?? 800); }
        _maxBodies() { return this._retention('observations.maxBodies', CONFIG.retention?.observations?.maxBodies ?? CONFIG.runtimeBudget?.maxBodiesInMemory ?? 150); }
        _maxBodyBytes() { return this._retention('observations.maxBodyBytes', CONFIG.retention?.observations?.maxBodyBytes ?? CONFIG.runtimeBudget?.maxBodyBytes ?? 5_000_000); }
        _maxDiscoveries() { return this._retention('discoveries.maxEntries', CONFIG.maxDiscoveriesInMemory ?? 2000); }
        _maxResources() { return this._retention('resources.maxEntries', CONFIG.maxResourcesInMemory ?? 2000); }
        _maxRelations() { return this._retention('resources.maxRelationsPerResource', 100); }
        _maxHashes() { return this._retention('fingerprint.maxHashes', 500); }
        _maxUrlsPerHash() { return this._retention('fingerprint.maxUrlsPerHash', 100); }
        _maxPatterns() { return this._retention('patterns.maxEntries', 500); }
        _maxClusters() { return this._retention('clusters.maxEntries', 500); }

        _enforceVisitedBound() {
            const max = this._maxVisited();
            while (this.visited.size > max) {
                const first = this.visited.values().next().value;
                if (first == null) break;
                this.visited.delete(first);
                this.recordDiagnostic('visited-evicted', { max, evictedKey: String(first).slice(0, 80) });
            }
        }
        _enforceCandidateKeysBound() {
            const max = this._maxCandidateKeys();
            while (this.candidateKeys.size > max) {
                // Prefer evicting historical (completed/skipped/missing) keys first — preserves live frontier index
                let evicted = false;
                for (const [key, id] of this.candidateKeys) {
                    const cand = this.candidates.get(id);
                    const isLive = cand && !['completed', 'skipped'].includes(cand.status);
                    if (!isLive) {
                        this.candidateKeys.delete(key);
                        this.recordDiagnostic('candidateKeys-evicted', { max, key: String(key).slice(0, 80), historical: true });
                        evicted = true;
                        break;
                    }
                }
                if (evicted) continue;
                // All remaining are live — do not evict live frontier; emit pressure and break to avoid breaking dedup
                this.recordDiagnostic('candidateKeys-pressure', { max, liveCount: this.candidateKeys.size, note: 'all keys are live, retention deferred' });
                break;
            }
        }
        _enforceCandidateHistoryBound() {
            const max = this._maxCandidateHistory();
            while (this.candidates.size > max) {
                // Evict oldest historical candidate (completed/skipped) first, FIFO within historical
                let victimId = null;
                for (const [id, cand] of this.candidates) {
                    if (['completed', 'skipped'].includes(cand.status)) { victimId = id; break; }
                }
                if (!victimId) {
                    // No historical to evict — all live (shouldn't exceed 2000 since live cap 750)
                    this.recordDiagnostic('candidate-history-pressure', { max, liveSize: this.candidates.size });
                    break;
                }
                const victim = this.candidates.get(victimId);
                this.candidates.delete(victimId);
                // clean candidateKeys reverse index for this candidate
                if (victim) {
                    const k = victim.identityKey();
                    if (this.candidateKeys.get(k) === victimId) this.candidateKeys.delete(k);
                    // also clean claimed set
                    this.claimed.delete(victimId);
                }
                this.recordDiagnostic('candidate-history-evicted', { max, id: victimId });
                // also clean resource candidateIds references to keep referential coherence
                this._removeCandidateReferences(victimId);
            }
        }
        _removeCandidateReferences(candidateId) {
            if (!candidateId) return;
            for (const res of this.resources.values()) {
                const idx = res.candidateIds.indexOf(candidateId);
                if (idx !== -1) {
                    res.candidateIds.splice(idx, 1);
                }
            }
        }
        _removeObservationReferences(observationId) {
            if (!observationId) return;
            for (const res of this.resources.values()) {
                const i = res.observationIds.indexOf(observationId);
                if (i !== -1) res.observationIds.splice(i, 1);
            }
        }
        _removeDiscoveryReferences(discoveryId) {
            if (!discoveryId) return;
            for (const res of this.resources.values()) {
                const i = res.discoveryIds.indexOf(discoveryId);
                if (i !== -1) res.discoveryIds.splice(i, 1);
            }
        }
        _removeResourceFingerprint(url, fingerprint) {
            try {
                const hash = fingerprint?.hash;
                if (!hash) return;
                const set = this.fingerprintIndex.get(hash);
                if (!set) return;
                set.delete(url);
                if (set.size === 0) this.fingerprintIndex.delete(hash);
            } catch {}
        }
        _enforceFingerprintBound() {
            const maxHashes = this._maxHashes();
            const maxPer = this._maxUrlsPerHash();
            // per-hash URL cap
            for (const [hash, set] of this.fingerprintIndex) {
                while (set.size > maxPer) {
                    const first = set.values().next().value;
                    if (first == null) break;
                    set.delete(first);
                    this.recordDiagnostic('fingerprint-url-evicted', { hash: String(hash).slice(0,16), maxPer });
                }
            }
            // global hash cap — FIFO by insertion order
            while (this.fingerprintIndex.size > maxHashes) {
                const first = this.fingerprintIndex.keys().next().value;
                if (first == null) break;
                this.fingerprintIndex.delete(first);
                this.recordDiagnostic('fingerprint-hash-evicted', { maxHashes });
            }
        }
        _enforcePatternBound() {
            const maxP = this._maxPatterns();
            const maxC = this._maxClusters();
            while (this.patternIndex.size > maxP) {
                const first = this.patternIndex.keys().next().value;
                if (first == null) break;
                this.patternIndex.delete(first);
                this.recordDiagnostic('pattern-evicted', { max: maxP });
            }
            while (this.clusterIndex.size > maxC) {
                const first = this.clusterIndex.keys().next().value;
                if (first == null) break;
                this.clusterIndex.delete(first);
                this.recordDiagnostic('cluster-evicted', { max: maxC });
            }
        }
        _enforceBodyBudget() {
            const maxBodies = this._maxBodies();
            const maxBytes = this._maxBodyBytes();
            // Collect bodies in insertion order
            const bodies = [];
            let total = 0;
            for (const obs of this.observations.values()) {
                if (obs.body && obs.body.length > 0) {
                    bodies.push(obs);
                    total += obs.body.length;
                }
            }
            let evicted = 0;
            while ((bodies.length > maxBodies || total > maxBytes) && bodies.length > 0) {
                const oldest = bodies.shift();
                if (!oldest || !oldest.body) continue;
                total -= oldest.body.length;
                const len = oldest.body.length;
                oldest.body = '';
                oldest.bodyTruncated = true;
                evicted++;
                this.recordDiagnostic('body-evicted', { observationId: oldest.id, len, maxBodies, maxBytes, totalAfter: total });
            }
            if (evicted > 0) {
                // keep total bounded — no further action
            }
        }
        _enforceGraphEdgesBound() {
            const max = this._retention('graphEdges.maxEntries', CONFIG.maxGraphEdges ?? 5000);
            while (this.graphEdges.length > max) {
                this.graphEdges.shift();
                this.recordDiagnostic('graphEdge-evicted', { max });
            }
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
                } else {
                    // Referential integrity fix: stale candidateKeys entry points to missing candidate (evicted) — clean it
                    this.candidateKeys.delete(key);
                    this.recordDiagnostic('candidateKeys-stale-cleaned', { key: String(key).slice(0,80) });
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
            // Enforce retention: candidateKeys and history
            this._enforceCandidateKeysBound();
            this._enforceCandidateHistoryBound();

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
            this._enforceVisitedBound();
            this._enforceCandidateHistoryBound();
            this.stats.completed++;
        }

        markSkipped(candidate, reason) {
            this._validateTransition(candidate, 'skipped');
            candidate.status = 'skipped';
            candidate.skippedAt = now();
            this.visited.add(candidate.identityKey());
            this._enforceVisitedBound();

            const resource =
                this.ensureResource(candidate.target);

            if (resource) {
                resource.merge({
                    status: 'skipped',
                    skipReason: reason,
                    candidateIds: [candidate.id]
                });
            }

            this._enforceCandidateHistoryBound();
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
            // Enforce observations cap with referential cleanup (FIFO)
            const maxObs = this._maxObservations();
            if (
                this.observations.size >= maxObs
            ) {
                const firstKey = this.observations.keys().next().value;
                if (firstKey) {
                    const evicted = this.observations.get(firstKey);
                    this.observations.delete(firstKey);
                    if (evicted) this._removeObservationReferences(evicted.id);
                    this.recordDiagnostic('observation-evicted', {
                        max: maxObs,
                        evictedId: firstKey
                    });
                }
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

            if (resource) {
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
            }

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

                this._enforceFingerprintBound();

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

            // Body budget enforcement — bounds retained body bytes, not just observation count
            this._enforceBodyBudget();
        }

        addDiscovery(discovery) {
            // Runtime bound: cap discoveries in memory (P1 hardening) with resource cleanup
            const maxD = this._maxDiscoveries();
            if (this.discoveries.size >= maxD) {
                const first = this.discoveries.keys().next().value;
                if (first) {
                    this.discoveries.delete(first);
                    this._removeDiscoveryReferences(first);
                    this.recordDiagnostic('discovery-evicted', { max: maxD, evictedId: first });
                }
            }
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

                    if (resource) {
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
                // Runtime bound: cap resources in memory with fingerprint cleanup
                const maxR = this._maxResources();
                if (this.resources.size >= maxR) {
                    const first = this.resources.keys().next().value;
                    if (first) {
                        const evicted = this.resources.get(first);
                        this.resources.delete(first);
                        if (evicted) this._removeResourceFingerprint(first, evicted.fingerprint);
                        // also clean up graph edges referencing this resource? resources are URL-keyed, edges are candidate IDs — no direct link
                        this.recordDiagnostic('resource-evicted', { max: maxR, evictedUrl: String(first).slice(0,80) });
                    }
                }
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

            const maxEdges = this._retention('graphEdges.maxEntries', CONFIG.maxGraphEdges ?? 5000);
            if (
                this.graphEdges.length >= maxEdges
            ) {
                // FIFO shift oldest edge to keep bounded and referentially coherent
                this.graphEdges.shift();
                this.recordDiagnostic('graphEdge-evicted', { max: maxEdges });
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

            const maxDiag = this._retention('diagnostics.maxEntries', CONFIG.maxDiagnostics ?? 500);
            if (
                this.diagnostics.length > maxDiag
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
                this._enforcePatternBound();
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
                ].slice(-CONFIG.retention?.visited?.maxEntries ?? 2000),

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

            // --- Bounded restoration: enforce runtime retention after loading persisted state ---
            // Otherwise persisted 5000 resources could bypass runtime cap of 2000.

            // Trim candidates history (keep live + most recent historical)
            this._enforceCandidateHistoryBound();
            // Need second pass for candidateKeys if still over due to stale entries
            this._enforceCandidateKeysBound();
            this._enforceVisitedBound();

            // Observations: keep most recent maxObs, also enforce body budget
            const maxObs = this._maxObservations();
            while (this.observations.size > maxObs) {
                const first = this.observations.keys().next().value;
                if (first == null) break;
                const ev = this.observations.get(first);
                this.observations.delete(first);
                if (ev) this._removeObservationReferences(ev.id);
                this.recordDiagnostic('observation-evicted-on-restore', { max: maxObs });
            }
            this._enforceBodyBudget();

            // Discoveries
            const maxD = this._maxDiscoveries();
            while (this.discoveries.size > maxD) {
                const first = this.discoveries.keys().next().value;
                if (first == null) break;
                this.discoveries.delete(first);
                this._removeDiscoveryReferences(first);
                this.recordDiagnostic('discovery-evicted-on-restore', { max: maxD });
            }

            // Resources
            const maxR = this._maxResources();
            while (this.resources.size > maxR) {
                const first = this.resources.keys().next().value;
                if (first == null) break;
                const ev = this.resources.get(first);
                this.resources.delete(first);
                if (ev) this._removeResourceFingerprint(first, ev.fingerprint);
                this.recordDiagnostic('resource-evicted-on-restore', { max: maxR });
            }

            // Fingerprint / pattern / cluster / edges / diagnostics already bounded via helpers
            this._enforceFingerprintBound();
            this._enforcePatternBound();
            this._enforceGraphEdgesBound();
            // Diagnostics trimmed via retention max
            const maxDiag = this._retention('diagnostics.maxEntries', CONFIG.maxDiagnostics ?? 500);
            while (this.diagnostics.length > maxDiag) this.diagnostics.shift();
        }
    }

    /*
     * ============================================================
     * ACQUISITION POLICY
     * ============================================================
     */

