.PHONY: all clean animated static build_done

BUILD_DIR = build
DONE_DIR = done

# Compile active lectures
ACTIVE_LECTURES = 07-rag.tex
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

$(BUILD_DIR)/%.pdf: %.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

# Rules for done/ directory lectures
$(BUILD_DIR)/%_animated.pdf: $(DONE_DIR)/%.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/%_static.pdf: $(DONE_DIR)/%.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode "\PassOptionsToClass{handout}{beamer} \def\staticmode{1} \input{$<}"
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(BUILD_DIR)/%.pdf: $(DONE_DIR)/%.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

$(GALLERY_PDF): tikz/full_gallery.tex $(THEME_DEPS) | $(BUILD_DIR)
	pdflatex -jobname=full_gallery -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	pdflatex -jobname=full_gallery -output-directory=$(BUILD_DIR) -interaction=nonstopmode $<
	@find $(BUILD_DIR) -type f ! -name '*.pdf' -delete

clean:
	rm -rf $(BUILD_DIR)

.PRECIOUS: $(BUILD_DIR)/%.pdf

# Expose generic targets so 'make 07-rag.pdf' builds correctly into 'build/07-rag.pdf'
%.pdf: $(BUILD_DIR)/%.pdf
	@echo "Built $(BUILD_DIR)/$@"
