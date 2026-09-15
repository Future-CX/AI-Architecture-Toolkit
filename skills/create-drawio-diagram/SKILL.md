---
name: create-drawio-diagram
description: Create Draw.io diagrams from reusable architecture diagram templates and always store editable `.drawio` files and exports in a `diagrams/` subfolder. Use when the user asks for Draw.io, diagrams.net, editable architecture diagrams, or when an architecture workflow needs Draw.io versions of target architecture, solution architecture, data architecture, capability context, application component, conceptual data model, integration design, or integration flow diagrams.
---

# Create Draw.io Diagram

## Quick Start

Create editable Draw.io diagrams for architecture deliverables using the templates in `templates/` and the visual rules in `STYLE.md`.

Use this skill when a generated architecture document needs diagrams that stakeholders can edit in Draw.io or diagrams.net. Always create a `diagrams/` subfolder next to the supporting document and store every generated `.drawio` source and same-basename export there. Never place diagram files beside the supporting document.

## Diagram Templates

Use these templates as starting points:

- `templates/capability-map.drawio` for a layered map of capabilities across Channel, Engagement Services, Integration, and Enterprise Foundation, with three cross-cutting columns
- `templates/capability-overview.drawio` for actors, neighboring capabilities, and external dependencies
- `templates/target-architecture-diagram.drawio` for a simple target architecture overview across capabilities, applications, data, integrations, and technology
- `templates/solution-architecture-diagram.drawio` for a simple solution architecture overview across channels, components, integrations, data stores, and external systems
- `templates/data-architecture-diagram.drawio` for a simple data architecture overview across source systems, owners, consumers, integrations, and governance
- `templates/data-flow.drawio` for data flow diagrams with process stages across the top, systems as horizontal lanes, and labeled data movements between lanes
- `templates/application-component-view.drawio` for applications, services, components, platforms, and responsibilities
- `templates/conceptual-data-model.drawio` for canonical data objects and relationships
- `templates/integration-design.drawio` for component maps organized in vertical layers: Public Internet, Frontend, Engagement, Integration, and Enterprise Foundation (Backoffice)
- `templates/integration-flow.drawio` for producers, consumers, interfaces, triggers, protocols, and sequence

## Style Rules

Use `STYLE.md` for colors, shape styles, connector styles, and layout rules.

Do not introduce new colors unless the user explicitly asks for a palette change. Reuse the standard palette so diagrams stay consistent across solution architecture documents.

## Light Theme Source Rules

Create `.drawio` sources as light-theme diagrams from the start.

- Every `mxGraphModel` must set `background="#fbfcfa"`. Do not leave the page background unset or transparent.
- Every visible shape, layer band, connector, label, and application header must use explicit hex colors from `STYLE.md`.
- Do not use Draw.io inherited or theme-dependent values such as `strokeColor=default`, `fontColor=default`, `labelBackgroundColor=default`, `currentColor`, CSS variables, or `light-dark(...)`.
- Use dark text, normally `fontColor=#17201d`, on light fills. Use `fontColor=#5d6964` for connector labels unless a specific palette color communicates flow type.
- Use `labelBackgroundColor=#fbfcfa` for connector labels so labels remain readable on light layer bands.
- Treat dark-theme or theme-adaptive source styles as defects in the `.drawio` file. Fix the `.drawio` source before exporting SVG.

## Workflow

1. Confirm the diagram purpose and choose the closest template.
2. Create a `diagrams/` subfolder next to the supporting document, then copy the template into it using a descriptive same-purpose filename, such as `diagrams/capability-overview.drawio`.
3. Replace placeholder labels with concrete architecture content from the source document, glossary, capability overview, or clarification session.
4. Position all components first and reserve visible whitespace corridors for every connector before adding or rerouting edges.
5. Apply the exact standard colors and connector styles from `STYLE.md`. Do not use dark theme variants, approximate colors, or inherited editor defaults.
6. Route and inspect every connector using the non-negotiable routing gate below. Do not rely on Draw.io automatic routing when it creates an ambiguous or obstructed path.
7. Keep labels business-readable and concise. Use notes in the surrounding architecture document for detail that would clutter the diagram.
8. Keep canonical data object names general. Do not use vendor object names, table names, endpoint resources, or internal system names in this public repository.
9. Do not invent systems, relationships, protocols, owners, or data flows. Mark unknowns as assumptions or open questions in the architecture document.
10. If an image export is needed, export the Draw.io diagram to a same-basename `.svg` using the SVG export rules below, visually inspect the rendered SVG at 100% zoom, and embed it only after it passes the routing gate.

