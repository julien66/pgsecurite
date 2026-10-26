# Sécurité en parapente (titre à trouver)

Manuscrit de Julien Garcia, migré depuis Google Docs. Le texte est repris tel quel depuis l'export Markdown : seul le découpage a changé.

## Organisation

```
chapitres/   un fichier Markdown par chapitre, dans l'ordre de lecture (00, 01, 10, 11…)
images/      les illustrations extraites de l'export
liminaire/   pages placées avant le préambule (licence et mentions)
couverture/  la couverture, en SVG (titre et auteur modifiables dans le fichier)
site/        la page d'accueil du site de lecture
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
make site   # build/site/ : page d'accueil, lecture en ligne, PDF et EPUB
```

La couverture est produite à partir de `couverture/couverture.svg` avec `rsvg-convert` (paquet `librsvg`). Elle sert de première page au PDF et de couverture à l'EPUB.

Sans rien installer : à chaque envoi sur `main`, GitHub compile le PDF, l'EPUB et le HTML (onglet **Actions**, puis l'artefact « livre » du dernier passage).

## État du manuscrit

Voir [notes/etat-du-manuscrit.md](notes/etat-du-manuscrit.md).

## Licence

Le livre est publié sous licence [Creative Commons BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.fr) : chacun peut le partager librement en citant l'auteur, sans usage commercial ni modification. Le texte complet est dans [LICENSE](LICENSE), et la mention figure en tête du livre (`liminaire/colophon.md`).

## Site de lecture

À chaque envoi sur `main`, GitHub construit un petit site (`build/site/`) : une page d'accueil avec la couverture, le livre à lire en ligne, et les liens pour télécharger le PDF et l'EPUB. La mise en ligne sur GitHub Pages est désactivée par défaut. Pour l'activer :

1. Le dépôt doit être public (GitHub Pages n'est gratuit que pour les dépôts publics ; sur un dépôt privé, il faut un compte GitHub Pro).
2. Dans **Settings > Pages**, choisir **GitHub Actions** comme source.
3. Dans **Settings > Secrets and variables > Actions > Variables**, créer la variable `PUBLIER_SITE` avec la valeur `true`.

Le site sera alors publié à l'adresse `https://julien66.github.io/pgsecurite/`.
