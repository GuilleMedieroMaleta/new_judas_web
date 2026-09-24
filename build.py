#!/usr/bin/env python3
"""
Genera las páginas estáticas de la web de JUDAS.

La cabecera, la navegación y el pie viven aquí una sola vez.
Para cambiar el menú o el pie de toda la web, edita este archivo
y ejecuta:  python3 build.py
"""

from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
SITE_NAME = "JUDAS"
BASE_URL = ""  # p. ej. "https://judasmiranda.es" para las etiquetas Open Graph

NAV = [
    ("index.html", "Inicio"),
    ("historia.html", "Historia"),
    ("musicos.html", "Músicos"),
    ("fotos.html", "Fotos"),
    ("videos.html", "Vídeos"),
    ("conciertos.html", "Conciertos"),
    ("prensa.html", "Prensa"),
    ("50-aniversario.html", "50 años"),
]

FOOTER = (
    "Archivo web dedicado a JUDAS, grupo de Miranda de Ebro. La información se "
    "amplía con documentación, fotografías y recuerdos aportados por fuentes "
    "públicas y por quienes vivieron la historia del grupo."
)

LAYOUT = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0a0a0a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site}">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{base}logo.png">
<link rel="canonical" href="{base}{slug}">
<link rel="icon" href="logo.png" type="image/png">
<link rel="apple-touch-icon" href="logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;500&display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="logo.png" width="108" height="58" alt="JUDAS, vintage music, desde 1975"></a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="menu">Menú</button>
    <nav class="nav" id="menu" data-nav aria-label="Secciones de la web">
      <ul>
{nav}
      </ul>
    </nav>
  </div>
</header>

<main id="contenido">
{main}
</main>

<footer class="site-footer">
  <div class="wrap"><p>{footer}</p></div>
</footer>

