---
name: "Brutalist Web"
category: "web-eras"
year: 2016
tags: [brutalist, raw, mono, highcontrast]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/40-brutalist-web/"
palette_colors: ["#ffffff", "#000000", "#0000ee", "#551a8b", "#ff0000", "#c0c0c0", "#e0e0e0", "#f0f0f0"]
---

# Brutalist Web

## 一句话

Times New Roman + 系统蓝链接 + 零 CSS。你的浏览器就是画布。

## 设计哲学

Web Brutalism 刻意拒绝一切设计系统——默认字体、默认链接颜色、无边框、无圆角、无阴影。设计意图是让内容赤裸裸地暴露，用'反设计'来表达态度。它不是'不会设计'，而是'故意不设计'。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#ffffff` | 背景 |
| `--ink` | `#000000` | 文字/前景 |
| `--link` | `#0000ee` | 文字/前景 |
| `--link-visited` | `#551a8b` | 文字/前景 |
| `--font` | `"Times New Roman", Times, serif` | 文字/前景 |
| `--font-size` | `16px` | 文字/前景 |
| `--border` | `2px solid #000` | 边框/线条 |

## Do / Don't

- ✅ 使用浏览器默认样式（或接近默认）
- ✅ Times New Roman / Georgia
- ✅ 蓝色下划线链接
- ✅ 无 max-width（全宽布局）

- ❌ 不要加 CSS reset
- ❌ 不要用无衬线字体
- ❌ 不要用圆角或阴影
- ❌ 不要用设计系统（Tailwind/Bootstrap）

## 适用场景

个人博客、宣言页面、反设计实验、学术内容

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
