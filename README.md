# Design Atlas

> 视觉设计风格聚合库 — 收录、分类、展示好看的 CSS 设计 token 和视觉设计系统。

## 这是什么

Design Atlas 是一个设计风格的聚合收藏库。在 vibecoding 的浪潮下，AI 能写出代码，但往往不知道什么是"好看的"。这个库收集各种好看的设计风格，做好分类，让视觉指引变得可搜索、可消费。

### 核心目标

1. **收录** — 收集各种好看的设计风格（从复古 OS 界面到当代 Web 设计）
2. **分类** — 按视觉来源分类，多维标签交叉筛选
3. **展示** — 一个有设计感的浏览广场（暗色美术馆模式）
4. **接入** — 未来支持 agent 消费，让 AI 生成 UI 时有明确的视觉指引

### 收录类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `aggregator` | 聚合仓库（含多个子风格） | retro-design-system (53 styles) |
| `single-style` | 单一风格 CSS | cyberpunk-css |
| `component-lib` | 组件库 | neobrutalism-components |
| `design-tokens` | 纯 token 集 | Tailwind preset |

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
├── collector/                 ← 收录 Agent
│   ├── collect.py             ← URL → 自动收录
│   └── templates/
└── _templates/                ← 模板
    └── STYLE.template.md
```

## 使用

### 浏览
```bash
cd design-atlas
python3 -m http.server 8000
# 打开 http://localhost:8000/gallery/
```

### 收录新风格（P3 完成后）
```bash
python3 collector/collect.py https://github.com/example/cool-css
```

## License

- 本仓库自身的内容（分类体系、广场页面、收录工具）：MIT
- 收录的设计系统：版权归各自作者所有，详见每个系统的 `source` 字段
