# Design Atlas

> 视觉设计风格聚合库 — 收录、分类、展示好看的 CSS 设计 token 和视觉设计系统。
> **AI Agent 友好** — 支持 Claude Code / Cursor / Codex 等 AI 编码工具接入。

## 这是什么

Design Atlas 是一个设计风格的聚合收藏库。在 vibecoding 的浪潮下，AI 能写出代码，但往往不知道什么是"好看的"。这个库收集各种好看的设计风格，做好分类，并通过 **MCP Server** 和 **Agent Skill** 让 AI 编码工具可以直接搜索和应用这些设计指引。

### 核心理念

```
Vibecoding 的瓶颈不在"AI 写不出代码"，而在"AI 不知道什么是好看的"
```

### Agent 接入方式

| 方式 | 说明 | 适用工具 |
|------|------|---------|
| **MCP Server** | 6 个实时查询工具：搜索风格、获取 Token、智能推荐 | Claude Code, Cursor, Codex |
| **Agent Skill** | `.agents/skills/design-atlas/` 三端通用 SKILL.md | Claude Code, Cursor, Codex |
| **静态阅读** | 本 README + Gallery 页面浏览 | 人类用户 |

详细设置指南: [server/SETUP.md](./server/SETUP.md)

### 核心能力

1. **收录** — 收集各种好看的设计风格（从复古 OS 界面到当代 Web 设计）
2. **分类** — 按视觉来源分类，8 大类 + 多维标签交叉筛选
3. **展示** — 暗色美术馆风格的 Gallery
4. **接入** — MCP Server + Agent Skill 双通道 Agent 接入

### 当前收录统计

- **59** 个设计系统 / **7** 个来源 / **8** 大分类
- **4** 种来源类型（aggregator / component-lib / theme-css / design-tokens）
- 最新收录: NES.css (21.8k⭐) / 98.css (11.1k⭐) / XP.css (3k⭐) / 7.css (2.4k⭐) / NeoBrutalismCSS / cyberpunk-css

### 收录来源类型

收录 Agent 会自动探测以下 4 种来源类型：

| 类型 | 说明 | 示例 | Token 存储方式 |
|------|------|------|--------------|
| `aggregator` | 聚合仓库（含多个子风格，每个有自己的 demo HTML） | retro-design-system (53 styles) | 每个子风格独立的 `:root` CSS 变量 |
| `component-lib` | 单一组件库或设计系统 | NES.css / 98.css / 7.css | CSS 自定义属性、SCSS `$variables` 或 Sass maps |
| `theme-css` | 主题 CSS（简单的 CSS 包，纯样式覆盖） | cyberpunk-css / NeoBrutalismCSS | 少量的 CSS 自定义属性或 SCSS 变量 |
| `design-tokens` | 纯 token 集（计划中） | — | — |

每个来源类型使用不同的探测算法和 token 提取方法。详见 [collector/ingest.py](./collector/ingest.py)。

每个收录的设计系统都明确标注来源（作者、仓库、许可证），尊重原创。

## 分类体系

8 大类，按"视觉来源"分（人类直觉能理解这个东西从哪来）：

| # | 大类 | 说明 |
|---|------|------|
| 1 | **OS Interfaces** | 操作系统界面美学（Mac System 7, Win95, Aqua...） |
| 2 | **Terminal & TUI** | 终端/命令行美学（CRT, DOS, IBM 3270...） |
| 3 | **Gaming** | 游戏/游戏机 UI（8-bit, Game Boy, PS1...） |
| 4 | **Design Movements** | 经典设计运动（Bauhaus, Swiss, Memphis...） |
| 5 | **Web Eras** | Web 设计时代演进（Web 2.0, Flat, Glassmorphism...） |
| 6 | **Retro-Futurism** | 复古未来/赛博美学（Vaporwave, Y2K, Matrix...） |
| 7 | **Print & Craft** | 印刷工艺/技术绘图（Risograph, Blueprint, Grid Paper...） |
| 8 | **Art** | 艺术风格转译（Pop Art, Op Art...） |

详见 [categories.md](./categories.md)。

## 目录结构

```
design-atlas/
├── server/                    ← Agent 接入层
│   ├── mcp_server.py          ← MCP Server（6 个 tools）
│   ├── SETUP.md               ← 三端配置指南
│   └── mcp.json.template      ← Claude Code MCP 配置模板
├── .agents/skills/            ← Agent Skill（三端通用）
│   └── design-atlas/
│       ├── SKILL.md           ← 设计风格指引
│       └── references/        ← 详细参考文档
├── .claude/skills/            ← Claude Code 兼容
├── .cursor/skills/            ← Cursor 兼容
├── manifest.json              ← 全局索引（所有系统的元数据）
├── categories.md              ← 分类体系说明
├── sources.md                 ← 来源仓库记录
├── systems/                   ← 所有收录的设计系统
│   └── {id}/
│       ├── STYLE.md           ← 设计语言描述 + 学习笔记 + Do/Don't
│       ├── tokens.css         ← CSS 变量（可直接 @import）
│       └── preview.png        ← 预览截图
├── gallery/                   ← 广场页面（暗色美术馆）
│   ├── index.html
│   ├── style.css
│   └── app.js                 ← 读 manifest.json 渲染网格 + 筛选
├── collector/                 ← 收录 Agent & 工具
│   ├── ingest.py              ← 自动收录 pipeline
│   ├── screenshot-all.js      ← Playwright 批量截图脚本
│   ├── screenshot-sources.js  ← 新来源截图工具
│   └── style_descriptions.json
└── _templates/                ← 模板
    └── STYLE.template.md
```

## 使用

### AI Agent：通过 MCP Server 查询

```bash
# 启动 MCP Server（stdio 模式，实时 JSON-RPC）
python3 server/mcp_server.py

# Agent 可以调用：
# - search_styles(query, category, tags) → 搜索设计风格
# - get_style_detail(id) → 获取设计哲学 + Do/Don't + Token
# - get_guidance(task_description) → 智能推荐（不知道用什么风格时）
# - list_categories() → 浏览所有分类
# - get_tokens(id) → 获取 CSS 变量
# - apply_style(id) → 一键应用（含 Token 注入 + 使用准则）
```

### 人类：浏览 Gallery 页面

```bash
cd design-atlas
python3 -m http.server 8000
# 打开 http://localhost:8000/gallery/
```

### 自动收录新来源

```bash
python3 collector/ingest.py --repo https://github.com/user/cool-css --demo https://user.github.io/cool-css/
```

收录 Agent 会自动：
1. 克隆仓库 → 探测来源类型（aggregator / component-lib / theme-css）
2. 检测 CSS 格式（`:root` 变量 / SCSS `$variables` / Sass maps）
3. 提取设计 token → 生成 `tokens.css`
4. Playwright 截取 demo 页面 → 生成 `preview.png`
5. 生成 `STYLE.md` → 更新 `manifest.json`

### 手动添加

1. 在 `systems/{id}/` 下创建文件
2. 参考 `_templates/STYLE.template.md` 编写 STYLE.md
3. 更新 `manifest.json` 的 `systems` 和 `sources` 数组

## License

- 本仓库自身的内容（分类体系、广场页面、收录工具、MCP Server）：MIT
- 收录的设计系统：版权归各自作者所有，详见每个系统的 `source` 字段
