# Values Reference Tables

This document contains quick-reference tables for all classification values across the L1-L3 hierarchy, Gender, and FoP (Field of Play) classifications. All fields allow `NULL` values when classification is not applicable or cannot be determined.

---

# L1 Values

| Parent | Values |
|--------|--------|
| (root) | `Apparel`, `Footwear`, `None`, `NULL` |

---

# L2 Values

| Parent (L1) | Values (L2) |
|-------------|-------------|
| Apparel | `Bottoms`, `Tops`, `Jackets & Outerwear`, `Bras`, `Dresses`, `Track Suits`, `Underwear`, `Other Apparel`, `NULL` |
| Footwear | `NULL` (no L2) |
| None | `NULL` (no L2) |

---

# L3 Values

| Parent (L2) | Values (L3) |
|-------------|-------------|
| Bottoms | `Baselayer Bottoms`, `Fleece Bottoms`, `Pants`, `Shorts`, `Skirts`, `Tights`, `Other Bottoms`, `NULL` |
| Tops | `Athletic Shirts & Tees`, `Baselayer Tops`, `Fleece Tops`, `Graphic Tees`, `Polos`, `Replica Jerseys`, `Other Tops`, `NULL` |
| Jackets & Outerwear | `Jackets`, `Outerwear`, `Other Jackets & Outerwear`, `NULL` |
| Bras | `NULL` (no L3) |
| Dresses | `NULL` (no L3) |
| Track Suits | `NULL` (no L3) |
| Underwear | `NULL` (no L3) |
| Other Apparel | `NULL` (no L3) |

---

# Gender Values

| Parent | Values |
|--------|--------|
| (root) | `Kids`, `Men's`, `Women's`, `Unisex/Undefined`, `NULL` |

---

# FoP Values

| Parent (L1) | Values (FoP) |
|-------------|--------------|
| Apparel | `sportswear`, `running`, `basketball`, `training`, `soccer`, `hiking`, `ski_snowboard`, `golf`, `tennis`, `american_football`, `baseball`, `softball`, `lacrosse`, `volleyball`, `swimming`, `cricket`, `pickleball`, `boxing`, `gymnastics`, `cheer_dance`, `rugby`, `wrestling`, `field_hockey`, `NULL` |
| Footwear | `sportswear`, `running`, `basketball`, `training`, `soccer`, `hiking`, `walking`, `flip_flops`, `slides`, `outdoor_sandals`, `ski_snowboard`, `golf`, `tennis`, `american_football`, `baseball`, `softball`, `lacrosse`, `volleyball`, `cricket`, `pickleball`, `boxing`, `cheer_dance`, `rugby`, `wrestling`, `field_hockey`, `NULL` |

---

# Sub-sport Values

| Parent (FoP) | Applies To | Values (Sub-sport) |
|--------------|------------|-------------------|
| sportswear | Footwear | `sportswear_running`, `sportswear_basketball`, `sportswear_tennis`, `sportswear_soccer`, `sportswear_skateboarding`, `sportswear_outdoor`, `sportswear_other`, `NULL` |
| running | Footwear | `trail_running`, `road_running`, `track_field_running`, `running_other`, `NULL` |
| basketball | Footwear | `signature_basketball`, `performance_basketball`, `basketball_other`, `NULL` |
| training | Apparel | `cross_training`, `yoga`, `training_other`, `NULL` |
| training | Footwear | `cross_training`, `training_other`, `NULL` |
| soccer | Footwear | `outdoor_soccer`, `indoor_soccer`, `NULL` |

---

# Complete Hierarchy Summary

```text
L1
├── Apparel
│   └── L2
│       ├── Bottoms → L3: Baselayer Bottoms, Fleece Bottoms, Pants, Shorts, Skirts, Tights, Other Bottoms
│       ├── Tops → L3: Athletic Shirts & Tees, Baselayer Tops, Fleece Tops, Graphic Tees, Polos, Replica Jerseys, Other Tops
│       ├── Jackets & Outerwear → L3: Jackets, Outerwear, Other Jackets & Outerwear
│       ├── Bras → (no L3)
│       ├── Dresses → (no L3)
│       ├── Track Suits → (no L3)
│       ├── Underwear → (no L3)
│       └── Other Apparel → (no L3)
├── Footwear → (no L2/L3)
└── None → (no L2/L3)
```

---

# Null Value Rules

| Field | When NULL is Valid |
|-------|-------------------|
| L1 | Classification failed or not yet performed |
| L2 | L1 is Footwear or None; L1 is Apparel but L2 not determined |
| L3 | L2 does not have L3 sub-categories; L3 not determined |
| Gender | Gender classification not performed or unclear |
| FoP | Field of Play not determined or item is out-of-scope |
| Sub-sport | FoP does not have sub-sports; sub-sport not determined |
