# Traductions

Le livre est traduit en anglais (`en/`), en allemand (`de/`), en espagnol (`es/`) et en persan (`fa/`). Le français, à la racine du dépôt, reste la version de référence : une traduction suit toujours le texte français, jamais l'inverse.

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
  fa/  (idem, plus fonts/ et deux feuilles de style : voir « Le persan » plus bas)
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

## Le persan

La traduction persane est l’œuvre d’un traducteur bénévole (crédité dans `fa/liminaire/colophon.md`). Elle couvre tout le livre, glossaire et remerciements compris. Comme ce n’est pas une traduction automatique, elle n’a ni encadré d’avertissement ni message sur le site.

Le persan s’écrit de droite à gauche :

- `fa/metadata.yaml` déclare `lang: fa-IR` et `dir: rtl` ; le PDF est compilé avec LuaLaTeX, dont l’algorithme bidirectionnel place correctement les mots latins, les chiffres et les liens dans le texte persan ;
- la police est Vazirmatn (licence SIL OFL), fournie dans `fa/fonts/` : le Makefile la rend visible à rsvg-convert et à LuaLaTeX, l’EPUB l’embarque et le site la copie dans `fa/fonts/` ;
- `fa/livre.css` (lecture en ligne) et `fa/epub.css` (EPUB) mettent le texte de droite à gauche ;
- `couverture/quatrieme.py` aligne à droite une quatrième de couverture écrite en persan.

Les schémas (Reason, Wilde, voyage du héros) restent les images communes ; leur légende persane détaillée est placée juste en dessous.

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
