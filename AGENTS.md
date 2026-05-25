## AGENTS

When creating agents, use the create-an-agent skill.

When creating or updating agents:

- Update the Agents table in the top-level README.md.
- Update the public homepage at `www/index.html` when the visible agent list or agent positioning changes.
- Keep agent briefs under `agents/`.
- Do not create real-company agent variants in this public repository.

## EXAMPLES

## GOVERNANCE

Do not add company-confidential information, customer names, internal system names, proprietary architecture details, credentials, or non-public business context to this repository. Use a separate private company lab repository for real-world testing.

Generated artifacts that contain real company context belong in a private company lab repository, not in this public toolkit. This includes real glossaries, ADRs, capability overviews, target architecture documents, high-level solution designs, diagrams, roadmaps, and review findings.

Toolkit-aware scripts and agents should honor `.toolkitignore` when deciding what counts as active toolkit content.

## PRINCIPLES

When creating principles, use the write-a-principle skill.

Generated principle documents belong under `principles/` in the consuming repository. Do not add company-confidential principle examples to this public toolkit.

## CAPABILITIES

When creating capability overviews, use the capability-overview skill.

Generated capability overviews belong under `capabilities/<slug>/` in the consuming repository. Do not write real company capability context into this public toolkit.

## SOLUTION ARCHITECTURES

When creating high-level solution designs, use the high-level-solution-design skill.

High-level solution design outputs belong under `solution-architectures/<slug>/` in the consuming repository, or under the private lab root when this toolkit is used as a submodule.

When a high-level solution design creates Mermaid diagrams:

- Store each Mermaid source as a separate `.mmd` file beside the design document.
- Render a same-basename `.svg` file for every `.mmd` file.
- Embed the `.svg` file in the design document.
- Link the `.mmd` source near the embedded SVG.
- Do not inline Mermaid code unless the user explicitly asks.

When creating target architecture documents, use the target-architecture-document skill.

## SKILLS

Skills are organized as folders under `skills/`.

When creating skills, use the create-a-skill skill.

Each skill entry in the top-level README.md must link the skill name to its SKILL.md.

The `skills/README.md` file must list every skill with a one-line description and link the skill name to its `SKILL.md`.

Each skill folder should include a README.md when the skill needs local usage notes, templates, scripts, or resources explained outside `SKILL.md`.

When updating skills, also update the public homepage at `www/index.html` if the visible skills list or skill positioning changes.

## TEMPLATES

Use existing templates before creating new ones.

When changing a template, update the owning skill instructions so future generated documents replace placeholders completely and do not leave drafting guidance in final artifacts.

When a template change affects public-facing behavior, update the top-level README.md and `www/index.html` if needed.
