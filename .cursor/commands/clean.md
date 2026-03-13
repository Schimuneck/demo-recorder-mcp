---
description: Clean build artifacts, caches, and temporary files
---

# Clean Project

Remove build artifacts, caches, and temporary files.

## Quick Clean

Remove Python caches and build artifacts:

```bash
cd /Users/schimuneck/projects/getademo/demo-recorder-mcp

# Python caches
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# Build artifacts
rm -rf build/ dist/

echo "✅ Python caches cleaned"
```

## Clean Recordings

Remove test recordings (keep real demos):

```bash
rm -f ~/recordings/test_*.mp4
rm -f ~/recordings/test_*.mp3
echo "✅ Test recordings cleaned"
```

## Clean Container Images

Remove old dev images:

```bash
podman rmi demo-recorder-mcp:dev 2>/dev/null
podman rmi demo-recorder-mcp:test 2>/dev/null
podman image prune -f
echo "✅ Container images cleaned"
```

## Deep Clean

Full cleanup including venv (use with caution):

```bash
# This removes virtual environment!
rm -rf .venv/
rm -f uv.lock

# Recreate
python -m venv .venv
source .venv/bin/activate
pip install -e ".[all,dev]"
```

## Verify Clean State

```bash
git status
du -sh .
```
