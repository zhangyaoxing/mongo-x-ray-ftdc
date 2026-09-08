# mongo-x-ray-ftdc — Release Notes

**Project:** FTDC (Full Time Diagnostic Data Capture) analysis plugin for [x-ray](https://github.com/mongodb-ps/ce-mongo-x-ray). 28 commits, 2026-08-23 → 2026-08-28.

## Release 2.0.0 — FTDC Analysis Plugin for x-ray

The FTDC analysis capability was extracted from the `mongo-x-ray` core into a standalone, installable plugin. It analyzes MongoDB FTDC archives and generates baseline workload/performance reports (Markdown, HTML or PDF) with charts and optional AI-generated summaries.

### Major Changes

**Initial extraction & packaging**
- Imported the full FTDC analysis pipeline from the core project: analysis items, parsers, chart engine, HTML report templates, and tests. `8a48e75`
- Renamed the import package to `mongo_x_ray_ftdc` and aligned imports with the core `mongo_x_ray` namespace; bumped version to 2.0.0. `713f3ce`, `eb0ef52`, `30c6845`

**AI analysis**
- Replaced the private OpenAI client with the shared AI client from core (`mongo_x_ray_ftdc/ai.py`), enabling 2–3 sentence AI assessments per report section. `0a3f2ca`

**Plugin distribution**
- Declared the `mongo-x-ray-ftdc` distribution so `x-ray ftdc --version` resolves correctly. `c85df05`

**Build, CI & publishing**
- Added a Makefile (lint, minify, unit tests), ruff-based linting, GitHub Actions CI (lint + tests on push to main), and pyright config. `3d83a0c`, `8ae77fa`, `07409ad`
- Enabled CodeQL analysis and fixed the browser fixture it flagged; declared direct dependencies. `ce93b3e`, `f77dad7`
- Added GitHub Actions workflows to publish to (Test)PyPI on release via trusted publishing. `d141bfe`

**Tests & fixes**
- Made CLI tests standalone (removed log-plugin command cases so CI passes with only ftdc installed); updated test expectations for the `hc` alias. `8697fa4`, `c7cd550`

**Documentation**
- Rewrote the README with usage, full CLI parameter reference, analysis item descriptions, and MongoDB 5.0+ topology compatibility matrix. `2cced71`, `e9ab546`, `3f78cf1`, `40ec0cf`, `d4f9142`, `b18f13a`

**Housekeeping**
- Standardized VSCode ruff/pyright settings, removed pylint suppressions, unified copyright headers to 2026, and applied final ruff formatting. `274a214`–`94ec7f7`

*Current version: 2.0.0; no tags.*
