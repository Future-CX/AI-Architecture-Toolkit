#!/usr/bin/env python3
"""Write an Architecture Decision Record under the consuming repository root."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("ADR title must contain at least one letter or number.")
    return slug


def next_adr_number(adr_dir: Path) -> int:
    highest = 0
    if adr_dir.exists():
        for path in adr_dir.glob("[0-9][0-9][0-9][0-9]-*.md"):
            try:
                highest = max(highest, int(path.name[:4]))
            except ValueError:
                continue
    return highest + 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Short ADR title.")
    parser.add_argument(
        "--summary",
        required=True,
        help="One to three sentences describing the context, decision, and reason.",
    )
    parser.add_argument(
        "--output-root",
        default=".",
        help="Repository root where the adr folder should be created. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--adr-dir",
        default="adr",
        help="ADR folder relative to output root. Defaults to adr.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root).expanduser().resolve()
    adr_dir = output_root / args.adr_dir
    number = next_adr_number(adr_dir)
    target = adr_dir / f"{number:04d}-{slugify(args.title)}.md"

    content = f"# {args.title.strip()}\n\n{args.summary.strip()}\n"

    adr_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(content + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
