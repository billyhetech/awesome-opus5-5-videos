#!/usr/bin/env python3
"""Generate README.md (English) and README.zh-CN.md (Chinese) from data/videos.json.

Usage:
    python scripts/build_readme.py          # write both READMEs
    python scripts/build_readme.py --check  # exit 1 if either file is out of sync

README files are NEVER edited by hand. All content changes go through
data/videos.json (use scripts/add_entry.py to add entries).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "videos.json"
# Written by the collector (readme_assets.py): the animated mosaic at the top.
README_META = ROOT / "data" / "readme.json"

# Per category, the README shows this many highlights; the rest live on
# clawshelf.com and in data/videos.json.
HIGHLIGHTS_PER_CATEGORY = 12
LATEST_COUNT = 30

REPO_URL = "https://github.com/billyhetech/awesome-opus5-5-videos"
SUBMIT_URL = REPO_URL + "/issues/new?template=submit-video.yml"
HERO_URL = "https://github.com/billyhetech/awesome-viral-ai-videos"
CLAWSHELF_BASE = "https://clawshelf.com/ai-videos/opus-5-5"
CLAWSHELF_UTM = "?utm_source=github&utm_medium=readme&utm_campaign=awesome-opus5-5-videos"
CLAWSHELF_URL = CLAWSHELF_BASE + CLAWSHELF_UTM

# Display label per model id (this list is Opus-only, but prompt files are
# generated with the shared multi-model tooling).
MODEL_LABELS = {
    "opus-5.5": "Opus 5.5",
}

# (slug, English display name, Chinese display name) — order is the README order.
CATEGORIES = [
    ("motion", "Motion graphics", "动态图形"),
    ("explainer", "Explainers", "讲解动画"),
    ("3d-scenes", "3D scenes", "3D 场景"),
    ("games-interactive", "Games & interactive", "游戏与交互"),
    ("long-form", "Long-form", "长片"),
    ("music-videos", "Music videos", "音乐视频"),
]

TAG_LABELS = {
    "canvas": "Canvas",
    "svg": "SVG",
    "threejs": "Three.js",
    "glsl": "GLSL",
    "gsap": "GSAP",
    "css": "CSS",
    "webgl": "WebGL",
    "web-audio": "Web Audio",
    "particles": "Particles",
    "pixel-art": "Pixel art",
    "playable": "Playable",
    "ai-image": "AI image",
    "physics": "Physics",
    "webgpu": "WebGPU",
    "remotion": "Remotion",
    "hyperframes": "HyperFrames",
    "blender": "Blender",
    "elevenlabs": "ElevenLabs",
    "ffmpeg": "FFmpeg",
    "python": "Python",
}

STRINGS = {
    "en": {
        "intro": (
            "Viral videos made with **Opus 5.5** — animations, games, 3D scenes and "
            "long-form shorts rendered entirely from code (HTML, Canvas, SVG, Three.js "
            "and friends). Every entry links to the creator's original post and, where "
            "the creator shared it, the prompt behind it."
        ),
        "stats_line": (
            "**{n_prompts} prompts** in [`prompts/`](prompts/) and "
            "[`data/videos.json`](data/videos.json) · every entry links to the "
            "creator's original post · [submit a video]({submit_url})"
        ),
        "latest_update": "- Latest update ({date}): {n} videos total",
        "contents": "Contents",
        "empty_category": "_No entries yet — [submit one]({submit_url})._",
        "prompt_link": "Prompt",
        "details_link": "Details",
        "verified": "✅ verified",
        "howto_heading": "How to use a prompt",
        "howto_body": (
            "1. Open a prompt file and copy the block under **Prompt**.\n"
            "2. Paste it into Opus 5.5 (or any agent running it) and ask for the result "
            "as a single HTML file.\n"
            "3. Record the page if you want a video.\n"
            "\n"
            "Some creators shared only part of their prompt, or only described the "
            "result in their post; those files say so."
        ),
        "credits_heading": "Credits",
        "credits_body": (
            "Every video and prompt belongs to its creator, linked from each entry. "
            "If you are a creator and want an entry changed or removed, open an issue — "
            "handled within 72 hours, no questions asked. See [CREDITS.md](CREDITS.md)."
        ),
        "lang_switch": "[English](README.md) · [中文](README.zh-CN.md)",
        "hero_line": "📦 Every model in one list: [Awesome Viral AI Videos]({hero_url})",
        "mosaic_alt": "A wall of viral videos made with Opus 5.5: games, 3D scenes, explainers and motion graphics",
        "watch_all": "**[▶ Watch all {n} videos on clawshelf.com]({url})**",
        "highlights_note": "- The {k} most viewed per category are highlighted below; tap any video to watch it on clawshelf.com",
        "see_all": "[▶ See all {n} on clawshelf.com]({url})",
        "latest_heading": "Latest videos",
    },
    "zh": {
        "intro": (
            "用 **Opus 5.5**「以代码渲染视频」的爆款合集 —— 动画、游戏、3D 场景与长片短片,"
            "全部用代码实时渲染(HTML、Canvas、SVG、Three.js 等)。每个条目都链接到创作者的"
            "原始帖子,并附上作者公开的 prompt(如有)。"
        ),
        "stats_line": (
            "[`prompts/`](prompts/) 与 [`data/videos.json`](data/videos.json) 中收录 "
            "**{n_prompts} 条 prompt** · 每个条目均链接原帖并署名 · "
            "[提交视频]({submit_url})"
        ),
        "latest_update": "- 最近更新({date}):共 {n} 条",
        "contents": "目录",
        "empty_category": "_还没有收录 —— [来提交第一个]({submit_url})。_",
        "prompt_link": "提示词",
        "details_link": "详情",
        "verified": "✅ 已复跑验证",
        "howto_heading": "如何使用 prompt",
        "howto_body": (
            "1. 打开 prompt 文件,复制 **Prompt** 下方的代码块。\n"
            "2. 粘贴给 Opus 5.5(或任何运行它的 agent),要求输出为单个 HTML 文件。\n"
            "3. 需要视频的话录屏即可。\n"
            "\n"
            "部分作者只公开了部分 prompt,或只在帖子里描述了效果;这类文件会注明。"
        ),
        "credits_heading": "版权与致谢",
        "credits_body": (
            "每个视频与 prompt 的版权归创作者所有,条目均链接回原帖。如果你是创作者,"
            "希望修改或移除某个条目,开个 issue 即可 —— 72 小时内处理,无需理由。"
            "详见 [CREDITS.md](CREDITS.md)。"
        ),
        "lang_switch": "[English](README.md) · [中文](README.zh-CN.md)",
        "hero_line": "📦 全模型总集:[Awesome Viral AI Videos]({hero_url})",
        "mosaic_alt": "Opus 5.5 爆款视频墙:游戏、3D 场景、讲解动画、动态图形",
        "watch_all": "**[▶ 在 clawshelf.com 观看全部 {n} 条视频]({url})**",
        "highlights_note": "- 下方每个分类展示播放量最高的 {k} 条;点击视频即可在 clawshelf.com 观看",
        "see_all": "[▶ 在 clawshelf.com 查看全部 {n} 条]({url})",
        "latest_heading": "最新收录",
    },
}


def anchor(text):
    """GitHub-style heading anchor: lowercase, spaces -> hyphens, drop punctuation."""
    out = []
    for ch in text.lower():
        if ch == " ":
            out.append("-")
        elif ch.isalnum() or ch in "-_":
            out.append(ch)
    return "".join(out)


def fmt_views(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def tag_labels(entry):
    return " · ".join(TAG_LABELS.get(t, t) for t in entry["tech_tags"])


def has_prompt(entry):
    return bool(entry.get("prompt", "").strip())


def detail_url(entry):
    return f"{CLAWSHELF_BASE}/{entry.get('seo_slug') or entry['slug']}{CLAWSHELF_UTM}"


def preview_image(entry):
    """Animated webp, else the poster frame, else the legacy thumbnail."""
    media = entry.get("media") or {}
    if media.get("status") == "ok":
        if media.get("preview_webp_url"):
            return media["preview_webp_url"]
        if media.get("poster_url"):
            return media["poster_url"]
    return (entry.get("thumbnail") or {}).get("url")


def views(entry):
    return (entry.get("stats_snapshot") or {}).get("views", 0)


def highlight_rank(entry):
    media = entry.get("media") or {}
    return (bool(media.get("preview_webp_url")), bool(preview_image(entry)), views(entry))


def cell(entry, lang):
    s = STRINGS[lang]
    href = detail_url(entry)
    img = preview_image(entry)
    if img:
        top = (
            f'<a href="{href}"><img src="{img}" '
            f'alt="Opus 5.5 video by @{entry["author"]}" width="100%"></a>'
        )
    else:
        top = f'<a href="{href}"><b>{entry["title"]}</b></a>'

    link_label = s["prompt_link"] if has_prompt(entry) else s["details_link"]
    line2 = (
        f'<a href="{entry["post_url"]}"><b>@{entry["author"]}</b></a> · '
        f'<a href="prompts/{entry["slug"]}.md">{link_label}</a>'
    )
    if entry.get("verification", {}).get("rerun"):
        line2 += f' · {s["verified"]}'

    sub = tag_labels(entry)
    if views(entry):
        sub = (sub + " · " if sub else "") + fmt_views(views(entry)) + " views"

    return f'<td width="33%" valign="top">{top}<br>{line2}<br><sub>{sub}</sub></td>'


def section(cat_slug, name, entries, lang):
    s = STRINGS[lang]
    lines = [f"## {name}", ""]
    if not entries:
        lines.append(s["empty_category"].format(submit_url=SUBMIT_URL))
        lines.append("")
        return "\n".join(lines)
    total = len(entries)
    entries = sorted(entries, key=highlight_rank, reverse=True)[:HIGHLIGHTS_PER_CATEGORY]
    cells = [cell(v, lang) for v in entries]
    lines.append("<table>")
    for i in range(0, len(cells), 3):
        lines.append("<tr>" + "".join(cells[i : i + 3]) + "</tr>")
    lines.append("</table>")
    lines.append("")
    if total > len(entries):
        lines.append(s["see_all"].format(n=total, url=f"{CLAWSHELF_BASE}{CLAWSHELF_UTM}&category={cat_slug}"))
        lines.append("")
    return "\n".join(lines)


def latest(data, lang):
    s = STRINGS[lang]
    newest = sorted(data, key=lambda v: (v.get("added", ""), views(v)), reverse=True)[:LATEST_COUNT]
    lines = [f'## {s["latest_heading"]}', ""]
    for v in newest:
        link_label = s["prompt_link"] if has_prompt(v) else s["details_link"]
        lines.append(
            f'- [{v["title"]}]({detail_url(v)}) — [@{v["author"]}]({v["post_url"]}) · '
            f'[{link_label}](prompts/{v["slug"]}.md)'
        )
    lines.append("")
    return "\n".join(lines)


def build(lang):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    s = STRINGS[lang]
    name_idx = 1 if lang == "en" else 2

    n_prompts = sum(1 for v in data if has_prompt(v))
    by_cat = {slug: [] for slug, _, _ in CATEGORIES}
    for v in data:
        by_cat.setdefault(v["category"], []).append(v)

    meta = json.loads(README_META.read_text(encoding="utf-8")) if README_META.exists() else {}
    mosaic = meta.get("mosaic") or {}

    lines = [
        "<!-- AUTO-GENERATED by scripts/build_readme.py — edit data/videos.json instead, "
        "then run: python scripts/build_readme.py -->",
        "# Awesome Opus 5.5 Videos",
        "",
        s["lang_switch"],
        "",
    ]
    if mosaic.get("url"):
        lines += [
            f'<a href="{CLAWSHELF_URL}"><img src="{mosaic["url"]}" '
            f'alt="{s["mosaic_alt"]}" width="100%"></a>',
            "",
        ]
    lines += [
        s["intro"],
        "",
        s["watch_all"].format(n=len(data), url=CLAWSHELF_URL),
        "",
        s["hero_line"].format(hero_url=HERO_URL),
        "",
        s["stats_line"].format(n_prompts=n_prompts, submit_url=SUBMIT_URL),
        "",
    ]

    if data:
        latest_date = max(v.get("added", "") for v in data)
        lines += [
            s["latest_update"].format(date=latest_date, n=len(data)),
            s["highlights_note"].format(k=HIGHLIGHTS_PER_CATEGORY),
            "",
        ]

    lines += [f'## {s["contents"]}', ""]
    for slug, en, zh in CATEGORIES:
        name = (en, zh)[name_idx - 1]
        lines.append(f"- [{name}](#{anchor(name)}) ({len(by_cat.get(slug, []))})")
    lines.append(f'- [{s["latest_heading"]}](#{anchor(s["latest_heading"])})')
    lines.append("")

    for slug, en, zh in CATEGORIES:
        name = (en, zh)[name_idx - 1]
        lines.append(section(slug, name, by_cat.get(slug, []), lang))

    lines.append(latest(data, lang))

    lines += [
        f'## {s["howto_heading"]}',
        "",
        s["howto_body"],
        "",
        f'## {s["credits_heading"]}',
        "",
        s["credits_body"],
        "",
    ]
    return "\n".join(lines)


def main():
    check = "--check" in sys.argv
    targets = {"en": ROOT / "README.md", "zh": ROOT / "README.zh-CN.md"}
    stale = []
    for lang, path in targets.items():
        text = build(lang)
        if check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != text:
                stale.append(path.name)
        else:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.name}")
    if check:
        if stale:
            print("README out of sync: " + ", ".join(stale))
            print("Run: python scripts/build_readme.py")
            sys.exit(1)
        print("README files are in sync with data/videos.json")


if __name__ == "__main__":
    main()
