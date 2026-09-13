#!/usr/bin/env node
// scripts/verify-build.js — deterministic rebuild check for v0.8.1
// Verifies dist header, src mirror, and hash vs meta
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const dist = path.join(import.meta.dirname, '../dist/generic-discovery-engine.user.js');
const metaPath = path.join(import.meta.dirname, '../dist/.build-meta.json');
const pkgPath = path.join(import.meta.dirname, '../package.json');
const srcDir = path.join(import.meta.dirname, '../src');

if (!fs.existsSync(dist)) {
  console.error('verify-build: dist missing');
  process.exit(1);
}
const content = fs.readFileSync(dist, 'utf8');
const hash = crypto.createHash('sha256').update(content, 'utf8').digest('hex');
const lines = (content.match(/\n/g) || []).length;
const size = Buffer.byteLength(content, 'utf8');
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));

if (!content.includes(`@version      ${pkg.version}`)) {
  console.error(`verify-build: dist header @version does not match package.json ${pkg.version}`);
  process.exit(1);
}
if (!content.includes(`v${pkg.version} —`)) {
  console.error(`verify-build: dist does not contain v${pkg.version} banner`);
  process.exit(1);
}
for (const rx of [/"builtAt"/, /__RANDOM__/]) {
  if (rx.test(content)) {
    console.error(`verify-build: forbidden pattern ${rx} in dist`);
    process.exit(1);
  }
}
console.log(`verify-build: v${pkg.version} ${lines} lines ${size} bytes sha256 ${hash.slice(0,12)}...`);

// src mirror check
const requiredSrc = ['config.js', 'utils.js', 'models.js', 'knowledge.js', 'ledger.js', 'providers.js', 'engine.js'];
for (const f of requiredSrc) {
  const p = path.join(srcDir, f);
  if (!fs.existsSync(p)) {
    console.error(`verify-build: src missing: src/${f}`);
    process.exit(1);
  }
}
console.log(`verify-build: src mirror ${requiredSrc.length} files OK`);

// meta check
if (fs.existsSync(metaPath)) {
  const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
  if (meta.sha256 !== hash) {
    console.error(`verify-build: hash mismatch! meta ${meta.sha256.slice(0,12)} != current ${hash.slice(0,12)}`);
    console.error(`  meta lines ${meta.lines} vs current ${lines}, run: npm run build`);
    process.exit(1);
  }
  if (meta.version !== pkg.version) {
    console.error(`verify-build: meta version ${meta.version} != pkg ${pkg.version}, run: npm run build`);
    process.exit(1);
  }
  console.log(`verify-build: meta matches ${path.relative(process.cwd(), metaPath)}`);
} else {
  console.log(`verify-build: no meta yet (run: npm run build)`);
}

