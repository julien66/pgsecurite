# Compilation du livre avec Pandoc.
#   make pdf        -> build/livre.pdf  (nécessite XeLaTeX)
#   make epub       -> build/livre.epub
#   make html       -> build/livre.html
#   make couverture -> build/couverture.png et build/couverture.pdf (nécessite rsvg-convert)
#   make site       -> build/site/ : page d'accueil, lecture en ligne, PDF et EPUB
#   make            -> le PDF, l'EPUB et le HTML

LIMINAIRE := liminaire/colophon.md
CHAPITRES := $(sort $(wildcard chapitres/*.md))
PANDOC    := pandoc
OPTIONS   := metadata.yaml $(LIMINAIRE) $(CHAPITRES) --resource-path=chapitres --top-level-division=chapter

all: pdf epub html

build:
	mkdir -p build

couverture: build
	rsvg-convert -w 1600 couverture/couverture.svg -o build/couverture.png
	rsvg-convert -f pdf couverture/couverture.svg -o build/couverture.pdf

pdf: couverture
	$(PANDOC) $(OPTIONS) --pdf-engine=xelatex -o build/livre.pdf

epub: couverture
	$(PANDOC) $(OPTIONS) --split-level=1 --epub-cover-image=build/couverture.png -o build/livre.epub

html: build
	$(PANDOC) $(OPTIONS) --standalone --embed-resources -o build/livre.html

site: all
	rm -rf build/site
	mkdir -p build/site
	cp site/index.html build/couverture.png build/livre.html build/livre.pdf build/livre.epub build/site/

clean:
	rm -rf build

.PHONY: all pdf epub html couverture site clean
