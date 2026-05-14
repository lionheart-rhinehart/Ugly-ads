#!/usr/bin/env python3
"""
Render an ugly ad PNG from a JSON config.

Usage:
    python render.py --config config.json --output ad.png

Config schema: see references/rendering.md
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    sys.stderr.write(
        "Pillow is required. Install with: pip install Pillow\n"
    )
    sys.exit(1)


FONT_CANDIDATES = {
    "impact": [
        "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",
        "/Library/Fonts/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "C:/Windows/Fonts/impact.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "comic": [
        "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf",
        "/Library/Fonts/Comic Sans MS.ttf",
        "/System/Library/Fonts/Supplemental/Comic Sans MS.ttf",
        "C:/Windows/Fonts/comic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "arial_black": [
        "/usr/share/fonts/truetype/msttcorefonts/Arial_Black.ttf",
        "/Library/Fonts/Arial Black.ttf",
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "C:/Windows/Fonts/ariblk.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "arial": [
        "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "times": [
        "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
        "/Library/Fonts/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "C:/Windows/Fonts/times.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ],
}


def load_font(family: str, size: int) -> ImageFont.FreeTypeFont:
    paths = FONT_CANDIDATES.get(family, FONT_CANDIDATES["arial"])
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def parse_color(c):
    if isinstance(c, (list, tuple)):
        return tuple(c)
    if isinstance(c, str) and c.startswith("#"):
        h = c.lstrip("#")
        if len(h) == 6:
            return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
        if len(h) == 8:
            return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4, 6))
    return (0, 0, 0)


def draw_text_block(draw, layer, canvas_size):
    text = layer["text"]
    family = layer.get("font", "arial")
    size = layer.get("size", 48)
    color = parse_color(layer.get("color", "#000000"))
    x, y = layer.get("x", 0), layer.get("y", 0)
    align = layer.get("align", "left")
    stroke_width = layer.get("stroke_width", 0)
    stroke_color = parse_color(layer.get("stroke_color", "#000000"))
    max_width = layer.get("max_width")

    font = load_font(family, size)

    lines = wrap_text(text, font, max_width) if max_width else text.split("\n")

    line_height = int(size * 1.15)
    for i, line in enumerate(lines):
        line_y = y + i * line_height
        bbox = font.getbbox(line)
        line_w = bbox[2] - bbox[0]
        if align == "center":
            line_x = x - line_w // 2
        elif align == "right":
            line_x = x - line_w
        else:
            line_x = x
        draw.text(
            (line_x, line_y),
            line,
            font=font,
            fill=color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color,
        )


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = []
    for word in words:
        trial = " ".join(current + [word])
        bbox = font.getbbox(trial)
        if bbox[2] - bbox[0] <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_rainbow_text(draw, layer, canvas_size):
    text = layer["text"]
    family = layer.get("font", "comic")
    size = layer.get("size", 80)
    x, y = layer.get("x", 0), layer.get("y", 0)
    align = layer.get("align", "left")
    stroke_width = layer.get("stroke_width", 0)
    stroke_color = parse_color(layer.get("stroke_color", "#000000"))
    colors = [parse_color(c) for c in layer.get("colors", [
        "#FF0000", "#FF8000", "#FFD800", "#00CC00",
        "#00B7FF", "#7F00FF", "#FF00FF",
    ])]

    font = load_font(family, size)

    total_w = sum(font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in text)
    if align == "center":
        cursor_x = x - total_w // 2
    elif align == "right":
        cursor_x = x - total_w
    else:
        cursor_x = x

    for i, ch in enumerate(text):
        color = colors[i % len(colors)]
        draw.text(
            (cursor_x, y),
            ch,
            font=font,
            fill=color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color,
        )
        bbox = font.getbbox(ch)
        cursor_x += bbox[2] - bbox[0]


def draw_rectangle(draw, layer, canvas_size):
    x, y = layer["x"], layer["y"]
    w, h = layer["width"], layer["height"]
    fill = parse_color(layer.get("fill", "#000000")) if layer.get("fill") else None
    outline = parse_color(layer.get("outline")) if layer.get("outline") else None
    radius = layer.get("radius", 0)
    width = layer.get("outline_width", 1)
    if radius > 0:
        draw.rounded_rectangle(
            [x, y, x + w, y + h],
            radius=radius,
            fill=fill,
            outline=outline,
            width=width,
        )
    else:
        draw.rectangle(
            [x, y, x + w, y + h],
            fill=fill,
            outline=outline,
            width=width,
        )


def draw_starburst(draw, layer, canvas_size):
    import math

    cx, cy = layer["cx"], layer["cy"]
    outer_r = layer["outer_radius"]
    inner_r = layer.get("inner_radius", int(outer_r * 0.55))
    points = layer.get("points", 16)
    fill = parse_color(layer.get("fill", "#FFD800"))
    outline = parse_color(layer.get("outline", "#000000"))
    outline_width = layer.get("outline_width", 4)
    rotation = layer.get("rotation", 0)

    vertices = []
    for i in range(points * 2):
        angle = math.radians(rotation + i * (360 / (points * 2)))
        r = outer_r if i % 2 == 0 else inner_r
        vertices.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(vertices, fill=fill, outline=outline)
    # Re-stroke for thicker outline (Pillow polygon outline is 1px only)
    if outline_width > 1:
        for i in range(len(vertices)):
            a = vertices[i]
            b = vertices[(i + 1) % len(vertices)]
            draw.line([a, b], fill=outline, width=outline_width)


def draw_diagonal_stripes(draw, layer, canvas_size):
    cw, ch = canvas_size
    stripe_w = layer.get("stripe_width", 40)
    colors = [parse_color(c) for c in layer.get("colors", ["#E60000", "#FFFFFF"])]
    spacing = stripe_w * len(colors)
    import math
    diag = int(math.hypot(cw, ch)) + spacing
    for i in range(-diag, diag, stripe_w):
        c = colors[(i // stripe_w) % len(colors)]
        draw.polygon(
            [(i, 0), (i + stripe_w, 0), (i + stripe_w + ch, ch), (i + ch, ch)],
            fill=c,
        )


def draw_tiled_background(draw, image, layer, canvas_size):
    pattern_path = layer.get("pattern_path")
    if pattern_path and os.path.exists(pattern_path):
        tile = Image.open(pattern_path).convert("RGBA")
        tw, th = tile.size
        for ty in range(0, canvas_size[1], th):
            for tx in range(0, canvas_size[0], tw):
                image.paste(tile, (tx, ty), tile)
    else:
        # Fallback: starfield (random small dots on dark bg)
        import random
        random.seed(layer.get("seed", 42))
        bg = parse_color(layer.get("bg", "#000033"))
        draw.rectangle([0, 0, canvas_size[0], canvas_size[1]], fill=bg)
        for _ in range(layer.get("stars", 200)):
            sx = random.randint(0, canvas_size[0] - 1)
            sy = random.randint(0, canvas_size[1] - 1)
            brightness = random.randint(150, 255)
            draw.point((sx, sy), fill=(brightness, brightness, brightness))


def draw_ribbon_corner(draw, layer, canvas_size):
    """Diagonal ribbon banner in a top corner."""
    cw, ch = canvas_size
    corner = layer.get("corner", "top-right")  # top-left or top-right
    text = layer["text"]
    fill = parse_color(layer.get("fill", "#E60000"))
    text_color = parse_color(layer.get("text_color", "#FFFFFF"))
    size = layer.get("size", 36)
    offset = layer.get("offset", 80)
    band = layer.get("band", 70)

    if corner == "top-right":
        pts = [
            (cw - offset - band, 0),
            (cw, offset + band),
            (cw, offset),
            (cw - offset, 0),
        ]
        cx = cw - offset / 2 - band / 4
        cy = offset / 2 + band / 4
        rotation = -45
    else:
        pts = [
            (0, offset),
            (offset, 0),
            (offset + band, 0),
            (0, offset + band),
        ]
        cx = offset / 2 + band / 4
        cy = offset / 2 + band / 4
        rotation = 45

    draw.polygon(pts, fill=fill)

    font = load_font(layer.get("font", "impact"), size)
    # Render text to a temp image and rotate
    tmp = Image.new("RGBA", (band * 4, band * 2), (0, 0, 0, 0))
    tmp_draw = ImageDraw.Draw(tmp)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tmp_draw.text(((tmp.size[0] - tw) // 2, (tmp.size[1] - th) // 2),
                  text, font=font, fill=text_color)
    tmp = tmp.rotate(rotation, resample=Image.BICUBIC, expand=False)
    return tmp, (int(cx - tmp.size[0] / 2), int(cy - tmp.size[1] / 2))


def draw_image_layer(image, layer):
    path = layer["path"]
    if not os.path.exists(path):
        sys.stderr.write(f"Warning: image not found: {path}\n")
        return
    img = Image.open(path).convert("RGBA")
    if "width" in layer or "height" in layer:
        w = layer.get("width", img.size[0])
        h = layer.get("height", img.size[1])
        img = img.resize((w, h), Image.LANCZOS)
    x, y = layer.get("x", 0), layer.get("y", 0)
    image.paste(img, (x, y), img)


def render(config: dict, output_path: str):
    width = config.get("width", 1080)
    height = config.get("height", 1080)
    bg = parse_color(config.get("bg", "#FFFFFF"))

    image = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(image, "RGBA")

    deferred = []  # (image_to_paste, (x, y))

    for layer in config.get("layers", []):
        kind = layer.get("type")
        if kind == "tiled_background":
            draw_tiled_background(draw, image, layer, (width, height))
        elif kind == "diagonal_stripes":
            draw_diagonal_stripes(draw, layer, (width, height))
        elif kind == "rectangle":
            draw_rectangle(draw, layer, (width, height))
        elif kind == "starburst":
            draw_starburst(draw, layer, (width, height))
        elif kind == "text":
            draw_text_block(draw, layer, (width, height))
        elif kind == "rainbow_text":
            draw_rainbow_text(draw, layer, (width, height))
        elif kind == "ribbon_corner":
            tmp_img, pos = draw_ribbon_corner(draw, layer, (width, height))
            deferred.append((tmp_img, pos))
        elif kind == "image":
            draw_image_layer(image, layer)
        else:
            sys.stderr.write(f"Warning: unknown layer type: {kind}\n")

    for tmp_img, pos in deferred:
        image.paste(tmp_img, pos, tmp_img)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, "PNG")
    print(f"Wrote {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    render(config, args.output)


if __name__ == "__main__":
    main()
