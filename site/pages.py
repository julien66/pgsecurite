"""Génère les pages d'accueil du site, une par langue.

Usage : python3 site/pages.py build/site
        python3 site/pages.py --bandeau en > bandeau.html

Écrit build/site/index.html (français) et build/site/<langue>/index.html
pour chaque traduction. Chaque page propose les autres langues, et la page
française suggère la traduction qui correspond à la langue du navigateur.
"""

import datetime
import html
import json
import os
import struct
import sys

# Ordre d'affichage du sélecteur de langue.
LANGUES = ["fr", "en", "de", "es", "fa"]

# Langues écrites de droite à gauche : la page reçoit dir="rtl".
RTL = {"fa"}

# Adresse publique du site (GitHub Pages). Les sous-domaines par langue
# (safety.jugarcia.fr, etc.) redirigent ici : voir site/sous-domaines/.
SITE = "https://securite.jugarcia.fr/"


def direction(langue):
    """Attribut dir à ajouter à un élément dans cette langue (vide pour le sens habituel)."""
    return ' dir="rtl"' if langue in RTL else ""


PAGES = {
    "fr": {
        "nom": "Français",
        "titre": "Sécurité en parapente",
        "sous_titre": "À nos risques et périls ?",
        "description": "Accidents, statistiques, mythes et culture de la sécurité en parapente : un livre gratuit de Julien Garcia, pilote, entraîneur et enquêteur accidents.",
        "titre_lecture": "Sécurité en parapente : lire le livre en ligne",
        "description_lecture": "Lisez gratuitement en ligne Sécurité en parapente, le livre de Julien Garcia sur nos accidents, leurs chiffres et les croyances de notre communauté.",
        "locale": "fr_FR",
        "gratuit": "Livre gratuit",
        "accueil": "Accueil",
        "introuvable": "Cette page n’existe pas.",
        "image_alt": "Couverture du livre Sécurité en parapente : un parapente au-dessus des montagnes au crépuscule",
        "presentation": "Ce livre n’est pas un manuel de pilotage. C’est un regard sur notre communauté et sur la façon dont elle pense la sécurité, écrit par un pilote, entraîneur et enquêteur sur les accidents. Il est gratuit, à lire en ligne ou à télécharger.",
        "lire": "Lire en ligne",
        "pdf": "Télécharger le PDF",
        "epub": "Télécharger l’EPUB",
        "fichier": "Sécurité en parapente - À nos risques et périls",
        # Pas de bandeau sur les traductions en cours pour la version française.
        "traductions": "",
        "licence": 'Diffusé sous licence <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.fr">CC BY-NC-ND 4.0</a> : vous pouvez le partager librement en citant l’auteur, sans usage commercial ni modification.',
        "autres": "Ce livre existe aussi en",
        "navigation": "Langues",
    },
    "en": {
        "nom": "English",
        "titre": "Safety in Paragliding",
        "sous_titre": "At our own risk and peril?",
        "description": "Accidents, statistics, myths and safety culture in paragliding: a free book by Julien Garcia, pilot, coach and accident investigator. English translation.",
        "titre_lecture": "Safety in Paragliding: read the book online",
        "description_lecture": "Read Safety in Paragliding online for free: Julien Garcia’s book on our accidents, their numbers and the beliefs of our community.",
        "locale": "en_GB",
        "gratuit": "Free book",
        "accueil": "Home",
        "introuvable": "This page does not exist.",
        "image_alt": "Cover of the book Safety in Paragliding: a paraglider above the mountains at dusk",
        "presentation": "This book is not a flying manual. It is a look at our community and at the way it thinks about safety, written by a pilot, coach and accident investigator. It is free, to read online or download.",
        "lire": "Read online",
        "pdf": "Download the PDF",
        "epub": "Download the EPUB",
        "fichier": "Safety in Paragliding - At our own risk and peril",
        "traductions": "This English version is, for now, a machine translation from French and may contain mistakes. A proper translation by pilots from the community is under way: if you prefer, you can wait for this better version. If you would like to help, contact Julien: ",
        "licence": 'Released under the <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.en">CC BY-NC-ND 4.0</a> licence: you may share it freely with credit to the author, with no commercial use and no changes.',
        "autres": "This book is also available in",
        "navigation": "Languages",
        "suggestion": "This book is also available in English.",
        "suggestion_lien": "Read it in English",
    },
    "de": {
        "nom": "Deutsch",
        "titre": "Sicherheit beim Gleitschirmfliegen",
        "sous_titre": "Risiko oder Gefahr?",
        "description": "Unfälle, Statistiken, Mythen und Sicherheitskultur beim Gleitschirmfliegen: ein kostenloses Buch von Julien Garcia, Pilot, Trainer und Unfallermittler.",
        "titre_lecture": "Sicherheit beim Gleitschirmfliegen: das Buch online lesen",
        "description_lecture": "Sicherheit beim Gleitschirmfliegen kostenlos online lesen: das Buch von Julien Garcia über unsere Unfälle, ihre Zahlen und die Überzeugungen unserer Gemeinschaft.",
        "locale": "de_DE",
        "gratuit": "Kostenloses Buch",
        "accueil": "Startseite",
        "introuvable": "Diese Seite gibt es nicht.",
        "image_alt": "Umschlag des Buches Sicherheit beim Gleitschirmfliegen: ein Gleitschirm über den Bergen in der Abenddämmerung",
        "presentation": "Dieses Buch ist kein Lehrbuch für das Fliegen. Es ist ein Blick auf unsere Gemeinschaft und darauf, wie sie über Sicherheit denkt, geschrieben von einem Piloten, Trainer und Unfallermittler. Es ist kostenlos, online zu lesen oder herunterzuladen.",
        "lire": "Online lesen",
        "pdf": "PDF herunterladen",
        "epub": "EPUB herunterladen",
        "fichier": "Sicherheit beim Gleitschirmfliegen - Risiko oder Gefahr",
        "traductions": "Diese deutsche Fassung ist vorerst eine maschinelle Übersetzung aus dem Französischen und kann Fehler enthalten. Eine echte Übersetzung durch Piloten aus der Gemeinschaft ist in Arbeit: Wenn Sie möchten, können Sie auf diese bessere Fassung warten. Wenn Sie mithelfen möchten, schreiben Sie Julien: ",
        "licence": 'Veröffentlicht unter der Lizenz <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.de">CC BY-NC-ND 4.0</a>: Sie dürfen es unter Nennung des Autors frei weitergeben, ohne kommerzielle Nutzung und ohne Änderungen.',
        "autres": "Dieses Buch gibt es auch auf",
        "navigation": "Sprachen",
        "suggestion": "Dieses Buch gibt es auch auf Deutsch.",
        "suggestion_lien": "Auf Deutsch lesen",
    },
    "es": {
        "nom": "Español",
        "titre": "Seguridad en parapente",
        "sous_titre": "¿Riesgo o peligro?",
        "description": "Accidentes, estadísticas, mitos y cultura de la seguridad en parapente: un libro gratuito de Julien Garcia, piloto, entrenador e investigador de accidentes.",
        "titre_lecture": "Seguridad en parapente: leer el libro en línea",
        "description_lecture": "Lea gratis en línea Seguridad en parapente, el libro de Julien Garcia sobre nuestros accidentes, sus cifras y las creencias de nuestra comunidad.",
        "locale": "es_ES",
        "gratuit": "Libro gratuito",
        "accueil": "Inicio",
        "introuvable": "Esta página no existe.",
        "image_alt": "Portada del libro Seguridad en parapente: un parapente sobre las montañas al anochecer",
        "presentation": "Este libro no es un manual de pilotaje. Es una mirada sobre nuestra comunidad y sobre la forma en que piensa la seguridad, escrita por un piloto, entrenador e investigador de accidentes. Es gratuito, para leer en línea o descargar.",
        "lire": "Leer en línea",
        "pdf": "Descargar el PDF",
        "epub": "Descargar el EPUB",
        "fichier": "Seguridad en parapente - Riesgo o peligro",
        "traductions": "Por ahora, esta versión en español es una traducción automática del francés y puede contener errores. Una verdadera traducción, hecha por pilotos de la comunidad, está en marcha: si lo prefiere, puede esperar a esta versión mejorada. Si quiere colaborar, escriba a Julien: ",
        "licence": 'Publicado con la licencia <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es">CC BY-NC-ND 4.0</a>: puede compartirlo libremente citando al autor, sin uso comercial ni modificaciones.',
        "autres": "Este libro también está disponible en",
        "navigation": "Idiomas",
        "suggestion": "Este libro también está disponible en español.",
        "suggestion_lien": "Leerlo en español",
    },
    "fa": {
        "nom": "فارسی",
        "titre": "ایمنی در پاراگلایدر",
        "sous_titre": "آیا مسئولیت خطرهای پرواز و پیامدهایشان با خودمان است؟",
        "description": "سوانح، آمار، باورهای رایج و فرهنگ ایمنی در پاراگلایدر: کتابی رایگان از ژولین گارسیا، خلبان، مربی و کارشناس بررسی سوانح.",
        "titre_lecture": "ایمنی در پاراگلایدر: خواندن آنلاین کتاب",
        "description_lecture": "کتاب «ایمنی در پاراگلایدر» نوشتهٔ ژولین گارسیا را رایگان و آنلاین بخوانید: دربارهٔ سوانح ما، آمارشان و باورهای جامعهٔ پروازی ما.",
        "locale": "fa_IR",
        "gratuit": "کتاب رایگان",
        "accueil": "صفحهٔ اصلی",
        "introuvable": "این صفحه وجود ندارد.",
        "image_alt": "جلد کتاب ایمنی در پاراگلایدر: پاراگلایدری بر فراز کوه‌ها در هنگام غروب",
        "presentation": "این کتاب راهنمای خلبانی نیست. نگاهی است به جامعهٔ پروازی ما و طرز فکرمان دربارهٔ ایمنی، به قلم یک خلبان، مربی و کارشناس بررسی سوانح. کتاب رایگان است و می‌توانید آن را آنلاین بخوانید یا دریافت کنید.",
        "lire": "خواندن آنلاین",
        "pdf": "دریافت PDF",
        "epub": "دریافت EPUB",
        "fichier": "ایمنی در پاراگلایدر",
        # Traduction complète, faite par un pilote bénévole : pas de message sur les traductions en cours.
        "traductions": "",
        "licence": 'منتشرشده با مجوز <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.fa">CC BY-NC-ND 4.0</a>: می‌توانید آن را با ذکر نام نویسنده آزادانه به اشتراک بگذارید، بدون استفادهٔ تجاری و بدون تغییر.',
        "autres": "این کتاب به این زبان‌ها هم در دسترس است:",
        "navigation": "زبان‌ها",
        "suggestion": "این کتاب به فارسی هم در دسترس است.",
        "suggestion_lien": "خواندن به فارسی",
        "auteur": "ژولین گارسیا",
    },
}

