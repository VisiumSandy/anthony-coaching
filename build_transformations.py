"""Génère transformations.html à partir de la liste PEOPLE ci-dessous (photos dans assets/avant_apres/).
Usage : python build_transformations.py"""
import html
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "assets" / "avant_apres"   # photos d'origine (PNG)
OUT = ROOT / "assets" / "transfo"       # versions web légères générées (JPG)

# ---------------------------------------------------------------
# DONNÉES : une entrée par personne. Pour chaque vue : (libellé, avant, après)
# Les fichiers sont ceux de assets/avant_apres/<dossier>/
# ---------------------------------------------------------------
PEOPLE = [
    dict(dir="paul", nom="Paul", resultat="-9 kg", duree="3 mois",
         texte="Perte de masse grasse, augmentation de la force et du cardio.",
         vues=[("Face", "face_apres_paul (2).png", "face_apres_paul (1).png"),
               ("Dos", "dos_avant_paul (1).png", "dos_avant_paul (2).png")]),
    dict(dir="lola", nom="Lola", resultat="+6 kg propre", duree="quelques mois",
         texte="Un fessier beaucoup plus galbé et une prise de masse musculaire sur tout le corps.",
         vues=[("Profil", "avant.png", "apres.png")]),
    dict(dir="teo", nom="Téo", resultat="+4 kg sec", duree="3 mois",
         texte="Une prise de masse sèche : du muscle, sans gras en trop.",
         vues=[("Face", "avant (2).png", "apres (3).png"),
               ("Profil", "avant (1).png", "apres (2).png"),
               ("Dos", "avant (3).png", "apres (1).png")]),
    dict(dir="lea", nom="Léa", resultat="-10 kg", duree="3 mois",
         texte="Dix kilos en moins en trois mois, sans régime extrême.",
         vues=[("Profil", "avant.png", "apres.png")]),
    dict(dir="clara", nom="Clara", resultat="Transformation", duree="environ 6 mois",
         texte="Six mois de travail, sous tous les angles.",
         vues=[("Face", "avant (2).png", "apres (1).png"),
               ("Profil", "avant (3).png", "apres (2).png"),
               ("Dos", "avant (1).png", "apres (3).png")]),
    dict(dir="nilson", nom="Nilson", resultat="+5 kg propre", duree="3 mois",
         texte="Cinq kilos de muscle propre en trois mois.",
         vues=[("Face", "avant.png", "apres.png")]),
    dict(dir="carl", nom="Carl", resultat="-7 kg", duree="", feature=True,
         texte="Une perte de poids, mais surtout un changement de mindset : Carl a acheté un tapis de course pour s'entraîner chez lui, alors que quelques semaines plus tôt il détestait le sport.",
         vues=[("Avant / après", "avant.png", "apres.png")]),
]


def web(person, name):
    """Convertit le PNG d'origine en JPG léger (une seule fois) et renvoie son chemin web."""
    src = SRC / person["dir"] / name
    if not src.exists():
        return None
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f'{person["dir"]}-{Path(name).stem}'.replace(" ", "").replace("(", "").replace(")", "")
    dst = OUT / (stem + ".jpg")
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        from PIL import Image
        im = Image.open(src).convert("RGB")
        im.thumbnail((800, 1000))
        im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
    return dst.relative_to(ROOT).as_posix()


def ph(p, tag, alt):
    if p:
        return (f'<figure class="tr__ph"><img src="{html.escape(p)}" width="800" height="1000" loading="lazy" alt="{html.escape(alt)}">'
                f'<span class="tr__tag{" tr__tag--r" if tag == "Après" else ""}">{tag}</span></figure>')
    return f'<figure class="tr__ph"><span class="tr__miss">Photo {tag.lower()}</span></figure>'


def card(person):
    nom = html.escape(person["nom"])
    rows = []
    for label, av, ap in person["vues"]:
        view = "" if len(person["vues"]) == 1 and label == "Avant / après" else f'<p class="tr__view">{label}</p>'
        rows.append(f'''            <div class="tr__pair">
              {view}
              <div class="tr__row">
                {ph(web(person, av), "Avant", f"{person['nom']} avant ({label.lower()})")}
                {ph(web(person, ap), "Après", f"{person['nom']} après ({label.lower()})")}
              </div>
            </div>''')
    meta = html.escape(person["duree"])
    cls = "tr tr--feature" if person.get("feature") else "tr"
    return f'''          <article class="{cls}" data-reveal>
            <div class="tr__head">
              <p class="tr__res">{html.escape(person["resultat"])}</p>
              <p class="tr__meta"><strong>{nom}</strong>{" · " + meta if meta else ""}</p>
            </div>
{chr(10).join(rows)}
            <p class="tr__desc">{html.escape(person["texte"])}</p>
          </article>'''


cards = chr(10).join(card(p) for p in PEOPLE)
folders = PEOPLE

page = (ROOT / "index.html").read_text(encoding="utf-8")
head, rest = page.split('<main id="main">', 1)
_, tail = rest.split("</main>", 1)

# Liens d'ancre du header/menu -> retour vers l'accueil
head = head.replace('href="#', 'href="index.html#')
tail = tail.replace('href="#', 'href="index.html#')
head = head.replace("<title>Anthony Coaching — Coach perte de poids et musculation</title>",
                    "<title>Transformations — Anthony Coaching</title>")
head = head.replace('content="Coach sportif spécialisé perte de poids : programme d\'entraînement, plan nutrition et suivi hebdomadaire sur WhatsApp. Appelle Anthony pour démarrer."',
                    'content="Avant / après des clients d\'Anthony Coaching : résultats réels, durée et parcours de chacun."', 1)
head = head.replace('href="https://www.example.com/"', 'href="https://www.example.com/transformations.html"')
head = head.replace('<a href="transformations.html">', '<a href="transformations.html" aria-current="page">')

main = f'''<main id="main">
    <!-- Page générée par build_transformations.py : ne pas modifier à la main -->
    <section class="section ba-sec trpage">
      <div class="wrap">
        <a class="tr__back" href="index.html#resultats">&larr; Retour au site</a>
        <h1 class="section__title" data-reveal>Les transformations</h1>
        <p class="section__sub" data-reveal>Photos publiées avec l'accord des clients. Les résultats varient selon chaque personne.</p>
        <div class="trgrid">
{cards}
        </div>
      </div>
    </section>

    <section class="final" id="contact">
      <div class="wrap final__in">
        <h2 data-reveal>Ta transformation<br>commence ici.</h2>
        <p data-reveal>Premier échange gratuit, sans engagement.</p>
        <a class="btn btn--primary btn--xl" href="tel:+33663959355" data-call data-reveal>
          <svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>
          <span data-phone-label>06 63 95 93 55</span>
        </a>
      </div>
    </section>
  </main>'''

(ROOT / "transformations.html").write_text(head + main + tail, encoding="utf-8")
print(f"transformations.html généré ({len(folders)} transformation(s))")
