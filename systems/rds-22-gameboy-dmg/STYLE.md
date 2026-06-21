---
name: "Game Boy DMG"
category: "gaming"
year: 1989
tags: [gameboy, green, lcd, 4-shade]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/22-gameboy-dmg/"
palette_colors: ["#b8b0a4", "#8a8478", "#6a6458", "#2a3028", "#0f380f", "#306230", "#8bac0f", "#9bbc0f"]
---

# Game Boy DMG

## 一句话

四色绿。口袋妖怪的故乡，限制即创意。

## 设计哲学

Game Boy DMG（Dot Matrix Game）只有 4 种绿色（从最浅到最深）。在这么极端的限制下，设计师创造了无数经典游戏。美学核心是：用 4 个明度阶表达一切——光影、材质、深度、情绪。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--shell` | `#b8b0a4` | 其他 |
| `--shell-dark` | `#8a8478` | 其他 |
| `--shell-shadow` | `#6a6458` | 阴影 |
| `--screen-bezel` | `#2a3028` | 其他 |
| `--lcd-0` | `#0f380f` | 其他 |
| `--lcd-1` | `#306230` | 其他 |
| `--lcd-2` | `#8bac0f` | 其他 |
| `--lcd-3` | `#9bbc0f` | 其他 |

## Do / Don't

- ✅ 严格使用 4 色绿阶（#0f380f #306230 #8bac0f #9bbc0f）
- ✅ dithering 图案创造灰度过渡
- ✅ 像素精灵图
- ✅ 紧凑的 tile-based 布局

- ❌ 不要用超过 4 种颜色
- ❌ 不要用平滑渐变
- ❌ 不要用真彩图像
- ❌ 不要用抗锯齿

## 适用场景

像素游戏、极简设计、限制色板创意

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
