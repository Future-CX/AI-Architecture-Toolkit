---
name: solution-architecture-design
description: Write solution architecture design documents from an existing capability overview, covering implementation design, applications, data model, integrations, diagrams, NFRs, and technical design choices. Use when the user asks to create, draft, or update a solution architecture design, capability architecture document, technical capability design, implementation architecture, or detailed technical design for a business capability.
---

# Solution Architecture Design

## Quick Start

Assume the Solution Architect Agent role from `agents/solution-architect.md`: translate business needs into coherent application, data, integration, security, operational architecture, and implementation trade-offs.

Write solution architecture design documents from an existing capability overview under the consuming repository's root `solution-architectures/<slug>/` folder.

Read the source overview first from `capabilities/<capability-slug>/<capability-slug>.md`. Store the generated technical document as `solution-architectures/<slug>/<slug>-architecture.md`, where `<slug>` is derived from the solution architecture design document name.

Before creating any output files, run a `grill-me` style clarification session using `../grill-me/SKILL.md`. Ask one question at a time until the capability boundary, source overview, systems, data, integrations, constraints, assumptions, terminology, and desired technical depth are clear enough to avoid avoidable misunderstanding.

During that clarification session, use `../ubiquitous-language/SKILL.md` whenever terms are vague, overloaded, conflicting, or important enough to become shared domain language. Create or update `<private-lab-root>/GLOSSARY.md` inline as terms are clarified; do not batch glossary updates until the end. Do not write the glossary inside this public toolkit repository when working with real company context.

After the clarification session, validate that `<private-lab-root>/GLOSSARY.md` was created or updated during the current run. If it was not created or updated, stop before generating solution architecture design files and ask the user to run the `grill-me` skill followed by the `ubiquitous-language` skill so the glossary is updated first.

When this toolkit is used as a submodule, do not write generated solution architecture design files under `toolkit/solution-architectures/`. Run from the private lab root, or otherwise target the private lab root explicitly, so output goes to `<private-lab-root>/solution-architectures/L2-solution-architecture-<slug>/`.

Use `templates/solution-architecture-design-template.md` as the output structure and follow the chapter writing guidance below when replacing placeholders. Preserve the two opening tables: the document metadata table first, followed by the `Solution Architecture Overview` table. Do not add a table of contents. Replace each complete placeholder block with finished document content; do not leave placeholder names, placeholder guidance, or drafting instructions in the generated document. Create every Draw.io diagram with `../create-drawio-diagram/SKILL.md` because it contains the required diagram instructions, style rules, and templates. Store each diagram as an editable `.drawio` file under a `diagrams/` subfolder next to the solution architecture design document. Export every same-basename `.svg` into that `diagrams/` subfolder and embed the SVG in the document.

## Required Inputs

- Source capability overview path
- Application name
- Capability name and scope boundary
- Applications and technical components involved
- Data objects, ownership, lifecycle, and persistence needs
- Data integrations, APIs, events, files, batches, and upstream/downstream dependencies
- Non-functional requirements, security, privacy, observability, resilience, and operations constraints
- Domain, owners, technical standards, technology choices, assumptions, risks, and open decisions

## Workflow

1. Assume the Solution Architect Agent role from `agents/solution-architect.md`.
2. Start with the `grill-me` clarification session and update `<private-lab-root>/GLOSSARY.md` with `ubiquitous-language` as terminology is clarified.
3. Validate that `<private-lab-root>/GLOSSARY.md` was created or updated. If not, stop and ask the user to run `grill-me` and then `ubiquitous-language` before continuing.
4. Locate and read the source capability overview from `capabilities/<capability-slug>/<capability-slug>.md`. If multiple matches exist, ask the user which overview to use.
5. Derive the output path as `solution-architectures/<slug>/<slug>-architecture.md`, where `<slug>` is derived from the solution architecture design document name.
6. Do not overwrite an existing solution architecture design document unless the user explicitly asks.
7. Extract the business objective, scope, applications, data involved, integrations, NFRs, risks, and future-state considerations from the capability overview.
8. Use repository context where available to validate stated systems, integrations, standards, and existing design decisions.
9. Update `<private-lab-root>/GLOSSARY.md` before or alongside drafting when the document introduces or changes:
   - Domain terms and aliases
   - Jargon, deprecated terms, or words to avoid, captured in the glossary `## Jargon` section
   - Applications and the capabilities or functions they deliver
   - General canonical data objects, ownership, source-of-truth, and lifecycle notes
   - Relationships between terms, applications, and data objects
