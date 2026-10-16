#!/usr/bin/env python3
"""Interactive entry point for adding a video to data/videos.json.

Usage:
    python scripts/add_entry.py

Asks for the post URL and metadata, then:
- generates the slug ({author-handle}-{last 6 digits of the status id})
- appends the entry to data/videos.json
- writes prompts/<slug>.md
Afterwards run: python scripts/validate.py && python scripts/build_readme.py

Only paste prompt text the author has publicly shared. If the author only
described the video in their post, paste that description and answer "yes"
to prompt_partial.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

from build_readme import TAG_LABELS

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "videos.json"
PROMPTS = ROOT / "prompts"

CATEGORIES = ["motion", "explainer", "3d-scenes", "games-interactive", "long-form", "music-videos"]
CATEGORY_NAMES = {
    "motion": "Motion graphics",
    "explainer": "Explainers",
    "3d-scenes": "3D scenes",
    "games-interactive": "Games & interactive",
    "long-form": "Long-form",
    "music-videos": "Music videos",
}

STATUS_RE = re.compile(r"x\.com/([^/]+)/status/(\d+)")


def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or (default or "")


def ask_choice(prompt, options):
    print(prompt)
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    while True:
        raw = input("number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("invalid, try again")


def slugify_author(author):
    s = re.sub(r"[^a-z0-9]+", "-", author.lower()).strip("-")
    return s or "unknown"


def prompt_md(v):
    tags = " · ".join(TAG_LABELS.get(t, t) for t in v["tech_tags"])
    lines = [
        f"# Opus 5.5 video by @{v['author']}",
        "",
        f"[Original post]({v['post_url']})",
        "",
        f"- **Category:** {CATEGORY_NAMES[v['category']]}",
        f"- **Built with:** {tags}",
        f"- **Author:** [@{v['author']}]({v['author_url']})",
        "",
    ]
    prompt = v.get("prompt", "").strip()
    if prompt:
        if v.get("prompt_partial"):
            lines += [
                "> The author didn't publish the full prompt. Below is what they shared publicly.",
                "",
            ]
        lines += ["## Prompt", "", "```text", prompt, "```", ""]
    else:
        lines += [
            "> The author didn't publish a prompt for this one. Watch the original post linked above.",
            "",
        ]
    return "\n".join(lines)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))

    post_url = ask("Original post URL (https://x.com/<user>/status/<id>)")
    m = STATUS_RE.search(post_url)
    if not m:
        sys.exit("could not parse author/status id from that URL")
    default_author, status_id = m.group(1), m.group(2)

    author = ask("Author handle (without @)", default_author)
    title = ask("Video title (short, English)")
    category = ask_choice("Category:", CATEGORIES)
    tags_raw = ask("Tech tags (comma separated, e.g. canvas,threejs)", "canvas")
    tech_tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    print("Paste the publicly shared prompt text, then a line containing only EOF "
          "(just EOF if none):")
    buf = []
    for line in sys.stdin:
        if line.rstrip("\n") == "EOF":
            break
        buf.append(line.rstrip("\n"))
    prompt_text = "\n".join(buf).strip()
    prompt_partial = False
    if prompt_text:
        prompt_partial = ask("Is this the FULL prompt? (yes/no)", "yes").lower() != "yes"

    slug = f"{slugify_author(author)}-{status_id[-6:]}"
    if any(v["slug"] == slug for v in data):
        sys.exit(f"slug already exists: {slug}")

    entry = {
        "slug": slug,
        "author": author,
        "author_url": f"https://x.com/{author}",
        "post_url": post_url,
        "title": title,
        "category": category,
        "tech_tags": tech_tags,
        "prompt": prompt_text,
        "prompt_partial": prompt_partial,
        "added": date.today().isoformat(),
    }
    data.append(entry)
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (PROMPTS / f"{slug}.md").write_text(prompt_md(entry), encoding="utf-8")
    print(f"added {slug}")
    print("next: python scripts/validate.py && python scripts/build_readme.py")


if __name__ == "__main__":
    main()
