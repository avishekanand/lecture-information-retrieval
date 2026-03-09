# Slides

This repository contains slides for my presentations. The corresponding links can be found [here](https://mrjleo.github.io/publications/).

## Local Development

Clone the repository and run the commands below.

### Using Docker

Simply run:

```
docker compose up --watch
```

Navigate your browser to http://localhost:8101/.

### Without Docker

Install the dependencies:

- [node.js](https://nodejs.org/en/)
- [pdf2svg](https://github.com/dawbarton/pdf2svg)
- [Inconsolata (font)](https://fonts.google.com/specimen/Inconsolata)
- [Libertine (font)](https://libertine-fonts.org/)
- A LaTeX distribution, e.g., [TeX Live](https://tug.org/texlive/)

Install the node modules:

```
npm install
```

Compile the LaTeX figues (this only needs to be done once):

```
npm run compile_latex
```

In order to work with live reloading, start a local server:

```
npm start
```

Navigate your browser to http://localhost:8101/.

## Libraries

- [reveal.js](https://revealjs.com/)
- [charts.css](https://chartscss.org/)
- [KaTeX](https://katex.org/)
- [PGF/TikZ](https://ctan.org/pkg/pgf)
- [PGFPlots](https://ctan.org/pkg/pgfplots)

## Attribution

Some slides contain icons created by [juicy_fish](https://www.flaticon.com/authors/juicy-fish/) ([Flaticon](https://www.flaticon.com/)).
