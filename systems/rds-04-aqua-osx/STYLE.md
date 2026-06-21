---
name: "Mac OS X Aqua"
category: "os-interfaces"
year: 2001
tags: [mac, glossy, gel, aqua]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/04-aqua-osx/"
palette_colors: ["#b8c9e0", "#e8e8e8", "#c8c8c8", "#4d90fe", "#2057c2", "#ff9a8a", "#ff4b2b", "#b21808"]
---

# Mac OS X Aqua

## 一句话

水滴、凝胶、条纹。苹果把'lickable'变成设计语言。

## 设计哲学

Aqua 是 Steve Jobs 时代的视觉宣言——界面应该看起来'好看到想舔'。标志性的凝胶按钮、pinstripe 背景、半透明窗口、液态滚动条——一切都在模仿水滴和半透明材质。这是skeuomorphism（拟物化）的巅峰，每个控件都在告诉你它的物理质感。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#b8c9e0` | 背景 |
| `--chrome` | `linear-gradient(to bottom, #e8e8e8, #c8c8c8)` | 其他 |
| `--pinstripe` | `repeating-linear-gradient(to bottom, rgba(255,255,255,0.7) 0 1px, rgba(220,22...` | 其他 |
| `--aqua-blue` | `#4d90fe` | 其他 |
| `--aqua-blue-deep` | `#2057c2` | 其他 |
| `--jelly-red` | `radial-gradient(circle at 30% 30%, #ff9a8a, #ff4b2b 40%, #b21808)` | 其他 |
| `--jelly-yellow` | `radial-gradient(circle at 30% 30%, #ffee8a, #ffbe2b 40%, #b28008)` | 其他 |
| `--jelly-green` | `radial-gradient(circle at 30% 30%, #b5f28a, #59c42b 40%, #1f7008)` | 其他 |

## Do / Don't

- ✅ 凝胶质感按钮（顶部高光 + 底部阴影）
- ✅ pinstripe 条纹窗口背景
- ✅ 半透明 + 模糊效果
- ✅ 圆润的大圆角

- ❌ 不要用扁平色块（必须有质感）
- ❌ 不要用暗色主题（Aqua 是明亮的）
- ❌ 不要用直角
- ❌ 不要省略高光和阴影——这是 Aqua 的灵魂

## 适用场景

macOS 怀旧、拟物化 UI、高品质工具栏设计

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles//