<script src="js/site.js?v=3" defer></script>
</body>
</html>
"""


def nav_html(current: str) -> str:
    out = []
    for href, label in NAV:
        if href == "index.html" and current == "index.html":
            continue  # el logo ya lleva a la portada
        out.append(f'        <li><a href="{href}">{label}</a></li>')
    return "\n".join(out)


def section(body: str, extra_class: str = "") -> str:
    cls = f"section {extra_class}".strip()
    return f'<section class="{cls}">\n  <div class="wrap">\n{body}\n  </div>\n</section>'


def cards(items, link=False, wide=False) -> str:
    cls = "grid grid--wide" if wide else "grid"
    rows = []
    for item in items:
        if link:
            href, title, text = item
            rows.append(
                f'      <article class="card card--link"><a href="{href}">'
                f"<h3>{title}</h3><p>{text}</p></a></article>"
            )
        else:
            title, text = item
            rows.append(f'      <article class="card"><h3>{title}</h3><p>{text}</p></article>')
    return f'    <div class="{cls}">\n' + "\n".join(rows) + "\n    </div>"


R2_PUBLIC = "https://pub-b47a15cd476946818777e182bcc31592.r2.dev"


def media_src(path: str) -> str:
    href = "/".join(quote(part, safe=".-") for part in path.split("/"))
    if path.startswith(("fotos/", "videos/web/", "videos/hero/")):
        return f"{R2_PUBLIC}/{href}"
    return href


VIDEOS = [
    (
        "videos/hero/grupo-judas.mp4",
        "Grupo JUDAS",
        "Miranda de Ebro · Burgos · España",
    ),
    (
        "videos/hero/judas-amador.mp4",
        "JUDAS y Amador Izquierdo",
        "Miranda de Ebro · Burgos · España",
    ),
    (
        "videos/hero/actuacion.mp4",
        "Actuación",
        "Grabación del grupo en directo.",
    ),
    (
        "videos/hero/actuacion-2.mp4",
        "Actuación",
        "Otra grabación de archivo en directo.",
    ),
]


def hero_bg_videos(items) -> str:
    clips = []
    for i, (src, _title, _caption) in enumerate(items):
        href = media_src(src)
        active = ' class="is-active" autoplay' if i == 0 else ""
        clips.append(
            f'    <video{active} muted playsinline loop preload="auto" tabindex="-1">'
            f'<source src="{href}" type="video/mp4"></video>'
        )
    return (
        '  <div class="hero-bg" data-hero-bg data-interval="5000" aria-hidden="true">\n'
        + "\n".join(clips)
        + "\n  </div>"
    )


def archive_photos() -> list:
    folder = ROOT / "fotos" / "archivo"
    if not folder.is_dir():
        return []
    items = []
    for path in sorted(folder.glob("*.jpg")):
        title = path.stem.replace("_", " ").replace("  ", " ").strip()
        items.append((path.relative_to(ROOT).as_posix(), title, "Archivo fotográfico"))
    return items


VIDEO_LABELS = {
    "grupo-judas.mp4": ("Grupo JUDAS", "Miranda de Ebro · Burgos · España"),
    "judas-amador.mp4": ("JUDAS y Amador Izquierdo", "Miranda de Ebro · Burgos · España"),
    "actuacion.mp4": ("Actuación", "Grabación del grupo en directo."),
    "actuacion-2.mp4": ("Actuación", "Otra grabación de archivo en directo."),
    "have-you-ever-seen-the-rain.mp4": ("Have You Ever Seen the Rain", "JUDAS en directo."),
    "mp41.mp4": ("Actuación", "Grabación de archivo."),
    "archivo.mp4": ("Archivo", "Grabación del grupo."),
    "50-aniversario.mp4": ("50 aniversario", "11 de enero de 2025."),
    "en-directo.mp4": ("En directo", "Actuación del grupo."),
    "leon-de-oro.mp4": ("León de Oro", "25 de febrero de 2025."),
    "whatsapp-2026-07-29.mp4": ("Grabación reciente", "29 de julio de 2026."),
}


def web_videos() -> list:
    folder = ROOT / "videos" / "web"
    if not folder.is_dir():
        return []
    items = []
    for path in sorted(folder.glob("*.mp4")):
        title, caption = VIDEO_LABELS.get(
            path.name, (path.stem.replace("-", " "), "Archivo audiovisual")
        )
        items.append((path.relative_to(ROOT).as_posix(), title, caption))
    return items


def exhibit(items, kind="img") -> str:
    rows = []
    for item in items:
        src, title, caption = item
        href = media_src(src)
        if kind == "video":
            media = (
                f'<video controls preload="metadata" playsinline>'
                f'<source src="{href}" type="video/mp4">'
                "Tu navegador no puede reproducir este vídeo."
                "</video>"
            )
        else:
            media = f'<img src="{href}" alt="{title}" loading="lazy">'
        rows.append(
            "      <figure>"
            f"{media}"
            f"<figcaption><strong>{title}</strong><span>{caption}</span></figcaption>"
            "</figure>"
        )
    return '    <div class="exhibit">\n' + "\n".join(rows) + "\n    </div>"


def timeline(events) -> str:
    rows = [
        f'      <li><span class="when">{when}</span><p>{text}</p></li>'
        for when, text in events
    ]
    return '    <ol class="timeline">\n' + "\n".join(rows) + "\n    </ol>"


# --- Contenido de cada página ---------------------------------------------

HERO = (
    '<section class="hero">\n'
    + hero_bg_videos(VIDEOS)
    + "\n"
    '  <div class="wrap">\n'
    '    <img class="hero-logo" src="logo.png" width="520" height="281" alt="">\n'
    '    <h1 class="sr-only">JUDAS · Vintage Music · Miranda de Ebro</h1>\n'
    '    <p class="hero-lede">Medio siglo de música, escenarios y amigos en Miranda de Ebro.</p>\n'
    '    <p><a class="btn btn--strong" href="historia.html">Empezar por la historia</a></p>\n'
    "  </div>\n"
    "</section>"
)

PAGES = {
    "index.html": dict(
        title="JUDAS · Vintage Music · Miranda de Ebro",
        description=(
            "Archivo web del grupo JUDAS, de Miranda de Ebro: historia, músicos, "
            "conciertos, prensa y documentación desde los años setenta."
        ),
        main="\n".join(
            [
                HERO,
                section(
                    "    <h2>Por dónde empezar</h2>\n"
                    + cards(
                        [
                            ("historia.html", "Historia", "Los comienzos, los cambios de formación, los parones y el regreso."),
                            ("musicos.html", "Músicos", "Quién ha pasado por el grupo y quién lo forma hoy."),
                            ("fotos.html", "Fotos", "Un archivo fotográfico que iremos completando con material de distintas épocas."),
                            ("videos.html", "Vídeos", "Actuaciones, televisión, entrevistas y material audiovisual."),
                            ("conciertos.html", "Conciertos", "Escenarios, actuaciones señaladas y recuerdos de carretera."),
                            ("prensa.html", "Prensa", "Noticias y documentos publicados sobre el grupo."),
                        ],
                        link=True,
                    )
                ),
                section(
                    '    <blockquote class="quote"><p>La parte que falta no está'
                    " necesariamente en Internet.</p></blockquote>\n"
                    "    <p>Puede estar en una caja de fotos, una cinta, un cartel guardado"
                    " durante cincuenta años o en la memoria de alguien que estuvo allí."
                    " Esta web nace para juntar esas piezas: lo que está documentado, lo"
                    " contamos; lo que todavía no podemos comprobar, lo dejamos señalado.</p>"
                ),
            ]
        ),
    ),
    "historia.html": dict(
        title="Historia · JUDAS",
        description="De los años setenta hasta hoy: origen, televisión, parones y regreso del grupo JUDAS de Miranda de Ebro.",
        main=section(
            "    <h2>De los setenta hasta hoy</h2>\n"
            '    <p class="deck">Hay una pequeña diferencia entre las fuentes: el'
            " Ayuntamiento sitúa el origen en 1975 y una reseña de El Correo habla de"
            " 1974. Las dos referencias forman parte del archivo y, hasta encontrar"
            " documentación anterior que lo aclare, preferimos no esconder la"
            " diferencia.</p>\n"
            + timeline(
                [
                    ("1974–1975", "Siete jóvenes empiezan a reunirse para tocar versiones de Led Zeppelin, Deep Purple, Uriah Heep, Creedence y otros grupos. La formación que se consolidó como cuarteto quedó formada por Toño, Jesús, Fernando y Alfredo."),
                    ("Años 70–80", "El grupo gana presencia en Miranda y fuera de la ciudad. Llega a Televisión Española y comparte escenario con artistas como Miguel Ríos y Leño, entre otros."),
                    ("2014", "Después de un parón importante por motivos laborales, el grupo vuelve a juntarse. Según el Ayuntamiento, bastó un café para recuperar las ganas de tocar."),
                    ("Años 2020", "La pandemia provoca otro parón y Fernando deja el grupo. Los fundadores que continúan buscan nuevos componentes para mantener JUDAS en los escenarios."),
                    ("2025", "JUDAS celebra su 50 aniversario y recibe el León de Oro de la Ciudad de Miranda de Ebro por su aportación cultural."),
                ]
            )
        ),
    ),
    "musicos.html": dict(
        title="Músicos · JUDAS",
        description="Las formaciones de JUDAS: el cuarteto histórico y la banda de seis músicos que celebró el 50 aniversario.",
        main=section(
            "    <h2>Los músicos</h2>\n"
            '    <p class="deck">La historia de JUDAS está hecha por distintas'
            " formaciones. No completamos nombres, fechas ni biografías a base de"
            " suposiciones: esta sección crecerá con documentación y con los recuerdos"
            " de los propios músicos.</p>\n"
            + cards(
                [
                    ("Formación histórica", "<strong>Toño · Jesús · Fernando · Alfredo</strong><br>La formación que las fuentes sitúan como la que alcanzó mayor popularidad."),
                    ("Formación actual, 2025", "<strong>Juan · Manolo · José Luis · Alfredo · Toño · Eduardo</strong><br>La banda de seis músicos con la que el grupo llegó al medio siglo."),
                ],
                wide=True,
            )
            + "\n"
            + '    <div class="grid">\n'
            + "\n".join(
                (
                    f'      <article class="card member member--photo">'
                    f'<div class="member-photo"><img src="{media_src(photo)}" alt="{name}" width="400" height="400"></div>'
                    f'<div class="member-body"><p class="role">{role}</p><h3>{name}</h3><p>{text}</p></div>'
                    "</article>"
                    if photo
                    else f'      <article class="card member"><p class="role">{role}</p>'
                    f"<h3>{name}</h3><p>{text}</p></article>"
                )
                for role, name, text, photo in [
                    ("Voz y guitarra · fundador", "Toño", "Uno de los pilares originales del grupo. Las fuentes lo sitúan como cantante y guitarra del cuarteto histórico, y sigue formando parte de JUDAS en la formación de 2025.", "fotos/toño.jpeg"),
                    ("Batería · fundador", "Jesús", "Fundador y pilar de la banda. Fue el batería del cuarteto más popular. Falleció de forma repentina y su recuerdo estuvo presente en el homenaje del 50 aniversario.", "fotos/jesus.png"),
                    ("Teclado · formación histórica", "Fernando", "Formó parte del cuarteto que alcanzó más popularidad. Tras el parón de la pandemia dejó el grupo, en un momento en el que los fundadores que continuaron buscaron nuevos componentes.", "fotos/fernando.png"),
                    ("Bajo · formación histórica y actual", "Alfredo", "Se incorporó al cuarteto histórico como bajista y es, junto a Toño, uno de los músicos que une aquella etapa con la banda de 2025.", "fotos/alfredo.jpeg"),
                    ("Formación 2025", "Juan", "Entró en JUDAS cuando los fundadores que siguieron buscaban nuevos componentes para mantener el grupo en los escenarios. Formó parte de la banda del 50 aniversario en el Teatro Apolo.", None),
                    ("Guitarra y saxofón · formación 2025", "Manolo", "Uno de los músicos que se sumó en la etapa reciente. Está documentado como integrante de la formación que celebró el medio siglo de JUDAS.", None),
                    ("Piano · formación 2025", "José Luis", "Componente de la banda actual. Las fuentes públicas lo sitúan en el escenario del 50 aniversario, junto al resto de la formación de 2025.", None),
                    ("Sonido e iluminación · formación 2025", "Eduardo", "Integra la formación de seis con la que JUDAS llegó a 2025. Su incorporación forma parte de la etapa posterior a los cambios que siguieron a la pandemia, y es una gran ayuda como técnico de sonido y luz.", None),
                ]
            )
            + "\n    </div>\n"
            '    <p class="note">Pendiente: fotografías de Juan, Manolo, José Luis y'
            " Eduardo, instrumentos de la formación actual, años de incorporación y"
            " testimonios personales con permiso de los protagonistas.</p>"
        ),
    ),
    "fotos.html": dict(
        title="Fotos · JUDAS",
        description="Archivo fotográfico de JUDAS: formación original, primeros escenarios, televisión, regreso y 50 aniversario.",
        main=section(
            "    <h2>Fotos</h2>\n"
            '    <p class="deck">Archivo fotográfico de JUDAS, dispuesto como una'
            " exposición: del cuarteto original a la formación que celebró el medio"
            " siglo.</p>\n"
            + exhibit(
                [
                    ("fotos/images-4.jpeg", "Formación original", "Retrato de estudio del cuarteto."),
                    ("fotos/images-6.jpeg", "Con la furgoneta", "Años 70 · la banda junto a su furgoneta."),
                    ("fotos/descarga.jpeg", "El cuarteto", "Toño, Jesús, Fernando y Alfredo."),
                    ("fotos/images-2.jpeg", "En el escenario", "Concierto con luces de escenario."),
                    ("fotos/images.3.jpeg", "Archivo sobre la mesa", "Revisando fotografías antiguas del grupo."),
                    ("fotos/images-5.jpeg", "Bajo y guitarra", "Actuación de la etapa reciente."),
                    ("fotos/images.jpeg", "Formación 2025", "Los seis músicos con la camiseta de JUDAS."),
                    ("fotos/images-7.jpeg", "Homenaje", "Acto institucional y recuerdo a Jesús."),
                    ("fotos/images-8.jpeg", "Tras el concierto", "La formación actual sobre el escenario."),
                ]
                + archive_photos()
            )
            + "\n"
            '    <p class="note">Las fotografías históricas son la parte que más puede'
            " crecer si antiguos miembros, familiares o seguidores aportan material.</p>"
        ),
    ),
    "videos.html": dict(
        title="Vídeos · JUDAS",
        description="Material audiovisual atribuible al grupo JUDAS de Miranda de Ebro: televisión, actuaciones y entrevistas.",
        main=section(
            "    <h2>Vídeos</h2>\n"
            '    <p class="deck">Material audiovisual atribuible a JUDAS, de Miranda de'
            " Ebro. Esta sección sólo incluye grabaciones que podemos situar en la"
            " historia del grupo.</p>\n"
            + exhibit(web_videos(), kind="video")
            + "\n"
            '    <p class="note">Sigue pendiente localizar el programa <em>Gente joven</em>'
            " y otras entrevistas o cintas antiguas que puedan aparecer.</p>"
        ),
    ),
    "conciertos.html": dict(
        title="Conciertos · JUDAS",
        description="Escenarios y actuaciones señaladas de JUDAS, del telonero de Miguel Ríos al concierto solidario de 2026.",
        main=section(
            "    <h2>Conciertos</h2>\n"
            '    <p class="deck">Actuaciones documentadas hasta ahora. Faltan muchas'
            " verbenas, salas y fiestas por fechar.</p>\n"
            + timeline(
                [
                    ("Años 70–80", "Una de las actuaciones más recordadas: JUDAS fue telonero de Miguel Ríos en la plaza de toros de Haro, según la reseña de El Correo."),
                    ("10 de junio de 2017", "Teatro Apolo de Miranda de Ebro. Concierto a beneficio de Cruz Roja."),
                    ("13 de septiembre de 2019", "Fiestas de Miranda de Ebro: JUDAS y Los 80 Principales en la calle Cantabria."),
                    ("2025", "Teatro Apolo: celebración del 50 aniversario."),
                    ("21 de marzo de 2026", "La Fábrica de Tornillos: concierto solidario por el Sáhara, dentro de un cartel con varios grupos."),
                ]
            )
        ),
    ),
    "prensa.html": dict(
        title="Prensa · JUDAS",
        description="Noticias y documentos publicados sobre JUDAS: Ayuntamiento de Miranda de Ebro, La de Miranda y El Correo.",
        main=section(
            "    <h2>Prensa</h2>\n"
            '    <p class="deck">Fuentes publicadas que sostienen lo que se cuenta en'
            " esta web.</p>\n"
            '    <div class="grid grid--wide">\n'
            + "\n".join(
                f'      <article class="card"><span class="year-mark">{year}</span>'
                f"<h3>{medio}</h3><p>{text}</p>"
                f'<p><a class="btn" href="{href}" target="_blank" rel="noopener">{cta}</a></p></article>'
                for year, medio, text, href, cta in [
                    ("29 de enero de 2025", "Ayuntamiento de Miranda", "Anuncio del León de Oro a JUDAS por su aportación cultural, con un repaso de su trayectoria.", "https://www.mirandadeebro.es/leon-de-oro-al-grupo-judas-por-su-gran-aportacion-cultural-a-miranda/", "Leer el anuncio"),
                    ("25 de febrero de 2025", "La de Miranda", "Crónica del reconocimiento y del 50 aniversario del grupo.", "https://lademiranda.com/2025/02/25/un-leon-de-oro-por-los-50-anos-de-judas-en-los-escenarios/", "Leer la crónica"),
                    ("10 de junio de 2017", "El Correo", "Reseña del concierto de JUDAS en el Teatro Apolo y repaso de sus comienzos.", "https://agenda.elcorreo.com/evento/judas-565368.html", "Leer la reseña"),
                ]
            )
            + "\n    </div>"
        ),
    ),
    "50-aniversario.html": dict(
        title="50 años · JUDAS",
        description="En 2025 JUDAS celebró medio siglo y recibió el León de Oro de la Ciudad de Miranda de Ebro.",
        main=section(
            '    <span class="year-mark">2025</span>\n'
            "    <h2>Medio siglo</h2>\n"
            '    <p class="deck">JUDAS celebró cincuenta años de trayectoria y recibió'
            " el León de Oro de la Ciudad de Miranda de Ebro por su aportación"
            " cultural.</p>\n"
            "    <p>La formación que llegó al 50 aniversario estuvo integrada por Juan,"
            " Manolo, José Luis, Alfredo, Toño y Eduardo. Jesús, fundador y uno de los"
            " pilares del grupo, fue recordado especialmente durante el homenaje.</p>\n"
            "    <p>En el acto, los músicos explicaron que siguen tocando porque les"
            " gusta y que el reconocimiento, aunque no lo esperaban, fue muy especial."
            " También subrayaron algo que aparece una y otra vez en la historia del"
            " grupo: el orgullo de decir que son de Miranda de Ebro.</p>\n"
            '    <blockquote class="quote"><p>Nos vais a tener que aguantar algún añito'
            " más.</p></blockquote>\n"
            '    <p class="note">Fuente principal: Ayuntamiento de Miranda de Ebro y'
            " crónica de La de Miranda TV, febrero de 2025.</p>"
        ),
    ),
}


def build() -> None:
    for slug, page in PAGES.items():
        html = LAYOUT.format(
            title=page["title"],
            description=page["description"],
            site=SITE_NAME,
            base=BASE_URL + "/" if BASE_URL else "",
            slug=slug,
            nav=nav_html(slug),
            main=page["main"],
            footer=FOOTER,
        )
        (ROOT / slug).write_text(html, encoding="utf-8")
        print("escrito:", slug)


if __name__ == "__main__":
    build()
