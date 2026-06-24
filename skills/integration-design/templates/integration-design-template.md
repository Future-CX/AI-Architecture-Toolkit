# Integration Design Template

| Field             | Value                    |
| ----------------- | ------------------------ |
| Confluence Link   | {{CONFLUENCE_LINK}}      |
| Last Update       | {{LAST_UPDATE}}          |
| Open questions    | {{OPEN_QUESTIONS_COUNT}} |
| Readability Score | TBD                      |

## Integration Overview

| Field          | Value                    |
| -------------- | ------------------------ |
| Status         | {{INTEGRATION_STATUS}}   |
| Purpose        | {{INTEGRATION_PURPOSE}}  |
| Source         | {{SOURCE_SYSTEM}}        |
| Destination    | {{DESTINATION_SYSTEM}}   |
| Data object    | {{DATA_OBJECT}}          |
| Trigger        | {{INTEGRATION_TRIGGER}}  |
| Pattern        | {{INTEGRATION_PATTERN}}  |
| Open questions | {{OPEN_QUESTIONS_COUNT}} |

Describe the integration purpose, source systems, target systems, and business process.

![{{INTEGRATION_NAME}} integration diagram](diagrams/{{INTEGRATION_DIAGRAM_SVG}})

## Open Questions

A bullet list of open questions.

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
