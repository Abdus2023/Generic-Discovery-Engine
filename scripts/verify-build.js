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
for (const rx of [/builtAt/, /__RANDOM__/]) {
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
console.log('verify-build: OK — deterministic');
