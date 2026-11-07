"""Génère les pages d'accueil du site, une par langue.

Usage : python3 site/pages.py build/site
        python3 site/pages.py --bandeau en > bandeau.html

Écrit build/site/index.html (français) et build/site/<langue>/index.html
pour chaque traduction. Chaque page propose les autres langues, et la page
française suggère la traduction qui correspond à la langue du navigateur.
"""

import html
import os
import sys

# Ordre d'affichage du sélecteur de langue.
LANGUES = ["fr", "en", "de", "es"]

PAGES = {
    "fr": {
        "nom": "Français",
        "titre": "Sécurité en parapente",
        "sous_titre": "À nos risques et périls ?",
        "description": "Un livre de Julien Garcia sur la sécurité en parapente, à lire en ligne ou à télécharger gratuitement.",
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
        "description": "A book by Julien Garcia on paragliding safety, free to read online or download. English translation.",
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
        "description": "Ein Buch von Julien Garcia über Sicherheit beim Gleitschirmfliegen, kostenlos online zu lesen oder herunterzuladen. Deutsche Übersetzung.",
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
        "description": "Un libro de Julien Garcia sobre la seguridad en parapente, gratuito para leer en línea o descargar. Traducción al español.",
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
}

CONTACT = "j.garcia@ffvl.fr"


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
        f'  <aside class="traductions" lang="{langue}"{attribut}>\n'
        f'    <p>{html.escape(PAGES[langue]["traductions"])}'
        f'<a href="mailto:{CONTACT}"{lien}>{CONTACT}</a></p>\n'
        f"  </aside>\n"
    )


# Style du bandeau dans livre.html, qui n'utilise pas style.css.
STYLE_LIVRE = (
    "border: 2px solid #b8860b; background: #fff8dc; color: #222; "
    "border-radius: 6px; padding: 0 1em; margin: 0 0 2em; font-size: .95em;"
)


def page(langue):
    p = PAGES[langue]
    racine = "" if langue == "fr" else "../"
    e = html.escape

    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{l}" href="{chemin(langue, l) or "./"}">'
        for l in LANGUES
    )

    liens_langues = "\n".join(
        f'    <a href="{chemin(langue, l) or "./"}" hreflang="{l}" lang="{l}"'
        + (' aria-current="page"' if l == langue else "")
        + f">{PAGES[l]['nom']}</a>"
        for l in LANGUES
    )

    autres = ", ".join(
        f'<a href="{chemin(langue, l) or "./"}" hreflang="{l}" lang="{l}">{PAGES[l]["nom"]}</a>'
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
            l: {"texte": PAGES[l]["suggestion"], "lien": PAGES[l]["suggestion_lien"], "href": l + "/"}
            for l in LANGUES
            if l != "fr"
        }
        import json

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
<html lang="{langue}">
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
    <img src="couverture.png" alt="{e(p["image_alt"])}">
    <div>
      <h1>{e(p["titre"])}</h1>
      <p class="sous-titre">{e(p["sous_titre"])}</p>
      <p class="auteur">Julien Garcia</p>
      <p>{e(p["presentation"])}</p>
{avertissement}      <div class="actions">
        <a class="principal" href="livre.html" data-goatcounter-click="lecture-en-ligne-{langue}" data-goatcounter-title="{e(p["lire"])} ({langue})">{e(p["lire"])}</a>
        <a href="livre.pdf" download="{e(p["fichier"])}.pdf" data-goatcounter-click="telechargement-pdf-{langue}" data-goatcounter-title="PDF ({langue})">{e(p["pdf"])}</a>
        <a href="livre.epub" download="{e(p["fichier"])}.epub" data-goatcounter-click="telechargement-epub-{langue}" data-goatcounter-title="EPUB ({langue})">{e(p["epub"])}</a>
      </div>
      <p class="autres-langues">{e(p["autres"])} {autres}.</p>
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
    sortie = sys.argv[1]
    for langue in LANGUES:
        dossier = sortie if langue == "fr" else os.path.join(sortie, langue)
        os.makedirs(dossier, exist_ok=True)
        with open(os.path.join(dossier, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(langue))


if __name__ == "__main__":
    main()
