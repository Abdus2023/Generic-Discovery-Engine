// eslint.config.js — flat config (ESLint 9+) for Generic Discovery Engine v0.7.4
// Requires: npm i -D eslint  (optional; npm run verify does not require it)
import js from "@eslint/js";
import globals from "globals";

export default [
  {
    ignores: ["dist/generic-discovery-engine.v0.7.1.user.js", "dist/generic-discovery-engine.min.js", "dist/generic-discovery-engine.esm.js", "dist/.build-meta.json", "dist/.esm-metafile.json", "Continue Architecture Planning.md", "coverage/**", "node_modules/**"],
  },
  js.configs.recommended,
  {
    files: ["dist/generic-discovery-engine.user.js", "src/**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: {
        ...globals.browser,
        ...globals.node,
        GM_getValue: "readonly",
        GM_setValue: "readonly",
        GM_xmlhttpRequest: "readonly",
        trustedTypes: "readonly",
        PerformanceObserver: "readonly",
        MutationObserver: "readonly",
        DOMParser: "readonly",
        AbortController: "readonly",
        Blob: "readonly",
        URL: "readonly",
        GM: "readonly",
      },
    },
    rules: {
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
      "no-undef": "off",
      "no-redeclare": "warn",
      "no-empty": "warn",
      "no-useless-escape": "warn",
    },
  },
  {
    files: ["tests/**/*.js", "scripts/**/*.js", "eslint.config.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: { ...globals.node },
    },
    rules: {
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "no-undef": "off",
      "no-dupe-keys": "warn",
      "no-useless-escape": "warn",
    },
  },
];
