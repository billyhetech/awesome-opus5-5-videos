# Opus 5.5 video by @Mochi_AGI

[Original post](https://x.com/Mochi_AGI/status/2104757097850421448)

- **Category:** 3D scenes
- **Built with:** Canvas
- **Author:** [@Mochi_AGI](https://x.com/Mochi_AGI)

## Prompt

```text
今回は ElevenLabs v4 のお試しで、終電のホームの短いホラー

声は v4 で2人の掛け合いを1回で生成
画は静止画9枚に奥行きつけて動かしてるだけ、動画生成AIはなし

最初の声がぜんぜん怖くなかったので
→ 台詞はそのまま、途中に [whispering] とか [laughs softly] とか英語で演技の指示
→ stability 0.5 → 0.3
→ 女の声は3人聞き比べて、息の多い低い声に
女は最後まで小声、顔は出さずに背中と唇だけ

字幕は明朝体、女は縦書きで男は横書き
女の字はささやく速さで1字ずつ、男の字は叫ぶほど震える仕様

使用ツール
・Claude Code の Opus 5.5　企画、演出、動きと字幕のコード、仕上がりのチェック
・ElevenLabs v4　2人の声の掛け合いと、環境音
・Codex の画像生成　静止画9枚
・Three.js　静止画に奥行きをつけてカメラを動かす
・しっぽり明朝 B1　字幕の書体
・Playwright　ブラウザで1コマずつ書き出し
・ffmpeg　動画の書き出し
```
