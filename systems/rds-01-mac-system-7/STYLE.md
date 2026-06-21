---
name: "Mac System 7"
category: "os-interfaces"
year: 1991
tags: [mac, monochrome, bevel, classic]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/01-mac-system-7/"
palette_colors: ["#a8a8a8", "#888888", "#ffffff", "#000000", "#dddddd"]
---

# Mac System 7

## 一句话

黑白灰的企鹅蛋时代。每个像素都经过手工调校的 bevel 和 dither。

## 设计哲学

System 7 是 pre-TrueColor 时代的巅峰——在只有灰度的世界里，设计师用 dither 图案、像素级 bevel 边框和精心选择的灰阶层次创造深度感。一切都是手工的、精确的、克制的。UI 元素靠 1px 高光和 1px 阴影暗示立体感，而非依赖色彩。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#a8a8a8` | 背景 |
| `--desktop` | `#888` | 背景 |
| `--paper` | `#ffffff` | 背景 |
| `--ink` | `#000000` | 文字/前景 |
| `--chrome` | `#dddddd` | 其他 |
| `--shadow` | `#000` | 阴影 |
| `--font-sys` | `"Chicago", "Charcoal", "Geneva", Tahoma, sans-serif` | 文字/前景 |
| `--font-body` | `"Geneva", "Helvetica", sans-serif` | 文字/前景 |

## Do / Don't

- ✅ 1px 级别的 bevel 边框（上左亮、下右暗）
- ✅ Chicago/Charcoal 位图字体
- ✅ 灰阶 dither 图案表达纹理
- ✅ 黑白条纹标题栏

- ❌ 不要用 TrueColor（32bit 色深）
- ❌ 不要用平滑抗锯齿
- ❌ 不要用圆角（所有元素都是直角）
- ❌ 不要用渐变（只能用 dither 模拟）

## 适用场景

复古 Mac 应用、极简工具类 UI、pixel-perfect 设计致敬

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles/7/
