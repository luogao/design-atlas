---
name: "DOS CGA"
category: "terminal-tui"
year: 1981
tags: [dos, cyan, magenta, 4-color]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/10-dos-cga/"
palette_colors: ["#000000", "#0000aa", "#5555ff", "#00aa00", "#00aaaa", "#55ffff", "#aa0000", "#aa00aa"]
---

# DOS CGA

## 一句话

4 色的地狱。青色、品红、白色、黑色——这就是你能用的全部。

## 设计哲学

CGA（Color Graphics Adapter）是 IBM PC 的第一个彩色标准，只有 4 种颜色（青、品红、白、黑）。在这种极端限制下诞生了独特的视觉美学——高对比度、像素感极强、没有过渡色。每个像素都是不可妥协的。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--c-black` | `#000000` | 其他 |
| `--c-blue` | `#0000aa` | 其他 |
| `--c-blue-bright` | `#5555ff` | 其他 |
| `--c-green` | `#00aa00` | 其他 |
| `--c-cyan` | `#00aaaa` | 其他 |
| `--c-cyan-bright` | `#55ffff` | 其他 |
| `--c-red` | `#aa0000` | 其他 |
| `--c-magenta` | `#aa00aa` | 其他 |

## Do / Don't

- ✅ 严格遵守 4 色调色板
- ✅ 大像素块组成的图形
- ✅ 等宽字体 + 高对比
- ✅ 利用 dithering 创造伪渐变

- ❌ 不要用超过 4 种颜色
- ❌ 不要用平滑曲线
- ❌ 不要用抗锯齿
- ❌ 不要追求'精致'

## 适用场景

极限制色挑战、复古游戏、像素艺术

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
