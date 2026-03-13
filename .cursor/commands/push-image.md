---
description: Push Docker image to Docker Hub
---

# Push Image to Docker Hub

Push demo-recorder-mcp image to Docker Hub registry.

## Prerequisites

- Docker Hub account
- Logged in: `podman login docker.io`

## Parameters

Ask user:
- **Docker Hub username**: (required)
- **Tag**: version to push (e.g., `latest`, `1.0.0`)
- **Image type**: `stdio` or `http`

## Steps

### 1. Verify login status

```bash
podman login --get-login docker.io
```

If not logged in:
```bash
podman login docker.io
```

### 2. Tag image for Docker Hub

```bash
podman tag demo-recorder-mcp:{{tag}} docker.io/{{username}}/demo-recorder-mcp:{{tag}}
```

For HTTP image:
```bash
podman tag demo-recorder-mcp:http-{{tag}} docker.io/{{username}}/demo-recorder-mcp:http-{{tag}}
```

### 3. Push to registry

```bash
podman push docker.io/{{username}}/demo-recorder-mcp:{{tag}}
```

### 4. Verify push

```bash
podman search docker.io/{{username}}/demo-recorder-mcp
```

### 5. Report success

Show the pull command users can use:
```
docker pull {{username}}/demo-recorder-mcp:{{tag}}
```