CONTACT = "j.garcia@ffvl.fr"

AUTEUR = "Julien Garcia"
LICENCE = "https://creativecommons.org/licenses/by-nc-nd/4.0/"

# Couverture : build/<langue>/couverture.png fait 1600 x 2270 pixels (A5) ; le site
# en affiche une version WebP de 600 pixels de large (couverture.webp, voir le Makefile).
COUVERTURE_WEBP = (600, 851)
# Image de partage (Open Graph) : og.png, produite par `pages.py --og`.
OG = (1200, 630)


def chemin(depuis, vers):
    """Lien relatif d'une page (racine pour le français) vers une autre."""
    racine = "" if depuis == "fr" else "../"
    return racine + ("" if vers == "fr" else vers + "/")


def bandeau_traductions(langue, style=""):
    """Bandeau annonçant que de vraies traductions sont en cours dans la communauté.

    Affiché en haut de la lecture en ligne traduite (livre.html, pas en français),
    où il est inséré par Pandoc avec un style en ligne. Sur la page d'accueil, le
    même texte figure sous la présentation (voir page()).
    """
    if not PAGES[langue]["traductions"]:
        return ""
    attribut = f' style="{style}"' if style else ""
    lien = f' style="color: inherit; font-weight: bold;"' if style else ""
    return (
        f'  <aside class="traductions" lang="{langue}"{direction(langue)}{attribut}>\n'
        f'    <p>{html.escape(PAGES[langue]["traductions"])}'
        f'<a href="mailto:{CONTACT}"{lien}>{CONTACT}</a></p>\n'
        f"  </aside>\n"
    )


