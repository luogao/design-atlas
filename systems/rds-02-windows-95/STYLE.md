     1|---
     2|name: "Windows 95"
     3|category: "os-interfaces"
     4|year: 1995
     5|tags: [windows, bevel, chrome, classic]
     6|source:
     7|  type: "aggregator"
     8|  repo: "https://github.com/novusgfx/retro-design-system"
     9|  author: "NovusGFX"
    10|  license: "MIT"
    11|  original_path: "styles/02-windows-95/"
    12|palette_colors: ["#008080", "#c0c0c0", "#dfdfdf", "#ffffff", "#808080", "#000000", "#000080"]
    13|---
    14|
    15|# Windows 95
    16|
## 一句话

3D 凸起边框 + Teal 桌面背景——定义了整个 90 年代的桌面计算体验。

## 设计哲学

Windows 95 的视觉语言建立在"用边框模拟物理按钮"的核心隐喻上：每个可交互元素都有 3D 凸起或凹陷的 bevel 效果，通过亮边（上左白）和暗边（下右灰）制造立体感。配色以灰色系统为主（chrome 灰），配合标志性的 Teal 桌面。字体用 MS Sans Serif，小字号，紧凑间距。整个设计传达的是"这是一个你可以按下去的东西"——所有的视觉线索都在告诉你什么是可交互的。
    24|
    25|## 关键 Token
    26|
    27|| Token | 值 | 用途 |
    28||-------|-----|------|
    29|<!-- 从 tokens.css 填充关键变量 -->
    30|
## Do / Don't

- ✅ 所有按钮用 bevel 边框（outset 凸起 / inset 凹陷）
- ✅ 系统字体 Tahoma/MS Sans Serif
- ✅ 1px 硬边框，不要模糊阴影
- ✅ 窗口用标题栏 + 内容区结构

- ❌ 不要用圆角（Win95 一切都是直角）
- ❌ 不要用半透明/毛玻璃
- ❌ 不要用渐变色填充按钮
- ❌ 不要用现代字体如 Inter/Geist
    38|
## 适用场景

复古软件 UI、Retro web 游戏、怀旧主题 landing page、Y2K 复古项目
    42|
    43|## 参考
    44|
    45|- 原仓库：https://github.com/novusgfx/retro-design-system
    46|- 在线预览：https://novusgfx.github.io/retro-design-system/styles/02-windows-95/
    47|