---
name: architecture-decision-record
description: Record durable architecture decisions as concise ADRs using the repository ADR format. Use when a decision is hard to reverse, surprising without context, and the result of a real trade-off.
---

# Architecture Decision Record

## Quick Start

Use this skill when a design conversation produces a decision that should be remembered by future readers.

When this toolkit is used as a submodule, do not write ADRs under `toolkit/adr/`. Run the command from the private repository root, or pass `--output-root <private-repo-root>`, so output goes to the consuming repository.

```sh
python3 skills/architecture-decision-record/scripts/write-adr.py "Use Domain Events Between Ordering And Billing" \
  --summary "Ordering and Billing will communicate via domain events instead of synchronous HTTP. This reduces runtime coupling and supports independent deployment, accepting eventual consistency as a trade-off."
```

When running from a private lab repo that contains this toolkit as a submodule:

```sh
python3 toolkit/skills/architecture-decision-record/scripts/write-adr.py "Use Domain Events Between Ordering And Billing" \
  --summary "Ordering and Billing will communicate via domain events instead of synchronous HTTP. This reduces runtime coupling and supports independent deployment, accepting eventual consistency as a trade-off."
```

Each generated ADR is also added to `adr/_adr-list.md` using a markdown table with `name`, `description`, and `last_updated` columns. Create `_adr-list.md` when it does not exist. Keep rows sorted alphabetically by ADR title.

Create ADRs only when all three conditions are true:

1. The decision is hard to reverse.
2. The decision is surprising without context.
3. The decision is the result of a real trade-off.

## Workflow

1. Confirm the decision, context, and selected option.
2. Identify the meaningful alternatives that were rejected.
3. Check whether the decision meets the ADR threshold.
4. If it qualifies, write the ADR under the consuming repository's root `adr/` folder using `templates/adr-template.md`.
5. Add or update the ADR in `adr/_adr-list.md` with a relative link, summary, and `last_updated` date.
6. If it does not qualify, summarize the decision inline without creating an ADR.

## Format

Use [ADR template](templates/adr-template.md) for file location, numbering, structure, and optional sections.
