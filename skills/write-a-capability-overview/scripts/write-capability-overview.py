#!/usr/bin/env python3
"""Write a capability overview markdown file from the preset template."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "capability-overview-template.md"


def normalize_name(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name.strip())
    if not cleaned:
        raise ValueError("Capability name cannot be empty.")
    return " ".join(word[:1].upper() + word[1:] for word in cleaned.split(" "))


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    if not slug:
        raise ValueError("Capability name must contain at least one letter or number.")
    return f"{slug}.md"


def bullet_list(items: list[str], fallback: str = "TBD") -> str:
    cleaned = [item.strip().rstrip(".") for item in items if item.strip()]
    if not cleaned:
        return f"- {fallback}"
    return "\n".join(f"- {item}." for item in cleaned)


def paragraph(value: str, fallback: str = "TBD") -> str:
    cleaned = value.strip()
    return cleaned if cleaned else fallback


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
    output_root = Path(args.output_root).expanduser().resolve()
    capabilities_dir = output_root / "capabilities"
    target = capabilities_dir / slugify(args.name)

    if target.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {target}")

    replacements = {
        "{{CAPABILITY_NAME}}": capability_name,
        "{{CAPABILITY_DEFINITION}}": f"{capability_name} is the business capability responsible for achieving the stated objective within the {args.domain.strip()} domain.",
        "{{DOMAIN}}": paragraph(args.domain),
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

    capabilities_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
