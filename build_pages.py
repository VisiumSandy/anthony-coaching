"""Génère transformations.html à partir de la liste PEOPLE ci-dessous (photos dans assets/avant_apres/).
Usage : python build_pages.py"""
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
    dict(dir="teo", nom="Téo", resultat="+4 kg de muscle", duree="3 mois",
         texte="Militaire, Téo n'arrivait pas à prendre du poids à cause de son métier. Résultat : 4 kg de muscle en 3 mois et une augmentation de la force maximale.",
         vues=[("Face", "avant (2).png", "apres (3).png"),
               ("Profil", "avant (1).png", "apres (2).png"),
               ("Dos", "avant (3).png", "apres (1).png")]),
    dict(dir="lea", nom="Léa", resultat="-10 kg", duree="3 mois",
         texte="Perte de masse grasse et augmentation de la masse musculaire. Un physique beaucoup plus tonique et plus d'énergie au quotidien.",
         vues=[("Profil", "avant.png", "apres.png")]),
    dict(dir="clara", nom="Clara", resultat="Moins de gras, plus de muscle", duree="environ 6 mois",
         texte="En quelques mois, nous avons perdu du gras pour faire place à plus de muscle. Un résultat physique remarquable, et un semi-marathon terminé : on peut allier la force, l'endurance et un beau physique.",
         vues=[("Face", "avant (2).png", "apres (1).png"),
               ("Profil", "avant (3).png", "apres (2).png"),
               ("Dos", "avant (1).png", "apres (3).png")]),
    dict(dir="nilson", nom="Nilson", resultat="+5 kg sec", duree="3 mois",
         texte="Une énorme transformation en 3 mois pour quelqu'un qui n'arrivait pas à prendre 500 g avant le suivi. Une grosse amélioration de son hygiène de vie, plus de confiance en soi, et la musculation est devenue sa nouvelle passion.",
         vues=[("Face", "avant.png", "apres.png")]),
    dict(dir="amad", nom="Amad", resultat="+18 kg", duree="",
         texte="Un travail de fond qui a pris du temps, mais le résultat est au rendez-vous. Un client qui a toujours rêvé d'être très massif et musclé à la fois.",
         vues=[("Avant / après", "avant.png", "apres.png")]),
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

