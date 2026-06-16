#!/usr/bin/env python3
"""Tests for the publish-to-confluence helper."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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

    def test_markdown_code_block_renders_as_confluence_code_macro(self) -> None:
        markdown = "\n".join(
            [
                "```",
                "line <one>",
                "line & two",
                "```",
            ]
        )

        html = publish_to_confluence.markdown_to_html(markdown)

        self.assertIn('<ac:structured-macro ac:name="code">', html)
        self.assertIn("<ac:plain-text-body><![CDATA[line <one>\nline & two]]></ac:plain-text-body>", html)
        self.assertNotIn("<pre><code>", html)

    def test_markdown_code_block_keeps_language_hint(self) -> None:
        markdown = "\n".join(
            [
                "```python",
                "print('hello')",
                "```",
            ]
        )

        html = publish_to_confluence.markdown_to_html(markdown)

        self.assertIn('<ac:parameter ac:name="language">python</ac:parameter>', html)
        self.assertIn("<ac:plain-text-body><![CDATA[print('hello')]]></ac:plain-text-body>", html)

    def test_markdown_html_anchor_renders_as_confluence_anchor_macro(self) -> None:
        markdown = "\n".join(
            [
                "# Principles",
                "",
                "- [ARCH001 - Architecture principles are leading](#arch001)",
                "",
                "<a id=\"arch001\"></a>",
                "",
                "## ARCH001 - Architecture principles are leading",
            ]
        )

        html = publish_to_confluence.read_content(markdown, Path("principles.md"), "markdown")

        self.assertIn(
            '<ac:link ac:anchor="arch001"><ac:plain-text-link-body><![CDATA[ARCH001 - Architecture principles are leading]]></ac:plain-text-link-body></ac:link>',
            html,
        )
        self.assertIn(
            '<ac:structured-macro ac:name="anchor"><ac:parameter ac:name="">arch001</ac:parameter></ac:structured-macro>',
            html,
        )
        self.assertNotIn("&lt;a id", html)
        self.assertNotIn('<a href="#arch001">', html)

    def test_html_anchor_renders_as_confluence_anchor_macro(self) -> None:
        raw_html = "\n".join(
            [
                '<p><a href="#arch001">ARCH001 - Architecture principles are leading</a></p>',
                '<p><a id="arch001"></a></p>',
                "<h2>ARCH001 - Architecture principles are leading</h2>",
            ]
        )

        html = publish_to_confluence.read_content(raw_html, Path("principles.html"), "html")

        self.assertIn(
            '<ac:link ac:anchor="arch001"><ac:plain-text-link-body><![CDATA[ARCH001 - Architecture principles are leading]]></ac:plain-text-link-body></ac:link>',
            html,
        )
        self.assertIn(
            '<ac:structured-macro ac:name="anchor"><ac:parameter ac:name="">arch001</ac:parameter></ac:structured-macro>',
            html,
        )
        self.assertNotIn('<a href="#arch001">', html)
        self.assertNotIn('<a id="arch001"', html)

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

    def test_git_status_lines_scopes_to_publish_related_paths(self) -> None:
        completed = subprocess.CompletedProcess(
            args=["git"],
            returncode=0,
            stdout=" M docs/design.md\n?? diagrams/context.drawio\n",
            stderr="",
        )

        with mock.patch.object(publish_to_confluence.subprocess, "run", return_value=completed) as run:
            lines = publish_to_confluence.git_status_lines(
                Path("/repo"),
                ["docs/design.md", "diagrams/context.drawio"],
            )

        run.assert_called_once_with(
            [
                "git",
                "status",
                "--porcelain",
                "--untracked-files=normal",
                "--",
                "docs/design.md",
                "diagrams/context.drawio",
            ],
            cwd=Path("/repo"),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(lines, [" M docs/design.md", "?? diagrams/context.drawio"])

    def test_git_status_lines_empty_scope_does_not_check_worktree(self) -> None:
        with mock.patch.object(publish_to_confluence.subprocess, "run") as run:
            lines = publish_to_confluence.git_status_lines(Path("/repo"), [])

        run.assert_not_called()
        self.assertEqual(lines, [])

    def test_commit_prompt_is_skipped_when_git_status_is_empty(self) -> None:
        with mock.patch.object(publish_to_confluence, "prompt_and_maybe_commit_publish_changes") as prompt:
            with mock.patch.object(publish_to_confluence, "git_repo_root", return_value=Path("/repo")):
                with mock.patch.object(
                    publish_to_confluence,
                    "collect_publish_git_paths",
                    return_value=[Path("/repo/docs/design.md")],
                ):
                    with mock.patch.object(
                        publish_to_confluence,
                        "git_relative_paths",
                        return_value=["docs/design.md"],
                    ):
                        with mock.patch.object(publish_to_confluence, "git_status_lines", return_value=[]):
                            publish_to_confluence.check_publish_git_changes(
                                "# Design",
                                Path("/repo/docs/design.md"),
                                "markdown",
                                False,
                            )

        prompt.assert_not_called()


if __name__ == "__main__":
    unittest.main()
