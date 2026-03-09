# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

LaTeX/Beamer slides for a 6-lecture Information Retrieval course. The project uses the TU Delft Beamer theme with a custom TikZ macro library.

## Build Commands

```bash
# Build all lectures (animated + static)
make all

# Build only animated versions
make animated

# Build only static (handout) versions
make static

# Clean build artifacts
make clean

# Build a single lecture (animated)
pdflatex -interaction=nonstopmode -output-directory=build 04_embeddings_reranking.tex
pdflatex -interaction=nonstopmode -output-directory=build 04_embeddings_reranking.tex  # run twice for refs

# Build a single lecture (static/handout)
pdflatex -jobname=04_embeddings_reranking_static -output-directory=build \
  "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{04_embeddings_reranking.tex}"
```

PDFs go to `build/`. The Makefile runs pdflatex twice to resolve cross-references.

## Active vs In-Development Lectures

- **Active** (compiled by `make`): `01_intro_vector_space.tex` through `06-ltr.tex`
- **In-development** (not compiled by default): `in-development/` — includes `05_dense_retrieval.tex`, `06_learning_to_rank.tex`, `07-rag.tex`

## Architecture

### Lecture Structure
Each `.tex` file is a self-contained Beamer document using `\documentclass[aspectratio=169]{beamer}` with `\usetheme{TUDelft}`. All lectures follow the same preamble pattern (see `04_embeddings_reranking.tex` lines 1–54).

### Animation Toggle
Every lecture defines `\cpause` — use this instead of `\pause` so static builds collapse all animations:
```latex
\newif\ifanimated
\animatedtrue
\ifdefined\staticmode \animatedfalse \fi
\newcommand{\cpause}{\ifanimated\pause\fi}
```

## TikZ Figure Convention for IR Lecture Slides

This repository uses a consistent TikZ figure system. All non-trivial TikZ figures must be extracted into `tikz/<descriptive_name>.tex` and included via `\input{tikz/...}`.

### 1. Core Principles
- **Layout Safety First**: No text spilling, no arrows through boxes, no labels on top of shapes.
- **Fixed Geometry**: All normal boxes use `text width`, `align=center`, and `minimum height` to prevent content-dependent explosions.
- **Relatively Positioned**: Prefer `right=of` over raw coordinates whenever possible.
- **Explicit Anchors**: Use `a.east` to `b.west` for horizontal flow, or `a.south` to `b.north` for vertical.

### 2. Semantic Color & Style System
Use these variants for boxes (defined in `tikz-styles.tex`):

| Node Variant | Meaning |
|---|---|
| `sparse` | Lexical / BM25 (#3498DB) |
| `dense` | Embeddings / Transformers (#E67E22) |
| `rerank` | Cross-encoder / Ranking (#C0392B) |
| `hybrid` | Fusion / Combination (#2ECC71) |
| `ann` | Vector indexing / ANN (#9B59B6) |
| `infra` | General infrastructure (#58595B) |
| `muted` | Background or inactive elements |
| `ghost` | Very light, placeholder elements |
| `emph` | Highlighted / Focus element |

### 3. Approved Macros (from `theme/macros.tex`)
- `\IRBox[width]{id}{at}{title}{subtitle}{variant}`: Width-controlled node with emboldened title and scriptsize subtitle.
- `\IRArrow{from}{to}{label}`: Safe horizontal flow (east to west).
- `\IRArrowTB{from}{to}{label}`: Safe vertical flow (south to north).
- `\IRArrowElbow{from anchor}{to anchor}{label}`: Orthogonal routing to bypass nodes.
- `\IRGroup{fit nodes}{label}{variant}`: Dotted group container with safe inner-sep.
- `\IRDocStack{id}{at}{label}`: Standard document stack icon.
- `\IRDatabase{id}{at}{label}`: Standard database icon.
- `\IRTelescopeTier{id}{at}{width}{text}{variant}`: Re-ranking funnel tier.
- `\irStage{name}`: Slide-corner badge overlay.

### 4. Authoring Workflow
1. Place boxes using relative positioning.
2. Verify text wrapping and subtitles.
3. Add arrows using explicit anchors (`.east`, `.west`).
4. Replace straight lines with `Elbow` routing if they cross nodes.
5. Add labels (macros provide a white background fill for readability).
6. Wrap related nodes in an `IRGroup` last.

## Overflow Handling
Frames with too much content use `[shrink=N]`. However, do not use shrink to hide poor figure design; fix text wrapping or split into overlays first.

## Content Reference

`contents.md` — complete concept tracker for all 6 lectures (useful for cross-referencing terminology and notation).

`master.bib` — BibTeX references for all citations used across lectures.
