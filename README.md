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

This toolkit helps architecture teams standardize how they use AI for solution design, enterprise architecture, integration design, API governance, risk assessment, and architecture review.

The active toolkit boundary is documented in [TOOLKIT.md](TOOLKIT.md). Toolkit-aware scanners should also honor [.toolkitignore](.toolkitignore).

For testing this public toolkit against real company context, use a separate private company lab repository. See [Private Company Lab](governance/private-company-lab.md).

## How To Use The Toolkit

1. Choose the agent that matches the work.
   Use the agent files in `agents/` as role briefs for architecture conversations. For example, use the Solution Architect Agent for high-level solution design, the Enterprise Architect Agent for capability and roadmap alignment, or the Integration Architect Agent for integration design.

2. Use skills for repeatable architecture tasks.
   Skills in `skills/` define focused workflows. Use them when creating agents, writing principles, recording ADRs, producing capability overviews, hardening domain language, or stress-testing a plan.

3. Start from templates.
   Use shared templates in `templates/` and skill-owned templates in `skills/*/templates/` to create consistent artifacts.

4. Store generated artifacts in the matching folder.
   Agent definitions belong in `agents/`, principles in `principles/`, generated capability overviews in `capabilities/`, and ADRs in the location defined by the ADR skill.

5. Keep public and private work separate.
   This repository should stay generic and public. Use a private company lab repository for real company context, internal system names, stakeholder details, generated company glossaries, and real architecture decisions.

6. Respect the active toolkit boundary.
   Use [TOOLKIT.md](TOOLKIT.md) to understand what counts as active toolkit content. Toolkit-aware scripts and agents should honor [.toolkitignore](.toolkitignore).

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
| [Architecture Review Board Agent](agents/architecture-review-board-agent.md) | Support architecture review board preparation, review consistency, and decision tracking. |
| [Enterprise Architect Agent](agents/enterprise-architect-agent.md) | Support enterprise alignment across capabilities, platforms, standards, roadmaps, and strategic technology direction. |
| [Integration Architect Agent](agents/integration-architect-agent.md) | Support integration design across APIs, events, data flows, messaging, orchestration, and operational ownership. |
| [Solution Architect Agent](agents/solution-architect-agent.md) | Support solution design by translating business needs into coherent application, data, integration, security, and operational architecture. |

## Skills

| Skill | Purpose |
| --- | --- |
| [Architecture Decision Record](skills/architecture-decision-record/SKILL.md) | Record durable architecture decisions as concise ADRs using the repository ADR format. |
| [Create An Agent](skills/create-an-agent/SKILL.md) | Create architecture agent definitions under `agents/` from a preset template. |
| [Grill Me](skills/grill-me/SKILL.md) | Interview the user relentlessly about a plan or design until reaching shared understanding. |
| [Ubiquitous Language](skills/ubiquitous-language/SKILL.md) | Extract a DDD-style ubiquitous language glossary, flag ambiguities, and propose canonical terms. |
| [Write A Capability Overview](skills/write-a-capability-overview/SKILL.md) | Write business capability overview documents under `capabilities/` from a preset template. |
| [Write A Principle](skills/write-a-principle/SKILL.md) | Write architecture principle documents under `principles/` from a preset template. |
| [Write A Skill](skills/write-a-skill/SKILL.md) | Create new agent skills with proper structure, progressive disclosure, and bundled resources. |
