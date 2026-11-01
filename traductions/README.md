# Traductions

Le livre est traduit en anglais (`en/`), en allemand (`de/`) et en espagnol (`es/`). Le français, à la racine du dépôt, reste la version de référence : une traduction suit toujours le texte français, jamais l'inverse.

## Organisation

Chaque langue reprend la structure du livre français :

```
traductions/
  glossaire-terminologique.md   équivalents fixés pour toutes les langues (à lire avant de traduire)
  en/
    metadata.yaml               titre, langue et mise en page pour Pandoc
    chapitres/                  un fichier par chapitre, mêmes noms que chapitres/ en français
    liminaire/                  colophon.md, glossaire.md, remerciements.md
    couverture/                 couverture.svg (titre traduit) et quatrieme.txt
  de/  (idem)
  es/  (idem)
```

Les fichiers gardent **les mêmes noms qu'en français** (`12-mythe-2.md` reste `12-mythe-2.md` en anglais). On retrouve ainsi tout de suite l'original d'un chapitre, et l'ordre de lecture est le même. Les images sont communes : elles restent dans `images/` à la racine et s'appellent toujours `../images/…`.

## Compiler une traduction

```sh
make pdf LANGUE=en     # build/en/livre.pdf
make epub LANGUE=de    # build/de/livre.epub
make all LANGUE=es     # PDF, EPUB et HTML en espagnol, dans build/es/
make traductions       # les trois langues
```

Une traduction en cours se compile quand même : seuls les chapitres déjà présents sont assemblés. Sur GitHub, chaque PR et chaque envoi sur `main` compile aussi les trois traductions (artefact « livre », dossiers `en/`, `de/`, `es/`).

## Règles de traduction

1. **Glossaire d'abord.** Les termes du [glossaire terminologique](glossaire-terminologique.md) ont un seul équivalent par langue. Pour en changer un, le modifier dans le glossaire et dans tous les chapitres concernés, dans la même PR.
2. **Notes et sources conservées.** Chaque note de bas de page est traduite et garde son identifiant d'origine. Les liens et les références bibliographiques sont repris tels quels.
3. **Chiffres inchangés.** Les chiffres de la FFVL et des autres sources sont reproduits tels quels. Si un chiffre a besoin de contexte pour un lecteur étranger, on ajoute une note de traduction, signalée comme telle.
4. **Fond inchangé.** On traduit, on n'améliore pas le propos. Une erreur repérée dans l'original se signale par une issue ou une PR sur le texte français, qui sera ensuite reportée dans toutes les langues.
5. **Mise en forme Markdown identique** : titres, attributs `{.unnumbered}`, tableaux, citations et appels de note au même endroit qu'en français.

## Contribuer comme traducteur ou relecteur natif

Les traductions de départ sont assistées par IA. Elles gagnent beaucoup à être relues par des pilotes dont c'est la langue maternelle.

1. Proposer ses corrections par une pull request sur les fichiers de sa langue (un chapitre par PR, c'est plus simple à relire).
2. Indiquer dans la PR le nom sous lequel on souhaite être crédité.
3. Le nom est ajouté au colophon de la langue (`liminaire/colophon.md`, ligne « Translation reviewed by », « Übersetzung durchgesehen von », « Traducción revisada por »).

Le livre reste sous licence CC BY-NC-ND 4.0 : les traductions sont publiées par l'auteur, et chaque contributeur accepte que ses corrections soient diffusées sous cette même licence.
