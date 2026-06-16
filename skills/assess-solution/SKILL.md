---
name: assess-solution
description: Assess a proposed or existing solution against architecture principles and a selected capability overview or solution architecture design. Use when the user asks to review, assess, self-assess, validate, or score a solution against principles, capability fit, or an existing solution design.
---

# Assess Solution

## Quick Start

Assess a proposed or existing solution against:

1. The architecture principles available in `principles/`.
2. One user-selected baseline:
   - A capability overview under `capabilities/<slug>/`.
   - A solution architecture design under `solution-architectures/<slug>/`.

If the user has not identified the capability overview or solution design, ask which one to use before starting the assessment. If multiple candidate files match, list the candidates and ask the user to choose one.

## Required Inputs

- Solution description, proposal, implementation notes, or path to an existing solution document.
- Solution supplier, vendor, product company, or implementation partner when the solution depends on an external company.
- Customer references, case studies, testimonials, analyst notes, or reference-call findings when available.
- Assessment baseline: one capability overview or one solution architecture design.
- Architecture principles to assess against. Prefer all principle documents under `principles/` unless the user names a subset.
- Target audience and desired depth, if different from architecture and delivery stakeholders.

## Workflow

1. Confirm the solution to assess. If the solution is only described in conversation, summarize it back before scoring.
2. Ask the user whether to assess against a capability overview or a solution architecture design when the baseline is not explicit.
3. Locate and read the selected baseline document. Do not assess against both unless the user asks.
4. Locate and read architecture principles from `principles/`. If the folder or relevant principles are missing, ask the user to provide the principle documents or continue with only the selected baseline.
5. Extract the baseline expectations:
   - Business outcome and scope boundary.
   - Main business features or requirements, users, processes, data, integrations, systems, and dependencies.
   - Security, privacy, compliance, non-functional, operational, and lifecycle expectations.
   - Explicit risks, assumptions, constraints, open questions, and design decisions.
6. Extract the solution claims:
   - What the solution changes or introduces.
   - Components, applications, data, integrations, deployment, operations, ownership, and migration approach.
   - Supplier, vendor, product company, or implementation partner involved.
   - Decisions, assumptions, constraints, known gaps, and unresolved questions.
7. Assess the solution supplier when a supplier is named:
   - General company information relevant to architecture and delivery decisions.
   - Product or service fit for the selected capability or solution design.
   - Company strengths, such as domain fit, product maturity, ecosystem, support model, implementation capability, security posture, or roadmap alignment.
   - Company cautions, such as lock-in, commercial dependency, unclear roadmap, limited local support, integration limits, data residency, compliance gaps, or operational maturity concerns.
   - Evidence gaps that need vendor due diligence, reference checks, procurement review, security review, or legal review.
8. Assess customer references when available:
   - Other customers or comparable organizations using the solution.
   - Their use case, industry, scale, geography, and similarity to the current context.
   - Reported experience, recommendation, benefits, limitations, implementation effort, support quality, and operational lessons.
   - Whether the reference is public, supplier-provided, independently verified, or based on a direct reference call.
   - Evidence gaps where the reference is too vague, not comparable, outdated, or unverifiable.
9. Assess principle alignment. For each relevant principle, mark:
   - `Aligned` when the solution clearly supports the principle.
   - `Partly aligned` when the intent is right but evidence, scope, or controls are incomplete.
   - `Misaligned` when the solution conflicts with the principle.
   - `Not enough evidence` when the solution does not provide enough information to judge.
10. Assess architectural fit:
   - Fit to business outcome and scope.
   - Coverage of required users, processes, data, integrations, and systems.
   - Consistency with architecture decisions, constraints, and target-state direction.
   - Target architecture, principle, integration, security, privacy, resilience, observability, and support alignment.
11. Create a simple 5-star scorecard using the required scorecard categories. Use half stars only when the evidence supports a clear midpoint.
12. Identify gaps, risks, trade-offs, and open questions. Do not invent missing facts.
13. Give a practical recommendation:
    - `Proceed` when only minor issues remain.
    - `Proceed with conditions` when risks or gaps need tracked mitigation.
    - `Revise before approval` when material conflicts or missing decisions remain.
    - `Do not proceed` when the solution conflicts with critical principles or baseline expectations.

## Output

Use concise, stakeholder-readable Markdown:

1. `Assessment Summary` - decision recommendation, main reason, and operational impact.
2. `Assessment Baseline` - linked capability overview or solution architecture design, plus principle source used.
3. `Scorecard` - simple 5-star table with only these rows: `Ease of Use`, `Main Business Features Fit`, `Other Features Provided`, `Integrations`, and `Architecture Fit`. Include `Price Indication` and `Overall` rows when the information is available. Show ratings as stars, for example `★★★★☆` or `★★★½☆`, and add one short evidence note per row.
4. `Main Business Features` - use one heading per business requirement found in the capability overview or solution design. Under each heading, summarize baseline fit, insight, gap, and recommended action.
5. `Architectural Fit` - technical insights with subsections: `Target Architecture Alignment` for target-state fit and constraints, `Principle Alignment` for principle rating, evidence, and required change, and `Integration Alignment` for interfaces, dependencies, contracts, data flow, error handling, observability, and ownership.
6. `Solution Supplier` - general company information, strengths, cautions, and due diligence needs.
7. `References` - other customers using the solution, their context, recommendation or experience, relevance, and evidence quality.
8. `Risks and Trade-offs` - material risks, impact, mitigation, and owner when known.
9. `Open Questions` - answerable questions needed to complete the assessment.
10. `Recommendation` - proceed status, conditions, and next actions.

## Guidance

- Start with the business outcome and decision impact before technical findings.
- Keep the assessment evidence-based. Cite source sections or filenames where possible.
- Separate facts from assumptions.
- Treat missing evidence as an assessment result, not as permission to guess.
- For supplier commentary, use neutral language and distinguish known facts from market perception, assumptions, or missing due diligence.
- For references, identify the source and comparability. Do not present supplier marketing claims as independent customer experience.
- Keep the scorecard easy to scan. Do not add extra scorecard categories unless the user asks.
- Prefer concrete remediation actions over generic advice.
- Keep company-confidential solution details out of this public toolkit repository. Assess real company solutions in a private company lab repository.
