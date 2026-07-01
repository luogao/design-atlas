---
id: spiderverse-neon-lottery
title: "Spider-Man: Into the Spider-Verse"
scene: 量子彩票球
year: 2018
director: "Bob Persichetti, Peter Ramsey, Rodney Rothman"
cinematographer: "N/A (Animation — Sony Pictures Imageworks)"
---

# Spider-Verse — 量子彩票球

> *"You won't believe it's not comics."*

## 场景

多元宇宙碰撞的视觉隐喻：巨大的青色球体悬浮在黑暗中，周围散布着粉色、绿色、紫色的光球，CMYK 印刷色点风格。

## 配色

| 色名 | Hex | 占比 | 角色 |
|------|-----|------|------|
| 量子青 | `#319C9C` | 36% | 主色 |
| 墨黑 | `#060607` | 22% | 背景 |
| 青柠 | `#A8B37C` | 16% | 辅色 |
| 冰蓝 | `#73D4E0` | 14% | 辅色 |
| 紫粉 | `#9A5B78` | 11% | 点缀 |

## 分析

**配色类型：分裂互补色（Split-Complementary）** — 主色青（H≈180°）与紫粉（H≈330°）形成 150° 分裂互补关系。青柠和冰蓝是青色的类比色延伸。

**色温：冷暖并存** — 青色系是冷调（60%+），但 11% 的紫粉注入了暖意，制造了微妙的张力。

**情绪关键词：** 跃动、超现实、漫画感、多元、不确定

**设计逻辑：** Spider-Verse 的核心美学是 **CMYK 印刷色叠加**。画面模拟丝网印刷的色彩错位和荧光油墨质感。暗色背景（22%）不是纯黑而是 #060607（带极微蓝调），这避免了纯黑导致的"廉价感"。主色量子青饱和度适中（S≈55%），既有漫画鲜艳感又不刺眼。

## 应用建议

**适用场景：** 创意机构官网、游戏 UI、音乐/艺术主题站、活动页面、App 首页

**CSS Tokens:**
```css
:root {
  --cinema-bg: #060607;
  --cinema-surface: #319C9C;
  --cinema-accent: #9A5B78;
  --cinema-text: #73D4E0;
  --cinema-highlight: #A8B37C;
}
```

## Do / Don't

**Do:**
- 在暗色背景上用高饱和色块——这是漫画分镜的逻辑
- 允许色彩"越界"：让青色和粉色在边界碰撞，模拟印刷色偏
- 用硬阴影（box-shadow 无模糊）代替柔和阴影

**Don't:**
- 不要用低饱和/灰色调——这个风格的灵魂就是色彩饱和
- 不要用线性渐变——用半色调点（halftone）或实色块叠加
- 不要超过 5 种色相——色彩丰富但不是杂乱
