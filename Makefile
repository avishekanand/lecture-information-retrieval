.PHONY: all clean animated static

BUILD_DIR = build
SRCS = $(wildcard *.tex)
PDFS_ANIMATED = $(addprefix $(BUILD_DIR)/, $(SRCS:.tex=_animated.pdf))
PDFS_STATIC = $(addprefix $(BUILD_DIR)/, $(SRCS:.tex=_static.pdf))

all: $(BUILD_DIR) $(PDFS_ANIMATED) $(PDFS_STATIC)

animated: $(BUILD_DIR) $(PDFS_ANIMATED)

static: $(BUILD_DIR) $(PDFS_STATIC)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Animated version (default)
$(BUILD_DIR)/%_animated.pdf: %.tex | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) $<
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) $<

# Static version
$(BUILD_DIR)/%_static.pdf: %.tex | $(BUILD_DIR)
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) "\def\staticmode{1} \input{$<}"
	pdflatex -jobname=$(basename $(notdir $@)) -output-directory=$(BUILD_DIR) "\def\staticmode{1} \input{$<}"

clean:
	rm -rf $(BUILD_DIR)
