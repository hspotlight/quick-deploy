#!/usr/bin/env python3
"""Regenerates index.html by listing every other *.html file in the repo root."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = TITLE_RE.search(text)
    if match:
        title = re.sub(r"\s+", " ", match.group(1)).strip()
        if title:
            return html.unescape(title)
    return path.stem.replace("-", " ").replace("_", " ").title()


def collect_pages():
    pages = [
        p for p in ROOT.glob("*.html")
        if p.name != "index.html"
    ]
    return sorted(pages, key=lambda p: page_title(p).lower())


def render(pages) -> str:
    items = "\n".join(
        f'      <li><a href="{html.escape(p.name)}">{html.escape(page_title(p))}</a></li>'
        for p in pages
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page Index</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 640px;
    margin: 4rem auto;
    padding: 0 1.5rem;
    color: #1a1a1a;
    background: #fafafa;
  }}
  h1 {{ font-size: 1.5rem; margin-bottom: 1.5rem; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: 0.5rem 0; }}
  a {{
    display: block;
    padding: 0.9rem 1.1rem;
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    text-decoration: none;
    color: #1a1a1a;
    transition: border-color 0.15s ease;
  }}
  a:hover {{ border-color: #999; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #111; color: #eee; }}
    a {{ background: #1b1b1b; border-color: #333; color: #eee; }}
    a:hover {{ border-color: #666; }}
  }}
</style>
</head>
<body>
  <h1>Pages</h1>
  <ul>
{items}
  </ul>
</body>
</html>
"""


def main():
    pages = collect_pages()
    (ROOT / "index.html").write_text(render(pages), encoding="utf-8")
    print(f"Generated index.html with {len(pages)} page(s).")


if __name__ == "__main__":
    main()
