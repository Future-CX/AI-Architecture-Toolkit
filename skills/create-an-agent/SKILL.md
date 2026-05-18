---
name: create-an-agent
description: Create repository-local architecture agent definitions from a standard template. Use when the user asks to create, draft, scaffold, or add an agent under the agents folder.
---

# Create An Agent

## Quick Start

Create agent definitions under `agents/` using the preset template in `templates/agent-template.md`.

Use the helper script when the requested agent has a clear name, purpose, and responsibilities:

```sh
python3 skills/create-an-agent/scripts/create-agent.py "Data Architect" \
  --purpose "Support data architecture decisions across platforms, ownership, quality, and governance." \
  --responsibility "Clarify data ownership, domains, and critical data flows." \
  --responsibility "Assess data quality, privacy, retention, and lineage needs." \
  --responsibility "Review analytics, integration, and operational data implications."
```

This creates `agents/data-architect-agent.md`.

## Workflow

1. Determine the agent name and convert it to `<slug>-agent.md`.
2. Capture a one-sentence purpose.
3. Capture 3-7 concrete responsibilities.
4. Generate the file under `agents/` using the preset template.
5. Do not overwrite an existing agent file unless the user explicitly asks.
6. Keep the style consistent with the existing files in `agents/`.
7. Update the Agents table in the top-level `README.md` whenever an agent is created or updated.

## Output Standard

Each agent file must use this structure:

```md
# Agent Name

## Purpose

One-sentence purpose.

## Recommended Model

Use a frontier reasoning model for complex architecture decisions, tradeoff analysis, and review preparation. Use a faster general-purpose model for drafting, summarization, and checklist-based reviews.

## Responsibilities

- Responsibility one.
- Responsibility two.
- Responsibility three.
```

## Template

Use `templates/agent-template.md` as the source template for generated agent files.