## Non-negotiable Connector Routing Gate

A generated diagram fails review if any connector or connector label passes through, runs over, or is hidden behind a component. Fix the `.drawio` source and re-export it; never accept the collision as a layout compromise.

- Treat the complete visible component as blocked space. This includes its body, border, text, icon, application-name header, badge, and any nested child shape.
- A connector may touch its source and target only at one deliberate boundary attachment point. Except for the arrowhead at that endpoint, no part of the connector may enter either endpoint component's interior.
- Application-name headers occupy the component's top edge. Never route a connector into, out of, across, or underneath such a header. Use a left, right, or unobstructed bottom port and an orthogonal waypoint instead.
- Keep the full connector path in whitespace with at least 10 px clearance from every unrelated component and header. Use more clearance where an arrowhead or label needs it.
- Use explicit entry and exit ports plus explicit orthogonal `mxPoint` waypoints whenever automatic routing could cross blocked space. Automatic routing is not evidence that the route is safe.
- Do not use a component as a visual bridge and do not let unrelated connectors share a hidden trunk behind it. Shared segments are allowed only for an explicitly modeled bus, and that bus must remain fully visible in whitespace.
- Trace each rendered connector end to end at 100% zoom after SVG export. Check the source endpoint, every bend and label, and the target arrowhead. If any section touches blocked space anywhere other than its two deliberate endpoints, move the nodes or reroute the connector and inspect again.
- When a clean route does not fit, enlarge the canvas or layer band and move components apart. Never solve the problem by drawing over a component, sending a connector behind it, or depending on z-order to conceal the collision.

## Capability Map Layout

When using `templates/capability-map.drawio`, preserve the four horizontal layers and the three cross-cutting vertical columns to their right. Place every confirmed layered capability in exactly one corresponding horizontal layer.

- Keep the layer order from top to bottom: Channel, Engagement Services, Integration, and Enterprise Foundation.
- Keep these three equal-width vertical columns from left to right: UI Design and Testing; Observability (Logging, Monitoring & Alerting); DevOps.
- Treat the vertical columns as cross-cutting capabilities that apply across all four horizontal layers. Do not duplicate them as nodes inside a horizontal layer.
- Use these editable starter capabilities inside the cross-cutting columns:
  - UI Design and Testing: Usability Testing; Browser Testing; Design System.
  - Observability (Logging, Monitoring & Alerting): Application Performance Monitoring; API Monitoring; Logfile Monitoring; Alerting.
  - DevOps: Code Management; CI/CD; Code Quality Management; Code Vulnerability Management; (Agile) Project Management; Project Documentation.
- Treat the starter capabilities as typical examples, not confirmed enterprise facts. Keep only capabilities supported by the source material; replace, remove, or add capability nodes when the target architecture differs.
- Align the top of every cross-cutting column with the top of the Channel layer and its bottom with the bottom of the Enterprise Foundation layer. Keep a consistent gap between the horizontal layers and the columns and between adjacent columns.
- Place each column heading at the top and stack its capability nodes vertically from top to bottom beneath it, in the order documented above. Start every column's first capability at the same vertical position and use consistent node widths, heights, and compact vertical gaps. Do not spread a short list evenly across the full column height.
- Use the neutral palette for cross-cutting columns: white fill, light grey stroke, and dark text. Use the light-grey Integration component palette for capability nodes inside the columns. Keep all labels horizontally centered and wrapped; do not rotate the text.
- Use capability names only inside capability nodes. Put definitions, applications, responsibilities, and rationale in the supporting document.
- Keep capability names identical to the names in the capability overview table and linked capability documents.
- Arrange peer capabilities from left to right inside their layer, with no more than eight capability nodes in one row.
- When a layer contains more than eight capabilities, use the minimum number of rows needed and distribute the capabilities as evenly as possible. Calculate `row_count = ceil(capability_count / 8)`; each row must differ from the others by no more than one capability. For example, use rows of `5 + 4` for 9 capabilities, `6 + 5` for 11, `8 + 8` for 16, and `6 + 6 + 5` for 17.
- Center every row horizontally within its layer. Use consistent node widths and horizontal gaps within that layer, while allowing long capability names to wrap without reducing the font below the template size.
- Increase the affected layer's height for additional rows, keep clear space below the layer label and between rows, then move every following layer down by the same added height. Increase `pageHeight` so the final layer and its nodes remain fully inside the page.
- Whenever horizontal layers grow taller, extend all three cross-cutting columns by the same total added height so they still span the complete layered area.
- Increase the canvas width and every layer-band width together only when eight readable nodes cannot fit in a row. Do not solve crowding by placing more than eight nodes in one row or by shrinking text until it is hard to read.
- Whenever the horizontal layer bands grow wider, move the three-column group to the right while preserving its column widths and gaps, then increase `pageWidth` to keep the final column inside the page.
- Duplicate or remove placeholder nodes as needed so every included capability appears exactly once and no unused placeholder remains.
- Use the exact layer and component colors from `STYLE.md`: Channel yellow, Engagement Services green, Integration grey, and Enterprise Foundation blue.
- Do not add connectors merely to decorate the map. Add a relationship only when the source architecture explicitly defines it and the relationship materially helps readers.
- If a capability's layer is unknown or disputed, do not guess. Record it as an open question in the Capability Overview and resolve it before completing the map.
- If a cross-cutting column needs more vertical space, increase the complete layered height, extend all three columns equally, and increase `pageHeight`; do not make capability labels unreadably small.
- Before export, verify each capability appears exactly once, no row has more than eight nodes, rows within each layer are balanced, all three cross-cutting columns span the full layered height, and no layer label, column heading, capability node, or row overlaps or is clipped.

