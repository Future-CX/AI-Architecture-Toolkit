#!/usr/bin/env python3
"""Create or update a Confluence page from markdown or HTML."""

from __future__ import annotations

import argparse
import base64
import getpass
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_PREFIX = "/rest/api"
CONFLUENCE_ENV_KEYS = (
    "CONFLUENCE_BASE_URL",
    "CONFLUENCE_EMAIL",
    "CONFLUENCE_API_TOKEN",
    "CONFLUENCE_SPACE_KEY",
)


class ConfluenceError(RuntimeError):
    """Raised when Confluence returns an error response."""


def parse_env_file(env_file: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_file.exists():
        return values
    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def shell_quote_env_value(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_env_values(env_file: Path, updates: dict[str, str]) -> None:
    lines = env_file.read_text(encoding="utf-8").splitlines() if env_file.exists() else []
    seen: set[str] = set()
    output: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            output.append(line)
            continue
        key = stripped.split("=", 1)[0].strip()
        if key in updates:
            output.append(f"{key}={shell_quote_env_value(updates[key])}")
            seen.add(key)
        else:
            output.append(line)

    if output and output[-1] != "":
        output.append("")
    for key in CONFLUENCE_ENV_KEYS:
        if key in updates and key not in seen:
            output.append(f"{key}={shell_quote_env_value(updates[key])}")

    env_file.write_text("\n".join(output) + "\n", encoding="utf-8")
    env_file.chmod(0o600)


def prompt_for_missing_config(config: dict[str, str], env_file: Path) -> dict[str, str]:
    prompts = {
        "CONFLUENCE_BASE_URL": "Confluence base URL, for example https://example.atlassian.net/wiki",
        "CONFLUENCE_EMAIL": "Confluence email",
        "CONFLUENCE_API_TOKEN": "Confluence API token",
        "CONFLUENCE_SPACE_KEY": "Confluence space key",
    }
    updates: dict[str, str] = {}
    for key in CONFLUENCE_ENV_KEYS:
        if config.get(key):
            continue
        if not sys.stdin.isatty():
            raise SystemExit(
                f"Missing {key}. Run interactively once to store it in {env_file}, "
                f"or set it as an environment variable."
            )
        if key == "CONFLUENCE_API_TOKEN":
            value = getpass.getpass(f"{prompts[key]}: ").strip()
        else:
            value = input(f"{prompts[key]}: ").strip()
        if not value:
            raise SystemExit(f"{key} is required.")
        config[key] = value
        updates[key] = value
    if updates:
        write_env_values(env_file, updates)
        print(f"Stored Confluence configuration in {env_file}", file=sys.stderr)
    return config


def load_confluence_config(env_file: Path, overrides: dict[str, str] | None = None) -> dict[str, str]:
    file_config = parse_env_file(env_file)
    config = dict(file_config)
    for key in CONFLUENCE_ENV_KEYS:
        if os.environ.get(key):
            config[key] = os.environ[key].strip()
    if overrides:
        missing_file_values: dict[str, str] = {}
        for key, value in overrides.items():
            if value:
                config[key] = value.strip()
                if not file_config.get(key):
                    missing_file_values[key] = value.strip()
        if missing_file_values:
            write_env_values(env_file, missing_file_values)
            print(f"Stored Confluence configuration in {env_file}", file=sys.stderr)
    return prompt_for_missing_config(config, env_file)


def build_auth_header(email: str, api_token: str) -> str:
    token = base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def request_json(
    base_url: str,
    auth_header: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}{path}"
    data = None
    headers = {
        "Authorization": auth_header,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ConfluenceError(f"{method} {url} failed with HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ConfluenceError(f"{method} {url} failed: {exc.reason}") from exc


def find_page(
    base_url: str,
    auth_header: str,
    space_key: str,
    title: str,
) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(
        {
            "spaceKey": space_key,
            "title": title,
            "expand": "version,body.storage,_links",
            "limit": "1",
        }
    )
    response = request_json(base_url, auth_header, "GET", f"{API_PREFIX}/content?{query}")
    results = response.get("results", [])
    return results[0] if results else None


def get_page(
    base_url: str,
    auth_header: str,
    page_id: str,
) -> dict[str, Any]:
    query = urllib.parse.urlencode({"expand": "version,body.storage,_links"})
    return request_json(base_url, auth_header, "GET", f"{API_PREFIX}/content/{page_id}?{query}")


def create_page(
    base_url: str,
    auth_header: str,
    space_key: str,
    title: str,
    storage_html: str,
    parent_id: str | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {"storage": {"value": storage_html, "representation": "storage"}},
    }
    if parent_id:
        payload["ancestors"] = [{"id": parent_id}]
    return request_json(base_url, auth_header, "POST", f"{API_PREFIX}/content", payload)


def update_page(
    base_url: str,
    auth_header: str,
    page: dict[str, Any],
    title: str,
    storage_html: str,
) -> dict[str, Any]:
    page_id = page["id"]
    current_version = int(page["version"]["number"])
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {"number": current_version + 1},
        "body": {"storage": {"value": storage_html, "representation": "storage"}},
    }
    return request_json(base_url, auth_header, "PUT", f"{API_PREFIX}/content/{page_id}", payload)


def markdown_to_html(markdown_text: str) -> str:
    try:
        import markdown  # type: ignore

        return markdown.markdown(
            markdown_text,
            extensions=["extra", "sane_lists", "tables", "toc"],
            output_format="html5",
        )
    except ImportError:
        return simple_markdown_to_html(markdown_text)


def prepare_markdown_for_publish(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    first_content_index = next((index for index, line in enumerate(lines) if line.strip()), None)
    if first_content_index is None:
        return markdown_text

    output = lines[:first_content_index] + lines[first_content_index + 1 :]
    metadata_start = next((index for index, line in enumerate(output) if line.strip()), None)
    if metadata_start is None:
        return "\n".join(output).strip() + "\n"

    metadata_end = top_metadata_table_end(output, metadata_start)
    if metadata_end is not None:
        output = output[:metadata_start] + output[metadata_end:]

    return "\n".join(output).strip() + "\n"


def top_metadata_table_end(lines: list[str], start: int) -> int | None:
    if start + 1 >= len(lines):
        return None
    header = table_cells(lines[start])
    separator = table_cells(lines[start + 1])
    if [cell.lower() for cell in header[:2]] != ["field", "value"]:
        return None
    if len(separator) < 2 or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator[:2]):
        return None

    end = start + 2
    while end < len(lines) and lines[end].strip().startswith("|"):
        end += 1
    while end < len(lines) and not lines[end].strip():
        end += 1
    return end


def table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def simple_markdown_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    in_ul = False
    in_ol = False
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            output.append("</ul>")
            in_ul = False
        if in_ol:
            output.append("</ol>")
            in_ol = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                flush_paragraph()
                close_lists()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not stripped:
            flush_paragraph()
            close_lists()
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_lists()
            level = len(heading.group(1))
            output.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        if unordered:
            flush_paragraph()
            if in_ol:
                output.append("</ol>")
                in_ol = False
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            output.append(f"<li>{inline_markdown(unordered.group(1))}</li>")
            continue

        ordered = re.match(r"^\d+[.]\s+(.+)$", stripped)
        if ordered:
            flush_paragraph()
            if in_ul:
                output.append("</ul>")
                in_ul = False
            if not in_ol:
                output.append("<ol>")
                in_ol = True
            output.append(f"<li>{inline_markdown(ordered.group(1))}</li>")
            continue

        paragraph.append(stripped)

    flush_paragraph()
    close_lists()
    if in_code:
        output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(output)


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def read_content(raw: str, path: Path, content_format: str) -> str:
    if content_format == "html":
        return raw
    if content_format == "markdown":
        return markdown_to_html(prepare_markdown_for_publish(raw))
    if path.suffix.lower() in {".html", ".htm"}:
        return raw
    return markdown_to_html(prepare_markdown_for_publish(raw))


def extract_title(raw: str) -> str | None:
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        heading = re.match(r"^#{1,6}\s+(.+)$", stripped)
        title = heading.group(1) if heading else stripped
        return re.sub(r"\s+", " ", title).strip()
    return None


def extract_confluence_link(raw: str) -> str | None:
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        field = re.sub(r"\s+", " ", cells[0]).strip().lower()
        if field != "confluence link":
            continue
        value = cells[1].strip()
        if not value or value.startswith("{{"):
            return None
        markdown_link = re.search(r"\[[^\]]+\]\(([^)]+)\)", value)
        return markdown_link.group(1).strip() if markdown_link else value
    return None


def extract_page_id(confluence_link: str | None) -> str | None:
    if not confluence_link:
        return None
    pages_match = re.search(r"/pages/(\d+)(?:/|$)", confluence_link)
    if pages_match:
        return pages_match.group(1)
    parsed = urllib.parse.urlparse(confluence_link)
    query = urllib.parse.parse_qs(parsed.query)
    page_ids = query.get("pageId")
    if page_ids and page_ids[0].isdigit():
        return page_ids[0]
    return None


def update_confluence_link(raw: str, confluence_link: str) -> str:
    lines = raw.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        field = re.sub(r"\s+", " ", cells[0]).strip().lower()
        if field == "confluence link":
            lines[index] = f"| Confluence Link | {confluence_link} |"
            return "\n".join(lines) + "\n"

    insert_at = 1 if lines else 0
    metadata_table = [
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Confluence Link | {confluence_link} |",
    ]
    return "\n".join(lines[:insert_at] + metadata_table + lines[insert_at:]) + "\n"


def prompt_for_missing_page_action() -> str:
    if not sys.stdin.isatty():
        raise SystemExit(
            "No Confluence page ID found. Run interactively and choose whether to provide "
            "a Confluence Link or create the page under the Overview page."
        )

    print("No Confluence page ID was found in the document's Confluence Link row.")
    print("Choose how to continue:")
    print("1. Provide an existing Confluence Link. The source markdown will be updated first, then published.")
    print("2. Create a new Confluence page under the Overview page. The returned link will be written to the source markdown.")
    while True:
        choice = input("Choice [1/2]: ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Enter 1 or 2.")


def prompt_for_confluence_link() -> str:
    while True:
        link = input("Confluence Link: ").strip()
        if extract_page_id(link):
            return link
        print("Enter a Confluence page URL containing a page ID.")


def page_url(base_url: str, response: dict[str, Any]) -> str:
    links = response.get("_links", {})
    webui = links.get("webui")
    if webui:
        return f"{base_url.rstrip('/')}{webui}"
    return f"{base_url.rstrip()}/pages/viewpage.action?pageId={response.get('id')}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Markdown or HTML file to publish.")
    parser.add_argument(
        "--space-key",
        help="Confluence space key. Overrides CONFLUENCE_SPACE_KEY from the environment or .env file.",
    )
    parser.add_argument("--title", help="Confluence page title. Defaults to the source document's first line.")
    parser.add_argument("--parent-id", help="Optional parent page ID for newly created pages.")
    parser.add_argument(
        "--overview-title",
        default="Overview",
        help="Confluence overview page title used when creating a new child page. Defaults to Overview.",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path.cwd() / ".env",
        help="Environment file for Confluence credentials. Defaults to .env in the current working directory.",
    )
    parser.add_argument(
        "--content-format",
        choices=["auto", "markdown", "html"],
        default="auto",
        help="How to interpret the source file. Defaults to auto.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print intended action without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.source.exists():
        raise SystemExit(f"Source file does not exist: {args.source}")

    raw = args.source.read_text(encoding="utf-8")
    title = args.title or extract_title(raw)
    if not title:
        raise SystemExit("Missing page title. Add a first line to the document or pass --title.")
    confluence_link = extract_confluence_link(raw)
    page_id = extract_page_id(confluence_link)
    missing_page_action: str | None = None
    if not page_id:
        missing_page_action = prompt_for_missing_page_action()
        if missing_page_action == "1":
            confluence_link = prompt_for_confluence_link()
            page_id = extract_page_id(confluence_link)
            if not page_id:
                raise SystemExit("Could not extract a page ID from the provided Confluence Link.")

    storage_html = read_content(raw, args.source, args.content_format)
    config = load_confluence_config(args.env_file, {"CONFLUENCE_SPACE_KEY": args.space_key})
    space_key = config["CONFLUENCE_SPACE_KEY"]

    if args.dry_run:
        print(
            json.dumps(
                {
                    "action": "create-or-update",
                    "page_id": page_id,
                    "space_key": space_key,
                    "title": title,
                    "confluence_link": confluence_link,
                    "parent_id": args.parent_id,
                    "overview_title": args.overview_title,
                    "missing_page_action": missing_page_action,
                    "body_bytes": len(storage_html.encode("utf-8")),
                },
                indent=2,
            )
        )
        return 0

    base_url = config["CONFLUENCE_BASE_URL"]
    email = config["CONFLUENCE_EMAIL"]
    api_token = config["CONFLUENCE_API_TOKEN"]
    auth_header = build_auth_header(email, api_token)

    try:
        if page_id:
            if missing_page_action == "1":
                raw = update_confluence_link(raw, confluence_link or "")
                args.source.write_text(raw, encoding="utf-8")
                storage_html = read_content(raw, args.source, args.content_format)
            page = get_page(base_url, auth_header, page_id)
            response = update_page(base_url, auth_header, page, title, storage_html)
            if missing_page_action == "1":
                print(f"Updated source markdown with Confluence Link: {args.source}")
            print(f"Updated Confluence page {response.get('id')}: {page_url(base_url, response)}")
        else:
            overview_page = find_page(base_url, auth_header, space_key, args.overview_title)
            if not overview_page:
                raise SystemExit(
                    f"Could not find overview page '{args.overview_title}' in Confluence space {space_key}."
                )
            created = create_page(base_url, auth_header, space_key, title, storage_html, overview_page["id"])
            confluence_link = page_url(base_url, created)
            raw = update_confluence_link(raw, confluence_link)
            args.source.write_text(raw, encoding="utf-8")
            storage_html = read_content(raw, args.source, args.content_format)
            page = get_page(base_url, auth_header, created["id"])
            response = update_page(base_url, auth_header, page, title, storage_html)
            print(f"Updated source markdown with Confluence Link: {args.source}")
            print(f"Created Confluence page {response.get('id')}: {page_url(base_url, response)}")
    except ConfluenceError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
