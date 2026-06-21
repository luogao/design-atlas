---
name: "Neumorphism"
category: "web-eras"
year: 2020
tags: [neumorph, soft, shadow, mono]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/37-neumorphism/"
palette_colors: ["#e0e5ec", "#4a5568", "#8a94a6", "#6c8cff", "#a3b1c6", "#ffffff"]
---

# Neumorphism

## 一句话

软 UI。光从四面八方来，按钮从背景里'长'出来。

## 设计哲学

Neumorphism（新拟物）把背景色作为基础，通过双重阴影（一明一暗）让元素看起来像是从背景里挤压出来的。关键是元素和背景同色——深度只通过阴影表达。视觉上极度柔和、统一、安静。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#e0e5ec` | 背景 |
| `--ink` | `#4a5568` | 文字/前景 |
| `--muted` | `#8a94a6` | 其他 |
| `--accent` | `#6c8cff` | 强调色 |
| `--shadow-dark` | `#a3b1c6` | 阴影 |
| `--shadow-light` | `#ffffff` | 阴影 |
| `--font` | `"Inter", "SF Pro", "Segoe UI", system-ui, sans-serif` | 文字/前景 |

## Do / Don't

- ✅ 元素与背景同色
- ✅ 双重 box-shadow（亮上左 + 暗下右）
- ✅ 大圆角（20px+）
- ✅ 柔和的内凹/外凸切换

- ❌ 不要用对比强烈的边框
- ❌ 不要用鲜艳的强调色
- ❌ 不要用渐变背景
- ❌ 不要忘记双阴影——单阴影会变成普通卡片

## 适用场景

设置面板、计算器、智能家居控制、安静的工具类 UI

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
