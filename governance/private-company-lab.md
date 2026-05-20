# Private Company Lab

## Purpose

Use a separate private repository when testing this public toolkit against real company context.

The public `AI-Architecture-Toolkit` repository should contain only reusable agents, skills, templates, examples, and governance guidance. Company-specific context, decisions, glossaries, risks, stakeholder names, internal system names, and generated outputs should stay in the private lab repository.

## Recommended Structure

```text
AI-Architecture-Toolkit-Company-Lab/
├── README.md
├── CONTEXT.md
├── GLOSSARY.md
├── docs/
│   └── adr/
├── company/
│   ├── capabilities.md
│   ├── constraints.md
│   ├── stakeholders.md
│   └── systems.md
├── outputs/
└── toolkit/
```

## Setup With Git Submodule

From the private company lab repository:

```sh
git submodule add https://github.com/Future-CX/AI-Architecture-Toolkit.git toolkit
git commit -m "Add AI Architecture Toolkit submodule"
```

This keeps the public toolkit in `toolkit/` while all private company material lives beside it.

## Updating The Toolkit

From the private company lab repository:

```sh
git submodule update --remote toolkit
git add toolkit
git commit -m "Update AI Architecture Toolkit submodule"
```

## Working Rules

- Put real company context only in the private lab repository.
- Do not commit private company information back into the public toolkit repository.
- Keep generated ADRs in `adr/` in the private lab repository unless they are fully fictionalized examples.
- Keep `GLOSSARY.md` in the private lab repository when it contains company-specific terminology.
- If a reusable pattern emerges, generalize it before copying it back into the public toolkit.

## Useful Private Lab Ignore Rules

Add a `.gitignore` to the private lab repository for local-only files:

```gitignore
.env
.env.*
.private/
*.local.md
```
