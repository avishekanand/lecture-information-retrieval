# Lecture Style Guide — Information Retrieval Course

This document defines the formatting conventions, structure, and quality standards for all lecture files in this repository.

## File Naming Convention

- **Format**: `XX_topic_name.tex` (e.g., `01_intro_vector_space.tex`, `02_indexing.tex`, `03_ranking.tex`)
- **No hyphens**: Use underscores only
- **Lowercase**: All filenames should be lowercase
- **Two-digit prefix**: Lecture numbers should be zero-padded (01, 02, 03, etc.)

## Document Structure

### 1. Preamble (Lines 1-60)

```latex
\documentclass[aspectratio=169]{beamer}

% Core packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{tikz}
\usepackage{tcolorbox}
\usepackage{pifont}

% TikZ libraries (REQUIRED)
\usetikzlibrary{shapes,arrows,positioning,calc,decorations.pathreplacing}

% Custom colors (REQUIRED)
\definecolor{sparse}{RGB}{52,152,219}    % Blue
\definecolor{dense}{RGB}{231,76,60}      % Red
\definecolor{hybrid}{RGB}{46,204,113}    % Green

% Import theme macros (REQUIRED)
\input{theme/macros.tex}

% Title information
\title[Short Title]{Full Lecture Title}
\subtitle{Lecture X: Specific Topic}
\author{Your Name}
\date{\today}
```

### 2. Document Body Structure

```latex
\begin{document}

% Title slide
\begin{frame}[plain]
\titlepage
\end{frame}

% Outline
\begin{frame}{Outline}
\tableofcontents
\end{frame}

% Section 1
\section{Section Name}

\begin{frame}[plain]
\sectionpage
\end{frame}

% Content frames...

\end{document}
```

## Section Organization

### Section Slides (REQUIRED)

Every `\section{...}` command **must** be followed by a section slide:

```latex
\section{Section Name}

\begin{frame}[plain]
\sectionpage
\end{frame}
```

This creates a visual break between major topics.

### Recommended Section Structure

1. **Introduction/Motivation** — Why this topic matters
2. **Core Concept 1** — Main theoretical content
3. **Core Concept 2** — Additional theoretical content
4. **Hands-On/Examples** — Practical demonstrations
5. **Connections** — Links to other lectures
6. **Summary** — Key takeaways and assignment

## TikZ Figures

### Extraction Rule

**All TikZ figures must be in separate files** in the `tikz/` directory.

❌ **Bad** (inline):
```latex
\begin{frame}{Example}
\begin{tikzpicture}
    \node[draw] (a) {A};
    \node[draw] (b) [right=of a] {B};
    \draw[->] (a) -- (b);
\end{tikzpicture}
\end{frame}
```

✅ **Good** (external file):
```latex
\begin{frame}{Example}
\input{tikz/example_diagram.tex}
\end{frame}
```

### TikZ File Naming

- **Format**: `descriptive_name.tex` (e.g., `tf_saturation_comparison.tex`, `rocchio_geometric.tex`)
- **Lowercase with underscores**
- **Descriptive**: Name should indicate what the figure shows
- **No frame wrapper**: TikZ files should contain only the `tikzpicture` environment

### TikZ File Template

```latex
\begin{tikzpicture}[
    node distance=1cm,
    box/.style={rectangle, draw, rounded corners, text width=3cm, align=center},
    arrow/.style={->, thick}
]
    % Figure content here
\end{tikzpicture}
```

## Animations

### Animation Control

Use `\pause` for simple animations:

```latex
\begin{frame}{Example}
\begin{itemize}
    \item First point \pause
    \item Second point \pause
    \item Third point
\end{itemize}
\end{frame}
```

### Static Mode Support

The build system supports both animated and static versions. No special handling needed in the source file.

### Animation Best Practices

1. **Don't overuse**: Use animations to reveal information progressively, not on every slide
2. **Logical progression**: Reveal items in the order they're discussed
3. **Group related items**: Don't pause between tightly related points
4. **Complex slides**: Use `\pause` to break down complex formulas or diagrams

## Frame Options

### Shrink for Dense Content

If a frame has too much content (overfull vbox warning), add `[shrink=X]`:

```latex
\begin{frame}[shrink=5]{Dense Content}
% Lots of content here
\end{frame}
```

- `shrink=5`: Mild reduction (5% smaller)
- `shrink=10`: Moderate reduction (10% smaller)
- `shrink=15`: Aggressive reduction (use sparingly)

### Fragile for Verbatim

Use `[fragile]` for frames with code listings:

```latex
\begin{frame}[fragile]{Code Example}
\begin{lstlisting}[language=Python]
def example():
    return "Hello"
\end{lstlisting}
\end{frame}
```

### Plain for Section Slides

Section slides should always use `[plain]`:

```latex
\begin{frame}[plain]
\sectionpage
\end{frame}
```

## Code Listings

### Standard Style

```latex
\begin{lstlisting}[language=Python]
import pyterrier as pt
pt.init()

# Your code here
\end{lstlisting}
```

### Supported Languages

- `Python`
- `Java`
- `SQL`
- `bash`

