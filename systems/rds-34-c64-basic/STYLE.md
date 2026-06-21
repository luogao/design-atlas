---
name: "Commodore 64 BASIC"
category: "terminal-tui"
year: 1982
tags: [c64, blue, petscii, basic]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/34-c64-basic/"
palette_colors: ["#9692d9", "#443ec4", "#2e2898", "#a8a0ff", "#c8c0ff", "#ffffff", "#e04040", "#4aff4a"]
---

# Commodore 64 BASIC

## 一句话

READY. 光标在闪烁。8 位色的童年。

## 设计哲学

Commodore 64 的 BASIC 界面是无数人的编程启蒙——浅蓝文字 on 深蓝背景，闪烁的光标等待输入。16 色调色板中有一些标志性的颜色组合成为了 8 位时代的视觉符号。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--border` | `#9692d9` | 边框/线条 |
| `--bg` | `#443ec4` | 背景 |
| `--bg-dark` | `#2e2898` | 背景 |
| `--text` | `#a8a0ff` | 文字/前景 |
| `--text-hi` | `#c8c0ff` | 文字/前景 |
| `--white` | `#ffffff` | 其他 |
| `--red` | `#e04040` | 其他 |
| `--green` | `#4aff4a` | 其他 |

## Do / Don't

- ✅ C64 16 色调色板
- ✅ 大写 ONLY 的等宽字体
- ✅ 全屏文本模式布局
- ✅ 闪烁光标效果

- ❌ 不要用超过 16 色
- ❌ 不要用小写字母（C64 默认大写）
- ❌ 不要用平滑图形
- ❌ 不要用现代字体

## 适用场景

8 位致敬、编程教育、复古计算演示

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
