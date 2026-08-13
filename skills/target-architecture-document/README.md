# Target Architecture Document

Write target architecture documents that connect business capabilities to strategy, target architecture, applications, data, integration, technology direction, and epics to build.

Generated documents belong under the private company lab root at `solution-architectures/<slug>/`, with numbered detailed section files and a summary `00-target-architecture-document.md` that links to them. Each summary entry contains the detailed page title, a one-sentence purpose, a management summary copied verbatim from the detailed page's introduction, and the detailed page link.

The Capability Overview presents each included capability under a level-three heading, followed by its definition, business outcome, scope boundary, and target-state direction. Definitions, outcomes, and target-state directions use plain English for non-technical readers rather than a wide table or implementation-heavy language. A horizontal divider separates consecutive capability blocks.

Before any files are created, the workflow must run a `grill-me` style clarification session and update the private lab root `GLOSSARY.md` with `ubiquitous-language` as terms are clarified. If `GLOSSARY.md` was not created or updated afterwards, stop and ask the user to run `grill-me` followed by `ubiquitous-language`.

While target architecture section files are created or updated, the workflow must keep `GLOSSARY.md` current with any newly introduced or changed domain terms, applications, data objects, and relationships.

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

All target architecture Draw.io sources and same-basename exports belong under `solution-architectures/<slug>/diagrams/`.

- [SKILL.md](SKILL.md)
- Epics are listed in Phase E and created under `requirements/<name-of-target-architecture>/` with [To Epics](../to-epics/SKILL.md) only after the user provides an epic name, description, and main capability.

### Templates

- [Preliminary phase template](templates/01-preliminary-phase-template.md)
- [Capability overview template](templates/02-capability-overview-template.md)
- [Phase A architecture vision template](templates/03-phase-a-architecture-vision-template.md)
- [Phase B business architecture template](templates/04-phase-b-business-architecture-template.md)
- [Phase C application architecture template](templates/05-phase-c-application-architecture-template.md)
- [Phase C data architecture template](templates/06-phase-c-data-architecture-template.md)
- [Phase D technology architecture template](templates/07-phase-d-technology-architecture-template.md)
- [Phase E epics template](templates/08-phase-e-solution-building-blocks-template.md)
- [Gap analysis template](templates/09-gap-analysis-template.md)
- [Roadmap themes template](templates/10-roadmap-themes-template.md)
- [Governance actions template](templates/11-governance-actions-template.md)
- [Risks and open questions template](templates/12-risks-and-open-questions-template.md)
- [Target architecture document template](templates/00-target-architecture-document-template.md)
