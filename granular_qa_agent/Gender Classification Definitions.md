# Gender Classification Definitions

This document defines the gender classification system used for categorizing Nike and athletic apparel/footwear items. Gender classification applies across all product types (Apparel and Footwear).

---

# Gender Categories

## Gender: `Kids`

- **Definition:** Products targeted at children/youth.
- **Signals:** Kid, kids, boy, boys, girl, girls, toddler, youth, children, child.
- **Examples:** "Boys' Training Shorts", "Girls' Running Tee", "Toddler Shoes", "Youth Basketball Jersey".

## Gender: `Men's`

- **Definition:** Products targeted at men.
- **Signals:** Men, mens, male, masculine.
- **Excludes:** If conflicting women's/feminine indicators present.
- **Examples:** "Men's Running Shorts", "Mens Training Tee", "Male Athletic Pants".

## Gender: `Women's`

- **Definition:** Products targeted at women.
- **Signals:** Women, womens, ladies, lady, female, wmn, feminine.
- **Excludes:** If conflicting men's/masculine indicators present.
- **Examples:** "Women's Sports Bra", "Womens Leggings", "Ladies Running Jacket", "WMN Training Top".

## Gender: `Unisex/Undefined`

- **Definition:** Default when no clear gender indicators are present.
- **Use when:** No clear gender signals detected in item description, brand, or category.
- **Examples:** "Training Shorts", "Running Shoes", "Athletic Tee" (no gender specified).

---

# Classification Rules

## Priority Order

Use semantic understanding to detect gender indicators. The examples above are illustrative, not exhaustive. Look for any words, phrases, or context that indicates gender targeting.

1. **Kids indicators** → `Kids`
2. **Women's indicators** (no conflict) → `Women's`
3. **Men's indicators** (no conflict) → `Men's`
4. **No clear indicators** → `Unisex/Undefined`

## Classification Sources

Gender can be detected from multiple data sources:

1. **Web Categories** — Merchant category paths often contain gender segments (e.g., "Men's > Clothing > Shorts").
2. **Item Description** — Product names frequently include gender (e.g., "Nike Women's Dri-FIT Top").
3. **Brand Context** — Some sub-brands or lines are gender-specific.

## Conflict Resolution

- If both men's and women's indicators are present, classify as `Unisex/Undefined`.
- Kids indicators take priority over adult gender indicators.
- When in doubt, default to `Unisex/Undefined`.

---

# Complete Value List

## All Gender Values

- `Kids`
- `Men's`
- `Women's`
- `Unisex/Undefined`

---

# Signal Reference

| Gender | Example Signals |
|--------|-----------------|
| Kids | kid, kids, boy, boys, girl, girls, toddler, youth, children, child |
| Men's | men, mens, male, masculine |
| Women's | women, womens, ladies, lady, female, wmn, feminine |
| Unisex/Undefined | *(no clear signals — default)* |

