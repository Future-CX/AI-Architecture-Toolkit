---
name: grill-me
description: Grilling session that challenges a plan against the existing domain model, sharpens terminology with the ubiquitous-language skill, and records durable decisions with the architecture-decision-record skill. Use when user wants to stress-test a plan against their project's language and documented decisions.
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

</what-to-do>

<related-skills>

Use related skills during the grilling session when their trigger conditions appear:

- Use `ubiquitous-language` when terms are vague, overloaded, conflicting, or important enough to become shared domain language. Read and update `GLOSSARY.md` using the rules in `../ubiquitous-language/SKILL.md`.
- Use `architecture-decision-record` when a decision is hard to reverse, surprising without context, and the result of a real trade-off. Record ADRs using `../architecture-decision-record/templates/adr-template.md`.

Do not duplicate those workflows inside this skill. Delegate glossary wording and ADR formatting to the related skill instructions, then return to the grilling sequence.

</related-skills>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
```

Create files lazily — only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update glossary inline

When a term is resolved, update `GLOSSARY.md` right there using the `ubiquitous-language` skill. Don't batch these up — capture them as they happen.

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the `architecture-decision-record` skill and the format in `../architecture-decision-record/templates/adr-template.md`.

</supporting-info>
