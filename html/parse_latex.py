import re
import json
import os
import hashlib

def protect_math(text):
    math_map = {}
    
    def repl_display(match):
        placeholder = f"__MATH_DISPLAY_{len(math_map)}__"
        math_map[placeholder] = match.group(0)
        return placeholder

    def repl_inline(match):
        placeholder = f"__MATH_INLINE_{len(math_map)}__"
        math_map[placeholder] = match.group(0)
        return placeholder

    # Use regex to find $...$ and $$...$$
    # Be careful with escaped \$
    text = re.sub(r'\$\$(.*?)\$\$', repl_display, text, flags=re.DOTALL)
    text = re.sub(r'(?<!\\)\$(.*?)(?<!\\)\$', repl_inline, text)
    
    return text, math_map

def restore_math(text, math_map):
    for placeholder, original in math_map.items():
        text = text.replace(placeholder, original)
    return text

def parse_table(latex_table):
    # Strip booktabs commands and other formatting noise often found in tables
    latex_table = re.sub(r'\\(?:toprule|midrule|bottomrule|cmidrule\{.*?\}|hline|vfill|hfill|hspace\{.*?\}|vspace\{.*?\})', '', latex_table)
    
    rows = []
    # Find all rows (separated by \\)
    # We use a more robust split that handles optional arguments like \\[5pt]
    latex_rows = re.split(r'\\\\(?:\s*\[.*?\])?', latex_table)
    for row in latex_rows:
        row = row.strip()
        if not row: continue
        # Split by &
        cols = [clean_latex(c.strip()) for c in row.split('&')]
        # Filter out empty columns often caused by trailing &
        cols = [c for c in cols if c or len(cols) == 1]
        if cols:
            rows.append(cols)
    
    if not rows: return ""
    
    html = "<table>"
    for i, row in enumerate(rows):
        html += "<tr>"
        tag = "th" if i == 0 else "td"
        for col in row:
            # Check for \multicolumn in the raw content before it was cleaned
            # Note: clean_latex might have already run on it in cols comprehension
            # We need to detect it. Let's re-parse multicolumn here if needed.
            colspan = ""
            mc_match = re.search(r'\\multicolumn\{(\d+)\}\{.*?\}\{(.*?)\}', col)
            if mc_match:
                colspan = f' colspan="{mc_match.group(1)}"'
                col = mc_match.group(2)
            
            html += f"<{tag}{colspan}>{col}</{tag}>"
        html += "</tr>"
    html += "</table>"
    return html

def parse_lists(text):
    def repl_itemize(match):
        inner = match.group(1)
        inner = handle_list_items(inner, "ul")
        return f"<ul>{inner}</ul>"

    def repl_enumerate(match):
        inner = match.group(1)
        inner = handle_list_items(inner, "ol")
        return f"<ol>{inner}</ol>"

    def handle_list_items(content, tag):
        items = re.split(r'\\item\s+', content)
        res = ""
        for i, item in enumerate(items):
            if i == 0: 
                # This could be text before the first \item
                text_before = item.strip()
                if text_before:
                    res += f"<div>{clean_latex(text_before)}</div>"
                continue
            item_content = item.strip()
            res += f"<li>{clean_latex(item_content)}</li>"
        return res

    text = re.sub(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', repl_itemize, text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{enumerate\}(.*?)\\end\{enumerate\}', repl_enumerate, text, flags=re.DOTALL)
    
    return text

# Global list to store extracted TikZ for compilation
EXTRACTED_TIKZ = []

