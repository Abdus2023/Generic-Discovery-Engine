// eslint.config.js — flat config (ESLint 9+) for Generic Discovery Engine v0.7.4
// Requires: npm i -D eslint  (optional; npm run verify does not require it)
import js from "@eslint/js";
import globals from "globals";

export default [
  {
    ignores: ["dist/*.v*.user.js", "Continue Architecture Planning.md"],
  },
  js.configs.recommended,
  {
    files: ["dist/generic-discovery-engine.user.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: {
        ...globals.browser,
        GM_getValue: "readonly",
        GM_setValue: "readonly",
        GM_xmlhttpRequest: "readonly",
      },
    },
    rules: {
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
      "no-undef": "warn",
      "no-redeclare": "warn",
    },
  },
  {
    files: ["tests/**/*.js", "eslint.config.js"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: { ...globals.node },
    },
    rules: {
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
    },
  },
];
