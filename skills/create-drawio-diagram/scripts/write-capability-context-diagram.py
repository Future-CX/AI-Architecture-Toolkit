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
PAGE_MARGIN = 60
NODE_GAP = 60
LANE_SPACING = 32
PORT_CLEARANCE = 40
ACTOR_WIDTH = 190
NODE_WIDTH = 210
NODE_HEIGHT = 80
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


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    style: str
    x: int
    y: int
    width: int
    height: int
    wrap_width: int = 22
    application: str | None = None

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    points: list[tuple[int, int]]
    label: str = ""
    label_point: tuple[int, int] | None = None


@dataclass(frozen=True)
class Layout:
    title: str
    nodes: list[Node]
    edges: list[Edge]
    width: int
    height: int


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


def distributed_port(index: int, count: int, start: int, size: int, padding: int = 34) -> int:
    if count <= 1:
        return start + size // 2
    usable = size - padding * 2
    return start + padding + round((usable * index) / (count - 1))


def fan_depths(outer: list[int], inner: list[int]) -> list[int]:
    """Order bends from the capability outward without crossing neighboring paths.

    Both endpoint lists are ordered along their boundary. Routes bending toward
    larger coordinates nest in forward order; routes bending toward smaller
    coordinates nest in reverse order. Opposing fans occupy disjoint intervals.
    """
    depths = [0] * len(outer)
    for selected in (
        [i for i in range(len(outer)) if outer[i] < inner[i]],
        [i for i in reversed(range(len(outer))) if outer[i] > inner[i]],
    ):
        for depth, index in enumerate(selected):
            depths[index] = depth
    return depths


def node_height(label: str, wrap_width: int, minimum: int = NODE_HEIGHT) -> int:
    return max(minimum, len(wrapped_svg_lines(label, wrap_width)) * 18 + 34)


def row_positions(count: int, center_x: int) -> list[int]:
    width = count * NODE_WIDTH + (count - 1) * NODE_GAP
    start = center_x - width // 2
    return [start + i * (NODE_WIDTH + NODE_GAP) for i in range(count)]


