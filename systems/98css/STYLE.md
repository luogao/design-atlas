---
name: 98.css
slug: 98
category: OS Interfaces
tags: ["mood:nostalgic", "palette:gray", "typography:sans", "density:compact", "best_for:win98-ui"]
source:
  name: 98.css
  repo: jdan/98.css
  url: https://github.com/jdan/98.css
  demo: https://jdan.github.io/98.css/
  type: component-lib
  license: MIT
  author: Jordan Scales
one_liner: Windows 98 风格 CSS 设计系统，忠于原版的 UI 复刻
---

# 98.css

> Windows 98 风格 CSS 设计系统，忠于原版的 UI 复刻

## 设计哲学

用纯 CSS 和语义化 HTML 忠实还原 Windows 98 的每个像素。3D 凸起边框、MS Sans Serif 字体、经典蓝标题栏——这不是"灵感"，这是"考古级复刻"。

## 关键 Token

| Token | 值 |
|-------|---|
| `--border-field` | `inset -1px -1px var(--button-highlight),
    inset 1px 1px var(--button-shadow), inset -2px -2px var(--button-face),
    inset 2px 2px var(--window-frame)` |
| `--border-raised-inner` | `inset -2px -2px var(--button-shadow),
    inset 2px 2px var(--button-face)` |
| `--border-raised-outer` | `inset -1px -1px var(--window-frame),
    inset 1px 1px var(--button-highlight)` |
| `--border-status-field` | `inset -1px -1px var(--button-face), inset 1px 1px var(--button-shadow)` |
| `--border-sunken-inner` | `inset -2px -2px var(--button-face),
    inset 2px 2px var(--button-shadow)` |
| `--border-sunken-outer` | `inset -1px -1px var(--button-highlight),
    inset 1px 1px var(--window-frame)` |
| `--border-width` | `1px` |
| `--border-window-inner` | `inset -2px -2px var(--button-shadow),
    inset 2px 2px var(--button-highlight)` |
| `--border-window-outer` | `inset -1px -1px var(--window-frame),
    inset 1px 1px var(--button-face)` |
| `--button-shadow` | `#808080` |

## ✅ 应该做的

- ✅ 使用 box-shadow 模拟 3D 凸起/凹陷边框
- ✅ 保持 #c0c0c0 灰色表面
- ✅ 用 --dialog-blue (#000080) 深蓝标题栏
- ✅ 组件间距保持 8px

## ❌ 不应该做的

- ❌ 不要用圆角——Win98 是直角的
- ❌ 不要用现代动画——保持静态
- ❌ 不要改变字体——MS Sans Serif 是灵魂

## 适用场景

- Windows 98 复古应用
- 怀旧管理面板
- 复古创意项目
- Y2K 主题活动

## 来源

- **仓库**: [jdan/98.css](https://github.com/jdan/98.css) (11.1k ⭐)
- **Demo**: [https://jdan.github.io/98.css/](https://jdan.github.io/98.css/)
- **许可证**: MIT
- **作者**: Jordan Scales
