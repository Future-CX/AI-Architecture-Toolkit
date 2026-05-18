#!/usr/bin/env python3
"""Write an architecture principle markdown file from the preset template."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "principle-template.md"


def title_case_name(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name.strip())
    if not cleaned:
        raise ValueError("Principle document name cannot be empty.")
    return " ".join(word[:1].upper() + word[1:] for word in cleaned.split(" "))


def slugify_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    if not slug:
        raise ValueError("Principle document name must contain at least one letter or number.")
    return f"{slug}.md"


def format_principles(items: list[str]) -> str:
    cleaned = [item.strip().rstrip(".") for item in items if item.strip()]
    if not cleaned:
        raise ValueError("At least one principle is required.")
    return "\n".join(f"{index}. {item}." for index, item in enumerate(cleaned, start=1))


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


def update_principles_list(principles_dir: Path, principle_name: str, filename: str, description: str) -> Path:
    principles_list = principles_dir / "_principles-list.md"
    existing = principles_list.read_text(encoding="utf-8") if principles_list.exists() else ""
    rows = parse_index_table(existing)
    rows[filename] = {
        "name": principle_name,
        "filename": filename,
        "description": description,
        "last_updated": date.today().isoformat(),
    }
    principles_list.write_text(render_index_table("Principles List", rows), encoding="utf-8")
    return principles_list


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Principle document name, for example 'Data Architecture Principles'.")
    parser.add_argument("--intent", required=True, help="One-sentence intent for the principle document.")
    parser.add_argument(
        "--principle",
        action="append",
        required=True,
        help="Principle statement. Repeat for multiple principles.",
    )
    parser.add_argument("--usage", required=True, help="Usage guidance for applying the principles.")
    parser.add_argument(
        "--output-root",
        default=".",
        help="Repository root where the principles folder should be created. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the principle file if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    principle_name = title_case_name(args.name)
    output_root = Path(args.output_root).expanduser().resolve()
    principles_dir = output_root / "principles"
    target = principles_dir / slugify_name(args.name)

    if target.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {target}")

    rendered = TEMPLATE.read_text(encoding="utf-8")
    rendered = rendered.replace("{{PRINCIPLE_NAME}}", principle_name)
    rendered = rendered.replace("{{INTENT}}", args.intent.strip())
    rendered = rendered.replace("{{PRINCIPLES}}", format_principles(args.principle))
    rendered = rendered.replace("{{USAGE}}", args.usage.strip())

    principles_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered + "\n", encoding="utf-8")
    principles_list = update_principles_list(
        principles_dir,
        principle_name,
        target.name,
        args.intent.strip(),
    )
    print(target)
    print(principles_list)


if __name__ == "__main__":
    main()
