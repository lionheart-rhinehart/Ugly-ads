---
name: ugly-ads-generator
description: Generate intentionally ugly but high-converting PNG ads for Facebook and Instagram in the Craigslist/Drudge tradition — where "ugly works" because lo-fi visuals read as authentic, information-dense, and trustworthy. Use this skill whenever the user wants to create an ad, social post, promo graphic, banner, or any marketing image, even if they don't explicitly say "ugly" — and especially when they mention FB/IG/Meta ads, organic posts, or want something that "stands out in the feed," "looks homemade," "converts," "feels real," or follows the used-car-lot, clickbait, or 90s GeoCities aesthetic. Also trigger when the user asks for ad copy that's punchy, urgent, or unhinged-on-purpose.
---

# Ugly Ads Generator

A skill for generating PNG ads in the "ugly works" tradition — the design philosophy that gave us Craigslist, Drudge Report, and every Facebook Marketplace listing that actually sells. The premise: in a feed full of polished brand content, an ad that looks like a real human made it in 5 minutes reads as authentic and information-dense, and authentic + information-dense = clicks.

The goal is not comedy. The goal is to look like the kind of ad someone scrolling FB/IG actually stops on.

## When to use this skill

Trigger this skill when the user wants:
- A social media ad or organic post (FB, IG, Marketplace)
- A promo graphic for a small business, service, or event
- Something "loud," "in your face," "homemade-looking," or that "stands out"
- A banner, sale graphic, or announcement post

Do **not** trigger this skill for: polished brand work, logos, infographics, or anything where the user explicitly wants "clean," "minimal," "professional," or "modern."

## The "ugly works" principles

Before generating anything, internalize what makes an ugly ad actually convert. These are not jokes — they're documented marketing patterns:

1. **Information density beats whitespace.** A polished ad has one headline and a logo. An ugly ad tells you the price, the phone number, the hours, three benefits, and the cross-streets. Density signals "I have something to say."
2. **Clashing colors grab attention.** Red on yellow. Lime on hot pink. Cyan on magenta. Brand-safe palettes blend into the feed; clashing ones interrupt the scroll. The contrast must be high enough to read at thumbnail size.
3. **Specific numbers beat vague claims.** Not "great prices" — "$47 install." Not "fast" — "in your driveway in 19 minutes." Specificity reads as real.
4. **Urgency markers, but earned.** "TODAY ONLY." "5 SPOTS LEFT." "PRICES GO UP MONDAY." These work because they imply scarcity. Don't fake them — let the user supply the actual constraint.
5. **Visible human contact.** A phone number, an @handle, or a name. Polished brand ads hide the human. Ugly ads put the owner's name and number on the graphic.
6. **At least one "trust hack."** A star rating, a years-in-business badge, a "family owned" stamp, a customer count. Even an unverified one. These slot into the corners.
7. **Lo-fi typographic chaos, intentionally.** Mix 3+ fonts. Vary sizes wildly. Use ALL CAPS for headlines, mixed case for body. Add a stroke or shadow on the key word. The "designed in 10 minutes" look is the point.

If the user's request would violate the *spirit* of a principle (e.g., they ask you to make fake reviews up), ask before fabricating — implied scarcity is fine; fabricated social proof is sketchy.

## The workflow

### Step 1: Gather the inputs

Ask the user for whatever's missing. Don't ask all of these at once — only what you actually need:

- **What's being advertised?** (Product, service, event, listing — be specific)
- **What's the offer or hook?** (Price, discount, deadline, what makes it worth stopping for)
- **Contact / CTA?** (Phone number, @handle, website, DM, "comment SOLD," etc.)
- **Format?** (Square 1080×1080 feed post is the default. Story 1080×1920 or link preview 1200×628 also available.)
- **Aesthetic preference?** If they don't say, pick three different ones for the three variants — that's the point of generating 3.
- **Product photo?** Optional. If they have one, ask for a file path; the skill will composite it in. If not, the ad is text-only.

If the user gives a one-liner ("make an ugly ad for my coffee shop"), ask 2-3 quick follow-ups before generating. Don't invent prices, phone numbers, or specific claims — those need to come from the user.

