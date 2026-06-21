#!/usr/bin/env python3
"""
Design Atlas Ingestion Agent
============================
Automatically discover, analyze, and ingest design style sources into
the Design Atlas repository.

Usage:
  python3 collector/ingest.py --repo https://github.com/user/repo
  python3 collector/ingest.py --repo https://github.com/user/repo --demo https://user.github.io/repo/
  python3 collector/ingest.py --aggregator https://github.com/user/collection-repo

Phases:
  1. SOURCE DETECTION — Determine source type (aggregator, component-lib, theme-css)
  2. TOKEN EXTRACTION — Extract design tokens based on detected format
  3. SCREENSHOT — Capture demo/preview with Playwright
  4. STYLE GENERATION — Create STYLE.md + tokens.css
  5. MANIFEST UPDATE — Add to manifest.json
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


def read_file(path):
    """Read file content as string."""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

# ─── Configuration ───
BASE_DIR = Path(__file__).resolve().parent.parent
VENDOR_DIR = BASE_DIR / '_vendor'
SYSTEMS_DIR = BASE_DIR / 'systems'
SCREENSHOT_DIR = VENDOR_DIR / 'screenshots'
MANIFEST_PATH = BASE_DIR / 'manifest.json'

# ─── Source Type Detection ───

def detect_source_type(repo_path):
    """
    Inspect the cloned repo to determine its type.
    Returns a dict with type, subsources, and detection metadata.
    """
    type_info = {
        'type': 'unknown',
        'confidence': 0,
        'subsources': [],
        'detection_signals': []
    }
    
    # Check: is it an aggregator with multiple style directories?
    style_dirs = find_aggregator_styles(repo_path)
    if len(style_dirs) >= 3:
        type_info['type'] = 'aggregator'
        type_info['confidence'] = 0.95
        type_info['subsources'] = style_dirs
        type_info['detection_signals'].append(f'Found {len(style_dirs)} style directories')
        return type_info
    
    # Check for SCSS gui/ + themes/ structure (themed SCSS like XP.css/7.css)
    if has_dir(repo_path, 'gui') and has_dir(repo_path, 'themes') or \
       has_file(repo_path, 'gui', '_variables.scss'):
        type_info['type'] = 'component-lib'
        type_info['token_format'] = 'themed-scss'
        type_info['confidence'] = 0.9
        type_info['detection_signals'].append('gui/ + themes/ SCSS structure detected')
        type_info['subsources'] = get_scss_subsources(repo_path)
        return type_info
    
    # Check for SCSS base/ components/ structure
    if has_dir(repo_path, 'scss') and (
        has_dir(repo_path / 'scss', 'base') or has_dir(repo_path / 'scss', 'components')
    ):
        type_info['type'] = 'component-lib'
        type_info['token_format'] = 'scss'
        type_info['confidence'] = 0.85
        type_info['detection_signals'].append('SCSS modular structure detected')
        type_info['subsources'] = get_scss_subsources(repo_path)
        return type_info
    
    # Check for single style.css with :root variables
    css_files = find_css_files(repo_path)
    for f in css_files:
        content = read_file(f)
        if ':root' in content:
            root_vars = extract_root_css_vars(content)
            if len(root_vars) >= 5:
                type_info['type'] = 'component-lib'
                type_info['token_format'] = 'css-vars'
                type_info['confidence'] = 0.8
                type_info['detection_signals'].append(
                    f'{f.name}: {len(root_vars)} CSS custom properties found'
                )
                type_info['subsources'] = [{
                    'id': repo_path.name.lower().replace('.', '-'),
                    'name': repo_path.name,
                    'css_file': str(f),
                    'tokens': root_vars
                }]
                return type_info
    
    # Check for SCSS $variables
    scss_files = find_scss_files(repo_path)
    for f in scss_files:
        content = read_file(f)
        vars = extract_scss_vars(content)
        if len(vars) >= 5:
            type_info['type'] = 'theme-css' if len(vars) < 20 else 'component-lib'
            type_info['token_format'] = 'scss-vars'
            type_info['confidence'] = 0.7
            type_info['detection_signals'].append(
                f'{f.name}: {len(vars)} SCSS variables found'
            )
            type_info['subsources'] = [{
                'id': repo_path.name.lower().replace('.', '-'),
                'name': repo_path.name,
                'css_file': str(f),
                'tokens': vars
            }]
            return type_info
    
    # Last resort: single CSS file
    css_files = find_css_files(repo_path, depth=2)
    if css_files:
        type_info['type'] = 'theme-css'
        type_info['token_format'] = 'raw-css'
        type_info['confidence'] = 0.5
        type_info['detection_signals'].append(f'{len(css_files)} CSS files found')
        type_info['subsources'] = [{
            'id': repo_path.name.lower().replace('.', '-'),
            'name': repo_path.name,
            'css_file': str(css_files[0]),
            'tokens': {}
        }]
        return type_info
    
    return type_info


def find_aggregator_styles(repo_path):
    """Find subdirectories containing index.html + style.css — typical aggregator pattern."""
    style_dirs = []
    for item in sorted(repo_path.iterdir()):
        if item.is_dir():
            has_html = (item / 'index.html').exists()
            has_css = bool(list(item.glob('*.css')))
            if has_html and has_css:
                style_dirs.append({
                    'path': str(item),
                    'name': item.name,
                    'id': item.name.lower().replace(' ', '-').replace('_', '-')
                })
    return style_dirs


def has_dir(base, name):
    return (base / name).is_dir()


def has_file(base, *parts):
    return (base / Path(*parts)).is_file()


def find_css_files(repo_path, depth=1):
    """Find CSS files up to given directory depth."""
    for pattern in ['*.css', '*.min.css']:
        if depth == 1:
            matches = list(repo_path.glob(pattern))
        else:
            matches = list(repo_path.rglob(pattern))
        if matches:
            return matches
    return []


def find_scss_files(repo_path):
    """Find SCSS variable/entry files."""
    # Look for common SCSS structure patterns
    patterns = [
        repo_path / 'scss' / 'base' / '_variables.scss',
        repo_path / 'gui' / '_variables.scss',
    ]
    for p in patterns:
        if p.exists():
            return [p]
    
    # Fallback: search for SCSS files with $variable definitions
    results = []
    for f in repo_path.rglob('*.scss'):
        if f.is_file():
            content = read_file(f)
            if re.search(r'\$[\w-]+\s*:', content):
                results.append(f)
                if len(results) >= 3:
                    break
    return results


def get_scss_subsources(repo_path):
    """For SCSS component libraries, find the individual style subsystems."""
    # If themed (XP.css/7.css): each theme is a subsource
    themes_dir = repo_path / 'themes'
    if themes_dir.is_dir():
        subsources = []
        for theme_dir in sorted(themes_dir.iterdir()):
            if theme_dir.is_dir() and theme_dir.stem not in ('node_modules', '.git'):
                subsources.append({
                    'id': f'{repo_path.name.lower()}-{theme_dir.stem}',
                    'name': f'{repo_path.name} ({theme_dir.stem})',
                    'theme': theme_dir.stem,
                    'path': str(theme_dir),
                })
        return subsources
    
    # Single component library — just return one subsource
    return [{
        'id': repo_path.name.lower().replace('.', '-'),
        'name': repo_path.name,
        'path': str(repo_path),
    }]


# ─── Token Extraction ───

def extract_root_css_vars(css_text):
    """Extract :root CSS custom properties."""
    tokens = {}
    for root_match in re.finditer(r':root\s*\{([^}]+)\}', css_text, re.DOTALL):
        block = root_match.group(1)
        for m in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', block):
            tokens[m.group(1)] = m.group(2).strip()
    return tokens


def extract_scss_vars(scss_text):
    """Extract SCSS $variables (non-map)."""
    tokens = {}
    for m in re.finditer(r'\$([\w-]+)\s*:\s*([^;{\n]+);', scss_text):
        value = re.sub(r'\s*!(?:default|global)$', '', m.group(2).strip()).strip()
        if value.startswith('$') or value.startswith('('):
            continue
        tokens[f'${m.group(1)}'] = value
    
    # Also extract map values (e.g., $default-colors: (normal: #fff, ...))
    for map_match in re.finditer(r'\$([\w-]+)\s*:\s*\(([^)]+)\)', scss_text, re.DOTALL):
        map_name = map_match.group(1)
        map_body = map_match.group(2)
        for pair in re.finditer(r'(\w+)\s*:\s*(#[0-9a-fA-F]+)', map_body):
            tokens[f'${map_name}-{pair.group(1)}'] = pair.group(2)
    
    return tokens


def extract_tokens_unified(css_text):
    """Extract tokens from any CSS/SCSS input — handles CSS vars + SCSS vars."""
    tokens = extract_root_css_vars(css_text)
    scss = extract_scss_vars(css_text)
    tokens.update(scss)
    return tokens


def generate_tokens_css(tokens, name='Design System'):
    """Convert extracted tokens to tokens.css file."""
    lines = [f'/* {name} — Design Tokens */', '/* Auto-extracted by Design Atlas Ingestion Agent */', ':root {']
    for k in sorted(tokens.keys()):
        lines.append(f'  {k}: {tokens[k]};')
    lines.append('}')
    return '\n'.join(lines) + '\n'


def select_key_tokens(tokens, max_count=10):
    """Select the most representative tokens for STYLE.md."""
    priority_keywords = [
        'color', 'surface', 'bg', 'background', 'font', 'border', 'spacing',
        'primary', 'link', 'dialog', 'shadow', 'red', 'blue', 'green',
        'yellow', 'orange', 'black', 'white', 'text'
    ]
    
    key_tokens = {}
    for k in sorted(tokens.keys()):
        lower = k.lower()
        if re.match(r'.*color-[0-9A-F]{2}$', k):
            continue  # Skip NES full palette indices
        if any(p in lower for p in priority_keywords):
            key_tokens[k] = tokens[k]
            if len(key_tokens) >= max_count:
                break
    
    if len(key_tokens) < 8:
        for k in sorted(tokens.keys()):
            if k not in key_tokens:
                key_tokens[k] = tokens[k]
                if len(key_tokens) >= max_count:
                    break
    return key_tokens


# ─── Screenshot ───

def take_screenshot(url, output_path, viewport_width=1200, viewport_height=800):
    """Capture a demo page screenshot using Playwright."""
    try:
        import subprocess
        script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const page = await browser.newPage({{
        viewport: {{ width: {viewport_width}, height: {viewport_height} }},
        deviceScaleFactor: 2
    }});
    await page.goto('{url}', {{ waitUntil: 'networkidle', timeout: 30000 }});
    await page.waitForTimeout(1500);
    await page.screenshot({{ path: '{output_path}', type: 'png' }});
    await browser.close();
    console.log('OK');
}})();
"""
        temp_script = os.path.join(tempfile.gettempdir(), 'screenshot.js')
        with open(temp_script, 'w') as f:
            f.write(script)
        result = subprocess.run(
            ['node', temp_script],
            capture_output=True, text=True, timeout=60
        )
        os.unlink(temp_script)
        return result.returncode == 0
    except Exception as e:
        print(f"  Screenshot error: {e}", file=sys.stderr)
        return False


