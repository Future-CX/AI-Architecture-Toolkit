#!/usr/bin/env python3
"""Check explicit connector geometry in flat, uncompressed solution Draw.io files.

Detect crossings, shared segments/ports, and component/header collisions before
export. Render the SVG afterwards to check text, arrowheads, and visual spacing.
"""

from __future__ import annotations

import argparse
import itertools
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


EPSILON = 0.0001
CLEARANCE = 10


def style_of(cell: ET.Element) -> dict[str, str]:
    return dict(item.split("=", 1) for item in cell.get("style", "").split(";") if "=" in item)


def number(value: str | None) -> float:
    result = float(value if value is not None else 0)
    if not math.isfinite(result):
        raise ValueError("Geometry must contain finite coordinates.")
    return result


def bounds(segment):
    (ax, ay), (bx, by) = segment
    return min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)


def intersects(first, second):
    return (
        max(first[0], second[0]) <= min(first[2], second[2])
        and max(first[1], second[1]) <= min(first[3], second[3])
    )


def same(first: float, second: float) -> bool:
    return abs(first - second) <= EPSILON


def is_application_header(style: dict[str, str], box) -> bool:
    return (
        style.get("fillColor", "").lower() == "#000000"
        and style.get("strokeColor", "").lower() == "#000000"
        and same(box[3] - box[1], 10)
    )


def allows_top_center_endpoint(
    header_id: str,
    header_box,
    shape_styles: dict[str, dict[str, str]],
    endpoint_shapes: tuple[str, str],
    endpoint_boxes: tuple[tuple[float, float, float, float], tuple[float, float, float, float]],
    endpoints: list[tuple[float, float]],
    segments,
) -> bool:
    """Allow only a vertical endpoint at a composite component's outer top-center."""
    if not is_application_header(shape_styles[header_id], header_box):
        return False
    for index, (_shape_id, component_box, endpoint) in enumerate(zip(endpoint_shapes, endpoint_boxes, endpoints)):
        left, top, right, _ = component_box
        if not (
            same(header_box[0], left)
            and same(header_box[1], top)
            and same(header_box[2], right)
            and same(endpoint[0], (left + right) / 2)
            and same(endpoint[1], top)
        ):
            continue
        endpoint_segment_index = 0 if index == 0 else len(segments) - 1
        colliding = [
            segment_index
            for segment_index, segment in enumerate(segments)
            if intersects(bounds(segment), header_box)
        ]
        if colliding != [endpoint_segment_index]:
            return False
        segment = segments[endpoint_segment_index]
        other = segment[1] if index == 0 else segment[0]
        return same(other[0], endpoint[0]) and other[1] < top - EPSILON
    return False


