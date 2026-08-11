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

Use the matching template in `templates/` for each generated section file. Use `templates/00-target-architecture-document-template.md` only for the summary and navigation document.

Every generated section file and the summary document must keep the top metadata table from its template. Replace every `{{PLACEHOLDER}}` and every drafting instruction with final, document-specific content; do not leave template guidance in generated artifacts. In particular, replace `{{CONFLUENCE_LINK}}`, `{{LAST_UPDATE}}`, and `{{OPEN_QUESTIONS_COUNT}}` with document-specific values. Leave `Readability Score` as `TBD` unless a readability check has actually been run.

Readability guideline: write for business stakeholders first. Aim for a readability score of `40+` for management summaries and section introductions, and `30+` for the remaining body content. Prefer short sentences, concrete nouns, active voice, and plain-language trade-offs. Keep specialist terms only where they affect decisions, risk, cost, ownership, timeline, or support model, and explain them on first use.

Store generated target architecture documents under the private company lab root at `solution-architectures/L1-target-architecture-<slug>/`.

When this toolkit is used as a submodule, do not write generated target architecture documents under `toolkit/solution-architectures/` or inside this public toolkit repository. Run from the private company lab root, or otherwise target the private lab root explicitly, so output goes to `<private-lab-root>/solution-architectures/`.

Use one file per major workflow section, plus one stakeholder-facing summary and navigation document:

```text
solution-architectures/<slug>/
├── 01-preliminary-phase.md
├── 02-capability-overview.md
├── diagrams/
│   ├── capability-map.drawio
│   └── capability-map.svg
├── 03-phase-a-architecture-vision.md
├── 04-phase-b-business-architecture.md
├── 05-phase-c-application-architecture.md
├── 06-phase-c-data-architecture.md
├── 07-phase-d-technology-architecture.md
├── 08-phase-e-solution-building-blocks.md
├── 09-gap-analysis.md
├── 10-roadmap-themes.md
├── 11-governance-actions.md
├── 12-risks-and-open-questions.md
└── 00-target-architecture-document.md
```

Store every Draw.io source and same-basename export created for a target architecture document under `solution-architectures/<slug>/diagrams/`. Do not place target architecture diagram files beside the numbered Markdown documents.

## Required Inputs

- Enterprise and organizational context
- Architecture capability, maturity, framework, governance, standards, roles, and reusable assets
- Rationale and scope for the target architecture initiative
- Capabilities to include
- Company mission and vision, strategic drivers, objectives, product vision, and business outcomes
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
5. Create the `solution-architectures/<slug>/` folder if needed. Create its `diagrams/` subfolder before generating any target architecture diagram.
6. For every section below, update `<private-lab-root>/GLOSSARY.md` before or alongside the section when the section introduces or changes:
   - Domain terms and aliases
   - Jargon, deprecated terms, or words to avoid, captured in the glossary `## Jargon` section
   - Applications and the capabilities or functions they deliver
   - General canonical data objects, ownership, source-of-truth, and lifecycle notes
   - Relationships between terms, applications, and data objects
7. Do not overwrite an existing section file or summary document unless the user explicitly asks.
8. Create `01-preliminary-phase.md` from `templates/01-preliminary-phase-template.md` using Preliminary Phase input to establish architecture context:

- Introduction explaining how enterprise architecture is organized and governed
- Enterprise and organizational context - Establishes where architecture operates organizationally
- Architecture capability and maturity - Defines where and how enterprise architecture is practiced
- Architecture framework and method - Describes the chosen framework and methodological approach
- Architecture principles and standards - Establishes reusable rules and constraints
- Governance model and decision rights - Defines architecture decision rights and governance mechanisms
- Architecture roles and decision forums - Establishes the standing architecture organization
- Integration with portfolio, delivery, risk, and other governance
- Architecture repository, tools, and reusable assets - Establishes the shared architecture knowledge base

9. Create `02-capability-overview.md` from `templates/02-capability-overview-template.md` with a high-level overview for each included capability:
   - Before the capability table, create `diagrams/capability-map.drawio` with `../create-drawio-diagram/SKILL.md` using `../create-drawio-diagram/templates/capability-map.drawio`
   - Place every included layered capability exactly once in its confirmed horizontal layer: Channel, Engagement Services, Integration, or Enterprise Foundation
   - Use at most eight capabilities per row in each layer; when a layer needs multiple rows, use the minimum number of rows and distribute its capabilities evenly according to the Capability Map layout rules in `../create-drawio-diagram/SKILL.md`
   - Preserve the three cross-cutting columns to the right of the horizontal layers: UI Design and Testing; Observability (Logging, Monitoring & Alerting); DevOps; do not duplicate these as nodes inside a horizontal layer
   - Start with the typical cross-cutting capabilities defined by the Capability Map layout in `../create-drawio-diagram/SKILL.md`, then keep, replace, remove, or add nodes based on confirmed target architecture input; do not present unconfirmed starter capabilities as enterprise facts
   - Keep capability names identical across the diagram, capability table, glossary, and linked capability documents
   - Export `diagrams/capability-map.drawio` to `diagrams/capability-map.svg`, inspect the SVG using the `create-drawio-diagram` export rules, embed the SVG under `## Capability Map`, and link the editable Draw.io source from the same `diagrams/` subfolder
   - If a capability's layer is unknown or disputed, record it as an open question and resolve it instead of guessing
   - Capability name linked to the matching capability overview document when one exists under `<private-lab-root>/capabilities/<capability-slug>/<capability-slug>.md`; otherwise use an explicit placeholder such as `TBD` or mark it as an open question instead of inventing a path
   - Definition
   - Business outcome
   - Scope boundary
   - Key stakeholders
   - Current-state pain points
   - Target-state direction
   - Application, data, integration, and technology implications
   - Dependencies, risks, and roadmap considerations
