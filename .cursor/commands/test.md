---
description: Run tests (unit, E2E, or both)
---

# Run Tests

Run test suite for demo-recorder-mcp.

## Parameters

Ask user:
- **Test type**: `unit` (fast), `e2e` (full), or `all`

## Unit Tests

```bash
cd /Users/schimuneck/projects/getademo/demo-recorder-mcp
source .venv/bin/activate
uv run pytest tests/ -v --tb=short
```

## E2E Tests

```bash
python .cursor/agents/scripts/run_e2e_tests.py
```

### Quick E2E (smoke test)

```bash
python .cursor/agents/scripts/run_e2e_tests.py --quick
```

### Full E2E with container build

```bash
python .cursor/agents/scripts/run_e2e_tests.py --container
```

## Report Results

Show:
- Total tests run
- Passed / Failed / Skipped
- Duration
- Any failures with details
