---
name: write-a-principle
description: Write private-lab architecture principle documents from a standard template, using this toolkit as a submodule and writing outputs to the private lab principles folder. Use when the user asks to create, draft, scaffold, write, or add a principle under the principles folder.
---

# Write A Principle

## Quick Start

Always run this skill from a private lab repository where this toolkit is mounted as a submodule, typically `toolkit/`. Write generated principle documents under the private lab repository's root `principles/` folder using the preset template in `toolkit/skills/write-a-principle/templates/principle-template.md`.

Do not run this skill from the public toolkit repository for generated output. Do not write generated principle files under `toolkit/principles/`. Run the command from the private lab root, or pass `--output-root <private-lab-root>`, so output goes to `<private-lab-root>/principles/`.

If running from a different working directory, explicitly target the private lab root:

```sh
python3 toolkit/skills/write-a-principle/scripts/write-principle.py "Data Architecture Principles" \
  --category-code DATA \
  --intent "Define durable data architecture principles for ownership, quality, governance, and integration." \
  --principle "Data ownership must be explicit and aligned to business domains" \
  --principle-description "Every important data object must have a named business owner and stewardship model" \
  --principle-rationale "Ownership makes data quality, access, lifecycle, and change decisions accountable" \
  --principle-consequence "Teams must identify ownership before introducing or changing critical data flows" \
  --principle-do "Name the owning domain or team for each critical data object" \
  --principle-dont "Treat shared data as ownerless platform inventory" \
  --principle "Critical data must have defined quality expectations and stewardship" \
  --usage "Use these principles when designing data platforms, integrations, analytics products, and governance processes." \
  --output-root <private-lab-root>
```

Run from the private lab root, this creates `principles/data-architecture-principles.md` beside `toolkit/`.

Each generated principle is also added to `principles/_principles-list.md` using a markdown table with `name`, `description`, and `last_updated` columns. Create `_principles-list.md` when it does not exist. Keep rows sorted alphabetically by principle name.

## Workflow

1. Confirm the current target is a private lab repository with the toolkit mounted as a submodule, usually at `toolkit/`.
2. Refuse to generate principle output inside the public toolkit repository or under `toolkit/principles/`.
3. Determine the principle document name and convert it to `<private-lab-root>/principles/<slug>.md`.
4. Capture a 3-4 letter category code for the principle set, such as `ARCH` for architecture, `DATA` for data, `CLD` for cloud, or `INT` for integration.
5. Capture a concise intent statement.
6. Capture 3-7 concrete principles. Each principle must have an identifier, name, description, rationale, and consequences. Do's and don'ts are optional.
7. Generate each principle identifier from the category code plus a three-digit incremental number starting with `001`, for example `DATA001`, `DATA002`, and `DATA003`.
8. Add a linked list at the top of the document's `## Principles` section containing only first-level principle identifiers and names. If the document has multiple levels of principles, sub-principles, controls, examples, or nested guidance, keep those inside the matching principle detail section and do not include them in the top list.
9. Capture practical usage guidance.
10. Generate the file under the private lab repository's root `principles/` folder using the preset template.
11. Add or update the generated principle in `<private-lab-root>/principles/_principles-list.md` with a relative link, intent, and `last_updated` date.
12. Do not overwrite an existing principle file unless the user explicitly asks.
13. Keep the style consistent with the existing files in `<private-lab-root>/principles/`.

## Output Standard

Each principle file must use this structure:

```md
# Principle Document Name

## Intent

One-sentence intent.

## Principles

- [DATA001 - Principle one.](#data001)
- [DATA002 - Principle two.](#data002)
- [DATA003 - Principle three.](#data003)

## Principle Details

<a id="data001"></a>

### DATA001 - Principle one.

Describe the principle in practical terms.

#### Rationale

Explain why the principle matters.

#### Consequences

Explain what teams must accept or change when applying the principle.

#### Do's and Don'ts

##### Do's

- Recommended behavior.

##### Don'ts

- Discouraged behavior.

#### Sub-Principles

##### DATA001.1 - Sub-principle one.

Describe lower-level guidance here. Do not add this sub-principle to the top `## Principles` list.

<a id="data002"></a>

### DATA002 - Principle two.

Describe the principle in practical terms.

#### Rationale

Explain why the principle matters.

#### Consequences

Explain what teams must accept or change when applying the principle.

<a id="data003"></a>

### DATA003 - Principle three.

Describe the principle in practical terms.

#### Rationale

Explain why the principle matters.

#### Consequences

Explain what teams must accept or change when applying the principle.

## Usage

When and how to apply these principles.
```

## Template

Use `templates/principle-template.md` as the source template for generated principle files.
