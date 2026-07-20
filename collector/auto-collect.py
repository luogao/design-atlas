#!/usr/bin/env python3
"""
Design Atlas — Auto Collector Script
=====================================
Weekly cron job that:
1. Scans GitHub trending CSS repos and awesome-niche-css list (via opencli browser)
2. Filters candidates: retro/classless/artistic aesthetics, 300+ stars, not already in atlas
3. Auto-ingests qualifying repos (top 3 per run)
4. Git commit + push → Cloudflare Pages auto-deploy
"""

import json, os, re, subprocess, sys, time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE_DIR / 'manifest.json'
INGEST_SCRIPT = BASE_DIR / 'collector' / 'ingest.py'
CANDIDATE_FILE = BASE_DIR / 'collector' / 'candidates.json'
MIN_STARS = 300
OPENCLI_SESSION = 'designatlas'

# ─── Helpers ───

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def load_manifest():
    with open(MANIFEST_PATH) as f:
        return json.load(f)

def get_existing_repos(manifest):
    repos = set()
    for s in manifest['systems']:
        repo = s.get('source', {}).get('repo', '') or ''
        repos.add(repo.rstrip('/'))
    for src in manifest.get('sources', []):
        repo = src.get('repo', '') or ''
        if repo:
            repos.add(repo.rstrip('/'))
    return repos

# ─── OpenCLI Browser Helpers ───

def browser_open_session():
    """Ensure opencli browser session is alive"""
    result = subprocess.run(
        ['opencli', 'browser', OPENCLI_SESSION, 'open', 'https://github.com'],
        capture_output=True, text=True, timeout=20)
    time.sleep(2)
    return result.stdout or ''

def browser_eval(js):
    """Execute JS in opencli browser and return stdout"""
    result = subprocess.run(
        ['opencli', 'browser', OPENCLI_SESSION, 'eval', js],
        capture_output=True, text=True, timeout=30)
    return result.stdout or ''

def browser_close():
    subprocess.run(['opencli', 'browser', OPENCLI_SESSION, 'close'],
                   capture_output=True, timeout=5)

def _parse_json_lenient(out):
    """从 opencli eval 输出中提取 JSON，去掉 'Update available' / 'npm install' 等噪声行。"""
    if not out:
        return None
    lines = [l for l in out.splitlines()
             if l.strip() and 'Update available' not in l and 'npm install' not in l]
    cleaned = '\n'.join(lines).strip()
    if not cleaned:
        return None
    # 直接解析整段；失败则逐行尝试（取第一个合法 JSON 行）
    try:
        return json.loads(cleaned)
    except Exception:
        for l in lines:
            l = l.strip()
            if l.startswith('{') or l.startswith('['):
                try:
                    return json.loads(l)
                except Exception:
                    continue
    return None

def _resolve_github_token():
    """获取 GitHub token 用于鉴权请求（60/hr → 5000/hr）。
    优先级：GITHUB_TOKEN / GH_TOKEN 环境变量，其次 `gh auth token`。"""
    tok = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if tok:
        return tok.strip()
    try:
        r = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return ''

_GITHUB_TOKEN = None  # lazy

def _get_github_token():
    global _GITHUB_TOKEN
    if _GITHUB_TOKEN is None:
        _GITHUB_TOKEN = _resolve_github_token()
        if _GITHUB_TOKEN:
            log("🔑 GitHub API: using authenticated requests (5000/hr)")
        else:
            log("⚠️  GitHub API: no token found, unauthenticated (60/hr) — may hit rate limit")
    return _GITHUB_TOKEN

def fetch_github_api(endpoint, retries=2):
    """通过 opencli 浏览器 eval 调用 GitHub API（绕 Clash）。
    若有 token 则带 Authorization 头（5000/hr），否则匿名（60/hr）。"""
    tok = _get_github_token()
    if tok:
        headers_js = "{'Authorization':'token " + tok + "','Accept':'application/vnd.github+json'}"
    else:
        headers_js = "{}"
    for i in range(retries + 1):
        try:
            js = (
                "(async () => {\n"
                "    var r = await fetch('https://api.github.com" + endpoint + "', {headers: " + headers_js + "});\n"
                "    var j = await r.json();\n"
                "    return JSON.stringify(j);\n"
                "})()"
            )
            out = browser_eval(js)
            j = _parse_json_lenient(out)
            if j is not None:
                return j
        except Exception:
            if i < retries:
                time.sleep(2)
    return None

