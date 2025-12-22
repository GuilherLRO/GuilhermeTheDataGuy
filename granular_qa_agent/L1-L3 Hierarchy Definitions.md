# L1-L3 Product Hierarchy Definitions

This document defines the product classification hierarchy used for categorizing Nike and athletic apparel/footwear items. The hierarchy has three levels (L1 → L2 → L3) providing progressively finer-grained classification.

---

# L1 Categories

L1 is the top-level product type classification.

## L1: `Apparel`

- **Definition:** Clothing items worn on the body including shirts, pants, dresses, jackets, bras, underwear, etc.
- **Includes:** Shirts, pants, shorts, dresses, jackets, bras, underwear, hoodies, tights, skirts, jerseys, tracksuits.
- **Excludes:** Socks, swimwear, sleepwear, accessories, equipment.

## L1: `Footwear`

- **Definition:** Shoes, boots, sandals, cleats, and other footwear items.
- **Includes:** Shoes, boots, sandals, cleats, sneakers, slides, flip-flops.
- **Excludes:** Socks.

## L1: `None`

- **Definition:** Out-of-scope items that are not apparel or footwear.
- **Includes:** Accessories, equipment, bags, hats, gloves, socks, swimwear, sleepwear.

---

# L2 Categories (Apparel Only)

L2 provides mid-level categorization for Apparel items.

## L2: `Bottoms`

- **Definition:** Lower-body athletic apparel.
- **Includes:** Pants, shorts, leggings, tights, joggers, skirts, skorts.
- **Excludes:** Jeans, swimwear, underwear.

## L2: `Tops`

- **Definition:** Upper-body athletic apparel.
- **Includes:** Tee, t-shirt, tank, hoodie, sweatshirt, fleece, polo, jersey.
- **Excludes:** Dress shirts, button-downs, jackets.
- **Note:** Fleece hoodie/pullover → Tops; "fleece jacket" → Jackets & Outerwear.

## L2: `Jackets & Outerwear`

- **Definition:** Outer-layer athletic apparel.
- **Includes:** Jacket, windbreaker, parka, puffer, vest, coat.
- **Excludes:** Hoodies (→ Tops), fleece without "jacket" (→ Tops).

## L2: `Bras`

- **Definition:** Sports and active bras.
- **Includes:** Sports bra, training bra, active bra.
- **Excludes:** Bralettes, lingerie.

## L2: `Dresses`

- **Definition:** Athletic one-piece dresses (athletic context required).
- **Includes:** Tennis dress, running dress, training dress.
- **Excludes:** Fashion dresses, formal dresses, maxi dresses, pajama dresses.

## L2: `Track Suits`

- **Definition:** Jacket + pants SET sold together.
- **Includes:** Track set, tracksuit set, pant set.
- **Excludes:** Individual pieces (→ classify in respective category).

## L2: `Underwear`

- **Definition:** Performance underwear (athletic context).
- **Includes:** Briefs, boxers, underwear.
- **Excludes:** Bras (→ Bras), compression shorts (→ Bottoms).

## L2: `Other Apparel`

- **Definition:** Apparel items that don't fit any of the above L2 categories.
- **Use when:** Item is apparel but doesn't clearly fit Bottoms, Tops, Jackets & Outerwear, Bras, Dresses, Track Suits, or Underwear.

---

# L3 Categories

L3 provides the most granular categorization within each L2 category.

---

## L3 for Bottoms

### L3: `Baselayer Bottoms`

- **Definition:** First-layer compression/thermal bottoms.
- **Signals:** Baselayer, compression, thermal, HeatGear, ColdGear + (short/pant/tight/legging).
- **Excludes:** Outerwear tights, fleece, regular shorts.

### L3: `Fleece Bottoms`

- **Definition:** Cozy/warmth-focused bottoms.
- **Signals:** Fleece, jogger, sweatpant, French terry, Tech Fleece.
- **Excludes:** Woven track pants, baselayer.

### L3: `Shorts`

- **Definition:** Athletic shorts (outerwear, not baselayer).
- **Excludes:** Compression shorts (→ Baselayer Bottoms), swimwear.

### L3: `Skirts`

- **Definition:** Athletic skirts.
- **Signals:** Skirt, skort.
- **Excludes:** Fashion skirts.

### L3: `Tights`

- **Definition:** Outerwear leggings/tights (running/yoga/training, not baselayer).
- **Signals:** Leggings, tights.
- **Excludes:** Baselayer leggings (→ Baselayer Bottoms).

### L3: `Pants`

- **Definition:** Woven full-length pants.
- **Signals:** Track pants, training pants, cargo, warm-up pants.
- **Excludes:** Fleece joggers (→ Fleece Bottoms), baselayer, shorts.

### L3: `Other Bottoms`

- **Definition:** Bottoms that don't fit any of the above L3 categories.
- **Use when:** Item is bottoms but doesn't clearly fit Baselayer Bottoms, Fleece Bottoms, Pants, Shorts, Skirts, or Tights.

### Priority Order (Bottoms)

1. Baselayer/compression → `Baselayer Bottoms`
2. Fleece/jogger → `Fleece Bottoms`
3. Shorts → `Shorts`
4. Skirt → `Skirts`
5. Leggings/tights → `Tights`
6. Pants → `Pants`
7. If none fit → `Other Bottoms`

