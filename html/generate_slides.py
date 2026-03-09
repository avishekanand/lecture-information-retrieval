import json
import argparse
import os

def generate(chapters, theme="contrast", output_path=None):
    if theme == "contrast":
        if not output_path:
            output_path = '/Users/avishekanand/Projects/Lectures/information-retrieval/html/html-contrast/rag-presentation.html'
        generate_contrast(chapters, output_path)
    elif theme == "white":
        if not output_path:
            output_path = '/Users/avishekanand/Projects/Lectures/information-retrieval/html/theme-white/rag-presentation.html'
        generate_white(chapters, output_path)

def generate_contrast(chapters, output_path):
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Information Retrieval Slides</title>
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
      displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
      processEscapes: true
    },
    svg: { fontCache: 'global' }
  };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  :root {
    --bg-color: #0f111a;
    --text-color: #e2e8f0;
    --accent-color: #38bdf8;
    --accent-secondary: #f43f5e;
    --sidebar-bg: #1e293b;
    --sidebar-text: #94a3b8;
    --sidebar-active: #e2e8f0;
  }
  body, html { margin: 0; padding: 0; height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg-color); color: var(--text-color); overflow: hidden; }
  .app-container { display: flex; height: 100vh; }
  .sidebar { width: 280px; background: var(--sidebar-bg); padding: 2rem 0; display: flex; flex-direction: column; overflow-y: auto; z-index: 10; box-shadow: 2px 0 10px rgba(0,0,0,0.5); }
  .chapter-link { padding: 1rem 1.5rem; cursor: pointer; color: var(--sidebar-text); transition: all 0.2s; font-size: 1.1rem; border-left: 4px solid transparent; }
  .chapter-link:hover { color: var(--sidebar-active); background: rgba(255,255,255,0.05); }
  .chapter-link.active { color: var(--sidebar-active); border-left-color: var(--accent-color); font-weight: bold; background: rgba(0,0,0,0.2); }
  
  .main-content { flex: 1; position: relative; overflow: hidden; }
  .slide-container { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.4s ease; pointer-events: none; padding: 3rem 5rem; box-sizing: border-box; flex-direction: column; }
  .slide-container.active { opacity: 1; pointer-events: auto; z-index: 5; }
  
  .slide-content { max-width: 1400px; width: 100%; text-align: center; display: flex; flex-direction: column; align-items: center; }
  .slide-content.image-layout { max-width: 1600px; }
  
  .slide-content h1 { font-size: 4rem; color: #fff; margin-bottom: 1.5rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.1; }
  .slide-content h2 { font-size: 2.8rem; color: var(--accent-color); margin-bottom: 1.5rem; font-weight: 600; line-height: 1.2; text-align: center;}
  .slide-content p { font-size: 2.1rem; line-height: 1.4; color: #cbd5e1; margin-bottom: 1rem; }
  .slide-content ul, .slide-content ol { text-align: left; display: inline-block; font-size: 2rem; line-height: 1.5; color: #cbd5e1; margin: 0 auto; max-width: 100%; padding-left: 2.5rem; }
  .slide-content li { margin-bottom: 0.8rem; }
  
  .highlight { color: var(--accent-color) !important; font-weight: bold; }
  
  .split-layout { display: flex; gap: 3rem; text-align: left; margin-top: 2rem; align-items: stretch; justify-content: center; width: 100%; height: 100%; }
  .half { flex: 1; background: rgba(255,255,255,0.03); padding: 2.5rem; border-radius: 1rem; border: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; overflow-y: auto; max-height: 60vh; }
  .half h3 { font-size: 2.3rem; color: #fff; margin-top: 0; margin-bottom: 1.5rem; text-align: center; border-bottom: 2px solid rgba(255,255,255,0.1); padding-bottom: 1rem;}
  .half p { font-size: 1.7rem; text-align: left; }
  .half ul { font-size: 1.7rem; line-height: 1.5; padding-left: 2rem; color: #cbd5e1; display: block; }
  
  .progress-container { position: absolute; top: 1.5rem; right: 2rem; font-size: 1.2rem; color: #64748b; font-weight: 600; z-index: 10; font-variant-numeric: tabular-nums; }
  .controls { position: absolute; bottom: 1.5rem; right: 2rem; display: flex; gap: 1rem; z-index: 10; }
  .btn { background: rgba(255,255,255,0.1); border: none; color: white; width: 40px; height: 40px; border-radius: 50%; font-size: 1.2rem; cursor: pointer; transition: background 0.2s; display: flex; align-items: center; justify-content: center; }
  .btn:hover { background: rgba(255,255,255,0.3); }
  
  table { border-collapse: collapse; margin: 2rem auto; font-size: 1.9rem; color: #e2e8f0; width: 90%; background: rgba(255,255,255,0.02); }
  th, td { border: 1px solid rgba(255,255,255,0.1); padding: 1.2rem 1.5rem; text-align: left; }
  th { background: rgba(255,255,255,0.05); color: var(--accent-color); font-weight: bold; border-bottom: 2px solid var(--accent-color); }
  
  .figure-img { max-width: 100%; max-height: 55vh; border-radius: 0.5rem; object-fit: contain; box-shadow: 0 10px 30px rgba(0,0,0,0.5); background: white; padding: 10px; margin: 1rem auto; display: block; }
  .figure-caption { font-size: 1.4rem; color: #94a3b8; font-style: italic; margin-bottom: 2rem; }
  
  code { font-family: monospace; background: rgba(255,255,255,0.1); padding: 0.2rem 0.5rem; border-radius: 0.3rem; color: var(--accent-secondary); }
</style>
</head>
<body>
<div class="app-container">
  <div class="sidebar" id="sidebar"></div>
  <div class="main-content" id="main-content">
    <div class="progress-container"><span id="current">1</span> / <span id="total">1</span></div>
    <div class="controls">
      <button class="btn" id="prev-btn" title="Previous Slide (Left Arrow)">&#8592;</button>
      <button class="btn" id="next-btn" title="Next Slide (Right Arrow)">&#8594;</button>
    </div>
  </div>
</div>

<script>
  const chapters = INJECT_CHAPTERS;
  
  let slides = [];
  let currentSlideIndex = 0;
  
  const sidebarEl = document.getElementById('sidebar');
  const mainContentEl = document.getElementById('main-content');
  const currentEl = document.getElementById('current');
  const totalEl = document.getElementById('total');
  
  function init() {
    let slideIdx = 0;
    chapters.forEach((chapter, cIdx) => {
      const navItem = document.createElement('div');
      navItem.className = 'chapter-link';
      navItem.textContent = chapter.title;
      navItem.dataset.chapter = cIdx;
      navItem.onclick = () => goToSlide(slides.findIndex(s => s.chapterIdx === cIdx));
      sidebarEl.appendChild(navItem);
      
      chapter.slides.forEach(slide => {
        slide.globalIndex = slideIdx++;
        slide.chapterIdx = cIdx;
        slides.push(slide);
        
        const slideEl = document.createElement('div');
        slideEl.className = 'slide-container';
        slideEl.id = 'slide-' + slide.globalIndex;
        
        const isImage = slide.type === 'image';
        let html = `<div class="slide-content ${isImage ? 'image-layout' : ''}">`;
        
        if (slide.type === 'title') {
          html += `<h1>${slide.title}</h1>`;
          if (slide.subtitle) html += `<h2 style="color:var(--text-color); font-weight:400;">${slide.subtitle}</h2>`;
        } else if (slide.type === 'bullet') {
          html += `<h2>${slide.title}</h2>`;
          html += slide.content;
        } else if (slide.type === 'split') {
            html += `<h2>${slide.title}</h2>`;
            html += `<div class="split-layout">
                <div class="half"><h3>${slide.left_title}</h3>${slide.left_content}</div>
                <div class="half"><h3>${slide.right_title}</h3>${slide.right_content}</div>
            </div>`;
            if (slide.bottom) html += `<div style="margin-top:2rem; width:100%;">${slide.bottom}</div>`;
        } else if (slide.type === 'image') {
            html += `<h2>${slide.title}</h2>`;
            html += `<img class="figure-img" src="../${slide.image}" alt="${slide.title}">`;
            if (slide.caption) html += `<div class="figure-caption">${slide.caption}</div>`;
            if (slide.content) html += `<div style="margin-top:1rem; width: 100%;">${slide.content}</div>`;
        }
        
        html += '</div>';
        slideEl.innerHTML = html;
        mainContentEl.appendChild(slideEl);
      });
    });
    
    totalEl.textContent = slides.length;
    goToSlide(0);
    
    document.getElementById('prev-btn').onclick = prevSlide;
    document.getElementById('next-btn').onclick = nextSlide;
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
        if (e.key === 'ArrowLeft') prevSlide();
    });
  }

  function nextSlide() { goToSlide(currentSlideIndex + 1); }
  function prevSlide() { goToSlide(currentSlideIndex - 1); }
  
  function goToSlide(idx) {
    if (idx < 0 || idx >= slides.length) return;
    document.querySelectorAll('.slide-container').forEach(el => el.classList.remove('active'));
    document.getElementById('slide-' + idx).classList.add('active');
    currentSlideIndex = idx;
    currentEl.textContent = idx + 1;
    const chapterIdx = slides[idx].chapterIdx;
    document.querySelectorAll('.chapter-link').forEach(el => {
        el.classList.toggle('active', parseInt(el.dataset.chapter) === chapterIdx);
    });
  }
  
  window.onload = () => {
      init();
      if (window.MathJax) {
          MathJax.typesetPromise().catch((err) => console.log('MathJax error:', err));
      }
  };
</script>
</body>
</html>
"""
    with open(output_path, 'w') as f:
        f.write(html_template.replace('INJECT_CHAPTERS', json.dumps(chapters)))
    print(f"Generated {output_path} successfully!")

def generate_white(chapters, output_path):
    # Get current file name to determine neighbors
    current_file = os.path.basename(output_path)
    lectures = [
        "01_intro_vector_space.html",
        "02_indexing.html",
        "03_ranking.html",
        "04_embeddings_reranking.html",
        "05_dense_retrieval.html"
    ]
    
    prev_lec = ""
    next_lec = ""
    if current_file in lectures:
        idx = lectures.index(current_file)
        if idx > 0: prev_lec = lectures[idx-1]
        if idx < len(lectures) - 1: next_lec = lectures[idx+1]

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Information Retrieval Slides</title>
<link rel="stylesheet" href="node_modules/reveal.js/dist/reveal.css">
<link rel="stylesheet" href="node_modules/reveal.js/dist/theme/serif.css">
<link rel="stylesheet" href="common.css">
<style>
  .reveal h1 { font-size: 1.4em !important; }
  .reveal h2 { font-size: 1.0em !important; color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 8px; }
  .reveal h3 { font-size: 0.75em !important; }
  
  .nav-hint { 
    position: fixed; bottom: 8px; left: 8px; z-index: 99; 
    font-size: 8px; color: #aaa; font-family: sans-serif;
    background: rgba(255,255,255,0.8); padding: 4px; border-radius: 4px;
  }
  .nav-hint a { color: #3498db; text-decoration: none; font-weight: bold; }
</style>
</head>
<body>
<div class="nav-hint">
    <a href="index.html">⌂ Index</a> | 
    Shift + ➔ Next | Shift + ⬅ Prev
</div>
<div class="reveal">
  <div class="slides">
    INJECT_SLIDES
  </div>
</div>
<script src="node_modules/reveal.js/dist/reveal.js"></script>
<script src="node_modules/reveal.js/plugin/math/math.js"></script>
<script>
  Reveal.initialize({
    hash: true,
    plugins: [ RevealMath.KaTeX ]
  });
  
  window.addEventListener('keydown', (e) => {
      if (e.shiftKey && e.key === 'ArrowRight') {
          const next = 'NEXT_LEC_URL';
          if (next) window.location.href = next;
      } else if (e.shiftKey && e.key === 'ArrowLeft') {
          const prev = 'PREV_LEC_URL';
          if (prev) window.location.href = prev;
      } else if (e.key === 'Escape') {
          window.location.href = 'index.html';
      }
  });
</script>
</body>
</html>
""".replace('NEXT_LEC_URL', next_lec).replace('PREV_LEC_URL', prev_lec)
    slides_html = ""
    for chapter in chapters:
        slides_html += '<section>\n'
        for slide in chapter['slides']:
            slides_html += '  <section>\n'
            if slide['type'] == 'title':
                slides_html += f'    <h1>{slide["title"]}</h1>\n'
                if slide.get('subtitle'):
                    slides_html += f'    <h3>{slide["subtitle"]}</h3>\n'
            elif slide['type'] == 'bullet':
                slides_html += f'    <h2>{slide["title"]}</h2>\n'
                slides_html += f'    <div class="content">{slide["content"]}</div>\n'
            elif slide['type'] == 'split':
                slides_html += f'    <h2>{slide["title"]}</h2>\n'
                slides_html += f'    <div class="split-layout">\n'
                slides_html += f'      <div class="half"><h3>{slide["left_title"]}</h3>{slide["left_content"]}</div>\n'
                slides_html += f'      <div class="half"><h3>{slide["right_title"]}</h3>{slide["right_content"]}</div>\n'
                slides_html += f'    </div>\n'
                if slide.get('bottom'):
                    slides_html += f'    <div style="margin-top:0.5em">{slide["bottom"]}</div>\n'
            elif slide['type'] == 'image':
                slides_html += f'    <h2>{slide["title"]}</h2>\n'
                slides_html += f'    <img class="figure-img" src="{slide["image"]}">\n'
                if slide.get('caption'):
                    slides_html += f'    <div class="figure-caption">{slide["caption"]}</div>\n'
                if slide.get('content'):
                    slides_html += f'    <div style="margin-top:0.5em">{slide["content"]}</div>\n'
            slides_html += '  </section>\n'
        slides_html += '</section>\n'

    with open(output_path, 'w') as f:
        f.write(html_template.replace('INJECT_SLIDES', slides_html))
    print(f"Generated {output_path} successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", choices=["contrast", "white"], default="contrast")
    parser.add_argument("--data", help="Path to JSON data file")
    parser.add_argument("--output", help="Path to output HTML file")
    args = parser.parse_args()
    
    if args.data:
        with open(args.data, 'r') as f:
            chapters = json.load(f)
    else:
        # Default RAG content backup
        chapters = [] 
    
    generate(chapters, args.theme, args.output)