## Capability Context Layout

When using `templates/capability-overview.drawio`, preserve the template topology. The diagram is a context view, not an inventory list.

- Place actors, teams, and channels in the left zone.
- Place the target capability in the center as the primary green node. The target capability node label must be only the capability name, such as `CRM`; do not list features, workspaces, screens, data products, roles, baselines, or responsibilities inside the target capability node.
- Place systems or capabilities that deliver data to the target capability below the target capability.
- Place systems or capabilities that get data from the target capability above the target capability.
- Place external dependencies, third parties, regulatory constraints, and vendor dependencies in the right zone.
- Connect each node to the target capability with a concise relationship label.
- Use light palette colors from `STYLE.md`: actors yellow, target capability green, upstream/downstream systems blue, and external dependencies red.
- When a node is backed by a named application, show only the application name in a separate 10 px high header box overlaid on the top edge of that node. Use the Application name header style from `STYLE.md`, make the header as wide as the component, align its top with the component top, and render it above the component body. Put capability names, component names, dependencies, and responsibilities in the node body. If the application name is unknown, omit the header.
- Show each confirmed stakeholder, user group, actor, or channel as a separate actor node. Do not collapse stakeholders and users into one list box, and do not create a wrapper node titled `Stakeholders and users`.
- Show components that provide data to the target capability as separate bottom nodes per main data object and/or contributing capability. When several data objects come from one application or source system, create one node per data object and repeat the application name in the node's application header. Do not collapse multiple main data objects into one provider box.
- Show each confirmed produced outcome, downstream consumer, or related capability as a separate top consumer node. Do not collapse produced outcomes into one list box.
- Do not stack every actor, system, platform, and dependency in one vertical column.
- Do not convert the target capability into a system dependency. Keep it visually distinct.
- Route actor connectors from the right side of actor nodes to the left side of the target capability, data-provider connectors from bottom nodes into the bottom of the target capability, consumer connectors from the top of the target capability to top nodes, and external dependency connectors from the right side of the target capability.
- Use orthogonal connectors for capability context diagrams. Do not use diagonal straight-line connectors when an orthogonal route can keep labels and arrowheads clearer.
- Attach arrows to the nearest relevant edge of each box using explicit ports. Do not let arrowheads float near a box or land inside another box.
- Route connector waypoints through whitespace lanes between rows and columns. Connectors must not cross through node bodies, application headers, or node text.
- Capability context connectors must not cross, touch, or share any segment with another connector. Give each relationship a distinct boundary port and a clear orthogonal path; line jumps and hidden overlaps do not satisfy this rule.
- Center provider and consumer rows on the target capability and preserve node order at the capability's ports. Order bends from the outside of each fan inward, reversing the bend order on the opposite side. Staggering every bend in the same left-to-right order can still create crossings.
- Keep horizontal provider and consumer routing lanes outside the full middle zone occupied by actors, the target capability, and constraints. A tall actor stack must not extend into these lanes. Route providers with application headers from side ports through gaps beside their nodes.
- Keep repeated relationship labels on their own connector segments. If repeated labels such as `uses / governs`, `produces`, `provides input`, or `depends on` collide, stagger the connector lanes or shorten the labels before exporting.
- Avoid repeated relationship labels that overlap. When many connectors share the same relationship such as `provides input` or `gets data`, label one clear lane or stagger labels in whitespace rather than labeling every parallel connector.
- Reserve only the vertical space needed for connector paths and labels between rows. Increase node sizes and routing gaps when more items or longer labels need them.
- When there are multiple nodes in one zone, stagger their connector lanes so labels and arrowheads do not overlap. Use explicit `mxPoint` waypoints where automatic routing creates overlap.
- If a zone has many items, widen the canvas and spread nodes across the zone before grouping. Group only when the source content does not provide enough detail to keep the nodes meaningful or the diagram would become unreadable even after widening.
- Fit `pageWidth`, `pageHeight`, and the SVG `viewBox` to the final visible content, including labels and connector bends, with approximately 60 px of outer padding. Do not retain a fixed minimum page height or add blank bottom space based on node counts. Keep the light background.
- If the source content does not identify a relationship direction, keep the node out of the diagram and record the gap as an assumption or open question in the document.

