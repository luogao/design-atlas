---
name: magick.css
source:
  url: https://github.com/wintermute-cell/magick.css
  demo: https://css.winterveil.net
  type: theme-css
  author: winterveil (wintermute-cell)
  license: MIT
one_liner: 单文件「魔法书」风 — 纯黑白 + 古籍衬线排版，旁注浮到页边，让裸 HTML 读起来像一本 17 世纪的手稿
tags: [classless, single-file, serif, playful, monochrome]
---

# magick.css

> **把网页做成古籍**：20KB 单文件，`magick.css` 一引，`<h1>` 变手刻标题、`<aside>` 变页边旁注、`<table>` 变账本。官方分类标签自己写着 `ttrpg` / `latex` / `old-school` / `wizard`。
> 2024-03 建仓，1041 ⭐。它不追求「好看的 App」，而是追求**读起来像印刷品**——这类「拟书」风格在 classless 圈子里辨识度最高。

## 视觉特征

1. **纯黑白，只有两个色变量** — `--fg: #0e0e0e` / `--bg: #fefefe`，没有强调色、没有渐变，视觉冲击全靠字号和字形
2. **四套字体分工** — 正文 `Averia Serif Libre`（略带弹性的衬线）、标题 `Averia Libre`（更像手绘）、引文/表格 `Spectral`、代码 `Courier Prime`、手写点缀 `Caveat`
3. **旁注浮到页边（sidenote）** — `.sidenote` / `<aside>` 用 `float: right; width: 40%` 拉到正文右侧，左侧 3px 实线；这是 LaTeX `\marginpar` 的网页版，手机端（≤600px）自动退化成普通块
4. **旁注自动编号** — body 上 `counter-reset: sidenote-counter`，配合计数器实现「¹²³」式注释，不用手写编号
5. **18px 正文 + 2.2rem 行高** — 行距明显比常规框架松（1.22 倍字号以上），是「书页」而非「屏幕」的密度
6. **76rem 正文宽度 + 居中** — `article, main { max-width: 76rem }`，长文不会摊平，留白两侧
7. **表单当纸片** — `form` 用 `grid-template-columns: 1fr 1fr` 两列，加 `box-shadow: 0 0 10px rgba(0,0,0,.1)` 做成「贴在页面上的便签」
8. **暗色模式内置** — `@media (prefers-color-scheme: dark)` 里把 `--fg`/`--bg` 对调，自动变黑纸白字，代码零改动

## 关键 Token

| Token | 值 | 说明 |
|-------|-----|------|
| `--palette-1` | `#fefefe` | 纸白（浅色底 / 深色文字） |
| `--palette-2` | `#0e0e0e` | 墨黑（浅色文字 / 深色底） |
| `--palette-3` | `#fbfbfb` | 表单底（浅色模式） |
| `--palette-4` | `#00004d` | 表单文字（极深蓝，几乎当黑用） |
| `--font-family-primary` | `"Averia Serif Libre", serif` | 正文衬线 |
| `--font-family-display` | `"Averia Libre", cursive` | 标题（手绘感） |
| `--font-family-serif` | `"Spectral", serif` | 引文/表格/图注 |
| `--font-family-hand` | `"Caveat", cursive` | 手写点缀 |
| `--font-size-base` | `1.8rem` | 18px（html 62.5% 基准） |
| `--line-height-base` | `2.2rem` | 行高，明显偏松 |
| `--box-shadow` | `0 0 10px 0 rgba(0, 0, 0, 0.1)` | 表单「纸片」投影 |

## 配色板

```
#fefefe  #fbfbfb          ← 纸白 / 表单底
#0e0e0e  #00004d          ← 墨黑 / 表单文字
```
（单色系统：三档灰度 + 一个近黑深蓝，没有彩色）

## 适合

长文阅读页、TTRPG 设定集/跑团 wiki、个人笔记与手记、教程与文档——任何「希望读者慢下来读」的页面。不适合后台面板、数据看板这类要密集控件的界面。

## 来源

- **仓库**: [wintermute-cell/magick.css](https://github.com/wintermute-cell/magick.css) (1041 ⭐)
- **Demo**: [css.winterveil.net](https://css.winterveil.net)
- **License**: MIT — 作者 winterveil，2024-03 建仓，当前 v1.0.5
- **技术**: 单文件纯 CSS（20.4KB 未压缩），字体走 Google Fonts `@import`，无 JS
