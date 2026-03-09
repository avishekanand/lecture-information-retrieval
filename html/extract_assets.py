import os
import re
import subprocess
import shutil

TEX_FILE = "../07-rag.tex"
ASSETS_DIR = "assets"
FIGURES_DIR = "../figures"
ABS_HTML_DIR = os.path.abspath(".")

os.makedirs(ASSETS_DIR, exist_ok=True)

print("Converting existing figures...")
# 1. Copy all PDF figures from ../figures and convert to PNG using sips (macOS)
for f in os.listdir(FIGURES_DIR):
    if f.endswith(".pdf"):
        src = os.path.join(FIGURES_DIR, f)
        dst_png = os.path.join(ASSETS_DIR, f.replace(".pdf", ".png"))
        
        try:
            subprocess.run(["sips", "-s", "format", "png", src, "--out", dst_png], check=True, stdout=subprocess.DEVNULL)
            print(f"Converted {f} to PNG")
        except Exception as e:
            print(f"Failed to convert {f}: {e}")

print("Extracting and compiling TikZ figures...")
# 2. Extract TikZ figures by creating standalone temp tex files and compiling them
with open(TEX_FILE, "r") as f:
    content = f.read()

tikz_inputs = re.findall(r'\\input\{(tikz/.*?\.tex)\}', content)

preamble = """\\documentclass[tikz, border=2mm]{standalone}
\\usepackage{xcolor}
\\input{theme/macros.tex}
\\colorlet{retrieval}{irSparse}
\\colorlet{prompt}{irDense}
\\colorlet{gen}{irRerank}
\\colorlet{ops}{irANN}
\\colorlet{warn}{irInfra}
\\usetikzlibrary{arrows.meta, positioning, shapes, fit, calc}
\\begin{document}
"""

for tikz_file in tikz_inputs:
    src_path = os.path.join("..", tikz_file)
    if os.path.exists(src_path):
        basename = os.path.basename(tikz_file).replace(".tex", "")
        tmp_tex = f"tmp_{basename}.tex"
        
        with open(tmp_tex, "w") as f:
            f.write(preamble)
            f.write(f"\\input{{{tikz_file}}}\n")
            f.write("\\end{document}\n")
            
        print(f"Compiling {tikz_file}...")
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", f"-output-directory={ABS_HTML_DIR}", f"{ABS_HTML_DIR}/{tmp_tex}"],
                cwd="..",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            
            pdf_out = f"tmp_{basename}.pdf"
            if os.path.exists(pdf_out):
                png_out = os.path.join(ASSETS_DIR, f"{basename}.png")
                subprocess.run(["sips", "-s", "format", "png", pdf_out, "--out", png_out], check=True, stdout=subprocess.DEVNULL)
                print(f"  -> Converted to {png_out}")
        except Exception as e:
            print(f"Error compiling {tikz_file}: {e}")
            
        # Cleanup
        for ext in [".tex", ".pdf", ".log", ".aux"]:
            f_to_clean = f"tmp_{basename}{ext}"
            if os.path.exists(f_to_clean):
                os.remove(f_to_clean)

print("Done preparing assets!")
