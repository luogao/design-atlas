---
name: "btop Meters"
category: "terminal-tui"
year: 2021
tags: [tui, monitor, gradient, meters]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/33-btop-meters/"
palette_colors: ["#131424", "#1a1c30", "#3b3e5e", "#e8ecff", "#7a82b0", "#00e4ff", "#6de37a", "#e5e56a"]
---

# btop Meters

## 一句话

现代终端仪表盘。系统监控也能赏心悦目。

## 设计哲学

btop 代表了现代 TUI 的美学巅峰——用 Unicode 块字符构建流畅的图表和进度条，配色精致，布局现代。它证明了终端不需要'难看'，只需要更好的字体和色彩设计。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#131424` | 背景 |
| `--panel-bg` | `#1a1c30` | 背景 |
| `--panel-border` | `#3b3e5e` | 边框/线条 |
| `--ink` | `#e8ecff` | 文字/前景 |
| `--muted` | `#7a82b0` | 其他 |
| `--accent` | `#00e4ff` | 强调色 |
| `--cpu-1` | `#6de37a` | 其他 |
| `--cpu-2` | `#e5e56a` | 其他 |

## Do / Don't

- ✅ Unicode 块字符构建图表
- ✅ 精细的调色板（不要只用绿）
- ✅ 实时动态数据可视化
- ✅ 响应式布局适配终端尺寸

- ❌ 不要用 ASCII 字符画图（用 Unicode）
- ❌ 不要用太多颜色
- ❌ 不要用大段文字
- ❌ 不要忽略动画流畅度

## 适用场景

系统监控仪表盘、CLI 数据可视化、现代终端工具

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
