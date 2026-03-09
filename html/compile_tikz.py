import os
import subprocess
import json
import hashlib

tikz_dir = "../tikz"
assets_dir = "assets"
temp_dir = "temp_tikz"
extracted_json = "extracted_tikz.json"

os.makedirs(temp_dir, exist_ok=True)
os.makedirs(assets_dir, exist_ok=True)

standalone_template = r"""
\documentclass[tikz,border=2pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{amsfonts}
\usepackage{xcolor}
\usetikzlibrary{arrows.meta,positioning,calc,shapes,decorations.pathreplacing}
% Define some common colors used in IR lectures if any
\definecolor{sparse}{rgb}{0.8,0.8,1}
\definecolor{dense}{rgb}{1,0.8,0.8}
\begin{document}
TIKZ_CONTENT
\end{document}
"""

def compile_tikz(content, filename):
    name = filename.replace(".tex", "")
    wrapper_name = f"wrap_{name}"
    wrapper_tex = f"{wrapper_name}.tex"
    wrapper_path = os.path.join(temp_dir, wrapper_tex)
    
    # Check if content is a file path or raw TikZ
    if content.endswith(".tex") and os.path.exists(os.path.join(tikz_dir, content)):
        with open(os.path.join(tikz_dir, content), "r") as f:
            tikz_body = f"\\input{{{os.path.abspath(os.path.join(tikz_dir, content))}}}"
    else:
        tikz_body = content

    with open(wrapper_path, "w") as f:
        f.write(standalone_template.replace("TIKZ_CONTENT", tikz_body))
    
    print(f"Compiling {filename}...")
    
    try:
        subprocess.run([
            "pdflatex", 
            "-interaction=nonstopmode", 
            wrapper_tex
        ], cwd=temp_dir, capture_output=True)
        
        pdf_path = os.path.join(temp_dir, f"{wrapper_name}.pdf")
        if not os.path.exists(pdf_path):
            print(f"Error: PDF not generated for {filename}")
            return False

        png_path = os.path.join(assets_dir, name + ".png")
        
        subprocess.run([
            "magick", 
            "-density", "300", 
            pdf_path, 
            "-background", "white",
            "-alpha", "remove",
            "-flatten",
            png_path
        ], check=True)
        
        print(f"Successfully converted {filename} to {png_path}")
        return True
    except Exception as e:
        print(f"Failed to process {filename}: {str(e)}")
        return False

def process_extracted():
    if not os.path.exists(extracted_json):
        return
    
    with open(extracted_json, "r") as f:
        extracted = json.load(f)
    
    for item in extracted:
        compile_tikz(item["content"], item["filename"])
    
    # Clean up after processing
    os.remove(extracted_json)

if __name__ == "__main__":
    import sys
    # If a filename is passed, compile it from ../tikz/
    if len(sys.argv) > 1:
        f = sys.argv[1]
        compile_tikz(f, f)
    else:
        # Check for extracted json
        process_extracted()
        # Also process all in tikz_dir if requested or just do specific ones
        # For this task, we want to ensure everything is covered
        files = [f for f in os.listdir(tikz_dir) if f.endswith(".tex")]
        for f in files:
            compile_tikz(f, f)
