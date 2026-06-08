# Publish To Confluence

Publish toolkit-generated markdown or HTML documents to Confluence through the Confluence REST API.

The helper script can create a new page or update an existing page with the same title in a target Confluence space.

## Files

- [SKILL.md](SKILL.md)
- [Publish script](scripts/publish-to-confluence.py)

## Example

```sh
python3 skills/publish-to-confluence/scripts/publish-to-confluence.py solution-architectures/search/design.md \
  --space-key ARCH
```

Run the script from the consuming private repo root. It loads Confluence settings from that repo's `.env`; when values are missing, it prompts for them and stores them there. `--space-key` is optional after `CONFLUENCE_SPACE_KEY` has been stored.

The page title defaults to the document's first line. If the top metadata table has a `Confluence Link` row, the script extracts the page ID from that URL and updates the matching page directly.

When no page ID is found, the script prompts for either an existing Confluence link or permission to create a new child page under the overview page. The overview page title defaults to `Overview` and can be changed with `--overview-title`.

Use `--dry-run` to inspect the request without writing to Confluence.
