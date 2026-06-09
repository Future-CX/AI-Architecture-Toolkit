# Draw.io Diagram Style Guide

Use this style guide for every Draw.io diagram created with this skill.

## Palette

Use the exact hex values below. Do not darken, tint, theme, or approximate these colors. If an element does not fit a listed category, use the neutral component style until the architecture document clarifies the category.

| Use                                                      | Fill      | Stroke    | Text      |
| -------------------------------------------------------- | --------- | --------- | --------- |
| Page background                                          | `#fbfcfa` | n/a       | `#000000` |
| Primary capability or business object                    | `#d9eadf` | `#0f766e` | `#000000` |
| Actor, channel, producer, or entry point                 | `#fff3c4` | `#b7791f` | `#000000` |
| Application, platform, integration, or system dependency | `#dae8fc` | `#315f8f` | `#000000` |
| Public Internet layer                                    | `#fee9e8` | n/a       | `#000000` |
| Frontend layer                                           | `#fffbe2` | n/a       | `#000000` |
| Engagement Services layer                                | `#def9ea` | n/a       | `#000000` |
| Integration layer                                        | `#f5f5f5` | n/a       | `#000000` |
| Enterprise Foundation (Backoffice) layer                 | `#e8f1ff` | n/a       | `#000000` |
| Public Internet component                                | `#f8cecc` | `#a3433f` | `#000000` |
| Frontend component                                       | `#fff3c4` | `#b7791f` | `#000000` |
| Engagement Service component                             | `#d9eadf` | `#0f766e` | `#000000` |
| Integration component                                    | `#edf2f0` | `#8a9992` | `#000000` |
| Enterprise Foundation (Backoffice) component             | `#dae8fc` | `#315f8f` | `#000000` |
| External dependency, risk, or constraint                 | `#f8cecc` | `#a3433f` | `#000000` |
| Neutral component, payload, or note                      | `#ffffff` | `#d8dfda` | `#000000` |
| Application name header                                  | `#000000` | `#000000` | `#ffffff` |
| Connector                                                | n/a       | `#000000` | `#000000` |

## Shape Styles

Use square-corner rectangles for architecture elements:

```text
rounded=0;whiteSpace=wrap;html=1;spacing=12;fontColor=#17201d;strokeWidth=2;
```

Add the category fill and stroke from the palette to every architecture element. For example, an actor must include `fillColor=#fff3c4;strokeColor=#b7791f;fontColor=#17201d;`, and an application or platform dependency must include `fillColor=#dae8fc;strokeColor=#315f8f;fontColor=#17201d;`.

Use this base style for component bodies:

```text
rounded=0;whiteSpace=wrap;html=1;spacing=12;fontColor=#17201d;fontStyle=1;strokeWidth=2;
```

For layered integration design maps, use layer colors for the layer-band rectangles and component colors for the component bodies. Component bodies must use dark text (`#17201d`) for readability: Public Internet component light red, Frontend component light yellow, Engagement component light green, Integration component light grey, and Enterprise Foundation (Backoffice) component light blue. If a component's layer is unclear, use the neutral component style and capture the categorization as an open question in the supporting document.

When a component, capability, system, or dependency is implemented by a named application, place only the application name in a separate 10 px high header box attached to the top of the component. Use the same width as the component, `fillColor=#000000`, `strokeColor=#000000`, `fontColor=#ffffff`, `fontStyle=1`, `fontSize=6`, `spacing=0`, and `strokeWidth=2`. Put capability names, component names, responsibilities, dependencies, and integration roles in the component body below the header. If the application name is unknown, omit the header.

Use swimlanes only for meaningful ownership or application boundaries:

```text
swimlane;whiteSpace=wrap;html=1;startSize=34;align=left;spacingLeft=12;fillColor=#edf3ef;strokeColor=#0f766e;fontColor=#17201d;strokeWidth=2;
```

For integration design layer bands, use plain colored rectangles, not Draw.io swimlanes. Use the layer fill color with `strokeColor=none`. Keep layer labels left-aligned and top-aligned with `align=left;verticalAlign=top;spacing=12;fontStyle=1`.

Use title text with:

```text
text;html=1;strokeColor=none;fillColor=none;align=left;fontStyle=1;fontSize=24;fontColor=#17201d;
```

Use connectors with:

```text
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;strokeColor=#5d6964;fontColor=#5d6964;labelBackgroundColor=#fbfcfa;labelBorderColor=none;strokeWidth=2;
```

Use dashed connectors only for optional, informational, or payload relationships.

## Layout Rules

- Keep left-to-right flow for context and application diagrams. For integration design diagrams, place components in vertical architecture layers from top to bottom: Public Internet, Frontend, Engagement, Integration, and Enterprise Foundation (Backoffice).
- Preserve the zones and relative positions in the selected template. Replace labels and duplicate nodes inside the same zone; do not collapse the diagram into a single vertical list.
- Canvas size is flexible. For integration design diagrams, increase `pageWidth` and `pageHeight` whenever the default template size would force cramped components, overlapping connectors, clipped labels, or crowded layer bands.
- Integration layer bands are flexible. Increase each layer band's width and height independently so its components, labels, and routing lanes have enough whitespace.
- In integration design diagrams, leave clear top and bottom padding around components inside each layer band.
- Keep data models centered around canonical business data objects.
- Prefer 80-120 px tall nodes for readability.
- Route connectors on separate orthogonal lanes. Do not let two connectors share the same horizontal or vertical segment when their labels or arrowheads would overlap.
- Do not route connectors through nodes, node labels, edge labels, or arrowheads.
- Place connector labels on clear line segments with enough whitespace around the label. If labels collide, move the label position or reroute the connector with explicit waypoints.
- For integration design diagrams, reserve connector lanes between components and between layer bands. Place components far enough apart that connectors can route around them without crossing through component bodies or application headers.
- Connector labels must not overlap components, application headers, layer labels, arrowheads, or other connector labels. If a label cannot fit cleanly on the connector, shorten the label and capture the detail in the document.
- Avoid crossing connectors when repositioning nodes or adding waypoints would remove the crossing.
- Keep labels short and business-readable.
- Do not use decorative colors outside the palette.
