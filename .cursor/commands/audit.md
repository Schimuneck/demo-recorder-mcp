---
description: Audit dependencies for updates and vulnerabilities
---

# Dependency Audit

Check for outdated packages, security vulnerabilities, and conflicts.

## Quick Audit

```bash
cd /Users/schimuneck/projects/getademo/demo-recorder-mcp
source .venv/bin/activate
python .cursor/agents/scripts/audit_deps.py
```

## Full Audit (with security scan)

```bash
python .cursor/agents/scripts/audit_deps.py --full
```

## Auto-fix Outdated

```bash
python .cursor/agents/scripts/audit_deps.py --fix
```

## Save Report

```bash
python .cursor/agents/scripts/audit_deps.py --report audit-$(date +%Y%m%d).md
```

## Report Summary

Show:
- Total packages
- Outdated count with list
- Vulnerabilities found
- Conflicts detected
- Recommended actions
