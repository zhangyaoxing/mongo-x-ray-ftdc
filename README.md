# mongo-x-ray-ftdc

[![CI](https://github.com/zhangyaoxing/mongo-x-ray-ftdc/actions/workflows/ci.yml/badge.svg)](https://github.com/zhangyaoxing/mongo-x-ray-ftdc/actions/workflows/ci.yml)

FTDC (Full Time Diagnostic Data Capture) analysis plugin for [x-ray](https://github.com/mongodb-ps/ce-mongo-x-ray).

## Install

```bash
pip install mongo-x-ray mongo-x-ray-ftdc
```

## Usage

```bash
x-ray ftdc /var/lib/mongo/diagnostic.data
x-ray ftdc /var/lib/mongo/diagnostic.data 2026-06-17T08:00:00Z 2026-06-17T10:00:00Z
x-ray ftdc --discover /data/
```

## Parameters

```bash
x-ray ftdc [-h] [-s CHECKSET] [-o OUTPUT] [-f {markdown,html,pdf}] [--no-browser]
           [--svg] [-r RATE] [--discover] ftdc_path [start_time] [end_time]
```

| Argument | Description | Default |
| --- | --- | --- |
| `ftdc_path` | Path to a directory containing FTDC files. | required |
| `start_time` | Inclusive UTC start time in ISO-8601 format. | first data point |
| `end_time` | Inclusive UTC end time in ISO-8601 format. | last data point |
| `-s, --checkset` | Checkset to run. | `default` |
| `-o, --output` | Output folder path. | `output/` |
| `-f, --format` | Output format: `markdown`, `html` or `pdf` (PDF also keeps Markdown and HTML). | `html` |
| `--no-browser` | Do not open the generated report in the browser. | `false` |
| `--svg` | Reference SVG charts in the report instead of converting them to PNG. | `false` |
| `-r, --rate` | FTDC sampling rate (0-1). | `1 / number of ingested files` |
| `--discover` | Recursively search the given path for folders containing FTDC files. | `false` |

## Analysis Items

| Item | Purpose |
| --- | --- |
| `BaselineAnalysisItem` | Summarize the workload and performance of an FTDC capture: Workload, Ops and Latencies and Performance sections with charts, plus an optional AI-generated summary per section. |
| `MetadataReviewItem` | Display all FTDC metadata in tabbed code blocks for review. |

## Development

Requires Python 3.10+, MongoDB 5.0 or later, and the [mongo-x-ray](https://github.com/mongodb-ps/ce-mongo-x-ray) core package.

```bash
make unit-test   # run the unit tests
make lint        # ruff check + ruff format --check
make minify      # minify templates
```
