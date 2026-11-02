---
name: matcha
source:
  url: https://github.com/lowlighter/matcha
  demo: https://matcha.mizu.sh
  type: theme-css
  author: lowlighter
  license: MIT
one_liner: 语义化 drop-in 样式库 — 裸 HTML 直接出界面，取 GitHub Primer 蓝调 + 明暗双主题，可按模块 à la carte 只引需要的部分
tags: [classless, semantic, modular, minimal, dark-mode]
---

# matcha

> **半 classless 的「元素即组件」库**：不写 class 也能把 `<article>` `<nav>` `<table>` 排好，还额外给了 `mods` 机制——每个 HTML 元素一个 mod 文件，可以只下载你要的那几个。
> 2024-05 建仓，1942 ⭐。对比同类的 milligram/wing，matcha 的差异点是**配色直接搬 GitHub Primer**（浅色/深色两套 + `prefers-color-scheme` 自动切）和**可拆分的构建设计**。

## 视觉特征

1. **配色 = GitHub Primer** — `#0969da` 浅色蓝强调、`#4493f8` 深色蓝强调，正文 `#1f2328`，次要文字 `#656d76`，浅蓝底块 `#ddf4ff`，近黑品牌底 `#010409`
2. **明暗双主题原生支持** — `--light-*` / `--dark-*` 两套变量并存，`--accent` 等语义变量按 `prefers-color-scheme` 切换，不用自己写暗色覆盖
3. **18px 基准字号** — 比一般框架（16px）大一号，正文读感偏「文档」而非「App」
4. **6px 统一圆角** — `--bd-radius: 6px`，按钮、输入框、代码块、卡片一致
5. **系统字体栈** — `-apple-system → Segoe UI → Noto Sans`，不加载 Web Font，零网络成本
6. **语义元素全覆盖** — `hgroup`、`menu`、`aside`、`figure`+`figcaption`、`details`/`summary` 都有专门样式（不是只做 h1-h6 + p + a）
7. **导航用 `<menu>`** — 菜单不用 `<ul class="nav">`，直接 `<menu>` + `<li>`，靠标签语义而非类名
8. **mods 可分拆** — `styles/@root`、`styles/forms`、`styles/tables`… 每块独立 CSS，官方支持只打包用到的部分

## 关键 Token

| Token | 值 | 说明 |
|-------|-----|------|
| `--palette-1` | `#0969da` | 浅色强调蓝（GitHub 蓝） |
| `--palette-2` | `#4493f8` | 深色强调蓝 |
| `--palette-3` | `#1f2328` | 正文近黑 |
| `--palette-4` | `#656d76` | 次要文字灰 |
| `--palette-5` | `#ddf4ff` | 浅蓝底块（选中/highlight） |
| `--palette-6` | `#e6edf3` | 近白文字（深色底上） |
| `--palette-7` | `#010409` | 品牌近黑底 |
| `--palette-8` | `#8250df` | 紫色（active/visited） |
| `--palette-9` | `#d1242f` | 危险红 |
| `--font-family-primary` | `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif` | 系统字体栈 |
| `--font-size-base` | `18px` | 基准字号（偏大） |
| `--border-radius` | `6px` | 全站统一圆角 |

## 配色板

```
#0969da  #4493f8  #8250df  #d1242f      ← 强调蓝 / 深色强调 / 紫 / 危险红
#1f2328  #656d76                        ← 正文 / 次要文字
#ddf4ff  #e6edf3  #010409               ← 浅蓝底 / 近白 / 品牌近黑
```

## 适合

GitHub 风格技术文档、Markdown 转出来的内容站、要明暗切换的静态页面、想只引几 KB 样式就成型的原型。做「工程师看着顺眼」的页面最省事。

## 来源

- **仓库**: [lowlighter/matcha](https://github.com/lowlighter/matcha) (1942 ⭐)
- **Demo**: [matcha.mizu.sh](https://matcha.mizu.sh)
- **License**: MIT — 作者 lowlighter，2024-05 建仓
- **技术**: 纯 CSS（`styles/*/mod.css` 模块化源码 → 按需构建），无 JS
