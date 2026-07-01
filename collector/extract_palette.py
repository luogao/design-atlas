#!/usr/bin/env python3
"""
Cinema Palette Extractor — 从电影画面提取配色方案

用法:
  python3 extract_palette.py <image_path> [--colors 5] [--output palettes/<id>]

输出:
  - JSON 格式的配色方案（hex + 面积比例）
  - 可选: 生成 tokens.css
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.cluster import MiniBatchKMeans


def extract_palette(image_path: str, n_colors: int = 5) -> list[dict]:
    """从图片提取主色和面积比例"""
    img = Image.open(image_path).convert("RGB")
    
    # 缩放以加速（保持宽高比，最长边 <= 400px）
    max_side = 400
    if max(img.size) > max_side:
        ratio = max_side / max(img.size)
        img = img.resize((int(img.width * ratio), int(img.height * ratio)))
    
    pixels = np.array(img).reshape(-1, 3)
    
    # K-means 聚类
    kmeans = MiniBatchKMeans(
        n_clusters=n_colors,
        random_state=42,
        n_init=3,
        max_iter=100,
        batch_size=min(4096, len(pixels)),
    )
    kmeans.fit(pixels)
    
    # 计算每个簇的像素占比
    counts = np.bincount(kmeans.labels_)
    ratios = counts / counts.sum()
    
    # 按占比降序排列
    results = []
    for i in range(n_colors):
        center = kmeans.cluster_centers_[i].astype(int)
        hex_color = "#{:02X}{:02X}{:02X}".format(*center)
        results.append({
            "hex": hex_color,
            "ratio": round(float(ratios[i]), 4),
        })
    
    results.sort(key=lambda x: x["ratio"], reverse=True)
    return results


def analyze_scheme(palette: list[dict]) -> dict:
    """分析配色类型（互补、类比、三分等）"""
    import colorsys
    
    hsv_colors = []
    for c in palette:
        r, g, b = int(c["hex"][1:3], 16) / 255, int(c["hex"][3:5], 16) / 255, int(c["hex"][5:7], 16) / 255
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        hsv_colors.append((h * 360, s, v, c["hex"]))
    
    # 取占比最大的两个色分析关系
    h1, s1, v1, _ = hsv_colors[0]
    h2, s2, v2, _ = hsv_colors[1] if len(hsv_colors) > 1 else (0, 0, 0, None)
    
    hue_diff = abs(h1 - h2)
    if hue_diff > 180:
        hue_diff = 360 - hue_diff
    
    scheme = "monochromatic"  # 默认单色
    if len(hsv_colors) > 1:
        if 150 <= hue_diff <= 210:
            scheme = "complementary"
        elif 20 <= hue_diff <= 50:
            scheme = "analogous"
        elif 110 <= hue_diff <= 140:
            scheme = "split-complementary"
        elif (abs(hue_diff - 120) < 20) and len(hsv_colors) >= 3:
            scheme = "triadic"
    
    # 色温倾向
    warm_count = sum(1 for h, s, v, _ in hsv_colors if s > 0.15 and (h < 60 or h > 300))
    cool_count = sum(1 for h, s, v, _ in hsv_colors if s > 0.15 and 180 < h < 270)
    
    if warm_count > cool_count:
        temperature = "warm"
    elif cool_count > warm_count:
        temperature = "cool"
    else:
        temperature = "balanced"
    
    # 明度倾向
    avg_v = sum(v for _, _, v, _ in hsv_colors) / len(hsv_colors)
    brightness = "dark" if avg_v < 0.4 else "light" if avg_v > 0.7 else "mid"
    
    return {
        "scheme": scheme,
        "temperature": temperature,
        "brightness": brightness,
    }


def generate_tokens_css(palette: list[dict], analysis: dict, movie_title: str = "") -> str:
    """生成 tokens.css"""
    lines = [
        "/* Cinema Palette — " + movie_title + " */",
        "/* Auto-extracted from movie frame, color-only overlay */",
        "/* Apply by overriding :root color variables */",
        "",
        ":root {",
    ]
    
    roles = ["bg", "surface", "accent", "text", "muted"]
    for i, c in enumerate(palette):
        role = roles[i] if i < len(roles) else f"extra-{i}"
        pct = round(c["ratio"] * 100)
        lines.append(f"  --cinema-{role}: {c['hex']};  /* {pct}% */")
    
    lines.append(f"  /* scheme: {analysis['scheme']}, temp: {analysis['temperature']}, brightness: {analysis['brightness']} */")
    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract color palette from movie frame")
    parser.add_argument("image", help="Path to movie frame image")
    parser.add_argument("--colors", type=int, default=5, help="Number of colors to extract")
    parser.add_argument("--output", help="Output directory (palettes/<id>)")
    parser.add_argument("--title", default="", help="Movie title for tokens.css header")
    args = parser.parse_args()
    
    if not Path(args.image).exists():
        print(f"Error: {args.image} not found", file=sys.stderr)
        sys.exit(1)
    
    # 提取
    palette = extract_palette(args.image, args.colors)
    analysis = analyze_scheme(palette)
    
    result = {
        "palette": palette,
        "analysis": analysis,
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 可选写入目录
    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # tokens.css
        css = generate_tokens_css(palette, analysis, args.title)
        (out_dir / "tokens.css").write_text(css)
        
        # palette.json
        (out_dir / "palette.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False)
        )
        
        # 复制图片
        import shutil
        shutil.copy2(args.image, out_dir / "scene.png")
        
        print(f"\n✓ Written to {out_dir}/")


if __name__ == "__main__":
    main()
