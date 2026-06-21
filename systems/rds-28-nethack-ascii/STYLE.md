---
name: "NetHack ASCII"
category: "terminal-tui"
year: 1987
tags: [ascii, roguelike, terminal, mono]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/28-nethack-ascii/"
palette_colors: ["#000000", "#a0a0a0", "#707070", "#ffff00", "#ff4040", "#40ff40", "#6080ff", "#ff40ff"]
---

# NetHack ASCII

## 一句话

ASCII 字符就是整个世界。@ 是你，d 是狗，D 是龙。

## 设计哲学

NetHack 和所有 Roguelike 的视觉哲学：用 ASCII 字符代替图形，让想象力填补画面。每个字符都有意义——@ 是人、$ 是金币、> 是下楼梯。这是'信息密度即美学'的极致体现。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#000000` | 背景 |
| `--wall` | `#a0a0a0` | 其他 |
| `--floor` | `#707070` | 其他 |
| `--player` | `#ffff00` | 其他 |
| `--monster-red` | `#ff4040` | 其他 |
| `--monster-green` | `#40ff40` | 其他 |
| `--monster-blue` | `#6080ff` | 其他 |
| `--monster-magenta` | `#ff40ff` | 其他 |

## Do / Don't

- ✅ 纯 ASCII/Unicode 字符渲染
- ✅ 颜色编码字符类型
- ✅ 等宽字体 + 网格对齐
- ✅ 信息密度最大化

- ❌ 不要用图形/图标
- ❌ 不要用比例字体
- ❌ 不要用渐变或阴影
- ❌ 不要降低信息密度

## 适用场景

Roguelike 游戏、终端 UI、ASCII 艺术项目

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
