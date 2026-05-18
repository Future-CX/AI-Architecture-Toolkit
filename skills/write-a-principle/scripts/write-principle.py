#!/usr/bin/env python3
"""Write an architecture principle markdown file from the preset template."""

from __future__ import annotations

import argparse
import re
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
    print(target)


if __name__ == "__main__":
    main()