10. Create the technical document from `templates/solution-architecture-design-template.md`. Preserve the document metadata table, the `Solution Architecture Overview` table, and the `Short Summary` section.
11. Create a `diagrams/` subfolder next to `<slug>-architecture.md`, then use `../create-drawio-diagram/SKILL.md` to create separate Draw.io source files there when the required architecture relationships are known:
    - `diagrams/solution-architecture-diagram.drawio` from `../create-drawio-diagram/templates/solution-architecture-diagram.drawio` for the solution architecture diagram after `Solution Architecture Overview`
    - `diagrams/capability-overview.drawio` from `../create-drawio-diagram/templates/capability-overview.drawio` for the capability overview diagram after `Capability Overview`
    - `diagrams/integration-flow.drawio` from `../create-drawio-diagram/templates/integration-flow.drawio` for the integration flow diagram after `Data Integrations and Interface Contracts`
12. Export a same-basename SVG for each created Draw.io file into the `diagrams/` subfolder, using the SVG export rules in `../create-drawio-diagram/SKILL.md`:
    - `diagrams/solution-architecture-diagram.svg`
    - `diagrams/capability-overview.svg`
    - `diagrams/integration-flow.svg`
13. Embed each created `.svg` file inline in the relevant section of `<slug>-architecture.md` using a `diagrams/<filename>.svg` Markdown image path. Do not add a separate `Diagrams` section or links to the matching `.drawio` source files in the document.
14. Do not create placeholder `.drawio` or `.svg` files for unknown diagrams. Mark missing diagrams as assumptions or open questions in the design document.
15. Record specific technical design choices in the document. If a choice is durable, hard to reverse, surprising without context, and based on a real trade-off, propose an ADR using `../architecture-decision-record/SKILL.md`.
16. Mark unknowns as assumptions or open questions. Do not invent implementation facts.
17. Use linked document titles as Markdown link labels whenever possible. For local Markdown files such as source capability overviews and target architecture documents, derive the title from the first `#` heading; otherwise use the filename without extension. Do not use generic labels such as "Target architecture" when a document title is available.
18. In the `Solution Architecture Overview` table, link the `Capability` value to the source capability overview using `{{SOURCE_CAPABILITY_OVERVIEW}}`. Use the capability name as the link label unless the user asks to use the source document title.

## Chapter Writing Guidance

Write each chapter as implementation-oriented architecture guidance, not as a restatement of the capability overview. Prefer specific decisions, responsibilities, boundaries, data ownership, interfaces, constraints, and trade-offs. Use concise prose plus tables where comparison or accountability is clearer than paragraphs.

The generated document title must stay `L2 - {{CAPABILITY_NAME}} Solution Architecture`. The generated content should be application-centered: use `Application Name` as the primary implementation anchor in the body, while using the capability as context in the title, `Architecture Summary`, and `Capability Overview`. After that, shift the rest of the document to the application, components, data, integrations, operations, and delivery impact. Avoid repeating the capability name throughout the body unless it prevents ambiguity.

Start the document with the document metadata table, then the `Solution Architecture Overview` table with application name, capability, target architecture, domain, and owners. Place the solution architecture diagram immediately after the `Solution Architecture Overview` table when enough detail is known. Include a `Short Summary` section after that diagram reference that gives the business outcome, application focus, ownership, and main architecture concern in a few plain-language sentences.

## Readability Guidance

Make the document easy to read for both architects and delivery teams.

- Start each major section with 2-4 plain-language sentences that explain the point of the section before adding details.
- Use short paragraphs. Prefer 2-4 sentences per paragraph and avoid long blocks of text.
- Use direct language. Prefer "The order service owns order status" over "Ownership of order status is facilitated by the order service."
- Explain acronyms and specialist terms the first time they appear, unless they are already defined in `GLOSSARY.md`.
- Use bullets for lists of responsibilities, assumptions, risks, controls, and open questions.
- Use tables for repeated structures such as components, data objects, integrations, decisions, risks, and dependencies.
- Keep table cells short. Move long explanations below the table as notes.
- Put the most important conclusion first, then explain the reasoning.
- Avoid vague architecture filler such as "robust", "seamless", "future-proof", "best practice", or "enterprise-grade" unless it is tied to a concrete requirement.
- Prefer examples when a concept may be unclear, especially for data ownership, integration behavior, failure handling, and operational responsibility.
- Split complex sections with `###` subheadings when a reader would otherwise have to scan more than 6-8 bullets or several paragraphs.
- Write open questions as answerable questions with an owner or target audience when known.

