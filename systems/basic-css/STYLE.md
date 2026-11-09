---
name: Basic.css
source:
  url: https://github.com/vladocar/Basic.css
  demo: https://vladocar.github.io/Basic.css/
  type: theme-css
  author: vladocar
  license: MIT
one_liner: 8 个变量的 classless 起步文件 — system-ui 正文 + 8px 圆角 + 单一蓝强调 #0074d9，靠 section 嵌套就能搭出 flex 网格
tags: [classless, minimal, sans, grid, responsive, dark-mode]
---

# Basic.css

> **「Classless CSS Starter File」** —— vladocar 2020 年的起步文件，核心只有 8 个自定义属性（`--sans` `--mono` `--c1..--c5` `--m1` `--rc`），压缩后约 1KB。
> 卖点不是排版精细度，而是**拿嵌套 `<section>` 当网格层**：`section` 里放 `section` 就成了 flex 子项，不写任何 class 也能排出卡片阵列。

## 视觉特征

1. **单一品牌蓝** — `--c1: #0074d9`（经典 flat 蓝），按钮/链接/强调全用它，其余靠黑灰拉开层级
2. **8px 圆角 + 8px 间距** — `--rc: 8px`、`--m1: 8px`，官网卡片就是这个圆角
3. **system-ui 正文**，行高 1.6，`--mono` 走 SFMono / Consolas 栈
4. **`section` 嵌套 = flex 网格** — `section > section` 自动成为栅格单元，官方叫「Flex Grid without classes」
5. **暗色靠变量翻转** — `prefers-color-scheme: dark` 里只改 `--c2:#333`、`--c3:#1e1f20`，其余规则复用
6. **可一键关圆角** — `--rc: 0px` 就整站变直角
7. **体积优先** — 1KB 级库，宁少样式不多依赖

## 关键 Token

| Token | 值 | 说明 |
|-------|-----|------|
| `--c1` | `#0074d9` | 品牌蓝强调 |
| `--c2` | `#eeeeee` | 浅底块（暗色下变 `#333`） |
| `--c3` | `#ffffff` | 卡片/内容底（暗色下变 `#1e1f20`） |
| `--c4` | `#000000` | 正文黑 |
| `--c5` | `#ffffff` | 反差白（按钮字） |
| `--m1` | `8px` | 基础间距单位 |
| `--rc` | `8px` | 统一圆角 |
| `--sans` | `system-ui, -apple-system, …` | 正文栈（含 1em/1.6） |
| `--mono` | `SFMono-Regular, Consolas, …` | 等宽栈 |

## 配色板

```
#0074d9                                  ← 品牌蓝
#000000  #eeeeee  #ffffff                ← 正文 / 浅底 / 卡片底
#333333  #1e1f20                         ← 暗色底两级
```

## 适合

快速原型、卡片式介绍页、单个 landing、不想碰 class 的小站点 —— 想要「一眼看着专业」又懒得写 CSS 的场合。

## 来源

- **仓库**: [vladocar/Basic.css](https://github.com/vladocar/Basic.css) (685 ⭐)
- **Demo**: [vladocar.github.io/Basic.css](https://vladocar.github.io/Basic.css/)
- **License**: MIT — 作者 vladocar，2020 建仓
- **技术**: 纯 CSS（`css/basic.css` + `basic.min.css` + `mobile.css` + `css/theme/*`），无 JS
