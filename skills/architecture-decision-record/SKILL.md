---
name: architecture-decision-record
description: Record durable architecture decisions as concise ADRs using the repository ADR format. Use when a decision is hard to reverse, surprising without context, and the result of a real trade-off.
---

# Architecture Decision Record

## Quick Start

Use this skill when a design conversation produces a decision that should be remembered by future readers.

Create ADRs only when all three conditions are true:

1. The decision is hard to reverse.
2. The decision is surprising without context.
3. The decision is the result of a real trade-off.

## Workflow

1. Confirm the decision, context, and selected option.
2. Identify the meaningful alternatives that were rejected.
3. Check whether the decision meets the ADR threshold.
4. If it qualifies, write the ADR using `templates/adr-template.md`.
5. If it does not qualify, summarize the decision inline without creating an ADR.

## Format

Use [ADR template](templates/adr-template.md) for file location, numbering, structure, and optional sections.
