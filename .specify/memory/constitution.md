# Demo Recorder MCP Constitution

An MCP server for creating professional demo videos with synchronized voiceover narration.

## Core Principles

### I. MCP-First Architecture
Every feature must be exposed as an MCP tool. Tools are the primary interface - they must be self-contained, independently testable, and have clear descriptions for LLM consumption. Use FastMCP decorators for tool registration.

### II. Backend Abstraction
Recording operations use the abstract `RecordingBackend` interface. Implementations (ContainerBackend, HostBackend) handle environment-specific logic. New features must work in both modes when applicable.

### III. Scene-Based Workflow
Demos are recorded as short scenes (10-30 seconds), not long videos. The 4-phase workflow (planning → setup → recording → editing) is mandatory. Tools guide users through this process via phase guides.

### IV. Return Values Over Exceptions
MCP tools return structured string responses with success/failure info. Never raise exceptions in tool functions - return descriptive error messages that LLMs can understand and act upon.

### V. Test Coverage Required
All new tools must have pytest tests. Use `asyncio_mode = "auto"` for async tests. Run E2E tests after significant changes to verify the full workflow.

## Technology Stack

| Component | Technology | Constraint |
|-----------|------------|------------|
| Framework | FastMCP | `>=2.0.0,<3.0.0` |
| Python | 3.10+ | Multi-version support |
| Video | FFmpeg | Required dependency |
| TTS | OpenAI / Edge TTS | Fallback pattern |
| Container | Podman/Docker | Both supported |

## Development Workflow

1. **Planning**: Use `/speckit.specify` for new features
2. **Implementation**: Follow existing patterns in `src/recorder/tools/`
3. **Testing**: Run `uv run pytest` and E2E tests
4. **Documentation**: Update README for user-facing changes

## Quality Gates

- [ ] All tests pass (`uv run pytest tests/ -v`)
- [ ] Ruff linting clean (`ruff check src/ tests/`)
- [ ] E2E workflow verified (recording, TTS, video editing)
- [ ] Works in both Host and Container modes (when applicable)
- [ ] Tool descriptions are clear for LLM consumption

## Governance

This constitution guides all development decisions. Refer to:
- `.cursor/rules/` - Coding patterns and conventions
- `.cursor/skills/` - Task-specific implementation guides
- `.cursor/commands/` - Development workflows

**Version**: 1.0.0 | **Ratified**: 2026-03-13 | **Last Amended**: 2026-03-13