def search_github(query, per_page=8):
    """GitHub Search via fetch, return parsed items or None"""
    import urllib.parse
    encoded = urllib.parse.quote(query)
    data = fetch_github_api(f"/search/repositories?q={encoded}&sort=stars&order=desc&per_page={per_page}")
    if not data:
        return None
    items = data.get('items', [])
    return items

def extract_repos_from_items(items):
    """从 GitHub API items 中提取关键字段"""
    repos = []
    seen_urls = set()
    for item in items:
        url = item.get('html_url', '').rstrip('/')
        if url in seen_urls:
            continue
        seen_urls.add(url)
        repos.append({
            'name': item.get('full_name', ''),
            'url': item.get('html_url', ''),
            'stars': item.get('stargazers_count', 0),
            'description': item.get('description', '') or '',
            'topics': item.get('topics', []),
            'demo': item.get('homepage', '') or '',
        })
    return repos

def get_stars(repo_full_name):
    data = fetch_github_api(f"/repos/{repo_full_name}")
    if not data:
        return 0
    return data.get('stargazers_count', 0)

# ─── Source 1: GitHub Search ───

def scrape_github_search():
    """GitHub Search: 视觉风格化 CSS 项目"""
    log("🔄 Searching GitHub CSS repos...")
    queries = [
        # Retro / 复古
        "retro css framework design-system",
        "retro design-system css",
        "css framework 8bit pixel nostalgic",
        # Game / 游戏
        "game ui css framework",
        "arcade css retro",
        "rpg ui css",
        # 极客 / 终端
        "terminal css framework",
        "monospace css framework",
        # 自然 / 手绘
        "hand-drawn css framework",
        "sketchy css framework",
        # 印刷/纸张
        "newspaper css framework",
        "zine css style",
        # 粗野/建筑
        "brutalist web design",
        "geometry css framework",
        # 玻璃态/新拟态
        "glassmorphism css",
        "neumorphism css",
        # 科幻/赛博
        "cyberpunk css framework",
        "scifi css design",
        # 极简/排版
        "classless css framework",
        "minimal design system",
        "pure css art grid",
        # 设计系统/设计Token
        "design system css retro",
        "design token css theme",
        "retro design tokens",
    ]
    all_repos = []
    seen_urls = set()
    for q in queries:
        items = search_github(q, per_page=8)
        if items:
            repos = extract_repos_from_items(items)
            for r in repos:
                if r['url'] not in seen_urls:
                    seen_urls.add(r['url'])
                    all_repos.append(r)
        time.sleep(1)
    log(f"  Found {len(all_repos)} unique repos")
    return all_repos

# ─── Source 2: awesome-css-frameworks (troxler) README via raw markdown ───

