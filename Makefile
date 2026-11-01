# Compilation du livre avec Pandoc.
#   make pdf        -> build/livre.pdf  (nécessite XeLaTeX)
#   make epub       -> build/livre.epub
#   make html       -> build/livre.html
#   make couverture -> couverture et quatrième de couverture en PNG et PDF (nécessite rsvg-convert et python3)
#   make favicon    -> favicons du site dans build/favicon/ (nécessite rsvg-convert et python3)
#   make site       -> build/site/ : page d'accueil, lecture en ligne, PDF et EPUB
#   make            -> le PDF, l'EPUB et le HTML
#
# Traductions : ajouter LANGUE=en, LANGUE=de ou LANGUE=es à n'importe quelle
# commande de livre (pdf, epub, html, couverture, all). Les sources sont lues
# dans traductions/<langue>/ et le résultat va dans build/<langue>/.
#   make pdf LANGUE=en  -> build/en/livre.pdf
#   make traductions    -> PDF, EPUB et HTML de chaque traduction
#
# Mesure d'audience : `make site GOATCOUNTER=moncode` ajoute GoatCounter
# (https://moncode.goatcounter.com) à la page d'accueil du site.
GOATCOUNTER ?=

LANGUE    ?= fr
LANGUES   := en de es

ifeq ($(LANGUE),fr)
SOURCE    := .
SORTIE    := build
else
SOURCE    := traductions/$(LANGUE)
SORTIE    := build/$(LANGUE)
endif

# Une traduction en cours ne contient pas encore tous les fichiers : on assemble ceux qui existent.
LIMINAIRE := $(wildcard $(SOURCE)/liminaire/colophon.md)
CHAPITRES := $(sort $(wildcard $(SOURCE)/chapitres/*.md))
FIN       := $(wildcard $(SOURCE)/liminaire/glossaire.md $(SOURCE)/liminaire/remerciements.md)
QUATRIEME := $(firstword $(wildcard $(SOURCE)/couverture/quatrieme.txt) couverture/quatrieme.txt)
PANDOC    := pandoc
# Les images sont communes à toutes les langues (images/), appelées en ../images/ depuis chapitres/.
OPTIONS   := -f markdown+autolink_bare_uris --toc $(SOURCE)/metadata.yaml $(LIMINAIRE) $(CHAPITRES) $(FIN) --resource-path=chapitres --top-level-division=chapter

all: pdf epub html

build:
	mkdir -p $(SORTIE)

couverture: build
	rsvg-convert -w 1600 $(SOURCE)/couverture/couverture.svg -o $(SORTIE)/couverture.png
	rsvg-convert -f pdf $(SOURCE)/couverture/couverture.svg -o $(SORTIE)/couverture.pdf
	python3 couverture/quatrieme.py $(QUATRIEME) $(SORTIE)/quatrieme.svg
	rsvg-convert -w 1600 $(SORTIE)/quatrieme.svg -o $(SORTIE)/quatrieme.png
	rsvg-convert -f pdf $(SORTIE)/quatrieme.svg -o $(SORTIE)/quatrieme.pdf

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
	$(PANDOC) $(OPTIONS) --pdf-engine=xelatex -o $(SORTIE)/livre.pdf

epub: couverture
	$(PANDOC) $(OPTIONS) --split-level=1 --epub-cover-image=$(SORTIE)/couverture.png -o $(SORTIE)/livre.epub

html: build
	$(PANDOC) $(OPTIONS) --standalone --embed-resources --toc-depth=3 -o $(SORTIE)/livre.html

site: all favicon
	rm -rf build/site
	mkdir -p build/site
	cp site/index.html build/couverture.png build/livre.html build/livre.pdf build/livre.epub build/site/
	cp build/favicon/favicon.ico build/favicon/favicon.svg build/favicon/apple-touch-icon.png build/favicon/icon-192.png build/favicon/icon-512.png site/site.webmanifest build/site/
ifneq ($(GOATCOUNTER),)
	sed -i 's|<!-- MESURE D.AUDIENCE[^>]*-->|<script data-goatcounter="https://$(GOATCOUNTER).goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>|' build/site/index.html
endif

traductions:
	for l in $(LANGUES); do $(MAKE) all LANGUE=$$l || exit 1; done

clean:
	rm -rf build

.PHONY: all build pdf epub html couverture favicon site traductions clean
