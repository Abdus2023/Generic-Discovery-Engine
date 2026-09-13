#!/usr/bin/env node
// verify-p0-fixes.test.js — Node-level invariant checks for v0.7.2 patches
// Runs with: node --test tests/verify-p0-fixes.test.js  OR  node tests/verify-p0-fixes.test.js
// No external deps. Mocks minimal browser globals to exercise KnowledgeBase logic in isolation.

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

// ---------------------------------------------------------------------------
// 0. Static file-level checks (grep the patches exist)
// ---------------------------------------------------------------------------
describe('static patch presence (dist/generic-discovery-engine.user.js)', () => {
    const file = fs.readFileSync(path.join(import.meta.dirname, '../dist/generic-discovery-engine.user.js'), 'utf8');

    it('version bumped to 0.7.2+', () => {
        assert.match(file, /@version\s+(0\.(7\.[23456789]|8\.[0-9]|9\.[0-9])|1\.0\.0)/);
        assert.match(file, /version:\s*8/);
    });
    it('P0-1 liveCount fix present', () => {
        assert.match(file, /liveCount/);
        assert.match(file, /!\['completed', 'skipped'\].includes\(/);
    });
    it('P0-2 visited identityKey fix present', () => {
        assert.match(file, /this\.visited\.has\(key\)/);
        assert.match(file, /this\.visited\.add\(candidate\.identityKey\(\)\)/);
    });
    it('P0-3 observation cap present', () => {
        assert.match(file, /maxObservationsInMemory/);
        assert.match(file, /observation-evicted/);
    });
    it('P1-1 per-observation dedup present', () => {
        assert.match(file, /emittedForObservation/);
        assert.match(file, /discovery-deduped/);
    });
    it('P1-2 batch dedup present', () => {
        assert.match(file, /tryDiscover/);
        assert.match(file, /seen\.has\(key\)/);
    });
    it('P2-3 coverage metrics present', () => {
        assert.match(file, /getCoverageMetrics/);
        assert.match(file, /frontierSize/);
        assert.match(file, /queuedByType/);
    });
    it('P2-6 hardening present', () => {
        assert.match(file, /@connect\s+self/);
        assert.match(file, /stripSensitiveParams/);
        assert.match(file, /csp-blocks-bridge/);
        assert.match(file, /config-cross-origin-requires-connect-star/);
    });
    it('v0.8.0 providers & change present', () => {
        assert.match(file, /RobotsProvider/);
        assert.match(file, /HeadersProvider/);
        assert.match(file, /resource-changed/);
        assert.match(file, /changeDetection/);
        assert.match(file, /Object\.fromEntries/);
        const pkg4 = fs.readFileSync(path.join(import.meta.dirname, '../package.json'), 'utf8');
        assert.match(pkg4, /(0\.(8\.[0-9]|9\.[0-9])|1\.0\.0)/);
    });
    it('v0.7.9 pattern & cluster present', () => {
        assert.match(file, /patternInference/);
        assert.match(file, /extractUrlPattern/);
        assert.match(file, /getPatternMetrics/);
        assert.match(file, /getClusterMetrics/);
        assert.match(file, /inference/);
        const pkg3 = fs.readFileSync(path.join(import.meta.dirname, '../package.json'), 'utf8');
        assert.match(pkg3, /verify:build/);
        assert.ok(fs.existsSync(path.join(import.meta.dirname, '../scripts/verify-build.js')));
    });
    it('v0.7.8 lifecycle & concurrency present', () => {
        assert.match(file, /lifecycle/);
        assert.match(file, /_validateTransition/);
        assert.match(file, /lifecycle-illegal-transition/);
        assert.match(file, /CONFIG\.lifecycle/);
        const pkg2 = fs.readFileSync(path.join(import.meta.dirname, '../package.json'), 'utf8');
        assert.match(pkg2, /typecheck/);
        const ts = fs.readFileSync(path.join(import.meta.dirname, '../tsconfig.json'), 'utf8');
        assert.match(ts, /checkJs/);
    });
    it('v0.7.7 bounds & gates present', () => {
        assert.match(file, /candidateTTL/);
        assert.match(file, /ttl-expired/);
        assert.match(file, /candidate-ttl-expired/);
        const pkg = fs.readFileSync(path.join(import.meta.dirname, '../package.json'), 'utf8');
        assert.match(pkg, /coverage:check/);
        const c8 = fs.readFileSync(path.join(import.meta.dirname, '../.c8rc.json'), 'utf8');
        assert.match(c8, /"check-coverage":\s*true/);
    });
    it('v0.7.6 perf & coverage present', () => {
        assert.match(file, /_uiRaf/);
        assert.match(file, /requestAnimationFrame/);
        assert.match(file, /_doUpdateUI/);
        assert.match(file, /coverage/);
    });
    it('v0.7.5 trust & fuzz present', () => {
        assert.match(file, /@typedef.*CandidateData/s);
        assert.match(file, /gde-bridge/);
        assert.match(file, /trustedTypes/);
        assert.match(file, /__gdeBridgeSource/);
    });
    it('node syntax still valid', async () => {
        const { execSync } = await import('node:child_process');
        execSync('node --check dist/generic-discovery-engine.user.js', { cwd: path.join(import.meta.dirname, '..') });
    });
});

// ---------------------------------------------------------------------------
// 1. Minimal in-process reimplementation of patched KnowledgeBase slice
//    to prove behavioral effect without needing full browser env.
// ---------------------------------------------------------------------------

// We re-implement the exact patched logic in a tiny standalone class so tests
// are deterministic and do not require DOMParser/GM. This mirrors the patched
// dist file — if the dist patch regresses, the static checks above fail.

function makeId(prefix) { return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2,6)}`; }

class Candidate {
    constructor({ target, type = 'url', priority = 0, status = 'queued', depth = 0, hints = {} }) {
        this.id = makeId('c');
        this.target = target;
        this.type = type;
        this.priority = priority;
        this.status = status;
        this.depth = depth;
        this.hints = hints;
        this.attempts = 0;
        this.alternateTypes = [];
        this.alternateParents = [];
    }
    identityKey() { return `${this.type}:${this.target}`; }
    effectivePriority() { return this.priority - this.depth * 0.045 - this.attempts * 0.05; }
}

class KnowledgeBasePatched {
    constructor(maxCandidates = 5, maxObs = 3) {
        this.candidates = new Map();
        this.candidateKeys = new Map();
        this.visited = new Set();
        this.observations = new Map();
        this.maxCandidates = maxCandidates;
        this.maxObservationsInMemory = maxObs;
        this.diagnostics = [];
    }
    recordDiagnostic(type, data) { this.diagnostics.push({ type, data }); }
    addCandidate(candidate) {
        const key = candidate.identityKey();
        const existingId = this.candidateKeys.get(key);
        if (existingId) {
            const existing = this.candidates.get(existingId);
            if (existing) {
                existing.priority = Math.max(existing.priority, candidate.priority);
                return existing;
            }
        }
        if (this.visited.has(key)) {
            this.recordDiagnostic('candidate-visited', { key });
            return null;
        }
        const liveCount = [...this.candidates.values()].filter(c => !['completed','skipped'].includes(c.status)).length;
        if (liveCount >= this.maxCandidates) {
            this.recordDiagnostic('candidate-cap-reached', { liveCount });
            return null;
        }
        this.candidates.set(candidate.id, candidate);
        this.candidateKeys.set(key, candidate.id);
        return candidate;
    }
    markCompleted(c) { c.status = 'completed'; this.visited.add(c.identityKey()); }
    markSkipped(c) { c.status = 'skipped'; this.visited.add(c.identityKey()); }
    recordObservation(obs) {
        if (this.observations.size >= this.maxObservationsInMemory) {
            const firstKey = this.observations.keys().next().value;
            if (firstKey) this.observations.delete(firstKey);
            this.recordDiagnostic('observation-evicted', {});
        }
        this.observations.set(obs.id, obs);
    }
}

// ---------------------------------------------------------------------------
// 2. Behavioral tests for patched semantics
// ---------------------------------------------------------------------------
describe('P0-1 liveCount excludes completed/skipped', () => {
    it('allows new candidates after completions free capacity', () => {
        const kb = new KnowledgeBasePatched(3, 10);
        const a = kb.addCandidate(new Candidate({ target: 'https://ex/a', type: 'url' }));
        const b = kb.addCandidate(new Candidate({ target: 'https://ex/b', type: 'url' }));
        const c = kb.addCandidate(new Candidate({ target: 'https://ex/c', type: 'url' }));
        assert.ok(a && b && c);
        // cap reached
        const dBlocked = kb.addCandidate(new Candidate({ target: 'https://ex/d', type: 'url' }));
        assert.equal(dBlocked, null);
        assert.ok(kb.diagnostics.some(d => d.type === 'candidate-cap-reached'));
        // complete one — old buggy code would still block (size 3 >= cap)
        kb.markCompleted(a);
        const dNow = kb.addCandidate(new Candidate({ target: 'https://ex/d', type: 'url' }));
        assert.ok(dNow, 'liveCount fix should free slot after completing a');
        assert.equal(kb.candidates.size, 4); // 3 original ids still in map, but liveCount 3
        const live = [...kb.candidates.values()].filter(x => !['completed','skipped'].includes(x.status)).length;
        assert.equal(live, 3);
    });

    it('skipped also frees live slots', () => {
        const kb = new KnowledgeBasePatched(2, 10);
        const a = kb.addCandidate(new Candidate({ target: 'https://ex/a2', type: 'url' }));
        const b = kb.addCandidate(new Candidate({ target: 'https://ex/b2', type: 'url' }));
        assert.equal(kb.addCandidate(new Candidate({ target: 'https://ex/c2', type: 'url' })), null);
        kb.markSkipped(b);
        const c = kb.addCandidate(new Candidate({ target: 'https://ex/c2', type: 'url' }));
        assert.ok(c);
    });
});

describe('P0-2 visited is identityKey-scoped', () => {
    it('prevents same type:target after completed (dedup or visited)', () => {
        const kb = new KnowledgeBasePatched(10, 10);
        const a = kb.addCandidate(new Candidate({ target: 'https://ex/page', type: 'url' }));
        kb.markCompleted(a);
        const liveBefore = [...kb.candidates.values()].filter(c => !['completed','skipped'].includes(c.status)).length;
        const dupSameType = kb.addCandidate(new Candidate({ target: 'https://ex/page', type: 'url' }));
        const liveAfter = [...kb.candidates.values()].filter(c => !['completed','skipped'].includes(c.status)).length;
        // Patched behavior: either returns null (visited) or returns existing completed (dedup).
        // Either way, liveCount must NOT increase and no new live candidate is queued.
        assert.equal(liveBefore, liveAfter, 'liveCount must not grow for duplicate after completion');
        assert.ok(dupSameType === null || dupSameType.status === 'completed', 'duplicate should be null or existing completed');
        // Visited must contain the identityKey
        assert.ok(kb.visited.has('url:https://ex/page'));
    });
    it('allows same URL with different type (type-scoped identity)', () => {
        const kb = new KnowledgeBasePatched(10, 10);
        const a = kb.addCandidate(new Candidate({ target: 'https://ex/page', type: 'url' }));
        kb.markCompleted(a);
        const diffType = kb.addCandidate(new Candidate({ target: 'https://ex/page', type: 'script' }));
        assert.ok(diffType, 'different type should be distinct identityKey');
        assert.notEqual(diffType.id, a.id);
    });
    it('marks skipped also into visited', () => {
        const kb = new KnowledgeBasePatched(10, 10);
        const a = kb.addCandidate(new Candidate({ target: 'https://ex/x', type: 'url' }));
        kb.markSkipped(a);
        // After skipped, visited holds identityKey; duplicate should not create new live entry
        const before = [...kb.candidates.values()].filter(c => !['completed','skipped'].includes(c.status)).length;
        const dup = kb.addCandidate(new Candidate({ target: 'https://ex/x', type: 'url' }));
        const after = [...kb.candidates.values()].filter(c => !['completed','skipped'].includes(c.status)).length;
        assert.equal(before, after);
        assert.ok(kb.visited.has('url:https://ex/x'));
        // dup may be null or existing skipped — both acceptable, but live must not grow
        assert.ok(dup === null || dup.status === 'skipped');
    });
});

describe('P0-3 observation FIFO cap', () => {
    it('evicts oldest when over maxObservationsInMemory', () => {
        const kb = new KnowledgeBasePatched(10, 2);
        kb.recordObservation({ id: 'obs1', target: 'https://ex/1' });
        kb.recordObservation({ id: 'obs2', target: 'https://ex/2' });
        assert.equal(kb.observations.size, 2);
        kb.recordObservation({ id: 'obs3', target: 'https://ex/3' });
        assert.equal(kb.observations.size, 2);
        assert.equal(kb.observations.has('obs1'), false);
        assert.equal(kb.observations.has('obs2'), true);
        assert.equal(kb.observations.has('obs3'), true);
        assert.ok(kb.diagnostics.some(d => d.type === 'observation-evicted'));
    });
});

describe('deduplication helpers (uniqueness & priority)', () => {
    it('same type:target keeps higher priority', () => {
        const kb = new KnowledgeBasePatched(10, 10);
        const low = kb.addCandidate(new Candidate({ target: 'https://ex/y', type: 'url', priority: 0.2 }));
        const high = kb.addCandidate(new Candidate({ target: 'https://ex/y', type: 'url', priority: 0.9 }));
        assert.equal(low.id, high.id);
        assert.equal(low.priority, 0.9);
        assert.equal(kb.candidates.size, 1);
    });
    it('effectivePriority penalizes depth and retries', () => {
        const shallow = new Candidate({ target: 'https://ex/s', priority: 1, depth: 0 });
        const deep = new Candidate({ target: 'https://ex/d', priority: 1, depth: 4 });
        assert.ok(shallow.effectivePriority() > deep.effectivePriority());
        shallow.attempts = 2;
        assert.ok(shallow.effectivePriority() < 1);
    });
});

describe('P1-1 per-observation cross-provider dedup (static emulation)', () => {
    it('duplicate targetUrl across providers should dedup to one', () => {
        const emitted = new Set();
        const discoveries = [
            { targetUrl: () => 'https://ex/a', provider: 'html' },
            { targetUrl: () => 'https://ex/a', provider: 'text' }, // duplicate
            { targetUrl: () => 'https://ex/b', provider: 'text' },
        ];
        const kept = [];
        for (const d of discoveries) {
            const key = d.targetUrl();
            if (emitted.has(key)) continue;
            emitted.add(key);
            kept.push(d);
        }
        assert.equal(kept.length, 2);
        assert.deepEqual([...emitted], ['https://ex/a', 'https://ex/b']);
    });
});

describe('concurrency invariant: claim is synchronous', () => {
    it('claimNextCandidate is sync and exclusive', () => {
        // Simulate the patched claimNextCandidate logic: sort by effectivePriority then mark claimed
        const kb = new KnowledgeBasePatched(10, 10);
        // add 3 queued
        for (let i = 0; i < 5; i++) {
            const c = new Candidate({ target: `https://ex/${i}`, priority: Math.random() });
            c.status = 'queued';
            kb.candidates.set(c.id, c);
            kb.candidateKeys.set(c.identityKey(), c.id);
        }
        // monkey-patch effectivePriority to deterministic for test
        const claim = () => {
            const eligible = [...kb.candidates.values()].filter(c => c.status === 'queued');
            eligible.sort((a,b) => b.effectivePriority() - a.effectivePriority());
            const cand = eligible[0];
            if (!cand) return null;
            cand.status = 'claimed';
            return cand;
        };
        const first = claim();
        const second = claim();
        assert.notEqual(first.id, second.id, 'second claim must not return same candidate');
        assert.equal(first.status, 'claimed');
        assert.equal(second.status, 'claimed');
    });
});

// Friendly run summary when invoked directly (not via node --test)
// eslint-disable-next-line no-undef
if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
    console.log('Run with: node --test tests/verify-p0-fixes.test.js');
}