# Style du bandeau dans livre.html, qui n'utilise pas style.css.
STYLE_LIVRE = (
    "border: 2px solid #b8860b; background: #fff8dc; color: #222; "
    "border-radius: 6px; padding: 0 1em; margin: 0 0 2em; font-size: .95em;"
)


def adresse(langue, fichier=""):
    """Adresse absolue d'une page du site (fichier vide : page d'accueil de la langue)."""
    return SITE + chemin("fr", langue) + fichier


def balises_partage(langue, fichier=""):
    """Balises de référencement communes : canonical, hreflang, Open Graph et Twitter.

    Les adresses sont absolues : l'adresse de référence reste securite.jugarcia.fr,
    même si le lecteur arrive par un sous-domaine. `fichier` vaut "" pour la page
    d'accueil et "livre.html" pour la lecture en ligne.
    """
    p = PAGES[langue]
    e = html.escape
    lecture = fichier == "livre.html"
    titre = p["titre_lecture"] if lecture else f'{p["titre"]}. {p["sous_titre"]}'
    description = p["description_lecture"] if lecture else p["description"]
    lignes = [f'<link rel="canonical" href="{adresse(langue, fichier)}">']
    lignes += [f'<link rel="alternate" hreflang="{l}" href="{adresse(l, fichier)}">' for l in LANGUES]
    lignes.append(f'<link rel="alternate" hreflang="x-default" href="{adresse("fr", fichier)}">')
    lignes += [
        f'<meta property="og:type" content="{"article" if lecture else "book"}">',
        f'<meta property="og:site_name" content="{e(p["titre"])}">',
        f'<meta property="og:title" content="{e(titre)}">',
        f'<meta property="og:description" content="{e(description)}">',
        f'<meta property="og:url" content="{adresse(langue, fichier)}">',
        f'<meta property="og:image" content="{adresse(langue, "og.png")}">',
        f'<meta property="og:image:width" content="{OG[0]}">',
        f'<meta property="og:image:height" content="{OG[1]}">',
        f'<meta property="og:image:alt" content="{e(p["image_alt"])}">',
        f'<meta property="og:locale" content="{p["locale"]}">',
    ]
    lignes += [f'<meta property="og:locale:alternate" content="{PAGES[l]["locale"]}">' for l in LANGUES if l != langue]
    if not lecture:
        lignes += [
            f'<meta property="book:author" content="{e(p.get("auteur", AUTEUR))}">',
            '<meta property="book:release_date" content="2026-11">',
        ]
    lignes += [
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(titre)}">',
        f'<meta name="twitter:description" content="{e(description)}">',
        f'<meta name="twitter:image" content="{adresse(langue, "og.png")}">',
    ]
    return lignes


