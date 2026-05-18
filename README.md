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

For testing this public toolkit against real company context, use a separate private company lab repository. See [Private Company Lab](governance/private-company-lab.md).

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
