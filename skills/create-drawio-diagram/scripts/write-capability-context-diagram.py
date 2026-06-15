#!/usr/bin/env python3
"""Create a capability context Draw.io diagram and matching SVG export."""

from __future__ import annotations

import argparse
import re
import textwrap
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DRAWIO_TEMPLATE = SKILL_DIR / "templates" / "capability-overview.drawio"
DEFAULT_BASENAME = "capability-overview"
TOP_NODE_Y = 105
CAPABILITY_Y = 320
ACTOR_START_Y = 255
EXTERNAL_Y = 330
BOTTOM_HEADER_Y = 575
BOTTOM_NODE_Y = 585
ACTOR_WIDTH = 190
NODE_WIDTH = 210
NODE_HEIGHT = 75
CAPABILITY_WIDTH = 265
CAPABILITY_HEIGHT = 120

ACTOR_STYLE = "rounded=0;whiteSpace=wrap;html=1;spacing=12;fillColor=#fff3c4;strokeColor=#b7791f;fontColor=#17201d;fontStyle=1;strokeWidth=2;"
CAPABILITY_STYLE = "rounded=0;whiteSpace=wrap;html=1;spacing=12;fillColor=#d9eadf;strokeColor=#0f766e;fontColor=#17201d;fontStyle=1;fontSize=16;strokeWidth=2;"
SYSTEM_STYLE = "rounded=0;whiteSpace=wrap;html=1;spacing=12;fillColor=#dae8fc;strokeColor=#315f8f;fontColor=#17201d;strokeWidth=2;"
EXTERNAL_STYLE = "rounded=0;whiteSpace=wrap;html=1;spacing=12;fillColor=#f8cecc;strokeColor=#a3433f;fontColor=#17201d;strokeWidth=2;"
APP_HEADER_STYLE = "rounded=0;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;fontColor=#ffffff;fontStyle=1;fontSize=6;spacing=0;strokeWidth=2;"
CONNECTOR_STYLE = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;strokeColor=#5d6964;fontColor=#5d6964;labelBackgroundColor=#fbfcfa;labelBorderColor=none;strokeWidth=2;"
ACTOR_GROUP_HEADINGS = {
    "actors",
    "actors or channels",
    "stakeholder",
    "stakeholders",
    "stakeholders and users",
    "users",
    "users and stakeholders",
}
INPUT_PROVIDER_HEADINGS = {
    "data",
    "data object",
    "data objects",
    "data provider",
    "data providers",
    "input",
    "input provider",
    "input providers",
    "inputs",
    "main data object",
    "main data objects",
    "source",
    "source system",
    "source systems",
    "systems",
    "systems that deliver data",
}


@dataclass(frozen=True)
class DataProviderNode:
    application: str | None
    label: str


def split_label_items(value: str) -> list[str]:
    normalized = value.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    parts = re.split(r"[\n;]+", normalized)
    cleaned = []
    for part in parts:
        item = re.sub(r"^\s*[-*]\s+", "", part).strip().rstrip(".")
        if item:
            cleaned.append(item)
    return cleaned


def capability_label(value: str) -> str:
    items = split_label_items(value)
    return items[0] if items else value.strip()


def diagram_list(items: list[str], fallback: str, limit: int = 3) -> str:
    cleaned = [item for value in items for item in split_label_items(value)]
    if not cleaned:
        return fallback
    return "<br>".join(cleaned[:limit])


def diagram_items(items: list[str], fallback: str, ignored_headings: set[str] | None = None) -> list[str]:
    ignored = ignored_headings or set()
    cleaned = []
    for value in items:
        for item in split_label_items(value):
            if item.lower() not in ignored:
                cleaned.append(item)
    return cleaned if cleaned else [fallback]


def split_inline_provider(value: str) -> tuple[str, str] | None:
    for separator in (" -> ", "=>", " | ", ": "):
        if separator in value:
            application, label = value.split(separator, 1)
            application = application.strip()
            label = label.strip()
            if application and label:
                return application, label
    return None


