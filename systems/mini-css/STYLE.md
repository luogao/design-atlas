---
name: mini.css
source:
  url: https://github.com/Chalarangelo/mini.css
  demo: https://chalarangelo.github.io/mini.css
  type: component-lib
  author: Angelos Chalaris
  license: MIT
one_liner: 轻量扁平组件库 — Sass + Flexbox，语义 HTML 直接出界面，自带多套配色风味
tags: [minimal, component-library, flat, responsive, sass]
---

# mini.css

> **7KB 以下的响应式组件库**：官方定位 "minimal, responsive, style-agnostic"，用 Sass 写成、组件基于 Flexbox。
> 与纯 classless 框架的区别：它有一套轻量组件（卡片、模态、toast、tooltip、collapse），但组件样式默认挂在语义标签上，class 只是可选增强。

## 视觉特征

1. **浅蓝强调** `#0277bd` — 链接、按钮 hover、表头高亮都用这个蓝，是「Material 蓝 700」那一档
2. **近白底** `#f8f8f8` — 页面底色不是纯白，卡片浮在浅灰上，层级靠底色差而不是阴影
3. **扁平到底** — 按钮、输入框基本无阴影、圆角极小（`0.125rem`），2016 前后流行的「扁平 + 细边框」审美的标准样本
4. **多风味（flavors）** — 同一套组件换配色变量就是另一套皮：`mini-default`（浅）/ `mini-dark`（暗）/ `mini-nord`（Nord 冷灰），结构不变
5. **0.5rem 全局节奏** — `--universal-margin` / `--universal-padding` 都是 `0.5rem`，间距靠这两个变量统一收紧
6. **小字号高密度** — 组件偏紧凑，适合信息密度高的后台而不是营销页
7. **响应式内建** — 网格、表格、导航在移动端自动折行，不用写媒体查询

## 关键 Token

| Token | 值 | 说明 |
|-------|---|------|
| `--a-link-color` | `#0277bd` | 链接 / 强调蓝 |
| `--back-color` | `#f8f8f8` | 页面底色 |
| `--border-color` | `#aaa` | 常规边框 |
| `--button-back-color` | `#e2e2e2` | 按钮底 |
| `--table-head-back-color` | `#212121` | 表头深色 |
| `--blockquote-color` | `#f57c00` | 引用条橙色 |
| `--universal-margin` | `0.5rem` | 全局间距 |
| `--universal-border-radius` | `0.125rem` | 近直角 |

## 配色板

```
#0277bd  #01579b                           ← 链接蓝 / 已访问
#212121  #f8f8f8                           ← 文字 / 页面底
#e2e2e2  #aaa  #ddd                        ← 按钮 / 边框 / 分隔
#f57c00                                    ← 引用强调橙
```

## 适合

后台管理界面、文档站、需要「组件齐全但视觉不抢戏」的内部产品。

## 来源

- **仓库**: [Chalarangelo/mini.css](https://github.com/Chalarangelo/mini.css) (2.9k ⭐)
- **Demo**: [chalarangelo.github.io/mini.css](https://chalarangelo.github.io/mini.css)
- **License**: MIT — Angelos Chalaris
- **技术**: Sass → dist CSS，<7KB gzip，Flexbox 组件，无 JS 依赖