def check_graph(graph: ET.Element) -> list[str]:
    cells = list(graph.iter("mxCell"))
    ids = [cell.get("id") for cell in cells]
    if None in ids or len(ids) != len(set(ids)):
        return ["Every cell needs a unique ID."]
    shapes = {}
    shape_styles = {}
    for cell in cells:
        if cell.get("vertex") != "1":
            continue
        id = cell.get("id")
        geometry = cell.find("mxGeometry")
        if cell.get("parent") != "1" or geometry is None or geometry.get("relative") == "1":
            return [f"{id}: use flat components with absolute geometry; nested groups need flattening for this check."]
        style = style_of(cell)
        if number(style.get("rotation")) != 0 or style.get("flipH") == "1" or style.get("flipV") == "1":
            return [f"{id}: rotated or flipped shapes need normalizing before this geometry check."]
        # Layer backgrounds and decorative rules are not component obstacles.
        if style.get("shape") == "line":
            continue
        if style.get("strokeColor") == "none" and style.get("fillColor", "none") != "none":
            continue
        x, y, width, height = [number(geometry.get(key)) for key in ("x", "y", "width", "height")]
        if width <= 0 or height <= 0:
            return [f"{id}: component width and height must be positive."]
        shapes[id] = (x, y, x + width, y + height)
        shape_styles[id] = style

    errors = []
    routes = {}
    for cell in cells:
        if cell.get("edge") != "1":
            continue
        id = cell.get("id")
        if cell.get("parent") != "1" or cell.find("mxGeometry") is None:
            errors.append(f"{id}: use root-level connectors with explicit geometry.")
            continue
        source, target = cell.get("source"), cell.get("target")
        if source not in shapes or target not in shapes:
            errors.append(f"{id}: attach both endpoints to component IDs.")
            continue
        style = style_of(cell)
        required = ("exitX", "exitY", "entryX", "entryY")
        if any(key not in style for key in required) or any(
            style.get(key) != value
            for key, value in (("noEdgeStyle", "1"), ("exitPerimeter", "0"), ("entryPerimeter", "0"))
        ):
            errors.append(f"{id}: automatic routing cannot be checked; set explicit ports, waypoints, noEdgeStyle=1, exitPerimeter=0, entryPerimeter=0.")
            continue
        endpoints = []
        for node_id, prefix in ((source, "exit"), (target, "entry")):
            px, py = number(style[prefix + "X"]), number(style[prefix + "Y"])
            if not (0 <= px <= 1 and 0 <= py <= 1 and (px in (0, 1) or py in (0, 1))):
                errors.append(f"{id}: {prefix} port must be on the component boundary.")
            left, top, right, bottom = shapes[node_id]
            endpoints.append((left + px * (right - left), top + py * (bottom - top)))
        waypoints = [
            (number(point.get("x")), number(point.get("y")))
            for point in cell.findall("mxGeometry/Array[@as='points']/mxPoint")
        ]
        points = [endpoints[0], *waypoints, endpoints[1]]
        segments = [
            (a, b) for a, b in zip(points, points[1:])
            if abs(a[0] - b[0]) > EPSILON or abs(a[1] - b[1]) > EPSILON
        ]
        if not segments:
            errors.append(f"{id}: connector has no visible path.")
            continue
        if any(abs(a[0] - b[0]) > EPSILON and abs(a[1] - b[1]) > EPSILON for a, b in segments):
            errors.append(f"{id}: route every segment orthogonally.")
            continue
        routes[id] = segments
        endpoint_shapes = (source, target)
        endpoint_boxes = (shapes[source], shapes[target])
        for shape_id, box in shapes.items():
            # Endpoints may touch their own boundary, never their interior.
            padding = -EPSILON if shape_id in (source, target) else CLEARANCE - EPSILON
            obstacle = (box[0] - padding, box[1] - padding, box[2] + padding, box[3] + padding)
            if any(intersects(bounds(segment), obstacle) for segment in segments):
                if allows_top_center_endpoint(
                    shape_id, box, shape_styles, endpoint_shapes, endpoint_boxes, endpoints, segments,
                ):
                    continue
                errors.append(f"{id}: component/header collision or insufficient clearance at {shape_id}.")
        for (i, a), (j, b) in itertools.combinations(enumerate(segments), 2):
            if j > i + 1 and intersects(bounds(a), bounds(b)):
                errors.append(f"{id}: connector crosses or reuses its own path.")
                break

    for (first_id, first), (second_id, second) in itertools.combinations(routes.items(), 2):
        if any(intersects(bounds(a), bounds(b)) for a, b in itertools.product(first, second)):
            errors.append(f"{first_id} / {second_id}: connectors cross, touch, or share a segment/port.")
    return errors


def check_file(path: Path) -> list[str]:
    try:
        tree = ET.parse(path)
        diagrams = tree.findall("diagram")
        if not diagrams or any(diagram.find("mxGraphModel") is None for diagram in diagrams):
            return ["Save as uncompressed Draw.io XML with an mxGraphModel on every page before checking."]
        errors = []
        for index, diagram in enumerate(diagrams, 1):
            name = diagram.get("name", f"Page {index}")
            errors.extend(f"{name}: {error}" for error in check_graph(diagram.find("mxGraphModel")))
        return errors
    except (OSError, ET.ParseError, ValueError) as error:
        return [f"Cannot check diagram: {error}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drawio", type=Path, help="Solution architecture .drawio source to check.")
    args = parser.parse_args()
    errors = check_file(args.drawio)
    if errors:
        print("FAIL: connector geometry needs attention.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: no connector crossings, shared segments/ports, or component/header collisions.")
    print("Render the SVG and inspect labels, arrowheads, and spacing before accepting it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
