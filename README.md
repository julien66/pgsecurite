# Sécurité en parapente. À nos risques et périls ?

Manuscrit de Julien Garcia, migré depuis Google Docs. Le texte est repris tel quel depuis l'export Markdown : seul le découpage a changé.

## Organisation

```
chapitres/   un fichier Markdown par chapitre, dans l'ordre de lecture (00, 01, 10, 11…)
images/      les illustrations extraites de l'export
liminaire/   pages hors chapitres : licence et mentions (au début), glossaire et remerciements (à la fin)
couverture/  la couverture (SVG) et la quatrième de couverture (texte dans quatrieme.txt, photo auteur.jpg)
site/        le site de lecture : pages.py génère les pages d'accueil des quatre langues (textes dans PAGES), style.css
notes/       éléments de travail, hors du livre compilé
traductions/ les éditions anglaise (en/), allemande (de/), espagnole (es/) et persane (fa/), et le glossaire terminologique commun
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
make pdf LANGUE=en   # une traduction : build/en/livre.pdf (de même avec de, es ou fa)
make traductions     # PDF, EPUB et HTML des quatre traductions
```

La couverture est produite à partir de `couverture/couverture.svg` avec `rsvg-convert` (paquet `librsvg`). Elle sert de première page au PDF et de couverture à l'EPUB.

Sans rien installer : à chaque envoi sur `main`, GitHub compile le PDF, l'EPUB et le HTML (onglet **Actions**, puis l'artefact « livre » du dernier passage).

## Traductions

Voir [traductions/README.md](traductions/README.md) : organisation des dossiers par langue, règles de traduction et façon de contribuer comme traducteur ou relecteur natif.

## État du manuscrit

Voir [notes/etat-du-manuscrit.md](notes/etat-du-manuscrit.md).

## Licence

Le livre est publié sous licence [Creative Commons BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.fr) : chacun peut le partager librement en citant l'auteur, sans usage commercial ni modification. Le texte complet est dans [LICENSE](LICENSE), et la mention figure en tête du livre (`liminaire/colophon.md`).

## Site de lecture

À chaque envoi sur `main`, GitHub construit un petit site (`build/site/`) : une page d'accueil avec la couverture, le livre à lire en ligne, et les liens pour télécharger le PDF et l'EPUB, en français à la racine et en traduction dans `en/`, `de/`, `es/` et `fa/`. La page persane est écrite de droite à gauche (`dir="rtl"`) avec la police Vazirmatn, copiée dans `fa/fonts/`.

Chaque page porte un sélecteur de langue en haut à droite et rappelle les autres langues sous les boutons. Chaque page traduite (pas la française) affiche un message dans sa langue, sous la présentation sur la page d'accueil et en bandeau en tête de la lecture en ligne : les traductions actuelles sont automatiques, de vraies traductions par des pilotes de la communauté sont en cours, le lecteur peut attendre cette meilleure version, et l'adresse de contact pour participer. Sur la page française, un lecteur dont le navigateur est réglé en anglais, en allemand ou en espagnol voit un bandeau qui lui propose sa langue ; il n'est jamais redirigé d'office, et le bandeau ne revient plus une fois fermé. Les textes des pages d'accueil sont dans `site/pages.py`.

La mise en ligne sur GitHub Pages est désactivée par défaut. Pour l'activer :

1. Le dépôt doit être public (GitHub Pages n'est gratuit que pour les dépôts publics ; sur un dépôt privé, il faut un compte GitHub Pro).
2. Dans **Settings > Pages**, choisir **GitHub Actions** comme source.
3. Dans **Settings > Secrets and variables > Actions > Variables**, créer la variable `PUBLIER_SITE` avec la valeur `true`.

Le site sera alors publié à l'adresse `https://julien66.github.io/pgsecurite/`.

## Sous-domaines par langue

Le site est servi par GitHub Pages sur `securite.jugarcia.fr`. GitHub Pages n'accepte qu'un seul nom de domaine par site, donc chaque langue a un sous-domaine court qui redirige vers sa page :

| Adresse | Redirige vers |
| --- | --- |
| `safety.jugarcia.fr` | `https://securite.jugarcia.fr/en/` |
| `sicherheit.jugarcia.fr` | `https://securite.jugarcia.fr/de/` |
| `seguridad.jugarcia.fr` | `https://securite.jugarcia.fr/es/` |
| `amniat.jugarcia.fr` (امنیت, « sécurité ») | `https://securite.jugarcia.fr/fa/` |

La suite de l'adresse est conservée (`safety.jugarcia.fr/livre.pdf` mène à `securite.jugarcia.fr/en/livre.pdf`). Les redirections sont faites par l'hébergement web OVH de `jugarcia.fr`, qui fournit aussi le certificat HTTPS :

1. Déposer par FTP le fichier `site/sous-domaines/.htaccess` dans un nouveau dossier `sous-domaines/` de l'hébergement.
2. Dans l'espace client OVH, **Hébergements > Multisite > Ajouter un domaine ou sous-domaine**, pour chacun des quatre sous-domaines : dossier racine `sous-domaines`, cocher **SSL** et laisser OVH **créer l'entrée DNS** (enregistrements A `5.135.23.164` et AAAA `2001:41d0:301::100`).
3. Une fois les quatre ajoutés, **Hébergements > Informations générales > Certificat SSL > Régénérer** si le certificat n'inclut pas encore les nouveaux noms.

Chaque page indique `securite.jugarcia.fr` comme adresse de référence (`rel="canonical"` et `hreflang` absolus dans `site/pages.py`), pour que les moteurs de recherche ne voient pas de doublons.

## Mesure d'audience

Le site peut compter ses visites, les lectures en ligne et les téléchargements du PDF et de l'EPUB avec [GoatCounter](https://www.goatcounter.com) : gratuit pour un usage non commercial, sans cookie et sans données personnelles, donc sans bandeau de consentement.

1. Créer un compte sur goatcounter.com et choisir un code (par exemple `pgsecurite`, pour `https://pgsecurite.goatcounter.com`).
2. Dans **Settings > Secrets and variables > Actions > Variables**, créer la variable `GOATCOUNTER` avec ce code.

Les chiffres apparaissent ensuite sur le tableau de bord GoatCounter : les visites de la page d'accueil, et les clics « lecture-en-ligne », « telechargement-pdf » et « telechargement-epub », suivis du code de la langue (par exemple « telechargement-pdf-de »). Sans la variable, le site est publié sans aucune mesure.
