#!/usr/bin/env python3
"""Write a capability overview markdown file from the preset template."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "capability-overview-template.md"


def strip_capability_suffix(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name.strip())
    cleaned = re.sub(r"^capability\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+capability$", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def normalize_name(name: str) -> str:
    cleaned = strip_capability_suffix(name)
    if not cleaned:
        raise ValueError("Capability name cannot be empty.")
    return " ".join(word[:1].upper() + word[1:] for word in cleaned.split(" "))


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", strip_capability_suffix(name).lower()).strip("-")
    if not slug:
        raise ValueError("Capability name must contain at least one letter or number.")
    return slug


def bullet_list(items: list[str], fallback: str = "TBD") -> str:
    cleaned = [item.strip().rstrip(".") for item in items if item.strip()]
    if not cleaned:
        return f"- {fallback}"
    return "\n".join(f"- {item}." for item in cleaned)


def paragraph(value: str, fallback: str = "TBD") -> str:
    cleaned = value.strip()
    return cleaned if cleaned else fallback


def inline_list(items: list[str], fallback: str = "TBD") -> str:
    cleaned = [item.strip() for item in items if item.strip()]
    return ", ".join(cleaned) if cleaned else fallback


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def parse_capability_table(existing: str) -> dict[str, dict[str, str]]:
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


def render_capability_table(rows: dict[str, dict[str, str]]) -> str:
    sorted_rows = sorted(rows.values(), key=lambda row: row["name"].lower())
    lines = [
        "# Capability List",
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


def update_capability_list(
    capabilities_dir: Path,
    capability_name: str,
    filename: str,
    description: str,
) -> Path:
    capability_list = capabilities_dir / "_capability-list.md"
    existing = capability_list.read_text(encoding="utf-8") if capability_list.exists() else ""
    rows = parse_capability_table(existing)
    rows[filename] = {
        "name": capability_name,
        "filename": filename,
        "description": description,
        "last_updated": date.today().isoformat(),
    }
    capability_list.write_text(render_capability_table(rows), encoding="utf-8")
    return capability_list


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Capability name, for example 'Order Management'.")
    parser.add_argument("--domain", required=True, help="Business or architecture domain.")
    parser.add_argument("--business-objective", required=True, help="Business objective for the capability.")
    parser.add_argument("--stakeholder", action="append", required=True, help="Stakeholder. Repeat for multiple stakeholders.")
    parser.add_argument("--existing-system", action="append", required=True, help="Existing system. Repeat for multiple systems.")
    parser.add_argument("--strategic-importance", required=True, help="Strategic importance, for example Low, Medium, High, or Critical.")
    parser.add_argument("--pain-point", action="append", required=True, help="Pain point. Repeat for multiple pain points.")
    parser.add_argument("--related-capability", action="append", required=True, help="Related capability. Repeat for multiple capabilities.")
    parser.add_argument(
        "--output-root",
        default=".",
        help="Repository root where the capabilities folder should be created. Defaults to the current working directory.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite the capability file if it already exists.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    capability_name = normalize_name(args.name)
    capability_slug = slugify(args.name)
    output_root = Path(args.output_root).expanduser().resolve()
    capabilities_dir = output_root / "capabilities"
    capability_dir = capabilities_dir / capability_slug
    target = capability_dir / f"{capability_slug}.md"

    if target.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {target}")

    replacements = {
        "{{CAPABILITY_NAME}}": capability_name,
        "{{CAPABILITY_DESCRIPTION}}": paragraph(args.business_objective),
        "{{CAPABILITY_DEFINITION}}": f"{capability_name} is the business capability responsible for achieving the stated objective within the {args.domain.strip()} domain.",
        "{{DOMAIN}}": paragraph(args.domain),
        "{{APPLICATION}}": inline_list(args.existing_system),
        "{{APPLICATION_LIFECYCLE_STATUS}}": "TBD",
        "{{OWNERS}}": inline_list(args.stakeholder),
        "{{LAST_UPDATE}}": date.today().isoformat(),
        "{{BUSINESS_OBJECTIVE}}": paragraph(args.business_objective),
        "{{BUSINESS_OUTCOME}}": "TBD: Define the measurable business outcome this capability should enable.",
        "{{STRATEGIC_IMPORTANCE}}": paragraph(args.strategic_importance),
        "{{SCOPE}}": "TBD: Define what is in scope and explicitly out of scope for this capability.",
        "{{STAKEHOLDERS}}": bullet_list(args.stakeholder),
        "{{ACTORS}}": "TBD: Identify people, teams, systems, and external parties that interact with this capability.",
        "{{PROCESSES_SUPPORTED}}": "TBD: List the business processes this capability supports.",
        "{{INPUTS}}": "TBD: List the information, events, requests, and triggers consumed by this capability.",
        "{{OUTPUTS}}": "TBD: List the decisions, records, events, products, services, and reports produced by this capability.",
        "{{EXISTING_SYSTEMS}}": bullet_list(args.existing_system),
        "{{APPLICATIONS_INVOLVED}}": bullet_list(args.existing_system),
        "{{APPLICATION_LIFECYCLE_MANAGEMENT}}": "TBD: Describe application ownership, lifecycle stage, roadmap status, technical health, support model, and retirement or modernization considerations.",
        "{{DATA_INVOLVED}}": "TBD: Identify core data entities, ownership, quality needs, and retention concerns.",
        "{{INTEGRATIONS}}": "TBD: Identify upstream and downstream integrations, APIs, events, files, and dependencies.",
        "{{KPIS}}": "TBD: Define measurable indicators for effectiveness, efficiency, quality, and adoption.",
        "{{NFR_CONSIDERATIONS}}": "TBD: Capture availability, performance, scalability, security, privacy, compliance, resilience, maintainability, and observability considerations.",
        "{{PAIN_POINTS}}": bullet_list(args.pain_point),
        "{{RISKS}}": "TBD: Identify business, delivery, operational, integration, data, security, and compliance risks.",
        "{{MATURITY_ASSESSMENT}}": "TBD: Assess current maturity and target maturity using a clear scale.",
        "{{RELATED_CAPABILITIES}}": bullet_list(args.related_capability),
        "{{FUTURE_STATE_CONSIDERATIONS}}": "TBD: Describe target-state improvements, simplification opportunities, platform changes, and roadmap implications.",
    }

    rendered = TEMPLATE.read_text(encoding="utf-8")
    for token, value in replacements.items():
        rendered = rendered.replace(token, value)

    capability_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered + "\n", encoding="utf-8")
    capability_list = update_capability_list(
        capabilities_dir,
        capability_name,
        f"{capability_slug}/{target.name}",
        paragraph(args.business_objective),
    )
    print(target)
    print(capability_list)


if __name__ == "__main__":
    main()
