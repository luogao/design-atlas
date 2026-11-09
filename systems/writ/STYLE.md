---
name: writ
source:
  url: https://github.com/programble/writ
  demo: https://writ.cmcenroe.me
  type: theme-css
  author: programble
  license: ISC
one_liner: 2015 年的「印刷书页」classless 样式 — Palatino 衬线 + 1.5rem 垂直节奏 + ch 单位测宽，旁注浮到页边，读起来像排过版的纸书
tags: [classless, serif, minimal, print, bookish, semantic]
---

# writ

> **排版先于装饰** —— Curtis McEnroe（programble）2015 年做的 3KB 样式表，只干一件事：让语义 HTML 读起来像一本排过版的书。
> 字号走 **minor third（约 1.2 倍）** 音阶：h1 2.488em → h2 2.074em → h3 1.728em → h4 1.44em → h5 1.2em；所有垂直间距都是 1.5rem 的整数倍，文字自然落在同一条基线上。

## 视觉特征

1. **Palatino 衬线正文** — `Palatino, Georgia, Lucida Bright, Book Antiqua, serif`，16px / 1.5rem 行高
2. **字阶 = minor third** — 五级标题严格按 1.2 倍递减，且标题 `font-weight: normal`：靠字号而非粗细分层，典型印刷做法
3. **`ch` 单位测宽** — 正文 `max-width: 78ch`，边距 `1.5rem 1ch`，列表缩进 `3ch`／引用 `1.5ch`，宽度锚在「字符」而非像素
4. **旁注浮页边** — `main figure, main aside { float: right }`，aside 限宽 26ch 加左侧粗线，天然支持 Tufte 式 marginalia
5. **链接无下划线** — `a { text-decoration: none }`，靠颜色区分：`#00e` 蓝、visited `#60b` 紫、`mark` 高亮 `#fe0` 黄
6. **代码块 2px 圆角 + 1px 边框** — 边框 `rgba(0,0,0,.1)`，表格线 `#dbdbdb`，全站零阴影
7. **列表符号分级** — ul 三层 disc → circle → square；ol 三层 decimal → lower-roman → lower-alpha
8. **header 居中 + nav 行内** — `body > header { text-align: center }`，`nav ul li` 全 `display: inline`，像书前的题名页

## 关键 Token

| Token | 值 | 说明 |
|-------|-----|------|
| `--palette-1` | `#ffffff` | 纸白底 |
| `--palette-2` | `#222222` | 正文 |
| `--palette-3` | `#111111` | 代码文字 |
| `--palette-4` | `#0000ee` | 链接蓝 |
| `--palette-5` | `#6600bb` | visited 紫 |
| `--palette-6` | `#ffee00` | mark 高亮黄 |
| `--palette-7` | `#f2f2f2` | 代码块底（5% 黑压白） |
| `--palette-8` | `#dbdbdb` | 表格边框 |
| `--font-family-primary` | `Palatino, Georgia, …` | 衬线正文栈 |
| `--font-size-base` | `16px` | 基准字号 |
| `--line-height` | `1.5rem` | 垂直节奏基数 |
| `--measure` | `78ch` | 正文最大宽度 |
| `--border-radius` | `2px` | 代码块圆角 |

## 配色板

```
#222222  #111111                         ← 正文 / 代码
#0000ee  #6600bb  #ffee00                ← 链接 / visited / 高亮
#f2f2f2  #dbdbdb  #ffffff                ← 代码底 / 边框 / 纸白
```

## 适合

长文、散文、书籍式文档、个人日志、把 README 变长文 —— 任何「要读十分钟以上」的页面。配代码块也稳，但 78ch 偏窄，不适合宽表格和数据面板。

## 来源

- **仓库**: [programble/writ](https://github.com/programble/writ) (466 ⭐)
- **Demo**: [writ.cmcenroe.me](https://writ.cmcenroe.me)
- **License**: ISC — 作者 Curtis McEnroe，2015 建仓，当前 v1.0.4
- **技术**: 单文件纯 CSS（`writ.css` 3.1KB / `writ.min.css` 2.2KB），无 JS，走 Cloudflare CDN