def data_provider_nodes(items: list[str], fallback: str) -> list[DataProviderNode]:
    nodes: list[DataProviderNode] = []
    for value in items:
        parts = [
            item
            for item in split_label_items(value)
            if item.lower() not in INPUT_PROVIDER_HEADINGS
        ]
        if not parts:
            continue
        if len(parts) == 1:
            inline = split_inline_provider(parts[0])
            if inline:
                nodes.append(DataProviderNode(application=inline[0], label=inline[1]))
            else:
                nodes.append(DataProviderNode(application=parts[0], label="Data provider"))
            continue
        application = parts[0]
        for label in parts[1:]:
            nodes.append(DataProviderNode(application=application, label=label))
    return nodes if nodes else [DataProviderNode(application=None, label=fallback)]


def remove_cells(root: ET.Element, cell_ids: set[str]) -> None:
    for parent in root.iter():
        for child in list(parent):
            if child.tag == "mxCell" and child.attrib.get("id") in cell_ids:
                parent.remove(child)


def add_cell(
    root_cell: ET.Element,
    cell_id: str,
    value: str,
    style: str,
    x: int,
    y: int,
    width: int,
    height: int,
) -> None:
    cell = ET.SubElement(
        root_cell,
        "mxCell",
        {
            "id": cell_id,
            "parent": "1",
            "style": style,
            "value": value,
            "vertex": "1",
        },
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "height": str(height),
            "width": str(width),
            "x": str(x),
            "y": str(y),
            "as": "geometry",
        },
    )


def relative_port(position: int, start: int, size: int) -> float:
    return min(1.0, max(0.0, (position - start) / size))


def add_edge(
    root_cell: ET.Element,
    edge_id: str,
    source: str,
    target: str,
    label: str,
    *,
    points: list[tuple[int, int]] | None = None,
    style_suffix: str = "",
) -> None:
    edge = ET.SubElement(
        root_cell,
        "mxCell",
        {
            "id": edge_id,
            "edge": "1",
            "parent": "1",
            "source": source,
            "style": CONNECTOR_STYLE + style_suffix,
            "target": target,
            "value": label,
        },
    )
    geometry = ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    if points:
        array = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in points:
            ET.SubElement(array, "mxPoint", {"x": str(x), "y": str(y)})


def distributed_port(index: int, count: int, start: int, size: int, padding: int = 34) -> int:
    if count <= 1:
        return start + size // 2
    usable = size - padding * 2
    return start + padding + round((usable * index) / (count - 1))


