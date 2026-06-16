---
name: assess-solution
description: Interview the user to assess a proposed or existing solution against architecture principles and a selected capability overview or solution architecture design. Use when the user asks to review, assess, self-assess, validate, or score a solution against principles, capability fit, or an existing solution design.
---

# Assess Solution

## Quick Start

Run an interview-based assessment of a proposed or existing solution against:

1. The architecture principles available in `principles/`.
2. One user-selected baseline:
   - A capability overview under `capabilities/<slug>/`.
   - A solution architecture design under `solution-architectures/<slug>/`.

If the user has not identified the capability overview or solution design, ask which one to use before starting the assessment. Use the selected baseline and principles to ask focused questions. Do not produce the final report until the user has answered the interview topics and confirmed that the assessment evidence is complete enough.

## Required Inputs

- Solution description, proposal, implementation notes, or path to an existing solution document, gathered or confirmed through the interview.
- Solution supplier, vendor, product company, or implementation partner when the solution depends on an external company.
- Customer references, case studies, testimonials, analyst notes, or reference-call findings when available.
- Assessment baseline: one capability overview or one solution architecture design.
- Architecture principles to assess against. Prefer all principle documents under `principles/` unless the user names a subset.
- Target audience and desired depth, if different from architecture and delivery stakeholders.

## Workflow

1. Start in interview mode. Ask one question at a time and do not generate the final assessment until the interview is complete.
2. Confirm the solution, supplier, and whether to assess against a capability overview or solution architecture design when the baseline is not explicit.
3. Locate and read the selected baseline and architecture principles. If multiple baselines match, ask the user to choose one.
4. Extract baseline expectations to build the interview plan:
   - Business outcome and scope boundary.
   - Main business features or requirements, users, processes, data, integrations, systems, and dependencies.
   - Security, privacy, compliance, non-functional, operational, and lifecycle expectations.
   - Explicit risks, assumptions, constraints, open questions, and design decisions.
5. Interview the user for each main business feature or requirement. Ask for fit, evidence, known gaps, user impact, operational impact, and required action.
6. Interview the user on each assessment topic: ease of use, other features, integrations, target architecture alignment, principle alignment, supplier, references, price indication, risks, constraints, and open questions.
7. After each topic, summarize captured facts, assumptions, missing evidence, and follow-up questions. Ask follow-ups when answers are vague or unsupported.
8. Before writing the report, summarize the evidence collected and ask the user to confirm whether to proceed or answer remaining questions.
9. Assess principle alignment using `Aligned`, `Partly aligned`, `Misaligned`, or `Not enough evidence`.
10. Create the simple 5-star scorecard using the required categories. Use half stars only when the evidence supports a clear midpoint.
11. Identify gaps, risks, trade-offs, and open questions. Do not invent missing facts.
12. Give a practical recommendation:
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
