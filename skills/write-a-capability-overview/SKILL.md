---
name: write-a-capability-overview
description: Write business capability overview documents from a standard template and store them under the root capabilities folder. Use when the user asks to create, draft, document, or assess a business capability, capability overview, capability map entry, or capability definition.
---

# Write A Capability Overview

## Quick Start

Write capability overview documents under the consuming repository's root `capabilities/` folder using the preset template in `templates/capability-overview-template.md`.

When this toolkit is used as a submodule, do not write generated capability files under `toolkit/capabilities/`. Run the command from the private repository root, or pass `--output-root <private-repo-root>`, so output goes to `<private-repo-root>/capabilities/`.

Use the helper script when the requested capability has clear input values:

```sh
python3 skills/write-a-capability-overview/scripts/write-capability-overview.py "Order Management" \
  --domain "Commerce" \
  --business-objective "Improve order accuracy, lifecycle visibility, and fulfillment coordination." \
  --stakeholder "Customer service" \
  --stakeholder "Operations" \
  --existing-system "ERP" \
  --strategic-importance "High" \
  --pain-point "Order status is fragmented across systems." \
  --related-capability "Inventory Management"
```

This creates `capabilities/order-management.md`.

If the requested name includes a redundant leading or trailing word `Capability`, remove it from the generated filename. For example, `Search Capability` and `Capability Search` both create `capabilities/search.md`.

Each generated capability must also be added to `capabilities/_capability-list.md` using a markdown table with `name`, `description`, and `last_updated` columns. Create `_capability-list.md` when it does not exist. Keep rows sorted alphabetically by capability name.

When running from a private lab repo that contains this toolkit as a submodule:

```sh
python3 toolkit/skills/write-a-capability-overview/scripts/write-capability-overview.py "Order Management" \
  --domain "Commerce" \
  --business-objective "Improve order accuracy, lifecycle visibility, and fulfillment coordination." \
  --stakeholder "Customer service" \
  --existing-system "ERP" \
  --strategic-importance "High" \
  --pain-point "Order status is fragmented across systems." \
  --related-capability "Inventory Management"
```

Run from the private lab root, this creates `capabilities/order-management.md` beside `toolkit/`.

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

1. Gather the required inputs.
2. Convert the capability name to `<workspace-root>/capabilities/<slug>.md`, removing a redundant leading or trailing word `Capability` from the slug.
3. Derive the outputs from the inputs and any available repository context.
4. Use `templates/capability-overview-template.md` as the output structure.
5. Do not overwrite an existing capability file unless the user explicitly asks.
6. Add or update the generated capability in `<workspace-root>/capabilities/_capability-list.md` with a relative link, description, and `last_updated` date.
7. If the toolkit is mounted as `toolkit/` in a private lab repo, write the generated capability overview to the private lab root, not to `toolkit/capabilities/`.
8. Keep company-confidential details out of the public toolkit repository; use a private company lab repo for real company content.

## Required Outputs

Each capability overview must include:

- Capability definition
- Business outcome
- Scope
- Inputs/outputs
- Actors
- Processes supported
- Applications involved
- Application lifecycle management
- Data involved
- Integrations
- KPIs
- NFR considerations
- Risks
- Maturity assessment
- Future-state considerations

## Template

Use `templates/capability-overview-template.md` as the source template for generated capability overview files.
