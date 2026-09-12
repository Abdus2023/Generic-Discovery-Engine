# Contradiction Register

These are derived evidence records. Historical source is not changed or resolved here.

## CONTRADICTION-001

**Evidence label:** `SUPPORTED`

The source calls the early userscripts self-contained/revised, but Markdown fence delimiters split their implementation bodies.

Evidence:
- Userscript Discovery Prototype.md:1940-2964 (art-5ff41289b5f1c428)
- Userscript Discovery Prototype.md:3045-4711 (art-b7850a391eddeb86)
- Continue Architecture Planning.md:36 explicitly calls stray backticks invalid JavaScript

Resolution: `NOT_RESOLVED`

## CONTRADICTION-002

**Evidence label:** `PROVED`

Document order regresses from a complete v0.5.0 userscript to another complete v0.4.0 userscript.

Evidence:
- Continue Architecture Planning.md:7177-7178 (art-2c6f74909f301798)
- Continue Architecture Planning.md:13486-13487 (art-c19ebb3956fba19c)

Resolution: `NOT_RESOLVED`

## CONTRADICTION-003

**Evidence label:** `PROVED`

Document order regresses from a complete v0.6.0 userscript to another complete v0.5.0 userscript.

Evidence:
- Continue Architecture Planning.md:23140-23141 (art-b1368ed9b372a6a6)
- Continue Architecture Planning.md:29438-29439 (art-f019277e6c28e8f5)

Resolution: `NOT_RESOLVED`

## CONTRADICTION-004

**Evidence label:** `PROVED`

The same explicit version labels identify byte-distinct complete userscripts.

Evidence:
- v0.4.0 at lines 2791 and 13486
- v0.5.0 at lines 7177, 18378, and 29438
- v0.6.0 at lines 23140, 34754, and 43195

Resolution: `NOT_RESOLVED; all variants retained`

