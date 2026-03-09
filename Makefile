.PHONY: all clean animated static build_done

BUILD_DIR = build
DONE_DIR = done

# Compile active lectures (06-07)
ACTIVE_LECTURES = 06_ltr.tex 07-rag.tex
PDFS_ANIMATED = $(addprefix $(BUILD_DIR)/, $(ACTIVE_LECTURES:.tex=_animated.pdf))
PDFS_STATIC = $(addprefix $(BUILD_DIR)/, $(ACTIVE_LECTURES:.tex=_static.pdf))

THEME_DEPS = theme/macros.tex theme/tikz-styles.tex

# Compile done lectures
DONE_LECTURES = $(wildcard $(DONE_DIR)/*.tex)
DONE_PDFS_ANIMATED = $(addprefix $(BUILD_DIR)/, $(notdir $(DONE_LECTURES:.tex=_animated.pdf)))
DONE_PDFS_STATIC = $(addprefix $(BUILD_DIR)/, $(notdir $(DONE_LECTURES:.tex=_static.pdf)))

GALLERY_PDF = $(BUILD_DIR)/full_gallery.pdf

all: $(BUILD_DIR) $(PDFS_ANIMATED) $(PDFS_STATIC) $(DONE_PDFS_ANIMATED) $(DONE_PDFS_STATIC) $(GALLERY_PDF)

animated: $(BUILD_DIR) $(PDFS_ANIMATED) $(DONE_PDFS_ANIMATED)

static: $(BUILD_DIR) $(PDFS_STATIC) $(DONE_PDFS_STATIC)

build_done: $(BUILD_DIR) $(DONE_PDFS_ANIMATED) $(DONE_PDFS_STATIC)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Rules for current directory lectures
$(BUILD_DIR)/%_animated.pdf: %.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/%_static.pdf: %.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

# Rules for done/ directory lectures
# We use a pattern match but must be careful because target has no path prefix in the stem if not handled correctly
# Actually, $(BUILD_DIR)/% matches build/01_intro_vector_space_animated.pdf
# then % is 01_intro_vector_space_animated

$(BUILD_DIR)/01_intro_vector_space_animated.pdf: $(DONE_DIR)/01_intro_vector_space.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=01_intro_vector_space_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=01_intro_vector_space_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/02_indexing_animated.pdf: $(DONE_DIR)/02_indexing.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=02_indexing_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=02_indexing_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/03_ranking_animated.pdf: $(DONE_DIR)/03_ranking.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=03_ranking_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=03_ranking_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/04_embeddings_reranking_animated.pdf: $(DONE_DIR)/04_embeddings_reranking.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=04_embeddings_reranking_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=04_embeddings_reranking_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/05_dense_retrieval_animated.pdf: $(DONE_DIR)/05_dense_retrieval.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=05_dense_retrieval_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=05_dense_retrieval_animated -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/01_intro_vector_space_static.pdf: $(DONE_DIR)/01_intro_vector_space.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=01_intro_vector_space_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=01_intro_vector_space_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/02_indexing_static.pdf: $(DONE_DIR)/02_indexing.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=02_indexing_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=02_indexing_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/03_ranking_static.pdf: $(DONE_DIR)/03_ranking.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=03_ranking_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=03_ranking_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/04_embeddings_reranking_static.pdf: $(DONE_DIR)/04_embeddings_reranking.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=04_embeddings_reranking_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=04_embeddings_reranking_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/05_dense_retrieval_static.pdf: $(DONE_DIR)/05_dense_retrieval.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=05_dense_retrieval_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=05_dense_retrieval_static -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(GALLERY_PDF): tikz/full_gallery.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=full_gallery -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=full_gallery -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

clean:
	rm -rf $(BUILD_DIR)
