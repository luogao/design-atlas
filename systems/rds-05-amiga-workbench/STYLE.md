---
name: "Amiga Workbench"
category: "os-interfaces"
year: 1985
tags: [amiga, retro, orange, blue]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/05-amiga-workbench/"
palette_colors: ["#0055aa", "#ff8800", "#ffffff", "#000000", "#a0a0a0"]
---

# Amiga Workbench

## 一句话

四个色块就能构建一个操作系统。Amiga 的限制即美学。

## 设计哲学

Workbench 在极度受限的硬件条件下（4 色到 4096 色）创造了独特的视觉语言。标志性的蓝橙配色、像素图标、屏幕拖拽机制——每个像素都在和硬件限制搏斗。它的美学来自对限制的拥抱而非对抗。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--wb-blue` | `#0055aa` | 其他 |
| `--wb-orange` | `#ff8800` | 其他 |
| `--wb-white` | `#ffffff` | 其他 |
| `--wb-black` | `#000000` | 其他 |
| `--wb-gray` | `#a0a0a0` | 其他 |
| `--ink` | `#000` | 文字/前景 |
| `--font` | `"Topaz", "Courier New", "Consolas", monospace` | 文字/前景 |

## Do / Don't

- ✅ 限制调色板（蓝/橙/白/黑经典四色）
- ✅ 像素艺术图标
- ✅ 等宽字体 + 紧凑布局
- ✅ 利用 dithering 扩展色彩

- ❌ 不要用平滑渐变
- ❌ 不要用太多颜色
- ❌ 不要用抗锯齿
- ❌ 不要用圆角

## 适用场景

极客工具、复古计算致敬、限制色板挑战

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
