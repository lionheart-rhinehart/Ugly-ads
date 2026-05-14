# Course Marketer

The "I sell a course" aesthetic. Designed to look like a high-converting promo from someone who sells training, masterclasses, programs, or coaching to a specific audience.

## Why it works (when it works)

This is the modern descendant of the used-car-lot ad — same density-forward, hook-first logic, but with a more confident color treatment. It works because:

1. **The qualifier pill identifies the audience immediately.** Scrolling past, only the target stops. The rest of the feed self-filters out.
2. **One enormous hook word does 80% of the work.** "FREE," "STOP," "WARNING," "HOW," "NEW" — one word, massive, all caps, white-on-color. Impossible to miss at thumbnail size.
3. **The punchline qualifier signals voice.** A small last line that breaks the formal pitch and gives the offer personality ("THAT DOESN'T SUCK", "WITHOUT THE BS", "NO FLUFF"). Reads as a real person, not a brand.
4. **The gradient is the only "polish" element.** Everything else is deliberately stark — flat type, no shadows, no decorative elements. The gradient does all the visual work.

Best used for: courses, trainings, free workshops, lead magnets, coaching, masterclasses, ebooks, SaaS trials, communities.

## Color palette

The signature is a diagonal two-color gradient. Pick one combo per ad:

- Purple `#7C3AED` → Orange `#F97316` (the reference — energetic, modern)
- Deep blue `#1E40AF` → Magenta `#EC4899` (tech / SaaS energy)
- Teal `#0D9488` → Lime `#84CC16` (wellness / fitness energy)
- Crimson `#B91C1C` → Amber `#D97706` (urgency / financial energy)
- Indigo `#4338CA` → Hot pink `#DB2777` (creative / agency energy)

Rules:
- Gradient runs **top-left to bottom-right** (135°). Other angles read as different aesthetic.
- The two colors should be visibly different in hue, not just lightness — that's what makes the diagonal blend feel intentional.
- Saturation high, but not neon. These are *confident* colors, not screaming ones.

Foreground elements use only **white** (`#FFFFFF`) and **near-black** (`#0F172A`). No accent colors fight the gradient.

## Typography

One font family throughout, ultra-bold, condensed sans-serif. Anton, Oswald, Bebas Neue, or Impact all work — the key is tall, narrow letters with very thin tracking so they can be packed enormous.

- **Qualifier pill text**: 28-40pt, black on white, all caps, letter-spacing slightly loose
- **Hook word ("FREE")**: 220-300pt, white, all caps. The hook should occupy ~45% of canvas height alone.
- **Offer lines ("FACEBOOK ADS / TRAINING")**: 110-150pt, white, all caps, stacked vertically. Tight line height (0.9x).
- **Punchline ("THAT DOESN'T SUCK")**: 70-90pt, **slightly darker / lower opacity** than the rest of the white text — looks like it recedes a half-step. Use `rgba(255,255,255,0.55)` or a dark muted tone `#1E1B4B` depending on the gradient.

All caps for every text element except possibly the punchline (where lowercase can also work for voice).

## Layout (1080×1080)

```
┌─────────────────────────────────────┐
│           ╔═══════════════╗         │
│           ║ QUALIFIER PILL ║        │  ← white rounded-pill, ~70px tall,
│           ╚═══════════════╝         │    centered, ~60% of canvas width
│                                     │
│                                     │
│                                     │
│              FREE                   │  ← the hook, MASSIVE, centered
│                                     │    occupies ~40-45% of height
│                                     │
│                                     │
│        FACEBOOK ADS                 │  ← offer line 1, centered
│           TRAINING                  │  ← offer line 2, centered
│                                     │
│       THAT DOESN'T SUCK             │  ← punchline, smaller, muted color
│                                     │
└─────────────────────────────────────┘
```

Vertical spacing is intentional and generous between the pill and the hook. Everything else is tight.

## Distinctive elements

- **Qualifier pill**: Solid white rounded rectangle with black all-caps text. Corner radius equals half the height (perfectly pill-shaped). 16-24px horizontal padding inside. Ends with a colon (`AGENCY OWNERS:`) — the colon implies "and here's what's coming."
- **Hook word**: One word, never two. If you can't get the hook to one word, you're using the wrong template.
- **Offer stack**: 2-3 short lines describing what the offer is. Stacked, centered, tight line height. Total stack should feel like one block, not three lines.
- **Punchline qualifier**: One short line at the bottom that breaks the formal pitch. Common patterns:
  - "THAT DOESN'T SUCK"
  - "WITHOUT THE BS"
  - "NO FLUFF, NO UPSELL"
  - "IN UNDER 30 DAYS"
  - "EVEN IF YOU'RE STARTING FROM ZERO"
  - "BUILT BY A REAL [PROFESSION], NOT A GURU"

## Copy voice

Direct address to a specific audience. The qualifier pill names them; the rest pitches them.

**Examples:**

```
DIGITAL MARKETING AGENCY OWNERS:
FREE
FACEBOOK ADS
TRAINING
THAT DOESN'T SUCK
```

```
SOLOPRENEURS DOING $10K/MO:
NEW
SCALING
PLAYBOOK
WITHOUT HIRING ANYONE
```

```
PARENTS OF PICKY EATERS:
FREE
MEAL PLAN
DOWNLOAD
THAT KIDS ACTUALLY EAT
```

```
LANDLORDS IN [CITY]:
STOP
LOSING MONEY
ON VACANCIES
(7-DAY FILL GUARANTEE)
```

## Rendering hints

The renderer can produce this template using:

- A diagonal gradient as the background. The current `render.py` doesn't have a native gradient layer yet — render one with Pillow by generating a 2-px-wide image colored along the gradient and resizing to canvas, *or* add a `gradient` layer type.
- One `rectangle` (rounded, white, full pill radius) + one centered `text` layer for the qualifier pill.
- One `text` layer for the hook word, very large size.
- Two `text` layers for the offer stack, smaller, centered.
- One `text` layer for the punchline, smallest, in `rgba(255,255,255,140)` or a dark tone.

**Note for whoever picks this up next:** add a `gradient` layer type to `scripts/render.py` (start color, end color, angle). It's the missing primitive for this template.

## What to avoid

- No exclamation points. The hook word is loud enough.
- No stars, starbursts, ribbons, or decorative shapes. The gradient and the type are the entire visual system.
- No multi-color text. White-on-gradient only. The punchline can be a muted shade, but never a third color.
- No serif fonts. Even for the punchline.
- Don't use this for tangible products with a fixed price (use `used-car-lot` instead). This template is for offers where the value prop is the transformation, not the SKU.
