---
name: marx
source:
  url: https://github.com/mblode/marx
  demo: https://blode.co/marx
  type: theme-css
  author: Matthew Blode
  license: MIT
one_liner: 零 class 的极简重置 — 零特异性让你自己的 CSS 永远覆盖，oklch 令牌自动明暗切换，裸 HTML 直接变可读页面
tags: [classless, minimal, reset, oklch, dark-mode]
---

# marx

> **「classless CSS reset（perfect for Communists）」**：官方 slogan 就在自嘲——没有 JS、没有 class、只有裸 CSS。
> 2015 年建仓、2026 年重写为 oklch + `light-dark()` 版本，1710 ⭐。它和其他 classless 框架最大的差别是**零特异性**：所有选择器都是 `:where(...)` 包裹，特异性为 0，你自己的任意一条 CSS 都能盖过它——这是它敢叫 "reset" 的原因。

## 视觉特征

1. **零特异性（zero specificity）** — 全部选择器套 `:where()`，`element {}` 级别，你的样式永远赢；当「底座」用不会打架
2. **纯 oklch 配色** — `--marx-primary: oklch(54.6% 0.245 262.9)`（≈ `#165dfc`），阈值统一、亮度可控，不是随手写死的 hex
3. **`light-dark()` 自动明暗** — 每个颜色变量写两遍：静态兜底值 + `light-dark(浅, 深)`；`color-scheme: light dark` 一开，暗色零 JS 实现
4. **一个蓝走全场** — 按钮、链接、focus ring 全部 `--marx-primary` 蓝，只有红/绿/黄做反馈语义
5. **0.5rem 圆角 + 42rem 行宽** — `--marx-measure: 42rem`（约 672px）是排版宽度上限，长文不会摊成一行 1400px
6. **系统字体栈 + 1.5 行高** — `-apple-system → Segoe UI → Roboto`，行高 `--marx-leading: 1.5`，节奏变量化
7. **无阴影** — 深度靠 `oklch(0% 0 0 / 12%)` 半透明边框，不用 box-shadow，界面很平很静
8. **小尺寸优先** — 官方定位 "any project (namely small ones)"，不做栅格、不做组件层，只调 HTML 默认样式

## 关键 Token

| Token | 值 | 说明 |
|-------|-----|------|
| `--palette-1` | `#165dfc` | 主蓝（按钮/链接/ring） |
| `--palette-2` | `#1447e6` | 主蓝 hover 深一档 |
| `--palette-3` | `#f6f7f8` | 浅灰表面（surface） |
| `--palette-4` | `#1c1f24` | 深色模式背景 |
| `--palette-5` | `#e7000b` | 危险红 |
| `--palette-6` | `#139948` | 成功绿 |
| `--palette-7` | `#d78d00` | 警告黄 |
| `--palette-8` | `#f4ce23` | mark 高亮黄（40% 混透明） |
| `--font-family-primary` | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", Arial, sans-serif` | 系统字体栈 |
| `--font-size-base` | `1rem` | 基准字号 |
| `--border-radius` | `0.5rem` | 全站统一圆角 |
| `--box-shadow` | `none` | 明确不用阴影 |

## 配色板

```
#165dfc  #1447e6                        ← 主蓝 / hover 深蓝
#e7000b  #139948  #d78d00  #f4ce23      ← 危险 / 成功 / 警告 / 高亮
#f6f7f8  #1c1f24                        ← 浅表面 / 深色背景
```

## 适合

小项目、个人主页、README 级营销页、内部工具——尤其是「已经有自己的 CSS，只想找个不抢戏的底座」的场景。要做零维护的暗色支持，`light-dark()` 这套是最干净的写法参考。

## 来源

- **仓库**: [mblode/marx](https://github.com/mblode/marx) (1710 ⭐)
- **Demo**: [blode.co/marx](https://blode.co/marx)
- **License**: MIT — 作者 Matthew Blode，2015-04 建仓
- **技术**: 纯 CSS，源码 `src/_tokens.css` / `_base.css` / `_typography.css` 等模块，产出 `css/marx.css` + `.min.css`
