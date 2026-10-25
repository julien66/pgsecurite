# Compilation du livre avec Pandoc.
#   make pdf    -> build/livre.pdf  (nécessite XeLaTeX)
#   make epub   -> build/livre.epub
#   make html   -> build/livre.html
#   make        -> les trois

CHAPITRES := $(sort $(wildcard chapitres/*.md))
PANDOC    := pandoc
OPTIONS   := metadata.yaml $(CHAPITRES) --resource-path=chapitres --top-level-division=chapter

all: pdf epub html

build:
	mkdir -p build

pdf: build
	$(PANDOC) $(OPTIONS) --pdf-engine=xelatex -o build/livre.pdf

epub: build
	$(PANDOC) $(OPTIONS) --split-level=1 -o build/livre.epub

html: build
	$(PANDOC) $(OPTIONS) --standalone --embed-resources -o build/livre.html

clean:
	rm -rf build

.PHONY: all pdf epub html clean
