#!/usr/bin/env python3
"""Make Draw.io SVG exports safe for light-background embedding."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


LIGHT_BACKGROUND = "#fbfcfa"


def sanitize_svg(svg: str, background: str = LIGHT_BACKGROUND) -> str:
    svg = re.sub(r"color-scheme\s*:\s*light\s+dark\s*;?", "color-scheme: light;", svg)
    svg = re.sub(r"color-scheme\s*:\s*dark\s*;?", "color-scheme: light;", svg)

    # Draw.io may emit CSS like light-dark(#17201d, #ced5d3). Keep the light value.
    svg = re.sub(r"light-dark\(\s*([^,\)]+?)\s*,\s*([^\)]+?)\s*\)", r"\1", svg)

    svg_tag = re.search(r"<svg\b[^>]*>", svg)
    if svg_tag:
        tag = svg_tag.group(0)
        if "color-scheme" not in tag:
            if "style=" in tag:
                tag = re.sub(r'style="([^"]*)"', r'style="\1 color-scheme: light;"', tag, count=1)
            else:
                tag = tag[:-1] + ' style="color-scheme: light;">'
        tag = re.sub(r"background:\s*transparent\s*;?", f"background: {background};", tag)
        tag = re.sub(r"background-color:\s*transparent\s*;?", f"background-color: {background};", tag)
        svg = svg[: svg_tag.start()] + tag + svg[svg_tag.end() :]

    background_rect = f'<rect width="100%" height="100%" fill="{background}" pointer-events="none"/>'
    if background_rect not in svg:
        svg = re.sub(r"(<defs\s*/>)", r"\1" + background_rect, svg, count=1)
        if background_rect not in svg:
            svg = re.sub(r"(</defs>)", r"\1" + background_rect, svg, count=1)
        if background_rect not in svg and svg_tag:
            insert_at = svg_tag.end()
            svg = svg[:insert_at] + background_rect + svg[insert_at:]

    return svg


def validate_svg(svg: str) -> None:
    if "color-scheme: light dark" in svg or "color-scheme: dark" in svg:
        raise SystemExit("SVG still contains a dark-capable color-scheme.")
    if "light-dark(" in svg:
        raise SystemExit("SVG still contains light-dark(...) CSS values.")
    if "color-scheme: light" not in svg:
        raise SystemExit("SVG does not contain explicit color-scheme: light.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path, help="SVG file exported from Draw.io.")
    parser.add_argument(
        "--background",
        default=LIGHT_BACKGROUND,
        help=f"Background fill to force into the SVG. Defaults to {LIGHT_BACKGROUND}.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw = args.svg.read_text(encoding="utf-8")
    sanitized = sanitize_svg(raw, args.background)
    validate_svg(sanitized)
    args.svg.write_text(sanitized, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
