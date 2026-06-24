---
name: problem-to-solution
description: Create stakeholder-ready problem-to-solution briefs that frame a problem, compare solution options with pros and cons, and recommend a way forward. Use when the user asks to address a problem, brainstorm possible solutions, evaluate alternatives, prepare a senior stakeholder decision paper, or write a recommendation brief.
---

# Problem To Solution

## Quick Start

Use this skill to turn an ambiguous problem into a concise decision document for non-technical business stakeholders.

Store generated problem-to-solution briefs under the consuming repository's private lab root in `problem-to-solutions/`.

```text
problem-to-solutions/<problem-slug>-problem-to-solution.md
```

Use `templates/problem-to-solution-template.md` as the output structure. Replace placeholders and drafting guidance with concrete content; do not leave unanswered sections unless the unknown is explicitly marked as `TBD` or an open question. Remove the `## Open Questions` section when there are no open questions.

Problem-to-solution briefs are written for non-technical business stakeholders first. Architects and delivery teams should get enough context to act, but the opening sections must be easy for a business reader to scan, understand, and use in a decision meeting.

Do not write real-company decision context into this public toolkit repository.

## Required Inputs

- Problem statement
- Decision needed
- Decision owner or forum
- Stakeholders and impacted groups
- Business or architecture context
- Constraints, assumptions, and non-goals
- Evaluation criteria
- Candidate solution options
- Recommendation and rationale after solution exploration is complete
- ADR link when the solution is decided

## Workflow

1. Clarify the problem, why it matters now, who needs to decide, and when a decision is needed.
2. Ask for known constraints, non-goals, dependencies, risks, and stakeholder concerns when not already provided.
3. Read related architecture documents when paths are provided.
4. Validate terminology against `<private-lab-root>/GLOSSARY.md` when the brief uses domain-specific applications, capabilities, data objects, or jargon. Use `../ubiquitous-language/SKILL.md` to clarify or update terminology before option brainstorming when important terms are missing, ambiguous, or overloaded.
5. Use `../grill-me/SKILL.md` to pressure-test the problem framing, assumptions, constraints, stakeholder tensions, and evaluation criteria before settling on solution options.
6. Brainstorm 2-5 realistic solution options. Include a "do nothing" or "defer" option only when it is a plausible decision path.
7. Evaluate each option against the same criteria so comparisons are fair and decision-ready.
8. Write balanced pros and cons for each option. Avoid strawman alternatives.
9. Before writing a recommendation, use `../grill-me/SKILL.md` for a dedicated exploration review of all options, pros, cons, assumptions, missing alternatives, hidden constraints, and stakeholder trade-offs. Ask questions one at a time and wait for feedback before concluding the review.
10. Revise the options, pros, cons, criteria, and open questions based on the grill-me session.
11. Only after the grill-me exploration review is complete, recommend one option, or a staged combination, with clear rationale, trade-offs, and conditions for success.
12. Create or update the problem-to-solution brief from `templates/problem-to-solution-template.md`. Preserve the two opening tables: the document metadata table first, followed by the `Integration Overview` table.
13. Run the readability and glossary compliance gate before finishing:

- Use `../check-readability/SKILL.md` against the generated brief.
- Treat the target audience as non-technical business stakeholders unless the user gives a different audience.
- Aim for a Flesch Reading Ease score of 40 or higher.
- If the score is below 40, revise the brief and run the readability check again before finishing, unless required names, legal terms, or quoted source text make the target impractical.
- Read `Glossary.md` or `GLOSSARY.md` when present and remove glossary `Jargon` terms from generated prose, headings, and tables unless they are quoted source text or explicit glossary references.
- Reread the executive summary, problem, context, recommendation, and option comparison sections. Simplify any sentence that a non-technical business reader would need to parse twice.

14. Capture unresolved facts as open questions rather than inventing costs, timelines, risk positions, or stakeholder preferences.
15. When the user confirms the selected solution is decided, approved, or accepted, use `../architecture-decision-record/SKILL.md` to create an ADR for the decision.
16. Link the created ADR from the `Integration Overview` table and `## Relevant Links` section of the problem-to-solution brief.

## Writing Guidance

- Write for non-technical business stakeholders: concise, explicit, and decision-oriented.
- Start with the business outcome, decision needed, recommendation, operational impact, and trade-offs.
- Use plain language first. Add technical detail only when it changes the decision, risk, cost, ownership, timeline, or support model.
- Prefer short sentences, short paragraphs, and concrete nouns. Avoid long setup clauses.
- Separate facts from assumptions and inferred judgments.
- State the decision in one sentence near the top.
- Do not write the recommendation until the grill-me exploration review has challenged the full set of options and trade-offs.
- Once written, make the recommendation easy to find and hard to misread.
- Start with the document metadata table, then the `Integration Overview` fact table with status, decision needed, owner or forum, recommendation, ADR, confidence, and decision timing.
- Put open questions directly under the opening tables. Remove the section entirely when there are no open questions.
- Before a solution is decided, use `TBD` for the ADR field. After the solution is decided, replace `TBD` with the created ADR link.
- Keep options mutually distinct. If two options differ only in implementation detail, merge them or explain the real decision difference.
- Use canonical terminology from the glossary, and call out terminology disputes when they affect the decision.
- Include delivery, operational, financial, security, customer, and organizational impacts when relevant.
- Show material trade-offs, not exhaustive analysis.
- Mark confidence as High, Medium, or Low, and explain what would raise confidence.
- Spell out acronyms on first use unless the expanded form would be misleading or the term is already defined in the glossary.
- Remove vague filler such as "robust", "seamless", "future-proof", "best practice", or "enterprise-grade" unless tied to a concrete requirement, KPI, risk, cost, owner, or decision.
- Keep table cells short. Move detailed explanation into notes or the relevant section when a table becomes hard to scan.

## Readability Gate

Use the `check-readability` skill in `../check-readability/SKILL.md` before finishing a problem-to-solution brief. Treat the target audience as non-technical business stakeholders unless the user gives a different audience. Aim for a Flesch Reading Ease score of 40 or higher.

The brief is not complete until the readability check passes these problem-to-solution expectations:

- Flesch Reading Ease is 40 or higher, or any lower score is explicitly justified because required names, legal terms, or quoted source text make the target impractical.
- The executive summary states the problem, decision needed, recommended option, business impact, and main trade-off in plain language.
- The problem section explains who is affected and what happens if no decision is made.
- The option comparison can be scanned without reading every option detail.
- Risks, owners, costs, timeline effects, dependencies, and open questions are easy to find.
- Glossary `Jargon` terms from `Glossary.md` or `GLOSSARY.md` are removed from generated prose, headings, and tables unless they are quoted source text or explicit glossary references.
- Acronyms are spelled out the first time they appear unless the expanded form would be misleading or the term is already defined in the glossary.
- Open questions are written as answerable questions with an owner or target audience when known.

## Output Rules

- Generated problem-to-solution briefs belong under `<private-lab-root>/problem-to-solutions/`.
- Do not put generated real-company problem-to-solution briefs inside this public toolkit repository.
- Use filenames ending in `-problem-to-solution.md`.
- When the solution is decided, create an ADR with `../architecture-decision-record/SKILL.md`; do not leave ADR creation as a suggestion.