---

## L3 for Tops

### L3: `Baselayer Tops`

- **Definition:** First-layer compression/thermal tops.
- **Signals:** Baselayer, compression, thermal, HeatGear, ColdGear + (top/shirt/mock/crew).
- **Excludes:** Outerwear tops, fleece.

### L3: `Fleece Tops`

- **Definition:** Cozy/warmth-focused tops.
- **Signals:** Hoodie, sweatshirt, fleece crew, pullover, French terry.
- **Excludes:** Baselayer, graphic tees.
- **Note:** Fleece hoodie/pullover → Fleece Tops; "fleece jacket" → Jackets & Outerwear.

### L3: `Graphic Tees`

- **Definition:** Tees with graphic prints/logos.
- **Signals:** Graphic, licensed, logo, print + (tee/t-shirt).
- **Excludes:** Plain athletic tees (→ Athletic Shirts & Tees).

### L3: `Polos`

- **Definition:** Collared polo shirts.
- **Signals:** Polo (with shirt context).
- **Excludes:** Tees without collar.

### L3: `Replica Jerseys`

- **Definition:** Fan replica jerseys.
- **Signals:** Replica, fan + jersey, team jersey (replica).
- **Excludes:** Performance jerseys (→ Athletic Shirts & Tees).

### L3: `Athletic Shirts & Tees`

- **Definition:** General athletic tops (not graphic, not fleece, not baselayer).
- **Signals:** Tee, t-shirt, tank.
- **Excludes:** Graphic tees, fleece, baselayer, polos, jerseys.

### L3: `Other Tops`

- **Definition:** Tops that don't fit any of the above L3 categories.
- **Use when:** Item is tops but doesn't clearly fit Athletic Shirts & Tees, Baselayer Tops, Fleece Tops, Graphic Tees, Polos, or Replica Jerseys.

### Priority Order (Tops)

1. Baselayer/compression → `Baselayer Tops`
2. Hoodie/fleece → `Fleece Tops`
3. Graphic/licensed → `Graphic Tees`
4. Polo → `Polos`
5. Replica/fan + jersey → `Replica Jerseys`
6. Tee/tank → `Athletic Shirts & Tees`
7. If none fit → `Other Tops`

---

## L3 for Jackets & Outerwear

### L3: `Outerwear`

- **Definition:** Insulated/weather-protective outer layers.
- **Signals:** Puffer, parka, down, rain jacket, insulated, softshell, hardshell, GORE-TEX, waterproof.
- **Excludes:** Lightweight track jackets, windbreakers.

### L3: `Jackets`

- **Definition:** Lightweight jackets.
- **Signals:** Windbreaker, track jacket, coach jacket, packable, lightweight.
- **Excludes:** Insulated, weatherproof, heavy parkas.

### L3: `Other Jackets & Outerwear`

- **Definition:** Jackets & Outerwear items that don't fit the above L3 categories.
- **Use when:** Item is jackets/outerwear but doesn't clearly fit Jackets or Outerwear.

### Priority Order (Jackets & Outerwear)

1. Puffer/parka/down/insulated/rain/waterproof → `Outerwear`
2. Windbreaker/track/coach/packable → `Jackets`
3. If none fit → `Other Jackets & Outerwear`

---

# Classification Rules Summary

## General Rules

- **Baselayer ambiguous** → Tops
- **Compression shorts** → Bottoms (Baselayer Bottoms at L3)
- **Track suit** → Must be a SET (jacket + pants together)
- **Fleece hoodie/pullover** → Tops (Fleece Tops at L3)
- **"Fleece jacket"** → Jackets & Outerwear

## L2/L3 Values Reference

| L2 Category | L3 Options |
|-------------|------------|
| Bottoms | Baselayer Bottoms, Fleece Bottoms, Pants, Shorts, Skirts, Tights, Other Bottoms |
| Tops | Athletic Shirts & Tees, Baselayer Tops, Fleece Tops, Graphic Tees, Polos, Replica Jerseys, Other Tops |
| Jackets & Outerwear | Jackets, Outerwear, Other Jackets & Outerwear |
| Bras | *(no L3 sub-categories)* |
| Dresses | *(no L3 sub-categories)* |
| Track Suits | *(no L3 sub-categories)* |
| Underwear | *(no L3 sub-categories)* |
| Other Apparel | *(no L3 sub-categories)* |

---

# Complete Value Lists

## All L1 Values

- `Apparel`
- `Footwear`
- `None`

## All L2 Values (Apparel)

- `Bottoms`
- `Tops`
- `Jackets & Outerwear`
- `Bras`
- `Dresses`
- `Track Suits`
- `Underwear`
- `Other Apparel`

## All L3 Values

### Bottoms L3

- `Baselayer Bottoms`
- `Fleece Bottoms`
- `Pants`
- `Shorts`
- `Skirts`
- `Tights`
- `Other Bottoms`

### Tops L3

- `Athletic Shirts & Tees`
- `Baselayer Tops`
- `Fleece Tops`
- `Graphic Tees`
- `Polos`
- `Replica Jerseys`
- `Other Tops`

### Jackets & Outerwear L3

- `Jackets`
- `Outerwear`
- `Other Jackets & Outerwear`
