---
name: spcss
source:
  url: https://github.com/susam/spcss
  demo: https://susam.github.io/spcss/
  type: theme-css
  author: susam
  license: MIT
one_liner: 1KB 级极小 classless 样式表 — 40em 阅读宽度 + Helvetica 正文 + 经典 Web 蓝链接，裸 HTML 直接能读，自带暗色
tags: [classless, minimal, sans, monochrome, single-file, dark-mode]
---

# spcss

> **「写普通 HTML，得到一张能看的页面」** —— susam 2020 年放的极简 classless 样式表，未压缩 1.7KB、min 版 1.1KB，只有 `sp.css` 一个文件，零 JS、零 Web Font。
> 定位不是「设计系统」而是一层**默认排版兜底**：给 README 级页面、个人笔记、小工具输出页一个不难看的默认样式。

## 视觉特征

1. **经典 Web 配色** — 正文 `#333`，链接 `#00e`（那一代浏览器默认蓝）、hover `#03f`、visited `#518`、active `#e00`；代码 `#050` 绿、`samp` 用 `#730` 赭色
2. **40em 阅读宽度** — `body { max-width: 40em; margin: 0 auto; padding: 0 1em }`，居中单栏，不做网格
3. **Helvetica/Arial 正文**，1.5 行高，标题 1.2 紧行高，全部系统字体
4. **标题自带 `#` 锚点** — `h1 a:empty:before { content: "#" }`，hover 才显示；写 `<h2>标题 <a></a></h2>` 就有可点锚点
5. **引用块左侧竖线** — `blockquote` 粗 `#ccc` 左边框 + `#eee` 底，不加装饰性引号
6. **表格只给细边框** — `thin solid #999`，无斑马纹，适合数据而非仪表盘
7. **原生暗色** — `prefers-color-scheme: dark` 整段重定义：底 `#111`、字 `#bbb`、链接 `#9bf`、代码 `#9c6`

## 关键 Token

| Token | 值 | 说明 |
|-------|-----|------|
| `--palette-1` | `#333333` | 正文 |
| `--palette-2` | `#0000ee` | 链接蓝（经典 Web Blue） |
| `--palette-3` | `#0033ff` | hover 蓝 |
| `--palette-4` | `#551188` | visited 紫 |
| `--palette-5` | `#ee0000` | active 红 |
| `--palette-6` | `#005500` | 代码绿 |
| `--palette-7` | `#773300` | samp 赭 |
| `--palette-8` | `#eeeeee` | 代码块底 |
| `--palette-9` | `#cccccc` | 引用竖线 |
| `--palette-10` | `#999999` | 表格边框 |
| `--palette-11` | `#111111` | 暗色底 |
| `--palette-12` | `#bbbbbb` | 暗色正文 |
| `--font-family-primary` | `helvetica, arial, sans-serif` | 正文栈 |
| `--measure` | `40em` | 最大阅读宽度 |

## 配色板

```
#333333  #0000ee  #0033ff  #551188  #ee0000   ← 正文 / 链接四态
#005500  #773300  #eeeeee  #cccccc  #999999   ← 代码 / samp / 底块 / 线条
#111111  #bbbbbb                              ← 暗色底 / 暗色正文
```

## 适合

README 转的页面、个人笔记、脚本输出报告、CLI 工具附带的说明页 —— 任何「只需要不难看」而不需要一套设计语言的场景。

## 来源

- **仓库**: [susam/spcss](https://github.com/susam/spcss) (969 ⭐)
- **Demo**: [susam.github.io/spcss](https://susam.github.io/spcss/)（GitHub Pages 在无头浏览器里会卡住，本预览改用本地 demo + 官方 `sp.css` 截图）
- **License**: MIT — 作者 susam，2020 建仓
- **技术**: 单文件纯 CSS，无构建、无 JS；CDN 路径 `https://cdn.jsdelivr.net/npm/spcss`
