---
description: Run linter and auto-fix code style issues
---

# Lint Code

Run ruff linter to check and fix code style.

## Check Only

```bash
cd /Users/schimuneck/projects/getademo/demo-recorder-mcp
source .venv/bin/activate
ruff check src/ tests/
```

## Auto-fix Issues

```bash
ruff check --fix src/ tests/
```

## Format Code

```bash
ruff format src/ tests/
```

## Check + Format (Recommended)

```bash
ruff check --fix src/ tests/ && ruff format src/ tests/
```

## Configuration

Ruff config from `pyproject.toml`:
- Line length: 100
- Target: Python 3.10
- Rules: E, F, I, W (ignore E501)

## Pre-commit Check

Run before committing:

```bash
ruff check src/ tests/ && uv run pytest tests/ -v -x
```
