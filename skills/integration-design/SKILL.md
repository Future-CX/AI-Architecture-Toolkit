---
name: integration-design
description: Create integration design documents for APIs, events, files, batches, messaging, orchestration, and system-to-system data flows. Use when the user asks to design, document, review, or update an integration, interface contract, integration flow, source-to-target exchange, API/event/file transfer, or operational integration behavior.
---

# Integration Design

## Quick Start

Assume the Integration Architect Agent role from `agents/integration-architect.md`: clarify producers, consumers, business triggers, interface contracts, data ownership, integration pattern, operational behavior, security, failure handling, and support ownership.

Use `templates/integration-design-template.md` as the output structure. Replace placeholders and drafting guidance with concrete content; do not leave unanswered sections unless the unknown is explicitly marked as `TBD` or an open question.

Store generated integration designs under the consuming repository's private lab root in `integrations/`.

```text
integrations/int-0001-<data-object>-from-<source>-to-<destination>.md
integrations/_integrations-overview.md
```

Each integration filename must start with `int-`, then a 4-digit sequence number, then the canonical data object, source, and destination:

```text
int-0001-order-from-commerce-to-erp.md
int-0002-customer-from-crm-to-commerce.md
```

Start at `int-0001`. For new files, inspect existing `integrations/int-*.md` files, choose the next available 4-digit number, and preserve gaps unless the user explicitly asks to renumber.

Do not write real-company integration details into this public toolkit repository.

## Required Inputs

- Integration name and business purpose
- Integration status, for example Proposed, In design, Approved, Implemented, or Deprecated
- Source system or producer
- Target system or consumer
- Main canonical data object
- Triggering event, process step, schedule, or user action
- Integration pattern: synchronous API, event-driven, batch, file transfer, messaging, or orchestration
- Payload, data object, schema, endpoint, topic, queue, file, or message contract
- Security, privacy, operational, and support constraints
- Failure handling, retry, idempotency, observability, and ownership expectations

## Workflow

1. Ask which capability, target architecture, solution architecture design, epic, or ADR the integration supports.
2. Ask for the source system, target system, business trigger, integration pattern, and business data involved when not already provided.
3. Read related architecture documents when paths are provided.
4. Validate terminology against `<private-lab-root>/GLOSSARY.md`. If important terms, applications, data objects, jargon, deprecated terms, or words to avoid are missing or ambiguous, use `../ubiquitous-language/SKILL.md` to update the private lab glossary before writing the design.
5. Determine the output path under `<private-lab-root>/integrations/`:
   - Create the folder if needed.
   - Scan existing files matching `int-[0-9][0-9][0-9][0-9]-*.md`.
   - Use the next available 4-digit sequence number, starting with `0001`.
   - Derive `<data-object>` from the canonical data object being exchanged.
   - Derive `<source>` from the source system or producer.
   - Derive `<destination>` from the target system or consumer.
   - Build the filename as `int-<4-digits>-<data-object>-from-<source>-to-<destination>.md`.
6. Create or update the integration design from `templates/integration-design-template.md`.
7. After writing the `## Integration Overview` description, create a visual integration diagram:
   - Use the `create-drawio-diagram` skill and its `templates/integration-design.drawio` template.
   - Create a `diagrams/` subfolder in the same folder as the integration design document.
   - Store the `.drawio` file and exported `.svg` file in that `diagrams/` subfolder.
   - Use the same basename as the integration design Markdown file. For example, `int-0001-product-from-pim-to-commerce.md`, `diagrams/int-0001-product-from-pim-to-commerce.drawio`, and `diagrams/int-0001-product-from-pim-to-commerce.svg`.
   - Populate the diagram with the integration's confirmed source, destination, intermediate components, layer placement, application headers, and connector labels.
   - Do not add separate data-contract, payload, message, or file boxes to the diagram. Capture detailed contract and payload information in the `## Contract` section instead.
   - Do not add monitoring, reconciliation, run-status, failed-record, stale-index, alerting, dashboard, or support components to the diagram. Capture those details in `## Security and Operations` instead.
   - Route connectors on clear orthogonal lanes. No connector or connector label may overlap a component, application header, layer label, arrowhead, or another connector label.
   - Use a left-biased component layout: start components near the left content margin and grow the canvas to the right as more components or connector lanes are needed.
   - Leave enough horizontal room for labeled connectors: at least 160 px between connected component edges, or 220 px for longer connector labels.
   - Treat the canvas and layer bands as flexible. If the diagram is crowded, increase canvas width or height, increase layer width or height, spread components apart, shorten connector labels, or add explicit Draw.io waypoints before exporting.
   - Export the `.drawio` file to a same-basename `.svg`.
   - Embed the `.svg` in the integration design's `## Integration Diagram` section using the relative path `diagrams/<same-basename>.svg`.