### Architecture Summary

- Write for senior stakeholders first, including readers who are not deeply technical.
- State the target solution in 3-6 plain-language paragraphs.
- Start with the business outcome and what will change for the organization, customers, users, operations, or delivery teams.
- Explain the main architectural approach in business-readable terms before naming technical components.
- Name the primary applications or components only when they are important to understand ownership, impact, cost, risk, or delivery.
- Include the key design consequences: what changes, what stays stable, what risk is reduced or introduced, and what must be decided next.
- Do not include generic benefits or marketing language.
- Keep the summary readable without the rest of the document. Avoid acronyms and implementation jargon unless they are expanded and briefly explained.
- Mention the capability once as context, then focus on the application and its business impact.

### Capability Overview

- Write for senior stakeholders first, including readers who are not deeply technical.
- Summarize only the capability context needed to understand why this solution architecture exists.
- Start with the business purpose of the capability and the outcome it enables.
- Explain the capability boundary in plain language: what is included, what is not included, and why that matters.
- Describe upstream and downstream capabilities as business dependencies before naming technical systems.
- Explain triggering business events and expected outcomes using business-readable examples when helpful.
- Link to the source capability overview and identify the source sections, assumptions, or statements used.
- Call out any gaps or contradictions found in the source overview.
- Do not link ADRs from this section; ADR links belong in `Technical Design Choices`.
- Keep this section short. After this section, avoid restating the capability and focus on the application architecture.

### Scope and Assumptions

- Use clear bullet lists for in scope, out of scope, and assumptions.
- Scope should define the technical responsibility boundary for the design, not the entire business capability.
- Assumptions must be testable or reviewable. Avoid vague assumptions such as "systems will integrate correctly."
- Move unresolved facts that require a decision or answer to `Open Questions`, not assumptions.

### Target Technical Implementation

- Describe the target runtime solution around the application: main services, components, platforms, deployment model, environments, and operational ownership.
- Explain build-versus-buy, reuse, replacement, and modernization choices where relevant.
- Identify lifecycle flows from request or event through processing, persistence, integration, observability, and user or system outcome.
- Include important technology standards, constraints, and version or platform assumptions when known.

### Application and Component Architecture

- Treat this as the core of the document.
- Identify each application, service, module, integration component, user interface, and shared platform involved.
- For each component, describe responsibility, ownership, key dependencies, and whether it is new, changed, reused, or retired.
- Make boundaries explicit: what each component owns, what it must not own, and where orchestration or business rules live.
- Use a table when there are multiple components.

### Data Model and Ownership

- Do not make the solution architecture the source of truth for the canonical data model.
- Link to the relevant data architecture design when it exists. If it does not exist and the model is material, raise an open question or recommend creating one with `../data-architecture-design/SKILL.md`.
- Summarize only the canonical data objects needed to understand this application.
- Focus on how the application uses the canonical model: local persistence, read/write behavior, mappings, projections, indexes, caches, API payloads, event payloads, and application-specific representations.
- State where the application maps canonical objects to local or vendor-specific structures.
- Capture application-specific data ownership, lifecycle, privacy, quality, or retention implications without redefining the enterprise data model.

### Data Integrations and Interface Contracts

- Use the same integration summary table format as Data Architecture Design: `Integration`, `From - To`, `Pattern`, `Purpose`, and `Design`.
- Add one row per API, event, file, batch, stream, or manual handoff needed for the solution.
- Write `Integration` as a short business-readable name, such as `Audience sync to Talon.One`.
- Write `From - To` as the producer and consumer path, such as `Masif - Talon.One`, without endpoint paths, topic names, table names, or payload fields.
- Write `Pattern` as the integration pattern and cadence, such as `Scheduled morning sync`, `API lookup`, `Event publication`, `Batch file`, or `Webhook`.
- Write `Purpose` as the business or operational reason for the integration in one concise sentence.
- Write `Design` as a Markdown link to the detailed integration design when one exists. Use `No design yet` when no detailed design exists, and mirror material missing designs in `Open Questions` or `Dependencies`.
- Keep full contracts out of this table. Put payload fields, schemas, endpoint paths, retry policy, idempotency details, error handling, observability, and ownership details in linked integration designs or supporting paragraphs only when they materially affect the solution architecture.
- Distinguish command, query, event, synchronization, and reporting flows.
- Flag unclear interface contracts as open questions instead of inventing fields or endpoints.

