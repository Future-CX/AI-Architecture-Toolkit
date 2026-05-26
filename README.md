# AI-Architecture-Toolkit

Open-source AI agents, skills, templates, and workflows for software architects and enterprise architecture teams.

## Repository Structure

- `principles/` - Architecture, AI agent, and quality guardrail principles.
- `capabilities/` - Capability overview documents created from the capability overview template.
- `skills/` - Reusable architecture skill modules for AI-assisted workflows.
- `agents/` - Role-specific agent briefs for architecture work.
- `templates/` - Markdown templates for common architecture deliverables.
- `examples/` - Example scenarios and reference applications of the toolkit.
- `governance/` - Contribution, maturity, and review guidance.

## Purpose

This toolkit helps architecture teams standardize how they use AI for enterprise architecture, solution design, integration design, API governance, risk assessment, architecture review, and implementation handover.

Toolkit-aware scanners should honor [.toolkitignore](.toolkitignore) when separating active toolkit content from local or generated files.

For testing this public toolkit against real company context, use a separate private company lab repository. See [Private Company Lab](governance/private-company-lab.md).

## How To Use The Toolkit

1. Choose the agent that matches the work.
   Use the agent files in `agents/` as role briefs for architecture conversations. For example, use the Enterprise Architect Agent for governance, principles, target architecture, and roadmap alignment; use the Solution Architect Agent for high-level solution design, technical choices, diagrams, and solution ADRs; or use the Integration Architect Agent for integration design.

2. Use skills for repeatable architecture tasks.
   Skills in `skills/` define focused workflows. Use them when creating agents, writing principles, recording ADRs, producing capability overviews, drafting target architecture, creating high-level solution designs, hardening domain language, or stress-testing a plan.

3. Start from templates.
   Use shared templates in `templates/` and skill-owned templates in `skills/*/templates/` to create consistent artifacts.

4. Store generated artifacts in the matching folder.
   Agent definitions belong in `agents/`, principles in `principles/`, generated capability overviews in `capabilities/`, solution architecture documents in `solution-architectures/`, epics in `requirements/<name-of-target-architecture>/`, private-lab glossaries in `GLOSSARY.md`, and ADRs in the location defined by the ADR skill.

5. Keep public and private work separate.
   This repository should stay generic and public. Use a private company lab repository for real company context, internal system names, stakeholder details, generated company glossaries, and real architecture decisions.

6. Respect the active toolkit boundary.
   Toolkit-aware scripts and agents should honor [.toolkitignore](.toolkitignore) when deciding what counts as active toolkit content.

## Git Usage

### Clone The Public Toolkit

```sh
git clone https://github.com/Future-CX/AI-Architecture-Toolkit.git
cd AI-Architecture-Toolkit
```

Use this public repository for reusable agents, skills, principles, templates, governance guidance, and fictional examples.

### Use The Toolkit From A Private Company Lab

Create a separate private repository for real company context, then add this public toolkit as a submodule:

```sh
git submodule add https://github.com/Future-CX/AI-Architecture-Toolkit.git toolkit
git commit -m "Add AI Architecture Toolkit submodule"
```

Recommended private lab layout:

```text
company-architecture-lab/
├── CONTEXT.md
├── GLOSSARY.md
├── docs/
│   └── adr/
├── company/
├── requirements/
├── outputs/
└── toolkit/
```

### Clone A Private Lab With The Toolkit Submodule

```sh
git clone --recurse-submodules <private-lab-repo-url>
```

If the private lab was already cloned without submodules:

```sh
git submodule update --init --recursive
```

### Update The Toolkit Submodule

From the private lab repository:

```sh
git submodule update --remote toolkit
git add toolkit
git commit -m "Update AI Architecture Toolkit submodule"
```

### Keep Public And Private Work Separate

- Commit reusable toolkit improvements to this public repository.
- Commit real company context, internal system names, private glossaries, and generated company ADRs only to the private lab repository.
- Generalize reusable patterns before copying them from the private lab back into the public toolkit.

## Agents