if (!content.includes('extractUrlPattern')) {
  console.error('verify-build: missing extractUrlPattern');
  process.exit(1);
}
if (!content.includes('RobotsProvider')) {
  console.error('verify-build: missing RobotsProvider');
  process.exit(1);
}
if (!content.includes('patternCount')) {
  console.error('verify-build: missing patternCount in getCoverageMetrics (export hardening)');
  process.exit(1);
}
if (!content.includes('inferenceEnabled')) {
  console.error('verify-build: missing inferenceEnabled in getCoverageMetrics');
  process.exit(1);
}
if (!content.includes('fingerprintUnique')) {
  console.error('verify-build: missing fingerprintUnique');
  process.exit(1);
}
// exportData must include inference block (hardening)
if (!content.includes('inference,') && !content.includes('inference:') ) {
  console.error('verify-build: missing inference in exportData');
  process.exit(1);
}
if (!content.includes('patternMetrics')) {
  console.error('verify-build: missing patternMetrics in exportData.inference');
  process.exit(1);
}
if (!content.includes('clusterMetrics')) {
  console.error('verify-build: missing clusterMetrics');
  process.exit(1);
}
if (!content.includes('revisitChanged')) {
  console.error('verify-build: missing revisitChanged (v0.9.1)');
  process.exit(1);
}
if (!content.includes('patternGuided')) {
  console.error('verify-build: missing patternGuided');
  process.exit(1);
}
if (!content.includes('suggestPatternCandidates')) {
  console.error('verify-build: missing suggestPatternCandidates');
  process.exit(1);
}
if (!content.includes('getChangedResources')) {
  console.error('verify-build: missing getChangedResources');
  process.exit(1);
}
if (!content.includes('CONFIG.providers')) {
  console.error('verify-build: missing CONFIG.providers (v1.1 lazy)');
  process.exit(1);
}
if (!content.includes('lazy')) {
  console.error('verify-build: missing lazy in providers');
  process.exit(1);
}
if (!content.includes('getProviderMetrics')) {
  console.error('verify-build: missing getProviderMetrics');
  process.exit(1);
}
if (!content.includes('providerInstances')) {
  console.error('verify-build: missing providerInstances in coverage');
  process.exit(1);
}
if (!content.includes('getInstanceCount')) {
  console.error('verify-build: missing getInstanceCount');
  process.exit(1);
}
if (!content.includes('SitemapIndexProvider')) {
  console.error('verify-build: missing SitemapIndexProvider (v1.2)');
  process.exit(1);
}
if (!content.includes('OpenApiProvider')) {
  console.error('verify-build: missing OpenApiProvider (v1.2)');
  process.exit(1);
}
if (!content.includes('sitemapIndex')) {
  console.error('verify-build: missing sitemapIndex in factories');
  process.exit(1);
}
if (!content.includes('openapi')) {
  console.error('verify-build: missing openapi in factories');
  process.exit(1);
}
if (!content.includes('WellKnownProvider')) {
  console.error('verify-build: missing WellKnownProvider (v1.3)');
  process.exit(1);
}
if (!content.includes('ManifestProvider')) {
  console.error('verify-build: missing ManifestProvider (v1.3)');
  process.exit(1);
}
if (!content.includes('wellKnown')) {
  console.error('verify-build: missing wellKnown in factories');
  process.exit(1);
}
if (!content.includes('manifest')) {
  console.error('verify-build: missing manifest in factories');
  process.exit(1);
}
if (!content.includes('getHealthMetrics')) {
  console.error('verify-build: missing getHealthMetrics (v1.4)');
  process.exit(1);
}
if (!content.includes('concurrent')) {
  console.error('verify-build: missing concurrent in providers');
  process.exit(1);
}
if (!content.includes('CONFIG.health')) {
  console.error('verify-build: missing CONFIG.health');
  process.exit(1);
}
if (!content.includes('health,')) {
  console.error('verify-build: missing health in exportData');
  process.exit(1);
}
if (!content.includes("redirect: CONFIG.sameOriginOnly ? 'error'")) {
  console.error('verify-build: missing redirect error when sameOriginOnly (v1.5 security)');
  process.exit(1);
}
if (!content.includes('// // @connect')) {
  console.error('verify-build: missing least-privilege @connect (v1.5 wildcard commented)');
  process.exit(1);
}
if (content.includes('\n// @connect      *  — uncomment')) {
  console.error('verify-build: wildcard @connect still active (must be commented)');
  process.exit(1);
}
if (!content.includes('maxDiscoveriesInMemory')) {
  console.error('verify-build: missing maxDiscoveriesInMemory (v1.5 runtime bound)');
  process.exit(1);
}
if (!content.includes('maxResourcesInMemory')) {
  console.error('verify-build: missing maxResourcesInMemory (v1.5 runtime bound)');
  process.exit(1);
}
if (!content.includes('diagnosticCount')) {
  console.error('verify-build: missing diagnosticCount in health (v1.5 dead branch fix)');
  process.exit(1);
}
if (!content.includes('configuredProviders')) {
  console.error('verify-build: missing configuredProviders in health (v1.5 provider metrics)');
  process.exit(1);
}
if (!content.includes('adaptive-target')) {
  console.error('verify-build: missing adaptive-target diagnostic (v1.5 concurrency clarification)');
  process.exit(1);
}
if (!content.includes('concurrencyTarget')) {
  console.error('verify-build: missing concurrencyTarget getter (v1.5)');
  process.exit(1);
}
// Check minified artifact if present (optional, not fatal)
const minPath = path.join(path.dirname(dist), 'generic-discovery-engine.min.js');
if (fs.existsSync(minPath)) {
  const minContent = fs.readFileSync(minPath, 'utf8');
  if (!minContent.includes('@version')) {
    console.warn('verify-build: minified missing header');
  } else {
    const minHash = crypto.createHash('sha256').update(minContent, 'utf8').digest('hex');
    console.log(`verify-build: minified ${minContent.length} bytes sha ${minHash.slice(0,12)}...`);
  }
}
console.log('verify-build: OK — deterministic');
