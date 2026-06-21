---
name: "Midnight Commander"
category: "terminal-tui"
year: 1994
tags: [tui, blue, filemanager, ncurses]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/31-midnight-commander/"
palette_colors: ["#0000aa", "#aaaaaa", "#ffffff", "#ffff55", "#55ffff", "#00aaaa", "#000000", "#55ff55"]
---

# Midnight Commander

## 一句话

双面板文件管理。键盘飞人的效率美学。

## 设计哲学

Midnight Commander 是 Norton Commander 的 Unix 传承者——双面板设计让用户左右对比、拖拽操作。视觉上它极度克制：蓝色边框、灰色背景、热键高亮。设计目标是零距离的手指记忆。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#0000aa` | 背景 |
| `--panel` | `#0000aa` | 卡片/面板 |
| `--panel-border` | `#aaaaaa` | 边框/线条 |
| `--text` | `#aaaaaa` | 文字/前景 |
| `--text-hi` | `#ffffff` | 文字/前景 |
| `--yellow` | `#ffff55` | 其他 |
| `--cyan` | `#55ffff` | 其他 |
| `--selected-bg` | `#00aaaa` | 背景 |

## Do / Don't

- ✅ 双面板对称布局
- ✅ 蓝色边框 + 灰色背景
- ✅ 热键高亮（黄色）+ 状态栏
- ✅ 全键盘可操作

- ❌ 不要用鼠标为主的交互
- ❌ 不要用图形图标
- ❌ 不要用渐变
- ❌ 不要打破双面板对称

## 适用场景

文件管理器、TUI 应用、键盘驱动的工具界面

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
