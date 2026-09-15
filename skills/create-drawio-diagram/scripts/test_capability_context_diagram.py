"""Regression checks for capability context routing and export geometry."""

import importlib.util
import itertools
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


SCRIPT = Path(__file__).with_name("write-capability-context-diagram.py")
SPEC = importlib.util.spec_from_file_location("capability_context", SCRIPT)
diagram = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = diagram
SPEC.loader.exec_module(diagram)


def segments(points):
    return [(a, b) for a, b in zip(points, points[1:]) if a != b]


def intersects(first, second):
    """Inclusive intersection catches crossings, shared trunks, and touches."""
    (ax, ay), (bx, by) = first
    (cx, cy), (dx, dy) = second
    return (
        max(min(ax, bx), min(cx, dx)) <= min(max(ax, bx), max(cx, dx))
        and max(min(ay, by), min(cy, dy)) <= min(max(ay, by), max(cy, dy))
    )


def touches_box(segment, box):
    (ax, ay), (bx, by) = segment
    left, top, right, bottom = box
    return (
        max(min(ax, bx), left) <= min(max(ax, bx), right)
        and max(min(ay, by), top) <= min(max(ay, by), bottom)
    )


def inputs(actors=2, providers=4, outcomes=2):
    return (
        "Order Management",
        [f"Actor {i + 1}" for i in range(actors)],
        [f"Application {i + 1}: Data object {i + 1}" for i in range(providers)],
        [f"Consumer {i + 1}" for i in range(outcomes)],
        ["Managed service dependency", "One cart per session", "Availability to confirm"],
    )


class CapabilityContextTests(unittest.TestCase):
    def assert_clean(self, layout):
        nodes = {node.id: node for node in layout.nodes}
        for first, second in itertools.combinations(layout.nodes, 2):
            self.assertFalse(
                first.x < second.right and second.x < first.right
                and first.y < second.bottom and second.y < first.bottom,
                f"Overlapping nodes: {first.id}, {second.id}",
            )
        for first, second in itertools.combinations(layout.edges, 2):
            for a, b in itertools.product(segments(first.points), segments(second.points)):
                self.assertFalse(intersects(a, b), f"Crossing edges: {first.id}, {second.id}: {a}, {b}")
        for edge in layout.edges:
            for a, b in segments(edge.points):
                self.assertTrue(a[0] == b[0] or a[1] == b[1], f"Diagonal edge: {edge.id}")
                for node in layout.nodes:
                    # Endpoint boxes may be touched only at their boundary.
                    clearance = -0.01 if node.id in {edge.source, edge.target} else 9.99
                    box = (node.x - clearance, node.y - clearance, node.right + clearance, node.bottom + clearance)
                    self.assertFalse(touches_box((a, b), box), f"Edge {edge.id} hits {node.id}")
            for endpoint, node_id in ((edge.points[0], edge.source), (edge.points[-1], edge.target)):
                node = nodes[node_id]
                x, y = endpoint
                self.assertTrue(
                    (x in (node.x, node.right) and node.y <= y <= node.bottom)
                    or (y in (node.y, node.bottom) and node.x <= x <= node.right),
                    f"Unattached edge: {edge.id}",
                )
                if node.application:
                    self.assertGreater(y, node.y + 10, f"Edge through application header: {edge.id}")
        labels = []
        for edge in layout.edges:
            if not edge.label:
                continue
            x, y = edge.label_point
            box = (x - 62, y - 10, x + 62, y + 10)
            labels.append((edge.id, box))
            for node in layout.nodes:
                self.assertFalse(
                    box[0] < node.right and node.x < box[2]
                    and box[1] < node.bottom and node.y < box[3],
                    f"Label {edge.id} overlaps {node.id}",
                )
            for other in layout.edges:
                for segment in segments(other.points):
                    self.assertFalse(touches_box(segment, box), f"Label {edge.id} obscures {other.id}")
        for (first, a), (second, b) in itertools.combinations(labels, 2):
            self.assertFalse(
                a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3],
                f"Labels overlap: {first}, {second}",
            )
        self.assertEqual(layout.height - max(node.bottom for node in layout.nodes), 60)
        for node in layout.nodes:
            self.assertGreaterEqual(node.x, 60)
            self.assertLessEqual(node.right, layout.width - 60)

    def test_four_providers_two_actors_two_consumers(self):
        self.assert_clean(diagram.build_layout(*inputs()))

    def test_empty_single_odd_even_and_dense_zones(self):
        for counts in itertools.product((0, 1, 2, 3, 4, 6, 10), repeat=3):
            with self.subTest(counts=counts):
                self.assert_clean(diagram.build_layout(*inputs(*counts)))

    def test_multiline_provider_and_long_labels(self):
        args = (
            "Order Management",
            ["Customer support and order service team", "Operations", "Customer"],
            ["Business platform\nCustomer account\nCustomer order\nDelivery address"],
            ["Order fulfillment and delivery coordination", "Customer communication"],
            ["Managed service with an availability dependency", "One active order per customer session"],
        )
        layout = diagram.build_layout(*args)
        self.assertEqual(len([node for node in layout.nodes if node.application == "Business platform"]), 3)
        self.assert_clean(layout)

    def test_drawio_and_svg_share_bounds_routes_and_labels(self):
        args = inputs()
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "capability-overview.drawio"
            export = source.with_suffix(".svg")
            diagram.write_capability_drawio(source, *args)
            diagram.write_capability_svg(export, *args)
            drawio = ET.parse(source)
            svg = ET.parse(export).getroot()
        graph = drawio.find(".//mxGraphModel")
        self.assertEqual(graph.get("pageWidth"), svg.get("width"))
        self.assertEqual(graph.get("pageHeight"), svg.get("height"))
        cells = {cell.get("id"): cell for cell in drawio.findall(".//mxCell")}
        lines = svg.findall("{http://www.w3.org/2000/svg}polyline")
        edges = [cell for cell in cells.values() if cell.get("edge") == "1"]
        self.assertEqual(len(edges), len(lines))
        for edge, line in zip(edges, lines):
            style = dict(item.split("=", 1) for item in edge.get("style").split(";") if "=" in item)
            source = cells[edge.get("source")].find("mxGeometry")
            target = cells[edge.get("target")].find("mxGeometry")
            first = (
                float(source.get("x")) + float(style["exitX"]) * float(source.get("width")),
                float(source.get("y")) + float(style["exitY"]) * float(source.get("height")),
            )
            last = (
                float(target.get("x")) + float(style["entryX"]) * float(target.get("width")),
                float(target.get("y")) + float(style["entryY"]) * float(target.get("height")),
            )
            waypoints = [
                (float(point.get("x")), float(point.get("y")))
                for point in edge.findall("mxGeometry/Array/mxPoint")
            ]
            exported = [tuple(map(float, point.split(","))) for point in line.get("points").split()]
            self.assertEqual(len(exported), len(waypoints) + 2)
            for expected, actual in zip([first, *waypoints, last], exported):
                for a, b in zip(expected, actual):
                    self.assertAlmostEqual(a, b, places=5)
            if edge.get("value"):
                self.assertIsNotNone(edge.find("mxGeometry/mxPoint[@as='offset']"))
                self.assertIn(edge.get("value"), "".join(svg.itertext()))
        self.assertNotIn("Application Name", ET.tostring(drawio.getroot(), encoding="unicode"))
        self.assertIn("Availability to confirm", "".join(svg.itertext()))


if __name__ == "__main__":
    unittest.main()
