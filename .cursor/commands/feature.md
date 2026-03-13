---
description: Plan a new feature using spec-kit specification workflow
---

# Plan New Feature

Use spec-kit to create formal specifications for new features.

## Workflow

### 1. Review Constitution

First, understand the project principles:

```bash
cat .specify/memory/constitution.md
```

### 2. Create Specification

Use `/speckit.specify` command with feature details:
- Feature name and description
- User stories / use cases
- Technical requirements
- Acceptance criteria

### 3. Generate Plan

Use `/speckit.plan` to create implementation plan:
- Break down into phases
- Identify dependencies
- Estimate complexity

### 4. Create Tasks

Use `/speckit.tasks` to generate actionable tasks:
- Specific implementation steps
- Test requirements
- Documentation needs

### 5. Implement

Use `/speckit.implement` or work through tasks manually.

## Example: New TTS Engine

```markdown
## Feature: Add ElevenLabs TTS Support

### User Stories
- As a user, I want to use ElevenLabs voices for higher quality narration
- As a user, I want to select different voice IDs

### Technical Requirements
- Add elevenlabs-python dependency
- Create fallback chain: OpenAI → ElevenLabs → Edge TTS
- Support ELEVENLABS_API_KEY environment variable

### Acceptance Criteria
- [ ] TTS tool auto-detects available engines
- [ ] Voice selection works with ElevenLabs
- [ ] Graceful fallback when API unavailable
- [ ] Tests cover new engine
```

## Spec-kit Commands Reference

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Review/update project principles |
| `/speckit.specify` | Create feature specification |
| `/speckit.plan` | Generate implementation plan |
| `/speckit.tasks` | Create actionable task list |
| `/speckit.implement` | Execute implementation |
| `/speckit.clarify` | Ask questions to de-risk ambiguity |
| `/speckit.analyze` | Check consistency across artifacts |