## Capability Context Helper

Use `scripts/write-capability-context-diagram.py` when a workflow needs to generate both an editable `.drawio` source and a same-basename `.svg` for a capability context diagram.

```sh
python3 skills/create-drawio-diagram/scripts/write-capability-context-diagram.py "Order Management" \
  --output-dir capabilities/order-management/diagrams \
  --stakeholder "Customer service" \
  --stakeholder "Operations" \
  --input-provider $'ERP\nCustomer order\nCustomer account' \
  --input-provider "Commerce platform: Cart checkout event" \
  --outcome "Inventory Management" \
  --constraint "Order status is fragmented across systems."
```

The `--output-dir` value must be the supporting document's `diagrams/` subfolder. The helper creates `capability-overview.drawio` and `capability-overview.svg` there by default. Use `--basename <name>` when a different same-basename pair is needed.

For `--input-provider`, pass either a single application or source system name, an inline `Application: Data object` value, or a multiline block where the first line is the application/source system and each later line is a main data object or contributing capability. Multiline blocks generate one bottom node per later line.

The helper uses one shared layout calculation for `.drawio` and `.svg`: centered rows, ordered connector bends, distinct ports, side exits around application headers, and a canvas fitted to the content. Preserve these rules when editing a generated diagram manually. Replace or remove every template placeholder, including application headers, before accepting the output.

The helper also accepts compatibility aliases for upstream capability workflows:

- `--existing-system` as an alias for `--input-provider`
- `--related-capability` as an alias for `--outcome`
- `--pain-point` as an alias for `--constraint`

## Solution Architecture Layout

When using `templates/solution-architecture-diagram.drawio`, preserve the layered architecture structure. The diagram is a solution overview for one application or capability implementation, not a detailed sequence diagram or interface catalog.

- Place components inside the corresponding layer band, ordered from top to bottom: Public Internet, Frontend, Engagement Services, Integration, and Enterprise Foundation (Backoffice).
- When the solution includes a Backend-for-Frontend component, place it in the Frontend layer directly below the frontend/channel component it supports. Align the frontend component and BFF on the same x-position. Use a vertical connector only when its attachment edges are unobstructed; when an application header blocks the top edge, keep the components aligned and route through side ports in the adjacent whitespace.
- Do not place a Backend-for-Frontend component in Engagement Services or Integration. It remains a Frontend component even when it calls APIs, composes responses, or orchestrates channel-specific requests.
- Treat the canvas as flexible. Increase `pageWidth`, `pageHeight`, and every layer-band width or height whenever the default template would force cramped components, overlapping connectors, clipped labels, or crowded layer bands.
- Prefer widening or heightening the canvas and spreading components before shrinking boxes, shortening important labels, or stacking unrelated components.
- Grow all layer bands to the same width when the diagram needs more horizontal space so the architecture layers remain visually aligned. Increase layer heights and move lower bands down when components, notes, or connector labels need more vertical space.
- Leave enough whitespace between components for connector routing and labels. For labeled horizontal connectors, reserve at least 180 px between component edges; for labels longer than 24 characters, reserve at least 240 px or move detail into the document.
- Solution architecture connectors must not cross, touch, or share a segment with another connector. Give every relationship its own attachment ports and route. A dashed line, line jump, or hidden segment does not resolve a collision.
- Before adding edges, reserve horizontal and vertical routing corridors and assign a distinct port to every connection. Keep neighboring ports and parallel paths at least 24 px apart, preferably 32 px when space allows. Keep ports clear of corners and application headers.
- For a component with several connections, order its ports to match the positions of connected components. Give each branch its own bend lane and order the bends so outer branches do not cross inner branches. Do not send every relationship through the same side-center port.
- Route request and return arrows through separate parallel paths with different ports. Use opposite sides of a component or separate perimeter corridors for incoming, outgoing, and long return paths when this removes crossings.
- Keep direct calls close to the main component column. Route longer links and branches that skip components through dedicated side corridors or beneath the affected row, with separate horizontal lanes. Move components or widen the layer when a reserved path is obstructed.
- Use explicit entry and exit ports plus all required orthogonal waypoints. Set `noEdgeStyle=1;exitPerimeter=0;entryPerimeter=0;` on these edges so the editor preserves the planned route instead of choosing new bends automatically. Use side or bottom ports when a top application header blocks attachment.
- Route long cross-layer connectors through open whitespace lanes. Do not run connectors through layer labels, component bodies, application headers, or other connector labels.
- For dense solution architecture diagrams, widen and heighten the canvas first, then increase layer heights, then move components farther apart. Do not accept an SVG where component labels, connector labels, or arrowheads overlap.
- Keep the diagram readable at document scale. It is better to create a wider or taller same-basename SVG than to compress a complete solution into the default canvas.
- Keep every confirmed relationship and its direction while fixing the layout. Do not remove an edge, merge unrelated relationships, or mark a confirmed flow as optional to conceal a routing problem. If a complete overview remains too dense, use additional focused views and keep the relationships traceable.
- Replace all template titles, component labels, application headers, and relationship labels with confirmed design content. Remove unused starter components and edges; omit application headers when the application is unknown. Do not leave template labels such as `Solution name` or `Application name` in the final diagram.

