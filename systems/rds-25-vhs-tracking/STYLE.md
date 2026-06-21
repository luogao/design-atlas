---
name: "VHS Tracking"
category: "retro-futurism"
year: 1980
tags: [vhs, glitch, scanline, analog]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/25-vhs-tracking/"
palette_colors: ["#0a0a0a", "#141014", "#ff1a1a", "#f4f4f4", "#ffe84a", "#4ae2ff", "#ff2a2a", "#2aff2a"]
---

# VHS Tracking

## 一句话

录像带追踪错位 + 色彩偏移。模拟时代的故障美学。

## 设计哲学

VHS 美学模拟录像带的视觉退化——tracking 错位的横条纹、色彩通道偏移（RGB split）、扫描线、噪点、时间戳。这种'故障'传达的是记忆的不稳定性和时间的流逝感。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#0a0a0a` | 背景 |
| `--tape` | `#141014` | 其他 |
| `--rec-red` | `#ff1a1a` | 其他 |
| `--osd-white` | `#f4f4f4` | 其他 |
| `--osd-yellow` | `#ffe84a` | 其他 |
| `--osd-cyan` | `#4ae2ff` | 其他 |
| `--smpte-red` | `#ff2a2a` | 其他 |
| `--smpte-green` | `#2aff2a` | 其他 |

## Do / Don't

- ✅ 色彩通道偏移（RGB split）
- ✅ 水平 tracking 线
- ✅ 扫描线 + 噪点叠加
- ✅ 时间戳 / REC 指示器

- ❌ 不要用高清干净的图像
- ❌ 不要用数字字体
- ❌ 不要修复'故障'
- ❌ 不要用太多颜色

## 适用场景

恐怖/惊悚主题、复古记忆项目、音乐 MV、Found footage 风格

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
