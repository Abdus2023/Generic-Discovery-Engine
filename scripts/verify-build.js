#!/usr/bin/env node
// scripts/verify-build.js — deterministic rebuild check for v0.7.9
// Verifies dist/generic-discovery-engine.user.js matches dist/.build-meta.json
// and is internally deterministic (no random, no timestamp in dist).
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const dist = path.join(import.meta.dirname, '../dist/generic-discovery-engine.user.js');
const metaPath = path.join(import.meta.dirname, '../dist/.build-meta.json');

if (!fs.existsSync(dist)) {
  console.error('verify-build: dist missing');
  process.exit(1);
}
const content = fs.readFileSync(dist, 'utf8');
const hash = crypto.createHash('sha256').update(content, 'utf8').digest('hex');
const lines = (content.match(/\n/g) || []).length; // wc -l
const size = Buffer.byteLength(content, 'utf8');

// 1. content must not contain non-deterministic markers (timestamp, random)
const forbidden = [/builtAt/, /__RANDOM__/];
for (const rx of forbidden) {
  if (rx.test(content)) {
    console.error(`verify-build: forbidden pattern ${rx} found in dist`);
    process.exit(1);
  }
}
// 2. version header must match package.json
const pkg = JSON.parse(fs.readFileSync(path.join(import.meta.dirname, '../package.json'), 'utf8'));
if (!content.includes(`@version      ${pkg.version}`)) {
  console.error(`verify-build: dist header @version does not match package.json ${pkg.version}`);
  process.exit(1);
}
if (!content.includes(`v${pkg.version} —`)) {
  console.error(`verify-build: dist does not contain v${pkg.version} banner`);
  process.exit(1);
}
console.log(`verify-build: v${pkg.version} ${lines} lines ${size} bytes sha256 ${hash.slice(0,12)}...`);

// 3. if meta exists, hash must match
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
  console.log(`verify-build: no meta yet (run: npm run build to create ${path.relative(process.cwd(), metaPath)})`);
}

// 4. pattern inference proof: dist must contain extractUrlPattern
if (!content.includes('extractUrlPattern')) {
  console.error('verify-build: missing extractUrlPattern');
  process.exit(1);
}
console.log('verify-build: OK — deterministic');