def clean_latex(text):
    if not text:
        return ""
    
    # Protect math before cleaning
    text, math_map = protect_math(text)
    
    # Handle TikZ (Inline)
    def repl_tikz(match):
        tikz_content = match.group(0)
        # Create a hash for the filename
        h = hashlib.md5(tikz_content.group(0).encode('utf-8')).hexdigest()[:10] if hasattr(tikz_content, 'group') else hashlib.md5(tikz_content.encode('utf-8')).hexdigest()[:10]
        filename = f"inline_{h}.png"
        EXTRACTED_TIKZ.append({"content": tikz_content, "filename": f"inline_{h}.tex"})
        return f'<img class="tikz-img" src="assets/{filename}" alt="Inline TikZ">'

    text = re.sub(r'\\begin\{tikzpicture\}(.*?)\\end\{tikzpicture\}', repl_tikz, text, flags=re.DOTALL)

    # Handle basic formatting early
    text = re.sub(r'\\textbf\{(.*?)\}', r'<strong>\1</strong>', text)
    text = re.sub(r'\\textit\{(.*?)\}', r'<em>\1</em>', text)
    text = re.sub(r'\\texttt\{(.*?)\}', r'<code>\1</code>', text)
    text = re.sub(r'\\mathhl\{(.*?)\}', r'<span class="highlight">\1</span>', text)
    
    # Unescape characters
    text = text.replace('\\&', '&').replace('\\#', '#').replace('\\_', '_').replace('\\%', '%')
    
    # Handle Tables - MOVE BEFORE GENERIC STRIPPING
    def repl_table(match):
        return parse_table(match.group(1))
    
    text = re.sub(r'\\begin\{tabular\}(?:\{.*?\})?(.*?)\\end\{tabular\}', repl_table, text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{table\}(?:\[.*?\])?(.*?)\\end\{table\}', r'\1', text, flags=re.DOTALL)

    # Handle TikZ/Input
    def repl_input(match):
        path = match.group(1)
        name = os.path.basename(path).replace(".tex", "")
        return f'<img class="tikz-img" src="assets/{name}.png" alt="{name}">'
    
    text = re.sub(r'\\input\{(.*?)\}', repl_input, text)
    
    # Heuristic: if a word like "Prompt:" precedes a tcolorbox, treat it as the title
    text = re.sub(r'(\w+:)\s*\\begin\{tcolorbox\}', r'\\begin{tcolorbox}[title={\1}]', text)
    
    # Handle tcolorbox (e.g. for Prompts)
    def repl_tcolorbox(match):
        args = match.group(1)
        content = match.group(2)
        # Try to find a title in the arguments
        title = "Box"
        title_match = re.search(r'title=\{(.*?)\}', args)
        if title_match:
            title = title_match.group(1)
        elif "Prompt" in content[:20]:
            # Heuristic: if it looks like a prompt, label it
            title = "Prompt"
        
        # Clean the args from the content just in case the regex missed it
        content = re.sub(r'^\[.*?\]\s*', '', content.strip())
        return f'<div class="block"><h3>{clean_latex(title)}</h3><div class="block-content">{clean_latex(content)}</div></div>'

    text = re.sub(r'\\begin\{tcolorbox\}(?:\[(.*?)\])?(.*?)\\end\{tcolorbox\}', repl_tcolorbox, text, flags=re.DOTALL)

    # Handle environment blocks
    def repl_block(match):
        b_type = match.group(1)
        b_title = clean_latex(match.group(2))
        b_content = clean_latex(match.group(3))
        cls = "block"
        if "alert" in b_type: cls = "alert-block"
        elif "example" in b_type: cls = "example-block"
        return f'<div class="{cls}"><h3>{b_title}</h3><div class="block-content">{b_content}</div></div>'

    text = re.sub(r'\\begin\{(block|alertblock|exampleblock)\}\{(.*?)\}(.*?)\\end\{\1\}', repl_block, text, flags=re.DOTALL)

    # Handle Lists
    text = parse_lists(text)

    # Strip orphan \item tags
    text = re.sub(r'\\item\s+', '• ', text)

    # NOW strip generic formatting commands to avoid breaking table logic
    commands_to_remove = [
        r'\\small', r'\\large', r'\\footnotesize', r'\\scriptsize', r'\\tiny',
        r'\\huge', r'\\Huge', r'\\centering', r'\\center', r'\\right', r'\\left',
        r'\\vspace\{.*?\}', r'\\hspace\{.*?\}', r'\\newline', r'\\\\',
        r'\\cpause', r'\\pause', r'\\hfill', r'\\vfill',
        r'\\column(?:.*?)', r'\\minipage(?:.*?)', r'\\endminipage',
        r'\\textwidth', r'\\linewidth', r'\\textheight'
    ]
    for cmd in commands_to_remove:
        text = re.sub(cmd, '', text)

    # Strip layout-related curly brace artifacts like {0.5}, {0.33}, etc.
    # We use word boundaries or space checks to avoid stripping math content {} which is protected
    text = re.sub(r'(?<![\$])\{\d+(?:\.\d+)?\}(?!\$)', '', text)
    
    # Strip tcolorbox / beamer layout artifacts in brackets like [colback=...] or [fragile]
    # More aggressive to catch the "Prompt" block artifact
    text = re.sub(r'\[(?:colback|colframe|fontupper|title|top|bottom|left|right|arc|boxrule|sharp corners|rounded corners|width|height|valign|halign|center|fragile|coltitle|fonttitle).*?\]', '', text, flags=re.IGNORECASE)
    
    # Final pass to strip all lingering \begin and \end tags
    text = re.sub(r'\\begin\{.*?\}', '', text)
    text = re.sub(r'\\end\{.*?\}', '', text)
    
    # Handle specific multi-arg commands to keep content
    # \textcolor{color}{text} -> text
    text = re.sub(r'\\textcolor\{.*?\}\{(.*?)\}', r'\1', text)
    # \multicolumn{n}{c}{text} -> text (already handled in parse_table but good for generic text)
    text = re.sub(r'\\multicolumn\{\d+\}\{.*?\}\{(.*?)\}', r'\1', text)
    
    # Map common symbols
    symbol_map = {
        r'\\checkmark': '✓',
        r'\\ding\{51\}': '✓',
        r'\\ding\{52\}': '✓',
        r'\\ding\{53\}': '✗',
        r'\\ding\{54\}': '✗',
        r'\\ding\{55\}': '✗',
        r'\\ding\{56\}': '✗',
    }
    for macro, char in symbol_map.items():
        text = re.sub(macro, char, text)

    # Strip common macros with arguments that we want to remove entirely
    text = re.sub(r'\\(?:ding|color|href|cite|ref|url|setbeamercolor|setbeamertemplate|usebeamertemplate|setbeamerfont)\{.*?\}', '', text)
    # Strip any remaining macros (e.g. \small, \vfill)
    text = re.sub(r'\\[a-zA-Z]+', '', text)

    # Strip empty curly braces {} and lingering single braces from stripped multi-arg commands
    text = text.replace('{}', '')
    # Strip any text that is just a number in braces like {3} or {c} left by stripped multicolumn
    text = re.sub(r'\{\w+\}', '', text)

    # Restore math
    text = restore_math(text, math_map)
    
    return text.strip()

def parse_latex(file_path):
    global EXTRACTED_TIKZ
    EXTRACTED_TIKZ = [] # Reset for each file
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove comments
    content = re.sub(r'(?<!\\)%.*', '', content)

    chapters = []
    sections = re.split(r'\\section\{', content)
    
    if len(sections) <= 1:
        title_match = re.search(r'\\title(?:\[.*?\])?\{(.*?)\}', content)
        main_title = title_match.group(1).replace('\\\\', ' ') if title_match else os.path.basename(file_path)
        sections = ["", main_title + "}" + content]

    for section in sections[1:]:
        if '}' not in section: continue
        section_title, section_content = section.split('}', 1)
        
        current_chapter = {
            "title": clean_latex(section_title.strip()),
            "slides": []
        }
        
        frames = re.findall(r'\\begin\{frame\}(?:\[.*?\])?(?:\{(.*?)\})?(.*?)\\end\{frame\}', section_content, re.DOTALL)
        
        for frame_title, frame_body in frames:
            frame_title = clean_latex(frame_title.strip()) if frame_title else ""
            
            if "\\titlepage" in frame_body:
                slide = {"type": "title", "title": frame_title, "content": ""}
                t_match = re.search(r'\\title(?:\[.*?\])?\{(.*?)\}', content)
                st_match = re.search(r'\\subtitle\{(.*?)\}', content)
                slide["title"] = clean_latex(t_match.group(1)) if t_match else frame_title
                slide["subtitle"] = clean_latex(st_match.group(1)) if st_match else ""
                current_chapter["slides"].append(slide)
                continue

            if "\\sectionpage" in frame_body or "\\tableofcontents" in frame_body:
                continue

            # Check for figures (includegraphics or tikz)
            has_img = re.search(r'\\includegraphics(?:\[.*?\])?\{(.*?)\}', frame_body)
            has_tikz = re.search(r'\\input\{tikz/.*?\}', frame_body) or "\\begin{tikzpicture}" in frame_body
            
            if (has_img or has_tikz):
                # Split content into text and figure
                # First, extract the figure
                fig_html = ""
                body_no_fig = frame_body
                
                if has_img:
                    img_path = has_img.group(1)
                    if img_path.startswith("figures/"):
                        img_path = "assets/" + img_path.split("/")[-1]
                    if img_path.endswith(".pdf"):
                        img_path = img_path.replace(".pdf", ".png")
                    elif "." not in os.path.basename(img_path):
                        img_path += ".png"
                    fig_html = f'<img class="figure-img" src="{img_path}" alt="Figure">'
                    body_no_fig = re.sub(r'\\includegraphics(?:\[.*?\])?\{.*?\}', '', body_no_fig)
                elif has_tikz:
                    # tikz is handled by clean_latex which returns <img> tags
                    # We need to temporarily extract it
                    tikz_match = re.search(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}|\\input\{tikz/.*?\}', body_no_fig, re.DOTALL)
                    if tikz_match:
                        fig_html = clean_latex(tikz_match.group(0))
                        body_no_fig = body_no_fig.replace(tikz_match.group(0), '')

                # Clean the text part
                text_content = clean_latex(body_no_fig.strip())
                
                # If there's significant text, create a text slide first
                if text_content and len(text_content) > 20: 
                    current_chapter["slides"].append({
                        "type": "bullet",
                        "title": frame_title,
                        "content": text_content
                    })
                
                # Create a dedicated figure slide
                current_chapter["slides"].append({
                    "type": "bullet", # Use bullet type but content is just the image
                    "title": frame_title + " (Figure)" if text_content else frame_title,
                    "content": f'<div class="h-center">{fig_html}</div>'
                })
                continue

            # Standard slide handling
            slide = {"type": "bullet", "title": frame_title, "content": ""}
            if "\\begin{columns}" in frame_body:
                slide["type"] = "split"
                cols = re.findall(r'\\begin\{column\}(?:\[.*?\])?\{(.*?)\}(.*?)\\end\{column\}', frame_body, re.DOTALL)
                if len(cols) >= 2:
                    slide["left_title"] = ""
                    slide["left_content"] = clean_latex(cols[0][1].strip())
                    slide["right_title"] = ""
                    slide["right_content"] = clean_latex(cols[1][1].strip())
                    slide["bottom"] = ""
                    current_chapter["slides"].append(slide)
                    continue

            slide["content"] = clean_latex(frame_body.strip())
            if slide["title"] or slide["content"]:
                current_chapter["slides"].append(slide)
        
        if current_chapter["slides"]:
            chapters.append(current_chapter)
            
    return chapters, EXTRACTED_TIKZ

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 parse_latex.py <latex_file>")
        sys.exit(1)
    
    data, extracted_tikz = parse_latex(sys.argv[1])
    # Write extracted TikZ to a temp file for compile_tikz.py to find
    if extracted_tikz:
        with open("extracted_tikz.json", "w") as f:
            json.dump(extracted_tikz, f)
    
    print(json.dumps(data, indent=2))
