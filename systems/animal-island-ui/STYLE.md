---
name: Animal Island UI
source:
  url: https://github.com/guokaigdg/animal-island-ui
  demo: https://guokaigdg.github.io/animal-island-ui/#/
  type: component-lib
  author: guokaigdg
  license: MIT
one_liner: 动物森友会风格 React 组件库 — 温暖大地色 + 大圆角 pill 形 + 游戏按键立体感
tags: [playful, warm, organic, pastoral]
---

# Animal Island UI

> 受《集合啦！动物森友会》启发的 React + TypeScript UI 组件库（24 个组件）。
> 设计语言核心：**温暖大地色系 + 大圆角 pill 形 + 游戏按键立体感 + 柔和动效 + 几何/有机形状并存**。

## 核心设计特征

1. **色彩**：薄荷青绿主色 `#19c8b9` + 温暖棕色文字 `#794f27` + 奶油背景 `#f8f8f0`
2. **圆角**：极大型圆角（16–24px），pill/胶囊形按钮，柔和不锐利
3. **阴影**：棕色基调柔和投影 `rgba(61,52,40,0.1)`，营造立体按键感
4. **字体**：Nunito（拉丁）+ Noto Sans SC（中文），圆润友好
5. **动效**：0.15–0.35s，`cubic-bezier(0.4,0,0.2,1)` 缓动，柔和自然
6. **装饰元素**：SVG blob 裁切、swallowtail clip-path 飘带、波点墙纸（radial-gradient）

## 关键 Token 速查

| Token | 值 | 说明 |
|-------|---|------|
| `--ai-primary` | `#19c8b9` | 薄荷青绿主色 |
| `--ai-text` | `#794f27` | 温暖棕色主文字 |
| `--ai-bg` | `#f8f8f0` | 奶油白背景 |
| `--ai-radius-base` | `18px` | 标志性大圆角 |
| `--ai-shadow-base` | `0 3px 10px rgba(61,52,40,0.1)` | 柔和立体阴影 |
| `--ai-warning` | `#f5c31c` | 动森黄色（聚焦/高亮） |
| `--ai-success` | `#6fba2c` | 自然绿色 |
| `--ai-error` | `#e05a5a` | 柔和红色 |

## 配色板

```
#19c8b9  #6fba2c  #f5c31c  #e05a5a   ← 功能色
#794f27  #9f927d  #c4b89e            ← 文字（棕系）
#f8f8f0  #f0e8d8  #e8e2d6            ← 背景（暖白系）
```

## 组件清单（24 个）

Button, Input, Switch, Modal, Card, Title, Collapse, Select, Checkbox,
Radio, Tooltip, Icon, Time, Phone, Footer, Divider, Cursor, Typewriter,
Tabs, CodeBlock, Loading, Table, WeddingInvitation

## 来源

- **仓库**: [guokaigdg/animal-island-ui](https://github.com/guokaigdg/animal-island-ui)
- **Demo**: [guokaigdg.github.io/animal-island-ui](https://guokaigdg.github.io/animal-island-ui/#/)
- **License**: MIT
- **技术栈**: React + TypeScript + Vite + Less Modules
- **自带 Skill**: 仓库内 `skill/SKILL.md` 有完整的设计风格指南 + AI 使用指南
