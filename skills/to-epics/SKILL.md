---
name: to-epics
description: Break approved target architecture work into reviewable epics, run a grill-me clarification session, validate terminology against the glossary, and list each epic in Phase E of the related target architecture document. Use when the user asks to create, draft, split, or convert architecture work into epics, especially from a target architecture document created by the target-architecture-document skill; require explicit user-provided epic name, phase, description, and main capability before creating or updating any epic.
---

# To Epics

## Quick Start

Use this skill after a target architecture document exists or when the user explicitly wants architecture work translated into epics.

Do not automatically create epics from analysis alone. Before creating or updating an epic file, require the user to provide:

- Target architecture to link to
- Epic name
- Phase
- Epic description
- Main capability

If any required input is missing, ask for it and stop before writing the epic.

## Output Location

Create epics in the private lab root under `requirements/<name-of-target-architecture>/`.

Use the target architecture folder name as `<name-of-target-architecture>` unless the target architecture document defines a clearer document name. Normalize it to the same slug style used for folders.

```text
<private-lab-root>/
├── requirements/
│   └── <target-architecture-slug>/
│       └── <epic-slug>.md
└── solution-architectures/
    └── <target-architecture-slug>/
        ├── 07-phase-e-solution-building-blocks.md
        └── target-architecture-document.md
```

Use `templates/epic-template.md` for the epic file. Preserve the two opening tables: the document metadata table first, followed by the `Epic Overview` table.

## Workflow

1. Ask the user which target architecture to link the epic to.
   - If the user named a target architecture, confirm the exact folder or document path before continuing.
   - If the user did not name one, search for `solution-architectures/*/target-architecture-document.md`, present the candidates, and ask the user to choose.
   - Do not create an epic until the user has selected or confirmed the target architecture linkage.
2. Read the target architecture document and relevant section files, especially `07-phase-e-solution-building-blocks.md`, roadmap themes, gap analysis, governance actions, risks, and open questions.
3. Ask the user for the epic name, phase, epic description, and main capability if not already provided.
4. Ask for reference links:
   - Main capability link
   - Main L2 solution architecture link
   - Existing Jira item URL/key, if any
   - Existing Confluence page URL, if any
   These references are optional except when the user can identify the linked artifact. Use `TBD` when the user does not provide a link.
   Use the linked document title as the Markdown link label whenever possible. For local markdown files, derive the title from the first `#` heading; otherwise use the filename without extension. For Jira and Confluence links, use the issue key/page title when the user provides it; otherwise ask for the title or use `TBD`.
5. Start a `grill-me` clarification session using `../grill-me/SKILL.md`.
   - Focus the session on whether the epic has enough detail to be useful for delivery planning.
   - Ask one question at a time and wait for the user's answer before continuing.
   - Cover scope, out of scope, assumptions, dependencies, business requirements, visual design, solution design, Site Reliability Engineering, architecture impact, open questions, and glossary-sensitive terminology.
   - Use `../ubiquitous-language/SKILL.md` during the session when terms are vague, overloaded, missing from `GLOSSARY.md`, or important enough to become shared domain language.
   - Continue only when the required epic fields are confirmed and remaining unknowns are explicitly captured as open questions or `TBD`.
6. Confirm the target architecture linkage:
   - Target architecture document path
   - Requirements output folder: `<private-lab-root>/requirements/<name-of-target-architecture>/`
   - Phase
   - Main capability
   - Main capability link, or `TBD`
   - Main capability link title, derived from the linked capability document title where possible
   - Main L2 solution architecture link, or `TBD`
   - Main L2 solution architecture link title, derived from the linked solution architecture document title where possible
   - Jira item reference, if provided
   - Jira link title, normally the issue key or issue summary
   - Confluence page reference, if provided
   - Confluence link title, normally the page title
   - Roadmap theme, gap, decision, governance action, or architecture section the epic supports
   - Any known dependencies or sequencing constraints
7. Validate terminology before writing the epic:
   - Locate `<private-lab-root>/GLOSSARY.md`.
   - Check the epic name, description, main capability, scope terms, application names, data objects, integrations, and business requirements against the glossary.
   - If `GLOSSARY.md` is missing, or if important terms are missing, ambiguous, or inconsistent, use `../ubiquitous-language/SKILL.md` to create or update `<private-lab-root>/GLOSSARY.md` before creating the epic.
   - Do not write real-company terminology into this public toolkit repository; update the private lab root glossary.
