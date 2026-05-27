---
name: target-architecture-document
description: Write target architecture documents that connect business capabilities to strategy, target architecture, applications, data, integration, technology direction, and epics to build. Use when the user asks to create, draft, or update a target architecture document, solution architecture document, domain architecture document, capability-aligned architecture document, or TOGAF-style Preliminary and Phase A-E architecture input.
---

# Target Architecture Document

## Quick Start

Assume the Enterprise Architect Agent role from `agents/enterprise-architect.md`: align initiatives to business capabilities, target architecture, standards, roadmaps, reuse opportunities, portfolio impact, cross-domain dependencies, and governance actions.

Ask the user which capabilities to include before drafting the target architecture document. If the user already named capabilities, confirm the list and ask for any missing domains, strategic drivers, constraints, or existing architecture inputs.

Before creating any output files, run a `grill-me` style clarification session using `../grill-me/SKILL.md`. Ask one question at a time until the request, scope, capabilities, assumptions, constraints, terminology, and desired output are clear enough to avoid avoidable misunderstanding.

During that clarification session, use `../ubiquitous-language/SKILL.md` whenever terms are vague, overloaded, conflicting, or important enough to become shared domain language. Create or update `<private-lab-root>/GLOSSARY.md` inline as terms are clarified; do not batch glossary updates until the end. Do not write the glossary inside this public toolkit repository when working with real company context.

While creating or updating target architecture section files, also update `<private-lab-root>/GLOSSARY.md` whenever the document introduces or changes domain terms, applications, or data objects. Treat glossary maintenance as part of writing each section, not as a final cleanup task. Use the glossary format and rules from `../ubiquitous-language/SKILL.md`, including the dedicated `## Applications` section and a `## Data objects` section when data objects are identified.

After the clarification session, validate that `<private-lab-root>/GLOSSARY.md` was created or updated during the current run. If it was not created or updated, stop before generating target architecture files and ask the user to run the `grill-me` skill followed by the `ubiquitous-language` skill so the glossary is updated first.

Use the matching template in `templates/` for each generated section file. Use `templates/target-architecture-document-template.md` only for the assembled final document.

Store generated target architecture documents under the private company lab root at `solution-architectures/L1-target-architecture-<slug>/`.

When this toolkit is used as a submodule, do not write generated target architecture documents under `toolkit/solution-architectures/` or inside this public toolkit repository. Run from the private company lab root, or otherwise target the private lab root explicitly, so output goes to `<private-lab-root>/solution-architectures/`.

Use one file per major workflow section, plus one assembled final document:

```text
solution-architectures/<slug>/
├── 00-index.md
├── 01-capability-overview.md
├── 02-preliminary-phase.md
├── 03-phase-a-architecture-vision.md
├── 04-phase-b-business-architecture.md
├── 05-phase-c-data-architecture.md
├── 06-phase-d-technology-architecture.md
├── 07-phase-e-solution-building-blocks.md
├── 08-gap-analysis.md
├── 09-roadmap-themes.md
├── 10-governance-actions.md
├── 11-risks-and-open-questions.md
└── target-architecture-document.md
```

## Required Inputs

- Domain or enterprise scope
- Capabilities to include
- Strategic drivers and business outcomes
- Stakeholders and governance bodies
- Current-state application, data, integration, and technology context
- Target-state direction, constraints, standards, and roadmap expectations
- Candidate delivery slices or architecture work packages
- Known risks, dependencies, and open decisions

## Workflow

1. Start with the `grill-me` clarification session and update `<private-lab-root>/GLOSSARY.md` with `ubiquitous-language` as terminology is clarified.
2. Validate that `<private-lab-root>/GLOSSARY.md` was created or updated. If not, stop and ask the user to run `grill-me` and then `ubiquitous-language` before continuing.
3. Gather and confirm the capability list from the user.
4. Determine the output folder as `<private-lab-root>/solution-architectures/<slug>/`, where `<slug>` is derived from the target architecture document name.
5. Create the `solution-architectures/<slug>/` folder if needed.
6. For every section below, update `<private-lab-root>/GLOSSARY.md` before or alongside the section when the section introduces or changes:
   - Domain terms and aliases
   - Jargon, deprecated terms, or words to avoid, captured in the glossary `## Jargon` section
   - Applications and the capabilities or functions they deliver
   - General canonical data objects, ownership, source-of-truth, and lifecycle notes
   - Relationships between terms, applications, and data objects
