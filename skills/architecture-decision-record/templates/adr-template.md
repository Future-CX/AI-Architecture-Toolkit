# Architecture Decision Record Template

ADRs live in the consuming repository's root `adr/` folder and use sequential numbering: `adr-0001-slug.md`, `adr-0002-slug.md`, etc.

Create the `adr/` directory lazily in the consuming repository root — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

| Field | Value |
| --- | --- |
| Confluence Link | {{CONFLUENCE_LINK}} |
| Last Update | {{LAST_UPDATE}} |
| Readability Score | TBD |

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording _that_ a decision was made and _why_ — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering. List the options as bullets first, then add a comparison table with one column per option and rows for Architecture Fit, Company Fit, Effort, and Complexity.
- **Consequences** — only when non-obvious downstream effects need to be called out

### Considered Options Format

Use this structure when the ADR includes considered options:

```md
## Considered Options

- Option 1: {{OPTION_1_NAME}}
- Option 2: {{OPTION_2_NAME}}
- Option 3: {{OPTION_3_NAME}}

| Criteria | Option 1: {{OPTION_1_NAME}} | Option 2: {{OPTION_2_NAME}} | Option 3: {{OPTION_3_NAME}} |
| --- | --- | --- | --- |
| Architecture Fit | {{OPTION_1_ARCHITECTURE_FIT}} | {{OPTION_2_ARCHITECTURE_FIT}} | {{OPTION_3_ARCHITECTURE_FIT}} |
| Company Fit | {{OPTION_1_COMPANY_FIT}} | {{OPTION_2_COMPANY_FIT}} | {{OPTION_3_COMPANY_FIT}} |
| Effort | {{OPTION_1_EFFORT}} | {{OPTION_2_EFFORT}} | {{OPTION_3_EFFORT}} |
| Complexity | {{OPTION_1_COMPLEXITY}} | {{OPTION_2_COMPLEXITY}} | {{OPTION_3_COMPLEXITY}} |

## Recommendation

Recommend {{PREFERRED_OPTION}} because {{WHY_THIS_OPTION_IS_PREFERRED}}. Explain the trade-offs that make this option stronger than the alternatives, including the architecture fit, company fit, effort, complexity, and any consequences the decision owner should accept.
```

## Numbering

Scan `adr/` for the highest existing `adr-<4-digits>-*.md` number and increment by one. If legacy `0001-*.md` ADRs already exist, include them when choosing the next number, but write new ADRs with the `adr-` prefix.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it — otherwise someone will suggest GraphQL again in six months.
