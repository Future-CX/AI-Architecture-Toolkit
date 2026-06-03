---
name: create-drawio-diagram
description: Create Draw.io diagrams from reusable architecture diagram templates and store editable `.drawio` files beside architecture documents. Use when the user asks for Draw.io, diagrams.net, editable architecture diagrams, or when an architecture workflow needs Draw.io versions of target architecture, solution architecture, data architecture, capability context, application component, conceptual data model, or integration flow diagrams.
---

# Create Draw.io Diagram

## Quick Start

Create editable Draw.io diagrams for architecture deliverables using the templates in `templates/` and the visual rules in `STYLE.md`.

Use this skill when a generated architecture document needs diagrams that stakeholders can edit in Draw.io or diagrams.net. Store generated `.drawio` files in the same folder as the architecture document they support.

## Diagram Templates

Use these templates as starting points:

- `templates/capability-overview.drawio` for actors, neighboring capabilities, and external dependencies
- `templates/target-architecture-diagram.drawio` for a simple target architecture overview across capabilities, applications, data, integrations, and technology
- `templates/solution-architecture-diagram.drawio` for a simple solution architecture overview across channels, components, integrations, data stores, and external systems
- `templates/data-architecture-diagram.drawio` for a simple data architecture overview across source systems, canonical data objects, owners, consumers, integrations, and governance
- `templates/application-component-view.drawio` for applications, services, components, platforms, and responsibilities
- `templates/conceptual-data-model.drawio` for canonical data objects and relationships
- `templates/integration-flow.drawio` for producers, consumers, interfaces, triggers, protocols, and sequence

## Style Rules

Use `STYLE.md` for colors, shape styles, connector styles, and layout rules.

Do not introduce new colors unless the user explicitly asks for a palette change. Reuse the standard palette so diagrams stay consistent across solution architecture documents.

## Workflow

1. Confirm the diagram purpose and choose the closest template.
2. Copy the template into the target architecture folder using a descriptive same-purpose filename, such as `capability-overview.drawio`.
3. Replace placeholder labels with concrete architecture content from the source document, glossary, capability overview, or clarification session.
4. Apply the standard colors and connector styles from `STYLE.md`.
5. Keep labels business-readable and concise. Use notes in the surrounding architecture document for detail that would clutter the diagram.
6. Keep canonical data object names general. Do not use vendor object names, table names, endpoint resources, or internal system names in this public repository.
7. Do not invent systems, relationships, protocols, owners, or data flows. Mark unknowns as assumptions or open questions in the architecture document.
8. If an image export is needed, export the Draw.io diagram to a same-basename `.svg` and embed the SVG in the architecture document with a nearby link to the `.drawio` source.

## Capability Context Layout

When using `templates/capability-overview.drawio`, preserve the template topology. The diagram is a context view, not an inventory list.

- Place actors, teams, and channels in the left zone.
- Place the target capability in the center as the primary green node.
- Place upstream capabilities, source systems, triggers, and inputs above or upper-left of the target capability.
- Place downstream capabilities, consuming systems, outcomes, and outputs below or lower-right of the target capability.
- Place external dependencies, third parties, regulatory constraints, and vendor dependencies in the right zone.
- Connect each node to the target capability with a concise relationship label.
- Do not stack every actor, system, platform, and dependency in one vertical column.
- Do not convert the target capability into a system dependency. Keep it visually distinct.
- If a zone has more than three items, group related items into one business-readable node such as `Commerce platforms`, `Data and analytics platforms`, or `Operational stakeholders`, and list the detailed names in the document instead of crowding the diagram.
- If the source content does not identify a relationship direction, keep the node out of the diagram and record the gap as an assumption or open question in the document.

## Output Rules

- Store `.drawio` files beside the document they support.
- Prefer one diagram per file.
- Use stable filenames that match the architecture section, such as `application-component-view.drawio`.
- Keep generated diagrams editable in Draw.io. Do not replace them with static-only SVGs unless the user explicitly asks for export-only output.
- Keep this public toolkit free of company-confidential information.
