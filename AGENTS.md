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

Generated artifacts that contain real company context belong in a private company lab repository, not in this public toolkit. This includes real glossaries, ADRs, capability overviews, target architecture documents, solution architecture designs, diagrams, roadmaps, and review findings.

Toolkit-aware scripts and agents should honor `.toolkitignore` when deciding what counts as active toolkit content.

## READABILITY

When creating stakeholder-facing documents:

- Treat non-technical business stakeholders as the primary audience.
- Start with the business outcome, the decision or recommendation, and the operational impact.
- Use plain language first. Add technical detail only when it changes a decision, risk, cost, ownership, timeline, or support model.
- Prefer short sentences, short paragraphs, clear headings, and concrete trade-offs.
- Keep dense implementation detail in later sections, tables, or appendices after the stakeholder summary.
- Avoid unnecessary technical jargon. Explain acronyms and domain-specific terms when first used.
- Make recommendations, decisions, owners, risks, and open questions easy to find.
- Before finishing, reread the opening sections and simplify any sentence that a business reader would need to parse twice.

## PRINCIPLES

When creating principles, use the write-a-principle skill.

Generated principle documents belong under `principles/` in the consuming repository. Do not add company-confidential principle examples to this public toolkit.

## CAPABILITIES

When creating capability overviews, use the capability-overview skill.

Generated capability overviews belong under `capabilities/<slug>/` in the consuming repository. Do not write real company capability context into this public toolkit.

## SOLUTION ARCHITECTURES

When creating solution architecture designs, use the solution-architecture-design skill.

Solution architecture design outputs belong under `solution-architectures/<slug>/` in the consuming repository, or under the private lab root when this toolkit is used as a submodule.

When a solution architecture design creates diagrams:

- Store each Draw.io source as a separate `.drawio` file beside the design document.
- Export a same-basename `.svg` file for every `.drawio` file when the diagram must be embedded.
- Embed the `.svg` file in the design document.
- Link the `.drawio` source near the embedded SVG.

When creating any Draw.io diagram, use the create-drawio-diagram skill because it contains the diagram instructions, style rules, and templates. Store generated `.drawio` files beside the document they support, and export same-basename `.svg` files when the diagram must be embedded.

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
