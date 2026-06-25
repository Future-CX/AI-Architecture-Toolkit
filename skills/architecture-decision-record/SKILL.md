---
name: architecture-decision-record
description: Record durable architecture decisions as concise ADRs using the repository ADR format. Use when a decision is hard to reverse, surprising without context, and the result of a real trade-off.
---

# Architecture Decision Record

## Quick Start

Use this skill when a design conversation produces a decision that should be remembered by future readers.

When this toolkit is used as a submodule, do not write ADRs under `toolkit/adr/`. Run the command from the private repository root, or pass `--output-root <private-repo-root>`, so output goes to the consuming repository.

ADR filenames must use this format:

```text
adr-<4-digits>-<slug>.md
```

Start at `adr-0001`. For new ADRs, inspect existing `adr/adr-*.md` files and any legacy `adr/0001-*.md` files, choose the next available 4-digit number, and preserve gaps unless the user explicitly asks to renumber.

```sh
python3 skills/architecture-decision-record/scripts/write-adr.py "Use Domain Events Between Ordering And Billing" \
  --status accepted \
  --summary "Ordering and Billing will communicate via domain events instead of synchronous HTTP. This reduces runtime coupling and supports independent deployment, accepting eventual consistency as a trade-off."
```

When running from a private lab repo that contains this toolkit as a submodule:

```sh
python3 toolkit/skills/architecture-decision-record/scripts/write-adr.py "Use Domain Events Between Ordering And Billing" \
  --status accepted \
  --summary "Ordering and Billing will communicate via domain events instead of synchronous HTTP. This reduces runtime coupling and supports independent deployment, accepting eventual consistency as a trade-off."
```

Each generated ADR is also added to `adr/_adr-overview.md` using a markdown table with `name`, `status`, `description`, and `last_updated` columns. Create `_adr-overview.md` when it does not exist. Keep rows sorted alphabetically by ADR title.

Status values use colored icons in the overview:

- `proposed` renders as `🟡 proposed`
- `accepted` renders as `🟢 accepted`
- `deprecated` renders as `🔴 deprecated`
- `superseded` renders as `⚫ superseded`

Create ADRs only when all three conditions are true:

1. The decision is hard to reverse.
2. The decision is surprising without context.
3. The decision is the result of a real trade-off.

## Workflow

1. Confirm the decision, context, and selected option.
2. Identify the meaningful alternatives that were rejected.
3. Write the opening summary as no more than two short paragraphs. Start with the business outcome, the decision, and the operational impact.
4. Target a Readability Score of 40 or higher. If the score is below 40, simplify before publishing.
5. When rejected alternatives are worth remembering, include a `Considered Options` section with the options listed as bullets first, followed by a comparison table. Use options as columns and include rows for Architecture Fit, Company Fit, Effort, and Complexity. Keep each table cell to one sentence, no more than about 15 words, and avoid implementation detail unless it changes the decision.
6. Add a `Recommendation` section after `Considered Options` that names the preferred option and explains why it is stronger than the alternatives.
7. Keep `Consequences` to 3-6 bullets when the downstream effects are worth calling out.
8. Avoid dense technical terms where a plain phrase works. If a technical term is necessary, use it consistently and explain it in the first paragraph or in a glossary.
9. Run a final readability pass before publishing: shorten long sentences, split dense paragraphs, explain necessary terms, and remove implementation detail that does not affect the decision.
10. Check whether the decision meets the ADR threshold.
11. If it qualifies, write the ADR under the consuming repository's root `adr/` folder using `templates/adr-template.md` and the `adr-<4-digits>-<slug>.md` filename format.
12. Add or update the ADR in `adr/_adr-overview.md` with a relative link, status with colored icon, summary, and `last_updated` date.
13. If it does not qualify, summarize the decision inline without creating an ADR.

## Format

Use [ADR template](templates/adr-template.md) for file location, numbering, structure, and optional sections.

Use [ADR overview template](templates/adr-overview-template.md) for the `adr/_adr-overview.md` table structure.
