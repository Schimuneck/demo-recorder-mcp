---
description: Plan a new feature - generates spec, plan, and tasks
---

# Plan New Feature

Create a complete feature specification with implementation plan and tasks.

## Workflow

When user invokes `/specify` with a description:

### Step 1: Gather Requirements

Ask clarifying questions if needed:
- What is the core functionality?
- What are the expected inputs/outputs?
- Are there any constraints or dependencies?

### Step 2: Create Specification

Create `.specify/specs/{feature-name}.md` with:
- Feature overview and goals
- User stories with priorities (P1, P2, P3)
- Acceptance scenarios (Given/When/Then)
- Functional requirements
- Edge cases
- Technical approach

### Step 3: Create Implementation Plan

Create `.specify/specs/{feature-name}-plan.md` with:
- Technical context (language, dependencies, testing)
- Constitution compliance check
- Project structure (new files/directories)
- Implementation phases
- Risk assessment
- Effort estimates

### Step 4: Create Task Breakdown

Create `.specify/specs/{feature-name}-tasks.md` with:
- Numbered tasks grouped by phase
- Each task has: priority, estimate, file, checklist
- Implementation order diagram
- Quick start commands

### Step 5: Summary

Report back with:
- Links to all created files
- Task count and effort estimate
- Suggested first steps
- Branch name suggestion

## Output Files

```
.specify/specs/
├── {feature-name}.md           # Specification
├── {feature-name}-plan.md      # Implementation plan
└── {feature-name}-tasks.md     # Task breakdown
```

## Example

**User**: `/spec-kit Add support for ElevenLabs TTS as alternative voice engine`

**Agent**:
1. Creates `elevenlabs-tts.md` specification
2. Creates `elevenlabs-tts-plan.md` implementation plan
3. Creates `elevenlabs-tts-tasks.md` task breakdown
4. Reports summary with task count and next steps

## Guidelines

- Follow project constitution (`.specify/memory/constitution.md`)
- Use existing patterns from `src/recorder/tools/`
- Ensure MCP-first architecture (all features as tools)
- Include tests for all new functionality
- Keep tasks small and independently testable

## Templates Reference

- Spec template: `.specify/templates/spec-template.md`
- Plan template: `.specify/templates/plan-template.md`
- Tasks template: `.specify/templates/tasks-template.md`
