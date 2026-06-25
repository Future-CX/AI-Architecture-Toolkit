---
name: data-architecture-design
description: Create data architecture design documents for a specific canonical data object, including data flow diagrams, integration traceability, ownership, lifecycle, quality, privacy, and governance. Use when the user asks to design, document, review, or update the architecture of a data object and link it to Target Architecture Phase C.
---

# Data Architecture Design

## Quick Start

Assume the Data Architect Agent role from `agents/data-architect.md`: clarify the canonical data object, ownership, source of truth, lifecycle, quality, privacy, retention, integration flows, and governance expectations.

Before creating or updating any data architecture design files, run a `grill-me` clarification session using `../grill-me/SKILL.md`. Ask one question at a time until the target architecture link, data object meaning, ownership, lifecycle, integrations, quality expectations, privacy concerns, assumptions, and open questions are clear enough to avoid avoidable misunderstanding.

During that clarification session, use `../ubiquitous-language/SKILL.md` whenever terms are vague, missing, overloaded, conflicting, or important enough to become shared domain language. Create or update `<private-lab-root>/GLOSSARY.md` inline as terms are clarified; do not batch glossary updates until the end.

Use `templates/data-architecture-design-template.md` as the output structure. Replace placeholders and drafting guidance with concrete content; mark unknown facts as `TBD` or open questions.

Store generated data architecture designs under the consuming repository's private lab root:

```text
data-architectures/<data-object-slug>/<data-object-slug>-data-architecture-design.md
data-architectures/<data-object-slug>/diagrams/
```

Do not write real-company data architecture details into this public toolkit repository.

## Required Inputs

- Target architecture document to link to
- Canonical data object name
- Data object description and business purpose
- Main capability or business process using the data object
- Source of truth and data owner
- Data classification
- Producing systems, consuming systems, and integration touchpoints
- Data lifecycle states, retention, privacy, and classification expectations
- Known quality rules, reconciliation needs, lineage needs, and governance constraints

## Workflow

1. Ask which target architecture document this data architecture design supports. Read it when a path is provided.
2. Start a mandatory `grill-me` clarification session using `../grill-me/SKILL.md`. Ask one question at a time and cover:
   - Canonical data object meaning and aliases
   - Business purpose and main capability
   - Source of truth, data owner, steward, allowed writers, and consumers
   - Producing systems, consuming systems, integrations, and transformations
   - Lifecycle states, retention, archival, deletion, audit, and exception handling
   - Quality rules, reconciliation, lineage, observability, and operational ownership
   - Privacy, classification, access, residency, masking, encryption, and compliance constraints
   - Assumptions, unresolved decisions, and open questions
3. During the `grill-me` session, validate terminology against `<private-lab-root>/GLOSSARY.md`. If the data object, applications, capabilities, integrations, lifecycle states, or important terms are missing or ambiguous, use `../ubiquitous-language/SKILL.md` immediately to update the private lab glossary.
4. After the clarification session, validate that `<private-lab-root>/GLOSSARY.md` was created or updated during the current run. If it was not created or updated, stop before generating data architecture files and ask the user to run `grill-me` followed by `ubiquitous-language` so the glossary is updated first.
5. Ask for the canonical data object, source of truth, owner, main capability, producers, consumers, and known integrations when still not provided.
6. Determine the output folder as `<private-lab-root>/data-architectures/<data-object-slug>/`.
7. Create or update `<data-object-slug>-data-architecture-design.md` from `templates/data-architecture-design-template.md`. Preserve the two opening tables: the document metadata table first, followed by the `Data Architecture Overview` table.
8. Create diagrams that make the data movement understandable:
   - Data flow diagram from `../create-drawio-diagram/templates/data-flow.drawio`
   - Integration map showing systems, interfaces, events, files, APIs, or batches
   - Optional conceptual data model when the object has important relationships
9. Create every Draw.io diagram with `../create-drawio-diagram/SKILL.md` because it contains the required diagram instructions, style rules, and templates. Store each editable `.drawio` source in `diagrams/`.
10. Export a same-basename `.svg` file for each Draw.io diagram that must be embedded, embed the SVG in the document, and link the `.drawio` source near the embedded SVG.
11. Link the data architecture design from Phase C of the target architecture:
   - Add it to the `## Data Architecture Designs` table in `05-phase-c-data-architecture.md` when section files exist.
   - Also update the assembled `target-architecture-document.md` when it exists.