# ─── STYLE.md Generation ───

def generate_style_md(subsources, type_info, source_info):
    """Generate a STYLE.md file for a system."""
    repo_name = source_info.get('name', 'Unknown')
    repo_url = source_info.get('repo', '')
    demo_url = source_info.get('demo', '')
    
    # Auto-generate descriptions
    tokens = subsources[0].get('tokens', {}) if subsources else {}
    key_tokens = select_key_tokens(tokens)
    
    token_table = '| Token | 值 |\n|-------|---|\n'
    for k in list(key_tokens.keys())[:10]:
        token_table += f'| `{k}` | `{tokens[k]}` |\n'
    if not key_tokens:
        token_table = '*（此系统使用内联 CSS 类名，未定义显式设计 token）*\n'
    
    one_liner = f'{repo_name} — 设计系统'
    
    style_md = f'''---
name: {repo_name}
source:
  url: {repo_url}
  demo: {demo_url or ""}
  type: {type_info.get('type', 'unknown')}
one_liner: {one_liner}
---

# {repo_name}

> 由 Design Atlas 收录 Agent 自动生成。
> 源：{repo_url}
> Demo：{demo_url or '未提供'}

## 设计 Token

{token_table}
## 来源

- **仓库**: [{repo_url}]({repo_url})
- **Demo**: [{demo_url}]({demo_url or repo_url})
- **类型**: {type_info.get('type', 'unknown')}
'''
    
    return style_md, one_liner


