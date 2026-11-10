# Compilation du livre avec Pandoc.
#   make pdf        -> build/livre.pdf  (nécessite XeLaTeX)
#   make epub       -> build/livre.epub
#   make html       -> build/livre.html
#   make couverture -> couverture et quatrième de couverture en PNG et PDF (nécessite rsvg-convert et python3)
#   make favicon    -> favicons du site dans build/favicon/ (nécessite rsvg-convert et python3)
#   make site       -> build/site/ : pages d'accueil (FR, EN, DE, ES, FA), lecture en ligne, PDF et EPUB
#   make            -> le PDF, l'EPUB et le HTML
#
# Traductions : ajouter LANGUE=en, LANGUE=de, LANGUE=es ou LANGUE=fa à n'importe quelle
# commande de livre (pdf, epub, html, couverture, all). Les sources sont lues
# dans traductions/<langue>/ et le résultat va dans build/<langue>/.
#   make pdf LANGUE=en  -> build/en/livre.pdf
#   make traductions    -> PDF, EPUB et HTML de chaque traduction
#
# Le persan (fa) s'écrit de droite à gauche : son PDF passe par LuaLaTeX et sa
# police Vazirmatn est lue dans traductions/fa/fonts/ (voir plus bas).
#
# Mesure d'audience : `make site GOATCOUNTER=moncode` ajoute GoatCounter
# (https://moncode.goatcounter.com) à la page d'accueil du site.
GOATCOUNTER ?=

LANGUE    ?= fr
LANGUES   := en de es fa

ifeq ($(LANGUE),fr)
SOURCE    := .
SORTIE    := build
else
SOURCE    := traductions/$(LANGUE)
SORTIE    := build/$(LANGUE)
endif

# Une traduction en cours ne contient pas encore tous les fichiers : on assemble ceux qui existent.
LIMINAIRE := $(wildcard $(SOURCE)/liminaire/avertissement.md $(SOURCE)/liminaire/colophon.md)
CHAPITRES := $(sort $(wildcard $(SOURCE)/chapitres/*.md))
FIN       := $(wildcard $(SOURCE)/liminaire/glossaire.md $(SOURCE)/liminaire/remerciements.md)
QUATRIEME := $(firstword $(wildcard $(SOURCE)/couverture/quatrieme.txt) couverture/quatrieme.txt)
PANDOC    := pandoc
# Les images sont communes à toutes les langues (images/), appelées en ../images/ depuis chapitres/.
OPTIONS   := -f markdown+autolink_bare_uris --toc $(SOURCE)/metadata.yaml $(LIMINAIRE) $(CHAPITRES) $(FIN) --resource-path=chapitres --top-level-division=chapter
MOTEUR    := xelatex
OPTIONS_EPUB :=
OPTIONS_HTML :=

# Persan : texte de droite à gauche et police Vazirmatn (traductions/fa/fonts/,
# licence SIL OFL). Fontconfig cherche les polices dans $(XDG_DATA_HOME)/fonts :
# rsvg-convert (couverture) et LuaLaTeX (PDF) la trouvent donc sans installation.
# LuaLaTeX applique l'algorithme bidirectionnel Unicode (babel, bidi=basic), ce qui
# place correctement les mots latins, les chiffres et les liens dans le texte persan.
ifeq ($(LANGUE),fa)
export XDG_DATA_HOME := $(CURDIR)/$(SOURCE)
MOTEUR       := lualatex
OPTIONS_EPUB := --css=$(SOURCE)/epub.css --epub-embed-font=$(SOURCE)/fonts/Vazirmatn-Regular.ttf --epub-embed-font=$(SOURCE)/fonts/Vazirmatn-Bold.ttf
OPTIONS_HTML := --css=$(SOURCE)/livre.css
endif

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
	$(PANDOC) $(OPTIONS) --pdf-engine=$(MOTEUR) -o $(SORTIE)/livre.pdf

epub: couverture
	$(PANDOC) $(OPTIONS) --split-level=1 --epub-cover-image=$(SORTIE)/couverture.png $(OPTIONS_EPUB) -o $(SORTIE)/livre.epub

# Le bandeau sur les traductions en cours (site/pages.py) est placé en tête de la lecture en ligne.
html: build
	python3 site/pages.py --bandeau $(LANGUE) > $(SORTIE)/bandeau.html
	$(PANDOC) $(OPTIONS) --standalone --embed-resources --toc-depth=3 --include-before-body=$(SORTIE)/bandeau.html $(OPTIONS_HTML) -o $(SORTIE)/livre.html

site: all favicon traductions
	rm -rf build/site
	mkdir -p build/site
	python3 site/pages.py build/site
	cp site/style.css build/couverture.png build/livre.html build/livre.pdf build/livre.epub build/site/
	cp build/favicon/favicon.ico build/favicon/favicon.svg build/favicon/apple-touch-icon.png build/favicon/icon-192.png build/favicon/icon-512.png site/site.webmanifest build/site/
	for l in $(LANGUES); do cp build/$$l/couverture.png build/$$l/livre.html build/$$l/livre.pdf build/$$l/livre.epub build/site/$$l/ || exit 1; done
	mkdir -p build/site/fa/fonts
	cp traductions/fa/fonts/Vazirmatn-Regular.ttf traductions/fa/fonts/Vazirmatn-Bold.ttf build/site/fa/fonts/
ifneq ($(GOATCOUNTER),)
	sed -i 's|<!-- MESURE D.AUDIENCE[^>]*-->|<script data-goatcounter="https://$(GOATCOUNTER).goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>|' build/site/index.html build/site/*/index.html
endif

traductions:
	for l in $(LANGUES); do $(MAKE) all LANGUE=$$l || exit 1; done

clean:
	rm -rf build

.PHONY: all build pdf epub html couverture favicon site traductions clean
