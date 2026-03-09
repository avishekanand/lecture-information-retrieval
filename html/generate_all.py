import os
import subprocess
import json

lectures = [
    "01_intro_vector_space.tex",
    "02_indexing.tex",
    "03_ranking.tex",
    "04_embeddings_reranking.tex",
    "05_dense_retrieval.tex"
]

base_dir = "../done"
output_dir = "theme-white"
os.makedirs("temp_data", exist_ok=True)

# First high-level compilation of all known tikz files
print("Ensuring all standard TikZ files are compiled...")
subprocess.run(["python3", "compile_tikz.py"], check=True)

for lec in lectures:
    lec_path = os.path.join(base_dir, lec)
    if not os.path.exists(lec_path):
        print(f"Skipping {lec}, not found.")
        continue
    
    name = lec.replace(".tex", "")
    json_path = f"temp_data/{name}.json"
    html_path = f"{output_dir}/{name}.html"
    
    print(f"\n>>> Processing {lec}...")
    
    # 1. Run parser (extracts JSON and potentially extracted_tikz.json)
    try:
        result = subprocess.run(["python3", "parse_latex.py", lec_path], capture_output=True, text=True, check=True)
        with open(json_path, "w") as f:
            f.write(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error parsing {lec}: {e.stderr}")
        continue

    # 2. Run TikZ compiler (handles extracted_tikz.json if present)
    try:
        subprocess.run(["python3", "compile_tikz.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error compiling TikZ for {lec}")

    # 3. Run slide generator
    try:
        subprocess.run([
            "python3", "generate_slides.py", 
            "--theme", "white", 
            "--data", json_path, 
            "--output", html_path
        ], check=True)
        print(f"Successfully generated {html_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating slides for {lec}")

print("\nDone! All lectures processed.")
