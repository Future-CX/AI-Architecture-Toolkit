---
name: ubiquitous-language
description: Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to GLOSSARY.md. Use when user wants to define domain terms, build a glossary, harden terminology, create a ubiquitous language, or mentions "domain model" or "DDD".
disable-model-invocation: true
---

# Ubiquitous Language

Extract and formalize domain terminology from the current conversation into a consistent glossary, saved to a local file.

## Process

1. **Scan the conversation** for domain-relevant nouns, verbs, concepts, and known applications
2. **Identify problems**:
   - Same word used for different concepts (ambiguity)
   - Different words used for the same concept (synonyms)
   - Vague or overloaded terms
3. **Propose a canonical glossary** with opinionated term choices
4. **Write to `GLOSSARY.md`** in the working directory using the format below
5. **Maintain the table of contents** immediately below `# Glossary`
6. **Output a summary** inline in the conversation

## Output Format

Write a `GLOSSARY.md` file with this structure:

```md
# Glossary

## Table of Contents

- [Applications](#applications)
- [Data objects](#data-objects)
- [Flagged ambiguities](#flagged-ambiguities)
- [Order lifecycle](#order-lifecycle)
- [People](#people)
- [Relationships](#relationships)

## Order lifecycle

| Term        | Definition                                                                             | Aliases to avoid      |
| ----------- | -------------------------------------------------------------------------------------- | --------------------- |
| **Invoice** | A request for payment sent to a customer after delivery<br>- Billing: Billing Document | Bill, payment request |
| **Order**   | A customer's request to purchase one or more items<br>- ERP: Sales Order               | Purchase, transaction |

## People

| Term         | Definition                                                                   | Aliases to avoid       |
| ------------ | ---------------------------------------------------------------------------- | ---------------------- |
| **Customer** | A person or organization that places orders<br>- Commerce Platform: B2B Unit | Client, buyer, account |
| **User**     | An authentication identity in the system<br>- Commerce Platform: Customer    | Login, account         |

## Applications

| Application           | Definition                                                        | Capabilities and functions delivered                                                                                                                |
| --------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Commerce Platform** | Application used to manage digital commerce interactions.         | Customer Management, Product Catalog, Order Capture<br>- Manage B2B units<br>- Maintain customer accounts<br>- Publish articles<br>- Capture orders |
| **ERP**               | System of record for core operational and financial transactions. | Order Management, Inventory Management, Financial Accounting<br>- Maintain sales orders<br>- Manage stock positions<br>- Post invoices              |

## Data objects

| Data object      | Definition                                                      | Owner or source of truth |
| ---------------- | --------------------------------------------------------------- | ------------------------ |
| **Availability** | Structured information representing whether something can sell. | Inventory Management     |
| **Customer**     | Structured information representing a person or organization.   | CRM                      |
| **Order**        | Structured information representing a customer's purchase.      | ERP                      |
| **Price**        | Structured information representing the amount charged.         | Pricing                  |
| **Product**      | Structured information representing an item offered for sale.   | Product Management       |

## Relationships

- An **Invoice** belongs to exactly one **Customer**
- An **Order** produces one or more **Invoices**

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — these are distinct concepts: a **Customer** places orders, while a **User** is an authentication identity that may or may not represent a **Customer**.
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others as aliases to avoid.
- **Flag conflicts explicitly.** If a term is used ambiguously in the conversation, call it out in the "Flagged ambiguities" section with a clear recommendation.
- **Only include terms relevant for domain experts.** Skip the names of modules or classes unless they have meaning in the domain language.
- **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
- **Show relationships.** Use bold term names and express cardinality where obvious.
- **Only include domain terms.** Skip generic programming concepts (array, function, endpoint) unless they have domain-specific meaning.
- **Maintain a table of contents.** Every time `GLOSSARY.md` is created or updated, rebuild the `## Table of Contents` section immediately below `# Glossary`. Include every main glossary section heading below the title, excluding `## Table of Contents` itself. Sort ToC entries alphabetically by heading text and link to the Markdown anchor, e.g. `[Data objects](#data-objects)`.
- **Sort rows alphabetically.** In every glossary table, sort rows alphabetically by the value in the first column, ignoring Markdown bold markers and case.
- **Group terms into multiple tables** when natural clusters emerge (e.g. by subdomain, lifecycle, or actor). Each group gets its own heading and table. If all terms belong to a single cohesive domain, one table is fine — don't force groupings.
- **Maintain an Applications section.** List known applications in a dedicated `## Applications` section using columns for `Application`, `Definition`, and `Capabilities and functions delivered`. Keep application definitions short and business-facing. Use the combined delivery column to name supported business capabilities first, followed by dash-prefixed concrete functions the application performs.
- **Maintain a Data objects section when data objects are discussed.** List data objects in a dedicated `## Data objects` section using columns for `Data object`, `Definition`, and `Owner or source of truth`. Keep data objects general and canonical, using business-level names such as **Product**, **Customer**, **User**, **Order**, **Price**, and **Availability**. Do not create application-specific data objects such as `SAP Material`, `Commerce Product`, `CRM Account`, `ERP Sales Order`, or API/resource/table names. Capture application-specific names as mappings on the canonical term when useful.
- **Map application-owned terms to canonical terms.** When an application uses its own name for an existing domain object, do not create a separate glossary term. Add it inside the canonical term's `Definition` cell after the definition sentence as a dash-prefixed entry, using the format `<br>- <Application>: <Application-owned term>`. For example, if the canonical term is **Customer** and an application calls it `B2B Unit`, add `<br>- Commerce Platform: B2B Unit` inside the **Customer** definition.
- **Use application-owned terms only as mappings.** Application-owned terms explain translation between systems and domain language; they are not canonical terms unless the business also uses them as the shared domain term.

## Re-running

When invoked again in the same conversation:

1. Read the existing `GLOSSARY.md`
2. Incorporate any new terms from subsequent discussion
3. Update definitions if understanding has evolved
4. Re-flag any new ambiguities
5. Rebuild the `## Table of Contents` section from the current main section headings