### Solution Architecture Routing Check

Before SVG export, run the geometry check on the generated source:

```sh
python3 skills/create-drawio-diagram/scripts/check-solution-architecture-routing.py \
  solution-architectures/<slug>/diagrams/solution-architecture-diagram.drawio
```

Use the toolkit script path from the consuming repository when this toolkit is a submodule. The check reads the specified file without modifying it. It checks flat, uncompressed Draw.io XML with rectangular components and explicit orthogonal connector paths. Save compressed pages as uncompressed XML and normalize nested, rotated, or flipped components before checking; unsupported geometry must not be treated as a pass.

Fix every reported crossing, shared segment or port, component/header collision, or unchecked automatic route and rerun the check. A geometry pass does not verify rendered label dimensions, arrowheads, or all visual spacing. Export the SVG, trace every connector and label at 100% zoom, and reroute or reposition anything that still overlaps before embedding it.

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
- For cross-layer flows, connect components from bottom-to-top or top-to-bottom using straight vertical orthogonal connectors only when both attachment edges are unobstructed. Use side ports and explicit waypoints when a vertical route would cross a component, application header, or label.
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

## Data Architecture Diagram Layout

When using `templates/data-architecture-diagram.drawio`, preserve the layered architecture structure. The diagram is a data architecture design view for one canonical data object, not an integration sequence diagram.

- Place components inside the corresponding layer band, ordered from top to bottom: Public Internet, Frontend, Engagement Services, Integration, and Enterprise Foundation (Backoffice).
- Always place the Backend-for-Frontend directly below the New Webshop component, aligned on the same x-position. Keep both components inside the Frontend layer. Connect them vertically only when the attachment edges are unobstructed; otherwise route through side ports in the adjacent whitespace. Do not place the BFF in the Engagement Services or Integration layer, even when it calls APIs, composes requests, or shapes channel responses.
- Use the exact layer colors from `STYLE.md`: Public Internet light red, Frontend light yellow, Engagement light green, Integration light grey, and Enterprise Foundation (Backoffice) light blue.
- Place components horizontally when they are different peer components, alternate sources, alternate consumers, parallel integrations, or separate solution copies. Do not stack unrelated components vertically inside one layer.
- Use vertical alignment only when components are part of the same direct end-to-end flow and the alignment makes the data path easier to trace. The New Webshop and its Backend-for-Frontend are a required related stack, not peer components.
- Grow layer width for additional horizontal component placement before adding vertical stacks. Grow layer height only when there are multiple related rows or connector routing needs.
- Route every connector through whitespace between components. Connectors and connector labels must not cross or overlap component bodies, application headers, layer labels, arrowheads, or other connector labels. Reposition components, enlarge layer bands, and add explicit orthogonal waypoints until every route is clear.
- Omit deprecated components and their connectors. If a deprecated component still affects a decision or migration, capture that context in the architecture document rather than showing the component in the diagram.
- Do not add a standalone box, node, or component for the canonical data object. The diagram's subject is the data object, while its visible components represent systems, capabilities, integrations, or external parties.
- Show where the data is mastered, stored, transformed, and consumed through the relevant components and connectors. Use the business data object name in a connector label only when it helps distinguish the flow.
- Keep the data flow visually central when possible. Place sources to the left or below, consumers to the right or above, and governance or ownership notes in the traceability area.
- Put interface names, events, files, APIs, batches, ownership, and traceability details in concise connector labels or in the surrounding document table. Do not turn the diagram into a dense interface catalog.
- Do not add real-company system names, internal endpoints, topics, queues, payload fields, credentials, or proprietary integration details to this public repository.