def relationship_label(
    points: list[tuple[int, int]],
    side: int = -1,
    vertical_segment: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> tuple[int, int]:
    # Prefer a horizontal segment that can hold the whole label. For a short or
    # straight route, use whitespace beside the longest vertical segment.
    segments = list(zip(points, points[1:]))
    for (x1, y1), (x2, y2) in segments:
        if y1 == y2 and abs(x2 - x1) >= 144:
            return ((x1 + x2) // 2, y1 - 16)
    (x1, y1), (x2, y2) = vertical_segment or max(segments, key=lambda pair: abs(pair[1][1] - pair[0][1]))
    return (x1 + side * 76, (y1 + y2) // 2)


def build_layout(
    capability_name: str,
    stakeholders: list[str],
    input_providers: list[str],
    outcomes: list[str],
    constraints: list[str],
) -> Layout:
    target_label = capability_label(capability_name)
    actors = diagram_items(stakeholders, "Stakeholders to confirm", ACTOR_GROUP_HEADINGS)
    providers = data_provider_nodes(input_providers, "Data provider to confirm")
    consumers = diagram_items(outcomes, "Outcome to confirm")
    external_label = f"Constraints and risks<br>{diagram_list(constraints, 'To be confirmed', limit=3)}"
    actor_heights = [node_height(label, 20) for label in actors]
    actor_stack_height = sum(actor_heights) + 30 * (len(actors) - 1)
    capability_width = max(CAPABILITY_WIDTH, 68 + (max(len(providers), len(consumers)) - 1) * LANE_SPACING)
    capability_height = max(node_height(target_label, 26, CAPABILITY_HEIGHT), 56 + (len(actors) - 1) * LANE_SPACING)
    external_height = node_height(external_label, 24, 100)
    middle_height = max(actor_stack_height, capability_height, external_height)
    row_count = max(len(providers), len(consumers))
    row_width = row_count * NODE_WIDTH + (row_count - 1) * NODE_GAP
    actor_gap = 220 + ((len(actors) - 1) // 2) * LANE_SPACING
    center_x = max(PAGE_MARGIN + row_width // 2, PAGE_MARGIN + ACTOR_WIDTH + actor_gap + capability_width // 2)
    capability_x = center_x - capability_width // 2
    provider_xs = row_positions(len(providers), center_x)
    consumer_xs = row_positions(len(consumers), center_x)
    provider_ports = [distributed_port(i, len(providers), capability_x, capability_width) for i in range(len(providers))]
    consumer_ports = [distributed_port(i, len(consumers), capability_x, capability_width) for i in range(len(consumers))]
    # Named applications cover the top border. Leave through a side port and
    # use a dedicated shaft in the gap beside the provider instead.
    provider_shafts = [
        x + (NODE_WIDTH + 20 if x + NODE_WIDTH // 2 <= center_x else -20)
        if provider.application else x + NODE_WIDTH // 2
        for x, provider in zip(provider_xs, providers)
    ]
    consumer_centers = [x + NODE_WIDTH // 2 for x in consumer_xs]
    input_depths = fan_depths(provider_shafts, provider_ports)
    outcome_depths = fan_depths(consumer_centers, consumer_ports)
    consumer_height = max(node_height(label, 22) for label in consumers)
    provider_height = max(node_height(provider.label, 22) for provider in providers)
    top_gap = 120 + max(outcome_depths) * LANE_SPACING
    bottom_gap = 120 + max(input_depths) * LANE_SPACING
    middle_y = TOP_NODE_Y + consumer_height + top_gap
    center_y = middle_y + middle_height // 2
    capability_y = center_y - capability_height // 2
    provider_y = middle_y + middle_height + bottom_gap
    capability = Node(
        "capability", target_label, CAPABILITY_STYLE,
        capability_x, capability_y, capability_width, capability_height, 26,
    )
    external = Node(
        "external", external_label, EXTERNAL_STYLE,
        capability.right + 200, center_y - external_height // 2, 220, external_height, 24,
    )
    nodes = [capability, external]
    edges = []

    actor_y = center_y - actor_stack_height // 2
    actor_nodes = []
    for i, (label, height) in enumerate(zip(actors, actor_heights)):
        actor_nodes.append(Node(f"actor-{i + 1}", label, ACTOR_STYLE, PAGE_MARGIN, actor_y, ACTOR_WIDTH, height, 20))
        actor_y += height + 30
    actor_centers = [node.y + node.height // 2 for node in actor_nodes]
    actor_ports = [distributed_port(i, len(actors), capability.y, capability.height, padding=28) for i in range(len(actors))]
    actor_depths = fan_depths(actor_centers, actor_ports)
    for i, node in enumerate(actor_nodes):
        lane_x = capability.x - PORT_CLEARANCE - actor_depths[i] * LANE_SPACING
        points = [
            (node.right, actor_centers[i]), (lane_x, actor_centers[i]),
            (lane_x, actor_ports[i]), (capability.x, actor_ports[i]),
        ]
        nodes.append(node)
        edges.append(Edge(
            f"edge-{node.id}-capability", node.id, capability.id, points,
            "triggers or uses" if i == 0 else "", relationship_label(points),
        ))

    for i, provider in enumerate(providers):
        node = Node(
            f"input-{i + 1}", provider.label, SYSTEM_STYLE,
            provider_xs[i], provider_y, NODE_WIDTH, provider_height, application=provider.application,
        )
        shaft_x = provider_shafts[i]
        lane_y = middle_y + middle_height + PORT_CLEARANCE + input_depths[i] * LANE_SPACING
        if provider.application:
            source_x = node.right if shaft_x > node.right else node.x
            source_y = node.y + node.height // 2
            points = [(source_x, source_y), (shaft_x, source_y), (shaft_x, lane_y)]
        else:
            points = [(shaft_x, node.y), (shaft_x, lane_y)]
        label_segment = (points[-2], points[-1])
        points.extend([(provider_ports[i], lane_y), (provider_ports[i], capability.bottom)])
        nodes.append(node)
        edges.append(Edge(
            f"edge-{node.id}-capability", node.id, capability.id, points,
            "provides input" if i == 0 else "",
            relationship_label(points, side=1 if len(providers) == 1 else -1, vertical_segment=label_segment),
        ))

    for i, label in enumerate(consumers):
        node = Node(f"outcome-{i + 1}", label, SYSTEM_STYLE, consumer_xs[i], TOP_NODE_Y, NODE_WIDTH, consumer_height)
        lane_y = middle_y - PORT_CLEARANCE - outcome_depths[i] * LANE_SPACING
        points = [
            (consumer_ports[i], capability.y), (consumer_ports[i], lane_y),
            (consumer_centers[i], lane_y), (consumer_centers[i], node.bottom),
        ]
        nodes.append(node)
        edges.append(Edge(
            f"edge-capability-{node.id}", capability.id, node.id, points,
            "gets data" if i == 0 else "",
            relationship_label(points, vertical_segment=(points[-2], points[-1])),
        ))

    points = [(capability.right, center_y), (external.x, center_y)]
    edges.append(Edge(
        "edge-capability-external", capability.id, external.id, points,
        "depends on", relationship_label(points),
    ))
    # Fit the page to actual content, including routing and labels. Node counts
    # determine needed corridors above; they must not add empty space below.
    width = max(
        max(node.right for node in nodes),
        max(x for edge in edges for x, _ in edge.points),
        max(edge.label_point[0] + 62 for edge in edges if edge.label),
    ) + PAGE_MARGIN
    height = max(
        max(node.bottom for node in nodes),
        max(y for edge in edges for _, y in edge.points),
        max(edge.label_point[1] + 10 for edge in edges if edge.label),
    ) + PAGE_MARGIN
    return Layout(f"{target_label} Context", nodes, edges, width, height)


def edge_midpoint(points: list[tuple[int, int]]) -> tuple[float, float]:
    lengths = [abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in zip(points, points[1:])]
    remaining = sum(lengths) / 2
    for ((x1, y1), (x2, y2)), length in zip(zip(points, points[1:]), lengths):
        if length and remaining <= length:
            ratio = remaining / length
            return (x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio)
        remaining -= length
    return points[-1]


def write_capability_drawio(
    target: Path,
    capability_name: str,
    stakeholders: list[str],
    input_providers: list[str],
    outcomes: list[str],
    constraints: list[str],
) -> None:
    layout = build_layout(capability_name, stakeholders, input_providers, outcomes, constraints)
    tree = ET.parse(DRAWIO_TEMPLATE)
    root = tree.getroot()
    graph_model = root.find(".//mxGraphModel")
    root_cell = root.find(".//root")
    if graph_model is None or root_cell is None:
        raise ValueError(f"Invalid Draw.io template: {DRAWIO_TEMPLATE}")
    graph_model.set("pageWidth", str(layout.width))
    graph_model.set("pageHeight", str(layout.height))
    # Keep the template's graph settings and title style, replacing all starter
    # shapes and application headers so no placeholder survives generation.
    for cell in list(root_cell):
        if cell.attrib.get("id") not in {"0", "1", "title"}:
            root_cell.remove(cell)
    title = root_cell.find("mxCell[@id='title']")
    if title is not None:
        title.set("value", layout.title)
        title.find("mxGeometry").set("width", str(layout.width - PAGE_MARGIN * 2))
    for node in layout.nodes:
        style = node.style if node.id == "capability" else node.style + "fontSize=14;"
        cell = ET.SubElement(root_cell, "mxCell", {
            "id": node.id, "parent": "1", "vertex": "1", "value": node.label, "style": style,
        })
        ET.SubElement(cell, "mxGeometry", {
            "x": str(node.x), "y": str(node.y),
            "width": str(node.width), "height": str(node.height), "as": "geometry",
        })
        if node.application:
            header = ET.SubElement(root_cell, "mxCell", {
                "id": f"{node.id}-app", "parent": "1", "vertex": "1",
                "value": node.application, "style": APP_HEADER_STYLE,
            })
            ET.SubElement(header, "mxGeometry", {
                "x": str(node.x), "y": str(node.y), "width": str(node.width), "height": "10", "as": "geometry",
            })
    nodes = {node.id: node for node in layout.nodes}
    for edge in layout.edges:
        source, destination = nodes[edge.source], nodes[edge.target]
        start, end = edge.points[0], edge.points[-1]
        ports = (
            f"exitX={(start[0] - source.x) / source.width:.8f};"
            f"exitY={(start[1] - source.y) / source.height:.8f};"
            f"entryX={(end[0] - destination.x) / destination.width:.8f};"
            f"entryY={(end[1] - destination.y) / destination.height:.8f};"
        )
        # Preserve the explicit orthogonal polyline instead of letting the
        # editor's automatic router choose different bends or shared segments.
        style = CONNECTOR_STYLE + "noEdgeStyle=1;exitPerimeter=0;entryPerimeter=0;fontSize=12;" + ports
        cell = ET.SubElement(root_cell, "mxCell", {
            "id": edge.id, "parent": "1", "edge": "1", "source": edge.source,
            "target": edge.target, "value": edge.label, "style": style,
        })
        geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
        points = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in edge.points[1:-1]:
            ET.SubElement(points, "mxPoint", {"x": str(x), "y": str(y)})
        if edge.label and edge.label_point:
            mid_x, mid_y = edge_midpoint(edge.points)
            ET.SubElement(geometry, "mxPoint", {
                "x": str(edge.label_point[0] - mid_x), "y": str(edge.label_point[1] - mid_y), "as": "offset",
            })
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
        + f'<rect x="{label_x - 62}" y="{label_y - 10}" width="124" height="20" fill="#fbfcfa"/>'
        + f'<text x="{label_x}" y="{label_y + 4}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
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
    layout = build_layout(capability_name, stakeholders, input_providers, outcomes, constraints)
    boxes = []
    for node in layout.nodes:
        style = dict(item.split("=", 1) for item in node.style.split(";") if "=" in item)
        boxes.append(svg_box(
            node.x, node.y, node.width, node.height, style["fillColor"], style["strokeColor"], node.label,
            font_size=int(style.get("fontSize", "14")), bold=style.get("fontStyle") == "1", wrap_width=node.wrap_width,
        ))
        if node.application:
            boxes.append(svg_app_header(node.x, node.y, node.width, node.application))
    connectors = [svg_connector(edge.points, edge.label, edge.label_point) for edge in layout.edges]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{layout.width}" height="{layout.height}" viewBox="0 0 {layout.width} {layout.height}" style="color-scheme: light; background: #fbfcfa;">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#5d6964"/>
</marker>
</defs>
<rect width="100%" height="100%" fill="#fbfcfa" pointer-events="none"/>
<text x="60" y="70" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700" fill="#17201d">{svg_text(layout.title)}</text>
{"".join(boxes)}
{"".join(connectors)}
</svg>
'''
    target.write_text(svg, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capability_name", help="Capability name shown as the central node.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Required diagrams/ subfolder where diagram files should be written.",
    )
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
