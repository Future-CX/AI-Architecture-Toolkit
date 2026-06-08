#!/usr/bin/env python3
"""Write an Architecture Decision Record under the consuming repository root."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

STATUS_ICONS = {
    "proposed": "🟡 proposed",
    "accepted": "🟢 accepted",
    "deprecated": "🔴 deprecated",
    "superseded": "⚫ superseded",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("ADR title must contain at least one letter or number.")
    return slug


def next_adr_number(adr_dir: Path) -> int:
    highest = 0
    if adr_dir.exists():
        patterns = (
            "adr-[0-9][0-9][0-9][0-9]-*.md",
            "[0-9][0-9][0-9][0-9]-*.md",
        )
        for pattern in patterns:
            for path in adr_dir.glob(pattern):
                match = re.match(r"(?:adr-)?(?P<number>[0-9]{4})-", path.name)
                if not match:
                    continue
                highest = max(highest, int(match.group("number")))
    return highest + 1


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def normalize_status(value: str) -> str:
    cleaned = re.sub(r"^[^\w]+", "", value).strip().lower()
    return cleaned if cleaned in STATUS_ICONS else "accepted"


def status_label(status: str) -> str:
    return STATUS_ICONS[normalize_status(status)]


def parse_overview_table(existing: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for line in existing.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) not in {3, 4} or cells[0].lower() == "name":
            continue
        match = re.match(r"\[(?P<name>[^\]]+)\]\((?P<filename>[^)]+)\)", cells[0])
        if not match:
            continue
        if len(cells) == 4:
            status = normalize_status(cells[1])
            description = cells[2].replace("\\|", "|")
            last_updated = cells[3]
        else:
            status = "accepted"
            description = cells[1].replace("\\|", "|")
            last_updated = cells[2]
        rows[match.group("filename")] = {
            "name": match.group("name"),
            "filename": match.group("filename"),
            "status": status,
            "description": description,
            "last_updated": last_updated,
        }
    return rows


def render_overview_table(title: str, rows: dict[str, dict[str, str]]) -> str:
    sorted_rows = sorted(rows.values(), key=lambda row: row["name"].lower())
    lines = [
        f"# {title}",
        "",
        "| name | status | description | last_updated |",
        "| --- | --- | --- | --- |",
    ]
    for row in sorted_rows:
        lines.append(
            f"| [{escape_table_cell(row['name'])}]({row['filename']}) | "
            f"{escape_table_cell(status_label(row.get('status', 'accepted')))} | "
            f"{escape_table_cell(row['description'])} | "
            f"{escape_table_cell(row['last_updated'])} |"
        )
    return "\n".join(lines) + "\n"


def update_adr_overview(adr_dir: Path, title: str, filename: str, status: str, description: str) -> Path:
    adr_overview = adr_dir / "_adr-overview.md"
    legacy_list = adr_dir / "_adr-list.md"
    if adr_overview.exists():
        existing = adr_overview.read_text(encoding="utf-8")
    elif legacy_list.exists():
        existing = legacy_list.read_text(encoding="utf-8")
    else:
        existing = ""
    rows = parse_overview_table(existing)
    rows[filename] = {
        "name": title,
        "filename": filename,
        "status": normalize_status(status),
        "description": description,
        "last_updated": date.today().isoformat(),
    }
    adr_overview.write_text(render_overview_table("ADR Overview", rows), encoding="utf-8")
    return adr_overview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Short ADR title.")
    parser.add_argument(
        "--summary",
        required=True,
        help="One to three sentences describing the context, decision, and reason.",
    )
    parser.add_argument(
        "--status",
        choices=sorted(STATUS_ICONS),
        default="accepted",
        help="ADR status shown in _adr-overview.md. Defaults to accepted.",
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
    adr_overview = update_adr_overview(adr_dir, args.title.strip(), target.name, args.status, args.summary.strip())
    print(target)
    print(adr_overview)


if __name__ == "__main__":
    main()
