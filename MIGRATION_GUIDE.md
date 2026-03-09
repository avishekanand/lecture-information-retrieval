# Migration Guide: New TikZ Figure System

> [!NOTE]
> **Migration is optional.** All existing figures are supported through a legacy compatibility layer in `theme/tikz-styles.tex`. Use this guide only if you wish to modernize an existing figure or for creating new ones.

This guide explains the differences between the legacy and the new opinionated macro system.

## 1. Box Definitions (`\IRBox`)

**Old System:**
```latex
\IRBox{id}{at}{Title}{Subtitle}{variant}
```
- Depended on `tabular` inside the node.
- Subtitle was `\tiny`.
- No fixed width (boxes resized based on text).

**New System:**
```latex
\IRBox[width]{id}{at}{Title}{Subtitle}{variant}
```
- **Breaking Change**: Now uses `text width` for automatic wrapping.
- Default width is `3.0cm`.
- Subtitle is now `\scriptsize`.
- Uses bold title hierarchy.

**Action**: If your text is very long, it will now wrap instead of making the box giant. If it's too narrow, pass a custom width: `\IRBox[4cm]{...}`.

---

## 2. Arrows and Routing (`\IRArrow`)

**Old System:**
```latex
\IRArrow{from}{to}{label}
```
- Used a direct straight line between node centers (often causing arrows to cross boxes).
- No label background (lines cut through text).

**New System:**
- **`\IRArrow{from}{to}{label}`**: Now defaults to `east -> west` (safe horizontal flow).
- **`\IRArrowTB{from}{to}{label}`**: New macro for `south -> north` (safe vertical flow).
- **`\IRArrowElbow{from anchor}{to anchor}{label}`**: New macro for orthogonal routing (`-|`) to bypass other nodes.
- **Labels**: All labels now have `fill=white` and appropriate padding automatically.

**Action**: Check your vertical arrows! Replace `\IRArrow` with `\IRArrowTB` for top-to-bottom flows. Use `.east`/.`.west` anchors for custom paths.

---

## 3. Style Variants

The semantic meaning of variants has been sharpened:

| Legacy | New Equivalent | Meaning |
|---|---|---|
| `primary` | `sparse` | BM25 / Lexical |
| `accent` | `dense` | Embeddings / Models |
| `secondary` | `rerank` | Re-rankers |
| N/A | `hybrid` | Fusion / Combination |
| N/A | `ann` | Vector infrastructure |

**Action**: Update the style names in your `\IRBox` and `\IRGroup` calls.

---

## 4. Groups and Containers (`\IRGroup`)

**Old System:**
```latex
\IRGroup{nodes}{label}{variant}
```
- Sat very tight against nodes.

**New System:**
- Increased `inner sep` to `0.45cm` to provide breathing room for labels and arrows.

---

## 5. New Semantic Shapes

- **`\IRDocStack{id}{at}{label}`**: Use for document collections.
- **`\IRDatabase{id}{at}{label}`**: Use for indexes or data stores.
- **`\IRStep{id}{at}{title}{subtitle}{variant}`**: Use for numbered architectural steps.
