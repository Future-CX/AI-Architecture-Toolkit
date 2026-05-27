# Solution Architecture Design

Write solution architecture design documents from an existing capability overview under `solution-architectures/<slug>/`.

The workflow reads `capabilities/<capability-slug>/<capability-slug>.md` and creates `solution-architectures/<slug>/<slug>-architecture.md` using the skill template and chapter-level writing guidance. Diagrams are created as editable Draw.io `.drawio` files from reusable diagram templates, exported to same-basename `.svg` files when embedded, and linked from the architecture document.

Before any files are created, the workflow must run a `grill-me` style clarification session and update the private lab root `GLOSSARY.md` with `ubiquitous-language` as terms are clarified. If `GLOSSARY.md` was not created or updated afterwards, stop and ask the user to run `grill-me` followed by `ubiquitous-language`.

- [SKILL.md](SKILL.md)
- [Solution architecture design template](templates/solution-architecture-design-template.md)
