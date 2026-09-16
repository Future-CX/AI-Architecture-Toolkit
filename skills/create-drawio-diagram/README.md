# Create Draw.io Diagram

Create editable Draw.io diagrams from reusable architecture templates.

Use this skill when a solution architecture, target architecture, data architecture, or integration design document needs stakeholder-editable `.drawio` diagrams. Templates cover layered capability maps, target architecture overviews, solution architecture overviews, data architecture overviews, capability context, application/component views, conceptual data models, integration design component maps, and integration flows.
Use the data flow template when an architecture workflow needs a swimlane-style operational trace across systems and process stages.

Integration flow diagrams always group participant lanes inside five adjoining layers, from top to bottom: Public Internet (red), Frontend (yellow), Engagement Services (green), Integrations (grey), and Enterprise Foundation (blue). Flow direction does not change the layer order.

Always store editable Draw.io sources and same-basename exports under a `diagrams/` subfolder next to the document they support. Never place diagram files beside the supporting document.

Create `.drawio` sources with explicit light-theme colors and a `#fbfcfa` page background. After exporting to SVG, use `scripts/sanitize-drawio-svg.py <diagram.svg>` only as a final compatibility guard when Draw.io still emits theme-adaptive SVG CSS.

Connector routing is a hard acceptance gate. Connectors may touch their source and target only at deliberate boundary ports; they must never pass through, over, or behind a component body, application header, or label. A composite component with an application header may expose one explicit outer top-center boundary port when the connector immediately travels into whitespace. Render and inspect the exported SVG at 100% zoom before accepting it.

Solution architecture diagrams use distinct ports and explicit paths for direct calls, branches, and return arrows. Before export, run `scripts/check-solution-architecture-routing.py <diagram.drawio>`. It checks flat, uncompressed XML for connector crossings, shared segments or ports, and component/header collisions, and rejects routes that still depend on automatic routing. Rendered labels and arrowheads still need visual inspection.

The capability context helper keeps connector paths separate, uses explicit top-center boundary ports on application headers, and fits the canvas to the content with 60 px of bottom padding. Both `.drawio` and `.svg` use the same node positions, connector bends, and page dimensions.

Run its routing and export regression checks from the repository root:

```sh
python3 -m unittest discover -s skills/create-drawio-diagram/scripts -p 'test_capability_context_diagram.py'
```

Run the solution routing checker tests with:

```sh
python3 -m unittest discover -s skills/create-drawio-diagram/scripts -p 'test_solution_architecture_routing.py'
```

- [SKILL.md](SKILL.md)
- [Style guide](STYLE.md)
- [Capability context diagram helper](scripts/write-capability-context-diagram.py)
- [Solution architecture routing check](scripts/check-solution-architecture-routing.py)
- [Target architecture diagram template](templates/target-architecture-diagram.drawio)
- [Solution architecture diagram template](templates/solution-architecture-diagram.drawio)
- [Data architecture diagram template](templates/data-architecture-diagram.drawio)
- [Data flow template](templates/data-flow.drawio)
- [Capability map template](templates/capability-map.drawio)
- [Capability overview template](templates/capability-overview.drawio)
- [Application component view template](templates/application-component-view.drawio)
- [Conceptual data model template](templates/conceptual-data-model.drawio)
- [Integration design template](templates/integration-design.drawio)
- [Integration flow template](templates/integration-flow.drawio)
