---
name: capability-overview
description: Write business capability overview documents from a standard template and store them under the root capabilities folder. Use when the user asks to create, draft, document, or assess a business capability, capability overview, capability map entry, or capability definition.
---

# Capability Overview

## Quick Start

Write capability overview documents under the consuming repository's root `capabilities/<slug>/` folder using the preset template in `templates/capability-overview-template.md`.

Before creating any output files or running the helper script, run a `grill-me` style clarification session using `../grill-me/SKILL.md`. Ask one question at a time until the capability name, domain, objective, scope, stakeholders, systems, terminology, assumptions, constraints, and desired output are clear enough to avoid avoidable misunderstanding.

During that clarification session, use `../ubiquitous-language/SKILL.md` whenever terms are vague, overloaded, conflicting, or important enough to become shared domain language. Create or update `<private-lab-root>/GLOSSARY.md` inline as terms are clarified; do not batch glossary updates until the end. Do not write the glossary inside this public toolkit repository when working with real company context.

After the clarification session, validate that `<private-lab-root>/GLOSSARY.md` was created or updated during the current run. If it was not created or updated, stop before generating capability overview files and ask the user to run the `grill-me` skill followed by the `ubiquitous-language` skill so the glossary is updated first.

When this toolkit is used as a submodule, do not write generated capability files under `toolkit/capabilities/`. Run the command from the private repository root, or pass `--output-root <private-repo-root>`, so output goes to `<private-repo-root>/capabilities/`.

Use the helper script only after the clarification session and glossary validation are complete, and only when the requested capability has clear input values:

```sh
python3 skills/capability-overview/scripts/write-capability-overview.py "Order Management" \
  --domain "Commerce" \
  --business-objective "Improve order accuracy, lifecycle visibility, and fulfillment coordination." \
  --stakeholder "Customer service" \
  --stakeholder "Operations" \
  --existing-system "ERP" \
  --strategic-importance "High" \
  --pain-point "Order status is fragmented across systems." \
  --related-capability "Inventory Management"
```

This creates `capabilities/order-management/order-management.md`.

If the requested name includes a redundant leading or trailing word `Capability`, remove it from the generated folder and filename. For example, `Search Capability` and `Capability Search` both create `capabilities/search/search.md`.

Each generated capability must also be added to `capabilities/_capability-list.md` using a markdown table with `name`, `description`, and `last_updated` columns. Create `_capability-list.md` when it does not exist. Keep rows sorted alphabetically by capability name.

When running from a private lab repo that contains this toolkit as a submodule:

```sh
python3 toolkit/skills/capability-overview/scripts/write-capability-overview.py "Order Management" \
  --domain "Commerce" \
  --business-objective "Improve order accuracy, lifecycle visibility, and fulfillment coordination." \
  --stakeholder "Customer service" \
  --existing-system "ERP" \
  --strategic-importance "High" \
  --pain-point "Order status is fragmented across systems." \
  --related-capability "Inventory Management"
```

Run from the private lab root, this creates `capabilities/order-management/order-management.md` beside `toolkit/`.

## Required Inputs

- Capability name
- Domain
- Business objective
- Stakeholders
- Existing systems
- Strategic importance
- Pain points
- Related capabilities

## Workflow

1. Start with the `grill-me` clarification session and update `<private-lab-root>/GLOSSARY.md` with `ubiquitous-language` as terminology is clarified.
2. Validate that `<private-lab-root>/GLOSSARY.md` was created or updated. If not, stop and ask the user to run `grill-me` and then `ubiquitous-language` before continuing.
3. Convert the capability name to `<workspace-root>/capabilities/<slug>/<slug>.md`, removing a redundant leading or trailing word `Capability` from the slug.
4. Derive the outputs from the inputs and any available repository context.
5. Use `templates/capability-overview-template.md` as the output structure.
6. Use `../create-drawio-diagram/SKILL.md` and its capability context helper to create `capability-overview.drawio` beside the generated overview. Keep diagram layout, styling, SVG generation, and application-header rules in the create-drawio-diagram skill.
7. Export or create a same-basename `capability-overview.svg`, sanitize it according to the Draw.io SVG export rules, and embed it in the capability overview just above `Main Business Features` without a separate diagram heading.
8. Do not overwrite an existing capability file unless the user explicitly asks.
9. Add or update the generated capability in `<workspace-root>/capabilities/_capability-list.md` with a relative link to `<slug>/<slug>.md`, description, and `last_updated` date.
10. If the toolkit is mounted as `toolkit/` in a private lab repo, write the generated capability overview to the private lab root, not to `toolkit/capabilities/`.
11. Keep company-confidential details out of the public toolkit repository; use a private company lab repo for real company content.
12. Run the readability and glossary compliance gate before finishing:

- Read `<private-lab-root>/GLOSSARY.md`.
- In the Glossary, find the `Jargon` section and its Avoid list.
- Search the generated capability overview Markdown for each avoided word or phrase.
- Replace avoided wording with the preferred glossary term when one is available.
- If no preferred term is available, rewrite the sentence in plain language or add an open question rather than leaving the avoided wording in the overview.
- Repeat the search after edits until no avoided terms remain, except inside explicit glossary references or quoted source text.
- Reread the opening sections and simplify any sentence that a non-technical business reader would need to parse twice.

## Required Outputs

Each capability overview must include:

- Capability definition
- Business outcome
- Capability context diagram as editable `.drawio` and embedded `.svg`
- Main Business Features
- Scope
- Inputs/outputs
- Processes supported
- Applications involved
- Application lifecycle management
- Data involved
- Integrations
- Potential KPIs
- NFR considerations
- Risks
- Maturity assessment
- Future-state considerations

## Readability Guidance

Capability overviews are for non-technical business readers. Architects and delivery teams should get enough context to act, but the document must be understandable to a reader without technical training and must start from business outcomes, ownership, impact, trade-offs, risks, and open questions.

Use the `check-readability` skill in `../check-readability/SKILL.md` before finishing a capability overview. Treat the target audience as non-technical business stakeholders unless the user gives a different audience.

The capability overview is not complete until the readability check passes these capability-specific expectations:

- The opening sections put the business outcome, operational impact, scope, trade-offs, risks, and open questions before implementation detail.
- Glossary `Jargon` terms from `Glossary.md` or `GLOSSARY.md` are removed from generated prose, headings, tables, and diagram labels unless they are quoted source text or explicit glossary references.
- Preferred glossary terms are used exactly when the glossary gives one. If a preferred term is missing or unclear, use plain language and capture the terminology gap as an open question.
- Acronyms are spelled out the first time they appear unless the expanded form would be misleading or the term is already defined in the glossary.
- Vague architecture filler such as "robust", "seamless", "future-proof", "best practice", or "enterprise-grade" is removed unless tied to a concrete requirement, KPI, risk, cost, owner, or decision.
- Long table cells are moved into notes or the relevant section when they make ownership, scope, risks, KPIs, or decisions hard to scan.
- Open questions are written as answerable questions with an owner or target audience when known.

## Template

Use `templates/capability-overview-template.md` as the source template for generated capability overview files.
