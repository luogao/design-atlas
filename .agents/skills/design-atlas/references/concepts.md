# Design Atlas — 术语表 & 概念

## 来源类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `aggregator` | 聚合仓库（多个子风格） | retro-design-system (53) |
| `component-lib` | 组件库/设计系统 | NES.css, 98.css, 7.css |
| `theme-css` | 主题 CSS（纯样式覆盖） | cyberpunk-css |
| `design-tokens` | 纯 token 集 | (计划中) |

## 在设计对话中使用的好句式

- "用 **Windows 98** 的风格做这个表单——#c0c0c0 灰色背景、凸起边框、MS Sans Serif 字体。"
- "这个页面走**新粗野主义**路线——粗黑边框、硬阴影、黄底黑字。"
- "赛博朋克风：霓虹黄底、青色高亮、锯齿字体。"
- "**NES.css 像素风**：Press Start 2P 字体、4px 粗边框、NES 调色板。"

## Token 命名惯例

- CSS 自定义属性: `--surface`, `--dialog-blue`, `--button-highlight`
- SCSS 变量: `$font-family`, `$border-size`
- 7.css 命名: `--w7-el-bg`, `--w7-el-bd`, `--w7-el-grad`
- NES.css maps: `$default-colors-hover`, `$error-colors-normal`
