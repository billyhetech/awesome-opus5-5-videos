# Contributing

[English](#english) · [中文](#中文)

---

## English

Thanks for helping grow the list!

### How to submit

- Easiest: open an issue with the [submit-video template](../../issues/new?template=submit-video.yml).
- Or send a PR: run `python scripts/add_entry.py` to add the entry interactively (it updates `data/videos.json` and creates `prompts/<slug>.md`).

### Rules

- **Every entry credits the creator and links the original post.** That's the whole point of the list.
- **Prompt text: only what the creator publicly shared.** If the post only describes the video, paste that description and mark `prompt_partial: true`. Don't paste private or leaked prompts.
- `README.md` and `README.zh-CN.md` are generated from `data/videos.json` — never edit them directly. Edit `data/videos.json`, then run `python scripts/build_readme.py`.
- Before pushing: `python scripts/validate.py && python scripts/build_readme.py --check` (CI runs the same).

### Entry format

- **slug**: `{author-handle-lowercase}-{last 6 digits of the status id}`, e.g. `imjustnewatai-168580`
- **category**: one of `motion`, `explainer`, `3d-scenes`, `games-interactive`, `long-form`, `music-videos`
- **tech_tags**: from `canvas, svg, threejs, glsl, gsap, css, webgl, web-audio, particles, pixel-art, playable, ai-image, physics` (propose new ones in your PR)

---

## 中文

### 如何投稿

- 最简单:用[投稿模板](../../issues/new?template=submit-video.yml)开 issue。
- 或提 PR:运行 `python scripts/add_entry.py` 交互录入(会更新 `data/videos.json` 并生成 `prompts/<slug>.md`)。

### 规则

- **每个条目必须署名并链接原帖。** 这是这个列表的意义所在。
- **prompt 只收录作者公开发布的内容。** 帖子只有效果描述时,粘贴该描述并标记 `prompt_partial: true`。不要收录私下泄露的 prompt。
- `README.md` 和 `README.zh-CN.md` 由 `data/videos.json` 生成,**不要手改**。改 `data/videos.json` 后运行 `python scripts/build_readme.py`。
- 提交前运行 `python scripts/validate.py && python scripts/build_readme.py --check`(CI 会做同样检查)。

### 条目格式

- **slug**:`{作者名小写}-{帖子 id 后 6 位}`,如 `imjustnewatai-168580`
- **category**:`motion` / `explainer` / `3d-scenes` / `games-interactive` / `long-form` / `music-videos` 六选一
- **tech_tags**:从 `canvas, svg, threejs, glsl, gsap, css, webgl, web-audio, particles, pixel-art, playable, ai-image, physics` 中选(新标签请在 PR 中说明)
