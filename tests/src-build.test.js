/**
 * src-build.test.js — Modular prelude & build determinism (v0.8.1)
 */
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const src = readFileSync(new URL('../dist/generic-discovery-engine.user.js', import.meta.url), 'utf8');
const pkg = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'));
const metaPath = new URL('../dist/.build-meta.json', import.meta.url);
const srcDir = new URL('../src/', import.meta.url);

describe('src modular prelude (v0.8.1)', () => {
  it('src/ contains 7 required files', () => {
    const files = readdirSync(srcDir);
    for (const f of ['config.js','utils.js','models.js','knowledge.js','ledger.js','providers.js','engine.js']) {
      assert.ok(files.includes(f), `src/${f} missing`);
      const p = path.join(new URL('../src/', import.meta.url).pathname, f);
      assert.ok(existsSync(p));
      const c = readFileSync(p, 'utf8');
      assert.ok(c.trim().length>10, `src/${f} empty`);
    }
  });
  it('src/config.js contains CONFIG.version 8', () => {
    const c = readFileSync(new URL('../src/config.js', import.meta.url), 'utf8');
    assert.match(c, /version:\s*8/);
    assert.match(c, /maxCandidates/);
  });
  it('dist header @version matches package.json', () => {
    assert.match(src, new RegExp(`@version\\s+${pkg.version.replace('.', '\\.')}`));
    assert.match(src, new RegExp(`v${pkg.version.replace('.', '\\.')} —`));
  });
  it('dist/.build-meta.json exists and matches dist hash and version', () => {
    assert.ok(existsSync(metaPath), 'dist/.build-meta.json missing — run npm run build');
    const meta = JSON.parse(readFileSync(metaPath, 'utf8'));
    const hash = crypto.createHash('sha256').update(src, 'utf8').digest('hex');
    assert.equal(meta.sha256, hash);
    assert.equal(meta.version, pkg.version);
    const wcLines = (src.match(/\n/g)||[]).length;
    assert.equal(meta.lines, wcLines);
  });
  it('ProviderRegistry has 9 providers ordered Html/Json/Xml/Css/JS/Robots/Headers/Binary/Text', () => {
    assert.match(src, /class ProviderRegistry/);
    const order = ['HtmlProvider','JsonProvider','XmlProvider','CssProvider','JavaScriptProvider','RobotsProvider','HeadersProvider','BinaryProvider','TextProvider'];
    let lastIdx=-1;
    for(const name of order){
      const idx=src.indexOf(`new ${name}()`);
      assert.ok(idx>lastIdx, `${name} out of order`);
      lastIdx=idx;
    }
    // Ensure TextProvider is last
    const textIdx=src.indexOf('new TextProvider()');
    const binaryIdx=src.indexOf('new BinaryProvider()');
    assert.ok(textIdx>binaryIdx);
  });
  it('exportData includes pattern/cluster via getPatternMetrics/getClusterMetrics', () => {
    assert.match(src, /getPatternMetrics/);
    assert.match(src, /getClusterMetrics/);
    assert.match(src, /patternIndex/);
  });
});
