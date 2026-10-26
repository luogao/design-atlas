---
name: milligram
source:
  url: https://github.com/milligram/milligram
  demo: https://milligram.io
  type: theme-css
  author: CJ Patoilo
  license: MIT
one_liner: 极简 CSS 框架 — 单紫色强调 + 宽松留白，2KB 的「排版优先」范本
tags: [minimal, typography, centered, light, sans-serif]
---

# milligram

> **极简 CSS 框架**：官方自述 "It's not about a UI framework"，只给一套干净的排版底座 + 10 列网格，压缩后 **约 2KB**。
> 2015 年发布，是「极简 CSS 框架」这一波（Skeleton / Milligram / mini.css）里最有辨识度的一个：白底、宽行距、只有一个紫色。

## 视觉特征

1. **单强调色** `#9b4dca`（紫）— 按钮、链接、focus 环全用这一个紫，其余全灰。整套系统只有 1 个彩色，克制到极致
2. **Roboto 打底** — `'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif`，无衬线、字重归一
3. **大字 + 大行距** — `1.6rem` 基准字号，`1.6` line-height，读起来像文档不像界面
4. **留白非常松** — `1rem` 节奏的 margin/padding，卡片与表单之间空隙大，页面像纸张而不是仪表盘
5. **小圆角统一** — `.4rem` 全站一个值（按钮、输入框、卡片一致），不出现直角混圆角
6. **无 box-shadow** — 深度全靠边框 `#d1d1d1` + 底色 `#f4f5f6`，纸感而非塑料感
7. **10 列网格** — `.container` + `.row` + `.column`，`column-1`…`column-10`，比 12 列更好心算
8. **class 需手写** — 不是 classless：`<a class="button">`、`<div class="container">`，但类名极少

## 关键 Token

| Token | 值 | 说明 |
|-------|---|------|
| `--palette-1` | `#9b4dca` | 唯一强调色（紫） |
| `--palette-2` | `#606c76` | 正文灰 |
| `--palette-3` | `#f4f5f6` | 浅底块 |
| `--palette-4` | `#d1d1d1` | 边框灰 |
| `--font-family-primary` | `Roboto, Helvetica Neue, Helvetica, Arial, sans-serif` | 全站字体 |
| `--font-size-base` | `1.6rem` | 基准字号 |
| `--border-radius` | `.4rem` | 全站唯一圆角 |
| `--box-shadow` | `none` | 明确不用阴影 |

## 配色板

```
#9b4dca                                    ← 强调紫（唯一彩色）
#606c76  #d1d1d1  #e1e1e1                  ← 文字 / 边框 / 分割
#f4f5f6  #ffffff                           ← 浅底 / 页面底
```

## 适合

营销落地页、产品文档、快速原型的排版底座。想要「安静、留白多、只有一个紫色点缀」的页面时最省事。

## 来源

- **仓库**: [milligram/milligram](https://github.com/milligram/milligram) (10.2k ⭐)
- **Demo**: [milligram.io](https://milligram.io)
- **License**: MIT — 设计 CJ Patoilo，2015-12 建仓
- **技术**: 纯 CSS（Sass 源 → dist CSS），无 JS
