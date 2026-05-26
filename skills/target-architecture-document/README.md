# Target Architecture Document

Write target architecture documents that connect business capabilities to strategy, target architecture, applications, data, integration, technology direction, solution building blocks, and epics to build.

Generated documents belong under the private company lab root at `solution-architectures/<slug>/`, with numbered section files and an assembled `target-architecture-document.md`.

Before any files are created, the workflow must run a `grill-me` style clarification session and update the private lab root `GLOSSARY.md` with `ubiquitous-language` as terms are clarified. If `GLOSSARY.md` was not created or updated afterwards, stop and ask the user to run `grill-me` followed by `ubiquitous-language`.

While target architecture section files are created or updated, the workflow must keep `GLOSSARY.md` current with any newly introduced or changed domain terms, applications, data objects, and relationships.

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

- [SKILL.md](SKILL.md)
- Epics are listed in Phase E and created under `requirements/<name-of-target-architecture>/` with [To Epics](../to-epics/SKILL.md) only after the user provides an epic name, description, and main capability.

### Templates

- [Index template](templates/00-index-template.md)
- [Capability overview template](templates/01-capability-overview-template.md)
- [Preliminary phase template](templates/02-preliminary-phase-template.md)
- [Phase A architecture vision template](templates/03-phase-a-architecture-vision-template.md)
- [Phase B business architecture template](templates/04-phase-b-business-architecture-template.md)
- [Phase C data architecture template](templates/05-phase-c-data-architecture-template.md)
- [Phase D technology architecture template](templates/06-phase-d-technology-architecture-template.md)
- [Phase E solution building blocks template](templates/07-phase-e-solution-building-blocks-template.md)
- [Gap analysis template](templates/08-gap-analysis-template.md)
- [Roadmap themes template](templates/09-roadmap-themes-template.md)
- [Governance actions template](templates/10-governance-actions-template.md)
- [Risks and open questions template](templates/11-risks-and-open-questions-template.md)
- [Target architecture document template](templates/target-architecture-document-template.md)
