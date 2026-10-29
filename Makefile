# Compilation du livre avec Pandoc.
#   make pdf        -> build/livre.pdf  (nécessite XeLaTeX)
#   make epub       -> build/livre.epub
#   make html       -> build/livre.html
#   make couverture -> couverture et quatrième de couverture en PNG et PDF (nécessite rsvg-convert et python3)
#   make favicon    -> favicons du site dans build/favicon/ (nécessite rsvg-convert et python3)
#   make site       -> build/site/ : page d'accueil, lecture en ligne, PDF et EPUB
#   make            -> le PDF, l'EPUB et le HTML
#
# Mesure d'audience : `make site GOATCOUNTER=moncode` ajoute GoatCounter
# (https://moncode.goatcounter.com) à la page d'accueil du site.
GOATCOUNTER ?=

LIMINAIRE := liminaire/colophon.md
CHAPITRES := $(sort $(wildcard chapitres/*.md))
FIN       := liminaire/glossaire.md liminaire/remerciements.md
PANDOC    := pandoc
OPTIONS   := -f markdown+autolink_bare_uris --toc metadata.yaml $(LIMINAIRE) $(CHAPITRES) $(FIN) --resource-path=chapitres --top-level-division=chapter

all: pdf epub html

build:
	mkdir -p build

couverture: build
	rsvg-convert -w 1600 couverture/couverture.svg -o build/couverture.png
	rsvg-convert -f pdf couverture/couverture.svg -o build/couverture.pdf
	python3 couverture/quatrieme.py couverture/quatrieme.txt build/quatrieme.svg
	rsvg-convert -w 1600 build/quatrieme.svg -o build/quatrieme.png
	rsvg-convert -f pdf build/quatrieme.svg -o build/quatrieme.pdf

# L'icône Apple est carrée : iOS arrondit lui-même les coins.
favicon: build
	mkdir -p build/favicon
	cp couverture/favicon.svg build/favicon/favicon.svg
	rsvg-convert -w 16 -h 16 couverture/favicon.svg -o build/favicon/favicon-16.png
	rsvg-convert -w 32 -h 32 couverture/favicon.svg -o build/favicon/favicon-32.png
	rsvg-convert -w 48 -h 48 couverture/favicon.svg -o build/favicon/favicon-48.png
	rsvg-convert -w 192 -h 192 couverture/favicon.svg -o build/favicon/icon-192.png
	rsvg-convert -w 512 -h 512 couverture/favicon.svg -o build/favicon/icon-512.png
	sed 's/rx="12"/rx="0"/' couverture/favicon.svg | rsvg-convert -w 180 -h 180 -o build/favicon/apple-touch-icon.png
	python3 couverture/ico.py build/favicon/favicon.ico build/favicon/favicon-16.png build/favicon/favicon-32.png build/favicon/favicon-48.png

pdf: couverture
	$(PANDOC) $(OPTIONS) --pdf-engine=xelatex -o build/livre.pdf

epub: couverture
	$(PANDOC) $(OPTIONS) --split-level=1 --epub-cover-image=build/couverture.png -o build/livre.epub

html: build
	$(PANDOC) $(OPTIONS) --standalone --embed-resources --toc-depth=3 -o build/livre.html

site: all favicon
	rm -rf build/site
	mkdir -p build/site
	cp site/index.html build/couverture.png build/livre.html build/livre.pdf build/livre.epub build/site/
	cp build/favicon/favicon.ico build/favicon/favicon.svg build/favicon/apple-touch-icon.png build/favicon/icon-192.png build/favicon/icon-512.png site/site.webmanifest build/site/
ifneq ($(GOATCOUNTER),)
	sed -i 's|<!-- MESURE D.AUDIENCE[^>]*-->|<script data-goatcounter="https://$(GOATCOUNTER).goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>|' build/site/index.html
endif

clean:
	rm -rf build

.PHONY: all pdf epub html couverture favicon site clean
