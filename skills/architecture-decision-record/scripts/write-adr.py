#!/usr/bin/env python3
"""Write an Architecture Decision Record under the consuming repository root."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("ADR title must contain at least one letter or number.")
    return slug


def next_adr_number(adr_dir: Path) -> int:
    highest = 0
    if adr_dir.exists():
        for path in adr_dir.glob("adr-[0-9][0-9][0-9][0-9]-*.md"):
            match = re.match(r"adr-(?P<number>[0-9]{4})-", path.name)
            if not match:
                continue
            highest = max(highest, int(match.group("number")))
    return highest + 1


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def parse_index_table(existing: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for line in existing.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 3 or cells[0].lower() == "name":
            continue
        match = re.match(r"\[(?P<name>[^\]]+)\]\((?P<filename>[^)]+)\)", cells[0])
        if not match:
            continue
        rows[match.group("filename")] = {
            "name": match.group("name"),
            "filename": match.group("filename"),
            "description": cells[1].replace("\\|", "|"),
            "last_updated": cells[2],
        }
    return rows


def render_index_table(title: str, rows: dict[str, dict[str, str]]) -> str:
    sorted_rows = sorted(rows.values(), key=lambda row: row["name"].lower())
    lines = [
        f"# {title}",
        "",
        "| name | description | last_updated |",
        "| --- | --- | --- |",
    ]
    for row in sorted_rows:
        lines.append(
            f"| [{escape_table_cell(row['name'])}]({row['filename']}) | "
            f"{escape_table_cell(row['description'])} | "
            f"{escape_table_cell(row['last_updated'])} |"
        )
    return "\n".join(lines) + "\n"


def update_adr_list(adr_dir: Path, title: str, filename: str, description: str) -> Path:
    adr_list = adr_dir / "_adr-list.md"
    existing = adr_list.read_text(encoding="utf-8") if adr_list.exists() else ""
    rows = parse_index_table(existing)
    rows[filename] = {
        "name": title,
        "filename": filename,
        "description": description,
        "last_updated": date.today().isoformat(),
    }
    adr_list.write_text(render_index_table("ADR List", rows), encoding="utf-8")
    return adr_list


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
    target = adr_dir / f"adr-{number:04d}-{slugify(args.title)}.md"

    content = f"# {args.title.strip()}\n\n{args.summary.strip()}\n"

    adr_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(content + "\n", encoding="utf-8")
    adr_list = update_adr_list(adr_dir, args.title.strip(), target.name, args.summary.strip())
    print(target)
    print(adr_list)


if __name__ == "__main__":
    main()
