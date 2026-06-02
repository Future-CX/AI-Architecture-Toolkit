---
name: problem-to-solution
description: Create stakeholder-ready problem-to-solution briefs that frame a problem, compare solution options with pros and cons, and recommend a way forward. Use when the user asks to address a problem, brainstorm possible solutions, evaluate alternatives, prepare a senior stakeholder decision paper, or write a recommendation brief.
---

# Problem To Solution

## Quick Start

Use this skill to turn an ambiguous problem into a concise decision document for senior stakeholders.

Store generated problem-to-solution briefs under the consuming repository's private lab root in `problem-to-solutions/`.

```text
problem-to-solutions/<problem-slug>-problem-to-solution.md
```

Use `templates/problem-to-solution-template.md` as the output structure. Replace placeholders and drafting guidance with concrete content; do not leave unanswered sections unless the unknown is explicitly marked as `TBD` or an open question. Remove the `## Open Questions` section when there are no open questions.

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
12. Create or update the problem-to-solution brief from `templates/problem-to-solution-template.md`.
13. Capture unresolved facts as open questions rather than inventing costs, timelines, risk positions, or stakeholder preferences.
14. When the user confirms the selected solution is decided, approved, or accepted, use `../architecture-decision-record/SKILL.md` to create an ADR for the decision.
15. Link the created ADR from the top context table and `## Relevant Links` section of the problem-to-solution brief.

## Writing Guidance

- Write for senior stakeholders: concise, explicit, and decision-oriented.
- Separate facts from assumptions and inferred judgments.
- State the decision in one sentence near the top.
- Do not write the recommendation until the grill-me exploration review has challenged the full set of options and trade-offs.
- Once written, make the recommendation easy to find and hard to misread.
- Put open questions directly under the top context table. Remove the section entirely when there are no open questions.
- Before a solution is decided, use `TBD` for the ADR field. After the solution is decided, replace `TBD` with the created ADR link.
- Keep options mutually distinct. If two options differ only in implementation detail, merge them or explain the real decision difference.
- Use canonical terminology from the glossary, and call out terminology disputes when they affect the decision.
- Include delivery, operational, financial, security, customer, and organizational impacts when relevant.
- Use plain business language first; add technical detail only where it affects the decision.
- Show material trade-offs, not exhaustive analysis.
- Mark confidence as High, Medium, or Low, and explain what would raise confidence.

## Output Rules

- Generated problem-to-solution briefs belong under `<private-lab-root>/problem-to-solutions/`.
- Do not put generated real-company problem-to-solution briefs inside this public toolkit repository.
- Use filenames ending in `-problem-to-solution.md`.
- When the solution is decided, create an ADR with `../architecture-decision-record/SKILL.md`; do not leave ADR creation as a suggestion.
