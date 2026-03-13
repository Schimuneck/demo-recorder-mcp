---
name: deploy-demo-recorder
description: Deploy demo-recorder MCP in host mode (local) or container mode (Docker/Podman with Playwright). Use when setting up, installing, configuring, or troubleshooting demo-recorder deployment.
---

# Deploy Demo Recorder

Two deployment modes with different capabilities:

| Mode | Best For | Browser | Quality |
|------|----------|---------|---------|
| **Host** | Production demos | Playwright MCP (separate) | Best - native |
| **Container** | CI/CD, reproducible | Playwright (included) | Good - Xvfb |

## Host Mode (Recommended)

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Playwright MCP)
- FFmpeg (`brew install ffmpeg`)
- Chrome browser

### Installation

```bash
cd /path/to/demo-recorder-mcp
python -m venv .venv && source .venv/bin/activate
pip install -e ".[all]"
```

### Cursor MCP Config (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--browser=chrome", "--isolated"]
    },
    "demo-recorder-local": {
      "command": "/path/to/demo-recorder-mcp/.venv/bin/recorder",
      "env": {
        "OPENAI_API_KEY": "sk-your-key",
        "RECORDINGS_DIR": "${workspaceFolder}/recordings"
      }
    }
  }
}
```

### Critical: Disable Cursor Browser Automation

**Settings → Tools → Browser → Browser Automation → OFF**

Without this, viewport overflows and window detection fails.

### macOS: Grant Screen Recording Permission

**System Settings → Privacy & Security → Screen Recording → Add Cursor → Restart Cursor**

---

## Container Mode

### Build

```bash
# STDIO container
podman build -t demo-recorder-mcp .

# HTTP/SSE container
podman build -f Dockerfile.http -t demo-recorder-mcp:http .
```

### Run (STDIO - Podman)

```json
{
  "mcpServers": {
    "demo-recorder": {
      "command": "podman",
      "args": [
        "run", "-i", "--rm",
        "-v", "/path/to/recordings:/app/recordings",
        "-e", "OPENAI_API_KEY=sk-your-key",
        "demo-recorder-mcp",
        "/app/run-mcp.sh", "multi-stdio"
      ]
    }
  }
}
```

### Run (STDIO - Docker)

```json
{
  "mcpServers": {
    "demo-recorder": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--add-host=host.docker.internal:host-gateway",
        "-v", "/path/to/recordings:/app/recordings",
        "-e", "OPENAI_API_KEY=sk-your-key",
        "demo-recorder-mcp",
        "/app/run-mcp.sh", "multi-stdio"
      ]
    }
  }
}
```

### Run (HTTP/SSE)

```bash
podman run -d --name demo-recorder \
  -p 8081:8081 -p 8080:8080 \
  -v ./recordings:/app/recordings \
  -e OPENAI_API_KEY=sk-your-key \
  demo-recorder-mcp:http
```

```json
{
  "mcpServers": {
    "demo-recorder": {
      "url": "http://localhost:8081/mcp/",
      "transport": "streamable-http"
    }
  }
}
```

---

## Access Local Dev Servers from Container

| Runtime | Hostname | Extra Flags |
|---------|----------|-------------|
| Podman | `host.containers.internal` | None |
| Docker | `host.docker.internal` | `--add-host=host.docker.internal:host-gateway` |

Update your dev server (e.g., Vite):

```typescript
server: {
  host: true,
  allowedHosts: ['host.containers.internal', 'host.docker.internal']
}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Window not found | Run `list_windows()`, use exact title |
| Viewport overflow | Disable Cursor Browser Automation |
| Black video (macOS) | Grant Screen Recording permission, restart Cursor |
| Container: no windows | Call `browser_navigate()` first |
| Orphaned FFmpeg | `pkill -9 ffmpeg` |

### Health Check (Container HTTP)

```bash
curl http://localhost:8081/health
# {"status":"healthy","service":"demo-recorder-mcp","tools_count":36}
```
