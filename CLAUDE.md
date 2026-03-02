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

### TikZ Figure Convention
All TikZ figures **must** be extracted to `tikz/<descriptive_name>.tex` and included via `\input{tikz/...}`. Never inline complex figures in the lecture `.tex` files.

### Theme System (`theme/`)
- `macros.tex` — imports `tikz-styles.tex` and defines all custom commands
- `tikz-styles.tex` — color definitions and base TikZ styles

**Semantic colors** (consistent across all lectures):
| Color name | Hex | Meaning |
|---|---|---|
| `irSparse` | `#3498DB` | Sparse/BM25 (blue) |
| `irDense` | `#E67E22` | Dense/Embeddings (orange) |
| `irRerank` | `#C0392B` | Re-ranker/Cross-encoder (red) |
| `irHybrid` | `#2ECC71` | Hybrid/Fusion (green) |
| `irANN` | `#9B59B6` | ANN/Infra (purple) |
| `irInfra` | `#58595B` | General infrastructure (dark gray) |

**Key macros** (defined in `theme/macros.tex`):
- `\IRBox{id}{at}{title}{subtitle}{variant}` — base box node
- `\IRArrow{from}{to}{label}` — styled arrow between nodes
- `\IRBadge{at}{text}` — small accent badge
- `\IRGroup{fit nodes}{label}{variant}` — dashed group container
- `\IRPipelineTier{id}{at}{text}{label}{variant}` — pipeline stage with side label
- `\IRTelescopeTier{id}{at}{width}{text}{variant}` — trapezoid for funnel diagrams
- `\irStage{name}` — corner badge overlay (top-right of slide)
- `\mathhl[color]{content}` — colored math highlight box

**TikZ variants** (use as node styles): `sparse`, `dense`, `rerank`, `hybrid`, `ann`, `infra`, `muted`, `ghost`, `emph`

### Overflow Handling
Frames with too much content use `[shrink=N]` on the `\begin{frame}` — always check beamer's shrink warnings after building. N% must cover actual overflow; increase if the warning shows a higher percentage required.

## Content Reference

`contents.md` — complete concept tracker for all 6 lectures (useful for cross-referencing terminology and notation).

`master.bib` — BibTeX references for all citations used across lectures.
