"""Regression checks for crossings and unsupported automatic routing."""

import copy
import importlib.util
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("solution_routing", SCRIPT_DIR / "check-solution-architecture-routing.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def fixture(crossing=False):
    graph = ET.Element("mxGraphModel")
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    for id, x, y in [("left", 0, 100), ("right", 300, 100), ("top", 150 if crossing else 400, 0), ("bottom", 150 if crossing else 400, 240)]:
        node = ET.SubElement(root, "mxCell", {
            "id": id, "parent": "1", "vertex": "1", "style": "fillColor=#ffffff;strokeColor=#17201d;",
        })
        ET.SubElement(node, "mxGeometry", {
            "x": str(x), "y": str(y), "width": "40", "height": "40", "as": "geometry",
        })
    for id, source, target, ports in [
        ("horizontal", "left", "right", "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"),
        ("vertical", "top", "bottom", "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"),
    ]:
        edge = ET.SubElement(root, "mxCell", {
            "id": id, "parent": "1", "edge": "1", "source": source, "target": target,
            "style": "noEdgeStyle=1;exitPerimeter=0;entryPerimeter=0;" + ports,
        })
        ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})
    return graph


class SolutionRoutingTests(unittest.TestCase):
    def test_template_has_no_geometry_collisions(self):
        template = SCRIPT_DIR.parent / "templates" / "solution-architecture-diagram.drawio"
        self.assertEqual(checker.check_file(template), [])

    def test_separate_paths_are_accepted(self):
        self.assertEqual(checker.check_graph(fixture()), [])

    def test_crossing_is_rejected(self):
        self.assertTrue(any("connectors cross" in error for error in checker.check_graph(fixture(crossing=True))))

    def test_shared_segments_and_ports_are_rejected(self):
        graph = fixture()
        edge = copy.deepcopy(graph.find(".//mxCell[@id='horizontal']"))
        edge.set("id", "duplicate-route")
        graph.find("root").append(edge)
        self.assertTrue(any("share a segment/port" in error for error in checker.check_graph(graph)))

    def test_component_obstruction_is_rejected(self):
        graph = fixture()
        blocker = graph.find(".//mxCell[@id='top']/mxGeometry")
        blocker.set("x", "120")
        blocker.set("y", "100")
        self.assertTrue(any("collision" in error and "top" in error for error in checker.check_graph(graph)))

    def test_application_header_allows_outer_top_center_endpoint(self):
        graph = fixture()
        header = ET.SubElement(graph.find("root"), "mxCell", {
            "id": "right-app", "parent": "1", "vertex": "1",
            "style": "fillColor=#000000;strokeColor=#000000;fontColor=#ffffff;",
        })
        ET.SubElement(header, "mxGeometry", {
            "x": "300", "y": "100", "width": "40", "height": "10", "as": "geometry",
        })
        edge = graph.find(".//mxCell[@id='horizontal']")
        edge.set("style", edge.get("style").replace("entryX=0;entryY=0.5", "entryX=0.5;entryY=0"))
        points = ET.SubElement(edge.find("mxGeometry"), "Array", {"as": "points"})
        for x, y in [(280, 120), (280, 80), (320, 80)]:
            ET.SubElement(points, "mxPoint", {"x": str(x), "y": str(y)})
        self.assertEqual(checker.check_graph(graph), [])

    def test_application_header_rejects_route_along_its_top_edge(self):
        graph = fixture()
        header = ET.SubElement(graph.find("root"), "mxCell", {
            "id": "right-app", "parent": "1", "vertex": "1",
            "style": "fillColor=#000000;strokeColor=#000000;fontColor=#ffffff;",
        })
        ET.SubElement(header, "mxGeometry", {
            "x": "300", "y": "100", "width": "40", "height": "10", "as": "geometry",
        })
        edge = graph.find(".//mxCell[@id='horizontal']")
        edge.set("style", edge.get("style").replace("entryX=0;entryY=0.5", "entryX=0.5;entryY=0"))
        points = ET.SubElement(edge.find("mxGeometry"), "Array", {"as": "points"})
        for x, y in [(280, 120), (280, 100)]:
            ET.SubElement(points, "mxPoint", {"x": str(x), "y": str(y)})
        self.assertTrue(any("right-app" in error for error in checker.check_graph(graph)))

    def test_automatic_or_detached_routes_are_not_silently_accepted(self):
        graph = fixture()
        edge = graph.find(".//mxCell[@id='horizontal']")
        edge.set("style", "edgeStyle=orthogonalEdgeStyle;")
        self.assertTrue(any("automatic routing cannot be checked" in error for error in checker.check_graph(graph)))
        edge.set("source", "missing")
        self.assertTrue(any("attach both endpoints" in error for error in checker.check_graph(graph)))

    def test_nested_or_rotated_components_require_normalization(self):
        graph = fixture()
        node = graph.find(".//mxCell[@id='left']")
        node.set("parent", "group")
        self.assertTrue(any("flat components" in error for error in checker.check_graph(graph)))
        node.set("parent", "1")
        node.set("style", node.get("style") + "rotation=90;")
        self.assertTrue(any("rotated" in error for error in checker.check_graph(graph)))

    def test_compressed_pages_are_not_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "compressed.drawio"
            path.write_text('<mxfile><diagram name="Compressed">compressed-content</diagram></mxfile>')
            self.assertTrue(any("uncompressed" in error for error in checker.check_file(path)))


if __name__ == "__main__":
    unittest.main()
