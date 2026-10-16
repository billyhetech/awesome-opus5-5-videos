# Opus 5.5 video by @okazaky

[Original post](https://x.com/okazaky/status/2107826563786084783)

- **Category:** 3D scenes
- **Built with:** Canvas
- **Author:** [@okazaky](https://x.com/okazaky)

## Prompt

```text
Create a 50-second vertical music video using programmatic rendering (Three.js) instead of native video AI.
1. Generate song with Suno. Extract lyrics from embedded metadata.
2. Separate stems with Demucs (vocals, drums, bass, other).
3. Transcribe vocals with mlx_whisper. Align with official lyrics to create script where '1 lyric line = 1 scene'.
4. Write storyboard: define 'What to show in 3D', 'Camera', 'Main word' for each lyric line.
5. Have 4 parallel Opus sub-agents write scene programs.
6. Export 16-frame contact sheet for visual verification.
7. Render headless Chrome at 1080x1920, 60fps.
8. Normalize volume to -14 LUFS.
Style: Engraving-like lines, colors limited to Black, Bone, Orange.
```
