# mongo-x-ray-ftdc — Release Notes

**Project:** FTDC (Full Time Diagnostic Data Capture) analysis plugin for [x-ray](https://github.com/mongodb-ps/ce-mongo-x-ray).

## Release 2.1.0

No functional changes in this plugin — it is a version alignment with the x-ray 2.1.0 release, plus documentation.

### Changed
- Version bumped to **2.1.0** to match the core release line.
- README gained the PyPI badge.

### Inherited from core (applies to every ftdc report)
- **Copy icons**: every backtick-wrapped string, every code block (top-right icon instead of the "Copy" text) and every table `<pre>` block can be copied with one click; copying code blocks preserves line breaks and indentation.
- **Output folder naming**: generated report folders are prefixed with the plugin name (`ftdc-default-<timestamp>`, `ftdc-<hostname>-default-<timestamp>`), including when using `--discover`.

## Release 2.0.0

The FTDC analysis capability was extracted from the `mongo-x-ray` core into a standalone, installable plugin: analysis items, parsers, chart engine and HTML report templates, with optional AI-generated summaries built on the shared core AI client. It ships a Makefile (lint, minify, unit tests), GitHub Actions CI, CodeQL, and (Test)PyPI publishing via trusted publishing; `x-ray ftdc --version` reports the plugin's own version.