# ─── Manifest Operations ───

def load_manifest():
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def save_manifest(manifest):
    # Check if source already exists
    new_sources = []
    new_systems = []
    
    for source in manifest['sources']:
        pass  # Keep existing
    
    manifest['count'] = len(manifest['systems'])
    manifest['updated'] = '2026-06-21'
    
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


# ─── Category Helper ───

def suggest_category(tags, name, type_info):
    """Suggest a category based on project name, tags, and type."""
    name_lower = name.lower()
    
    category_map = {
        'os-interfaces': ['win98', 'win95', 'windows', 'macos', 'os x', 'system 7', 'xp', 'luna', 'aero', '7.css', '98.css', 'os/2', 'aqua'],
        'terminal-tui': ['terminal', 'crt', 'dos', 'tui', 'ibm', 'ansi', 'monospace', 'console', 'xterm'],
        'gaming': ['nes', 'game', '8bit', 'pixel', 'retro-game', 'ps1', 'gameboy', 'arcade', 'rpg'],
        'design-movements': ['bauhaus', 'swiss', 'memphis', 'brutalist', 'neobrutalism', 'art-deco', 'modernism'],
        'web-eras': ['geocities', 'web 2.0', 'flat', 'glassmorphism', 'frutiger', 'vaporwave'],
        'retro-futurism': ['cyberpunk', 'synthwave', 'outrun', 'y2k', 'tron', 'matrix', 'cassette', 'futurism'],
        'print-craft': ['risograph', 'duotone', 'blueprint', 'cad', 'grid', 'print', 'newsletter'],
        'art': ['pop', 'op art', 'art', 'minimal', 'contemporary']
    }
    
    for cat, keywords in category_map.items():
        for kw in keywords:
            if kw in name_lower:
                return cat
    
    return 'web-eras'  # Default


