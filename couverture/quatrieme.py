"""Fabrique la quatrième de couverture (SVG) à partir de couverture/quatrieme.txt.

La photo de l'auteur (couverture/auteur.jpg) est ajoutée en médaillon si elle existe.

Format du texte, un paragraphe par bloc séparé d'une ligne vide :
  # ...  accroche, en gros
  > ...  citation, en italique
  @ ...  quelques mots sur l'auteur, en bas
  sinon  paragraphe normal

Usage : python3 couverture/quatrieme.py couverture/quatrieme.txt build/quatrieme.svg
"""
import base64
import os
import sys
import textwrap
from html import escape

source, sortie = sys.argv[1], sys.argv[2]
blocs = [b.strip().replace("\n", " ") for b in open(source, encoding="utf-8").read().split("\n\n") if b.strip()]

X = 170            # marge gauche
y = 250            # position du premier texte
lignes = []

def ecrire(texte, largeur, taille, interligne, style):
    global y
    for ligne in textwrap.wrap(texte, largeur):
        lignes.append(f'<text x="{X}" y="{y}" font-size="{taille}" {style}>{escape(ligne)}</text>')
        y += interligne

for bloc in blocs:
    if bloc.startswith("#"):
        ecrire(bloc[1:].strip(), 32, 58, 74, 'font-family="DejaVu Serif" font-weight="bold" fill="#ffffff"')
        y += 40
    elif bloc.startswith(">"):
        y += 10
        ecrire(bloc[1:].strip(), 48, 40, 56, 'font-family="DejaVu Serif" font-style="italic" fill="#f2c38b"')
        y += 40
    elif bloc.startswith("@"):
        y += 30
        lignes.append(f'<rect x="{X}" y="{y - 50}" width="120" height="4" fill="#f2c38b"/>')
        photo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auteur.jpg")
        if os.path.exists(photo):
            # Photo de l'auteur en médaillon, le texte se décale à droite.
            d = 200
            donnees = base64.b64encode(open(photo, "rb").read()).decode()
            lignes.append(f'<clipPath id="medaillon"><circle cx="{X + d/2}" cy="{y - 10 + d/2}" r="{d/2}"/></clipPath>')
            lignes.append(f'<image x="{X}" y="{y - 10}" width="{d}" height="{d}" clip-path="url(#medaillon)" href="data:image/jpeg;base64,{donnees}"/>')
            lignes.append(f'<circle cx="{X + d/2}" cy="{y - 10 + d/2}" r="{d/2}" fill="none" stroke="#f2c38b" stroke-width="4"/>')
            X += d + 40
            ecrire(bloc[1:].strip(), 50, 32, 48, 'font-family="DejaVu Sans" fill="#ffffff"')
            X -= d + 40
        else:
            ecrire(bloc[1:].strip(), 62, 32, 48, 'font-family="DejaVu Sans" fill="#ffffff"')
    else:
        ecrire(bloc, 54, 37, 54, 'font-family="DejaVu Serif" fill="#e8edf5"')
        y += 26

modele = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "quatrieme.svg"), encoding="utf-8").read()
open(sortie, "w", encoding="utf-8").write(modele.replace("<!-- TEXTE -->", "\n  ".join(lignes)))
