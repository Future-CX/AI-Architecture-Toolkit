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
7. Use `--dry-run` first when the target page, parent page, or conversion output is uncertain.
8. Prefer `--overview-title <title>` when the overview page is not named `Overview`.
9. Publish with the helper script.
10. Record the returned page URL and page ID in the working notes or handoff summary.

## Behavior

The script uses `--title` when creating a new page. Otherwise, it derives the new page title from the first non-empty line of the source document. When updating an existing page from a `Confluence Link`, the script preserves the existing Confluence page title and does not rename it. For markdown publishing, the first non-empty line is removed from the Confluence body so the page title does not appear twice.

When a top metadata table includes a `Confluence Link` row, the script extracts the page ID from URLs such as `https://example.atlassian.net/wiki/spaces/ARCH/pages/677838849/L2+-+Promotions` and updates that page directly. In that example, the page ID is `677838849`.

For markdown publishing, a leading `Field` / `Value` metadata table is also removed from the Confluence body. The table can stay in the source file for toolkit tracking without being shown at the top of the published page.

For markdown publishing, links to local `.md` files are rewritten before conversion. The script resolves each local markdown link relative to the source file, reads the linked file's top `Field` / `Value` metadata table, and replaces the markdown file target with that file's `Confluence Link`. If the linked file does not exist or has no usable top-table `Confluence Link`, the published body keeps the link text as plain text and does not create a Confluence link.

If no Confluence page ID is found, the script always prompts the user to choose before credential loading, dry-run output, source updates, page creation, or publishing. The user can provide an existing Confluence link, or choose to create the page as a child of the overview page. The overview page is found by title in the target space and defaults to `Overview`; override this with `--overview-title <title>`.

When the script creates a new child page, it writes the returned Confluence link back to the source markdown, regenerates the content, and updates the new page so the Confluence copy contains the link too.

Markdown conversion uses the optional `markdown` package when installed. Without it, the script falls back to a small built-in converter for headings, paragraphs, lists, links, inline code, fenced code blocks, and bold text. For highly formatted documents, convert to storage-safe HTML before publishing.

Use `--content-format html` to publish HTML directly, or `--content-format markdown` to force markdown conversion.

## Script

See [README.md](README.md) and [scripts/publish-to-confluence.py](scripts/publish-to-confluence.py).