## Blocks and Alerts

### Standard Block

```latex
\begin{block}{Title}
Content here
\end{block}
```

### Example Block (Green)

```latex
\begin{exampleblock}{Example}
Example content
\end{exampleblock}
```

### Alert Block (Red)

```latex
\begin{alertblock}{Warning}
Important warning or limitation
\end{alertblock}
```

## Quality Checks

### Pre-Compilation Checklist

Before committing a lecture file, verify:

- [ ] All TikZ figures extracted to `tikz/` directory
- [ ] Section slides added after each `\section{...}`
- [ ] Theme macros imported (`\input{theme/macros.tex}`)
- [ ] Custom colors defined (sparse, dense, hybrid)
- [ ] TikZ libraries imported
- [ ] File named correctly (`XX_topic.tex`)

### Compilation Checks

Run both compilation targets and verify:

```bash
# Animated version
pdflatex -jobname=XX_topic_animated -output-directory=build XX_topic.tex

# Static version
pdflatex -jobname=XX_topic_static -output-directory=build "\def\staticmode{1} \input{XX_topic.tex}"
```

Check for:

1. **No overfull boxes**: Add `[shrink=X]` to problematic frames
2. **No underfull boxes**: Adjust spacing or content
3. **No missing references**: All `\input{tikz/...}` files exist
4. **Correct page count**: Verify animated vs static versions
5. **Visual inspection**: Check section slides appear correctly

### Overfull Box Resolution

If you see warnings like:
```
Overfull \vbox (19.8769pt too high) detected at line 123
```

**Solutions** (in order of preference):

1. **Add shrink option**: `\begin{frame}[shrink=5]{...}`
2. **Use smaller font**: Wrap content in `{\small ...}` or `{\footnotesize ...}`
3. **Break content**: Split into multiple frames
4. **Reduce spacing**: Use `\vspace{-0.5em}` judiciously

### Common Warnings to Ignore

- `Package hyperref Warning: Token not allowed in a PDF string` — Safe to ignore
- `LaTeX Font Warning: Size substitutions with differences` — Cosmetic only
- Beamer warnings about `\headheight` — Not critical for slides

## Makefile Integration

### Adding a New Lecture

Edit `Makefile` and add to `ACTIVE_LECTURES`:

```makefile
ACTIVE_LECTURES = 01_intro_vector_space.tex 02_indexing.tex 03_ranking.tex 04_new_lecture.tex
```

### Build Commands

```bash
make                 # Build all (animated + static)
make animated        # Build only animated versions
make static          # Build only static versions
make clean           # Remove all build artifacts
```

## Pedagogical Guidelines

### Section Ordering

Consider the logical flow:

1. **Foundation first**: Introduce basic concepts before advanced ones
2. **Dependencies**: Ensure prerequisites are covered earlier
3. **Examples after theory**: Show applications after explaining concepts
4. **Hands-on near end**: Practical exercises after theoretical coverage

### Example: Ranking Lecture

✅ **Good order**:
1. BM25 (foundation)
2. Language Models (theoretical framework)
3. Query Expansion (applies language models)
4. Hands-on (practice with all concepts)

❌ **Bad order**:
1. BM25
2. Query Expansion (mentions RM3 without LM background)
3. Language Models (too late for RM3 understanding)

## Common Patterns

### Two-Column Layout

```latex
\begin{columns}
\begin{column}{0.48\textwidth}
Left content
\end{column}

\begin{column}{0.48\textwidth}
Right content
\end{column}
\end{columns}
```

### Itemized Lists with Icons

```latex
\begin{itemize}
    \item \textcolor{green}{\checkmark} Advantage
    \item \textcolor{red}{\ding{55}} Limitation
\end{itemize}
```

### Formulas in Blocks

```latex
\begin{block}{Formula Name}
$$\text{BM25}(q,d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{f(t,d) \cdot (k_1+1)}{f(t,d) + k_1}$$
\end{block}
```

## Version Control

### Commit Messages

Use descriptive commit messages:

- ✅ `Add lecture 4 on embeddings and re-ranking`
- ✅ `Fix overfull boxes in lecture 3`
- ✅ `Extract TikZ figures to separate files`
- ❌ `Update files`
- ❌ `WIP`

### What to Commit

**Include**:
- `.tex` source files
- `tikz/*.tex` figure files
- `Makefile` updates
- `contents.md` updates

**Exclude** (in `.gitignore`):
- `build/*.pdf`
- `build/*.aux`, `*.log`, `*.nav`, `*.out`, `*.toc`, `*.vrb`
- Temporary files

## Summary Checklist

When creating or refactoring a lecture:

1. ✅ Follow file naming convention
2. ✅ Import theme and define colors
3. ✅ Extract all TikZ to separate files
4. ✅ Add section slides after each `\section{...}`
5. ✅ Add animations thoughtfully with `\pause`
6. ✅ Compile both animated and static versions
7. ✅ Fix all overfull/underfull box warnings
8. ✅ Visual inspection of section slides
9. ✅ Update Makefile if new lecture
10. ✅ Update `contents.md` with lecture summary