### Step 2: Pick three aesthetics

For each request, generate three variants using three different aesthetics. This gives the user real options to choose from. The built-in aesthetics are in `templates/`:

- **`clickbait-popup`** — Mobile-popup energy. Big "YOU WON'T BELIEVE" headline, fake-X-button vibes, urgency banner across the top, "tap here" CTA. Color palette: lime green, hot pink, electric blue on white or yellow.
- **`used-car-lot`** — Screaming-spokesman energy. ALL CAPS hook, starburst with the price, "BUT WAIT" mid-graphic, exclamation points, phone number huge at the bottom. Color palette: red/yellow/black, sometimes with a strip of American-flag stripes.
- **`geocities-web1`** — 90s web aesthetic. Comic Sans, marquee-style banner, "under construction" gif energy, tiled background, visitor counter, animated-gif-as-static-PNG vibes. Color palette: neon on black, or rainbow gradients.

Each template in `templates/` has a `template.md` describing its visual rules, color palettes, and typographic patterns. **Read the relevant template.md before generating** — they encode the actual rules each aesthetic follows.

When the user adds their own screenshots to `templates/<new-name>/`, read both the screenshot and any `notes.md` they include, and treat that as a new aesthetic option.

### Step 3: Generate copy for each variant

For each of the three aesthetics, write the copy in that voice:
- **Clickbait** wants curiosity gaps and second-person ("THIS is what every [audience] is doing in [city]").
- **Used-car-lot** wants the price up front, the offer in the middle, the urgency at the end.
- **GeoCities** wants enthusiasm and density, like a personal homepage announcing something.

Then assemble:
- 1 headline (the scroll-stopper)
- 1 subhead or offer line
- 1-2 supporting bullets or features
- 1 CTA with the contact info
- 1 trust hack (rating, years, "family owned," etc. — only if the user has one to claim)

### Step 4: Render the PNGs

Use `scripts/render.py` to produce each PNG. It takes a JSON config and outputs a PNG at the requested dimensions. See `references/rendering.md` for the config schema, color helpers, and font handling.

For each variant:
1. Build the config dict (template name, dimensions, copy fields, colors, optional product image path).
2. Call `python scripts/render.py --config <path-to-config.json> --output <path-to-output.png>`.
3. Save outputs to `ugly-ads-output/<timestamp>/variant-{1,2,3}.png` by default, or wherever the user specified.

After all three render, tell the user the file paths and briefly describe what each variant emphasizes ("Variant 1 leads with the price, Variant 2 leads with the deadline, Variant 3 leads with the testimonial").

### Step 5: Iterate

The first batch is a draft. Ask: "Which direction is closest? Want me to push one of these harder, swap an aesthetic, or try a different angle?" Then regenerate just what needs regenerating — don't re-render all three if only one needs work.

## Adding new templates

When the user shares a screenshot of an ugly ad they want to emulate:

1. Create `templates/<short-name>/` (e.g., `templates/infomercial-lower-third/`).
2. Save the screenshot as `reference.png` (or whatever extension).
3. Read the screenshot carefully. In `template.md`, document:
   - **Color palette** (sample the actual hex codes from the screenshot)
   - **Typography** (font families, weights, sizes, where caps/mixed are used)
   - **Layout** (where the headline, price, CTA, trust hack live spatially)
   - **Distinctive elements** (starbursts? stripes? fake-3D bevels? specific shapes?)
4. Add a one-line entry for it in the "built-in aesthetics" list in this SKILL.md so future invocations know it exists.

## Output expectations

- Three PNG files per request, at the requested dimensions (default 1080×1080).
- File paths reported back to the user so they can download and upload to FB/IG.
- A short note per variant explaining the angle, so the user can choose without opening all three.

## What this skill does NOT do

- It does not fabricate testimonials, reviews, ratings, or credentials. Trust hacks must reflect something real the user can claim.
- It does not produce parody or satire ads (different goal — those want comedy first, conversion second).
- It does not produce ads designed to deceive (fake system alerts that look like real OS dialogs, fake "your account is locked" graphics, etc.). Ugly-but-honest is the line.
