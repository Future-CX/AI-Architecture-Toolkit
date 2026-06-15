#!/usr/bin/env python3
"""Write a capability overview markdown file from the preset template."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
import xml.etree.ElementTree as ET


TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "capability-overview-template.md"
DRAWIO_TEMPLATE = Path(__file__).resolve().parents[2] / "create-drawio-diagram" / "templates" / "capability-overview.drawio"
DIAGRAM_BASENAME = "capability-overview"


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


def diagram_list(items: list[str], fallback: str, limit: int = 3) -> str:
    cleaned = [item.strip().rstrip(".") for item in items if item.strip()]
    if not cleaned:
        return fallback
    shown = cleaned[:limit]
    if len(cleaned) > limit:
        shown.append("More listed in overview")
    return "<br>".join(shown)


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


def remove_cells(root: ET.Element, cell_ids: set[str]) -> None:
    for parent in root.iter():
        for child in list(parent):
            if child.tag == "mxCell" and child.attrib.get("id") in cell_ids:
                parent.remove(child)


def write_capability_drawio(
    target: Path,
    capability_name: str,
    stakeholders: list[str],
    existing_systems: list[str],
    related_capabilities: list[str],
    pain_points: list[str],
) -> None:
    tree = ET.parse(DRAWIO_TEMPLATE)
    root = tree.getroot()
    labels = {
        "title": f"{capability_name} Context",
        "actor": f"Stakeholders and users<br>{diagram_list(stakeholders, 'To be confirmed')}",
        "capability": capability_name,
        "upstream": f"Inputs and source systems<br>{diagram_list(existing_systems, 'To be confirmed')}",
        "downstream": f"Related capabilities<br>{diagram_list(related_capabilities, 'To be confirmed')}",
        "external": f"Constraints and risks<br>{diagram_list(pain_points, 'To be confirmed', limit=2)}",
    }
    remove_cells(
        root,
        {
            "wtTJ4m9Lci7Y-lzfFHPa-1",
            "hzigCzCzZuQ-4PxgagW3-1",
            "hzigCzCzZuQ-4PxgagW3-2",
            "hzigCzCzZuQ-4PxgagW3-3",
        },
    )
    for cell in root.iter("mxCell"):
        cell_id = cell.attrib.get("id")
        if cell_id in labels:
            cell.set("value", labels[cell_id])
    tree.write(target, encoding="utf-8", xml_declaration=False)


def svg_text(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_lines(text: str, x: int, y: int, line_height: int = 18) -> str:
    lines = text.split("<br>")
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(f'<tspan x="{x}" dy="{dy}">{svg_text(line)}</tspan>')
    return "".join(tspans)


def svg_box(
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str,
    stroke: str,
    label: str,
    *,
    font_size: int = 14,
    bold: bool = False,
) -> str:
    weight = "700" if bold else "400"
    text_x = x + width // 2
    text_y = y + 30
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2"/>'
        f'<text x="{text_x}" y="{text_y}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="{font_size}" font-weight="{weight}" fill="#17201d">'
        f'{svg_lines(label, text_x, text_y)}</text>'
    )


def svg_connector(x1: int, y1: int, x2: int, y2: int, label: str) -> str:
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2 - 8
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#5d6964" stroke-width="2" '
        'marker-end="url(#arrow)"/>'
        f'<rect x="{mid_x - 62}" y="{mid_y - 14}" width="124" height="20" fill="#fbfcfa"/>'
        f'<text x="{mid_x}" y="{mid_y}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="12" fill="#5d6964">{svg_text(label)}</text>'
    )


def write_capability_svg(
    target: Path,
    capability_name: str,
    stakeholders: list[str],
    existing_systems: list[str],
    related_capabilities: list[str],
    pain_points: list[str],
) -> None:
    actor_label = f"Stakeholders and users<br>{diagram_list(stakeholders, 'To be confirmed')}"
    capability_label = capability_name
    upstream_label = f"Inputs and source systems<br>{diagram_list(existing_systems, 'To be confirmed')}"
    downstream_label = f"Related capabilities<br>{diagram_list(related_capabilities, 'To be confirmed')}"
    external_label = f"Constraints and risks<br>{diagram_list(pain_points, 'To be confirmed', limit=2)}"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1169" height="827" viewBox="0 0 1169 827" style="color-scheme: light; background: #fbfcfa;">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#5d6964"/>
</marker>
</defs>
<rect width="100%" height="100%" fill="#fbfcfa" pointer-events="none"/>
<text x="60" y="70" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="700" fill="#17201d">{svg_text(capability_name)} Context</text>
{svg_box(70, 250, 180, 100, "#fff3c4", "#b7791f", actor_label, bold=True)}
{svg_box(455, 230, 265, 120, "#d9eadf", "#0f766e", capability_label, font_size=16, bold=True)}
{svg_box(455, 100, 265, 90, "#dae8fc", "#315f8f", upstream_label)}
{svg_box(455, 430, 265, 90, "#dae8fc", "#315f8f", downstream_label)}
{svg_box(880, 250, 220, 100, "#f8cecc", "#a3433f", external_label)}
{svg_connector(250, 300, 455, 290, "triggers or uses")}
{svg_connector(588, 190, 588, 230, "provides input")}
{svg_connector(588, 350, 588, 430, "produces outcome")}
{svg_connector(720, 290, 880, 300, "depends on")}
</svg>
'''
    target.write_text(svg, encoding="utf-8")


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
        "{{MAIN_BUSINESS_FEATURES}}": "TBD: Summarize the main business features this capability provides.",
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
    drawio_target = capability_dir / f"{DIAGRAM_BASENAME}.drawio"
    svg_target = capability_dir / f"{DIAGRAM_BASENAME}.svg"
    write_capability_drawio(
        drawio_target,
        capability_name,
        args.stakeholder,
        args.existing_system,
        args.related_capability,
        args.pain_point,
    )
    write_capability_svg(
        svg_target,
        capability_name,
        args.stakeholder,
        args.existing_system,
        args.related_capability,
        args.pain_point,
    )
    target.write_text(rendered + "\n", encoding="utf-8")
    capability_list = update_capability_list(
        capabilities_dir,
        capability_name,
        f"{capability_slug}/{target.name}",
        paragraph(args.business_objective),
    )
    print(target)
    print(drawio_target)
    print(svg_target)
    print(capability_list)


if __name__ == "__main__":
    main()
