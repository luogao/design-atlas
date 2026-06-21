---
name: "IBM 3270 Mainframe"
category: "terminal-tui"
year: 1971
tags: [ibm, mainframe, terminal, cics]
source:
  type: "aggregator"
  repo: "https://github.com/novusgfx/retro-design-system"
  author: "NovusGFX"
  license: "MIT"
  original_path: "styles/27-ibm-3270/"
palette_colors: ["#000000", "#00d4d4", "#00d400", "#e4e4e4", "#ff3030", "#ffe84a", "#4a9cff", "#ff7aa8"]
---

# IBM 3270 Mainframe

## 一句话

绿色字 + 黑底。半个世纪的企业计算，一屏搞定。

## 设计哲学

IBM 3270 终端是大型机时代的标准——绿色磷光文字在纯黑背景上，没有鼠标，全键盘操作。设计上它极度克制：颜色编码信息（绿=正常、红=错误、蓝=高亮），布局用精确的对齐和留白。这是功能即设计的典范。

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--bg` | `#000000` | 背景 |
| `--turquoise` | `#00d4d4` | 其他 |
| `--green` | `#00d400` | 其他 |
| `--white` | `#e4e4e4` | 其他 |
| `--red` | `#ff3030` | 其他 |
| `--yellow` | `#ffe84a` | 其他 |
| `--blue` | `#4a9cff` | 其他 |
| `--pink` | `#ff7aa8` | 文字/前景 |

## Do / Don't

- ✅ 磷光绿文字 on 纯黑背景
- ✅ 颜色编码状态（绿/红/蓝/白）
- ✅ 全键盘导航设计
- ✅ 精确的列对齐

- ❌ 不要用渐变或装饰
- ❌ 不要用鼠标交互范式
- ❌ 不要用图标
- ❌ 不要超过 4-5 种文字颜色

## 适用场景

企业级终端界面、TUI 应用、高密度信息展示

## 参考

- 原仓库：https://github.com/novusgfx/retro-design-system
- 在线预览：https://novusgfx.github.io/retro-design-system/styles/3270/