def suggest_tags(name, category, type_info):
    """Suggest tags based on name, category, and type."""
    tags = []
    name_lower = name.lower()
    
    mood_map = {
        'os-interfaces': 'nostalgic',
        'terminal-tui': 'dry',
        'gaming': 'playful',
        'design-movements': 'bold',
        'web-eras': 'warm',
        'retro-futurism': 'futuristic',
        'print-craft': 'minimal',
        'art': 'bold'
    }
    
    tags.append(mood_map.get(category, 'minimal'))
    
    # Detect palette indicators from name
    palette_map = {
        'cyberpunk': 'neon',
        'synthwave': 'neon',
        'brutalist': 'high-contrast',
        'neobrutalism': 'high-contrast',
        'pastel': 'pastel',
        'duotone': 'duotone',
        'monochrome': 'monochrome',
    }
    
    for keyword, palette in palette_map.items():
        if keyword in name_lower:
            tags.append(palette)
            break
    else:
        tags.append('duotone')
    
    return tags


# ─── Main Pipeline ───

def ingest_source(repo_url, demo_url=None, output_dir=None):
    """Main ingestion pipeline."""
    print(f"\n{'='*60}")
    print(f"  Design Atlas Ingestion Agent")
    print(f"  Source: {repo_url}")
    print(f"{'='*60}\n")
    
    # Phase 1: Clone or use existing
    repo_name = repo_url.rstrip('/').split('/')[-1]
    temp_dir = tempfile.mkdtemp(prefix='design-atlas-')
    
    try:
        # Clone
        print(f"📦 Cloning {repo_name}...")
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, str(temp_dir / repo_name)],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode != 0:
            print(f"❌ Clone failed: {result.stderr}")
            return False
        
        repo_path = Path(temp_dir) / repo_name
        print(f"✅ Cloned to {repo_path}\n")
        
        # Phase 2: Detect source type
        print("🔍 Phase 1: Source Type Detection...")
        type_info = detect_source_type(repo_path)
        print(f"  Type: {type_info['type']}")
        print(f"  Format: {type_info.get('token_format', 'N/A')}")
        print(f"  Confidence: {int(type_info['confidence'] * 100)}%")
        for signal in type_info['detection_signals']:
            print(f"  Signal: {signal}")
        
        if type_info['type'] == 'unknown' or type_info['confidence'] < 0.3:
            print("❌ Cannot reliably determine source type. Skipping.")
            return False
        
        print()
        
        # Phase 3: Token Extraction
        print("🔧 Phase 2: Token Extraction...")
        subsources = type_info['subsources']
        for sub in subsources:
            if 'css_file' in sub:
                with open(sub['css_file']) as f:
                    content = f.read()
                tokens = extract_tokens_unified(content)
                sub['tokens'] = tokens
                print(f"  📊 {sub['name']}: {len(tokens)} tokens extracted")
        
        print()
        
        # Phase 4: Screenshot (if demo URL provided)
        print("📸 Phase 3: Screenshot...")
        if demo_url:
            # Screenshot naming
            slug = repo_name.lower().replace('.', '-')
            screenshot_path = SCREENSHOT_DIR / f'{slug}.png'
            success = take_screenshot(demo_url, str(screenshot_path))
            if success:
                print(f"  ✅ Screenshot: {screenshot_path}")
            else:
                print(f"  ⚠️  Screenshot failed")
                screenshot_path = None
        else:
            print(f"  ⚠️  No demo URL provided, skipping screenshot")
            screenshot_path = None
        
        print()
        
        slug = repo_name.lower().replace('.', '-').replace('_', '-')
        
        # Phase 5: STYLE Generation
        print("📝 Phase 4: STYLE.md Generation...")
        source_info = {
            'name': repo_name,
            'repo': repo_url,
            'url': repo_url,
            'demo': demo_url or '',
        }
        
        for i, sub in enumerate(subsources):
            sys_id = sub.get('id', f'{slug}-{i}')
            sys_name = sub.get('name', repo_name)
            sys_dir = SYSTEMS_DIR / sys_id
            
            if sys_dir.exists():
                print(f"  ⚠️  System '{sys_id}' already exists. Backing up...")
            
            os.makedirs(sys_dir, exist_ok=True)
            
            # Write tokens.css
            tokens = sub.get('tokens', {})
            tokens_css = generate_tokens_css(tokens, sys_name)
            with open(sys_dir / 'tokens.css', 'w') as f:
                f.write(tokens_css)
            print(f"  📄 {sys_dir / 'tokens.css'}")
            
            # Write STYLE.md
            style_md, one_liner = generate_style_md([sub], type_info, source_info)
            with open(sys_dir / 'STYLE.md', 'w', encoding='utf-8') as f:
                f.write(style_md)
            print(f"  📄 {sys_dir / 'STYLE.md'}")
            
            # Copy screenshot
            if screenshot_path and screenshot_path.exists():
                shutil.copy2(str(screenshot_path), str(sys_dir / 'preview.png'))
                print(f"  🖼️  {sys_dir / 'preview.png'}")
        
        print()
        
        # Phase 6: Manifest Update
        print("📋 Phase 5: Manifest Update...")
        manifest = load_manifest()
        
        # Add source entry
        source_entry = {
            'id': repo_name.lower().replace('.', '-').replace('_', '-'),
            'name': repo_name,
            'repo': repo_url,
            'author': repo_url.rstrip('/').split('/')[-2] if 'github.com' in repo_url else '',
            'type': type_info['type'],
            'license': 'MIT',
            'description': f'{type_info["type"]} — {len(subsources)} styles',
            'url': demo_url or repo_url,
            'count': len(subsources)
        }
        
        # Check for duplicate
        existing = [s for s in manifest['sources'] if s['repo'] == repo_url]
        if existing:
            print(f"  ℹ️  Source '{repo_url}' already in manifest")
        else:
            manifest['sources'].append(source_entry)
            print(f"  ✅ Added source: {repo_name}")
        
        # Add system entries
        for i, sub in enumerate(subsources):
            sys_id = sub.get('id', f'{slug}-{i}')
            sys_name = sub.get('name', repo_name)
            
            # Generate per-system description
            _, sys_one_liner = generate_style_md([sub], type_info, source_info)
            
            sys_entry = {
                'id': sys_id,
                'name': sys_name,
                'category': suggest_category(sys_id, sys_name, type_info),
                'tags': suggest_tags(sys_name, suggest_category(sys_id, sys_name, type_info), type_info),
                'source': {
                    'type': type_info['type'],
                    'repo': repo_url,
                    'author': source_entry['author'],
                    'license': 'MIT'
                },
                'palette': list(sub.get('tokens', {}).values())[:6] or ['#333', '#666', '#999', '#ccc', '#fff'],
                'tokens': f'systems/{sys_id}/tokens.css',
                'style_md': f'systems/{sys_id}/STYLE.md',
                'demo_url': demo_url or repo_url,
                'preview': f'systems/{sys_id}/preview.png',
                'one_liner': sys_one_liner if i == 0 else f'{sys_name} — 设计风格',
                'best_for': '多种场景'
            }
            
            existing = [s for s in manifest['systems'] if s['id'] == sys_id]
            if existing:
                print(f"  ℹ️  System '{sys_id}' already in manifest")
            else:
                manifest['systems'].append(sys_entry)
                print(f"  ✅ Added system: {sys_name} ({sys_id})")
        
        manifest['count'] = len(manifest['systems'])
        manifest['updated'] = '2026-06-21'
        
        with open(MANIFEST_PATH, 'w') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"  📋 manifest.json updated")
        
        print()
        print(f"{'='*60}")
        print(f"  ✅ Ingestion complete!")
        print(f"  Source: {repo_name}")
        print(f"  Type: {type_info['type']}")
        print(f"  Systems added: {len(subsources)}")
        print(f"{'='*60}")
        
        return True
        
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description='Design Atlas Ingestion Agent')
    parser.add_argument('--repo', required=True, help='GitHub repository URL')
    parser.add_argument('--demo', help='Demo site URL (for screenshot)')
    parser.add_argument('--output', help='Output directory (default: systems/ in project)')
    
    args = parser.parse_args()
    
    success = ingest_source(args.repo, args.demo, args.output)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