10. Create `03-phase-a-architecture-vision.md` from `templates/03-phase-a-architecture-vision-template.md` using Phase A input:

- Introduction explaining why this target architecture is needed now - Explains the purpose and value of this architecture initiative
- Company mission and vision - Provides strategic context for the proposed change
- Strategic drivers
- Objectives
- Product vision - Describes the intended future product or service experience
- Business outcomes
- Stakeholders, concerns, and key requirements - Identifies who is affected by this architecture and what matters to them
- Architecture initiative scope and exclusions - Defines what this specific ADM cycle includes and excludes
- Value streams or major scenarios
- High-level baseline and target vision - Communicates the proposed change at vision level
- Assumptions, constraints, dependencies, and risks
- Transformation readiness
- Success measures - Supports approval of the architecture work
- Approval and Statement of Architecture Work

11. Create `04-phase-b-business-architecture.md` from `templates/04-phase-b-business-architecture-template.md` using Phase B input:

- Capability map
- Organization impacts
- Business processes
- Operating model changes
- Business risks and dependencies

12. Create `05-phase-c-application-architecture.md` from `templates/05-phase-c-application-architecture-template.md` using Phase C input:

- Application landscape
- Application responsibilities and boundaries
- Channels and frontends
- Engagement services
- Commerce services
- Enterprise applications
- Application interactions
- APIs and integration patterns
- Reuse and application rationalization
- Application gaps, dependencies, and risks
- Detailed Ecommerce Solution Blueprint

13. Create `06-phase-c-data-architecture.md` from `templates/06-phase-c-data-architecture-template.md` using Phase C input:

- Data domains
- Data ownership
- Systems of record
- Master and reference data
- Customer identity and 360-degree customer view
- Product, customer, order, and interaction data
- Data flows and synchronization
- Data quality, privacy, and retention
- Analytics and data activation
- Data gaps, dependencies, and risks
- Linked data architecture designs for specific canonical data objects, left as `_No linked data architecture designs yet._` until the user explicitly creates them with `../data-architecture-design/SKILL.md`

14. Create `07-phase-d-technology-architecture.md` from `templates/07-phase-d-technology-architecture-template.md` using Phase D input:

- Platforms, infrastructure, security, observability, and operations
- Technology standards and constraints
- Technology lifecycle concerns

15. Create `08-phase-e-solution-building-blocks.md` from `templates/08-phase-e-solution-building-blocks-template.md` using Phase E input:

- Related capabilities and architecture trace references
- Delivery dependencies and sequencing notes
- Epics to build, left as `_No linked epics yet._` until the user explicitly creates epics with `../to-epics/SKILL.md`

16. Create `09-gap-analysis.md`, `10-roadmap-themes.md`, `11-governance-actions.md`, and `12-risks-and-open-questions.md` from their matching templates.
17. Before creating the summary document, review the generated section files against `<private-lab-root>/GLOSSARY.md` and add any missing terms, applications, data objects, and relationships discovered during drafting.
18. Create `00-target-architecture-document.md` from `templates/00-target-architecture-document-template.md` as the summary and navigation document.
19. Begin `00-target-architecture-document.md` with its title and a one-sentence document purpose directly below it, without a purpose heading.
20. For every numbered detailed page, add the following to `00-target-architecture-document.md` in this order:
    - The detailed page title
    - A one-sentence purpose directly below the title, with no purpose heading
    - A `Management Summary` copied verbatim from that detailed page's `Introduction`; do not paraphrase, shorten, or otherwise rewrite it
    - A link to the detailed page
21. Keep every detailed page's `Introduction` concise and suitable for management readers because it is also the source text for the summary document. Keep detailed analysis, tables, and implementation detail in the numbered section files.
22. Keep the section files as the detailed reviewable artifacts. The `00-target-architecture-document.md` file is the stakeholder-facing overview with links to those detailed sections.
23. Leave the Phase E `Epics To Build` table empty until the user explicitly creates epics with `../to-epics/SKILL.md`. Generated epic files belong under `<private-lab-root>/requirements/<name-of-target-architecture>/`, not under the target architecture folder. Do not infer or create epics during target architecture drafting. Every epic requires a user-provided main capability.
24. Leave the Phase C `Data Architecture Designs` table empty until the user explicitly creates data architecture designs with `../data-architecture-design/SKILL.md`. Generated data architecture design files belong under `<private-lab-root>/data-architectures/<data-object-slug>/`, not under the target architecture folder.

## Guardrails

- Keep this public toolkit free of company-confidential information, customer names, internal system names, credentials, and non-public business context.
- If using real company details, work in a private company lab repository and write outputs to that repository's `solution-architectures/` folder.
- Do not invent specific enterprise facts. Mark unknowns as assumptions or open questions.
- Prefer generic capability names unless the user is working in a private repository.
- Do not create data architecture design documents automatically. Data architecture designs require an explicit target architecture link and canonical data object through the `data-architecture-design` skill.
- Do not create epics automatically. Epics require explicit user-provided names, descriptions, and main capabilities through the `to-epics` skill.