def write_capability_drawio(
    target: Path,
    capability_name: str,
    stakeholders: list[str],
    input_providers: list[str],
    outcomes: list[str],
    constraints: list[str],
) -> None:
    tree = ET.parse(DRAWIO_TEMPLATE)
    root = tree.getroot()
    graph_model = root.find(".//mxGraphModel")
    root_cell = root.find(".//root")
    if graph_model is None or root_cell is None:
        raise ValueError(f"Invalid Draw.io template: {DRAWIO_TEMPLATE}")

    target_label = capability_label(capability_name)
    actor_items = diagram_items(stakeholders, "Stakeholders to confirm", ACTOR_GROUP_HEADINGS)
    input_items = data_provider_nodes(input_providers, "Data provider to confirm")
    outcome_items = diagram_items(outcomes, "Outcome to confirm")
    max_items = max(len(actor_items), len(input_items), len(outcome_items))
    page_width = max(1169, 360 + max(len(input_items), len(outcome_items)) * 245)
    page_height = max(950, 700 + max_items * 100)
    graph_model.set("pageWidth", str(page_width))
    graph_model.set("pageHeight", str(page_height))

    remove_cells(
        root,
        {
            "actor",
            "upstream",
            "downstream",
            "external",
            "edge-actor-capability",
            "edge-upstream-capability",
            "edge-capability-downstream",
            "edge-capability-external",
            "wtTJ4m9Lci7Y-lzfFHPa-1",
            "hzigCzCzZuQ-4PxgagW3-1",
            "hzigCzCzZuQ-4PxgagW3-2",
            "hzigCzCzZuQ-4PxgagW3-3",
        },
    )
    for cell in root.iter("mxCell"):
        if cell.attrib.get("id") == "title":
            cell.set("value", f"{target_label} Context")
        if cell.attrib.get("id") == "capability":
            cell.set("value", target_label)
            cell.set("style", CAPABILITY_STYLE)
            geometry = cell.find("mxGeometry")
            if geometry is not None:
                geometry.set("x", str((page_width - 265) // 2))
                geometry.set("y", str(CAPABILITY_Y))
                geometry.set("width", str(CAPABILITY_WIDTH))
                geometry.set("height", str(CAPABILITY_HEIGHT))

    capability_x = (page_width - CAPABILITY_WIDTH) // 2
    capability_center_y = CAPABILITY_Y + CAPABILITY_HEIGHT // 2
    actor_x = 70
    input_start_x = max(360, capability_x - ((len(input_items) * 245 - 25) // 2))
    outcome_start_x = max(360, capability_x - ((len(outcome_items) * 245 - 25) // 2))
    external_x = page_width - 290
    actor_lane_x = capability_x - 70
    input_bus_y = BOTTOM_NODE_Y - 55
    outcome_bus_y = TOP_NODE_Y + NODE_HEIGHT + 55

    for index, stakeholder in enumerate(actor_items):
        node_id = f"actor-{index + 1}"
        y = ACTOR_START_Y + index * 105
        actor_center_y = y + NODE_HEIGHT // 2
        add_cell(root_cell, node_id, stakeholder, ACTOR_STYLE, actor_x, y, ACTOR_WIDTH, NODE_HEIGHT)
        add_edge(
            root_cell,
            f"edge-{node_id}-capability",
            node_id,
            "capability",
            "triggers or uses",
            points=[(actor_lane_x, actor_center_y), (actor_lane_x, capability_center_y)],
            style_suffix=f"exitX=1;exitY=0.5;entryX=0;entryY={relative_port(capability_center_y, CAPABILITY_Y, CAPABILITY_HEIGHT):.2f};",
        )

    for index, provider in enumerate(input_items):
        node_id = f"input-{index + 1}"
        x = input_start_x + index * 245
        source_x = x + NODE_WIDTH // 2
        target_x = distributed_port(index, len(input_items), capability_x, CAPABILITY_WIDTH)
        target_port = relative_port(target_x, capability_x, CAPABILITY_WIDTH)
        if provider.application:
            add_cell(root_cell, f"{node_id}-app", provider.application, APP_HEADER_STYLE, x, BOTTOM_HEADER_Y, NODE_WIDTH, 10)
        add_cell(root_cell, node_id, provider.label, SYSTEM_STYLE, x, BOTTOM_NODE_Y, NODE_WIDTH, NODE_HEIGHT)
        add_edge(
            root_cell,
            f"edge-{node_id}-capability",
            node_id,
            "capability",
            "provides input" if index == 0 else "",
            points=[(source_x, input_bus_y), (target_x, input_bus_y)],
            style_suffix=f"exitX=0.5;exitY=0;entryX={target_port:.2f};entryY=1;",
        )

    for index, outcome in enumerate(outcome_items):
        node_id = f"outcome-{index + 1}"
        x = outcome_start_x + index * 245
        source_x = distributed_port(index, len(outcome_items), capability_x, CAPABILITY_WIDTH)
        source_port = relative_port(source_x, capability_x, CAPABILITY_WIDTH)
        target_x = x + NODE_WIDTH // 2
        add_cell(root_cell, node_id, outcome, SYSTEM_STYLE, x, TOP_NODE_Y, NODE_WIDTH, NODE_HEIGHT)
        add_edge(
            root_cell,
            f"edge-capability-{node_id}",
            "capability",
            node_id,
            "gets data" if index == 0 else "",
            points=[(source_x, outcome_bus_y), (target_x, outcome_bus_y)],
            style_suffix=f"exitX={source_port:.2f};exitY=0;entryX=0.5;entryY=1;",
        )

    add_cell(
        root_cell,
        "external",
        f"Constraints and risks<br>{diagram_list(constraints, 'To be confirmed', limit=3)}",
        EXTERNAL_STYLE,
        external_x,
        EXTERNAL_Y,
        220,
        100,
    )
    add_edge(
        root_cell,
        "edge-capability-external",
        "capability",
        "external",
        "depends on",
        style_suffix="exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
    )
    tree.write(target, encoding="utf-8", xml_declaration=False)


def svg_text(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def wrapped_svg_lines(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for part in text.split("<br>"):
        wrapped = textwrap.wrap(part, width=width, break_long_words=False)
        lines.extend(wrapped if wrapped else [""])
    return lines


def svg_lines(text: str, x: int, y: int, line_height: int = 18, wrap_width: int = 24) -> str:
    lines = wrapped_svg_lines(text, wrap_width)
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(f'<tspan x="{x}" dy="{dy}">{svg_text(line)}</tspan>')
    return "".join(tspans)


def svg_box(
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str,
    stroke: str,
    label: str,
    *,
    font_size: int = 14,
    bold: bool = False,
    wrap_width: int = 24,
) -> str:
    weight = "700" if bold else "400"
    text_x = x + width // 2
    line_count = len(wrapped_svg_lines(label, wrap_width))
    text_y = y + max(26, (height - ((line_count - 1) * 18)) // 2)
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2"/>'
        f'<text x="{text_x}" y="{text_y}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="{font_size}" font-weight="{weight}" fill="#17201d">'
        f'{svg_lines(label, text_x, text_y, wrap_width=wrap_width)}</text>'
    )


def svg_app_header(x: int, y: int, width: int, label: str) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="10" fill="#000000" '
        'stroke="#000000" stroke-width="2"/>'
        f'<text x="{x + width // 2}" y="{y + 8}" text-anchor="middle" '
        'font-family="Helvetica, Arial, sans-serif" font-size="6" font-weight="700" '
        f'fill="#ffffff">{svg_text(label)}</text>'
    )


def svg_connector(points: list[tuple[int, int]], label: str = "", label_point: tuple[int, int] | None = None) -> str:
    point_value = " ".join(f"{x},{y}" for x, y in points)
    connector = (
        f'<polyline points="{point_value}" fill="none" stroke="#5d6964" stroke-width="2" '
        'marker-end="url(#arrow)"/>'
    )
    if not label:
        return connector
    label_x, label_y = label_point or points[len(points) // 2]
    return (
        connector
        + f'<rect x="{label_x - 62}" y="{label_y - 14}" width="124" height="20" fill="#fbfcfa"/>'
        + f'<text x="{label_x}" y="{label_y}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="12" fill="#5d6964">{svg_text(label)}</text>'
    )


def write_capability_svg(
    target: Path,
    capability_name: str,
    stakeholders: list[str],
    input_providers: list[str],
    outcomes: list[str],
    constraints: list[str],
) -> None:
    target_label = capability_label(capability_name)
    actor_items = diagram_items(stakeholders, "Stakeholders to confirm", ACTOR_GROUP_HEADINGS)
    input_items = data_provider_nodes(input_providers, "Data provider to confirm")
    outcome_items = diagram_items(outcomes, "Outcome to confirm")
    external_label = f"Constraints and risks<br>{diagram_list(constraints, 'To be confirmed', limit=2)}"
    max_items = max(len(actor_items), len(input_items), len(outcome_items))
    page_width = max(1169, 360 + max(len(input_items), len(outcome_items)) * 245)
    page_height = max(950, 700 + max_items * 100)
    capability_x = (page_width - CAPABILITY_WIDTH) // 2
    capability_y = CAPABILITY_Y
    actor_x = 70
    input_start_x = max(360, capability_x - ((len(input_items) * 245 - 25) // 2))
    outcome_start_x = max(360, capability_x - ((len(outcome_items) * 245 - 25) // 2))
    external_x = page_width - 290
    capability_center_y = capability_y + CAPABILITY_HEIGHT // 2
    actor_lane_x = capability_x - 70
    input_bus_y = BOTTOM_NODE_Y - 55
    outcome_bus_y = TOP_NODE_Y + NODE_HEIGHT + 55

    actor_nodes = []
    actor_edges = []
    for index, stakeholder in enumerate(actor_items):
        y = ACTOR_START_Y + index * 105
        actor_center_y = y + NODE_HEIGHT // 2
        actor_nodes.append(svg_box(actor_x, y, ACTOR_WIDTH, NODE_HEIGHT, "#fff3c4", "#b7791f", stakeholder, bold=True, wrap_width=20))
        actor_edges.append(
            svg_connector(
                [
                    (actor_x + ACTOR_WIDTH, actor_center_y),
                    (actor_lane_x, actor_center_y),
                    (actor_lane_x, capability_center_y),
                    (capability_x, capability_center_y),
                ],
                "triggers or uses",
                (actor_lane_x - 18, actor_center_y - 10),
            )
        )

    input_nodes = []
    input_edges = []
    for index, provider in enumerate(input_items):
        x = input_start_x + index * 245
        source_x = x + NODE_WIDTH // 2
        target_x = distributed_port(index, len(input_items), capability_x, CAPABILITY_WIDTH)
        if provider.application:
            input_nodes.append(svg_app_header(x, BOTTOM_HEADER_Y, NODE_WIDTH, provider.application))
        input_nodes.append(svg_box(x, BOTTOM_NODE_Y, NODE_WIDTH, NODE_HEIGHT, "#dae8fc", "#315f8f", provider.label, wrap_width=22))
        input_edges.append(
            svg_connector(
                [
                    (source_x, BOTTOM_NODE_Y),
                    (source_x, input_bus_y),
                    (target_x, input_bus_y),
                    (target_x, capability_y + CAPABILITY_HEIGHT),
                ],
                "provides input" if index == 0 else "",
                ((source_x + target_x) // 2, input_bus_y - 10),
            )
        )

    outcome_nodes = []
    outcome_edges = []
    for index, outcome in enumerate(outcome_items):
        x = outcome_start_x + index * 245
        source_x = distributed_port(index, len(outcome_items), capability_x, CAPABILITY_WIDTH)
        target_x = x + NODE_WIDTH // 2
        outcome_nodes.append(svg_box(x, TOP_NODE_Y, NODE_WIDTH, NODE_HEIGHT, "#dae8fc", "#315f8f", outcome, wrap_width=22))
        outcome_edges.append(
            svg_connector(
                [
                    (source_x, capability_y),
                    (source_x, outcome_bus_y),
                    (target_x, outcome_bus_y),
                    (target_x, TOP_NODE_Y + NODE_HEIGHT),
                ],
                "gets data" if index == 0 else "",
                ((source_x + target_x) // 2, outcome_bus_y - 10),
            )
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{page_width}" height="{page_height}" viewBox="0 0 {page_width} {page_height}" style="color-scheme: light; background: #fbfcfa;">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#5d6964"/>
</marker>
</defs>
<rect width="100%" height="100%" fill="#fbfcfa" pointer-events="none"/>
<text x="60" y="70" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700" fill="#17201d">{svg_text(target_label)} Context</text>
{"".join(actor_nodes)}
{svg_box(capability_x, capability_y, CAPABILITY_WIDTH, CAPABILITY_HEIGHT, "#d9eadf", "#0f766e", target_label, font_size=16, bold=True)}
{"".join(input_nodes)}
{"".join(outcome_nodes)}
{svg_box(external_x, EXTERNAL_Y, 220, 100, "#f8cecc", "#a3433f", external_label, wrap_width=24)}
{"".join(actor_edges)}
{"".join(input_edges)}
{"".join(outcome_edges)}
{svg_connector([(capability_x + CAPABILITY_WIDTH, capability_center_y), (external_x, capability_center_y)], "depends on", ((capability_x + CAPABILITY_WIDTH + external_x) // 2, capability_center_y - 10))}
</svg>
'''
    target.write_text(svg, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capability_name", help="Capability name shown as the central node.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Folder where diagram files should be written.")
    parser.add_argument("--basename", default=DEFAULT_BASENAME, help="Diagram filename basename. Defaults to capability-overview.")
    parser.add_argument("--stakeholder", action="append", default=[], help="Stakeholder, user, team, or actor. Repeat for multiple actors.")
    parser.add_argument("--input-provider", action="append", default=[], help="Input provider or source system. Repeat for multiple providers.")
    parser.add_argument("--existing-system", action="append", default=[], help="Alias for --input-provider.")
    parser.add_argument("--outcome", action="append", default=[], help="Produced outcome, consumer, or downstream capability. Repeat for multiple outcomes.")
    parser.add_argument("--related-capability", action="append", default=[], help="Alias for --outcome.")
    parser.add_argument("--constraint", action="append", default=[], help="External dependency, risk, or constraint. Repeat for multiple constraints.")
    parser.add_argument("--pain-point", action="append", default=[], help="Alias for --constraint.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    input_providers = args.input_provider + args.existing_system
    outcomes = args.outcome + args.related_capability
    constraints = args.constraint + args.pain_point
    drawio_target = output_dir / f"{args.basename}.drawio"
    svg_target = output_dir / f"{args.basename}.svg"
    write_capability_drawio(
        drawio_target,
        args.capability_name,
        args.stakeholder,
        input_providers,
        outcomes,
        constraints,
    )
    write_capability_svg(
        svg_target,
        args.capability_name,
        args.stakeholder,
        input_providers,
        outcomes,
        constraints,
    )
    print(drawio_target)
    print(svg_target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
