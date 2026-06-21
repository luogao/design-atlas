---
name: "Style Name"
category: "category-id"          # 从 manifest.json categories[].id 中选
year: 2000                        # 风格起源年份
tags: ["tag1", "tag2"]           # 自由标签
mood: ["minimal", "bold"]        # 从 tag_dimensions.mood 中选
palette: ["monochrome"]          # 从 tag_dimensions.palette 中选
typography: ["sans-serif"]       # 从 tag_dimensions.typography 中选
density: ["spacious"]            # 从 tag_dimensions.density 中选
best_for: ["landing-page"]       # 从 tag_dimensions.best_for 中选

source:
  type: "single-style"            # aggregator | single-style | component-lib | design-tokens
  repo: "https://github.com/..."  # 原始仓库 URL
  author: "Author Name"           # 原作者
  license: "MIT"                  # 许可证
  original_path: ""               # 如果是聚合仓库的子风格，填子路径

palette_colors: ["#hex1", "#hex2", "#hex3"]  # 主要颜色
---

# {Style Name}

## 一句话

{一句话概括这个风格的核心特征}

## 设计哲学

{这个风格的核心信念是什么、为什么好看、设计原则是什么}

## 关键 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--color-primary` | #hex | 主色 |
| `--color-bg` | #hex | 背景 |
| `--font-display` | Font Name | 标题字体 |
| `--radius` | Npx | 圆角 |
| `--spacing` | Npx | 间距基准 |

## Do / Don't

✅ 要做的：
- {具体做法}

❌ 不要做的：
- {具体禁忌}

## 适用场景

- ✅ {适合的场景}
- ❌ {不适合的场景}

## 参考

- 原仓库：{repo URL}
- 设计哲学来源：{如果有}