8. Populate the top context table with concise concrete values so agents can understand the integration status, purpose, source, destination, data object, trigger, pattern, and open-question count without reading the full document.
9. Populate `## Relevant Links` with every confirmed related document, including capability overview, target architecture, solution architecture design, epic, ADR, or other integration designs. Use the linked document name as the Markdown link label.
10. Update `<private-lab-root>/integrations/_integrations-overview.md` with the integration identifier, name, status, description, and count of open questions in the integration design.
11. Capture unresolved facts as open questions rather than inventing payloads, endpoints, schemas, retry rules, owners, or service-level expectations.
12. Link the integration design from the related target architecture, solution architecture design, capability overview, epic, or relevant links section when the related document exists and the user confirms the linkage. Whenever a link to the integration design is added to one of those documents, add the reciprocal link back to that document in the integration design's `## Relevant Links` section.

## Writing Guidance

- Prefer concrete interface details over generic integration principles.
- Keep the top context table short and factual. Use `TBD` for unknown fields, and mirror unresolved items in `## Open Questions`.
- Identify producer, consumer, owner, protocol, contract, trigger, frequency, payload, and versioning.
- Call out source-of-truth and canonical data object ownership.
- Document idempotency, retries, ordering, dead-letter behavior, replay, timeout, and compensation where relevant.
- Include observability details: logs, metrics, traces, alerts, dashboards, correlation IDs, and support ownership.
- Include security details: authentication, authorization, identity propagation, encryption, secrets, network trust boundary, audit logging, and data classification.
- Include an editable Draw.io integration diagram and a rendered same-basename SVG in every integration design. Store both files in a `diagrams/` subfolder next to the integration design. The diagram should visually summarize the integration after the `## Integration Overview` section, not replace the contract, quality, security, or operations detail.
- Visually inspect the rendered SVG before embedding. If connectors or connector labels overlap components, headers, labels, or arrowheads, if connectors cross through components, if labeled connectors are cramped, or if the diagram is unnecessarily centered with large unused left-side whitespace, revise the `.drawio` layout and export again.
- Keep relevant links bidirectional: if the integration design is linked from a target architecture, solution architecture design, or capability overview, also link that document from the integration design.
- Use linked document names as relevant-link labels. For local Markdown files, derive the name from the first `#` heading; otherwise use the filename without extension. Do not use generic labels such as "Target architecture" when a document title is available.
- Maintain `integrations/_integrations-overview.md` every time an integration design is created or updated. The overview must list each integration file with its identifier, integration name, status, description, and count of open questions.
- Mark unknown contract details as `TBD` or open questions.

## Integrations Overview

Maintain `<private-lab-root>/integrations/_integrations-overview.md` with this structure:

```md
# Integrations Overview

| Identifier                     | Integration                                                                                           | Status                 | Description                 | Open Questions            |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | ---------------------- | --------------------------- | ------------------------: |
| {{INTEGRATION_IDENTIFIER}}     | [{{INTEGRATION_NAME}}](int-0001-{{DATA_OBJECT_SLUG}}-from-{{SOURCE_SLUG}}-to-{{DESTINATION_SLUG}}.md) | {{INTEGRATION_STATUS}} | {{INTEGRATION_DESCRIPTION}} | {{OPEN_QUESTIONS_COUNT}} |
```

When updating the overview:

- Scan `integrations/int-*.md` so the overview represents every integration design file.
- Use the `int-0001` prefix from each integration filename as the identifier.
- Use the integration document title or integration name as the link label.
- Use the `Status` value from the integration design's top context table. Use `TBD` when the field is absent or unknown.
- Use the integration overview/purpose as the description.
- Count Markdown bullets in each integration document's `## Open Questions` section. Use `0` when the section is absent, empty, or explicitly says there are no open questions.
- Keep rows sorted by integration number.
- Do not include `_integrations-overview.md` as an integration row.

## Guardrails

- Keep real-company integration designs in a private company lab repository.
- Write integration design files to `<private-lab-root>/integrations/`, not inside this public toolkit repository.
- Always update `<private-lab-root>/integrations/_integrations-overview.md` after creating or updating an integration design.
- Do not renumber existing `int-` files unless the user explicitly asks.
- Do not invent internal system names, endpoints, payload fields, credentials, keys, vendor-specific configuration, or non-public business context.
- Use canonical glossary terms for business data objects and applications whenever possible.
