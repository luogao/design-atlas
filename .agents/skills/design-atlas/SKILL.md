---
name: design-atlas
description: Design Atlas 设计风格知识库——AI 编码 Agent 可搜索、引用和应用的设计风格集合
type: knowledge-base
cost: low
---

# Design Atlas — 设计风格知识库

Design Atlas 是一个收录了 **59 个设计系统**（来自 7 个来源）的设计风格聚合库。包含从 Mac System 7 到赛博朋克 2077 的完整视觉指引。

## 接入方式

### 方式一（推荐）：MCP Server

MCP（Model Context Protocol）Server 提供 6 个实时查询工具，用于在设计开发过程中搜索和获取设计风格指引。

**启动 MCP Server：**
```bash
python3 /path/to/design-atlas/server/mcp_server.py
```

**可用的 MCP Tools：**

| Tool | 用途 | 何时使用 |
|------|------|---------|
| `search_styles(query, category, tags)` | 搜索设计风格 | 查找某个风格时 |
| `get_style_detail(id)` | 获取风格完整信息 | 确定使用某个风格后 |
| `get_guidance(task_description)` | 智能推荐 | 不确定用什么风格时 |
| `list_categories()` | 浏览分类 | 了解整体结构 |
| `get_tokens(id)` / `apply_style(id)` | 获取/应用 Token | 开始写 CSS 时 |

### 方式二：静态 Skill 文件（本文件）

本 Skill 文件中包含所有风格的**关键指引摘要**，Agent 可以直接阅读这部分内容获得设计指引，无需启动 MCP Server。

---

## 关键风格指引摘要

> 以下是每个风格的一句话描述和核心 Do/Don't 准则。如需详细 Token 值，请启动 MCP Server 的 `get_tokens` 工具。

### Gaming（游戏 UI）

1. **NES.css** — 8-bit 像素风 CSS 框架，复古任天堂美学
   - ✅ Press Start 2P 像素字体、4px 粗边框、NES 调色板（蓝/绿/黄/红）
   - ❌ 无圆角、无渐变/阴影、不混现代字体
   - 🔗 `https://nostalgic-css.github.io/NES.css/`
   - 🆔 `ext-nes-css`

### OS Interfaces（操作系统界面）

2. **98.css** — Windows 98 风格 CSS 设计系统
   - ✅ box-shadow 模拟 3D 凸起边框、#c0c0c0 灰色表面、#000080 深蓝标题栏
   - ❌ 无圆角、无现代动画、不改变 MS Sans Serif 字体
   - 🔗 `https://jdan.github.io/98.css/`
   - 🆔 `ext-98css`

3. **XP.css** — Windows XP Luna 主题 CSS
   - ✅ Luna 蓝色渐变标题栏、圆角、米色表面、双主题切换
   - ❌ 不要过度 glassmorphism、不用 Win98 硬边框
   - 🔗 `https://botoxparty.github.io/XP.css/`
   - 🆔 `ext-xp-css`

4. **7.css** — Windows 7 Aero Glass 风格
   - ✅ Segoe UI 字体、Aero 毛玻璃、完整状态覆盖（normal/hover/active/disabled）
   - ❌ 不要扁平化、用 1px 精致边框
   - 🔗 `https://khang-nd.github.io/7.css/`
   - 🆔 `ext-7-css`

### Design Movements（设计运动）

5. **NeoBrutalismCSS** — 新粗野主义 CSS 框架
   - ✅ 粗黑边框（2-4px solid）、偏移硬阴影（无模糊）、高饱和色块、粗体 sans-serif
   - ❌ 无圆角、无模糊阴影、无渐变、不怕"丑"
   - 🔗 `https://matifandy8.github.io/NeoBrutalismCSS/`
   - 🆔 `ext-neobrutalism-css`

### Retro-Futurism（复古未来）

6. **cyberpunk-css** — 赛博朋克 2077 风格
   - ✅ 霓虹黄底黑字 + 青色链接、锯齿字体、斜切角、信息密度高
   - ❌ 不柔和不圆角、不大量留白
   - 🔗 `https://alddesign.github.io/cyberpunk-css/demo/`
   - 🆔 `ext-cyberpunk-css`

> 完整 59 个风格请启动 MCP Server（`python3 server/mcp_server.py`）并用 `search_styles` 或 `list_categories` 浏览。

---

## 工作时流程

当被要求"根据某个风格做 UI"时，请按以下步骤：

1. **搜索风格** → `search_styles(query, category, tags)` 找到匹配的风格
2. **获取详情** → `get_style_detail(id)` 获取设计哲学 + Do/Don't + Token 表
3. **获取 Token** → `get_tokens(id)` 获取原始 CSS 变量
4. **应用** → 将 Token 注入 CSS `:root`，按 Do/Don't 准则编码

当你不确定用什么风格时：
1. **获取推荐** → `get_guidance(task_description)` 获取智能推荐
2. **浏览分类** → `list_categories()` 了解整体结构
3. **详情+应用** → 同上

---

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
