---
name: create-mcp-tool
description: Create new MCP tools for demo-recorder following project patterns. Use when adding recording, video, TTS, or utility tools, or when the user asks to add a new tool to the MCP server.
---

# Create MCP Tool

Guide for adding new tools to the demo-recorder MCP server.

## Tool Categories

| Category | File | Purpose |
|----------|------|---------|
| Recording | `src/recorder/tools/recording.py` | Start/stop recording |
| Video | `src/recorder/tools/video.py` | Editing, merging, trimming |
| TTS | `src/recorder/tools/tts.py` | Text-to-speech |
| Guides | `src/recorder/tools/guides.py` | Workflow phase guides |
| Windows | `src/recorder/tools/windows.py` | Window management |

## Step 1: Choose Location

- **New category**: Create `src/recorder/tools/your_category.py`
- **Existing category**: Add to appropriate file above

## Step 2: Create Tool Function

```python
def register_your_tools(mcp, backend):
    """Register your tools with the MCP server."""
    
    @mcp.tool(description="Clear, concise description for the LLM")
    async def your_tool_name(
        param1: str,
        param2: int = 30,
        optional_param: str = None
    ) -> str:
        """Docstring with Args/Returns sections.
        
        Args:
            param1: Description of param1.
            param2: Description with default noted.
            optional_param: Optional parameter description.
        
        Returns:
            String describing success/failure and relevant info.
        """
        # Implementation
        return f"Result: {param1}"
```

## Step 3: Register in `__init__.py`

Add to `src/recorder/tools/__init__.py`:

```python
from .your_category import register_your_tools

def register_all_tools(mcp, backend):
    # ... existing registrations ...
    register_your_tools(mcp, backend)
```

## Patterns to Follow

### Return Structured Info (not just "done")

```python
# ✅ Good
return (
    f"Recording stopped\n"
    f"Output: {filename}\n"
    f"Duration: {duration:.1f}s\n"
    f"Size: {size:.1f} MB"
)

# ❌ Bad
return "Done"
```

### Use Backend for Environment-Specific Logic

```python
# Get recordings directory (varies by mode)
output_path = backend.get_recordings_dir() / filename

# Get URL for media (container mode only)
url = backend.get_media_url(output_path)
```

### Return Errors as Strings, Not Exceptions

```python
# ✅ Good - LLM can understand and retry
if not file.exists():
    return f"Error: File not found: {filename}"

# ❌ Bad - breaks the MCP call
raise FileNotFoundError(filename)
```

## Testing

```bash
# Run tests
uv run pytest tests/ -v

# Test specific tool
uv run pytest tests/test_tools.py -k "test_your_tool"
```