## Data Flow Layout

When using `templates/data-flow.drawio`, preserve the horizontal swimlane structure. The diagram is an operational trace of one canonical data object, not a generic architecture context diagram.

- Replace the title with `<Organization or domain> | Data Flow | <Data object>`.
- Put the business journey, process stages, screens, or major events across the top from left to right.
- Keep the default lane order from top to bottom: Customer; Channel, for example New Webshop; optionally one backend-for-frontend lane when a BFF participates in the flow; then one horizontal lane for each Engagement solution; one horizontal lane for each Integration component; and one horizontal lane for each Enterprise Foundation or MDM solution. Rename the channel and solution labels to the real non-confidential names for the target design, but preserve this order unless the user explicitly asks for a different stack.
- Include the backend-for-frontend lane only when a BFF has a meaningful data-flow responsibility such as request composition, channel-specific orchestration, response shaping, or aggregation. Omit the BFF lane when the channel calls engagement solutions directly.
- Do not group multiple solutions into one broad lane such as `Engagement solutions` or `Integration components`. Each named solution or component gets its own lane and its own horizontal divider.
- Align each stage or event header with the vertical flow column it describes. Center the header above the boxes and arrows for that stage, and move the stage guide line to the same x-position.
- Draw data movement as vertical or orthogonal arrows crossing lanes. Label each arrow with the specific data object, event, command, file, API call, batch, or transformation.
- Use the template's connector colors consistently: blue for primary read, write, replication, or publication flows; green for enrichment, rules, calculation, validation, or decisioning flows; grey dashed lines for optional, planned, deprecated, or uncertain flows.
- Show where the data object is created, updated, enriched, read, replicated, archived, deleted, or submitted.
- Keep lane labels readable on the left and process-stage labels aligned across the top.
- Expand the canvas horizontally and vertically before compressing the flow. Add width for more stages and add height for more solution lanes. The exported SVG must not have overlapping arrows, labels, lane headers, boxes, or process-stage labels.
- Do not use real-company names, internal systems, proprietary event names, payload fields, endpoints, or confidential process details in this public repository.

## Integration Flow Layout

When using `templates/integration-flow.drawio`, preserve its five adjoining architecture-layer bands and the participant lanes within them. The diagram is an operational trace of one integration scenario or interface chain. Stages progress from left to right; architecture layers determine the vertical order.

- Replace the title with `<Organization or domain> | Integration Flow | <Integration scenario or interface name>`.
- Put the business trigger, request, orchestration, transformation, delivery, acknowledgement, error handling, and completion stages across the top from left to right.
- Always keep these five layer bands together in this exact top-to-bottom order, using these visible names and the existing palette:
  1. `Public Internet` — red (`#fee9e8` band; `#f8cecc` components with `#a3433f` borders).
  2. `Frontend` — yellow (`#fffbe2` band; `#fff3c4` components with `#b7791f` borders).
  3. `Engagement Services` — green (`#def9ea` band; `#d9eadf` components with `#0f766e` borders).
  4. `Integrations` — grey (`#f5f5f5` band; `#edf2f0` components with `#8a9992` borders).
  5. `Enterprise Foundation` — blue (`#e8f1ff` band; `#dae8fc` components with `#315f8f` borders).
