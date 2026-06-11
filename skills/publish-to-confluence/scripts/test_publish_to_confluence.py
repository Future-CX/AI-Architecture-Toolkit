#!/usr/bin/env python3
"""Tests for the publish-to-confluence helper."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("publish-to-confluence.py")
SPEC = importlib.util.spec_from_file_location("publish_to_confluence", SCRIPT_PATH)
assert SPEC is not None
publish_to_confluence = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(publish_to_confluence)


class MarkdownTableConversionTests(unittest.TestCase):
    def test_simple_fallback_converter_renders_markdown_table(self) -> None:
        markdown = "\n".join(
            [
                "| Decision | Owner | Status |",
                "| --- | --- | --- |",
                "| Use API gateway | Platform | Proposed |",
                "| Move later | Team | Open |",
            ]
        )

        html = publish_to_confluence.simple_markdown_to_html(markdown)

        self.assertIn("<table>", html)
        self.assertIn("<th>Decision</th>", html)
        self.assertIn("<td>Use API gateway</td>", html)
        self.assertIn("<td>Open</td>", html)
        self.assertNotIn("<p>| Decision", html)

    def test_simple_fallback_converter_supports_inline_markdown_in_table_cells(self) -> None:
        markdown = "\n".join(
            [
                "| Field | Value |",
                "| --- | --- |",
                "| Link | [Confluence](https://example.atlassian.net/wiki/spaces/ARCH) |",
                "| Code | `system-id` and **owned** |",
            ]
        )

        html = publish_to_confluence.simple_markdown_to_html(markdown)

        self.assertIn('<a href="https://example.atlassian.net/wiki/spaces/ARCH">Confluence</a>', html)
        self.assertIn("<code>system-id</code> and <strong>owned</strong>", html)

    def test_table_cells_keep_escaped_pipe_inside_cell(self) -> None:
        cells = publish_to_confluence.table_cells("| Name | A \\| B |")

        self.assertEqual(cells, ["Name", "A | B"])

    def test_read_content_removes_top_metadata_table_but_keeps_document_table(self) -> None:
        raw = "\n".join(
            [
                "# Architecture Decision",
                "",
                "| Field | Value |",
                "| --- | --- |",
                "| Confluence Link | https://example.atlassian.net/wiki/spaces/ARCH/pages/123/Decision |",
                "",
                "## Options",
                "",
                "| Option | Impact |",
                "| --- | --- |",
                "| A | Lower cost |",
                "| B | Lower risk |",
            ]
        )

        html = publish_to_confluence.read_content(raw, Path("decision.md"), "markdown")

        self.assertIn("<h2>Options</h2>", html)
        self.assertIn("<th>Option</th>", html)
        self.assertIn("<td>Lower risk</td>", html)
        self.assertNotIn("Confluence Link", html)

    def test_collect_publish_git_paths_includes_source_svg_drawio_and_linked_drawio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source = root / "int-0001-order-from-commerce-to-erp.md"
            svg = root / "diagrams" / "int-0001-order-from-commerce-to-erp.svg"
            drawio = root / "diagrams" / "int-0001-order-from-commerce-to-erp.drawio"
            linked_drawio = root / "diagrams" / "detail.drawio"
            svg.parent.mkdir()
            source.write_text("", encoding="utf-8")
            svg.write_text("<svg />", encoding="utf-8")
            drawio.write_text("<mxfile />", encoding="utf-8")
            linked_drawio.write_text("<mxfile />", encoding="utf-8")
            raw = "\n".join(
                [
                    "# Order Integration",
                    "",
                    "![Integration diagram](diagrams/int-0001-order-from-commerce-to-erp.svg)",
                    "[Draw.io source](diagrams/detail.drawio)",
                ]
            )

            paths = publish_to_confluence.collect_publish_git_paths(raw, source, "markdown")

            self.assertEqual(
                paths,
                [
                    source.resolve(),
                    svg.resolve(),
                    drawio.resolve(),
                    linked_drawio.resolve(),
                ],
            )


if __name__ == "__main__":
    unittest.main()
