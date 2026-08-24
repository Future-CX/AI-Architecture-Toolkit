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
| Readability Score | TBD, target 40+ |

{Opening summary, maximum two short paragraphs. State the business outcome, context, and operational impact. Explain any necessary technical term here or in a glossary.}

{Optional second short paragraph. Keep implementation detail out unless it changes the decision.}

## Decision

{State the selected option and its important boundaries in direct language.}

## Reference Links

- [ADR Overview]({{ADR_OVERVIEW_CONFLUENCE_LINK}})
- [This ADR]({{CONFLUENCE_LINK}})
```

That's it. An ADR can be a short summary. The value is in recording _that_ a decision was made and _why_ — not in filling out sections.

Before publishing, make a final readability pass. Target a Readability Score of 40 or higher, shorten long sentences, split dense paragraphs, and replace dense technical terms with plain words where possible.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering. List the options as bullets first, then add a comparison table with one column per option and required rows for Architecture Fit, Company Fit, Effort, and Complexity. Keep each table cell to one sentence, no more than about 15 words, and avoid implementation detail unless it changes the decision.
- **Consequences** — only when non-obvious downstream effects need to be called out. Keep this section to 3-6 bullets.

### Considered Options Format

Use this structure when the ADR includes considered options:

```md
## Decision

{{STATE_THE_SELECTED_OPTION_AND_ITS_IMPORTANT_BOUNDARIES}}

## Considered Options

- Option 1: {{OPTION_1_NAME}}
- Option 2: {{OPTION_2_NAME}}
- Option 3: {{OPTION_3_NAME}}

| Criteria | Option 1: {{OPTION_1_NAME}} | Option 2: {{OPTION_2_NAME}} | Option 3: {{OPTION_3_NAME}} |
| --- | --- | --- | --- |
| Architecture Fit | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} |
| Company Fit | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} |
| Effort | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} |
| Complexity | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} | {{ONE_SENTENCE_MAX_15_WORDS}} |

## Recommendation

Recommend {{PREFERRED_OPTION}} because {{WHY_THIS_OPTION_IS_PREFERRED}}. Explain the trade-offs that make this option stronger than the alternatives.

## Consequences

- {{CONSEQUENCE_1}}
- {{CONSEQUENCE_2}}
- {{CONSEQUENCE_3}}

## Reference Links

- [ADR Overview]({{ADR_OVERVIEW_CONFLUENCE_LINK}})
- [This ADR]({{CONFLUENCE_LINK}})
```

### Compact Example

Use this shape as the model for future ADRs:

```md
# Use Events Between Ordering And Billing

| Field | Value |
| --- | --- |
| Confluence Link | {{CONFLUENCE_LINK}} |
| Last Update | 2026-06-25 |
| Readability Score | 44 |

Checkout currently depends on Billing responding immediately. A Billing outage can therefore stop customers from completing an order.

The integration must keep checkout responsive when Billing is slow while preserving clear ownership between the systems.

## Decision

Ordering and Billing will communicate through domain events instead of direct API calls or a shared database.

## Considered Options

- Option 1: Events
- Option 2: Direct API calls
- Option 3: Shared database

| Criteria | Option 1: Events | Option 2: Direct API calls | Option 3: Shared database |
| --- | --- | --- | --- |
| Architecture Fit | Keeps systems separate and supports independent release. | Creates runtime dependency between two systems. | Blurs ownership of customer and order data. |
| Company Fit | Matches the goal of team autonomy. | Fits current skills but slows future change. | Conflicts with ownership and audit expectations. |
| Effort | Needs message setup and monitoring. | Lowest short-term build effort. | Needs data model changes and migration planning. |
| Complexity | Adds delivery and retry handling. | Simple flow but fragile during outages. | Creates hidden coupling across teams. |

## Recommendation

Recommend events because they protect checkout and support independent team changes.

## Consequences

- Teams must monitor failed and delayed events.
- Billing updates may appear after checkout completes.
- Support teams need clear status messages for delayed billing.

## Reference Links

- [ADR Overview](https://example.atlassian.net/wiki/spaces/ARCH/pages/100/ADR+Overview)
- [This ADR](https://example.atlassian.net/wiki/spaces/ARCH/pages/101/Use+Events+Between+Ordering+And+Billing)
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
