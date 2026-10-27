# Compilation du livre avec Pandoc.
#   make pdf        -> build/livre.pdf  (nécessite XeLaTeX)
#   make epub       -> build/livre.epub
#   make html       -> build/livre.html
#   make couverture -> couverture et quatrième de couverture en PNG et PDF (nécessite rsvg-convert et python3)
#   make site       -> build/site/ : page d'accueil, lecture en ligne, PDF et EPUB
#   make            -> le PDF, l'EPUB et le HTML
#
# Mesure d'audience : `make site GOATCOUNTER=moncode` ajoute GoatCounter
# (https://moncode.goatcounter.com) à la page d'accueil du site.
GOATCOUNTER ?=

LIMINAIRE := liminaire/colophon.md
CHAPITRES := $(sort $(wildcard chapitres/*.md))
FIN       := liminaire/remerciements.md
PANDOC    := pandoc
OPTIONS   := -f markdown+autolink_bare_uris metadata.yaml $(LIMINAIRE) $(CHAPITRES) $(FIN) --resource-path=chapitres --top-level-division=chapter

all: pdf epub html

build:
	mkdir -p build

couverture: build
	rsvg-convert -w 1600 couverture/couverture.svg -o build/couverture.png
	rsvg-convert -f pdf couverture/couverture.svg -o build/couverture.pdf
	python3 couverture/quatrieme.py couverture/quatrieme.txt build/quatrieme.svg
	rsvg-convert -w 1600 build/quatrieme.svg -o build/quatrieme.png
	rsvg-convert -f pdf build/quatrieme.svg -o build/quatrieme.pdf

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
ifneq ($(GOATCOUNTER),)
	sed -i 's|<!-- MESURE D.AUDIENCE[^>]*-->|<script data-goatcounter="https://$(GOATCOUNTER).goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>|' build/site/index.html
endif

clean:
	rm -rf build

.PHONY: all pdf epub html couverture site clean