- Draw each layer as one continuous, full-width background rectangle with a visible layer heading. Use the same left edge and width for all five bands. Each band's bottom must meet the next band's top with no blank gap. Keep padding and routing space inside the bands.
- Group all participant lanes from the same architecture layer together inside that band's boundaries. Never split or repeat a layer elsewhere in the stack. A producer or consumer stays in its architecture layer even when this requires an upward arrow or a return path. Put external actors and external parties in Public Internet; channels and their BFFs in Frontend; business services in Engagement Services; middleware in Integrations; and foundation APIs and stores in Enterprise Foundation. Resolve uncertain classification from the source design before placing a participant.
- Retain all five bands, including a compact heading-only band when that layer has no active participants. Do not invent participants to fill an empty layer.
- Include only lanes that actively send, receive, transform, route, persist, acknowledge, or monitor the integration. Do not add passive systems that are only mentioned in background context.
- Keep separate participant lanes and horizontal dividers within a layer when applications or middleware have distinct responsibilities. The shared colored layer band must not collapse participants into a single broad lane such as `Source systems` or `Consumers`.
- Do not duplicate the same participant in the same lane just to show a later step in the same interaction. Keep one participant box where possible and draw an orthogonal arrow from the preceding step to that existing box, then onward to the next participant.
- Duplicate a participant only when it represents a clearly separate occurrence in a different stage, branch, or independent interaction and a direct arrow would create crossings, unreadable backtracking, or an excessively long connector. If duplicated, use the exact same label and styling so readers understand it is the same participant appearing again for layout clarity.
- Prefer continuous arrows across stage columns over repeated component boxes. Use upward or return arrows when the scenario requires them, keeping the layer order fixed. A reader should be able to follow the scenario by tracing arrows.
- Color each participant by its architecture layer, not by the direction of the flow.
- Use the red Public Internet component style for external actors and parties in this view, including customer nodes; the yellow actor style used in capability context diagrams does not apply here.
- Treat Backend-for-Frontend and BFF components as Frontend components. They must use the yellow Frontend component style (`fillColor=#fff3c4;strokeColor=#b7791f`) even when they call APIs, compose responses, or orchestrate channel requests.
- Place a Backend-for-Frontend directly below the frontend/channel participant it supports and align it on the same x-position. Connect them vertically only when the attachment edges are unobstructed; otherwise route through side ports in the adjacent whitespace. Do not place the BFF as a peer beside the frontend component unless the flow has multiple frontend participants and vertical placement would make the path unreadable.
- Treat API gateway, API management, mediation, routing, and integration-platform components as Integration components. Azure API Management, API gateway, ESB, iPaaS, queue broker, and event broker nodes must use the grey Integration component style (`fillColor=#edf2f0;strokeColor=#8a9992`).
- Treat backoffice API providers, MDM APIs, host APIs, mainframe APIs, and enterprise system APIs as Enterprise Foundation components. IBMi APIs and similar foundation API provider nodes must use the blue Enterprise Foundation component style (`fillColor=#dae8fc;strokeColor=#315f8f`).
- Use green Engagement Service component styling (`fillColor=#d9eadf;strokeColor=#0f766e`) only for business-facing engagement services or application capabilities, not for BFFs, API management, or foundation APIs.
- Align each stage or event header with the vertical flow column it describes. Center the header above the messages, transformations, acknowledgements, or failure paths for that stage, and move the stage guide line to the same x-position.
- Draw integration messages as vertical or orthogonal arrows crossing lanes. Label each arrow with the business event, command, query, API call, event publication, file transfer, batch run, acknowledgement, retry, or error notification.
- Put protocol or pattern information in concise connector labels only when it changes the design, for example `REST command`, `event publish`, `batch file`, `webhook`, `async acknowledgement`, or `manual retry`.
- Use the template's connector colors consistently: blue for primary commands, queries, event publications, file transfers, batches, reads, writes, and delivery flows; green for routing, transformation, validation, enrichment, policy checks, or decisioning flows; grey dashed lines for optional, planned, deprecated, fallback, manual, or uncertain flows.
- Show direction and sequencing explicitly. If an acknowledgement, response, callback, retry, compensation, or dead-letter path materially affects ownership or operations, show it as a separate arrow instead of hiding it inside a label.
- Show where the payload is created, transformed, validated, enriched, routed, persisted, acknowledged, retried, rejected, or handed over. Keep payload and contract names business-readable and general.
- Keep interface details at the right level of abstraction. Use connector labels for interface names, canonical data objects, protocol or pattern, trigger, frequency, retry, idempotency, acknowledgement, and ownership when short. Put endpoint paths, fields, schemas, topic names, queue names, credentials, and detailed error codes in the supporting document, not in the diagram.
- Keep lane labels readable on the left and stage labels aligned across the top.
- Expand the canvas horizontally and vertically before compressing the flow. Add width for more stages and add height for more participants. The exported SVG must not have overlapping arrows, labels, lane headers, boxes, or process-stage labels.
- When adding participant lanes, grow their enclosing layer and shift every lower band down by the same amount so all five bands remain adjoining. Widen all five bands together when adding stages. Fit the page to the final bands and legend with a small outer margin.
- Replace the template title, stage labels, participant labels, component labels, and connector labels with confirmed scenario content. Remove unused example nodes, participant lanes, and connectors while retaining all five layer headings. Leave no `Domain`, `Scenario`, `name`, or other drafting placeholder in the final diagram.
- Use explicit orthogonal waypoints when automatic routing would make arrows cross through participant boxes, lane labels, stage headers, arrowheads, or other connector labels.
- Do not use real-company names, internal systems, proprietary event names, payload fields, endpoints, topics, queues, credentials, or confidential process details in this public repository.

