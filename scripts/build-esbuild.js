#!/usr/bin/env node
// scripts/build-esbuild.js — esbuild minify for v1.1.0 (lazy providers)
// Reads dist/generic-discovery-engine.user.js (deterministic concat) and produces
// dist/generic-discovery-engine.min.js via esbuild transform (minify, no banner drift).
// Falls back to no-op if esbuild not installed. Records minified stats into .build-meta.json
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const root = path.join(import.meta.dirname, '..');
const srcDist = path.join(root, 'dist/generic-discovery-engine.user.js');
const minDist = path.join(root, 'dist/generic-discovery-engine.min.js');
const metaPath = path.join(root, 'dist/.build-meta.json');

if (!fs.existsSync(srcDist)) {
  console.error('build:esbuild: src dist missing — run npm run build first');
  process.exit(1);
}

let esbuild;
try {
  esbuild = await import('esbuild');
} catch {
  console.warn('build:esbuild: esbuild not installed — skipping minify (run: npm i -D esbuild)');
  process.exit(0);
}

const input = fs.readFileSync(srcDist, 'utf8');
// Extract header block (==UserScript==) to preserve verbatim; esbuild would strip comments if minified whole file.
// We keep header as-is and minify only the body between "(function () {" and "})();\n"
const headerEnd = input.indexOf("(function () {");
if (headerEnd === -1) {
  console.error('build:esbuild: could not find IIFE start');
  process.exit(1);
}
const header = input.slice(0, headerEnd);
const body = input.slice(headerEnd);

let result;
try {
  result = await esbuild.transform(body, {
    minify: true,
    target: 'es2022',
    keepNames: true,
    legalComments: 'none',
    charset: 'utf8'
  });
} catch (e) {
  console.error('build:esbuild: transform failed', e);
  process.exit(1);
}

const minified = header + result.code;
fs.writeFileSync(minDist, minified, 'utf8');

const hash = crypto.createHash('sha256').update(minified, 'utf8').digest('hex');
const lines = (minified.match(/\n/g) || []).length;
const size = Buffer.byteLength(minified, 'utf8');
const srcSize = Buffer.byteLength(input, 'utf8');
const ratio = ((size / srcSize) * 100).toFixed(1);

// Update meta with minified stats (non-breaking additive)
let meta = {};
if (fs.existsSync(metaPath)) {
  try { meta = JSON.parse(fs.readFileSync(metaPath, 'utf8')); } catch {}
}
meta.minified = { file: 'dist/generic-discovery-engine.min.js', sha256: hash, lines, size, ratio: Number(ratio) };
fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2) + '\n');

console.log(`build:esbuild: minified ${size} bytes (${ratio}% of ${srcSize}) sha256 ${hash.slice(0,12)}... → ${path.relative(process.cwd(), minDist)}`);
