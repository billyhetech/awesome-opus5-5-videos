#!/usr/bin/env python3
"""Validate data/videos.json: schema and cross-checks.

Rules enforced:
- every entry has the required fields with the right types
- slug is unique, matches {author-slug}-{6 digits}, and has prompts/<slug>.md
- seo_slug (the clawshelf.com URL) is unique, 2-10 lowercase ascii words, <= 60 chars
- category and tech_tags come from the known vocabularies
- if prompt text is present, prompt_partial flags whether it's the full prompt
- if a thumbnail is present, the file must exist

Exit code 0 = valid, 1 = any errors (all printed).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "videos.json"
PROMPTS = ROOT / "prompts"

MODELS = {"opus-5.5"}
CATEGORIES = {"motion", "explainer", "3d-scenes", "games-interactive", "long-form", "music-videos"}
TAGS = {
    "canvas", "svg", "threejs", "glsl", "gsap", "css", "webgl", "web-audio",
    "particles", "pixel-art", "playable", "ai-image", "physics",
    "webgpu", "remotion", "hyperframes", "blender", "elevenlabs", "ffmpeg", "python",
}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-\d{6}$")
# URL slug on clawshelf.com: 2-10 lowercase ascii words, <= 60 chars, unique, never changed once published
SEO_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){1,9}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https://")


def err(errors, slug, msg):
    errors.append(f"[{slug}] {msg}")


def check_entry(v, errors, seen_slugs, seen_seo_slugs=None):
    slug = v.get("slug", "<missing slug>")
    seen_seo_slugs = set() if seen_seo_slugs is None else seen_seo_slugs

    # --- SEO slug (public URL) ---
    seo = v.get("seo_slug")
    if not isinstance(seo, str) or not SEO_SLUG_RE.match(seo) or len(seo) > 60:
        err(errors, slug, "seo_slug must be 2-10 lowercase ascii words joined by '-', max 60 chars")
    elif seo in seen_seo_slugs:
        err(errors, slug, f"duplicate seo_slug: {seo}")
    else:
        seen_seo_slugs.add(seo)

    # --- required scalar fields ---
    for field in ("slug", "model", "author", "author_url", "post_url", "title", "category", "added"):
        if not isinstance(v.get(field), str) or not v[field].strip():
            err(errors, slug, f"missing or empty required field: {field}")

    if v.get("model") not in MODELS:
        err(errors, slug, f"unknown model: {v.get('model')} (this list covers Opus 5.5 only; other models go to the multi-model list)")

    if slug in seen_slugs:
        err(errors, slug, "duplicate slug")
    seen_slugs.add(slug)

    if not SLUG_RE.match(slug):
        err(errors, slug, "slug must look like author-name-123456 (lowercase, 6 trailing digits)")

    for field in ("author_url", "post_url"):
        if isinstance(v.get(field), str) and not URL_RE.match(v[field]):
            err(errors, slug, f"{field} must be an https URL")

    if not DATE_RE.match(v.get("added", "")):
        err(errors, slug, "added must be YYYY-MM-DD")

    if v.get("category") not in CATEGORIES:
        err(errors, slug, f"unknown category: {v.get('category')}")

    # --- tech tags ---
    tags = v.get("tech_tags")
    if not isinstance(tags, list) or not tags:
        err(errors, slug, "tech_tags must be a non-empty list")
    else:
        for t in tags:
            if t not in TAGS:
                err(errors, slug, f"unknown tech tag: {t} (add it to TAGS here and TAG_LABELS in build_readme.py)")

    if not isinstance(v.get("prompt_partial"), bool):
        err(errors, slug, "prompt_partial must be a boolean")

    # --- prompt consistency ---
    if not v.get("prompt", "").strip() and v.get("prompt_partial") is False:
        err(errors, slug, "prompt is empty but prompt_partial is false")

    # --- thumbnail ---
    thumb = v.get("thumbnail")
    if thumb is not None:
        if not isinstance(thumb, dict) or not thumb.get("url"):
            err(errors, slug, "thumbnail needs a url")
        elif not (ROOT / thumb["url"]).is_file():
            err(errors, slug, f"thumbnail file not found: {thumb['url']}")

    # --- optional blocks ---
    stats = v.get("stats_snapshot")
    if stats is not None:
        if not isinstance(stats.get("views", 0), int) or not DATE_RE.match(str(stats.get("captured_at", ""))):
            err(errors, slug, "stats_snapshot needs integer views and captured_at YYYY-MM-DD")

    ver = v.get("verification")
    if ver is not None and ver.get("rerun"):
        for field in ("rerun_at", "model", "time_minutes", "success"):
            if field not in ver:
                err(errors, slug, f"verification.rerun is true but {field} is missing")

    # --- prompt file must exist ---
    if not (PROMPTS / f"{slug}.md").is_file():
        err(errors, slug, f"missing prompt file: prompts/{slug}.md")


def main():
    errors = []
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"data/videos.json is not valid JSON: {e}")
        sys.exit(1)
    if not isinstance(data, list):
        print("data/videos.json must be a JSON array")
        sys.exit(1)

    seen = set()
    seen_seo = set()
    for v in data:
        if isinstance(v, dict):
            check_entry(v, errors, seen, seen_seo)
        else:
            errors.append("every entry must be an object")

    if errors:
        print(f"{len(errors)} problem(s) found:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"OK — {len(data)} entries valid")


if __name__ == "__main__":
    main()
