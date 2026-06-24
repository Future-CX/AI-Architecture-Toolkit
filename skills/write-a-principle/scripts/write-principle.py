#!/usr/bin/env python3
"""Write an architecture principle markdown file from the preset template."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "principle-template.md"
TOOLKIT_ROOT = Path(__file__).resolve().parents[3]


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


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_output_root(output_root: Path) -> None:
    if output_root == TOOLKIT_ROOT or is_relative_to(output_root, TOOLKIT_ROOT):
        raise SystemExit(
            "Refusing to write generated principles inside the toolkit repository. "
            "Run from a private lab root with this toolkit mounted as a submodule, "
            "or pass --output-root <private-lab-root>."
        )


def infer_category_code(name: str) -> str:
    lowered = name.lower()
    known_codes = {
        "data": "DATA",
        "architecture": "ARCH",
        "cloud": "CLD",
        "integration": "INT",
        "security": "SEC",
        "api": "API",
    }
    words = re.findall(r"[a-zA-Z]+", lowered)
    for word in words:
        if word in known_codes:
            return known_codes[word]
    for keyword, code in known_codes.items():
        if keyword in lowered:
            return code
    if not words:
        raise ValueError("Cannot infer a category code from the principle document name.")
    return words[0][:4].upper()


def normalize_category_code(value: str) -> str:
    code = value.strip().upper()
    if not re.fullmatch(r"[A-Z]{3,4}", code):
        raise ValueError("Category code must be 3-4 letters, for example ARCH, DATA, CLD, or INT.")
    return code


def clean_items(items: list[str] | None) -> list[str]:
    if not items:
        return []
    return [item.strip().rstrip(".") for item in items if item.strip()]


def clean_principles(items: list[str], category_code: str) -> list[dict[str, str | list[str]]]:
    cleaned = clean_items(items)
    if not cleaned:
        raise ValueError("At least one principle is required.")
    return [{"identifier": f"{category_code}{index:03d}", "name": item} for index, item in enumerate(cleaned, start=1)]


def attach_field(principles: list[dict[str, str | list[str]]], field: str, values: list[str] | None) -> None:
    cleaned = clean_items(values)
    for index, principle in enumerate(principles):
        principle[field] = cleaned[index] if index < len(cleaned) else "TBD"


def attach_list_field(principles: list[dict[str, str | list[str]]], field: str, values: list[str] | None) -> None:
    cleaned = clean_items(values)
    for index, principle in enumerate(principles):
        principle[field] = [cleaned[index]] if index < len(cleaned) else []


def format_principles_index(items: list[dict[str, str | list[str]]]) -> str:
    return "\n".join(f"- [{item['identifier']} - {item['name']}.](#{str(item['identifier']).lower()})" for item in items)


def bullet_list(items: list[str], fallback: str = "TBD") -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}." for item in items)


def format_principle_details(items: list[dict[str, str | list[str]]]) -> str:
    sections = []
    for item in items:
        optional_guidance = ""
        if isinstance(item["dos"], list) and isinstance(item["donts"], list) and (item["dos"] or item["donts"]):
            guidance_parts = ["\n\n#### Do's and Don'ts"]
            if item["dos"]:
                guidance_parts.append(f"\n\n##### Do's\n\n{bullet_list(item['dos'])}")
            if item["donts"]:
                guidance_parts.append(f"\n\n##### Don'ts\n\n{bullet_list(item['donts'])}")
            optional_guidance = "".join(guidance_parts)
        sections.append(
            f'<a id="{str(item["identifier"]).lower()}"></a>\n\n'
            f"### {item['identifier']} - {item['name']}.\n\n"
            f"#### Identifier\n\n"
            f"{item['identifier']}.\n\n"
            f"#### Description\n\n"
            f"{item['description']}.\n\n"
            f"#### Rationale\n\n"
            f"{item['rationale']}.\n\n"
            f"#### Consequences\n\n"
            f"{item['consequences']}."
            f"{optional_guidance}"
        )
    return "\n\n".join(sections)


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
    parser.add_argument(
        "--category-code",
        help="3-4 letter principle category code, for example ARCH, DATA, CLD, or INT. Defaults to a value inferred from the document name.",
    )
    parser.add_argument("--intent", required=True, help="One-sentence intent for the principle document.")
    parser.add_argument(
        "--principle",
        action="append",
        required=True,
        help="Principle name or statement. Repeat for multiple principles.",
    )
    parser.add_argument(
        "--principle-description",
        action="append",
        help="Principle description. Repeat in the same order as --principle.",
    )
    parser.add_argument(
        "--principle-rationale",
        action="append",
        help="Principle rationale. Repeat in the same order as --principle.",
    )
    parser.add_argument(
        "--principle-consequence",
        action="append",
        help="Principle consequence. Repeat in the same order as --principle.",
    )
    parser.add_argument(
        "--principle-do",
        action="append",
        help="Principle do guidance. Repeat in the same order as --principle.",
    )
    parser.add_argument(
        "--principle-dont",
        action="append",
        help="Principle don't guidance. Repeat in the same order as --principle.",
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
    validate_output_root(output_root)
    principles_dir = output_root / "principles"
    target = principles_dir / slugify_name(args.name)

    if target.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {target}")

    category_code = normalize_category_code(args.category_code or infer_category_code(args.name))
    principles = clean_principles(args.principle, category_code)
    attach_field(principles, "description", args.principle_description)
    attach_field(principles, "rationale", args.principle_rationale)
    attach_field(principles, "consequences", args.principle_consequence)
    attach_list_field(principles, "dos", args.principle_do)
    attach_list_field(principles, "donts", args.principle_dont)
    rendered = TEMPLATE.read_text(encoding="utf-8")
    rendered = rendered.replace("{{PRINCIPLE_NAME}}", principle_name)
    rendered = rendered.replace("{{CONFLUENCE_LINK}}", "TBD")
    rendered = rendered.replace("{{LAST_UPDATE}}", date.today().isoformat())
    rendered = rendered.replace("{{INTENT}}", args.intent.strip())
    rendered = rendered.replace("{{PRINCIPLES_INDEX}}", format_principles_index(principles))
    rendered = rendered.replace("{{PRINCIPLE_DETAILS}}", format_principle_details(principles))
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
