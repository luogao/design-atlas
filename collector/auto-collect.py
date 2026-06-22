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

def fetch_github_api(endpoint, retries=2):
    """通过 opencli 浏览器 eval 调用 GitHub API（绕 Clash）
    只提取关键字段，避免输出截断"""
    for i in range(retries + 1):
        try:
            js = f"""
(async () => {{
    var r = await fetch('https://api.github.com{endpoint}');
    var j = await r.json();
    return JSON.stringify(j);
}})()
"""
            out = browser_eval(js)
            # Attempt parse
            try:
                j = json.loads(out)
                return j
            except:
                # Maybe got a status line, try again
                pass
        except Exception as e:
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
        "retro css framework design-system",
        "classless css framework",
        "aesthetic css framework",
        "retro design-system css",
        "css framework 8bit pixel nostalgic",
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

# ─── Source 2: awesome-niche-css README ───

def scrape_niche_css_list():
    """通过 opencli 浏览器读取 awesome-niche-css README 内容"""
    log("🔄 Reading awesome-niche-css README...")
    result = subprocess.run(
        ['opencli', 'browser', OPENCLI_SESSION, 'open',
         'https://github.com/AMR2010M/awesome-niche-css'],
        capture_output=True, text=True, timeout=15)
    time.sleep(3)

    # Extract README innerText
    eval_out = subprocess.run(
        ['opencli', 'browser', OPENCLI_SESSION, 'eval',
         "document.querySelector('[data-testid=readme]')?.innerText "
         "|| document.querySelector('.readme')?.innerText || 'NOT_FOUND'"],
        capture_output=True, text=True, timeout=10)
    content = eval_out.stdout or ''

    # Parse GitHub URLs from content
    urls = set()
    for m in re.finditer(r'https://github\.com/[\w.-]+/[\w.-]+', content):
        url = m.group().rstrip('/')
        if '/topics/' not in url and '/topic/' not in url:
            urls.add(url)
    log(f"  Found {len(urls)} links")

    repos = []
    for url in urls:
        parts = url.replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            repos.append({
                'name': f"{parts[0]}/{parts[1]}",
                'url': url,
                'source': 'awesome-niche-css',
            })
    log(f"  → {len(repos)} repos")
    return repos

# ─── Filtering ───

def is_visual_repo(repo_info):
    """判断是否视觉风格化系统（vs 普通 UI 框架/工具库）"""
    text = (repo_info.get('description', '') or '') + ' ' + ' '.join(repo_info.get('topics', []))
    text_lower = text.lower()

    # Skip: generic UI libs, utilities
    skip_patterns = [
        'ui library', 'ui component', 'component library', 'ui framework',
        'utility-first', 'utility class', 'responsive grid', 'css-in-js',
        'css framework', 'admin template', 'admin panel',
        'wordpress', 'jekyll', 'hugo', 'gatsby', 'next.js', 'react',
        'tailwind plugin', 'bootstrap theme', 'design token',
        'starter', 'boilerplate', 'kit ', 'scss framework', 'sass',
        'atomic css', 'design system implementation',
    ]

    vision_signals = [
        'retro', 'vintage', 'pixel', '8-bit', '8bit', 'nes', 'vaporwave',
        'cyberpunk', 'brutalist', 'neon', 'glitch', 'hand-drawn', 'handdrawn',
        'sketchy', 'wobble', 'cartoon', 'game', 'arcade', 'terminal',
        'rough', 'paper', 'glassmorphism', 'neumorphism', 'clay', 'y2k',
        'aesthetic', 'nostalgic', 'chunky', 'dot matrix', 'typewriter',
        'wireframe', 'sketch', 'pop art', 'bauhaus', 'swiss',
        'no class', 'classless', 'minimal', 'serif', 'typography',
        'gradient', 'duotone', 'monochrome', 'glossy', 'strikethrough',
        'win95', 'win98', 'winxp', 'mac os', 'crt', 'phosphor',
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

    # Source 2: awesome-niche-css
    niche = scrape_niche_css_list()
    new_niche = []
    existing_in_candidates = {c['url'] for c in candidates}
    for r in niche:
        if r['url'].rstrip('/') in existing_repos:
            continue
        if r['url'] in existing_in_candidates:
            continue
        stars = get_stars(r['name'])
        if stars >= MIN_STARS and is_visual_repo({'description': '', 'topics': [r['name']]}):
            r['stars'] = stars
            new_niche.append(r)
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