### Visual Architecture Views

- Create editable `.drawio` files using `../create-drawio-diagram/SKILL.md`; do not hand-roll Draw.io files outside that skill's instructions and templates.
- Embed the exported SVG for each created view inline where the template places it. Do not add a separate `Diagrams` section or `.drawio` source links to the document.
- Use visual views only where they clarify boundaries, relationships, ownership, or sequence. Do not add decorative views.
- The solution architecture view must use `../create-drawio-diagram/templates/solution-architecture-diagram.drawio` and show channels, application components, integration components, data stores, external systems, and ownership boundaries.
- The capability overview view must use `../create-drawio-diagram/templates/capability-overview.drawio` and show actors, neighboring capabilities, and external dependencies while preserving the template's zone-based layout.
- The integration flow view must use `../create-drawio-diagram/templates/integration-flow.drawio` and show direction, trigger, protocol or pattern, and important sequencing.

### Security, Privacy, and Compliance

- Describe authentication, authorization, identity propagation, secrets, encryption, audit logging, data protection, consent, retention, and regulatory constraints where relevant.
- Tie controls to concrete data objects, interfaces, components, or user roles.
- Identify trust boundaries and privileged operations.
- Mark missing security or privacy decisions as open questions.

### NFR and Operational Design

- Cover availability, resilience, performance, scalability, latency, recovery, observability, support model, deployment, release, backup, monitoring, alerting, and incident response.
- Use measurable targets where known. If targets are unknown, identify the decision needed rather than inventing numbers.
- Explain failure modes and recovery behavior for critical integrations and data stores.
- Include operational ownership and handover concerns.

### Technical Design Choices

- Record meaningful choices with alternatives, rationale, trade-offs, and whether an ADR is needed or already exists.
- Link existing or newly created ADRs in this section, next to the decision they support.
- Include only choices that affect delivery, reversibility, coupling, cost, risk, operations, security, or future evolution.
- Avoid filling the table with obvious implementation facts.
- Propose an ADR when a choice is durable, hard to reverse, surprising without context, and based on a real trade-off.

### Risks, Dependencies, and Migration Notes

- Separate risks, dependencies, and migration notes clearly.
- Risks should include cause, impact, and mitigation or owner where known.
- Dependencies should identify the external decision, team, system, platform, data, vendor, or prerequisite needed.
- Migration notes should explain transition states, coexistence, cutover, rollback, data migration, compatibility, and decommissioning concerns.

### Open Questions

- Capture unresolved decisions, missing facts, and review items that block or materially influence the design.
- Each question should have an owner or target audience when known.
- Prefer concrete questions that can be answered, such as "Which system is source of truth for Product availability?".
- Do not use open questions as a place for generic next steps.

### Relevant Links

- Use linked document titles as Markdown link labels whenever possible.
- For source capability overviews and target architecture documents, read the first `#` heading and use it as the link text.
- If a title cannot be found, use the filename without extension.
- Keep extra relevant links concise and directly related to the solution design.

## Required Outputs

Each solution architecture design document must include:

- Document metadata table
- Solution Architecture Overview table with application name, capability, target architecture, domain, and owners
- Short Summary in italic text
- Solution architecture design summary
- Source capability overview reference
- Scope and assumptions
- Target technical implementation
- Application and component architecture
- Data model and data ownership
- Data integrations and interface contracts
- Draw.io `.drawio` source files and exported `.svg` files under the design document's `diagrams/` subfolder, with SVGs embedded inline where enough detail is known
- Security, privacy, and compliance design
- NFR and operational design
- Technical design choices and trade-offs
- Risks, dependencies, migration notes, and open questions

## Guardrails

- Keep this public toolkit free of company-confidential information, customer names, internal system names, credentials, and non-public business context.
- If using real company details, work in a private company lab repository and write outputs to that repository's `solution-architectures/` folder.
- Keep data objects general and canonical. Do not create application-specific data objects such as API resources, tables, or vendor object names.
- Prefer diagrams and tables that clarify implementation decisions; avoid decorative diagrams.
