---
name: design-atlas
description: Design Atlas 设计风格知识库——AI Agent 可搜索、引用和应用的设计风格集合（纯 Skill 方案，无需 MCP Server）
type: knowledge-base
cost: low
---

# Design Atlas — 设计风格知识库

Design Atlas 是一个收录了 **59 个设计系统**（来自 7 个来源）的设计风格聚合库。包含从 Mac System 7 到赛博朋克 2077 的完整视觉指引。

## 数据位置

所有数据在 `~/Documents/Hermes/design-atlas/` 目录下：

```
design-atlas/
├── manifest.json          ← 全局索引（所有系统的元数据 + 标签 + 分类）
├── systems/
│   └── {id}/
│       ├── STYLE.md       ← 设计语言描述 + Do/Don't + 使用场景
│       └── tokens.css     ← CSS 变量（可直接复制或 @import）
└── .agents/skills/
    └── design-atlas/SKILL.md  ← 本文件（快速指引摘要）
```

## 工作流程

当被要求"根据某个风格做 UI"时：

1. **快速匹配** → 先看下方的 **风格指引摘要**，如果已有，直接用 Do/Don't 和 Token
2. **按分类浏览** → 见下方 **分类体系速查**，确定大类
3. **搜索 manifest.json** → 用 `read_file` 读 `manifest.json`，搜索 `category`、`tags`、`name` 字段
4. **获取完整详情** → 用 `read_file` 读 `systems/{id}/STYLE.md`
5. **获取 CSS Token** → 用 `read_file` 读 `systems/{id}/tokens.css`，注入 `:root`
6. **预览参考** → 参考 `systems/{id}/preview.png`（如有）

当不确定用什么风格时：
1. **分类速查** → 浏览下方 8 大类
2. **按 mood 搜索** → 在 manifest.json 的 `tags` 中搜索 mood（minimal/bold/playful/dark/warm/futuristic/nostalgic/elegant/raw）
3. **确定风格** → 读对应的 STYLE.md 确认

## 关键风格指引摘要

> 以下是 6 个核心风格的快速指引。全部 59 个风格请通过 manifest.json 搜索。

### Gaming（游戏 UI）

**ext-nes-css** — 8-bit 像素风 CSS 框架，复古任天堂美学
- ✅ Press Start 2P 像素字体、4px 粗边框、NES 调色板（蓝/绿/黄/红）
- ❌ 无圆角、无渐变/阴影、不混现代字体
- 📁 `systems/nes-css/STYLE.md` · `systems/nes-css/tokens.css`

### OS Interfaces（操作系统界面）

**ext-98css** — Windows 98 风格 CSS 设计系统
- ✅ box-shadow 模拟 3D 凸起边框、#c0c0c0 灰色表面、#000080 深蓝标题栏
- ❌ 无圆角、无现代动画、不改变 MS Sans Serif 字体
- 📁 `systems/98css/STYLE.md` · `systems/98css/tokens.css`

**ext-xp-css** — Windows XP Luna 主题 CSS
- ✅ Luna 蓝色渐变标题栏、圆角、米色表面、双主题切换
- ❌ 不要过度 glassmorphism、不用 Win98 硬边框
- 📁 `systems/xp-css/STYLE.md` · `systems/xp-css/tokens.css`

**ext-7-css** — Windows 7 Aero Glass 风格
- ✅ Segoe UI 字体、Aero 毛玻璃、完整状态覆盖（normal/hover/active/disabled）
- ❌ 不要扁平化、用 1px 精致边框
- 📁 `systems/7-css/STYLE.md` · `systems/7-css/tokens.css`

### Design Movements（设计运动）

**ext-neobrutalism-css** — 新粗野主义 CSS 框架
- ✅ 粗黑边框（2-4px solid）、偏移硬阴影（无模糊）、高饱和色块、粗体 sans-serif
- ❌ 无圆角、无模糊阴影、无渐变、不怕"丑"
- 📁 `systems/neobrutalism-css/STYLE.md` · `systems/neobrutalism-css/tokens.css`

### Retro-Futurism（复古未来）

**ext-cyberpunk-css** — 赛博朋克 2077 风格
- ✅ 霓虹黄底黑字 + 青色链接、锯齿字体、斜切角、信息密度高
- ❌ 不柔和不圆角、不大量留白
- 📁 `systems/cyberpunk-css/STYLE.md` · `systems/cyberpunk-css/tokens.css`

## 分类体系速查

| 分类 ID | 分类名 | 风格数 |
|---------|-------|-------|
| `os-interfaces` | OS Interfaces（操作系统界面） | 13 |
| `terminal-tui` | Terminal & TUI（终端美学） | 8 |
| `gaming` | Gaming（游戏 UI） | 5 |
| `design-movements` | Design Movements（设计运动） | 6 |
| `web-eras` | Web Eras（Web 时代） | 10 |
| `retro-futurism` | Retro-Futurism（复古未来） | 10 |
| `print-craft` | Print & Craft（印刷工艺） | 5 |
| `art` | Art（艺术风格） | 2 |

## tags 标签体系

manifest.json 中每个风格有 `tags` 数组，支持多维筛选：

- **mood**：minimal, bold, playful, dark, warm, futuristic, nostalgic, elegant, raw
- **palette**：monochrome, duotone, neon, primary-colors, pastel, earth-tone, 8bit, inverted, gray
- **typography**：serif, sans, pixel, mono, script, display
- **era**：1970s, 1980s, 1990s, 2000s, 2010s, 2020s
- **best_for**：app-ui, game-ui, data-viz, landing-page, portfolio, blog, game, tool, poster

## 使用示例

**用户说：** "帮我做一个复古游戏排行榜页面"

1. 先看摘要 → ext-nes-css 匹配（Gaming 类 + playful + 像素字体）
2. 读 `systems/nes-css/STYLE.md` 获取 Do/Don't 和关键 Token
3. 读 `systems/nes-css/tokens.css` 获取完整 CSS 变量
4. 按 Do/Don't 生成代码

**用户说：** "做一个黑暗氛围的 dashboard"

1. 在 manifest.json 搜索 "dark" tag
2. 找到匹配的风格（如 rds-31-midnight-commander、rds-46-monochrome-zen 等）
3. 读对应 STYLE.md 确认设计哲学
4. 读 tokens.css 应用
