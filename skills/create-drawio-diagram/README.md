# Create Draw.io Diagram

Create editable Draw.io diagrams from reusable architecture templates.

Use this skill when a solution architecture, target architecture, data architecture, or integration design document needs stakeholder-editable `.drawio` diagrams. Templates cover target architecture overviews, solution architecture overviews, data architecture overviews, capability context, application/component views, conceptual data models, integration design component maps, and integration flows.
Use the data flow template when a data architecture design needs a swimlane-style operational trace across systems and process stages.

Create `.drawio` sources with explicit light-theme colors and a `#fbfcfa` page background. After exporting to SVG, use `scripts/sanitize-drawio-svg.py <diagram.svg>` only as a final compatibility guard when Draw.io still emits theme-adaptive SVG CSS.

- [SKILL.md](SKILL.md)
- [Style guide](STYLE.md)
- [Capability context diagram helper](scripts/write-capability-context-diagram.py)
- [Target architecture diagram template](templates/target-architecture-diagram.drawio)
- [Solution architecture diagram template](templates/solution-architecture-diagram.drawio)
- [Data architecture diagram template](templates/data-architecture-diagram.drawio)
- [Data flow template](templates/data-flow.drawio)
- [Capability overview template](templates/capability-overview.drawio)
- [Application component view template](templates/application-component-view.drawio)
- [Conceptual data model template](templates/conceptual-data-model.drawio)
- [Integration design template](templates/integration-design.drawio)
- [Integration flow template](templates/integration-flow.drawio)