| Agent | Purpose |
| --- | --- |
| [API Governance Agent](agents/api-governance-agent.md) | Support API design quality, consistency, discoverability, lifecycle management, and compliance with API standards. |
| [Architecture Review Board Agent](agents/architecture-review-board.md) | Support architecture review board preparation, review consistency, and decision tracking. |
| [Business Analyst Agent](agents/business-analyst.md) | Support requirements discovery by clarifying business needs, scope, stakeholders, outcomes, terminology, and traceability for architecture work. |
| [Data Architect Agent](agents/data-architect.md) | Support data architecture decisions across canonical data objects, ownership, lifecycle, privacy, quality, integration, and governance. |
| [Enterprise Architect Agent](agents/enterprise-architect.md) | Own governance, principles, target architecture, roadmap alignment, and enterprise-impacting architecture decisions. |
| [Integration Architect Agent](agents/integration-architect.md) | Own integration principles and patterns, and support integration design across APIs, events, data flows, messaging, orchestration, and operational ownership. |
| [Lead Developer Agent](agents/lead-developer.md) | Support implementation leadership by turning approved solution and integration designs into buildable, testable, operable software delivery plans. |
| [Security Architect Agent](agents/security-architect.md) | Support security architecture by identifying threats, controls, privacy concerns, compliance constraints, and operational security requirements for architecture work. |
| [Solution Architect Agent](agents/solution-architect.md) | Create high-level solution designs from capability overviews, record material ADRs, and embed rendered Mermaid diagrams. |

## Skills

| Skill | Purpose |
| --- | --- |
| [Architecture Decision Record](skills/architecture-decision-record/SKILL.md) | Record durable architecture decisions as concise ADRs when choices are hard to reverse and based on real trade-offs. |
| [Create An Agent](skills/create-an-agent/SKILL.md) | Create architecture agent definitions under `agents/` from a preset template. |
| [Target Architecture Document](skills/target-architecture-document/SKILL.md) | Connect capabilities to strategy, business architecture, data, applications, integration, technology, and epics to build. |
| [Grill Me](skills/grill-me/SKILL.md) | Challenge plans, assumptions, constraints, terminology, risks, and decisions until the design context is explicit. |
| [Ubiquitous Language](skills/ubiquitous-language/SKILL.md) | Extract a shared glossary, flag ambiguous terms, and define canonical applications, data objects, and relationships. |
| [High-Level Solution Design](skills/high-level-solution-design/SKILL.md) | Write implementation-oriented solution designs with chapter guidance, Mermaid sources, rendered SVGs, and linked ADRs. |
| [Integration Design](skills/integration-design/SKILL.md) | Create integration design documents for APIs, events, files, batches, messaging, and orchestration. |
| [Create Draw.io Diagram](skills/create-drawio-diagram/SKILL.md) | Create editable Draw.io architecture diagrams from reusable templates for solution and target architecture documents. |
| [To Epics](skills/to-epics/SKILL.md) | Break target architecture work into user-confirmed epics and list each epic in Phase E of the target architecture document. |
| [Capability Overview](skills/capability-overview/SKILL.md) | Write business capability overview documents under `capabilities/` from a preset template. |
| [Write A Principle](skills/write-a-principle/SKILL.md) | Draft architecture principle documents with identifiers, rationale, consequences, and reviewable guidance. |
| [Create A Skill](skills/create-a-skill/SKILL.md) | Create reusable skills with progressive disclosure, templates, scripts, and clear trigger guidance. |

## What The Toolkit Creates

- Capability overviews under `capabilities/`.
- Target architecture and high-level solution design documents under `solution-architectures/`.
- User-confirmed epics under `requirements/<name-of-target-architecture>/`, listed in Phase E of the target architecture document.
- Integration designs under `integrations/` using `INT-0001-<integration-slug>.md` numbering.
- Mermaid `.mmd` diagram sources paired with same-basename `.svg` files embedded in design documents.
- Editable Draw.io `.drawio` diagrams for stakeholders who need diagrams.net-compatible source files.
- ADRs linked from the technical design choices they support.
- Private-lab glossary entries in `GLOSSARY.md`.
- Architecture principle documents under `principles/`.
