---
name: "Glassmorphism"
category: "web-eras"
year: 2020
tags: [glass, blur, frosted, modern]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/36-glassmorphism/"
palette_colors: ["#ffffff", "#ff6ec4", "#7873f5"]
---

# Glassmorphism

## 一句话

磨砂玻璃 + 模糊背景。Apple 和微软都在追的未来感。

## 设计哲学

Glassmorphism 用半透明 + 背景模糊（backdrop-filter: blur）创造层次感。元素像浮在毛玻璃后面，色彩从背景渗透出来。关键是要有足够丰富的背景才能让模糊效果发挥作用。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--ink` | `#ffffff` | 文字/前景 |
| `--muted` | `rgba(255,255,255,0.7)` | 其他 |
| `--glass-bg` | `rgba(255,255,255,0.15)` | 背景 |
| `--glass-border` | `rgba(255,255,255,0.3)` | 边框/线条 |
| `--accent` | `#ff6ec4` | 强调色 |
| `--accent-2` | `#7873f5` | 强调色 |
| `--font` | `"Inter", "SF Pro Display", "Segoe UI", system-ui, sans-serif` | 文字/前景 |

## Do / Don't

- ✅ backdrop-filter: blur() 磨砂效果
- ✅ 半透明白色叠加层
- ✅ 彩色渐变背景（必须）
- ✅ 细边框（1px rgba white）

- ❌ 不要在纯色背景上用（看不到效果）
- ❌ 不要用 100% 不透明度
- ❌ 不要忽略性能（blur 开销大）
- ❌ 不要用太多层模糊

## 适用场景

现代 SaaS 仪表盘、iOS/macOS 风格 UI、浮层和弹窗

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
