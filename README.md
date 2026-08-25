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

## Report

The baseline analysis reports the capture timespan and the effective sample rate,
then groups metrics into Workload, Read/Write Operations and Latencies, and
Performance sections. It includes operation rates and latencies, host memory
and CPU utilization, WiredTiger cache utilization, queue depth for each block
device, and free-space and utilization charts for every reported mount point.
Each metric shows its peak, average, unit, and a chart saved under the report
output's `charts` directory.

`start_time` and `end_time` are inclusive UTC ISO-8601 timestamps. When omitted,
the first and last data points in the archive are used.

### Chart configuration

Chart dimensions can be tuned in the checkset config:

```json
"BaselineAnalysisItem": {
  "chart_width": 450,
  "chart_height": 150
}
```

The fallback dimensions are defined in `mongo_x_ray_ftdc/charts.py`. Vertical
grid lines are spaced every 100 pixels and horizontal grid lines every 50 pixels.
Workload and operation/latency charts use lines. Performance charts use bars.
Member-state charts are always 450×50 pixel bars.

## AI Analysis (Optional)

FTDC reports can include AI-generated summaries for each section (Workload,
Ops and Latencies, Performance). The analysis appears as a brief 2-3 sentence
assessment at the end of each section, flagging potential issues or confirming
normal operation.

**Configuration** — set the following environment variables:

| Variable          | Required | Default        | Description                             |
| ----------------- | :------: | -------------- | --------------------------------------- |
| `OPENAI_API_KEY`  |   Yes    | —              | API key for the AI service              |
| `OPENAI_BASE_URL` |    No    | OpenAI default | Compatible API endpoint (e.g. DeepSeek) |
| `AI_MODEL`        |    No    | `gpt-4o`       | Model name to use                       |

If `OPENAI_API_KEY` is not set, AI analysis is silently skipped.

**Example** `.env` file:

```bash
OPENAI_API_KEY="sk-..."
OPENAI_BASE_URL="https://api.deepseek.com"
AI_MODEL="deepseek-v4-pro"
```

Or export directly in the shell:

```bash
export OPENAI_API_KEY="sk-..."
x-ray ftdc /var/lib/mongo/diagnostic.data
```

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
