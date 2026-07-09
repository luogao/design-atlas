#!/usr/bin/env python3
"""
Design Atlas — 豆瓣 Top 50 电影配色采集器
==========================================
1. 用 opencli browser 打开每部电影的豆瓣剧照页（绕过反爬）
2. 抓取前 5 张剧照大图 URL
3. 下载 → k-means 聚类提取 5 色 + 比例
4. 分析配色类型/色温/明度
5. 输出 palette.json / tokens.css / COLOR_STORY.md
"""

import subprocess, json, re, time, sys, os
from pathlib import Path
from io import BytesIO
import requests
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import colorsys

BASE = Path(__file__).resolve().parent.parent
PALETTES_DIR = BASE / 'palettes'
MOVIES_JSON = Path(__file__).resolve().parent / 'douban_top50.json'
SESSION = 'atlas'
STILLS_PER_MOVIE = 5  # 每部电影取几张剧照做分析

# ── Helpers ──

def run_opencli(args, timeout=30):
    """Run opencli command, strip update footer, return stdout."""
    result = subprocess.run(
        f'opencli {args}', shell=True, capture_output=True, text=True, timeout=timeout
    )
    out = result.stdout
    # Strip update footer
    idx = out.rfind('Update available')
    if idx > 0:
        out = out[:idx]
    return out.strip()

def open_douban_stills(douban_id):
    """Open douban stills page via opencli, return list of image URLs."""
    url = f'https://movie.douban.com/subject/{douban_id}/photos?type=S'
    run_opencli(f'browser {SESSION} open "{url}"')
    time.sleep(3)
    
    js = """(() => {
      const imgs = document.querySelectorAll('.cover img');
      return JSON.stringify(Array.from(imgs).map(i => i.src));
    })()"""
    raw = run_opencli(f'browser {SESSION} eval "{js}"')
    try:
        urls = json.loads(raw)
    except:
        urls = []
    return urls

def thumb_to_large(url):
    """Convert douban thumbnail URL to large version."""
    return url.replace('/m/public/', '/l/public/')

