# Write A Capability Overview

Write business capability overview documents under the consuming repository's root `capabilities/<slug>/` folder using a preset markdown template.

Before any files are created or the helper script is run, the workflow must run a `grill-me` style clarification session and update the private lab root `GLOSSARY.md` with `ubiquitous-language` as terms are clarified. If `GLOSSARY.md` was not created or updated afterwards, stop and ask the user to run `grill-me` followed by `ubiquitous-language`.

When this toolkit is used as a submodule, run the helper script from the private repository root so generated files are created beside `toolkit/`, not inside it.

The helper also creates or updates `capabilities/_capability-list.md` as an alphabetically sorted table with `name`, `description`, and `last_updated` columns. Links point to `<slug>/<slug>.md`.

- [SKILL.md](SKILL.md)
- [Capability overview template](templates/capability-overview-template.md)
- [Write capability overview script](scripts/write-capability-overview.py)
