---
name: create-drawio-diagram
description: Create Draw.io diagrams from reusable architecture diagram templates and store editable `.drawio` files beside architecture documents. Use when the user asks for Draw.io, diagrams.net, editable architecture diagrams, or when an architecture workflow needs Draw.io versions of target architecture, solution architecture, data architecture, capability context, application component, conceptual data model, integration design, or integration flow diagrams.
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
- `templates/integration-design.drawio` for component maps organized in vertical layers: Public Internet, Frontend, Engagement, Integration, and Enterprise Foundation (Backoffice)
- `templates/integration-flow.drawio` for producers, consumers, interfaces, triggers, protocols, and sequence

## Style Rules

Use `STYLE.md` for colors, shape styles, connector styles, and layout rules.

Do not introduce new colors unless the user explicitly asks for a palette change. Reuse the standard palette so diagrams stay consistent across solution architecture documents.

## Workflow

1. Confirm the diagram purpose and choose the closest template.
2. Copy the template into the target architecture folder using a descriptive same-purpose filename, such as `capability-overview.drawio`.
3. Replace placeholder labels with concrete architecture content from the source document, glossary, capability overview, or clarification session.
4. Apply the exact standard colors and connector styles from `STYLE.md`. Do not use dark theme variants, approximate colors, or inherited editor defaults.
5. Keep labels business-readable and concise. Use notes in the surrounding architecture document for detail that would clutter the diagram.
6. Keep canonical data object names general. Do not use vendor object names, table names, endpoint resources, or internal system names in this public repository.
7. Do not invent systems, relationships, protocols, owners, or data flows. Mark unknowns as assumptions or open questions in the architecture document.
8. If an image export is needed, export the Draw.io diagram to a same-basename `.svg` using the SVG export rules below, then embed the SVG in the architecture document with a nearby link to the `.drawio` source.

## Capability Context Layout

When using `templates/capability-overview.drawio`, preserve the template topology. The diagram is a context view, not an inventory list.

- Place actors, teams, and channels in the left zone.
- Place the target capability in the center as the primary green node.
- Place upstream capabilities, source systems, triggers, and inputs above or upper-left of the target capability.
- Place downstream capabilities, consuming systems, outcomes, and outputs below or lower-right of the target capability.
- Place external dependencies, third parties, regulatory constraints, and vendor dependencies in the right zone.
- Connect each node to the target capability with a concise relationship label.
- Use light palette colors from `STYLE.md`: actors yellow, target capability green, upstream/downstream systems blue, and external dependencies red.
- When a node is backed by a named application, show only the application name in a separate 10 px high header box attached to the top of that node. Use the Application name header style from `STYLE.md`, make the header as wide as the component, and put capability names, component names, dependencies, and responsibilities in the node body. If the application name is unknown, omit the header.
- Show each confirmed stakeholder, user group, actor, or channel as a separate actor node. Do not collapse stakeholders and users into one list box.
- Show each confirmed input provider, source system, upstream capability, trigger, or input component as a separate upstream node. When the application name is known, put that application name in the node's application header.
- Show each confirmed produced outcome, downstream consumer, or related capability as a separate downstream node. Do not collapse produced outcomes into one list box.
- Do not stack every actor, system, platform, and dependency in one vertical column.
- Do not convert the target capability into a system dependency. Keep it visually distinct.
- Route actor connectors from the right side of actor nodes to the left side of the target capability, upstream connectors into the top of the target capability, downstream connectors out of the bottom, and external dependency connectors from the right side of the target capability.
- When there are multiple nodes in one zone, stagger their connector lanes so labels and arrowheads do not overlap. Use explicit `mxPoint` waypoints where automatic routing creates overlap.
- If a zone has many items, widen the canvas and spread nodes across the zone before grouping. Group only when the source content does not provide enough detail to keep the nodes meaningful or the diagram would become unreadable even after widening.
- If the source content does not identify a relationship direction, keep the node out of the diagram and record the gap as an assumption or open question in the document.

## Capability Context Helper

Use `scripts/write-capability-context-diagram.py` when a workflow needs to generate both an editable `.drawio` source and a same-basename `.svg` for a capability context diagram.

```sh
python3 skills/create-drawio-diagram/scripts/write-capability-context-diagram.py "Order Management" \
  --output-dir capabilities/order-management \
  --stakeholder "Customer service" \
  --stakeholder "Operations" \
  --input-provider "ERP" \
  --input-provider "Commerce platform" \
  --outcome "Inventory Management" \
  --constraint "Order status is fragmented across systems."
```

By default, the helper creates `capability-overview.drawio` and `capability-overview.svg` in the output directory. Use `--basename <name>` when a different same-basename pair is needed.

The helper also accepts compatibility aliases for upstream capability workflows:

- `--existing-system` as an alias for `--input-provider`
- `--related-capability` as an alias for `--outcome`
- `--pain-point` as an alias for `--constraint`

## Integration Design Layout

When using `templates/integration-design.drawio`, preserve the vertical layer structure. The diagram is a layered component map for an integration design, not a sequence diagram, endpoint catalog, or source-to-destination column layout.

