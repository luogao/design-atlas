#!/usr/bin/env python3
"""Re-fetch movie stills from Douban and save as scene.png in each palette dir."""
import subprocess, json, time, requests, sys, os
from pathlib import Path
from io import BytesIO
from PIL import Image

BASE = Path(__file__).parent.parent
SESSION = 'atlas'
results = json.loads((BASE / 'collector/palettes_results.json').read_text())
movies = json.loads((BASE / 'collector/douban_top50.json').read_text())['movies']

# Build rank -> (title, douban_id, slug) map
rank_map = {}
for m in movies:
    rank_map[m['rank']] = m
for r in results['results']:
    if r['rank'] in rank_map:
        rank_map[r['rank']]['slug'] = r['slug']

def run_opencli(args, timeout=30):
    result = subprocess.run(f'opencli {args}', shell=True, capture_output=True, text=True, timeout=timeout)
    out = result.stdout
    idx = out.rfind('Update available')
    if idx > 0: out = out[:idx]
    return out.strip()

def open_stills(douban_id):
    url = f'https://movie.douban.com/subject/{douban_id}/photos?type=S'
    run_opencli(f'browser {SESSION} open "{url}"')
    time.sleep(3)
    js = "(() => { const imgs = document.querySelectorAll('.cover img'); return JSON.stringify(Array.from(imgs).map(i => i.src)); })()"
    raw = run_opencli(f'browser {SESSION} eval "{js}"')
    try:
        return json.loads(raw)
    except:
        return []

def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'Referer': 'https://movie.douban.com/'}
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        return Image.open(BytesIO(resp.content)).convert('RGB')
    return None

done = 0
failed = 0
for rank in sorted(rank_map.keys()):
    m = rank_map[rank]
    slug = m.get('slug')
    if not slug:
        print(f"[{rank}] {m['title_cn']}: no slug, skip")
        failed += 1
        continue
    
    palette_dir = BASE / 'palettes' / slug
    scene_png = palette_dir / 'scene.png'
    if scene_png.exists():
        print(f"[{rank}] {m['title_cn']}: already have scene.png")
        done += 1
        continue
    
    sys.stdout.flush()
    try:
        thumbs = open_stills(m['douban_id'])
        if not thumbs:
            print(f"[{rank}] {m['title_cn']}: no stills found")
            failed += 1
            continue
        
        for thumb_url in thumbs[:5]:
            large_url = thumb_url.replace('/m/public/', '/l/public/')
            img = download(large_url)
            if img and img.size[0] > 200:
                max_w = 800
                if img.size[0] > max_w:
                    ratio = max_w / img.size[0]
                    img = img.resize((max_w, int(img.size[1] * ratio)), Image.LANCZOS)
                img.save(scene_png, 'PNG', optimize=True)
                print(f"[{rank}] {m['title_cn']}: ✓ {img.size[0]}x{img.size[1]}")
                done += 1
                break
        else:
            print(f"[{rank}] {m['title_cn']}: all downloads failed")
            failed += 1
    except Exception as e:
        print(f"[{rank}] {m['title_cn']}: ✗ {e}")
        failed += 1

print(f"\nTotal: {done} saved, {failed} failed")