def scrape_awesome_css_list():
    """从 troxler/awesome-css-frameworks 的 raw markdown 提取 GitHub 链接。
    raw markdown 含完整 URL，免疫 GitHub 页面 DOM 变更（旧 selectors 已失效）。
    旧源 AMR2010M/awesome-niche-css 的 README 无任何链接，已弃用。"""
    log("🔄 Reading troxler/awesome-css-frameworks README (raw markdown)...")
    # 1) 解析默认分支
    meta = fetch_github_api("/repos/troxler/awesome-css-frameworks")
    if not meta or 'default_branch' not in meta:
        log("  ⚠ could not fetch repo meta")
        return []
    branch = meta.get('default_branch', 'master')
    # 2) 拉 raw readme（尝试常见文件名）
    body = ''
    for fname in ('readme.md', 'README.md'):
        js = (
            f"(async()=>{{var r=await fetch("
            f"'https://raw.githubusercontent.com/troxler/awesome-css-frameworks/{branch}/{fname}');"
            f"if(!r.ok) return 'FAIL_'+r.status; return await r.text()}})()"
        )
        out = browser_eval(js)
        out = '\n'.join(l for l in out.splitlines()
                        if l.strip() and 'Update available' not in l and 'npm install' not in l).strip()
        if out and not out.startswith('FAIL_'):
            body = out
            break
    if not body:
        log("  ⚠ could not fetch readme body")
        return []
    # 3) 提取唯一 GitHub repo URL
    urls = []
    seen = set()
    for m in re.finditer(r'https?://github\.com/[\w.\-]+/[\w.\-]+', body):
        url = m.group().rstrip('/').rstrip(').,;')
        if '/topics/' in url or '/topic/' in url or '/awesome' in url.lower():
            continue
        if url in seen:
            continue
        seen.add(url)
        urls.append(url)
    repos = []
    for url in urls:
        parts = url.replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            repos.append({
                'name': f"{parts[0]}/{parts[1]}",
                'url': url,
                'source': 'troxler/awesome-css-frameworks',
            })
    log(f"  Found {len(repos)} repo links in readme")
    return repos

# ─── Filtering ───

def is_visual_repo(repo_info):
    """判断是否视觉风格化系统（vs 普通 UI 框架/工具库）"""
    desc = (repo_info.get('description', '') or '')
    topics = ' '.join(repo_info.get('topics', []))
    text = desc + ' ' + topics
    name = repo_info.get('name', '')
    text_lower = (desc + ' ' + topics + ' ' + name).lower()

    # ❌ 硬排除：非设计类 repo / 元列表（awesome-list 本身不是风格系统）
    hard_skip = [
        '反中共', '政治', 'propaganda', 'dictatorship',
        'github topic', 'awesome list', 'curated list',
        'a list of', 'list of awesome', 'awesome-css',
        'awesome niche', 'collection of',
        '动漫', 'discord', '.github community',
    ]
    if any(s in text_lower for s in hard_skip):
        return False

    # ❌ 跳过：通用 UI 框架/工具
    skip_patterns = [
        'ui library', 'ui component', 'component library',
        'utility-first', 'utility class', 'responsive grid',
        'admin template', 'admin panel',
        'wordpress', 'jekyll', 'hugo', 'gatsby', 'next.js', 'react',
        'tailwind plugin', 'bootstrap theme',
        'starter', 'boilerplate',
        'atomic css', 'design system implementation',
    ]

    # ✅ 视觉风格关键词
    vision_signals = [
        'retro', 'vintage', 'pixel', '8-bit', '8bit', 'nes',
        'vaporwave', 'cyberpunk', 'brutalist', 'neon', 'glitch',
        'hand-drawn', 'handdrawn', 'sketchy', 'wobble', 'cartoon',
        'game ui', 'arcade', 'rpg', 'terminal ui', 'terminal theme',
        'tui', 'text-based ui', 'old-school', 'old school rpg',
        'rough', 'paper', 'glassmorphism', 'neumorphism', 'clay',
        'y2k', 'aesthetic', 'nostalgic', 'chunky', 'dot matrix',
        'typewriter', 'wireframe', 'sketch', 'pop art',
        'bauhaus', 'swiss', 'geometry',
        'no class', 'classless', 'minimal', 'minimalist',
        'serif', 'typography', 'monospace',
        'gradient', 'duotone', 'monochrome', 'glossy',
        'win95', 'win98', 'winxp', 'mac os', 'crt', 'phosphor',
        'zine', 'newspaper', 'print style',
        'pure css', 'css art',
    ]

    has_vision = any(s in text_lower for s in vision_signals)
    has_skip = any(s in text_lower for s in skip_patterns)

    if has_vision:
        return True
    if has_skip:
        return False
    return False

# ─── Main Pipeline ───

