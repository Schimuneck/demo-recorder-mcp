---
description: Build Docker image using Podman
---

# Build Docker Image

Build the demo-recorder-mcp container image.

## Parameters

Ask user if not specified:
- **Image type**: `stdio` (default) or `http`
- **Tag**: version tag (default: `latest`)

## Steps

### 1. Verify Podman is available

```bash
podman --version
```

### 2. Build the image

**For STDIO image (default):**
```bash
podman build -t demo-recorder-mcp:{{tag}} .
```

**For HTTP/SSE image:**
```bash
podman build -f Dockerfile.http -t demo-recorder-mcp:http-{{tag}} .
```

### 3. Verify build

```bash
podman images | grep demo-recorder-mcp
```

### 4. Report success

Show image size and creation time.
