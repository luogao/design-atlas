# Design Atlas — Agent 接入设置指南

> 让 Claude Code、Cursor、Codex 等 AI 编码工具可以直接使用 Design Atlas 的设计风格。
> **纯 Skill 方案，无需启动任何服务。**

## 前置条件

- 已 clone `design-atlas` 仓库到本地

## 接入方式

### Agent Skill（推荐，零基础设施）

Skill 文件已位于以下三端兼容位置：

| 路径 | 兼容工具 |
|------|---------|
| `.agents/skills/design-atlas/SKILL.md` | 所有工具（推荐标准位置） |
| `.claude/skills/design-atlas/SKILL.md` | Claude Code |
| `.cursor/skills/design-atlas/SKILL.md` | Cursor |

如果你在自己的项目中使用 Design Atlas，请在项目根目录创建 symlink：

```bash
cd /path/to/your/project
ln -sf $(pwd)/design-atlas/.agents/skills/design-atlas .agents/skills/design-atlas
```

### 工作原理

Agent 通过读取本地文件获取设计指引，无需任何后台服务：

1. **浏览/搜索风格** → Agent 读取 `manifest.json`，按分类/tag/名称筛选
2. **获取完整详情** → Agent 读取 `systems/{id}/STYLE.md`
3. **获取 CSS Token** → Agent 读取 `systems/{id}/tokens.css`
4. **参考预览** → `systems/{id}/preview.png`

## 各工具的配置

### Claude Code

Claude Code 会自动检测 `.claude/skills/` 目录。
不需要任何配置，Skill 文件就位即可。

### Cursor

Cursor 会自动扫描 `.cursor/skills/` 目录。
也可以使用 `.cursor/rules/` 规则：

在 `.cursor/rules/design-atlas.mdc`：
```yaml
---
description: Design Atlas 设计风格知识库指引
globs: *.css, *.tsx, *.jsx, *.html
alwaysApply: false
---
加载 design-atlas SKILL.md（位于 .cursor/skills/design-atlas/SKILL.md）获取完整指引。
```

### Codex CLI (OpenAI)

Codex CLI 会自动检测 `.codex/skills/` 目录，也兼容 `.claude/skills/` 和 `.cursor/skills/`。
或者使用项目根目录的 `AGENTS.md`：

```markdown
## Design Atlas 设计风格库

本项目使用 Design Atlas（位于 design-atlas/ 目录）作为设计风格参考。
Agent 在执行 UI 任务前，请先搜索 Design Atlas 中的设计风格。

设计风格搜索请读取 design-atlas/manifest.json 获取索引，
再读取 design-atlas/systems/{id}/STYLE.md 和 tokens.css 获取完整指引。
```

## 工作流程

当 Agent 被要求创建 UI 时：

1. **确定风格** → 读 SKILL.md 快速匹配，或在 manifest.json 搜索 category/tags
2. **获取详情** → 读 `systems/{id}/STYLE.md`（设计哲学 + Do/Don't）
3. **获取 Token** → 读 `systems/{id}/tokens.css`
4. **生成 UI** → 将 Token 注入 CSS `:root`，按 Do/Don't 编码

## 注意事项

- 所有路径使用**项目内的相对路径**即可
- Agent 在项目目录下工作，路径从项目根开始
- 如果使用 git submodule，`git submodule update --remote` 后即可获取最新风格
- 新增风格会自动更新 manifest.json 的索引
