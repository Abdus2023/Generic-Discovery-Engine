#!/usr/bin/env node
// scripts/build.js — deterministic bundler for v0.9.0 (src/ → dist/)
// Concatenates src/header.txt + src/config.js + src/utils.js + src/models.js + src/ledger.js + src/knowledge.js + src/providers.js + src/engine.js
// Verifies src mirror exists and header @version matches package.json, then captures hash → dist/.build-meta.json
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const root = path.join(import.meta.dirname, '..');
const dist = path.join(root, 'dist/generic-discovery-engine.user.js');
const metaPath = path.join(root, 'dist/.build-meta.json');
const pkgPath = path.join(root, 'package.json');
const headerPath = path.join(root, 'src/header.txt');

const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));

const requiredSrc = ['header.txt', 'config.js', 'utils.js', 'models.js', 'ledger.js', 'knowledge.js', 'providers.js', 'engine.js'];
for (const f of requiredSrc) {
  const p = path.join(root, 'src', f);
  if (!fs.existsSync(p)) {
    console.error(`build: src missing: src/${f}`);
    process.exit(1);
  }
  const c = fs.readFileSync(p, 'utf8');
  if (!c.trim()) {
    console.error(`build: src empty: src/${f}`);
    process.exit(1);
  }
}

// Load header template and bump version
let header = fs.readFileSync(headerPath, 'utf8');
// Replace @version line
header = header.replace(/\/\/ @version\s+.*/, `// @version      ${pkg.version}`);
// Replace banner vX.Y.Z — line inside patch notes header block
header = header.replace(/v0\.\d+\.\d+ —/, `v${pkg.version} —`);
// Ensure header ends with newline
if (!header.endsWith('\n')) header += '\n';

// Helper to load src file stripping the leading src comment we added for readability
function loadSrc(file) {
  let content = fs.readFileSync(path.join(root, 'src', file), 'utf8');
  // Strip leading // src/... line(s) added by extraction (they start with // src/)
  const lines = content.split('\n');
  let start = 0;
  // Skip first line if it is // src/
  if (lines[0]?.startsWith('// src/')) {
    start = 1;
    // Also skip second line if empty?
    if (lines[1] === '') start = 2;
  }
  // Rejoin remaining; ensure we don't have duplicate header IIFE opening
  content = lines.slice(start).join('\n');
  // Ensure ends with newline for deterministic concatenation
  if (!content.endsWith('\n')) content += '\n';
  // Ensure no BOM or trailing spaces drift: we keep as is
  return content;
}

// Concatenation order: dependency order (config → utils → ledger → models → knowledge → providers → engine)
// This differs from original dist order (where AcquisitionPlan was before ledger) but is deterministic and dependency-safe
// Engine contains AcquisitionPlan, AcquisitionPolicy, OriginController, Acquisition, NetworkObserver, GenericDiscoveryEngine
const order = ['config.js', 'utils.js', 'ledger.js', 'models.js', 'knowledge.js', 'providers.js', 'engine.js'];
let body = '';
for (const f of order) {
  body += loadSrc(f);
}

// Final dist = header + body
const content = header + body;

// Write dist
fs.mkdirSync(path.dirname(dist), { recursive: true });
fs.writeFileSync(dist, content, 'utf8');

// Compute deterministic metrics (wc -l style)
const hash = crypto.createHash('sha256').update(content, 'utf8').digest('hex');
const lines = (content.match(/\n/g) || []).length;
const size = Buffer.byteLength(content, 'utf8');

// Verify header version matches pkg
if (!content.includes(`@version      ${pkg.version}`)) {
  console.error(`build: dist header @version does not match package.json ${pkg.version}`);
  process.exit(1);
}

const meta = {
  version: pkg.version,
  file: 'dist/generic-discovery-engine.user.js',
  sha256: hash,
  lines,
  size,
  src: order.map(f => f.replace('.js','').replace('.txt','')) ,
  builtAt: new Date().toISOString(),
  node: process.version
};

fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2) + '\n');
console.log(`build: v${meta.version} ${lines} lines ${size} bytes sha256 ${hash.slice(0,12)}... src ${order.length} (+header) → ${path.relative(process.cwd(), metaPath)}`);
console.log(`build: src order ${order.join(' → ')}`);