def donnees_structurees(langue):
    """Données structurées schema.org (JSON-LD) : le livre, ses formats et ses traductions."""
    p = PAGES[langue]
    livre = {
        "@context": "https://schema.org",
        "@type": "Book",
        "@id": adresse(langue) + "#livre",
        "name": p["titre"],
        "alternativeHeadline": p["sous_titre"],
        "description": p["description"],
        "author": {"@type": "Person", "name": AUTEUR},
        "inLanguage": langue,
        "url": adresse(langue),
        "image": adresse(langue, "couverture.png"),
        "datePublished": "2026-11",
        "copyrightYear": 2026,
        "copyrightHolder": {"@type": "Person", "name": AUTEUR},
        "license": LICENCE,
        "isAccessibleForFree": True,
        "bookFormat": "https://schema.org/EBook",
        "associatedMedia": [
            {"@type": "MediaObject", "name": p["lire"], "encodingFormat": "text/html", "contentUrl": adresse(langue, "livre.html")},
            {"@type": "MediaObject", "name": "PDF", "encodingFormat": "application/pdf", "contentUrl": adresse(langue, "livre.pdf")},
            {"@type": "MediaObject", "name": "EPUB", "encodingFormat": "application/epub+zip", "contentUrl": adresse(langue, "livre.epub")},
        ],
    }
    if langue == "fr":
        livre["workTranslation"] = [{"@id": adresse(l) + "#livre"} for l in LANGUES if l != "fr"]
    else:
        livre["translationOfWork"] = {"@id": adresse("fr") + "#livre"}
    texte = json.dumps(livre, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{texte}\n</script>'


# Barre de navigation en tête de la lecture en ligne du site (livre.html n'utilise pas style.css).
STYLE_BARRE = """<style>
nav.barre-site { display: flex; flex-wrap: wrap; gap: .4em 1.2em; align-items: baseline; font-family: "DejaVu Sans", Arial, sans-serif; font-size: .9em; border-bottom: 1px solid #ddd; padding: 0 0 .8em; margin: 0 0 2em; }
nav.barre-site a { color: #14213d; }
nav.barre-site .langues { margin-inline-start: auto; display: flex; flex-wrap: wrap; gap: .4em .9em; }
nav.barre-site .langues a { text-decoration: none; }
nav.barre-site .langues a[aria-current="page"] { font-weight: bold; text-decoration: underline; }
img { max-width: 100%; height: auto; }
</style>"""


def entete_lecture(langue):
    """En-tête (dans <head>) de la lecture en ligne du site : référencement et style de la barre."""
    lignes = balises_partage(langue, "livre.html")
    racine = "" if langue == "fr" else "../"
    lignes += [
        f'<link rel="icon" href="{racine}favicon.ico" sizes="32x32">',
        f'<link rel="icon" href="{racine}favicon.svg" type="image/svg+xml">',
        f'<link rel="apple-touch-icon" href="{racine}apple-touch-icon.png">',
        STYLE_BARRE,
    ]
    return "\n".join(lignes) + "\n"


def meta_lecture(langue):
    """Métadonnées Pandoc de la lecture en ligne du site : titre de l'onglet et description."""
    p = PAGES[langue]
    return json.dumps({"pagetitle": p["titre_lecture"], "description-meta": p["description_lecture"]}, ensure_ascii=False)


def barre_lecture(langue):
    """Barre en tête de la lecture en ligne du site : accueil, PDF, EPUB et autres langues."""
    p = PAGES[langue]
    e = html.escape
    langues = " ".join(
        f'<a href="{chemin(langue, l)}livre.html" hreflang="{l}" lang="{l}"{direction(l)}'
        + (' aria-current="page"' if l == langue else "")
        + f">{PAGES[l]['nom']}</a>"
        for l in LANGUES
    )
    return (
        f'<nav class="barre-site" aria-label="{e(p["titre"])}">\n'
        f'  <a href="./">{e(p["accueil"])}</a>\n'
        f'  <a href="livre.pdf" data-goatcounter-click="telechargement-pdf-{langue}">{e(p["pdf"])}</a>\n'
        f'  <a href="livre.epub" data-goatcounter-click="telechargement-epub-{langue}">{e(p["epub"])}</a>\n'
        f'  <span class="langues">{langues}</span>\n'
        f"</nav>\n"
        "<!-- MESURE D'AUDIENCE : remplacé par le script GoatCounter si la variable GOATCOUNTER est définie -->\n"
        + bandeau_traductions(langue, STYLE_LIVRE)
    )


def dimensions_png(chemin_png):
    """Largeur et hauteur d'une image PNG, lues dans son en-tête."""
    with open(chemin_png, "rb") as f:
        return struct.unpack(">II", f.read(24)[16:24])


def images_lecture(fichier, langue):
    """Adapte les images de la lecture en ligne du site.

    Pandoc laisse les adresses des sources (../images/x.png, ../images/fa/x.png).
    Sur le site, les images sont copiées en WebP dans images/ à la racine : depuis
    une traduction (en/livre.html), ../images/ y mène déjà ; depuis la page
    française, il faut images/. On ajoute les dimensions (pas de décalage pendant
    le chargement) et le chargement différé.
    """
    import re

    racine = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    with open(fichier, encoding="utf-8") as f:
        texte = f.read()

    def remplacer(m):
        nom = m.group(1)
        largeur, hauteur = dimensions_png(os.path.join(racine, "images", nom + ".png"))
        prefixe = "images/" if langue == "fr" else "../images/"
        return f'src="{prefixe}{nom}.webp" width="{largeur}" height="{hauteur}" loading="lazy" decoding="async"'

    texte, n = re.subn(r'src="\.\./images/((?:fa/)?[a-z0-9-]+)\.png"', remplacer, texte)
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(texte)
    print(f"{fichier} : {n} image(s)", file=sys.stderr)


def image_partage(langue, couverture):
    """Image de partage 1200 x 630 (Open Graph) en SVG, à convertir avec rsvg-convert.

    Reprend le fond de la couverture : ciel de nuit, montagnes, titre et couverture
    à côté. Pour le persan, la mise en page est inversée (texte à droite).
    """
    import base64
    import textwrap

    p = PAGES[langue]
    e = html.escape
    rtl = langue in RTL
    with open(couverture, "rb") as f:
        donnees = base64.b64encode(f.read()).decode()
    police = "Vazirmatn" if rtl else "DejaVu Serif"
    sans = "Vazirmatn" if rtl else "DejaVu Sans"
    # Couverture : 300 x 426, inclinée d'une ombre.
    cx = 120 if rtl else 780
    x = 1128 if rtl else 72
    ancre = "end" if rtl else "start"
    lignes = textwrap.wrap(p["titre"], 18 if not rtl else 22)
    taille = 64 if len(lignes) <= 2 else 52
    y = 200
    titre = ""
    for i, ligne in enumerate(lignes):
        titre += f'<text x="{x}" y="{y}" font-family="{police}" font-weight="bold" font-size="{taille}" fill="#ffffff" text-anchor="{ancre}">{e(ligne)}</text>\n'
        y += int(taille * 1.15)
    sous = textwrap.wrap(p["sous_titre"], 34 if not rtl else 40)
    y += 20
    sous_titre = ""
    for ligne in sous[:2]:
        sous_titre += f'<text x="{x}" y="{y}" font-family="{police}" font-style="{"normal" if rtl else "italic"}" font-size="30" fill="#f0bd84" text-anchor="{ancre}">{e(ligne)}</text>\n'
        y += 40
    auteur = p.get("auteur", AUTEUR)
    if not rtl:
        auteur = auteur.upper()
    largeur_pastille = 30 + len(p["gratuit"]) * 15
    px = x - largeur_pastille if rtl else x
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{OG[0]}" height="{OG[1]}" viewBox="0 0 {OG[0]} {OG[1]}">
<defs>
<linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#14213d"/><stop offset=".45" stop-color="#1f3355"/><stop offset=".7" stop-color="#2e4a72"/><stop offset=".88" stop-color="#6a6070"/><stop offset="1" stop-color="#c98a64"/>
</linearGradient>
<radialGradient id="ombre"><stop offset="0" stop-color="#000" stop-opacity=".5"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{OG[0]}" height="{OG[1]}" fill="url(#ciel)"/>
<polygon points="0,440 180,380 330,420 470,360 640,430 820,390 1000,440 1200,400 1200,630 0,630" fill="#9b6f6f" opacity=".85"/>
<polygon points="0,500 160,460 320,500 520,450 700,510 900,470 1200,520 1200,630 0,630" fill="#3c3350"/>
<rect y="560" width="{OG[0]}" height="70" fill="#1b1a2e"/>
<rect x="{px}" y="72" rx="17" width="{largeur_pastille}" height="34" fill="#f0bd84"/>
<text x="{px + largeur_pastille / 2}" y="96" font-family="{sans}" font-weight="bold" font-size="17" fill="#1b1a2e" text-anchor="middle" letter-spacing="{0 if rtl else 2}">{e(p["gratuit"] if rtl else p["gratuit"].upper())}</text>
{titre}{sous_titre}<text x="{x}" y="{y + 30}" font-family="{sans}" font-size="20" fill="#e8e4f0" text-anchor="{ancre}" letter-spacing="{0 if rtl else 4}">{e(auteur)}</text>
<text x="{x}" y="604" font-family="DejaVu Sans" font-weight="bold" font-size="26" fill="#ffffff" text-anchor="{ancre}">securite.jugarcia.fr</text>
<ellipse cx="{cx + 150}" cy="532" rx="190" ry="26" fill="url(#ombre)"/>
<image x="{cx}" y="80" width="300" height="426" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/png;base64,{donnees}"/>
</svg>
"""


def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n"


def plan_du_site():
    """sitemap.xml : pages d'accueil et lectures en ligne avec leurs versions dans les autres langues, puis les PDF."""
    jour = datetime.date.today().isoformat()
    entrees = []
    for fichier in ["", "livre.html"]:
        for langue in LANGUES:
            alternates = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{adresse(l, fichier)}"/>' for l in LANGUES
            ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{adresse("fr", fichier)}"/>'
            entrees.append(f"  <url>\n    <loc>{adresse(langue, fichier)}</loc>\n    <lastmod>{jour}</lastmod>{alternates}\n  </url>")
    for langue in LANGUES:
        entrees.append(f"  <url>\n    <loc>{adresse(langue, 'livre.pdf')}</loc>\n    <lastmod>{jour}</lastmod>\n  </url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entrees)
        + "\n</urlset>\n"
    )


def page_introuvable():
    """404.html, servi par GitHub Pages pour toute adresse inconnue, à n'importe quelle profondeur :
    les liens sont donc absolus."""
    e = html.escape
    liens = "\n".join(
        f'      <li lang="{l}"{direction(l)}>{e(PAGES[l]["introuvable"])} '
        f'<a href="{adresse(l)}" hreflang="{l}">{e(PAGES[l]["titre"])}</a></li>'
        for l in LANGUES
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>Page introuvable · {e(PAGES["fr"]["titre"])}</title>
  <link rel="icon" href="{SITE}favicon.ico" sizes="32x32">
  <link rel="stylesheet" href="{SITE}style.css">
</head>
<body>
  <main class="introuvable">
    <div>
      <h1>404</h1>
      <ul>
{liens}
      </ul>
    </div>
  </main>
</body>
</html>
"""


def page(langue):
    p = PAGES[langue]
    racine = "" if langue == "fr" else "../"
    e = html.escape

    # Référencement : canonical, hreflang, Open Graph (balises_partage) et données structurées.
    alternates = "\n".join("  " + ligne for ligne in balises_partage(langue)) + "\n  " + donnees_structurees(langue).replace("\n", "\n  ")

    liens_langues = "\n".join(
        f'    <a href="{chemin(langue, l) or "./"}" hreflang="{l}" lang="{l}"{direction(l)}'
        + (' aria-current="page"' if l == langue else "")
        + f">{PAGES[l]['nom']}</a>"
        for l in LANGUES
    )

    autres = ("، " if langue in RTL else ", ").join(
        f'<a href="{chemin(langue, l) or "./"}" hreflang="{l}" lang="{l}"{direction(l)}>{PAGES[l]["nom"]}</a>'
        for l in LANGUES
        if l != langue
    )

    # Sur la page d'accueil, le message sur les traductions est placé sous la
    # présentation, au même endroit et avec le même style que l'ancien avertissement.
    avertissement = ""
    if p["traductions"]:
        avertissement = (
            f'      <p class="avertissement-ia">{e(p["traductions"])}'
            f'<a href="mailto:{CONTACT}">{CONTACT}</a></p>\n'
        )

    # Sur la page française seulement : si la langue du navigateur correspond
    # à une traduction, on la propose dans un bandeau (sans redirection).
    suggestion = ""
    if langue == "fr":
        textes = {
            l: {"texte": PAGES[l]["suggestion"], "lien": PAGES[l]["suggestion_lien"], "href": l + "/", "dir": "rtl" if l in RTL else "ltr"}
            for l in LANGUES
            if l != "fr"
        }
        suggestion = f"""  <aside class="suggestion" id="suggestion" hidden>
    <div><span id="suggestion-texte"></span> <a id="suggestion-lien" href="#"></a>
    <button type="button" id="suggestion-fermer" aria-label="Fermer">×</button></div>
  </aside>
  <script>
    (function () {{
      var textes = {json.dumps(textes, ensure_ascii=False)};
      try {{ if (localStorage.getItem("langue-ignoree")) return; }} catch (e) {{}}
      var prefs = navigator.languages || [navigator.language || ""];
      for (var i = 0; i < prefs.length; i++) {{
        var l = (prefs[i] || "").slice(0, 2).toLowerCase();
        if (l === "fr") return;
        if (textes[l]) {{
          document.getElementById("suggestion-texte").textContent = textes[l].texte;
          var lien = document.getElementById("suggestion-lien");
          lien.textContent = textes[l].lien;
          lien.href = textes[l].href;
          lien.lang = l;
          document.getElementById("suggestion-texte").lang = l;
          document.getElementById("suggestion").lang = l;
          document.getElementById("suggestion").dir = textes[l].dir;
          document.getElementById("suggestion").hidden = false;
          document.getElementById("suggestion-fermer").onclick = function () {{
            document.getElementById("suggestion").hidden = true;
            try {{ localStorage.setItem("langue-ignoree", "1"); }} catch (e) {{}}
          }};
          return;
        }}
      }}
    }})();
  </script>
"""

    return f"""<!doctype html>
<html lang="{langue}"{direction(langue)}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(p["titre"])}. {e(p["sous_titre"])}</title>
  <meta name="description" content="{e(p["description"])}">
{alternates}
  <link rel="icon" href="{racine}favicon.ico" sizes="32x32">
  <link rel="icon" href="{racine}favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{racine}apple-touch-icon.png">
  <link rel="manifest" href="{racine}site.webmanifest">
  <meta name="theme-color" content="#14213d">
  <link rel="stylesheet" href="{racine}style.css">
</head>
<body>
  <nav class="langues" aria-label="{e(p["navigation"])}">
{liens_langues}
  </nav>
{suggestion}  <main>
    <picture>
      <source srcset="couverture.webp" type="image/webp">
      <img src="couverture.png" alt="{e(p["image_alt"])}" width="{COUVERTURE_WEBP[0]}" height="{COUVERTURE_WEBP[1]}" fetchpriority="high">
    </picture>
    <div>
      <h1>{e(p["titre"])}</h1>
      <p class="sous-titre">{e(p["sous_titre"])}</p>
      <p class="auteur">{e(p.get("auteur", "Julien Garcia"))}</p>
      <p>{e(p["presentation"])}</p>
{avertissement}      <div class="actions">
        <a class="principal" href="livre.html" data-goatcounter-click="lecture-en-ligne-{langue}" data-goatcounter-title="{e(p["lire"])} ({langue})">{e(p["lire"])}</a>
        <a href="livre.pdf" download="{e(p["fichier"])}.pdf" data-goatcounter-click="telechargement-pdf-{langue}" data-goatcounter-title="PDF ({langue})">{e(p["pdf"])}</a>
        <a href="livre.epub" download="{e(p["fichier"])}.epub" data-goatcounter-click="telechargement-epub-{langue}" data-goatcounter-title="EPUB ({langue})">{e(p["epub"])}</a>
      </div>
      <p class="autres-langues">{e(p["autres"])} {autres}{"" if langue in RTL else "."}</p>
      <p class="licence">© 2026 Julien Garcia. {p["licence"]}</p>
    </div>
  </main>
  <!-- MESURE D'AUDIENCE : remplacé par le script GoatCounter si la variable GOATCOUNTER est définie -->
</body>
</html>
"""


def main():
    # `pages.py --bandeau <langue>` écrit seulement le bandeau, pour livre.html.
    if sys.argv[1] == "--bandeau":
        sys.stdout.write(bandeau_traductions(sys.argv[2], STYLE_LIVRE))
        return
    # Lecture en ligne du site (règle html-site du Makefile).
    if sys.argv[1] == "--entete":
        sys.stdout.write(entete_lecture(sys.argv[2]))
        return
    if sys.argv[1] == "--meta":
        sys.stdout.write(meta_lecture(sys.argv[2]))
        return
    if sys.argv[1] == "--barre":
        sys.stdout.write(barre_lecture(sys.argv[2]))
        return
    if sys.argv[1] == "--images":
        images_lecture(sys.argv[2], sys.argv[3])
        return
    # `pages.py --og <langue> <couverture.png>` écrit l'image de partage en SVG.
    if sys.argv[1] == "--og":
        sys.stdout.write(image_partage(sys.argv[2], sys.argv[3]))
        return
    sortie = sys.argv[1]
    for langue in LANGUES:
        dossier = sortie if langue == "fr" else os.path.join(sortie, langue)
        os.makedirs(dossier, exist_ok=True)
        with open(os.path.join(dossier, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(langue))
    for nom, contenu in [("robots.txt", robots()), ("sitemap.xml", plan_du_site()), ("404.html", page_introuvable())]:
        with open(os.path.join(sortie, nom), "w", encoding="utf-8") as f:
            f.write(contenu)


if __name__ == "__main__":
    main()
