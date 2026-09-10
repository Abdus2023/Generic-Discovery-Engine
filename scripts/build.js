#!/usr/bin/env node
// scripts/build.js — deterministic build stub for v0.7.9
// For now src is dist itself (single-file userscript). This script captures
// the deterministic hash + line count so verify-build can prove no manual drift.
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const dist = path.join(import.meta.dirname, '../dist/generic-discovery-engine.user.js');
const metaPath = path.join(import.meta.dirname, '../dist/.build-meta.json');

if (!fs.existsSync(dist)) {
  console.error('dist missing:', dist);
  process.exit(1);
}
const content = fs.readFileSync(dist, 'utf8');
const hash = crypto.createHash('sha256').update(content, 'utf8').digest('hex');
const lines = (content.match(/\n/g) || []).length; // wc -l
const size = Buffer.byteLength(content, 'utf8');
const pkg = JSON.parse(fs.readFileSync(path.join(import.meta.dirname, '../package.json'), 'utf8'));

const meta = {
  version: pkg.version,
  file: 'dist/generic-discovery-engine.user.js',
  sha256: hash,
  lines,
  size,
  builtAt: new Date().toISOString(),
  node: process.version
};

fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2) + '\n');
console.log(`build: v${meta.version} ${lines} lines ${size} bytes sha256 ${hash.slice(0,12)}... → ${path.relative(process.cwd(), metaPath)}`);
