# {{DATA_OBJECT}} Data Architecture Design

| Field             | Value                    |
| ----------------- | ------------------------ |
| Confluence Link   | {{CONFLUENCE_LINK}}      |
| Last Update       | {{LAST_UPDATE}}          |
| Open questions    | {{OPEN_QUESTIONS_COUNT}} |
| Readability Score | TBD                      |

## Data Architecture Overview

| Field           | Value                                                 |
| --------------- | ----------------------------------------------------- |
| Data Object     | {{DATA_OBJECT}}                                       |
| Source of Truth | {{SOURCE_OF_TRUTH}}                                   |
| Main Capability | [{{MAIN_CAPABILITY_TITLE}}]({{MAIN_CAPABILITY_LINK}}) |
| Data Owner      | {{DATA_OWNER}}                                        |
| Classification  | {{DATA_CLASSIFICATION}}                               |

## Short Summary

_{{SHORT_SUMMARY}}_

## Description

{{DESCRIPTION}}

## Open Questions

- {{OPEN_QUESTION}}

## Data Object Context

Describe the data object, its business meaning, boundaries, aliases, and relationship to nearby concepts.

## Data Flow

Explain how the data object moves from source through transformations, storage, integrations, and consumers. Describe the flow in the same order as the diagram: process stages across the top, systems or actors as horizontal lanes, and labeled movements between lanes.

![{{DATA_OBJECT}} data flow](diagrams/{{DATA_OBJECT_SLUG}}-data-flow.svg)

Source: [{{DATA_OBJECT_SLUG}}-data-flow.drawio](diagrams/{{DATA_OBJECT_SLUG}}-data-flow.drawio)

| Step | Stage or Event     | From - To             | Data Movement     | Action                           | Notes     |
| ---- | ------------------ | --------------------- | ----------------- | -------------------------------- | --------- |
| 1    | {{STAGE_OR_EVENT}} | {{LANE_TO_LANE_PATH}} | {{DATA_MOVEMENT}} | {{CREATE_UPDATE_READ_TRANSFORM}} | {{NOTES}} |

## Integration Map

Summarize the integrations that produce, transform, enrich, replicate, or consume the data object. Link detailed integration designs instead of duplicating full contracts.

![{{DATA_OBJECT}} integration map](diagrams/{{DATA_OBJECT_SLUG}}-integration-map.svg)

Source: [{{DATA_OBJECT_SLUG}}-integration-map.drawio](diagrams/{{DATA_OBJECT_SLUG}}-integration-map.drawio)

| Integration          | From - To     | Pattern     | Purpose     | Design                                                      |
| -------------------- | ------------- | ----------- | ----------- | ----------------------------------------------------------- |
| {{INTEGRATION_NAME}} | {{DIRECTION}} | {{PATTERN}} | {{PURPOSE}} | [{{INTEGRATION_DESIGN_TITLE}}]({{INTEGRATION_DESIGN_LINK}}) |

## Conceptual Data Model

Describe important relationships, identifiers, aggregates, reference data, master data, and derived data. Add a diagram when relationships materially affect the architecture.

## Ownership and Source of Truth

Document the authoritative owner, source-of-truth application, allowed writers, allowed readers, and stewardship responsibilities.

## Lifecycle

Describe creation, update, deletion, archival, retention, purge, audit, and exception handling across the data object's lifecycle.

## Data Quality and Lineage

Document validation rules, quality dimensions, reconciliation points, lineage expectations, observability, and issue ownership.

## Privacy, Security, and Compliance

Document data classification, sensitive attributes, access controls, consent, residency, masking, encryption, retention, audit, and regulatory constraints.

## Architecture Decisions

List data architecture decisions that are already accepted or need an ADR.

| Decision     | Status     | ADR                           |
| ------------ | ---------- | ----------------------------- |
| {{DECISION}} | {{STATUS}} | [{{ADR_TITLE}}]({{ADR_LINK}}) |

## Relevant Links

- [{{TARGET_ARCHITECTURE_TITLE}}]({{TARGET_ARCHITECTURE_LINK}})
- [{{MAIN_CAPABILITY_TITLE}}]({{MAIN_CAPABILITY_LINK}})
- [{{SOLUTION_ARCHITECTURE_DESIGN_TITLE}}]({{SOLUTION_ARCHITECTURE_DESIGN_LINK}})
- [{{INTEGRATION_DESIGN_TITLE}}]({{INTEGRATION_DESIGN_LINK}})
- [{{ADR_TITLE}}]({{ADR_LINK}})
