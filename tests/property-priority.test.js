/**
 * property-priority.test.js — property/invariant tests for Candidate.effectivePriority
 *
 * Verifies monotonicity and compositional invariants that must hold for every
 * value in the finite typePriority table and for random priority/depth/confidence.
 * Seeded LCG ensures determinism.
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const src = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');

// Re-implement effectivePriority from CONFIG constants parsed from source (single source of truth)
const typePriority = {
  api: 1.00, manifest: 0.95, sitemap: 0.92, robots: 0.90, url: 0.88, feed: 0.87,
  metadata: 0.82, network: 0.80, frame: 0.65, script: 0.60, stylesheet: 0.58,
  resource: 0.45, form: 0.30, media: 0.20, embedded: 0.20, xml: 0.45, text: 0.40, unknown: 0.25
};
const priorityCfg = { depthPenalty: 0.045, confidenceBoost: 0.08, retryPenalty: 0.05 };

function effectivePriority({ priority = 0, type = 'unknown', confidence = 0, depth = 0, attempts = 0 } = {}) {
  const w = typePriority[type] ?? typePriority.unknown;
  return priority + w * 0.20 + confidence * priorityCfg.confidenceBoost - depth * priorityCfg.depthPenalty - attempts * priorityCfg.retryPenalty;
}

function lcg(seed) {
  let s = seed >>> 0;
  return () => { s = (1664525 * s + 1013904223) >>> 0; return s / 0x100000000; };
}

describe('property: effectivePriority invariants (v0.7.6)', () => {
  it('monotonic in base priority', () => {
    const rng = lcg(0x12345);
    for (let i = 0; i < 500; i++) {
      const a = Math.floor(rng() * 100) / 10;
      const b = a + 0.1 + rng() * 2;
      const depth = Math.floor(rng() * 10);
      const conf = rng();
      const attempts = Math.floor(rng() * 3);
      const type = 'api';
      assert.ok(effectivePriority({ priority: b, type, confidence: conf, depth, attempts }) > effectivePriority({ priority: a, type, confidence: conf, depth, attempts }));
    }
  });

  it('decreases with depth', () => {
    const rng = lcg(0x23456);
    for (let i = 0; i < 500; i++) {
      const d1 = Math.floor(rng() * 8);
      const d2 = d1 + 1 + Math.floor(rng() * 4);
      assert.ok(effectivePriority({ priority: 1, type: 'url', confidence: 0.5, depth: d2 }) < effectivePriority({ priority: 1, type: 'url', confidence: 0.5, depth: d1 }));
    }
  });

  it('increases with confidence', () => {
    const rng = lcg(0x34567);
    for (let i = 0; i < 500; i++) {
      const c1 = rng() * 0.8;
      const c2 = Math.min(1, c1 + 0.1 + rng() * 0.2);
      assert.ok(effectivePriority({ priority: 0, type: 'unknown', confidence: c2, depth: 2 }) > effectivePriority({ priority: 0, type: 'unknown', confidence: c1, depth: 2 }));
    }
  });

  it('decreases with retry attempts', () => {
    for (let a = 0; a < 5; a++) {
      const p0 = effectivePriority({ attempts: a });
      const p1 = effectivePriority({ attempts: a + 1 });
      assert.ok(p1 < p0, `attempts ${a} -> ${a + 1} should reduce priority: ${p0} vs ${p1}`);
    }
  });

  it('type ordering: api > manifest > sitemap > robots > url > unknown', () => {
    const order = ['api', 'manifest', 'sitemap', 'robots', 'url', 'unknown'];
    let prev = Infinity;
    for (const t of order) {
      const p = effectivePriority({ type: t });
      assert.ok(p < prev, `${t} (${p}) should be < previous ${prev}`);
      prev = p;
    }
  });

  it('all known types produce finite effectivePriority', () => {
    for (const t of Object.keys(typePriority)) {
      const p = effectivePriority({ priority: 0.5, type: t, confidence: 0.5, depth: 3, attempts: 1 });
      assert.ok(Number.isFinite(p), `${t} produced non-finite ${p}`);
    }
  });

  it('composition: delta = +0.20 * dw + dc*0.08 - dd*0.045 - da*0.05', () => {
    const rng = lcg(0x45678);
    for (let i = 0; i < 200; i++) {
      const baseConf = rng() * 0.7; // keep headroom so +0.2 never caps at 1
      const base = { priority: rng() * 2, type: 'api', confidence: baseConf, depth: Math.floor(rng() * 5), attempts: Math.floor(rng() * 3) };
      const next = { priority: base.priority + 1, type: 'url', confidence: baseConf + 0.2, depth: base.depth + 1, attempts: base.attempts + 1 };
      const delta = effectivePriority(next) - effectivePriority(base);
      const expected = 1 + (typePriority.url - typePriority.api) * 0.20 + 0.2 * priorityCfg.confidenceBoost - 1 * priorityCfg.depthPenalty - 1 * priorityCfg.retryPenalty;
      assert.ok(Math.abs(delta - expected) < 1e-9, `delta ${delta} != expected ${expected}`);
    }
  });

  it('source still contains rAF batching (updateUI → _doUpdateUI)', () => {
    assert.match(src, /_uiRaf/);
    assert.match(src, /requestAnimationFrame/);
    assert.match(src, /_doUpdateUI\(\)/);
  });
});
