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

Use `templates/solution-architecture-design-template.md` as the output structure and follow the chapter writing guidance below when replacing placeholders. Replace each complete placeholder block with finished document content; do not leave placeholder names, placeholder guidance, or drafting instructions in the generated document. Create every Draw.io diagram with `../create-drawio-diagram/SKILL.md` because it contains the required diagram instructions, style rules, and templates. Store each diagram as an editable `.drawio` file in the same folder as the solution architecture design document. Export a same-basename `.svg` file for every `.drawio` file that must be embedded, embed the SVG in the document, and link the `.drawio` source near the embedded SVG.

## Required Inputs

- Source capability overview path
- Capability name and scope boundary
- Applications and technical components involved
- Data objects, ownership, lifecycle, and persistence needs
- Data integrations, APIs, events, files, batches, and upstream/downstream dependencies
- Non-functional requirements, security, privacy, observability, resilience, and operations constraints
- Technical standards, technology choices, assumptions, risks, and open decisions

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
   - Applications and the capabilities or functions they deliver
   - General canonical data objects, ownership, source-of-truth, and lifecycle notes
   - Relationships between terms, applications, and data objects
10. Create the technical document from `templates/solution-architecture-design-template.md`.
11. Use `../create-drawio-diagram/SKILL.md` to create separate Draw.io source files in the same output folder when the required architecture relationships are known:
    - `capability-context.drawio` for the capability context diagram
    - `application-component-view.drawio` for the application/component diagram
    - `conceptual-data-model.drawio` for the data model or conceptual entity relationship diagram
    - `integration-flow.drawio` for the integration flow or sequence diagram
12. Export a same-basename SVG for each created Draw.io file in the same output folder:
    - `capability-context.svg`
    - `application-component-view.svg`
    - `conceptual-data-model.svg`
    - `integration-flow.svg`
13. Embed each created `.svg` file in the `## Diagrams` section of `<slug>-architecture.md` using Markdown image syntax, and include a nearby source link to the matching `.drawio` file.
14. Do not create placeholder `.drawio` or `.svg` files for unknown diagrams. Mark missing diagrams as assumptions or open questions in the design document.
15. Record specific technical design choices in the document. If a choice is durable, hard to reverse, surprising without context, and based on a real trade-off, propose an ADR using `../architecture-decision-record/SKILL.md`.
16. Mark unknowns as assumptions or open questions. Do not invent implementation facts.
17. Use linked document titles as Markdown link labels whenever possible. For local Markdown files such as source capability overviews and target architecture documents, derive the title from the first `#` heading; otherwise use the filename without extension. Do not use generic labels such as "Target architecture" when a document title is available.

## Chapter Writing Guidance

Write each chapter as implementation-oriented architecture guidance, not as a restatement of the capability overview. Prefer specific decisions, responsibilities, boundaries, data ownership, interfaces, constraints, and trade-offs. Use concise prose plus tables where comparison or accountability is clearer than paragraphs.

### Architecture Summary

- State the target solution in 3-6 paragraphs for senior stakeholders and delivery leads.
- Name the capability, the business outcome, the main architectural approach, the primary applications or components, and the most important constraints.
- Include the key design consequences: what changes, what stays stable, and what must be decided next.
- Do not include generic benefits or marketing language.

### Capability Overview

- Summarize only the capability context needed to understand the design.
- Link to the source capability overview and identify the source sections, assumptions, or statements used.
- Capture the capability boundary, upstream/downstream capabilities, triggering business events, and expected outcomes.
- Call out any gaps or contradictions found in the source overview.
- Do not link ADRs from this section; ADR links belong in `Technical Design Choices`.

### Scope and Assumptions

- Use clear bullet lists for in scope, out of scope, and assumptions.
- Scope should define the technical responsibility boundary for the design, not the entire business capability.
- Assumptions must be testable or reviewable. Avoid vague assumptions such as "systems will integrate correctly."
- Move unresolved facts that require a decision or answer to `Open Questions`, not assumptions.

### Target Technical Implementation

- Describe the target runtime solution: main services, applications, platforms, deployment model, environments, and operational ownership.
- Explain build-versus-buy, reuse, replacement, and modernization choices where relevant.
- Identify lifecycle flows from request or event through processing, persistence, integration, observability, and user or system outcome.
- Include important technology standards, constraints, and version or platform assumptions when known.

### Application and Component Architecture

- Identify each application, service, module, integration component, user interface, and shared platform involved.
- For each component, describe responsibility, ownership, key dependencies, and whether it is new, changed, reused, or retired.
- Make boundaries explicit: what each component owns, what it must not own, and where orchestration or business rules live.
- Use a table when there are multiple components.

### Data Model and Ownership

- Define canonical business data objects, their meaning, owner or source of truth, lifecycle, and consumers.
- Keep data objects business-level and general. Do not use vendor object names, table names, endpoint resources, or application-specific object names as canonical data objects.
- Capture important relationships, identifiers, master/reference data, retention needs, privacy classification, and data quality responsibilities.
- State where mappings are needed between canonical objects and application-specific representations.

### Data Integrations and Interface Contracts

- Describe each interface, event, API, file, batch, stream, or manual handoff needed for the capability.
- For each integration, state producer, consumer, payload or data object, trigger, frequency, protocol or pattern, ownership, error handling, retry/idempotency needs, and observability.
- Distinguish command, query, event, synchronization, and reporting flows.
- Flag unclear interface contracts as open questions instead of inventing fields or endpoints.

### Diagrams

- Create editable `.drawio` diagrams using `../create-drawio-diagram/SKILL.md`; do not hand-roll Draw.io files outside that skill's instructions and templates.
- Embed the exported SVG for each diagram and provide a nearby link to the matching `.drawio` source file.
- Use diagrams only where they clarify boundaries, relationships, ownership, or sequence. Do not add decorative diagrams.
- The capability context diagram should show actors, neighboring capabilities, and external dependencies.
- The application/component view should show applications, services, components, platforms, and major responsibilities.
- The conceptual data model should show canonical data objects and meaningful relationships.
- The integration flow should show direction, trigger, protocol or pattern, and important sequencing.

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

- Solution architecture design summary
- Source capability overview reference
- Scope and assumptions
- Target technical implementation
- Application and component architecture
- Data model and data ownership
- Data integrations and interface contracts
- Draw.io `.drawio` source files and exported `.svg` files in the same folder as the design document, with SVGs embedded in the document where enough detail is known
- Security, privacy, and compliance design
- NFR and operational design
- Technical design choices and trade-offs
- Risks, dependencies, migration notes, and open questions

## Guardrails

- Keep this public toolkit free of company-confidential information, customer names, internal system names, credentials, and non-public business context.
- If using real company details, work in a private company lab repository and write outputs to that repository's `solution-architectures/` folder.
- Keep data objects general and canonical. Do not create application-specific data objects such as API resources, tables, or vendor object names.
- Prefer diagrams and tables that clarify implementation decisions; avoid decorative diagrams.
