     1|---
     2|name: "CRT Phosphor Terminal"
     3|category: "terminal-tui"
     4|year: 1980
     5|tags: [terminal, green, scanline, phosphor]
     6|source:
     7|  type: "aggregator"
     8|  repo: "https://github.com/novusgfx/retro-design-system"
     9|  author: "NovusGFX"
    10|  license: "MIT"
    11|  original_path: "styles/09-crt-phosphor/"
    12|palette_colors: ["#001a00", "#33ff33", "#1a8a1a", "#aaffaa", "#ffb400"]
    13|---
    14|
    15|# CRT Phosphor Terminal
    16|
## 一句话

荧光绿在黑暗中发光——早期 CRT 显示器的磷光美学。

## 设计哲学

CRT Phosphor 再现了早期单色显示器（尤其是 P1 绿色磷光管）的视觉效果。核心美学是：暗背景上的高对比度发光文字，配合扫描线、磷光辉散和像素化边缘。这不是简单的"绿字黑底"，而是一种有深度、有质感的光线——文字仿佛真的在发光，边缘有自然的辉散。传递的是 60-80 年代大型机终端、示波器、早期雷达屏幕的技术浪漫主义。
    24|
    25|## 关键 Token
    26|
    27|| Token | 值 | 用途 |
    28||-------|-----|------|
    29|<!-- 从 tokens.css 填充关键变量 -->
    30|
## Do / Don't

- ✅ 等宽字体（必须）
- ✅ 文字加 text-shadow 实现辉光效果
- ✅ 扫描线 overlay 增加真实感
- ✅ 限制颜色到单一磷光色 + 黑底

- ❌ 不要用多色（磷光管是单色的）
- ❌ 不要用圆角
- ❌ 不要用平滑字体渲染（要 pixelated）
- ❌ 不要加花哨的 CSS 动画
    38|
## 适用场景

终端模拟器 UI、黑客/安全主题界面、监控/日志 dashboard、复古科技产品页
    42|
    43|## 参考
    44|
    45|- 原仓库：https://github.com/novusgfx/retro-design-system
    46|- 在线预览：https://novusgfx.github.io/retro-design-system/styles/09-crt-phosphor/
    47|