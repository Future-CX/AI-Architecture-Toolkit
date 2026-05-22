# Write A Principle

Write architecture principle documents under a private lab repository's root `principles/` folder using a preset markdown template.

Always run this skill from a private lab repository where this toolkit is mounted as a submodule, typically `toolkit/`. Generated files must be created beside `toolkit/`, not inside it. Do not write generated principle files under the public toolkit repository or `toolkit/principles/`.

Generated principle documents include a linked list at the top of the `## Principles` section. Each item contains only a first-level principle identifier and name, and links to the matching principle detail section below. If the document has lower-level sub-principles or nested guidance, keep them inside the relevant detail section and exclude them from the top list. Identifiers use a 3-4 letter category code plus a three-digit incremental number starting with `001`, such as `DATA001`. Each principle detail includes identifier, name, description, rationale, consequences, and optional do's and don'ts.

The helper also creates or updates `principles/_principles-list.md` as an alphabetically sorted table with `name`, `description`, and `last_updated` columns.

- [SKILL.md](SKILL.md)
- [Principle template](templates/principle-template.md)
- [Write principle script](scripts/write-principle.py)
