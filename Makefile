.PHONY: all clean animated static

BUILD_DIR = build
# Compile all lectures (01-06)
ACTIVE_LECTURES = 01_intro_vector_space.tex 02_indexing.tex 03_ranking.tex 04_embeddings_reranking.tex 05_dense_retrieval.tex 06_ltr.tex
PDFS_ANIMATED = $(addprefix $(BUILD_DIR)/, $(ACTIVE_LECTURES:.tex=_animated.pdf))
PDFS_STATIC = $(addprefix $(BUILD_DIR)/, $(ACTIVE_LECTURES:.tex=_static.pdf))

all: $(BUILD_DIR) $(PDFS_ANIMATED) $(PDFS_STATIC)

animated: $(BUILD_DIR) $(PDFS_ANIMATED)

static: $(BUILD_DIR) $(PDFS_STATIC)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Animated version (default)
$(BUILD_DIR)/%_animated.pdf: %.tex | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

# Static version
$(BUILD_DIR)/%_static.pdf: %.tex | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

clean:
	rm -rf $(BUILD_DIR)