# ---------------------------------------------------------------
# PARCOURS D'ANTHONY : fresque chronologique
# Photos (optionnelles) dans assets/parcours/ : 2019.jpg, 2022.jpg, 2023.jpg, 2024.jpg, 2026.jpg
# + avant.jpg et apres.jpg (en haut de la page). Une photo absente n'est pas affichée.
# ---------------------------------------------------------------
PARCOURS_SRC = ROOT / "assets" / "parcours"
PARCOURS_OUT = ROOT / "assets" / "parcours-web"
INTRO = "Je m'appelle Anthony et je vais vous raconter mon histoire."
STEPS = [
    ("2019", "17 octobre 2019. Un tournant majeur dans ma vie.", [
        "C'est le jour où j'ai poussé les portes d'une salle de sport pour la première fois, avec un objectif : prendre de la masse musculaire.",
        "À l'époque, je faisais 1 m 70 pour 52 kg et je ne me sentais pas à l'aise dans mon corps. Il fallait que ça change.",
        "Pas de coach, pas d'accompagnement. J'ai appris seul, en me documentant quotidiennement.",
        "Pendant presque 2 ans, je me suis entraîné 6 fois par semaine, je mangeais énormément… mais les résultats restaient très limités.",
        "Mon erreur ? Copier les entraînements et les méthodes des autres sans tenir compte de mon propre profil. À l'époque, je travaillais sur le chantier et ma dépense calorique était très importante. Mon alimentation et mon entraînement n'étaient tout simplement pas adaptés à mes besoins.",
        "Le déclic est arrivé lorsque j'ai compris qu'il fallait arrêter de copier les autres et commencer à adapter mon entraînement et mon alimentation à MOI. En quelques mois, j'ai obtenu des résultats qui m'avaient demandé presque 2 ans auparavant.",
        "C'est ce que je veux transmettre aujourd'hui en tant que coach : chaque personne est différente et la progression passe avant tout par un accompagnement personnalisé.",
    ]),
    ("2022", "2022. Une expérience qui a changé ma vision du sport.", [
        "J'ai passé quelques mois où j'ai pu expérimenter le métier de militaire au 27e bataillon de chasseurs alpins, et c'est là que j'ai eu un véritable déclic.",
        "Être musclé, c'est bien. Mais avoir un corps complet, performant et capable de s'adapter à toutes les situations, c'est encore mieux ! Marche en montagne, course à pied, escalade, natation, musculation au poids du corps… Des activités exigeantes qui poussent constamment à dépasser ses limites.",
        "J'ai surtout compris une chose : ce n'est pas forcément le plus musclé qui va le plus loin, mais celui qui possède le meilleur mental. Le mental, c'est cette capacité à continuer quand le corps te demande d'arrêter. C'est souvent dans ces moments-là que tout se joue.",
        "Cette expérience a profondément changé ma vision du sport et ma façon d'aborder le coaching. Être performant, ce n'est pas seulement construire du muscle, c'est développer un corps fort, endurant et un mental à toute épreuve.",
    ]),
    ("2023", "2023. Je décide de faire de ma passion mon métier.", [
        "Je passe mon BPJEPS avec un objectif bien précis : vivre du sport et de ce qui m'anime au quotidien.",
        "Ma passion ? Le sport, le dépassement de soi, mais surtout l'envie d'aider les autres à atteindre leurs objectifs dans les meilleures conditions possibles.",
        "Je ne voulais pas simplement devenir coach, je voulais transmettre ce que le sport m'avait appris et accompagner chaque personne dans sa propre évolution. Parce que ma plus grande satisfaction, c'est de voir les autres progresser.",
    ]),
    ("2024", "2024. Je fais mes premiers pas en tant que coach sportif.", [
        "Je commence à accompagner mes premiers clients en salle de sport et j'ai la chance de travailler avec plus d'une centaine de personnes, pour des séances ponctuelles ou des suivis à long terme.",
        "Perte de poids, prise de masse, développement de la force et de l'endurance, préparation physique pour le MMA, la boxe ou le football, préparation aux concours de la douane, de la gendarmerie ou de l'armée… J'ai également accompagné des personnes qui souhaitaient simplement entretenir leur forme et prendre soin de leur santé.",
        "Une expérience humaine et professionnelle incroyable, qui m'a permis de développer mes compétences, d'apprendre énormément et surtout de faire de très belles rencontres. Un immense merci à toutes les personnes qui m'ont accordé leur confiance et qui ont contribué, de près ou de loin, à mon évolution.",
    ]),
    ("2026", "2026. Un nouveau chapitre commence.", [
        "Je relance mon activité avec un objectif qui me tient particulièrement à cœur : ouvrir mon propre studio de coaching.",
        "Un rêve que je porte depuis longtemps : avoir mon propre espace, pouvoir travailler librement et proposer un accompagnement sans dépendre d'une salle de sport. Ce projet a demandé du temps, beaucoup d'investissement et de la détermination. Mais pour moi, ça n'a pas de prix.",
        "Aujourd'hui, ce rêve est devenu réalité. Je suis fier de pouvoir vous accueillir dans mon propre studio et de vous accompagner dans les meilleures conditions. À très vite !",
    ]),
]


def photo(stem):
    """Cherche assets/parcours/<stem>.(jpg|jpeg|png|webp), le convertit en JPG léger, renvoie le chemin web ou None."""
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        src = PARCOURS_SRC / (stem + ext)
        if src.exists():
            PARCOURS_OUT.mkdir(parents=True, exist_ok=True)
            dst = PARCOURS_OUT / (stem + ".jpg")
            if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                from PIL import Image
                im = Image.open(src).convert("RGB")
                im.thumbnail((1000, 1250))
                im.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
            return dst.relative_to(ROOT).as_posix()
    return None


TIMELINE = [("2019", "1re séance, 52 kg"), ("2022", "Chasseurs alpins"), ("2023", "BPJEPS"), ("2024", "Premiers clients"), ("2026", "Mon studio")]


def timeline():
    li = chr(10).join(f'          <li><a href="#y{y}" aria-label="{y} : {t}"><span class="tl__dot" aria-hidden="true"></span><span class="tl__y">{y}</span><span class="tl__t">{t}</span></a></li>' for y, t in TIMELINE)
    return f'<nav class="tl" aria-label="Chronologie du parcours" data-reveal><ol>{chr(10)}{li}{chr(10)}        </ol></nav>'