- Place components inside the corresponding layer band, ordered from top to bottom: Public Internet, Frontend, Engagement Services, Integration, and Enterprise Foundation (Backoffice).
- Use plain colored rectangles for layer bands, not Draw.io swimlanes. Keep layer labels left-aligned and top-aligned. Use the layer fill color with no stroke.
- Treat the canvas as flexible. Increase `pageWidth`, `pageHeight`, and the layer-band rectangle sizes as needed so all components, routing lanes, connector labels, and notes fit cleanly.
- Treat every layer band as flexible in width and height. Grow a layer wider for additional horizontal component lanes, and grow it taller for stacked components or extra connector routing space.
- Leave clear top and bottom padding around components inside each layer band.
- Align components toward the left side of the canvas by default. Start the first meaningful component column close to the layer content area, then place later components to the right as the integration progresses. Do not center the whole diagram when there is unused space on the left.
- Use a consistent component grid across layers: align related components by x-position when they participate in the same flow, and align peer components on the same baseline inside a layer.
- Prefer vertical flow columns for linear integrations across layers. When a component in one layer directly calls, publishes to, or consumes from a component in another layer, place the related components above and below each other on the same x-position where space allows.
- Use horizontal placement primarily for peer components in the same layer, branching alternatives, fan-out/fan-in paths, or same-layer handoffs. Do not force a left-to-right stair-step layout when a top-to-bottom column would be clearer.
- Keep components as the main diagram elements. Use the exact layer colors from `STYLE.md` to classify each component: Public Internet light red, Frontend light yellow, Engagement light green, Integration light grey, and Enterprise Foundation (Backoffice) light blue.
- Show every confirmed component needed to understand how data or commands move from source to destination.
- Show the integration path by connecting components across layers. Route connectors clearly between layers and between peer components when needed.
- Use concise connector labels for trigger, protocol, contract, routing, transformation, retry, acknowledgement, or ownership details.
- For cross-layer flows, connect components from bottom-to-top or top-to-bottom using straight vertical orthogonal connectors whenever possible. Use side connectors only when vertical routing would cross another component or label.
- Route every connector around components, not through components. Use explicit orthogonal `mxPoint` waypoints whenever Draw.io automatic routing would cross a component, component header, layer label, or another connector label.
- Put connector labels on open horizontal or vertical lane segments with clear whitespace. Do not place connector text on top of components, application headers, layer labels, arrowheads, or other connector labels.
- Leave at least 160 px of horizontal space between two components connected by a labeled connector. If the connector label is longer than 24 characters, leave at least 220 px, shorten the label, or route the label onto a longer empty segment.
- Use separate routing lanes for parallel or crossing flows. Stagger vertical lanes and horizontal lanes so no two connectors share the same segment when their labels or arrowheads would collide.
- For dense integration diagrams, widen the canvas, increase layer widths and heights, or move components farther apart before exporting. Do not accept an SVG where connectors or connector labels overlap components.
- Do not add separate data-contract, payload, message, or file boxes to integration design diagrams. Keep contract and payload details in connector labels when short, and put detailed contract information in the integration design document.
- Do not add monitoring, reconciliation, run-status, failed-record, stale-index, alerting, dashboard, or support components to integration design diagrams. Capture observability, reconciliation, and support details in the integration design document instead.
- Duplicate nodes inside a layer when the design has multiple components in that layer. Keep related components aligned so readers can trace each integration path through the layers.
- If the source content does not identify a component layer, use the neutral component style and record the categorization as an assumption or open question in the integration design.
- Do not add real-company system names, internal endpoints, topics, queues, payload fields, credentials, or proprietary integration details to this public repository.

## SVG Export Rules

Exported SVGs must preserve the exact colors from the `.drawio` source.

- Export from the light-themed diagram using the diagram's explicit styles. Do not export from a dark-mode preview, themed preview, or editor mode that rewrites colors.
- Keep the page background in the SVG. Exported SVGs must have a white or light page background from the source diagram, normally `#fbfcfa`. Do not export with transparent background.
- Treat a dark, black, transparent, or theme-inverted SVG background as a failed export. Re-export from the light-themed `.drawio` source with an explicit page background before embedding or publishing.
- Exported SVGs must use `color-scheme: light` only. Treat `color-scheme: light dark`, `color-scheme: dark`, missing explicit light color scheme, or `light-dark(...)` as failed exports. These Draw.io-generated CSS values can make Confluence, browsers, or dark-mode previews render the diagram with inverted/dark colors.
- Before embedding or publishing, inspect the SVG text for `color-scheme` and `light-dark(`. If `color-scheme` is not explicitly light-only, or if `light-dark(` is present, regenerate or sanitize the SVG so all colors are fixed explicit hex values and the background remains white/light.
- After every Draw.io SVG export, run `skills/create-drawio-diagram/scripts/sanitize-drawio-svg.py <diagram.svg>`. This forces `color-scheme: light`, removes `light-dark(...)`, and inserts a light background rectangle.
- Do not post-process exported SVGs with CSS color filters, dark-mode transforms, image optimizers, or theme substitution.
- Do not replace concrete hex colors with `currentColor`, CSS variables, inherited colors, or generated dark palette values.
- Before embedding the SVG, inspect it visually against the `.drawio` source. If colors differ, regenerate the SVG before embedding it.
- Before embedding the SVG, inspect the exported background. Regenerate the `.drawio` or export if the SVG background is not white/light.
- Before embedding an integration design SVG, inspect connector routing and labels. Regenerate the `.drawio` with wider spacing or explicit waypoints if any connector or connector label overlaps a component, component header, layer label, arrowhead, or other label.
- Before embedding an integration design SVG, inspect alignment and spacing. Regenerate the `.drawio` if the diagram has large unused left-side whitespace, components appear unnecessarily centered, labeled connectors have cramped horizontal space, or any connector crosses through a component.

## Output Rules

- Store `.drawio` files beside the document they support.
- Prefer one diagram per file.
- Use stable filenames that match the architecture section, such as `application-component-view.drawio`.
- Keep generated diagrams editable in Draw.io. Do not replace them with static-only SVGs unless the user explicitly asks for export-only output.
- Keep exported SVG colors identical to their `.drawio` source colors.
- Keep this public toolkit free of company-confidential information.