8. Create `requirements/<name-of-target-architecture>/<epic-slug>.md` from the template. Preserve the document metadata table and the `Epic Overview` table. Do not overwrite an existing epic unless the user explicitly asks to update it.
9. Update the target architecture linkage:
   - Add or update the `## Epics To Build` table in `07-phase-e-solution-building-blocks.md` when that file exists.
   - Add or update the `### Epics To Build` table in the Phase E section of `target-architecture-document.md`.
   - Link the epic file with a relative markdown link from the target architecture document folder to the requirements file.
10. Summarize what was created, which grill-me questions materially shaped the epic, which glossary terms were confirmed or added, and which target architecture sections the epic traces to.

## Epic Content Guidance

Keep the epic useful for delivery planning while preserving architecture traceability.

Include:

- Document metadata table.
- Epic Overview table with epic, phase, main capability, target architecture, L2 solution architecture, Jira, and Confluence references.
- User-provided name and description, unchanged except for minor formatting.
- User-provided phase, unchanged except for minor formatting.
- User-provided main capability, unchanged except for minor formatting.
- Main capability link and main L2 solution architecture link when provided; otherwise use `TBD`. Use the linked document titles as link labels.
- Jira item and Confluence page references when provided; otherwise use `TBD`. Use the issue key, issue summary, or Confluence page title as the link label when known.
- Scope: in scope, out of scope, and key assumptions.
- Candidate capabilities, applications, data objects, integrations, and quality attributes affected.
- Dependencies.
- Business requirements.
- Visual design needs, UX/UI references, screens, flows, or `TBD`.
- Solution design notes, components, integration behavior, data changes, or `TBD`.
- Site Reliability Engineering answers for criticality, failure modes, detection, response, and impact prevention or minimization.
- Open questions that need product, architecture, security, data, or delivery input.

Do not invent delivery commitments, dates, team names, estimates, or business facts. Mark unknowns as `TBD` or open questions.

## Grill-Me Clarification

Treat the `grill-me` session as mandatory before creating or updating an epic file.

Use `../grill-me/SKILL.md` to challenge whether the epic is clear enough to hand to delivery. Ask one question at a time. Prefer questions that expose missing scope boundaries, unclear capability ownership, weak business requirements, hidden dependencies, unresolved visual design expectations, incomplete solution design details, SRE risks, and ambiguous terminology.

Ask these SRE questions during the session:

1. How critical is this process or component?
2. What can go wrong?
3. How do we see when it goes wrong?
4. What can we do when it goes wrong?
5. How can we prevent or minimize impact when it goes wrong?

Do not create the epic file until the user has answered the clarification questions needed to avoid avoidable misunderstanding. If an answer is genuinely unknown, record it as `TBD` or an open question in the epic.

## Glossary Validation

Treat glossary maintenance as part of epic creation.

Before writing an epic, verify that the terms used in the epic are known in `<private-lab-root>/GLOSSARY.md`, especially:

- Main capability
- Business terms from the epic name and description
- Applications
- Data objects
- Integrations and externally visible events or APIs when they are business-facing
- Terms used in business requirements

If terms are missing or unclear, pause epic creation and use `../ubiquitous-language/SKILL.md` to clarify and update the glossary. Continue only after the glossary has been created or updated. Use canonical glossary terms in the epic whenever possible, and note unresolved terminology in `Open Questions`.

## Phase E Epic List Format

When adding the link to `07-phase-e-solution-building-blocks.md`, use this table:

```md
## Epics To Build

| Epic                                                                              | Main Capability     | Description          | Phase     |
| --------------------------------------------------------------------------------- | ------------------- | -------------------- | --------- |
| [{{EPIC_NAME}}](../../requirements/{{TARGET_ARCHITECTURE_NAME}}/{{EPIC_SLUG}}.md) | {{MAIN_CAPABILITY}} | {{EPIC_DESCRIPTION}} | {{PHASE}} |
```

When adding the same link to the assembled `target-architecture-document.md`, use the matching `### Epics To Build` table inside `## 8. Phase E - Solution Building Blocks`.

If the table still contains `_No linked epics yet._`, replace that placeholder row with the first real epic. If the table already has epics, append or update the matching epic row. Keep the table sorted by epic name unless the document already uses another ordering.

## Guardrails

- User input is mandatory for the target architecture linkage and for every epic name, phase, description, and main capability.
- A `grill-me` clarification session is mandatory before creating or updating an epic file.
- Suggest candidate epics only as a review list; do not create files until the user selects a candidate and provides or confirms the name, description, and main capability.
- Keep generated real-company epics in the private company lab repository, not inside this public toolkit.
- Keep real-company glossary updates in the private company lab repository, not inside this public toolkit.
- Preserve existing target architecture content; only add or update epic links and clearly related traceability text.