7. Create or update `00-index.md` from `templates/00-index-template.md` with document metadata, status, section links, and open review checkpoints.
8. Do not overwrite an existing section file or assembled document unless the user explicitly asks.
9. Create `01-capability-overview.md` from `templates/01-capability-overview-template.md` with a high-level overview for each included capability:
   - Definition
   - Business outcome
   - Scope boundary
   - Key stakeholders
   - Current-state pain points
   - Target-state direction
   - Application, data, integration, and technology implications
   - Dependencies, risks, and roadmap considerations
10. Create `02-preliminary-phase.md` from `templates/02-preliminary-phase-template.md` using Preliminary Phase input to establish architecture context:

- Enterprise scope
- Architecture principles and standards
- Governance model
- Stakeholders and decision forums
- Architecture repository or reusable assets

11. Create `03-phase-a-architecture-vision.md` from `templates/03-phase-a-architecture-vision-template.md` using Phase A input:

- Strategic drivers
- Business outcomes
- Value streams or major scenarios
- Scope, assumptions, constraints, and success measures

12. Create `04-phase-b-business-architecture.md` from `templates/04-phase-b-business-architecture-template.md` using Phase B input:

- Capability map
- Organization impacts
- Business processes
- Operating model changes
- Business risks and dependencies

13. Create `05-phase-c-data-architecture.md` from `templates/05-phase-c-data-architecture-template.md` using Phase C input:

- Application landscape
- Data domains and ownership
- Linked data architecture designs for specific canonical data objects, left as `_No linked data architecture designs yet._` until the user explicitly creates them with `../data-architecture-design/SKILL.md`
- Integration patterns
- Reuse and rationalization opportunities

14. Create `06-phase-d-technology-architecture.md` from `templates/06-phase-d-technology-architecture-template.md` using Phase D input:

- Platforms, infrastructure, security, observability, and operations
- Technology standards and constraints
- Technology lifecycle concerns

15. Create `07-phase-e-solution-building-blocks.md` from `templates/07-phase-e-solution-building-blocks-template.md` using Phase E input:

- Related capabilities and architecture trace references
- Delivery dependencies and sequencing notes
- Epics to build, left as `_No linked epics yet._` until the user explicitly creates epics with `../to-epics/SKILL.md`

16. Create `08-gap-analysis.md`, `09-roadmap-themes.md`, `10-governance-actions.md`, and `11-risks-and-open-questions.md` from their matching templates.
17. Before assembling the final document, review the generated section files against `<private-lab-root>/GLOSSARY.md` and add any missing terms, applications, data objects, and relationships discovered during drafting.
18. Assemble `target-architecture-document.md` from the section files using `templates/target-architecture-document-template.md` as the final document structure.
19. Keep the section files as reviewable working artifacts. The assembled `target-architecture-document.md` is the final consolidated artifact.
20. Leave the Phase E `Epics To Build` table empty until the user explicitly creates epics with `../to-epics/SKILL.md`. Generated epic files belong under `<private-lab-root>/requirements/<name-of-target-architecture>/`, not under the target architecture folder. Do not infer or create epics during target architecture drafting. Every epic requires a user-provided main capability.
21. Leave the Phase C `Data Architecture Designs` table empty until the user explicitly creates data architecture designs with `../data-architecture-design/SKILL.md`. Generated data architecture design files belong under `<private-lab-root>/data-architectures/<data-object-slug>/`, not under the target architecture folder.

## Guardrails

- Keep this public toolkit free of company-confidential information, customer names, internal system names, credentials, and non-public business context.
- If using real company details, work in a private company lab repository and write outputs to that repository's `solution-architectures/` folder.
- Do not invent specific enterprise facts. Mark unknowns as assumptions or open questions.
- Prefer generic capability names unless the user is working in a private repository.
- Do not create data architecture design documents automatically. Data architecture designs require an explicit target architecture link and canonical data object through the `data-architecture-design` skill.
- Do not create epics automatically. Epics require explicit user-provided names, descriptions, and main capabilities through the `to-epics` skill.
