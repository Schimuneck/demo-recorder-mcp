---
description: Start local development environment
---

# Start Development

Set up and run the local development environment.

## Parameters

Ask user:
- **Mode**: `host` (local MCP) or `http` (HTTP server for testing)

## Host Mode (Default)

Run these commands to start the MCP server:

```bash
cd /Users/schimuneck/projects/getademo/demo-recorder-mcp
source .venv/bin/activate
export $(cat .env 2>/dev/null | xargs)
recorder
```

Note: STDIO mode runs interactively - use HTTP mode for background testing.

## HTTP Mode

Start HTTP server for testing (can run in background):

```bash
cd /Users/schimuneck/projects/getademo/demo-recorder-mcp
source .venv/bin/activate
export $(cat .env 2>/dev/null | xargs)
recorder-http
```

Server runs on `http://localhost:8000`

Health check: `curl http://localhost:8000/health`

## Container Dev Mode

Build and run container locally:

```bash
cd /Users/schimuneck/projects/getademo/demo-recorder-mcp
podman build -t demo-recorder-mcp:dev .
podman run -it --rm \
  -v ./recordings:/app/recordings \
  -e OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d= -f2) \
  demo-recorder-mcp:dev
```

## Environment

The `.env` file is automatically loaded. Required variables:
- `OPENAI_API_KEY` - For high-quality TTS (falls back to Edge TTS if not set)
