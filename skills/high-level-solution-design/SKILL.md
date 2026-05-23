---
name: high-level-solution-design
description: Write high-level solution design documents from an existing capability overview, covering implementation design, applications, data model, integrations, diagrams, NFRs, and technical design choices. Use when the user asks to create, draft, or update a high-level solution design, capability architecture document, technical capability design, implementation architecture, or detailed technical design for a business capability.
---

# High-Level Solution Design

## Quick Start

Assume the Solution Architect Agent role from `agents/solution-architect.md`: translate business needs into coherent application, data, integration, security, operational architecture, and implementation trade-offs.

Write high-level solution design documents from an existing capability overview under the consuming repository's root `solution-architectures/<slug>/` folder.

Read the source overview first from `capabilities/<capability-slug>/<capability-slug>.md`. Store the generated technical document as `solution-architectures/<slug>/<slug>-architecture.md`, where `<slug>` is derived from the high-level solution design document name.

Before creating any output files, run a `grill-me` style clarification session using `../grill-me/SKILL.md`. Ask one question at a time until the capability boundary, source overview, systems, data, integrations, constraints, assumptions, terminology, and desired technical depth are clear enough to avoid avoidable misunderstanding.

During that clarification session, use `../ubiquitous-language/SKILL.md` whenever terms are vague, overloaded, conflicting, or important enough to become shared domain language. Create or update `<private-lab-root>/GLOSSARY.md` inline as terms are clarified; do not batch glossary updates until the end. Do not write the glossary inside this public toolkit repository when working with real company context.

After the clarification session, validate that `<private-lab-root>/GLOSSARY.md` was created or updated during the current run. If it was not created or updated, stop before generating high-level solution design files and ask the user to run the `grill-me` skill followed by the `ubiquitous-language` skill so the glossary is updated first.

When this toolkit is used as a submodule, do not write generated high-level solution design files under `toolkit/solution-architectures/`. Run from the private lab root, or otherwise target the private lab root explicitly, so output goes to `<private-lab-root>/solution-architectures/L2-solution-design-<slug>/`.

Use `templates/high-level-solution-design-template.md` as the output structure. When Mermaid diagrams are created, store each diagram as a separate `.mmd` file in the same folder as the high-level solution design document and reference those files from the document.

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
5. Derive the output path as `solution-architectures/<slug>/<slug>-architecture.md`, where `<slug>` is derived from the high-level solution design document name.
6. Do not overwrite an existing high-level solution design document unless the user explicitly asks.
7. Extract the business objective, scope, applications, data involved, integrations, NFRs, risks, and future-state considerations from the capability overview.
8. Use repository context where available to validate stated systems, integrations, standards, and existing design decisions.
9. Update `<private-lab-root>/GLOSSARY.md` before or alongside drafting when the document introduces or changes:
   - Domain terms and aliases
   - Applications and the capabilities or functions they deliver
   - General canonical data objects, ownership, source-of-truth, and lifecycle notes
   - Relationships between terms, applications, and data objects
10. Create the technical document from `templates/high-level-solution-design-template.md`.
11. Create separate Mermaid files in the same output folder when the required architecture relationships are known:
    - `capability-context.mmd` for the capability context diagram
    - `application-component-view.mmd` for the application/component diagram
    - `conceptual-data-model.mmd` for the data model or conceptual entity relationship diagram
    - `integration-flow.mmd` for the integration flow or sequence diagram
12. Reference each created `.mmd` file from the `## Diagrams` section of `<slug>-architecture.md`. Do not inline Mermaid diagram code in the design document unless the user explicitly asks for inline diagrams.
13. Do not create placeholder `.mmd` files for unknown diagrams. Mark missing diagrams as assumptions or open questions in the design document.
14. Record specific technical design choices in the document. If a choice is durable, hard to reverse, surprising without context, and based on a real trade-off, propose an ADR using `../architecture-decision-record/SKILL.md`.
15. Mark unknowns as assumptions or open questions. Do not invent implementation facts.

## Required Outputs

Each high-level solution design document must include:

- High-level solution design summary
- Source capability overview reference
- Scope and assumptions
- Target technical implementation
- Application and component architecture
- Data model and data ownership
- Data integrations and interface contracts
- Mermaid diagram files in the same folder as the design document, referenced from the document, where enough detail is known
- Security, privacy, and compliance design
- NFR and operational design
- Technical design choices and trade-offs
- Risks, dependencies, migration notes, and open questions

## Guardrails

- Keep this public toolkit free of company-confidential information, customer names, internal system names, credentials, and non-public business context.
- If using real company details, work in a private company lab repository and write outputs to that repository's `solution-architectures/` folder.
- Keep data objects general and canonical. Do not create application-specific data objects such as API resources, tables, or vendor object names.
- Prefer diagrams and tables that clarify implementation decisions; avoid decorative diagrams.
