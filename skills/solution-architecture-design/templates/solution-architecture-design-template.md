# L2 - {{CAPABILITY_NAME}} Solution Architecture

| Field               | Value                                                         |
| ------------------- | ------------------------------------------------------------- |
| Application Name    | {{APPLICATION_NAME}}                                          |
| Capability          | [{{CAPABILITY_NAME}}]({{SOURCE_CAPABILITY_OVERVIEW}})         |
| Target architecture | [{{TARGET_ARCHITECTURE_TITLE}}]({{TARGET_ARCHITECTURE_LINK}}) |
| Domain              | {{DOMAIN}}                                                    |
| Owner(s)            | {{OWNERS}}                                                    |
| Last update         | {{LAST_UPDATE}}                                               |

## Table of Contents

- [Architecture Summary](#architecture-summary)
- [Capability Overview](#capability-overview)
- [Open Questions](#open-questions)
- [Scope and Assumptions](#scope-and-assumptions)
- [Target Technical Implementation](#target-technical-implementation)
- [Application and Component Architecture](#application-and-component-architecture)
- [Data Model and Ownership](#data-model-and-ownership)
- [Data Integrations and Interface Contracts](#data-integrations-and-interface-contracts)
- [Diagrams](#diagrams)
- [Security, Privacy, and Compliance](#security-privacy-and-compliance)
- [NFR and Operational Design](#nfr-and-operational-design)
- [Technical Design Choices](#technical-design-choices)
- [Risks, Dependencies, and Migration Notes](#risks-dependencies-and-migration-notes)
- [Relevant Links](#relevant-links)

## Architecture Summary

{{ARCHITECTURE_SUMMARY:
State the target solution in 3-6 plain-language paragraphs for senior stakeholders. Mention the capability once as context, then focus on the application: what business outcome it enables, what changes for users or operations, the main architectural approach, key application ownership or impact, key constraints, main design consequences, and decisions still needed. Avoid generic benefits, marketing language, acronyms, and implementation jargon unless briefly explained.}}

## Capability Overview

{{CAPABILITY_OVERVIEW:
Link to the source capability overview. Briefly summarize only the capability context needed to understand why this application architecture exists: business purpose, boundary, upstream/downstream business dependencies, triggering business events, expected outcomes, and source assumptions used. Keep this section short and avoid repeating the capability name elsewhere in the document unless needed for clarity. Call out source gaps or contradictions. Do not link ADRs here; ADR links belong in Technical Design Choices.}}

## Open Questions

{{OPEN_QUESTIONS:
List unresolved decisions, missing facts, and review items that block or materially influence the design. Add owner or target audience where known.}}

## Scope and Assumptions

### In Scope

{{IN_SCOPE:
List the technical responsibilities covered by this design.}}

### Out of Scope

{{OUT_OF_SCOPE:
List responsibilities, systems, processes, or decisions intentionally excluded.}}

### Assumptions

{{ASSUMPTIONS:
List testable or reviewable assumptions. Move unresolved decisions to Open Questions.}}

## Target Technical Implementation

{{TARGET_TECHNICAL_IMPLEMENTATION:
Describe the target runtime solution around the application, including services, components, platforms, deployment model, environments, operational ownership, lifecycle flows, and relevant technical standards or constraints.}}

## Application and Component Architecture

{{APPLICATION_AND_COMPONENT_ARCHITECTURE:
Identify the main application, supporting services, modules, integration components, user interfaces, and shared platforms. For each, describe responsibility, ownership, key dependencies, and whether it is new, changed, reused, or retired. Make component boundaries explicit.}}

## Data Model and Ownership

{{DATA_MODEL_AND_OWNERSHIP:
Define canonical business data objects, their meaning, owner or source of truth, lifecycle, consumers, relationships, identifiers, retention needs, privacy classification, and mappings to application-specific representations.}}

## Data Integrations and Interface Contracts

{{DATA_INTEGRATIONS_AND_INTERFACE_CONTRACTS:
Describe each API, event, file, batch, stream, or manual handoff. For each, state producer, consumer, payload or data object, trigger, frequency, protocol or pattern, ownership, error handling, retry/idempotency needs, and observability.}}

## Diagrams

### Capability Context

{{CAPABILITY_CONTEXT_DIAGRAM_REFERENCE:
Embed capability-context.svg and link to capability-context.drawio when created. Show actors, neighboring capabilities, and external dependencies.}}

### Application and Component View

{{APPLICATION_COMPONENT_DIAGRAM_REFERENCE:
Embed application-component-view.svg and link to application-component-view.drawio when created. Show applications, services, components, platforms, and major responsibilities.}}

### Conceptual Data Model

{{CONCEPTUAL_DATA_MODEL_DIAGRAM_REFERENCE:
Embed conceptual-data-model.svg and link to conceptual-data-model.drawio when created. Show canonical data objects and meaningful relationships.}}

### Integration Flow

{{INTEGRATION_FLOW_DIAGRAM_REFERENCE:
Embed integration-flow.svg and link to integration-flow.drawio when created. Show direction, trigger, protocol or pattern, and important sequencing.}}

## Security, Privacy, and Compliance

{{SECURITY_PRIVACY_AND_COMPLIANCE:
Describe authentication, authorization, identity propagation, secrets, encryption, audit logging, data protection, consent, retention, regulatory constraints, trust boundaries, and privileged operations where relevant.}}

## NFR and Operational Design

{{NFR_AND_OPERATIONAL_DESIGN:
Cover availability, resilience, performance, scalability, latency, recovery, observability, support model, deployment, release, backup, monitoring, alerting, incident response, measurable targets where known, failure modes, and operational ownership.}}

## Technical Design Choices

| Decision     | Choice     | Alternatives considered     | Rationale     | Trade-offs     | ADR                    |
| ------------ | ---------- | --------------------------- | ------------- | -------------- | ---------------------- |
| {{DECISION}} | {{CHOICE}} | {{ALTERNATIVES_CONSIDERED}} | {{RATIONALE}} | {{TRADE_OFFS}} | {{ADR_LINK_OR_STATUS}} |

## Risks, Dependencies, and Migration Notes

### Risks

{{RISKS:
List risks with cause, impact, mitigation, and owner where known.}}

### Dependencies

{{DEPENDENCIES:
List external decisions, teams, systems, platforms, data, vendors, or prerequisites needed.}}

### Migration Notes

{{MIGRATION_NOTES:
Explain transition states, coexistence, cutover, rollback, data migration, compatibility, and decommissioning concerns.}}

## Relevant Links

- [Capability Overview: {{SOURCE_CAPABILITY_OVERVIEW_TITLE}}]({{SOURCE_CAPABILITY_OVERVIEW}})
- [Target Architecture: {{TARGET_ARCHITECTURE_TITLE}}]({{TARGET_ARCHITECTURE_LINK}})
- {{RELEVANT_LINK}}