def download_image(url, timeout=15):
    """Download image with browser-like headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://movie.douban.com/'
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    if resp.status_code == 200:
        return Image.open(BytesIO(resp.content)).convert('RGB')
    return None

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def extract_palette(img, n_colors=5):
    """K-means clustering to extract dominant colors with ratios."""
    # Resize for speed
    img_small = img.resize((200, 200), Image.LANCZOS)
    pixels = np.array(img_small).reshape(-1, 3)
    
    # K-means
    kmeans = KMeans(n_clusters=n_colors, n_init=10, random_state=42)
    labels = kmeans.fit_predict(pixels)
    
    # Count cluster sizes for ratios
    counts = np.bincount(labels, minlength=n_colors)
    total = counts.sum()
    
    # Sort by ratio descending
    order = np.argsort(-counts)
    
    palette = []
    for idx in order:
        rgb = tuple(kmeans.cluster_centers_[idx].astype(int))
        ratio = counts[idx] / total
        palette.append({
            'hex': rgb_to_hex(rgb),
            'rgb': list(rgb),
            'ratio': round(float(ratio), 4)
        })
    
    return palette

def analyze_color_scheme(palette):
    """Determine color scheme, temperature, brightness."""
    def hex_to_hsl(h):
        r, g, b = [x/255 for x in hex_to_rgb(h)]
        h_, l_, s_ = colorsys.rgb_to_hls(r, g, b)
        return h_*360, s_, l_
    
    hues = []
    for c in palette:
        h, s, l = hex_to_hsl(c['hex'])
        if s > 0.08:  # Skip near-grayscale
            hues.append(h)
    
    # Temperature: count warm (0-60, 300-360) vs cool (180-260)
    warm = sum(1 for c in palette if hex_to_hsl(c['hex'])[0] in range(0, 75) or hex_to_hsl(c['hex'])[0] > 300)
    cool = sum(1 for c in palette if 150 <= hex_to_hsl(c['hex'])[0] <= 280)
    
    if warm > cool:
        temperature = 'warm'
    elif cool > warm:
        temperature = 'cool'
    else:
        temperature = 'balanced'
    
    # Brightness: average lightness weighted by ratio
    avg_lightness = sum(hex_to_hsl(c['hex'])[2] * c['ratio'] for c in palette)
    if avg_lightness < 0.30:
        brightness = 'dark'
    elif avg_lightness < 0.55:
        brightness = 'medium'
    else:
        brightness = 'bright'
    
    # Scheme classification based on hue spread
    if len(hues) < 2:
        scheme = 'monochromatic'
    else:
        hue_range = max(hues) - min(hues)
        if hue_range < 40 or hue_range > 320:
            scheme = 'monochromatic'
        elif hue_range < 100:
            scheme = 'analogous'
        elif hue_range < 200:
            scheme = 'complementary'
        else:
            scheme = 'split-complementary'
    
    return {
        'scheme': scheme,
        'temperature': temperature,
        'brightness': brightness
    }

def slugify(title_cn):
    """Create URL-safe slug from Chinese title."""
    import hashlib
    # Use pinyin-like approach: hash-based short slug
    h = hashlib.md5(title_cn.encode()).hexdigest()[:6]
    # Clean title for readable part
    clean = re.sub(r'[^\w]', '', title_cn)[:10].lower()
    return f'{clean}-{h}' if clean else f'film-{h}'

def generate_files(movie, palette, analysis, scene_img_path=None):
    """Generate palette.json, tokens.css, COLOR_STORY.md for a movie."""
    slug = slugify(movie['title_cn'])
    out_dir = PALETTES_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # palette.json
    palette_data = {
        'palette': [{'hex': c['hex'], 'ratio': c['ratio']} for c in palette],
        'analysis': analysis,
        'meta': {
            'title_cn': movie['title_cn'],
            'title_en': movie['title_en'],
            'year': movie['year'],
            'rating': movie['rating'],
            'rank': movie['rank'],
            'douban_id': movie['douban_id'],
            'source': 'douban_top50'
        }
    }
    (out_dir / 'palette.json').write_text(
        json.dumps(palette_data, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    
    # tokens.css
    roles = ['bg', 'surface', 'accent', 'text', 'muted']
    css_lines = [
        f'/* Cinema Palette — {slug} */',
        f'/* {movie["title_cn"]} ({movie["title_en"]}, {movie["year"]}) — 豆瓣 #{movie["rank"]} */',
        '/* Auto-extracted from movie stills via k-means clustering */',
        '',
        ':root {'
    ]
    for i, color in enumerate(palette):
        role = roles[i] if i < len(roles) else f'extra{i}'
        pct = int(color['ratio'] * 100)
        css_lines.append(f'  --cinema-{role}: {color["hex"]};  /* {pct}% */')
    css_lines.append(f'  /* scheme: {analysis["scheme"]}, temp: {analysis["temperature"]}, brightness: {analysis["brightness"]} */')
    css_lines.append('}')
    (out_dir / 'tokens.css').write_text('\n'.join(css_lines) + '\n', encoding='utf-8')
    
    # COLOR_STORY.md
    color_names = name_colors(palette)
    md_lines = [
        f'---',
        f'id: {slug}',
        f'title: {movie["title_cn"]} ({movie["title_en"]})',
        f'year: {movie["year"]}',
        f'rank: 豆瓣 Top {movie["rank"]}',
        f'rating: {movie["rating"]}',
        f'source: douban_top50',
        f'---',
        f'',
        f'# {movie["title_cn"]} — {movie["title_en"]}',
        f'',
        f'> 豆瓣评分 {movie["rating"]} | {movie["year"]}年 | Top {movie["rank"]}',
        f'',
        f'## 配色',
        f'',
        f'| 色名 | Hex | 占比 |',
        f'|------|-----|------|',
    ]
    for i, color in enumerate(palette):
        name = color_names[i]
        pct = f'{color["ratio"]*100:.1f}%'
        md_lines.append(f'| {name} | `{color["hex"]}` | {pct} |')
    
    md_lines.extend([
        f'',
        f'## 分析',
        f'',
        f'**配色类型：{scheme_cn(analysis["scheme"])}** — 从剧照中通过 k-means 聚类提取，按画面占比排序。',
        f'',
        f'**色温：{temp_cn(analysis["temperature"])}**',
        f'',
        f'**明度：{brightness_cn(analysis["brightness"])}**',
        f'',
        f'## 应用建议',
        f'',
        f'**适用场景：** {suggest_usage(analysis)}',
        f'',
        f'**CSS Tokens:**',
        f'```css',
        f':root {{',
    ])
    for i, color in enumerate(palette):
        role = roles[i] if i < len(roles) else f'extra{i}'
        md_lines.append(f'  --cinema-{role}: {color["hex"]};')
    md_lines.extend([f'}}', f'```', f''])
    
    (out_dir / 'COLOR_STORY.md').write_text('\n'.join(md_lines), encoding='utf-8')
    
    return slug

def scheme_cn(s):
    return {'monochromatic': '单色系（Monochromatic）', 'analogous': '邻近色（Analogous）',
            'complementary': '互补色（Complementary）', 'split-complementary': '分裂互补（Split-Complementary）'}.get(s, s)

def temp_cn(t):
    return {'warm': '暖调', 'cool': '冷调', 'balanced': '中性'}.get(t, t)

def brightness_cn(b):
    return {'dark': '暗调', 'medium': '中调', 'bright': '亮调'}.get(b, b)

def suggest_usage(analysis):
    s = analysis['scheme']
    b = analysis['brightness']
    t = analysis['temperature']
    suggestions = []
    if b == 'dark':
        suggestions.append('Dashboard、监控面板、暗色 IDE、数据可视化大屏')
    elif b == 'bright':
        suggestions.append('品牌官网、营销页面、产品展示、移动端 UI')
    else:
        suggestions.append('内容平台、博客、仪表盘、企业官网')
    if t == 'warm':
        suggestions.append('餐饮/生活方式品牌')
    elif t == 'cool':
        suggestions.append('科技/金融产品')
    return '、'.join(suggestions)

def name_colors(palette):
    """Generate Chinese color names based on HSL."""
    names = []
    for c in palette:
        r, g, b = [x/255 for x in c['rgb']]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        h_deg = h * 360
        
        if l < 0.12:
            prefix = '墨'
        elif l < 0.25:
            prefix = '深'
        elif l < 0.45:
            prefix = '暗'
        elif l < 0.65:
            prefix = ''
        elif l < 0.85:
            prefix = '浅'
        else:
            prefix = '白'
        
        if s < 0.08:
            if l < 0.2: name = f'{prefix}灰'
            elif l < 0.5: name = '深灰'
            elif l < 0.8: name = '灰'
            else: name = '浅灰'
        elif h_deg < 15 or h_deg >= 345:
            name = f'{prefix}红'
        elif h_deg < 40:
            name = f'{prefix}橙'
        elif h_deg < 70:
            name = f'{prefix}黄'
        elif h_deg < 100:
            name = f'{prefix}黄绿'
        elif h_deg < 160:
            name = f'{prefix}绿'
        elif h_deg < 200:
            name = f'{prefix}青'
        elif h_deg < 250:
            name = f'{prefix}蓝'
        elif h_deg < 290:
            name = f'{prefix}蓝紫'
        elif h_deg < 330:
            name = f'{prefix}紫'
        else:
            name = f'{prefix}玫红'
        
        names.append(name)
    return names

# ── Main ──

def main():
    movies = json.loads(MOVIES_JSON.read_text())['movies']
    
    # Resume support
    progress_file = Path(__file__).resolve().parent / 'progress.json'
    if progress_file.exists():
        done = set(json.loads(progress_file.read_text()).get('done', []))
        print(f'Resuming: {len(done)} already done')
    else:
        done = set()
    
    results = []
    errors = []
    
    for movie in movies:
        if movie['douban_id'] in done:
            print(f'  [SKIP] #{movie["rank"]} {movie["title_cn"]}')
            continue
        
        print(f'\n[{movie["rank"]}/50] {movie["title_cn"]} ({movie["title_en"]})')
        
        # Step 1: Get stills URLs
        try:
            thumb_urls = open_douban_stills(movie['douban_id'])
            if not thumb_urls:
                print(f'  ⚠ No images found, skipping')
                errors.append({'rank': movie['rank'], 'title': movie['title_cn'], 'error': 'no_images'})
                continue
            
            # Take first N, convert to large
            stills_urls = [thumb_to_large(u) for u in thumb_urls[:STILLS_PER_MOVIE]]
            print(f'  Found {len(thumb_urls)} stills, using top {len(stills_urls)}')
            
            # Step 2: Download and analyze
            all_pixels = []
            for i, url in enumerate(stills_urls):
                img = download_image(url)
                if img:
                    img_small = img.resize((150, 150), Image.LANCZOS)
                    all_pixels.append(np.array(img_small).reshape(-1, 3))
                    print(f'  ✓ Still {i+1}: {img.size[0]}x{img.size[1]}')
                else:
                    print(f'  ✗ Still {i+1}: download failed')
                time.sleep(0.3)
            
            if not all_pixels:
                print(f'  ⚠ All downloads failed, skipping')
                errors.append({'rank': movie['rank'], 'title': movie['title_cn'], 'error': 'download_failed'})
                continue
            
            # Step 3: Combined k-means on all stills
            combined = np.vstack(all_pixels)
            kmeans = KMeans(n_clusters=5, n_init=10, random_state=42)
            labels = kmeans.fit_predict(combined)
            counts = np.bincount(labels, minlength=5)
            total = counts.sum()
            order = np.argsort(-counts)
            
            palette = []
            for idx in order:
                rgb = tuple(kmeans.cluster_centers_[idx].astype(int))
                ratio = counts[idx] / total
                palette.append({
                    'hex': rgb_to_hex(rgb),
                    'rgb': list(rgb),
                    'ratio': round(float(ratio), 4)
                })
            
            # Step 4: Analyze
            analysis = analyze_color_scheme(palette)
            
            # Step 5: Generate files
            slug = generate_files(movie, palette, analysis)
            
            colors_str = ' '.join(f'{c["hex"]}({c["ratio"]*100:.0f}%)' for c in palette)
            print(f'  → {slug}')
            print(f'  → {analysis["scheme"]} / {analysis["temperature"]} / {analysis["brightness"]}')
            print(f'  → {colors_str}')
            
            results.append({
                'rank': movie['rank'],
                'title_cn': movie['title_cn'],
                'slug': slug,
                'palette': [{'hex': c['hex'], 'ratio': c['ratio']} for c in palette],
                'analysis': analysis
            })
            
            done.add(movie['douban_id'])
            progress_file.write_text(json.dumps({'done': list(done)}))
            
        except Exception as e:
            print(f'  ✗ ERROR: {e}')
            errors.append({'rank': movie['rank'], 'title': movie['title_cn'], 'error': str(e)})
        
        time.sleep(1.5)  # Rate limit
    
    # Save results
    results_file = Path(__file__).resolve().parent / 'palettes_results.json'
    results_file.write_text(json.dumps({'results': results, 'errors': errors}, ensure_ascii=False, indent=2))
    
    print(f'\n{"="*60}')
    print(f'Done: {len(results)} palettes generated, {len(errors)} errors')
    if errors:
        print(f'Errors: {json.dumps(errors, ensure_ascii=False, indent=2)}')

if __name__ == '__main__':
    main()
