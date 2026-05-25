# High-Level Solution Design

Write high-level solution design documents from an existing capability overview under `solution-architectures/<slug>/`.

The workflow reads `capabilities/<capability-slug>/<capability-slug>.md` and creates `solution-architectures/<slug>/<slug>-architecture.md` using the skill template and chapter-level writing guidance. When Mermaid diagrams are created, they are stored as separate `.mmd` source files in the same `solution-architectures/<slug>/` folder, rendered to same-basename `.svg` files, and embedded in the architecture document.

Before any files are created, the workflow must run a `grill-me` style clarification session and update the private lab root `GLOSSARY.md` with `ubiquitous-language` as terms are clarified. If `GLOSSARY.md` was not created or updated afterwards, stop and ask the user to run `grill-me` followed by `ubiquitous-language`.

- [SKILL.md](SKILL.md)
- [High-level solution design template](templates/high-level-solution-design-template.md)