12. Populate `## Relevant Links` with the target architecture, capability overview, solution architecture design, integration designs, ADRs, and glossary references that are explicitly related. Use linked document titles as Markdown link labels when available.
13. Capture unresolved ownership, lineage, quality, retention, privacy, integration, and operational facts as open questions rather than inventing details.

## Writing Guidance

- Center the document on one canonical data object.
- Start with the document metadata table, then the `Data Architecture Overview` table with the data object, source of truth, main capability, data owner, and classification.
- Include a `Short Summary` section before `Description` that gives the business meaning, ownership, and main architecture concern in a few plain-language sentences.
- Treat the data architecture design as the source of truth for the canonical data model. Solution architecture documents should reference this model and describe application-specific usage, not redefine it.
- Be explicit about source of truth, authoritative owner, allowed writers, and downstream consumers.
- Identify data lifecycle states, create/update/delete behavior, retention, archival, purge, and audit requirements.
- Describe data movement in business terms first, then technical integration details.
- Link related integration designs instead of duplicating full interface contracts.
- Document data quality rules, validation points, reconciliation, lineage, observability, and stewardship responsibilities.
- Include privacy and security concerns such as classification, sensitive attributes, access controls, consent, residency, masking, encryption, and audit logging.
- Keep relevant links bidirectional. If the data architecture design is linked from Target Architecture Phase C, link back to the target architecture from the data architecture design.
- Use linked document names as link labels. For local Markdown files, derive the name from the first `#` heading; otherwise use the filename without extension.
- Maintain `<private-lab-root>/GLOSSARY.md` while writing whenever the design introduces or changes domain terms, applications, canonical data objects, lifecycle states, integration names, ownership roles, relationships, jargon, deprecated terms, or words to avoid.

## Data Flow Diagram Format

Use `../create-drawio-diagram/templates/data-flow.drawio` as the starting point for the data flow diagram. The diagram should read like an operational trace of the data object across systems and process steps.

- Title the diagram `<Organization or domain> | Data Flow | <Data object>`.
- Put the business journey, process stages, screens, or major events across the top from left to right when they are known.
- Use one horizontal lane per concrete solution or component. Keep Customer first, Channel second, then Engagement solution lanes, Integration component lanes, and Enterprise Foundation or MDM solution lanes.
- Do not group several solutions into one broad lane. Add more vertical canvas space instead.
- Draw data movements as vertical or orthogonal arrows crossing lanes. Label each arrow with the specific data object, event, command, file, API call, batch, or transformation.
- Use color intentionally:
  - Blue for primary read, write, replication, or publication flows.
  - Green for enrichment, rules, calculation, validation, or decisioning flows.
  - Grey or dashed lines for optional, planned, deprecated, or uncertain flows.
- Show where the data object is created, updated, enriched, read, replicated, archived, deleted, or submitted.
- Keep lane labels stable and readable on the left. Keep each process-stage label centered over the boxes and arrows that belong to that stage.
- Prefer a wide landscape canvas over compressed diagrams. Increase the canvas width for more stages and the canvas height for more solution lanes until arrows, labels, lane headers, stage labels, and boxes do not overlap.
- Do not use a generic box-and-line context view for the data flow. The data flow diagram must show movement through lanes over time or process progression.

## Phase C Link Format

Use this table shape in Target Architecture Phase C:

```md
## Data Architecture Designs

| Data Architecture Design                                                | Data Object     | Source of Truth     | Description     |
| ----------------------------------------------------------------------- | --------------- | ------------------- | --------------- |
| [{{DATA_ARCHITECTURE_DESIGN_TITLE}}]({{DATA_ARCHITECTURE_DESIGN_LINK}}) | {{DATA_OBJECT}} | {{SOURCE_OF_TRUTH}} | {{DESCRIPTION}} |
```

## Guardrails

- Keep real-company data architecture designs in a private company lab repository.
- Write generated files to `<private-lab-root>/data-architectures/`, not inside this public toolkit repository.
- Do not create or update a data architecture design without an explicit target architecture link.
- Do not create or update a data architecture design without first running the `grill-me` clarification session and updating the private lab glossary with `ubiquitous-language` when terminology is missing or unclear.
- Do not invent internal system names, data fields, classifications, retention periods, integration contracts, or non-public business context.
- Do not overwrite existing documents or diagrams unless the user explicitly asks.
