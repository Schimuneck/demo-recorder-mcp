---
description: Create a new git tag and GitHub release
---

# Create Release

Create a new version tag and GitHub release for demo-recorder-mcp.

## Parameters

Ask user:
- **Version**: Semantic version (e.g., `1.0.0`, `1.1.0`)
- **Release type**: `major`, `minor`, or `patch`
- **Release notes**: Summary of changes (or auto-generate from commits)

## Pre-flight Checks

### 1. Verify clean working directory

```bash
git status --porcelain
```

If dirty, ask user to commit or stash changes first.

### 2. Verify on main branch

```bash
git branch --show-current
```

Warn if not on `main`.

### 3. Pull latest changes

```bash
git pull origin main
```

### 4. Run tests before release

```bash
uv run pytest tests/ -v
```

Abort if tests fail.

## Release Steps

### 5. Update version in pyproject.toml

Change `version = "X.X.X"` to new version.

### 6. Commit version bump

```bash
git add pyproject.toml
git commit -m "chore: bump version to v{{version}}"
```

### 7. Create annotated tag

```bash
git tag -a v{{version}} -m "Release v{{version}}"
```

### 8. Push tag and commits

```bash
git push origin main
git push origin v{{version}}
```

### 9. Create GitHub release

```bash
gh release create v{{version}} \
  --title "v{{version}}" \
  --notes "{{release_notes}}" \
  --latest
```

### 10. Verify release

```bash
gh release view v{{version}}
```

## Post-release

Remind user to:
- Build and push new Docker images with version tag
- Update documentation if needed
- Announce release
