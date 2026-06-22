---
name: Water.css
source:
  url: https://github.com/kognise/water.css
  demo: https://watercss.kognise.dev/
  type: theme-css
  author: Kognise
  license: MIT
one_liner: Classless CSS 框架 — 纯语义 HTML → 干净现代文档风格，零 class 写入
tags: [minimal, elegant, sans-serif, spacious, documentation]
---

# Water.css

> **Classless CSS** 的开创者之一：把纯 `<link rel="stylesheet">` 到一个 `<html>` 文件上，"just add water"——水一样自然。
> 不需要写任何 class 名，纯 HTML 标签就能出干净现代的文档页面。

## 视觉特征

1. **Zero-class** — 没有 `.btn` `.card` `.container`，只用 `<h1>` `<p>` `<button>` `<input>` 等原生标签
2. **双模式** — `light.css`（白底）和 `dark.css`（暗底），自动应用
3. **蓝色链接** `#0076d1` — 经典 Web 蓝色链接，像 90s 互联网但更现代
4. **大字号** `16px` base + `1.5` line-height — 侧重可读性
5. **灰底代码块** — `<code>` 用 `#efefef` 背景，干净不晃眼
6. **表单自动美化** — `<input>` `<select>` `<button>` 自带圆角、边框、悬停态
7. **越少越好的哲学**——与其他 classless 框架相比，Water.css 是最克制的那一个

## 关键 Token

| Token | 值 | 说明 |
|-------|---|------|
| `--water-bg-body` | `#ffffff` | 页背景 |
| `--water-text-main` | `#363636` | 正文色 |
| `--water-links` | `#0076d1` | 链接蓝 |
| `--water-border` | `#dbdbdb` | 边框灰 |
| `--water-button-base` | `#d0cfcf` | 按钮底色 |
| `--water-dark-bg-body` | `#1b1b1b` | 暗色背景 |

## 配色板

```
#ffffff  #efefef  #f7f7f7            ← 背景
#363636  #000000  #70777f            ← 文字
#0076d1  #0096bf                     ← 链接蓝
#d0cfcf  #9b9b9b                     ← 按钮灰
#dbdbdb                              ← 边框
#39a33c  #ffff00                     ← 高亮
```

## 来源

- **仓库**: [kognise/water.css](https://github.com/kognise/water.css) (8.2k ⭐)
- **Demo**: [watercss.kognise.dev](https://watercss.kognise.dev/)
- **License**: MIT
- **技术**: 纯 CSS（无 JS 无构建）
- **大小**: ~4KB minified
