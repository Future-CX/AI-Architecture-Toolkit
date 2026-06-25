# Integration Design Template

| Field             | Value                    |
| ----------------- | ------------------------ |
| Confluence Link   | {{CONFLUENCE_LINK}}      |
| Last Update       | {{LAST_UPDATE}}          |
| Open questions    | {{OPEN_QUESTIONS_COUNT}} |
| Readability Score | TBD                      |

## Integration Overview

| Field          | Value                                               |
| -------------- | --------------------------------------------------- |
| Status         | {{INTEGRATION_STATUS}}                              |
| Purpose        | {{INTEGRATION_PURPOSE_ONE_SENTENCE_UNDER_25_WORDS}} |
| Source         | {{SOURCE_SYSTEM}}                                   |
| Destination    | {{DESTINATION_SYSTEM}}                              |
| Data object    | {{DATA_OBJECT}}                                     |
| Trigger        | {{INTEGRATION_TRIGGER}}                             |
| Pattern        | {{INTEGRATION_PATTERN}}                             |
| Open questions | {{OPEN_QUESTIONS_COUNT}}                            |

## Business Summary

### Business Outcome

{{WHAT_THIS_ENABLES_IN_2_TO_4_SHORT_SENTENCES}}

![{{INTEGRATION_NAME}} integration diagram](diagrams/{{INTEGRATION_DIAGRAM_SVG}})

### Operational Impact

- {{WHAT_CHANGES_FOR_USERS_OR_TEAMS}}
- {{WHAT_HAPPENS_IF_THIS_IS_DELAYED_OR_FAILS}}
- {{WHO_NEEDS_TO_RESPOND}}

### Failure Impact

- What users, teams, or processes are affected if this integration fails: {{FAILURE_IMPACT}}
- What business work stops, slows down, or needs manual handling: {{BUSINESS_CONTINUITY_IMPACT}}
- How quickly the issue must be noticed or resolved: {{FAILURE_RESPONSE_EXPECTATION}}

### Ownership

| Responsibility            | Owner                         |
| ------------------------- | ----------------------------- |
| Business owner            | {{BUSINESS_OWNER}}            |
| Source system owner       | {{SOURCE_SYSTEM_OWNER}}       |
| Destination system owner  | {{DESTINATION_SYSTEM_OWNER}}  |
| Integration support owner | {{INTEGRATION_SUPPORT_OWNER}} |
| Escalation contact        | {{ESCALATION_CONTACT}}        |

### Scope

- In scope: {{IN_SCOPE}}
- Out of scope: {{OUT_OF_SCOPE}}

## Open Questions

- {{OPEN_QUESTION}}

## Pattern

Synchronous API | Event-driven | Batch | File transfer | Messaging | Orchestration

## Contract

Document endpoints, example payloads, schemas, topics, queues, protocols, and versioning.

Place sample API payloads in fenced `javascript` code blocks so comments can explain important fields:

```javascript
{
  // Explain business meaning, ownership, or mapping rules where useful.
  "exampleField": "example value"
}
```

## Integration Qualities

Capture latency, throughput, ordering, reliability, idempotency, retries, and failure handling.

## Security and Operations

Document authentication, authorization, encryption, monitoring, alerting, and support ownership.

## Relevant Links

- [Capability Overview: {{CAPABILITY_OVERVIEW_TITLE}}]({{CAPABILITY_OVERVIEW_LINK}})
- [Target Architecture: {{TARGET_ARCHITECTURE_TITLE}}]({{TARGET_ARCHITECTURE_LINK}})
- [{{SOLUTION_ARCHITECTURE_DESIGN_TITLE}}]({{SOLUTION_ARCHITECTURE_DESIGN_LINK}})
- {{RELEVANT_LINK}}
