---
name: publish-to-confluence
description: Publish markdown or HTML content to Confluence pages through the Confluence REST API. Use when the user asks to publish, create, update, sync, or push architecture content, documents, ADRs, designs, or generated toolkit artifacts to Confluence.
---

# Publish To Confluence

## Quick Start

Publish a markdown or HTML file to Confluence using the helper script:

```sh
python3 skills/publish-to-confluence/scripts/publish-to-confluence.py path/to/document.md \
  --space-key ARCH
```

When this toolkit is used as a submodule in a private lab repository, run the script from the private lab root:

```sh
python3 toolkit/skills/publish-to-confluence/scripts/publish-to-confluence.py outputs/design.md
```

## Inputs

- `CONFLUENCE_BASE_URL`, such as `https://example.atlassian.net/wiki`.
- `CONFLUENCE_EMAIL` and `CONFLUENCE_API_TOKEN` for Confluence Cloud basic authentication.
- `CONFLUENCE_SPACE_KEY` for the default Confluence publishing space.
- A source `.md`, `.html`, or `.htm` file.
- Any local image files referenced by markdown image syntax, such as `![Diagram](diagram.svg)`.
- A page title in the first line of the source document.
- Optional overview page title. Defaults to `Overview`.

Never commit API tokens, credentials, private Confluence URLs, customer names, or real company content to this public toolkit repository.

## Credential Storage

The helper loads Confluence settings from `.env` in the current working directory. When values are missing, it asks the user for them and stores the missing values in that `.env` file with owner-only file permissions.

When this toolkit is mounted as `toolkit/` in a private lab repo, always run the command from the private lab root so credentials are stored in `<private-lab-root>/.env`, not in the public toolkit submodule.

The expected `.env` keys are:

```sh
CONFLUENCE_BASE_URL="https://example.atlassian.net/wiki"
CONFLUENCE_EMAIL="name@example.com"
CONFLUENCE_API_TOKEN="..."
CONFLUENCE_SPACE_KEY="ARCH"
```

Use `--env-file <path>` only when the private repo keeps local secrets somewhere other than `<private-lab-root>/.env`.

Use `--space-key <key>` when publishing to a different space for one run. If `.env` does not yet contain `CONFLUENCE_SPACE_KEY`, the script stores the provided `--space-key` value there.

## Workflow

1. Confirm the source file is safe to publish to the target Confluence space.
2. Run the helper from the private lab root, or pass `--env-file` pointing to the private repo's local `.env`.
3. Let the helper prompt for missing Confluence settings during the first interactive run.
4. Use the first line of the document as the Confluence page title. A markdown heading like `# L2 - Promotions` becomes `L2 - Promotions`. The first line is not included in the published Confluence body.
5. If the top metadata table contains `Confluence Link`, use the page ID from that link as the target page to update.
6. If no Confluence page ID is found, stop immediately and ask the user which option they want before checking credentials, running a dry run, creating a page, updating a source file, or publishing. Do not choose for the user:
   - Ask for an existing `Confluence Link`. After the user provides it, update the source markdown first, then publish to that page.
   - Ask whether to create the page under the Confluence overview page. If the user chooses this, find the overview page, create a new child page, then update the source markdown with the returned `Confluence Link`.
7. Before a real publish, always check Git for open changes to the source document, linked local images, embedded SVG diagram files, same-basename `.drawio` files for embedded SVG diagrams, and local Markdown links to `.drawio` or `.svg` diagrams. Only ask about committing when Git reports open changes for those files. If any of those files have changes, explicitly ask the user whether to commit those publish-related files before publishing. If the user chooses yes, ask for a commit message and create the Git commit. If the user chooses no, skip the Git commit and continue publishing.
8. Use `--dry-run` first when the target page, parent page, or conversion output is uncertain.
9. Prefer `--overview-title <title>` when the overview page is not named `Overview`.
10. When the markdown references local images or SVG files, make sure those files exist beside the markdown or at the referenced relative path before publishing.
11. Publish with the helper script.
12. After a successful publish, check Git again for the source document and linked images or diagrams. Only ask about committing when Git reports open changes for those files.
13. Record the returned page URL, page ID, and Git Commit in the working notes or handoff summary.

## Behavior

The script uses `--title` when creating a new page. Otherwise, it derives the new page title from the first non-empty line of the source document. When updating an existing page from a `Confluence Link`, the script preserves the existing Confluence page title and does not rename it. For markdown publishing, the first non-empty line is removed from the Confluence body so the page title does not appear twice.

When a top metadata table includes a `Confluence Link` row, the script extracts the page ID from URLs such as `https://example.atlassian.net/wiki/spaces/ARCH/pages/677838849/L2+-+Promotions` and updates that page directly. In that example, the page ID is `677838849`.

For markdown publishing, a leading `Field` / `Value` metadata table is also removed from the Confluence body. The table can stay in the source file for toolkit tracking without being shown at the top of the published page.

For markdown publishing, links to local `.md` files are rewritten before conversion. The script resolves each local markdown link relative to the source file, reads the linked file's top `Field` / `Value` metadata table, and replaces the markdown file target with that file's `Confluence Link`. If the linked file does not exist or has no usable top-table `Confluence Link`, the published body keeps the link text as plain text and does not create a Confluence link.

For markdown publishing, local image references such as `![Diagram](diagram.svg)` or `![Screenshot](images/screen.png)` are uploaded to the target Confluence page as attachments. The published page body is rewritten to use Confluence attachment image macros so the images render from the page attachments. If an attachment with the same filename already exists on the page, the script uploads a new attachment version. Missing local image files stop the publish.

Markdown or HTML same-page anchors are rewritten to Confluence storage format. Links such as `[ARCH001](#arch001)` become Confluence anchor links, and raw anchors such as `<a id="arch001"></a>` or `<a name="arch001"></a>` become Confluence anchor macros instead of visible plain text.

Before a real publish, the script checks Git for open changes to the source document, embedded local image or SVG diagram files, same-basename `.drawio` files for embedded SVG diagrams, and local Markdown links to `.drawio` or `.svg` diagrams. If any of those files have open changes, the script asks whether to commit those publish-related files before publishing. Choosing yes prompts for a commit message and commits only those publish-related files. Choosing no skips the commit and continues. After a successful publish, the script checks those files again and asks the same commit question only when Git reports remaining changes for those files. Use `--skip-git-check` only for automation where this prompt is intentionally bypassed.

If no Confluence page ID is found, the script always prompts the user to choose before credential loading, dry-run output, source updates, page creation, or publishing. The user can provide an existing Confluence link, or choose to create the page as a child of the overview page. The overview page is found by title in the target space and defaults to `Overview`; override this with `--overview-title <title>`.

When the script creates a new child page, it writes the returned Confluence link back to the source markdown, regenerates the content, and updates the new page so the Confluence copy contains the link too.

Markdown conversion uses the optional `markdown` package when installed. Without it, the script falls back to a small built-in converter for headings, paragraphs, pipe tables, lists, links, inline code, fenced code blocks, and bold text. For highly formatted documents, convert to storage-safe HTML before publishing.

Fenced markdown code blocks are converted to Confluence `code` macros. A language hint such as ```` ```python ```` is carried into the macro language parameter when present.

Use `--content-format html` to publish HTML directly, or `--content-format markdown` to force markdown conversion.

## Script

See [README.md](README.md) and [scripts/publish-to-confluence.py](scripts/publish-to-confluence.py).
