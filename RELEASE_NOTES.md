# mongo-x-ray-ftdc — Release Notes

## 2.1.2

### Dependencies
- Requires `pymongoftdc>=0.1.2`. The parser API the plugin uses (`FTDCReader`, `FTDCError`, `DataPoint`) is unchanged, and the unit tests run against 0.1.2.

## 2.1.1

Dependency and automation release — the plugin's own behaviour is unchanged.

### Dependencies
- Build: `setuptools` 84.0.0 → 84.2.1 ([`GHSA-xmj3-9gf7-h52w`](https://github.com/advisories/GHSA-xmj3-9gf7-h52w), low — Windows path escape via `namespace_packages.txt` during a legacy wheel install).

### Automation
- **Dependabot auto-merge repaired**: the workflow counted its own in-progress `auto-merge` check when waiting for "every check to pass", so it always timed out and updates stayed open. It now ignores its own check, retries a merge that lost a race with a sibling update, requests a rebase when the branch conflicts, and tolerates branches modified by hand.
- Repository labels `dependencies`, `python` and `github-actions` added, so Dependabot can tag its pull requests.

**Project:** FTDC (Full Time Diagnostic Data Capture) analysis plugin for [x-ray](https://github.com/mongodb-ps/ce-mongo-x-ray).

## Release 2.1.0

No functional changes in this plugin — it is a version alignment with the x-ray 2.1.0 release, plus documentation, CI and tooling updates.

### Changed
- Version bumped to **2.1.0** to match the core release line.
- README gained the PyPI badge.

### Development
- **CI now runs on pull requests** as well as on pushes to `main`, so a dependency bump is linted and tested before it can land.
- **Dependabot** is enabled for `pip` and GitHub Actions (weekly). Patch and minor updates merge automatically once every check is green, as do major updates of the CI actions and the build/lint/test tooling; a major update of a runtime dependency (`mongo-x-ray`) is left for review, and a failing or missing check leaves the pull request open instead of merging.
- **Tooling bumped**: `setuptools` 83.0.0 → 84.0.0, `actions/checkout` v4 → v7, `actions/setup-python` v5 → v7.

### Inherited from core (applies to every ftdc report)
- **Copy icons**: every backtick-wrapped string, every code block (top-right icon instead of the "Copy" text) and every table `<pre>` block can be copied with one click; copying code blocks preserves line breaks and indentation.
- **Output folder naming**: generated report folders are prefixed with the plugin name (`ftdc-default-<timestamp>`, `ftdc-<hostname>-default-<timestamp>`), including when using `--discover`.

## Release 2.0.0

The FTDC analysis capability was extracted from the `mongo-x-ray` core into a standalone, installable plugin: analysis items, parsers, chart engine and HTML report templates, with optional AI-generated summaries built on the shared core AI client. It ships a Makefile (lint, minify, unit tests), GitHub Actions CI, CodeQL, and (Test)PyPI publishing via trusted publishing; `x-ray ftdc --version` reports the plugin's own version.