def main():
    dry_run = '--dry-run' in sys.argv
    log(f"{'🔍 DRY RUN' if dry_run else '🚀 AUTO COLLECT'} — Design Atlas")

    manifest = load_manifest()
    existing_repos = get_existing_repos(manifest)
    log(f"Already in atlas: {len(existing_repos)} sources")

    # Open browser session
    browser_open_session()

    candidates = []

    # Source 1: GitHub Search
    search_results = scrape_github_search()
    new_from_search = [r for r in search_results
                       if r['url'].rstrip('/') not in existing_repos
                       and r['stars'] >= MIN_STARS
                       and is_visual_repo(r)]
    log(f"Search total: {len(search_results)}, qualified new: {len(new_from_search)}")
    candidates.extend(new_from_search)

    # Source 2: awesome-css-frameworks (troxler)
    niche = scrape_awesome_css_list()
    new_niche = []
    existing_in_candidates = {c['url'] for c in candidates}
    for r in niche:
        if r['url'].rstrip('/') in existing_repos:
            continue
        if r['url'] in existing_in_candidates:
            continue
        # 一次 API 调用拿到 stars + description + topics + homepage
        data = fetch_github_api(f"/repos/{r['name']}")
        if not data:
            continue
        info = {
            'name': r['name'],
            'url': r['url'],
            'source': r.get('source', ''),
            'stars': data.get('stargazers_count', 0),
            'description': data.get('description', '') or '',
            'topics': data.get('topics', []),
            'demo': data.get('homepage', '') or '',
        }
        # 用真实 description+topics 判定视觉风格（旧代码传空 desc + 假 topic，导致几乎全被误杀）
        if info['stars'] >= MIN_STARS and is_visual_repo(info):
            new_niche.append(info)
    log(f"Niche new eligible: {len(new_niche)}")
    candidates.extend(new_niche)

    # Close browser session
    browser_close()

    # Sort by stars
    candidates.sort(key=lambda r: r.get('stars', 0), reverse=True)

    # Save & report
    log(f"\n{'='*50}")
    log(f"📋 CANDIDATE SUMMARY: {len(candidates)} new")
    log(f"{'='*50}")
    for r in candidates[:15]:
        log(f"  ⭐{r.get('stars', '?'):>6}  {r['name']:<40} {(r.get('description','') or '')[:60]}")
    if len(candidates) > 15:
        log(f"  ... and {len(candidates)-15} more")

    CANDIDATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CANDIDATE_FILE, 'w') as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    log(f"\nCandidates saved to collector/candidates.json")

    if dry_run or not candidates:
        log(f"\n{'DRY RUN — no ingestion' if dry_run else 'No candidates'}")
        return

    # Auto-ingest top 3
    MAX_INGEST = 3
    ingested = 0
    log(f"\n{'='*50}")
    log(f"🚀 Auto-ingesting up to {MAX_INGEST}...")
    log(f"{'='*50}")

    for r in candidates[:MAX_INGEST]:
        demo = r.get('demo') or f"https://{r['name'].split('/')[0]}.github.io/{r['name'].split('/')[1]}/"
        log(f"\nIngesting {r['name']} ({r.get('stars', '?')}⭐)...")
        result = subprocess.run(
            ['python3', str(INGEST_SCRIPT), '--repo', r['url'], '--demo', demo],
            capture_output=True, text=True, timeout=120, cwd=str(BASE_DIR))
        if result.returncode == 0:
            log(f"  ✅ OK")
            ingested += 1
            subprocess.run(['git', 'add', '-A'], cwd=str(BASE_DIR), capture_output=True)
            subprocess.run(
                ['git', 'commit', '-m', f'feat: auto-collect {r["name"]} ({r.get("stars",0)}⭐)'],
                cwd=str(BASE_DIR), capture_output=True)
        else:
            log(f"  ❌ {result.stdout[-200:] if result.stdout else 'no output'}")

    if ingested > 0:
        log(f"\n↗️  Pushing...")
        subprocess.run(['git', 'push'], cwd=str(BASE_DIR), capture_output=True)
        log("✅ Cloudflare Pages deployed")

    log(f"\n{'='*50}")
    log(f"📊 {ingested}/{len(candidates)} ingested")
    log(f"{'='*50}")

if __name__ == '__main__':
    main()
