# Create Draw.io Diagram

Create editable Draw.io diagrams from reusable architecture templates.

Use this skill when a solution architecture, target architecture, data architecture, or integration design document needs stakeholder-editable `.drawio` diagrams. Templates cover target architecture overviews, solution architecture overviews, data architecture overviews, capability context, application/component views, conceptual data models, integration design component maps, and integration flows.

After exporting a Draw.io diagram to SVG, run `scripts/sanitize-drawio-svg.py <diagram.svg>` so the SVG uses a fixed light color scheme and renders with a light background in Confluence and dark-mode browsers.

- [SKILL.md](SKILL.md)
- [Style guide](STYLE.md)
- [Capability context diagram helper](scripts/write-capability-context-diagram.py)
- [Target architecture diagram template](templates/target-architecture-diagram.drawio)
- [Solution architecture diagram template](templates/solution-architecture-diagram.drawio)
- [Data architecture diagram template](templates/data-architecture-diagram.drawio)
- [Capability overview template](templates/capability-overview.drawio)
- [Application component view template](templates/application-component-view.drawio)
- [Conceptual data model template](templates/conceptual-data-model.drawio)
- [Integration design template](templates/integration-design.drawio)
- [Integration flow template](templates/integration-flow.drawio)
