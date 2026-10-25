# Sécurité en parapente (titre à trouver)

Manuscrit de Julien Garcia, migré depuis Google Docs. Le texte est repris tel quel depuis l'export Markdown : seul le découpage a changé.

## Organisation

```
chapitres/   un fichier Markdown par chapitre, dans l'ordre de lecture (00, 01, 10, 11…)
images/      les illustrations extraites de l'export
notes/       éléments de travail, hors du livre compilé
metadata.yaml  titre, auteur, langue et mise en page pour Pandoc
Makefile     commandes de compilation
```

La numérotation des fichiers suit les parties : `0x` pour l'ouverture, `1x` pour la partie 1, `2x` pour la partie 2. La compétition fera l'objet d'un second livre : ses chapitres sont rangés dans `notes/livre-competition/`, hors du livre compilé. Pour insérer un chapitre, il suffit de choisir un numéro libre entre deux autres (par exemple `125-…md` entre `12` et `13`) : les fichiers sont assemblés par ordre alphabétique.

Les notes de bas de page sont placées à la fin du chapitre qui les appelle. Elles gardent leur numéro d'origine dans les fichiers, mais Pandoc les renumérote automatiquement dans le livre compilé.

## Compiler le livre

Il faut [Pandoc](https://pandoc.org) (et XeLaTeX pour le PDF).

```sh
make pdf    # build/livre.pdf
make epub   # build/livre.epub
make html   # build/livre.html
make        # les trois
```

Sans rien installer : à chaque envoi sur `main`, GitHub compile le PDF, l'EPUB et le HTML (onglet **Actions**, puis l'artefact « livre » du dernier passage).

## État du manuscrit

Voir [notes/etat-du-manuscrit.md](notes/etat-du-manuscrit.md).