def step_html(year, title, paras):
    title = title.removeprefix(year + ". ")
    p = photo(year)
    img = f'<figure class="pc__photo"><img src="{p}" loading="lazy" alt="Anthony en {year}"></figure>' if p else ""
    body = "\n".join(f"              <p>{html.escape(t)}</p>" for t in paras)
    return f'''          <article class="pc__step" id="y{year}" data-reveal>
            <span class="pc__year" aria-hidden="true">{year}</span>
            <div class="pc__card">
              <h2>{html.escape(title)}</h2>
{body}
              {img}
            </div>
          </article>'''


def before_after():
    av, ap = photo("avant"), photo("apres")
    if not (av and ap):
        return ""

    def ph(p, tag):
        cls = " tr__tag--r" if tag == "Après" else ""
        return (f'<figure class="tr__ph"><img src="{p}" loading="lazy" alt="Anthony {tag.lower()}">'
                f'<span class="tr__tag{cls}">{tag}</span></figure>')

    return f'<div class="tr__row pc__pair" data-reveal>{ph(av, "Avant")}{ph(ap, "Après")}</div>'


# ---------------------------------------------------------------
# Génération des pages à partir de l'enveloppe (header/footer) de index.html
# ---------------------------------------------------------------
page = (ROOT / "index.html").read_text(encoding="utf-8")
head0, rest = page.split('<main id="main">', 1)
_, tail0 = rest.split("</main>", 1)
HOME_TITLE = "<title>Anthony Coaching — Coach perte de poids et musculation</title>"
HOME_DESC = ('content="Coach sportif spécialisé perte de poids : programme d\'entraînement, '
             'plan nutrition et suivi hebdomadaire sur WhatsApp. Appelle Anthony pour démarrer."')


def shell(file, title, desc, main):
    head = head0.replace('href="#', 'href="index.html#')
    tail = tail0.replace('href="#', 'href="index.html#')
    head = head.replace(HOME_TITLE, f"<title>{title}</title>")
    head = head.replace(HOME_DESC, f'content="{desc}"', 1)
    head = head.replace('href="https://www.example.com/"', f'href="https://www.example.com/{file}"')
    head = head.replace(f'<a href="{file}">', f'<a href="{file}" aria-current="page">')
    (ROOT / file).write_text(head + main + tail, encoding="utf-8")


def final(h):
    return f'''    <section class="final" id="contact">
      <div class="wrap final__in">
        <h2 data-reveal>{h}</h2>
        <p data-reveal>Premier échange gratuit, sans engagement.</p>
        <a class="btn btn--primary btn--xl" href="tel:+33663959355" data-call data-reveal>
          <svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>
          <span data-phone-label>06 63 95 93 55</span>
        </a>
      </div>
    </section>
  </main>'''


cards = chr(10).join(card(p) for p in PEOPLE)

shell("transformations.html", "Transformations — Anthony Coaching",
      "Avant / après des clients d'Anthony Coaching : résultats réels, durée et parcours de chacun.",
      f'''<main id="main">
    <!-- Page générée par build_pages.py : ne pas modifier à la main -->
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

''' + final("Ta transformation<br>commence ici."))

steps = chr(10).join(step_html(*s) for s in STEPS)
shell("parcours.html", "Mon parcours — Anthony Coaching",
      "L'histoire d'Anthony, coach sportif : de 52 kg en 2019 à son propre studio de coaching en 2026.",
      f'''<main id="main">
    <!-- Page générée par build_pages.py : ne pas modifier à la main -->
    <section class="section trpage pcpage">
      <div class="wrap">
        <a class="tr__back" href="index.html#bio">&larr; Retour au site</a>
        <h1 class="section__title" data-reveal>Mon parcours</h1>
        <p class="section__sub" data-reveal>{html.escape(INTRO)}</p>
        {timeline()}
        {before_after()}
        <div class="pc">
{steps}
        </div>
      </div>
    </section>

''' + final("On commence<br>quand tu veux."))

print(f"transformations.html ({len(PEOPLE)} transformations) et parcours.html générés")
