# Draw.io Diagram Style Guide

Use this style guide for every Draw.io diagram created with this skill.

## Palette

| Use | Fill | Stroke | Text |
| --- | --- | --- | --- |
| Page background | `#fbfcfa` | n/a | `#17201d` |
| Primary capability or business object | `#d9eadf` | `#0f766e` | `#17201d` |
| Actor, channel, producer, or entry point | `#fff3c4` | `#b7791f` | `#17201d` |
| Application, platform, integration, or system dependency | `#dae8fc` | `#315f8f` | `#17201d` |
| External dependency, risk, or constraint | `#f8cecc` | `#a3433f` | `#17201d` |
| Neutral component, payload, or note | `#ffffff` | `#d8dfda` | `#17201d` |
| Connector | n/a | `#5d6964` | `#5d6964` |

## Shape Styles

Use rounded rectangles for architecture elements:

```text
rounded=1;whiteSpace=wrap;html=1;arcSize=8;absoluteArcSize=1;spacing=12;fontColor=#17201d;strokeWidth=2;
```

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
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;strokeColor=#5d6964;fontColor=#5d6964;strokeWidth=2;
```

Use dashed connectors only for optional, informational, or payload relationships.

## Layout Rules

- Keep left-to-right flow for context, application, and integration diagrams.
- Preserve the zones and relative positions in the selected template. Replace labels and duplicate nodes inside the same zone; do not collapse the diagram into a single vertical list.
- Keep data models centered around canonical business data objects.
- Prefer 80-120 px tall nodes for readability.
- Avoid crossing connectors when a simple repositioning would remove the crossing.
- Keep labels short and business-readable.
- Do not use decorative colors outside the palette.
