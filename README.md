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

## Development

Requires Python 3.10+ and the [mongo-x-ray](https://github.com/mongodb-ps/ce-mongo-x-ray) core package.

```bash
make unit-test   # run the unit tests
make lint        # ruff check + ruff format --check
make minify      # minify templates
```
