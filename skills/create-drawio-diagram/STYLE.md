# Draw.io Diagram Style Guide

Use this style guide for every Draw.io diagram created with this skill.

## Palette

Use the exact hex values below. Do not darken, tint, theme, or approximate these colors. If an element does not fit a listed category, use the neutral component style until the architecture document clarifies the category.

| Use | Fill | Stroke | Text |
| --- | --- | --- | --- |
| Page background | `#fbfcfa` | n/a | `#17201d` |
| Primary capability or business object | `#d9eadf` | `#0f766e` | `#17201d` |
| Actor, channel, producer, or entry point | `#fff3c4` | `#b7791f` | `#17201d` |
| Application, platform, integration, or system dependency | `#dae8fc` | `#315f8f` | `#17201d` |
| External dependency, risk, or constraint | `#f8cecc` | `#a3433f` | `#17201d` |
| Neutral component, payload, or note | `#ffffff` | `#d8dfda` | `#17201d` |
| Application name header | `#ffffff` | match component stroke | `#17201d` |
| Connector | n/a | `#5d6964` | `#5d6964` |

## Shape Styles

Use rounded rectangles for architecture elements:

```text
rounded=1;whiteSpace=wrap;html=1;arcSize=8;absoluteArcSize=1;spacing=12;fontColor=#17201d;strokeWidth=2;
```

Add the category fill and stroke from the palette to every architecture element. For example, an actor must include `fillColor=#fff3c4;strokeColor=#b7791f;fontColor=#17201d;`, and an application or platform dependency must include `fillColor=#dae8fc;strokeColor=#315f8f;fontColor=#17201d;`.

When a component, capability, system, or dependency is implemented by a named application, place the application name in a separate header box attached to the top of the component. Use the same width as the component, 30-40 px height, `fillColor=#ffffff`, the component's stroke color, `fontStyle=1`, and `fontColor=#17201d`. Keep the component's business-readable responsibility or capability name in the body below the header.

Use swimlanes only for meaningful ownership or application boundaries:

```text
swimlane;whiteSpace=wrap;html=1;startSize=34;fillColor=#edf3ef;strokeColor=#0f766e;fontColor=#17201d;strokeWidth=2;
```

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

- Keep left-to-right flow for context, application, and integration diagrams.
- Preserve the zones and relative positions in the selected template. Replace labels and duplicate nodes inside the same zone; do not collapse the diagram into a single vertical list.
- Keep data models centered around canonical business data objects.
- Prefer 80-120 px tall nodes for readability.
- Route connectors on separate orthogonal lanes. Do not let two connectors share the same horizontal or vertical segment when their labels or arrowheads would overlap.
- Do not route connectors through nodes, node labels, edge labels, or arrowheads.
- Place connector labels on clear line segments with enough whitespace around the label. If labels collide, move the label position or reroute the connector with explicit waypoints.
- Avoid crossing connectors when repositioning nodes or adding waypoints would remove the crossing.
- Keep labels short and business-readable.
- Do not use decorative colors outside the palette.
