#!/usr/bin/env node
// scripts/build.js — deterministic build for v0.8.1 modular prelude
// For v0.8.1 src/ is a mirror of dist logical sections; this script verifies
// that src files exist and that dist header @version matches package.json,
// then captures deterministic hash + line count to dist/.build-meta.json
import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';

const dist = path.join(import.meta.dirname, '../dist/generic-discovery-engine.user.js');
const metaPath = path.join(import.meta.dirname, '../dist/.build-meta.json');
const pkgPath = path.join(import.meta.dirname, '../package.json');
const srcDir = path.join(import.meta.dirname, '../src');

if (!fs.existsSync(dist)) {
  console.error('build: dist missing:', dist);
  process.exit(1);
}
const content = fs.readFileSync(dist, 'utf8');
const hash = crypto.createHash('sha256').update(content, 'utf8').digest('hex');
const lines = (content.match(/\n/g) || []).length;
const size = Buffer.byteLength(content, 'utf8');
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));

// Verify src mirror exists (v0.8.1 modular prelude)
const requiredSrc = ['config.js', 'utils.js', 'models.js', 'knowledge.js', 'ledger.js', 'providers.js', 'engine.js'];
let srcOk = true;
for (const f of requiredSrc) {
  const p = path.join(srcDir, f);
  if (!fs.existsSync(p)) {
    console.error(`build: src missing: src/${f}`);
    srcOk = false;
  } else {
    const c = fs.readFileSync(p, 'utf8');
    if (!c.trim()) {
      console.error(`build: src empty: src/${f}`);
      srcOk = false;
    }
  }
}
if (!srcOk) {
  console.error('build: src mirror incomplete — see src/README.md');
  process.exit(1);
}
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
  src: requiredSrc,
  builtAt: new Date().toISOString(),
  node: process.version
};

fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2) + '\n');
console.log(`build: v${meta.version} ${lines} lines ${size} bytes sha256 ${hash.slice(0,12)}... src ${requiredSrc.length} files → ${path.relative(process.cwd(), metaPath)}`);
