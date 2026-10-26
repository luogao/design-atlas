---
name: wing
source:
  url: https://github.com/kbrsh/wing
  demo: https://kbrsh.github.io/wing
  type: theme-css
  author: Kabir Shah
  license: MIT
one_liner: 2KB 极简样式底座 — 系统字体栈 + 一个蓝色链接，几乎不用记 class
tags: [minimal, classless, system-font, light, utility]
---

# wing

> **2KB 的极简样式底板**：作者 Kabir Shah 把它定位成「任何项目的 boilerplate stylesheet」。
> README 原话：*almost everything is styled automatically, without the need for learning specific classes* —— 语义标签直接出样式，只有少数工具类。

## 视觉特征

1. **系统字体栈打底** — `-apple-system, BlinkMacSystemFont, Avenir Next, Segoe UI, Roboto, …`，不引外部字体，观感随操作系统走
2. **一个蓝色强调** `#0062ff` — 链接与交互态统一用这个蓝，接近系统蓝
3. **语义色齐全但克制** — 红 `#ff1500` / 琥珀 `#ffbf00` / 绿 `#00b30f` 只出现在状态（错误、警告、成功）里，不当装饰
4. **灰阶三分** — `#111111` 正文、`#a7a7a7` 次要、`#f5f5f5` 底，界面几乎只有灰 + 一个蓝
5. **近直角** — `border-radius: 2px`，几乎方，硬朗
6. **16px 基准** — 不做 62.5% 换算，直接用浏览器默认 16px 作为 1rem
7. **样式自动落到裸标签** — 表格、表单、代码块不用 class 也有样子；需要布局时才用工具类

## 关键 Token

| Token | 值 | 说明 |
|-------|---|------|
| `--palette-1` | `#111111` | 正文黑 |
| `--palette-2` | `#a7a7a7` | 次要灰 |
| `--palette-3` | `#f5f5f5` | 页面浅底 |
| `--palette-4` | `#0062ff` | 强调蓝（链接） |
| `--palette-5` | `#ff1500` | 错误红 |
| `--palette-6` | `#ffbf00` | 警告琥珀 |
| `--palette-7` | `#00b30f` | 成功绿 |
| `--font-size-base` | `16px` | 基准字号 |
| `--border-radius` | `2px` | 近直角 |

## 配色板

```
#0062ff                                    ← 强调蓝（链接 / 交互）
#111111  #a7a7a7                           ← 正文 / 次要文字
#f5f5f5  #e7e7e7  #d7d7d7                  ← 底色 / 分隔 / 边框
#ff1500  #ffbf00  #00b30f                  ← 错误 / 警告 / 成功
```

## 适合

技术博客、极简产品页、内部工具。想要「装上一行 link 就有体面排版、又不想要框架感」时最合适。

## 来源

- **仓库**: [kbrsh/wing](https://github.com/kbrsh/wing) (2.0k ⭐)
- **Demo**: [kbrsh.github.io/wing](https://kbrsh.github.io/wing)
- **License**: MIT — Kabir Shah
- **技术**: SCSS → dist CSS，2KB（min+gzip），无 JS
