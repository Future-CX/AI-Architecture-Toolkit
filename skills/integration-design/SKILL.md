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
integrations/INT-0001-<integration-slug>.md
integrations/_integrations-overview.md
```

Each integration filename must start with `INT-`, then a 4-digit sequence number, then a slug:

```text
INT-0001-order-submitted-event.md
INT-0002-customer-profile-api.md
```

Start at `INT-0001`. For new files, inspect existing `integrations/INT-*.md` files, choose the next available 4-digit number, and preserve gaps unless the user explicitly asks to renumber.

Do not write real-company integration details into this public toolkit repository.

## Required Inputs

- Integration name and business purpose
- Source system or producer
- Target system or consumer
- Triggering event, process step, schedule, or user action
- Integration pattern: synchronous API, event-driven, batch, file transfer, messaging, or orchestration
- Payload, data object, schema, endpoint, topic, queue, file, or message contract
- Security, privacy, operational, and support constraints
- Failure handling, retry, idempotency, observability, and ownership expectations

## Workflow

1. Ask which capability, target architecture, high-level solution design, epic, or ADR the integration supports.
2. Ask for the source system, target system, business trigger, integration pattern, and business data involved when not already provided.
3. Read related architecture documents when paths are provided.
4. Validate terminology against `<private-lab-root>/GLOSSARY.md`. If important terms, applications, or data objects are missing or ambiguous, use `../ubiquitous-language/SKILL.md` to update the private lab glossary before writing the design.
5. Determine the output path under `<private-lab-root>/integrations/`:
   - Create the folder if needed.
   - Scan existing files matching `INT-[0-9][0-9][0-9][0-9]-*.md`.
   - Use the next available 4-digit sequence number, starting with `0001`.
   - Derive `<integration-slug>` from the integration name.
6. Create or update the integration design from `templates/integration-design-template.md`.
7. Populate `## Relevant Links` with every confirmed related document, including capability overview, target architecture, high-level solution design, epic, ADR, or other integration designs. Use the linked document name as the Markdown link label.
8. Update `<private-lab-root>/integrations/_integrations-overview.md` with the integration name and description.
9. Capture unresolved facts as open questions rather than inventing payloads, endpoints, schemas, retry rules, owners, or service-level expectations.
10. Link the integration design from the related target architecture, high-level solution design, capability overview, epic, or relevant links section when the related document exists and the user confirms the linkage. Whenever a link to the integration design is added to one of those documents, add the reciprocal link back to that document in the integration design's `## Relevant Links` section.

## Writing Guidance

- Prefer concrete interface details over generic integration principles.
- Identify producer, consumer, owner, protocol, contract, trigger, frequency, payload, and versioning.
- Call out source-of-truth and canonical data object ownership.
- Document idempotency, retries, ordering, dead-letter behavior, replay, timeout, and compensation where relevant.
- Include observability details: logs, metrics, traces, alerts, dashboards, correlation IDs, and support runbooks.
- Include security details: authentication, authorization, identity propagation, encryption, secrets, network trust boundary, audit logging, and data classification.
- Keep relevant links bidirectional: if the integration design is linked from a target architecture, high-level solution design, or capability overview, also link that document from the integration design.
- Use linked document names as relevant-link labels. For local Markdown files, derive the name from the first `#` heading; otherwise use the filename without extension. Do not use generic labels such as "Target architecture" when a document title is available.
- Maintain `integrations/_integrations-overview.md` every time an integration design is created or updated. The overview must list each integration file with its integration name and description.
- Mark unknown contract details as `TBD` or open questions.

## Integrations Overview

Maintain `<private-lab-root>/integrations/_integrations-overview.md` with this structure:

```md
# Integrations Overview

| Integration | Description |
| --- | --- |
| [{{INTEGRATION_NAME}}](INT-0001-{{INTEGRATION_SLUG}}.md) | {{INTEGRATION_DESCRIPTION}} |
```

When updating the overview:

- Scan `integrations/INT-*.md` so the overview represents every integration design file.
- Use the integration document title or integration name as the link label.
- Use the integration overview/purpose as the description.
- Keep rows sorted by integration number.
- Do not include `_integrations-overview.md` as an integration row.

## Guardrails

- Keep real-company integration designs in a private company lab repository.
- Write integration design files to `<private-lab-root>/integrations/`, not inside this public toolkit repository.
- Always update `<private-lab-root>/integrations/_integrations-overview.md` after creating or updating an integration design.
- Do not renumber existing `INT-` files unless the user explicitly asks.
- Do not invent internal system names, endpoints, payload fields, credentials, keys, vendor-specific configuration, or non-public business context.
- Use canonical glossary terms for business data objects and applications whenever possible.
