# Rendering reference

The skill renders PNGs via `scripts/render.py`, which takes a JSON config and composites layers in order. This file documents the config schema, the available layer types, and the conventions for assembling an ad.

## Requirements

- Python 3
- Pillow (`pip install Pillow`)

Fonts: the renderer tries common system paths for Impact, Comic Sans, Arial Black, Arial, and Times. If a font isn't installed, it falls back to DejaVu (Linux) or Pillow's default. For best results on Linux:

```bash
sudo apt-get install fonts-liberation ttf-mscorefonts-installer
```

## Top-level config

```json
{
  "width": 1080,
  "height": 1080,
  "bg": "#FFFFFF",
  "layers": [ ... ]
}
```

| Field | Type | Notes |
|---|---|---|
| `width` | int | Canvas width in pixels. Defaults: 1080 (square), 1200 (link preview width). |
| `height` | int | Canvas height. Square = 1080, Story = 1920, Link preview = 628. |
| `bg` | hex string or `[r,g,b]` | Base fill before any layers. |
| `layers` | array | Drawn in order — first layer is bottom, last is top. |

## Layer types

### `text`
Plain text block. Use this for most copy.

```json
{
  "type": "text",
  "text": "$47 INSTALL",
  "font": "impact",
  "size": 120,
  "color": "#000000",
  "x": 540,
  "y": 200,
  "align": "center",
  "max_width": 900,
  "stroke_width": 4,
  "stroke_color": "#FFFFFF"
}
```

- `font` — one of `impact`, `comic`, `arial_black`, `arial`, `times`.
- `align` — `left` (default), `center`, `right`. `x` is the anchor point.
- `max_width` — if set, text wraps to fit.
- `stroke_width` / `stroke_color` — for outlined text (useful for headlines).

### `rainbow_text`
Per-character color cycling. Use for GeoCities-style headlines.

```json
{
  "type": "rainbow_text",
  "text": "WELCOME",
  "font": "comic",
  "size": 90,
  "x": 540, "y": 300,
  "align": "center",
  "colors": ["#FF0000", "#FF8000", "#FFD800", "#00CC00", "#00B7FF", "#FF00FF"],
  "stroke_width": 3,
  "stroke_color": "#000000"
}
```

### `rectangle`
Solid or outlined rectangle, optionally rounded. Use for CTA buttons, banners, dividers.

```json
{
  "type": "rectangle",
  "x": 100, "y": 800,
  "width": 880, "height": 120,
  "fill": "#FF2D87",
  "outline": "#000000",
  "outline_width": 4,
  "radius": 16
}
```

### `starburst`
Multi-point star. Use for price callouts in used-car-lot style.

```json
{
  "type": "starburst",
  "cx": 270, "cy": 400,
  "outer_radius": 200,
  "inner_radius": 110,
  "points": 14,
  "fill": "#FFD800",
  "outline": "#000000",
  "outline_width": 6,
  "rotation": 12
}
```

Tip: layer a `text` element on top of the starburst at the same center for the price.

### `ribbon_corner`
Diagonal banner across a top corner.

```json
{
  "type": "ribbon_corner",
  "corner": "top-right",
  "text": "TODAY ONLY!",
  "fill": "#E60000",
  "text_color": "#FFFFFF",
  "size": 36,
  "offset": 120,
  "band": 80
}
```

### `gradient`
Linear two-color gradient across the canvas. Place as the first layer for a gradient background.

```json
{
  "type": "gradient",
  "start_color": "#7C3AED",
  "end_color": "#F97316",
  "angle": 135
}
```

Angle in degrees: `0` = left→right, `90` = top→bottom, `135` = top-left→bottom-right (the course-marketer default), `45` = bottom-left→top-right. Renders pixel-by-pixel in pure Python — adds ~1s at 1080×1080.

### `diagonal_stripes`
Full-canvas diagonal stripe background. Place as the first layer for a striped backdrop.

```json
{
  "type": "diagonal_stripes",
  "stripe_width": 60,
  "colors": ["#E60000", "#FFFFFF", "#003DA5"]
}
```

### `tiled_background`
Repeating pattern background (GeoCities). If `pattern_path` points to an existing PNG, it tiles that. Otherwise renders a starfield.

```json
{
  "type": "tiled_background",
  "bg": "#000033",
  "stars": 250,
  "seed": 7
}
```

### `image`
Composite an external image (product photo, logo). PNG with alpha is best.

```json
{
  "type": "image",
  "path": "/path/to/product.png",
  "x": 200, "y": 500,
  "width": 400, "height": 400
}
```

If `width`/`height` omitted, uses native size. Maintains alpha.

## Layering conventions

Order matters. A typical build is:

1. **Background** — `rectangle` (solid), `diagonal_stripes`, or `tiled_background`.
2. **Decorative shapes** — `starburst`, `ribbon_corner`, divider `rectangle`s.
3. **Images** — product photos, logos.
4. **Text** — headline, subhead, bullets, CTA, fine print.
5. **Top-corner overlays** — `ribbon_corner` always goes last so it sits on top.

## Color reference

Pre-baked palettes for the three built-in aesthetics:

**Clickbait**
- Accent: `#FF2D87` (hot pink), `#C4FF1E` (lime), `#00B7FF` (electric blue)
- Background: `#FFFFFF` or `#FFE600` (yellow)
- Text: `#000000`

**Used-car-lot**
- Accent: `#E60000` (red), `#FFD800` (yellow)
- Trust: `#003DA5` (blue)
- Background: `#FFFFFF` or `#FFE600`
- Text: `#000000`, callouts in `#FFFFFF` on red

**GeoCities**
- Bright primaries on black: `#FF0000`, `#FF8000`, `#FFD800`, `#00CC00`, `#00B7FF`, `#7F00FF`, `#FF00FF`
- Background: `#000000`, `#000033`, or sepia `#F4ECD8`

**Course-marketer (gradient pairs)**
- Purple `#7C3AED` → Orange `#F97316`
- Deep blue `#1E40AF` → Magenta `#EC4899`
- Teal `#0D9488` → Lime `#84CC16`
- Crimson `#B91C1C` → Amber `#D97706`
- Indigo `#4338CA` → Hot pink `#DB2777`
- Foreground: `#FFFFFF` for hook & offer, `#0F172A` (or `rgba(255,255,255,0.55)`) for the punchline qualifier

## Running the renderer

From the skill root:

```bash
python scripts/render.py --config /tmp/variant-1-config.json --output /tmp/variant-1.png
```

Or from anywhere with absolute paths. Output directory is created if it doesn't exist.

## Tips

- For 1080×1080, headlines around 90-130pt feel right. For 1080×1920 stories, go bigger (140-180pt).
- High-contrast outlines (stroke 4-8px) keep text legible against busy backgrounds.
- When in doubt, render once, eyeball the output, and adjust positions. Pixel-perfect placement matters less than overall density and contrast.
- The renderer is forgiving — out-of-bounds coordinates just clip silently. Use that for half-off-screen ribbons or oversized starbursts.
