#!/usr/bin/env python3
"""
Design Atlas MCP Server
======================
Model Context Protocol server for the Design Atlas design system collection.

Provides tools for AI coding agents to:
- Search and discover design styles
- Get detailed design guidance (philosophy, Do/Don't, tokens)
- Apply design tokens to projects
- Find the best style for a given UI task

Transports: stdio (default), streamable HTTP (optional)
Compatible with: Claude Code, Cursor, Codex, and any MCP client
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

# ─── Project Base ───
BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE_DIR / 'manifest.json'
SYSTEMS_DIR = BASE_DIR / 'systems'

# ─── Manifest Cache ───
_manifest_cache = None


def load_manifest():
    """Load and cache the manifest."""
    global _manifest_cache
    if _manifest_cache is None:
        with open(MANIFEST_PATH, 'r') as f:
            _manifest_cache = json.load(f)
    return _manifest_cache


def get_categories():
    """Get all categories."""
    m = load_manifest()
    return m.get('categories', [])


def get_sources():
    """Get all sources."""
    m = load_manifest()
    return m.get('sources', [])


def get_system(system_id: str) -> Optional[dict]:
    """Get a single system by ID."""
    m = load_manifest()
    for s in m.get('systems', []):
        if s['id'] == system_id:
            return s
    return None


def search_systems(query: str = '', category: str = '', tags: list[str] = None) -> list[dict]:
    """Search systems by query, category, and tags."""
    m = load_manifest()
    systems = m.get('systems', [])
    tags = tags or []
    results = []

    for s in systems:
        score = 0

        # Category filter
        if category and s.get('category') != category:
            continue

        # Text search
        if query:
            q = query.lower()
            name = s.get('name', '').lower()
            one_liner = s.get('one_liner', '').lower()
            best_for = s.get('best_for', '').lower()
            sys_tags = ' '.join(s.get('tags', [])).lower()

            haystack = f'{name} {one_liner} {best_for} {sys_tags}'
            if q in haystack:
                score += 10
            else:
                # Fuzzy scoring: count word matches
                words = q.split()
                match_count = sum(1 for w in words if w in haystack)
                if match_count == 0:
                    continue
                score += match_count

        # Tag filter
        if tags:
            sys_tags = s.get('tags', [])
            match = all(t in sys_tags for t in tags)
            if not match:
                continue
            score += len(tags)

        # Default score for empty query
        if score == 0 and not query and not tags:
            score = 1

        results.append({
            'id': s['id'],
            'name': s['name'],
            'category': s.get('category', ''),
            'category_name': get_category_name(s.get('category', '')),
            'tags': s.get('tags', []),
            'one_liner': s.get('one_liner', ''),
            'best_for': s.get('best_for', ''),
            'source_type': s.get('source', {}).get('type', ''),
            'source_author': s.get('source', {}).get('author', ''),
            'demo_url': s.get('demo_url', ''),
            'palette': s.get('palette', []),
            'score': score,
        })

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def get_category_name(category_id: str) -> str:
    """Get human-readable category name."""
    cats = get_categories()
    for c in cats:
        if c['id'] == category_id:
            return c.get('name', category_id)
    return category_id


def read_style_md(system_id: str) -> Optional[str]:
    """Read STYLE.md content for a system."""
    s = get_system(system_id)
    if not s:
        return None
    style_path = s.get('style_md', '')
    if not style_path:
        return None
    full_path = BASE_DIR / style_path
    if not full_path.exists():
        return None
    return full_path.read_text(encoding='utf-8')


def read_tokens_css(system_id: str) -> Optional[str]:
    """Read tokens.css for a system."""
    s = get_system(system_id)
    if not s:
        return None
    tokens_path = s.get('tokens', '')
    if not tokens_path:
        return None
    full_path = BASE_DIR / tokens_path
    if not full_path.exists():
        return None
    return full_path.read_text(encoding='utf-8')


def parse_style_md(md_text: str) -> dict:
    """Parse STYLE.md to extract structured design guidance."""
    result = {
        'design_philosophy': '',
        'guidelines': {'do': [], 'dont': []},
        'best_for': '',
        'tokens_table': '',
    }

    # Extract design philosophy (text between ## 设计哲学 and next heading)
    m = re.search(r'## 设计哲学\n\n(.+?)(?=\n## |\Z)', md_text, re.DOTALL)
    if m:
        result['design_philosophy'] = m.group(1).strip()

    # Extract Do items
    do_section = re.search(r'## ✅ 应该做的\n\n(.+?)(?=\n## |\Z)', md_text, re.DOTALL)
    if do_section:
        do_items = re.findall(r'-\s*✅\s*(.+?)(?:\n|$)', do_section.group(1))
        if not do_items:
            do_items = re.findall(r'-\s*(.+?)(?:\n|$)', do_section.group(1))
        result['guidelines']['do'] = [item.strip() for item in do_items]

    # Extract Don't items
    dont_section = re.search(r'## ❌ 不应该做的\n\n(.+?)(?=\n## |\Z)', md_text, re.DOTALL)
    if dont_section:
        dont_items = re.findall(r'-\s*❌\s*(.+?)(?:\n|$)', dont_section.group(1))
        if not dont_items:
            dont_items = re.findall(r'-\s*(.+?)(?:\n|$)', dont_section.group(1))
        result['guidelines']['dont'] = [item.strip() for item in dont_items]

    # Extract Best For
    m = re.search(r'## 适用场景\n\n(.+?)(?=\n## |\Z)', md_text, re.DOTALL)
    if m:
        items = re.findall(r'-\s*(.+?)(?:\n|$)', m.group(1))
        result['best_for'] = items

    # Extract token table
    m = re.search(r'## 关键 Token\n\n(.+?)(?=\n## |\Z)', md_text, re.DOTALL)
    if m:
        result['tokens_table'] = m.group(1).strip()

    return result


def get_ideal_style_for_task(task_description: str) -> list[dict]:
    """
    Given a task description, find the ideal design styles.
    Matches based on best_for keywords and design philosophy overlap.
    """
    td = task_description.lower()
    all_systems = search_systems()
    scored = []

    # Keyword scoring
    keywords = {
        'game': ['game', 'gaming', '8bit', 'pixel', 'retro-game', 'arcade'],
        'dashboard': ['dashboard', 'tool', 'data', 'management', 'admin'],
        'landing': ['landing', 'homepage', 'marketing', 'product', 'hero'],
        'blog': ['blog', 'article', 'writing', 'reading', 'newsletter'],
        'creative': ['portfolio', 'creative', 'studio', 'artist', 'designer'],
        'retro': ['retro', 'vintage', 'nostalgic', 'classic', 'old school'],
        'futuristic': ['futuristic', 'cyberpunk', 'sci-fi', 'neon', 'tech'],
        'clean': ['clean', 'minimal', 'modern', 'sleek', 'professional'],
        'dark': ['dark', 'night', 'matrix', 'terminal', 'hacker'],
        'bright': ['bright', 'colorful', 'playful', 'bold', 'fun'],
    }

    for s in all_systems:
        score = 0
        match_reasons = []

        for kw_group, kw_list in keywords.items():
            if any(w in td for w in kw_list):
                # Check if this system's best_for or tags match
                best_for = str(s.get('best_for', '')).lower()
                sys_tags = ' '.join(s.get('tags', [])).lower()
                combined = best_for + ' ' + sys_tags

                tag_matches = sum(1 for w in kw_list if w in combined)
                if tag_matches > 0:
                    score += tag_matches * 3
                    match_reasons.append(kw_group)

        if score > 0:
            scored.append({
                **s,
                'relevance_score': score,
                'match_reasons': match_reasons,
            })

    scored.sort(key=lambda x: x['relevance_score'], reverse=True)
    return scored[:10]


# ─── MCP Protocol Implementation ───

def send_json(message: dict):
    """Send a JSON-RPC message to stdout."""
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + '\n')
    sys.stdout.flush()


def read_json() -> dict:
    """Read a JSON-RPC message from stdin."""
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line.strip())


def handle_tools_list() -> list[dict]:
    """Return the list of available tools."""
    return [
        {
            "name": "search_styles",
            "description": "搜索设计风格。基于查询词、分类和标签多维搜索。返回匹配的设计系统列表，含名称和一句话描述。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词（支持中文/英文，搜索名称、描述、标签）"
                    },
                    "category": {
                        "type": "string",
                        "description": "过滤分类（如: os-interfaces, gaming, design-movements, retro-futurism 等）",
                        "enum": ["os-interfaces", "terminal-tui", "gaming", "design-movements",
                                 "web-eras", "retro-futurism", "print-craft", "art", ""]
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "过滤标签（如: mood:playful, palette:neon, typography:pixel 等）"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回最大数量（默认 10）",
                        "default": 10
                    }
                }
            }
        },
        {
            "name": "get_style_detail",
            "description": "获取某个设计风格的详细信息。包含设计哲学、Do/Don't 准则、设计 Token 表格、适用场景等结构化数据。Agent 可以根据这些信息来生成对应风格的 UI。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "设计系统 ID（如: ext-nes-css, ext-98css, rds-01-mac-system-7）"
                    }
                },
                "required": ["id"]
            }
        },
        {
            "name": "get_tokens",
            "description": "获取某个设计风格的原始 CSS 设计 Token（CSS 自定义属性或 SCSS 变量）。可直接注入到项目的 CSS 文件中使用。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "设计系统 ID"
                    }
                },
                "required": ["id"]
            }
        },
        {
            "name": "get_guidance",
            "description": "(智能推荐) 根据任务描述，推荐最匹配的设计风格。Agent 在接到一个 UI 开发任务时，先调用这个工具获取视觉指引，再开始写代码。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "任务描述（如: 做一个游戏排行榜页面、一个赛博朋克风的 Dashboard、一个创业公司 Landing Page）"
                    }
                },
                "required": ["task_description"]
            }
        },
        {
            "name": "list_categories",
            "description": "列出所有设计风格分类和统计信息。Agent 可以先用这个了解整体分类结构，再进行精确搜索。",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "apply_style",
            "description": "应用设计风格到项目。返回该风格的 CSS Token 注入 + 关键使用准则。Agent 调用后可以直接将结果写到项目的 CSS 文件。",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "设计系统 ID"
                    }
                },
                "required": ["id"]
            }
        },
    ]


def handle_tools_call(name: str, arguments: dict) -> dict:
    """Route tool calls."""
    if name == "search_styles":
        return handle_search_styles(arguments)
    elif name == "get_style_detail":
        return handle_get_style_detail(arguments)
    elif name == "get_tokens":
        return handle_get_tokens(arguments)
    elif name == "get_guidance":
        return handle_get_guidance(arguments)
    elif name == "list_categories":
        return handle_list_categories()
    elif name == "apply_style":
        return handle_apply_style(arguments)
    else:
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
            "isError": True
        }


def handle_search_styles(args: dict) -> dict:
    query = args.get('query', '')
    category = args.get('category', '')
    tags = args.get('tags', None)
    limit = args.get('limit', 10)

    results = search_systems(query, category, tags)[:limit]

    if not results:
        return {
            "content": [{"type": "text", "text": "未找到匹配的设计风格。"}]
        }

    lines = []
    for r in results:
        tag_str = ', '.join(r['tags']) if r['tags'] else ''
        category_str = r.get('category_name', '')
        lines.append(f"### {r['name']}")
        lines.append(f"- ID: `{r['id']}`")
        lines.append(f"- 分类: {category_str}")
        lines.append(f"- 来源: {r.get('source_type', '')}/{r.get('source_author', '')}")
        lines.append(f"- 描述: {r.get('one_liner', '')}")
        if tag_str:
            lines.append(f"- 标签: {tag_str}")
        lines.append("")

    return {
        "content": [{"type": "text", "text": '\n'.join(lines).strip()}]
    }


def handle_get_style_detail(args: dict) -> dict:
    system_id = args.get('id', '')
    s = get_system(system_id)
    if not s:
        return {
            "content": [{"type": "text", "text": f"设计系统 '{system_id}' 未找到。"}],
            "isError": True
        }

    # Try to get detailed guidance from STYLE.md
    md = read_style_md(system_id)
    parsed = parse_style_md(md) if md else {}

    lines = [
        f"# {s['name']}",
        f"**分类:** {get_category_name(s.get('category', ''))}",
        f"**ID:** `{s['id']}`",
    ]

    if parsed.get('design_philosophy'):
        lines.append(f"\n## 设计哲学\n{parsed['design_philosophy']}")

    if s.get('one_liner'):
        lines.append(f"\n> {s['one_liner']}")

    if parsed.get('guidelines', {}).get('do'):
        lines.append(f"\n## ✅ 应该做的")
        for item in parsed['guidelines']['do']:
            lines.append(f"- {item}")

    if parsed.get('guidelines', {}).get('dont'):
        lines.append(f"\n## ❌ 不应该做的")
        for item in parsed['guidelines']['dont']:
            lines.append(f"- {item}")

    if s.get('best_for'):
        lines.append(f"\n## 适用场景\n{s['best_for']}")

    if parsed.get('tokens_table'):
        lines.append(f"\n## 关键 Token\n{parsed['tokens_table']}")

    if s.get('palette'):
        palette_str = ', '.join(s['palette'])
        lines.append(f"\n## 调色板\n{palette_str}")

    demo_url = s.get('demo_url', '')
    if demo_url:
        lines.append(f"\n## 演示\n{demo_url}")

    return {
        "content": [{"type": "text", "text": '\n'.join(lines).strip()}]
    }


def handle_get_tokens(args: dict) -> dict:
    system_id = args.get('id', '')
    tokens = read_tokens_css(system_id)

    if tokens is None:
        # Fallback: generate from STYLE.md table
        s = get_system(system_id)
        if s:
            palette = s.get('palette', [])
            if palette:
                tokens_lines = [
                    "/* Design Atlas — Auto-generated from palette */",
                    ":root {"
                ]
                for i, color in enumerate(palette):
                    tokens_lines.append(f"  --atlas-color-{i}: {color};")
                tokens_lines.append("}")
                tokens = '\n'.join(tokens_lines)

    if not tokens:
        return {
            "content": [{"type": "text", "text": f"设计系统 '{system_id}' 无可用 token。"}],
            "isError": True
        }

    return {
        "content": [
            {"type": "text", "text": f"/* Design Atlas — {system_id} / Design Tokens */\n{tokens}"}
        ]
    }


def handle_get_guidance(args: dict) -> dict:
    task = args.get('task_description', '')
    if not task:
        return {
            "content": [{"type": "text", "text": "请输入任务描述。"}],
            "isError": True
        }

    results = get_ideal_style_for_task(task)
    if not results:
        return {
            "content": [{"type": "text", "text": f"未找到与「{task}」匹配的风格。试试用 search_styles 手动搜索。"}]
        }

    lines = [
        f"## 为「{task}」推荐的设计风格\n"
    ]

    for r in results[:5]:
        reasons = ', '.join(r.get('match_reasons', []))
        lines.append(f"### {r['name']}（{r.get('category_name', '')}）")
        lines.append(f"ID: `{r['id']}`")
        if r.get('one_liner'):
            lines.append(f"> {r['one_liner']}")
        if reasons:
            lines.append(f"匹配原因: {reasons}")
        lines.append("")

    return {
        "content": [{"type": "text", "text": '\n'.join(lines).strip()}]
    }


def handle_list_categories() -> dict:
    cats = get_categories()
    lines = ["## 设计风格分类\n"]

    # Count per category
    m = load_manifest()
    cat_counts = {}
    for s in m.get('systems', []):
        c = s.get('category', '')
        cat_counts[c] = cat_counts.get(c, 0) + 1

    for c in cats:
        count = cat_counts.get(c['id'], 0)
        lines.append(f"### {c['name']}（{c.get('name_cn', '')}）")
        lines.append(f"  ID: `{c['id']}`")
        lines.append(f"  风格数: {count}")
        lines.append(f"  说明: {c.get('description', '')}")
        lines.append("")

    return {
        "content": [{"type": "text", "text": '\n'.join(lines).strip()}]
    }


def handle_apply_style(args: dict) -> dict:
    """
    Combines style detail + tokens + generation guidance into one
    ready-to-apply response for an AI coding agent.
    """
    system_id = args.get('id', '')
    s = get_system(system_id)
    if not s:
        return {
            "content": [{"type": "text", "text": f"设计系统 '{system_id}' 未找到。"}],
            "isError": True
        }

    md = read_style_md(system_id)
    parsed = parse_style_md(md) if md else {}
    tokens = read_tokens_css(system_id)

    lines = [
        f"# 应用 {s['name']} 到项目\n",
        f"## 设计哲学\n{parsed.get('design_philosophy', s.get('one_liner', ''))}",
    ]

    if parsed.get('guidelines', {}).get('do'):
        lines.append("\n## ✅ 使用准则")
        for item in parsed['guidelines']['do'][:4]:
            lines.append(f"- {item}")

    if parsed.get('guidelines', {}).get('dont'):
        lines.append("\n## ❌ 避免")
        for item in parsed['guidelines']['dont'][:3]:
            lines.append(f"- {item}")

    if tokens:
        lines.append(f"\n## CSS Token 注入\n在你的 CSS 中引入：\n```css\n/* 引入 {s['name']} 设计 token */\n{_shorten_tokens(tokens)}\n```\n将上述 `:root` 代码块添加到你的 `styles.css` 或 `globals.css` 顶部，即可在项目中使用这些 CSS 变量。")

    if s.get('demo_url'):
        lines.append(f"\n## 参考 Demo\n打开 {s['demo_url']} 查看实际效果。")

    return {
        "content": [{"type": "text", "text": '\n'.join(lines).strip()}]
    }


def _shorten_tokens(tokens_css: str) -> str:
    """Shorten tokens CSS to first 15 lines for display."""
    lines = tokens_css.split('\n')
    if len(lines) > 18:
        lines = lines[:17] + ['  /* ... 更多 token ... */', '}']
    return '\n'.join(lines)


# ─── Main Server Loop ───

def main():
    """MCP stdio server main loop."""
    # Signal server startup
    send_json({
        "jsonrpc": "2.0",
        "id": 0,
        "result": {
            "serverInfo": {
                "name": "design-atlas",
                "version": "1.0.0"
            },
            "capabilities": {
                "tools": {
                    "listChanged": False
                }
            }
        }
    })

    while True:
        msg = read_json()
        if msg is None:
            break

        method = msg.get('method', '')
        msg_id = msg.get('id')
        params = msg.get('params', {})

        if method == 'tools/list':
            send_json({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": handle_tools_list()
                }
            })

        elif method == 'tools/call':
            tool_name = params.get('name', '')
            tool_args = params.get('arguments', {})
            result = handle_tools_call(tool_name, tool_args)
            send_json({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": result
            })

        elif method == 'resources/list':
            send_json({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "resources": []
                }
            })

        elif method == 'resources/read':
            send_json({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "contents": []
                }
            })

        else:
            # Unknown method - respond with empty result to avoid blocking
            if msg_id:
                send_json({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {}
                })


if __name__ == '__main__':
    main()
