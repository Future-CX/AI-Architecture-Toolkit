#!/usr/bin/env python3
"""Create an architecture agent markdown file from the preset template."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "agent-template.md"
AGENTS_DIR = ROOT / "agents"


def title_case_agent_name(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name.strip())
    cleaned = re.sub(r"\s+agent$", "", cleaned, flags=re.IGNORECASE)
    if not cleaned:
        raise ValueError("Agent name cannot be empty.")
    return " ".join(word[:1].upper() + word[1:] for word in cleaned.split(" "))


def slugify_agent_name(name: str) -> str:
    base = re.sub(r"\s+agent$", "", name.strip(), flags=re.IGNORECASE)
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    if not slug:
        raise ValueError("Agent name must contain at least one letter or number.")
    return f"{slug}-agent.md"


def format_responsibilities(items: list[str]) -> str:
    cleaned = [item.strip().rstrip(".") for item in items if item.strip()]
    if not cleaned:
        raise ValueError("At least one responsibility is required.")
    return "\n".join(f"- {item}." for item in cleaned)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Agent name, for example 'Data Architect'.")
    parser.add_argument("--purpose", required=True, help="One-sentence agent purpose.")
    parser.add_argument(
        "--responsibility",
        action="append",
        required=True,
        help="Agent responsibility. Repeat for multiple responsibilities.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the agent file if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    agent_name = title_case_agent_name(args.name)
    target = AGENTS_DIR / slugify_agent_name(args.name)

    if target.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {target}")

    rendered = TEMPLATE.read_text(encoding="utf-8")
    rendered = rendered.replace("{{AGENT_NAME}}", agent_name)
    rendered = rendered.replace("{{PURPOSE}}", args.purpose.strip())
    rendered = rendered.replace(
        "{{RESPONSIBILITIES}}",
        format_responsibilities(args.responsibility),
    )

    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
