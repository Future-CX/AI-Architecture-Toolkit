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
7. Populate the top context table with concise concrete values so agents can understand the integration status, purpose, source, destination, data object, trigger, pattern, and open-question count without reading the full document.
8. Populate `## Relevant Links` with every confirmed related document, including capability overview, target architecture, solution architecture design, epic, ADR, or other integration designs. Use the linked document name as the Markdown link label.
9. Update `<private-lab-root>/integrations/_integrations-overview.md` with the integration name, status, description, and count of open questions in the integration design.
10. Capture unresolved facts as open questions rather than inventing payloads, endpoints, schemas, retry rules, owners, or service-level expectations.
11. Link the integration design from the related target architecture, solution architecture design, capability overview, epic, or relevant links section when the related document exists and the user confirms the linkage. Whenever a link to the integration design is added to one of those documents, add the reciprocal link back to that document in the integration design's `## Relevant Links` section.

## Writing Guidance

- Prefer concrete interface details over generic integration principles.
- Keep the top context table short and factual. Use `TBD` for unknown fields, and mirror unresolved items in `## Open Questions`.
- Identify producer, consumer, owner, protocol, contract, trigger, frequency, payload, and versioning.
- Call out source-of-truth and canonical data object ownership.
- Document idempotency, retries, ordering, dead-letter behavior, replay, timeout, and compensation where relevant.
- Include observability details: logs, metrics, traces, alerts, dashboards, correlation IDs, and support runbooks.
- Include security details: authentication, authorization, identity propagation, encryption, secrets, network trust boundary, audit logging, and data classification.
- Keep relevant links bidirectional: if the integration design is linked from a target architecture, solution architecture design, or capability overview, also link that document from the integration design.
- Use linked document names as relevant-link labels. For local Markdown files, derive the name from the first `#` heading; otherwise use the filename without extension. Do not use generic labels such as "Target architecture" when a document title is available.
- Maintain `integrations/_integrations-overview.md` every time an integration design is created or updated. The overview must list each integration file with its integration name, status, description, and count of open questions.
- Mark unknown contract details as `TBD` or open questions.

## Integrations Overview

Maintain `<private-lab-root>/integrations/_integrations-overview.md` with this structure:

```md
# Integrations Overview

| Integration                                                                                           | Status                 | Description                 | Open Questions            |
| ----------------------------------------------------------------------------------------------------- | ---------------------- | --------------------------- | ------------------------: |
| [{{INTEGRATION_NAME}}](int-0001-{{DATA_OBJECT_SLUG}}-from-{{SOURCE_SLUG}}-to-{{DESTINATION_SLUG}}.md) | {{INTEGRATION_STATUS}} | {{INTEGRATION_DESCRIPTION}} | {{OPEN_QUESTIONS_COUNT}} |
```

When updating the overview:

- Scan `integrations/int-*.md` so the overview represents every integration design file.
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
