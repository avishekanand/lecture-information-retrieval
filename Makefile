.PHONY: all clean

BUILD_DIR = build
SRCS = $(wildcard *.tex)
PDFS = $(addprefix $(BUILD_DIR)/, $(SRCS:.tex=.pdf))

all: $(BUILD_DIR) $(PDFS)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/%.pdf: %.tex | $(BUILD_DIR)
	pdflatex -output-directory=$(BUILD_DIR) $<
	pdflatex -output-directory=$(BUILD_DIR) $<

clean:
	rm -rf $(BUILD_DIR)