## SVG Export Rules

Exported SVGs must preserve the exact colors from the `.drawio` source.

- Export from the light-themed diagram using the diagram's explicit styles. Do not export from a dark-mode preview, themed preview, or editor mode that rewrites colors.
- Keep the page background in the SVG. Exported SVGs must have a white or light page background from the source diagram, normally `#fbfcfa`. Do not export with transparent background.
- Treat a dark, black, transparent, or theme-inverted SVG background as a failed export. Re-export from the light-themed `.drawio` source with an explicit page background before embedding or publishing.
- Exported SVGs must use `color-scheme: light` only. Treat `color-scheme: light dark`, `color-scheme: dark`, missing explicit light color scheme, or `light-dark(...)` as failed exports. These Draw.io-generated CSS values can make Confluence, browsers, or dark-mode previews render the diagram with inverted/dark colors.
- Before embedding or publishing, inspect the SVG text for `color-scheme` and `light-dark(`. If `color-scheme` is not explicitly light-only, or if `light-dark(` is present, first fix the `.drawio` source and re-export. Run `skills/create-drawio-diagram/scripts/sanitize-drawio-svg.py <diagram.svg>` only as a final compatibility guard for Draw.io exports that still emit theme-adaptive SVG CSS.
- Do not post-process exported SVGs with CSS color filters, dark-mode transforms, image optimizers, or theme substitution.
- Do not replace concrete hex colors with `currentColor`, CSS variables, inherited colors, or generated dark palette values.
- Before embedding the SVG, inspect it visually against the `.drawio` source. If colors differ, regenerate the SVG before embedding it.
- Before embedding the SVG, inspect the exported background. Regenerate the `.drawio` or export if the SVG background is not white/light.
- Before embedding a capability overview SVG, inspect connector routing and labels. Regenerate the `.drawio` with staggered connector lanes or wider spacing if any connector, connector label, or arrowhead overlaps another connector, node, application header, or label.
- Before embedding a solution architecture SVG, require a passing solution architecture routing check and inspect the rendered paths, ports, arrowheads, and labels. Regenerate the source and export if connectors cross or share segments, if labels obscure another path, or if any route touches a component or application header outside its deliberate endpoint.
- Before embedding an integration design SVG, inspect connector routing and labels. Regenerate the `.drawio` with wider spacing or explicit waypoints if any connector or connector label overlaps a component, component header, layer label, arrowhead, or other label.
- Before embedding an integration design SVG, inspect alignment and spacing. Regenerate the `.drawio` if the diagram has large unused left-side whitespace, components appear unnecessarily centered, labeled connectors have cramped horizontal space, or any connector crosses through a component.
- Before embedding a data architecture design SVG, inspect connector routing, the Frontend layer, component status, and data representation. Regenerate the `.drawio` if any connector or connector label overlaps a component or label, if the Backend-for-Frontend is not directly below New Webshop within the Frontend layer, if a deprecated component is shown, or if the data object appears as a standalone component.
- Before embedding an integration flow SVG, verify that all five adjoining bands appear exactly once in this order: Public Internet (red), Frontend (yellow), Engagement Services (green), Integrations (grey), Enterprise Foundation (blue). Regenerate the `.drawio` if a band is missing, repeated, separated by a gap, or out of order; if participant lanes are outside their architecture layer; or if participant colors differ from their layer. Check external actors are red, BFFs are yellow, middleware is grey, and foundation APIs are blue.

## Output Rules

- Always store `.drawio` files and same-basename exports under a `diagrams/` subfolder next to the supporting document.
- Never place diagram sources or exports beside the supporting document.
- Prefer one diagram per file.
- Use stable filenames that match the architecture section, such as `application-component-view.drawio`.
- Keep generated diagrams editable in Draw.io. Do not replace them with static-only SVGs unless the user explicitly asks for export-only output.
- Keep exported SVG colors identical to their `.drawio` source colors.
- Keep this public toolkit free of company-confidential information.
