---
name: write-a-principle
description: Write repository-local architecture principle documents from a standard template. Use when the user asks to create, draft, scaffold, write, or add a principle under the principles folder.
---

# Write A Principle

## Quick Start

Write principle documents under the consuming repository's root `principles/` folder using the preset template in `templates/principle-template.md`.

When this toolkit is used as a submodule, do not write generated principle files under `toolkit/principles/`. Run the command from the private repository root, or pass `--output-root <private-repo-root>`, so output goes to `<private-repo-root>/principles/`.

Use the helper script when the requested principle has a clear name, intent, principles, and usage guidance:

```sh
python3 skills/write-a-principle/scripts/write-principle.py "Data Architecture Principles" \
  --intent "Define durable data architecture principles for ownership, quality, governance, and integration." \
  --principle "Data ownership must be explicit and aligned to business domains." \
  --principle "Critical data must have defined quality expectations and stewardship." \
  --usage "Use these principles when designing data platforms, integrations, analytics products, and governance processes."
```

This creates `principles/data-architecture-principles.md`.

When running from a private lab repo that contains this toolkit as a submodule:

```sh
python3 toolkit/skills/write-a-principle/scripts/write-principle.py "Data Architecture Principles" \
  --intent "Define durable data architecture principles for ownership, quality, governance, and integration." \
  --principle "Data ownership must be explicit and aligned to business domains." \
  --principle "Critical data must have defined quality expectations and stewardship." \
  --usage "Use these principles when designing data platforms, integrations, analytics products, and governance processes."
```

Run from the private lab root, this creates `principles/data-architecture-principles.md` beside `toolkit/`.

Each generated principle is also added to `principles/_principles-list.md` using a markdown table with `name`, `description`, and `last_updated` columns. Create `_principles-list.md` when it does not exist. Keep rows sorted alphabetically by principle name.

## Workflow

1. Determine the principle document name and convert it to `<workspace-root>/principles/<slug>.md`.
2. Capture a concise intent statement.
3. Capture 3-7 concrete principles.
4. Capture practical usage guidance.
5. Generate the file under the consuming repository's root `principles/` folder using the preset template.
6. Add or update the generated principle in `<workspace-root>/principles/_principles-list.md` with a relative link, intent, and `last_updated` date.
7. Do not overwrite an existing principle file unless the user explicitly asks.
8. If the toolkit is mounted as `toolkit/` in a private lab repo, write the generated principle to the private lab root, not to `toolkit/principles/`.
9. Keep the style consistent with the existing files in `principles/`.

## Output Standard

Each principle file must use this structure:

```md
# Principle Document Name

## Intent

One-sentence intent.

## Principles

1. Principle one.
2. Principle two.
3. Principle three.

## Usage

When and how to apply these principles.
```

## Template

Use `templates/principle-template.md` as the source template for generated principle files.
