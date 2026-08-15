#!/usr/bin/env python3
"""Mirror thefarmerwasreplaced.wiki.gg into docs/wiki/ as Markdown.

Pulls raw wikitext through the MediaWiki API (never scrapes rendered HTML) and
converts it with pandoc. Re-runnable: it overwrites docs/wiki/ in place, so the
git diff after a run is exactly what changed upstream.

Usage:  python3 tools/fetch_wiki.py [--limit N]

Requires: pandoc on PATH (~/.local/bin/pandoc is fine).
Content is CC BY-SA; this mirror is for personal/offline reference.
"""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://thefarmerwasreplaced.wiki.gg/api.php"
UA = "tfwr-automation/1.0 (personal offline docs mirror)"
OUT = Path(__file__).resolve().parent.parent / "docs" / "wiki"

# Pages that are wiki plumbing rather than game reference.
SKIP_EXACT = {"The Farmer Was Replaced Wiki", "Steam"}


def api(**params):
    params.setdefault("format", "json")
    params.setdefault("formatversion", "2")
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def all_titles():
    titles, cont = [], {}
    while True:
        data = api(action="query", list="allpages", aplimit="500", **cont)
        titles += [p["title"] for p in data["query"]["allpages"]]
        if "continue" not in data:
            return titles
        cont = data["continue"]


def fetch_batch(titles):
    """Return {title: wikitext} for up to 50 titles."""
    data = api(
        action="query",
        prop="revisions",
        rvprop="content",
        rvslots="main",
        titles="|".join(titles),
    )
    out = {}
    for page in data["query"]["pages"]:
        if "missing" in page or not page.get("revisions"):
            continue
        out[page["title"]] = page["revisions"][0]["slots"]["main"]["content"]
    return out


def slug(title):
    return re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-")


def pandoc(src, frm, to):
    p = subprocess.run(
        ["pandoc", "-f", frm, "-t", to, "--wrap=none"],
        input=src, capture_output=True, text=True,
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    return p.stdout


def flatten_cells(html):
    """Make wiki tables expressible as GFM pipe tables.

    Pandoc's gfm writer dumps a whole table as raw HTML if any single cell holds
    block content — a wrapping <p> or a <br />. The reference tables (operation
    costs, item costs, unlocks) are the pages we consult most, so it is worth
    flattening cells to inline text to keep them as compact pipe tables.
    """
    html = re.sub(r"<br\s*/?>", " ", html)
    html = re.sub(
        r"<(t[dh])(?:\s[^>]*)?>\s*(?:<p>)?(.*?)(?:</p>)?\s*</\1>",
        lambda m: f"<{m.group(1)}>{m.group(2).strip()}</{m.group(1)}>",
        html, flags=re.S,
    )
    return html


def to_markdown(wikitext):
    return pandoc(flatten_cells(pandoc(wikitext, "mediawiki", "html")), "html", "gfm")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="fetch only N pages (smoke test)")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*.md"):
        stale.unlink()

    titles = [t for t in all_titles() if t not in SKIP_EXACT]
    if args.limit:
        titles = titles[: args.limit]

    pages, redirects = {}, {}
    for i in range(0, len(titles), 50):
        batch = fetch_batch(titles[i : i + 50])
        for title, text in batch.items():
            m = re.match(r"\s*#REDIRECT\s*\[\[([^\]]+)\]\]", text, re.I)
            if m:
                redirects[title] = m.group(1).strip()
            else:
                pages[title] = text
        time.sleep(0.3)  # be polite to wiki.gg

    written = []
    for title in sorted(pages):
        md = to_markdown(pages[title])
        aliases = sorted(a for a, tgt in redirects.items() if tgt == title)
        header = [
            f"# {title}",
            "",
            f"> Mirrored from <https://thefarmerwasreplaced.wiki.gg/wiki/{urllib.parse.quote(title.replace(' ', '_'))}>",
            "> — CC BY-SA. Regenerate with `python3 tools/fetch_wiki.py`.",
        ]
        if aliases:
            header.append(f"> Also known as: {', '.join(aliases)}.")
        header += ["", md.strip(), ""]
        path = OUT / f"{slug(title)}.md"
        path.write_text("\n".join(header))
        written.append((title, path.name))

    index = [
        "# TFWR Wiki Mirror",
        "",
        f"{len(written)} pages mirrored from thefarmerwasreplaced.wiki.gg "
        f"({len(redirects)} redirects folded into their targets).",
        "",
        "The wiki is the *conceptual* reference. For authoritative function signatures",
        "matching this save's unlock state and game version, use",
        "[`docs/api/__builtins__.py`](../api/__builtins__.py).",
        "",
        "| Page | File |",
        "| --- | --- |",
    ]
    index += [f"| {t} | [{f}]({f}) |" for t, f in written]
    (OUT / "index.md").write_text("\n".join(index) + "\n")

    print(f"wrote {len(written)} pages + index.md to {OUT}")
    if redirects:
        print(f"folded {len(redirects)} redirects")


if __name__ == "__main__":
    sys.exit(main())
