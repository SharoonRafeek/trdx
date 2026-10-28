#!/usr/bin/env python3
"""Generates the static pages in public/ so header, footer and SEO tags stay identical."""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
SITE = "%%SITE_URL%%"
ARROW = ('<svg class="arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
         'aria-hidden="true"><path d="M1 8h13M9 3l5 5-5 5"/></svg>')

SYSTEMS = [
    ("A.01 / Compute", "T.Core", "trav-core.jpg",
     "An omnichannel software spine that links all our products and services together."),
    ("A.02 / Sensors", "T.Sense", "trav-sense.jpg",
     "Modular sensing units capable of detecting incoming threats before they hit perimeter bounds."),
    ("A.03 / Data &amp; comms", "T.Sync", "trav-sync.jpg",
     "A closed-channel sync for analysis, communications and recon planning."),
    ("A.04 / Act", "T.Pulse", "trav-pulse.jpg",
     "A suite of services for recon actions."),
]

FAQ = [
    ("What does Traversion Dynamics do?",
     "Traversion Dynamics is a deep-tech AI startup that builds modular border defense and counter-UAV systems. Our systems help nations see incoming threats early and protect land, air and water."),
    ("What are T.Core, T.Sense, T.Sync and T.Pulse?",
     "They are our four systems. T.Core is an omnichannel software spine that links all our products and services. T.Sense is a set of modular sensing units that detect incoming threats before they hit perimeter bounds. T.Sync is a closed-channel sync for analysis, communications and recon planning. T.Pulse is a suite of services for recon actions."),
    ("How does counter-UAV protection work?",
     "We detect, track and respond to hostile drones. Sensing, compute and response work as one chain, so the time between first detection and action stays short."),
    ("Can the systems protect borders and coastlines?",
     "Yes. Modular sensing units provide persistent awareness along a border line, and the same stack extends over water to coastal and maritime approaches."),
    ("How do I request a briefing?",
     "Open the contact page, choose a topic and write a short message. It goes straight to our team, and a specialist replies to the address you provide."),
]


def faq_schema():
    return {"@type": "FAQPage", "@id": SITE + "/#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}


ALT = {
    "T.Core": "Racks of processing hardware with glowing status lights",
    "T.Sense": "Sensor array on a mast, seen from below",
    "T.Sync": "Communication towers silhouetted at dusk",
    "T.Pulse": "Cinema lens on a camera rig at golden hour",
}

ORG = {
    "@type": "Organization", "@id": SITE + "/#org", "name": "Traversion Dynamics", "alternateName": "Trav DNMX",
    "url": SITE + "/", "logo": SITE + "/images/logo-512.png",
    "description": "Deep-tech AI startup building modular border defense and counter-UAV systems.",
    "slogan": "Everyone has drones, we bring them down.",
    "knowsAbout": ["Border defense", "Counter-UAV", "Coastal and maritime security", "Reconnaissance planning", "Artificial intelligence"],
    "image": SITE + "/images/og-image.png",
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Traversion Dynamics",
           "alternateName": "Trav DNMX", "inLanguage": "en", "publisher": {"@id": SITE + "/#org"}}


def jsonld(graph):
    return ('<script type="application/ld+json">' +
            json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"), ensure_ascii=False) +
            "</script>")


def breadcrumb(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}


def head(title, desc, path, graph, robots="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1", js=()):
    preload = '<link rel="preload" href="images/trav-macro.jpg" as="image" fetchpriority="high">' if path == "/" else ""
    scripts = "".join('<script src="js/%s" defer></script>\n' % s for s in js)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<link rel="alternate" hreflang="en" href="{SITE}{path}">
<link rel="alternate" hreflang="x-default" href="{SITE}{path}">
<meta name="robots" content="{robots}">
<meta name="keywords" content="border defense, counter-UAV, drone defense, perimeter security, maritime security, recon planning, AI defense technology">
<meta name="application-name" content="Traversion Dynamics">
<meta name="format-detection" content="telephone=no">
{preload}
<meta name="theme-color" content="#07080C">
<meta name="color-scheme" content="dark">
<meta name="author" content="Traversion Dynamics">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml" sizes="any">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Traversion Dynamics">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/images/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Traversion Dynamics. Everyone has drones, we bring them down.">
<meta property="og:image:type" content="image/png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/images/og-image.png">
<meta name="twitter:image:alt" content="Traversion Dynamics. Everyone has drones, we bring them down.">
<link rel="preload" href="fonts/adventor-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/jakarta-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
{jsonld(graph)}
<script src="js/boot.js"></script>
{scripts}</head>
'''


def header(active):
    def a(href, text, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<li><a href="{href}"{cur}>{text}</a></li>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="nav" id="nav">
  <div class="wrap nav__bar">
    <a class="nav__brand" href="index.html" aria-label="Traversion Dynamics, home">
      <img src="images/logo-mark-light.svg" alt="" width="26" height="27">
      <span>Traversion</span>
    </a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="navPanel">
      <span class="nav__toggle-label">Menu</span><span class="nav__bars" aria-hidden="true"></span>
    </button>
    <div class="nav__panel" id="navPanel">
      <nav aria-label="Primary">
        <ul class="nav__links">
          {a("index.html", "Home", "home")}
          {a("index.html#systems", "Systems", "systems")}
          {a("missions.html", "Missions", "missions")}
        </ul>
      </nav>
      <a class="btn btn--sm" href="contact.html?topic=briefing">Request a briefing {ARROW}</a>
    </div>
  </div>
</header>
'''


def footer():
    systems = "".join(f'<li><a href="index.html#systems">{n}</a></li>' for _, n, _, _ in SYSTEMS)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__brand">
        <a class="footer__logo" href="index.html" aria-label="Traversion Dynamics, home">
          <img src="images/logo-mark-light.svg" alt="" width="44" height="46">
          <span>Traversion Dynamics</span>
        </a>
        <p class="footer__about">Modular, AI-driven border defense and counter-UAV systems that protect land, air and water.</p>
        <a class="btn btn--sm" href="contact.html?topic=briefing">Request a briefing {ARROW}</a>
      </div>
      <nav class="footer__col" aria-label="Systems">
        <p class="footer__h">Systems</p>
        <ul>{systems}</ul>
      </nav>
      <nav class="footer__col" aria-label="Company">
        <p class="footer__h">Company</p>
        <ul>
          <li><a href="missions.html">Missions</a></li>
          <li><a href="contact.html?topic=careers">Careers</a></li>
          <li><a href="contact.html?topic=press">Press</a></li>
        </ul>
      </nav>
      <nav class="footer__col" aria-label="Contact">
        <p class="footer__h">Contact</p>
        <ul>
          <li><a href="contact.html?topic=briefing">Request a briefing</a></li>
          <li><a href="contact.html?topic=partnership">Partnerships</a></li>
          <li><a href="contact.html?topic=security">Security</a></li>
        </ul>
      </nav>
    </div>
  </div>
  <div class="footer__word" aria-hidden="true">Traversion</div>
  <div class="wrap">
    <div class="footer__bottom">
      <p class="footer__legal">&copy; <span data-year>2026</span> Traversion Dynamics. All rights reserved.</p>
      <div class="footer__end">
        <a href="privacy.html">Privacy</a>
        <img class="footer__tile" src="images/logo.svg" alt="Traversion Dynamics" width="30" height="30">
      </div>
    </div>
  </div>
</footer>
'''


def cta():
    return f'''<section class="cta section" aria-labelledby="cta-title">
  <div class="wrap cta__inner">
    <div data-reveal>
      <p class="eyebrow">Next step</p>
      <h2 class="h2" id="cta-title">Put a mission on the map.</h2>
    </div>
    <a class="btn" href="contact.html?topic=briefing" data-reveal>Request a briefing {ARROW}</a>
  </div>
</section>
'''


def page(name, head_html, active, main_html, js_after=""):
    body = f'<body class="page-{name}">\n{header(active)}\n<main id="main">\n{main_html}</main>\n{footer()}\n</body>\n</html>\n'
    return head_html + body


def write(fname, html):
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname, len(html), "bytes")


# ------------------------------------------------------------------ home
cards = ""
for i, (tag, name, img, text) in enumerate(SYSTEMS):
    cls = "card" + ("" if i == 0 else "")
    reveal = "data-reveal" if i == 0 else "data-reveal"
    # stagger via a wrapper-free approach: delay classes live on the same element
    dcls = f' d{i}' if i else ''
    cards += f'''      <article class="card{dcls}" data-reveal>
        <div class="card__media"><img src="images/{img}" alt="{ALT[name]}" width="800" height="1000" loading="lazy" decoding="async"></div>
        <div class="card__body">
          <p class="card__id">{tag}</p>
          <h3 class="card__title">{name}</h3>
          <p class="card__text">{text}</p>
          <a class="card__link" href="contact.html?topic=briefing">Request a briefing {ARROW}</a>
        </div>
      </article>
'''

DOMAINS = [
    ("01", "Land", "Persistent awareness along the line, from perimeter sensing to one shared picture.", "missions.html#land"),
    ("02", "Air", "Detect, track and respond to hostile drones with one chain from sensing to action.", "missions.html#air"),
    ("03", "Water", "Extend the perimeter over coast and littoral approaches with the same modular stack.", "missions.html#water"),
]
drows = ""
for i, (no, name, text, href) in enumerate(DOMAINS):
    dcls = f" d{i}" if i else ""
    drows += f'''      <a class="drow{dcls}" href="{href}" data-reveal aria-label="{name}: view mission">
        <span class="drow__no">{no}</span>
        <span class="drow__name">{name}</span>
        <span class="drow__text">{text}</span>
        {ARROW}
      </a>
'''

faq_html = "".join(f'''      <details class="qa" data-reveal>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>
''' for q, a in FAQ)

home_main = f'''<section class="hero" aria-labelledby="hero-title">
  <div class="hero__media" aria-hidden="true">
    <img src="images/trav-macro.jpg" alt="" width="1920" height="1080" fetchpriority="high" decoding="async">
  </div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__grid" aria-hidden="true"></div>
  <div class="wrap">
    <p class="eyebrow hero__eyebrow">Modular Modern Warfare</p>
    <h1 class="hero__title" id="hero-title">
      <span class="line"><span>Everyone has drones,</span></span>
      <span class="line"><span>We bring them down.</span></span>
    </h1>
    <p class="hero__sub">Modular, AI-driven border defense and counter-UAV systems for nations that build at the edge of what hardware allows.</p>
    <div class="hero__cta">
      <a class="btn" href="contact.html?topic=briefing">Request a briefing {ARROW}</a>
      <a class="btn btn--ghost" href="#systems">Explore systems</a>
    </div>
  </div>
  <div class="wrap hero__foot" aria-hidden="true">
    <span>Land / Air / Water</span>
    <span class="hero__scroll">Scroll</span>
  </div>
</section>

<section class="statement section" aria-labelledby="statement-title">
  <div class="wrap statement__grid">
    <p class="eyebrow" data-reveal>Mission</p>
    <div>
      <h2 class="statement__text" id="statement-title" data-reveal>We build modular, AI-driven systems that protect borders and critical infrastructure, so nations can see incoming threats before they reach the perimeter and act with precision.</h2>
      <a class="link" href="missions.html" data-reveal>Our missions {ARROW}</a>
    </div>
  </div>
</section>

<section class="section" id="systems" aria-labelledby="systems-title">
  <div class="wrap">
    <div class="shead">
      <div class="shead__title" data-reveal>
        <p class="eyebrow">Systems</p>
        <h2 class="h2" id="systems-title">Four systems.<br>One spine.</h2>
      </div>
      <p class="shead__text lede" data-reveal>Each system works on its own and gets stronger when connected. T.Core links them all.</p>
    </div>
    <div class="cards">
{cards}    </div>
  </div>
</section>

<section class="domains section" aria-labelledby="domains-title">
  <div class="wrap">
    <div class="shead">
      <div class="shead__title" data-reveal>
        <p class="eyebrow">Domains</p>
        <h2 class="h2" id="domains-title">Land. Air. Water.</h2>
      </div>
      <p class="shead__text lede" data-reveal>One modular stack, built to defend every edge a nation has to hold.</p>
    </div>
    <div class="drows">
{drows}    </div>
  </div>
</section>

<section class="section faq" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="shead">
      <div class="shead__title" data-reveal>
        <p class="eyebrow">Questions</p>
        <h2 class="h2" id="faq-title">Good<br>questions.</h2>
      </div>
      <p class="shead__text lede" data-reveal>Straight answers about what we build and how to get started.</p>
    </div>
    <div class="qas">
{faq_html}    </div>
  </div>
</section>

{cta()}'''

home_graph = [dict(ORG, makesOffer=[
    {"@type": "Offer", "itemOffered": {"@type": "Product", "name": n, "description": t}}
    for _, n, _, t in SYSTEMS]), WEBSITE,
    {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": "Traversion Dynamics | AI Border Defense & Counter-UAV Systems",
     "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"}, "inLanguage": "en",
     "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/images/og-image.png"}},
    faq_schema()]
write("index.html", page(
    "home",
    head("Traversion Dynamics | AI Border Defense &amp; Counter-UAV Systems",
         "Traversion Dynamics builds modular, AI-driven border defense and counter-UAV systems: T.Core, T.Sense, T.Sync and T.Pulse for land, air and water.",
         "/", home_graph, js=("site.js",)),
    "home", home_main))

# ------------------------------------------------------------------ missions
MISSIONS = [
    ("land", "M.01", "Land", "Border perimeter defense",
     "Persistent awareness along the line. Modular sensing units detect incoming threats before they hit perimeter bounds, while the software spine links every unit into one picture.",
     ["T.Sense", "T.Core"]),
    ("air", "M.02", "Air", "Counter-UAV protection",
     "Detect, track and respond to hostile drones. Sensing, compute and response work as one chain, so the time between first detection and action stays short.",
     ["T.Sense", "T.Core", "T.Pulse"]),
    ("water", "M.03", "Water", "Coastal and maritime security",
     "Extend the perimeter over water. The same modular stack carries from shoreline to littoral approaches, sharing detections across units over a closed channel.",
     ["T.Sense", "T.Sync"]),
    ("recon", "M.04", "Recon", "Analysis and recon planning",
     "A closed-channel sync for analysis, communications and recon planning, backed by a suite of services for recon actions.",
     ["T.Sync", "T.Pulse"]),
]
mrows = ""
for i, (mid, no, dom, title, text, chips) in enumerate(MISSIONS):
    chip_html = "".join(f'<li class="chip">{c}</li>' for c in chips)
    mrows += f'''      <article class="mrow" id="{mid}" data-reveal>
        <div><span class="mrow__no">{no}</span><p class="mrow__domain">{dom}</p></div>
        <div><h3 class="mrow__title">{title}</h3><p class="mrow__text">{text}</p></div>
        <ul class="chips" aria-label="Systems used">{chip_html}</ul>
      </article>
'''

missions_main = f'''<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow">Missions</p>
    <h1 class="page-hero__title" id="page-title"><span class="line"><span>Built for</span></span><span class="line"><span>the edge.</span></span></h1>
    <p class="lede">Four missions, one spine. Everything we build exists to detect threats early, share one picture, and respond with precision across land, air and water.</p>
  </div>
</section>

<section class="mstatement section" aria-labelledby="statement-title">
  <div class="wrap mstatement__grid">
    <div class="mstatement__title" data-reveal>
      <p class="eyebrow">Mission statement</p>
      <h2 class="h2" id="statement-title">Data &amp; defense.</h2>
    </div>
    <p class="mstatement__text" data-reveal class="d1">Traversion Dynamics builds modular, AI-driven systems that protect borders and critical infrastructure. Our mission is to give nations an edge at the edge: see incoming threats before they reach the perimeter, link every unit into a single operating picture, and act with precision.</p>
  </div>
</section>

<section class="section" aria-labelledby="missions-title">
  <div class="wrap">
    <div class="mhead" data-reveal>
      <h2 class="h2" id="missions-title">Four missions</h2>
      <span class="mhead__tag">Land / Air / Water / Recon</span>
    </div>
    <div class="mlist">
{mrows}    </div>
  </div>
</section>

{cta()}'''
missions_main = missions_main.replace('data-reveal class="d1"', 'data-reveal')  # single class attr
write("missions.html", page(
    "missions",
    head("Missions | Land, Air &amp; Water Defense | Traversion Dynamics",
         "Traversion Dynamics missions: border perimeter defense, counter-UAV protection, coastal and maritime security, and recon planning across land, air and water.",
         "/missions.html", [ORG, WEBSITE, breadcrumb("Missions", "/missions.html"),
                            {"@type": "WebPage", "name": "Missions", "url": SITE + "/missions.html", "isPartOf": {"@id": SITE + "/#website"}}] +
                           [{"@type": "Service", "name": t, "serviceType": t, "description": x, "provider": {"@id": SITE + "/#org"}}
                            for _, _, _, t, x, _ in MISSIONS],
         js=("site.js",)),
    "missions", missions_main))

# ------------------------------------------------------------------ contact
TOPICS = [("briefing", "Requesting a briefing"), ("border", "Border perimeter defense"),
          ("counter-uav", "Counter-UAV protection"), ("maritime", "Coastal and maritime security"),
          ("recon", "Analysis and recon planning"), ("partnership", "A partnership"),
          ("careers", "Careers"), ("press", "Press"), ("security", "A security disclosure"),
          ("other", "Something else")]
opts = "".join(f'<option value="{v}"{" selected" if v == "briefing" else ""}>{t}</option>' for v, t in TOPICS)

contact_main = f'''<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1 class="page-hero__title" id="page-title"><span class="line"><span>Request a</span></span><span class="line"><span>briefing.</span></span></h1>
    <p class="lede">Tell us about your perimeter, airspace or coastline. We will come back to you to scope the right conversation, whether that is a briefing, a partnership or a security question.</p>
  </div>
</section>

<section class="section" aria-label="Contact form">
  <div class="wrap contact__grid">
    <aside class="contact__info" data-reveal>
      <p class="eyebrow">What happens next</p>
      <h2 class="h2">Three simple steps.</h2>
      <ol class="steps">
        <li><strong>We read your request</strong>Your message goes straight to the team that handles it.</li>
        <li><strong>We get in touch</strong>A specialist replies to the email address you provide.</li>
        <li><strong>We scope the briefing</strong>Together we agree what to cover and who should be in the room.</li>
      </ol>
      <p class="note">Please do not include classified or sensitive operational details in this form. We will agree on a secure channel for that first.</p>
    </aside>

    <div data-reveal class="d1">
      <form class="form" id="contactForm" novalidate data-endpoint="/api/contact" aria-label="Contact form">
        <div class="field">
          <label class="field__label" for="f-name">Name</label>
          <input class="input" id="f-name" name="name" type="text" autocomplete="name" maxlength="100" required aria-describedby="err-name">
          <p class="field__error" id="err-name" aria-live="polite"></p>
        </div>
        <div class="field">
          <label class="field__label" for="f-email">Work email</label>
          <input class="input" id="f-email" name="email" type="email" autocomplete="email" maxlength="254" required aria-describedby="err-email">
          <p class="field__error" id="err-email" aria-live="polite"></p>
        </div>
        <div class="field">
          <label class="field__label" for="f-org">Organization <small>(optional)</small></label>
          <input class="input" id="f-org" name="organization" type="text" autocomplete="organization" maxlength="120" aria-describedby="err-organization">
          <p class="field__error" id="err-organization" aria-live="polite"></p>
        </div>
        <div class="field">
          <label class="field__label" for="f-role">Role <small>(optional)</small></label>
          <input class="input" id="f-role" name="role" type="text" autocomplete="organization-title" maxlength="120" aria-describedby="err-role">
          <p class="field__error" id="err-role" aria-live="polite"></p>
        </div>
        <div class="field field--full">
          <label class="field__label" for="f-topic">I am contacting you about</label>
          <select class="input" id="f-topic" name="topic" required aria-describedby="err-topic">{opts}</select>
          <p class="field__error" id="err-topic" aria-live="polite"></p>
        </div>
        <div class="field field--full">
          <label class="field__label" for="f-message">Message</label>
          <textarea class="input" id="f-message" name="message" maxlength="1500" required aria-describedby="err-message"></textarea>
          <p class="field__error" id="err-message" aria-live="polite"></p>
        </div>

        <div class="hp" aria-hidden="true">
          <label for="f-website">Leave this field empty</label>
          <input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off">
        </div>

        <div class="field field--full">
          <label class="check">
            <input type="checkbox" id="f-consent" name="consent" aria-describedby="err-consent" required>
            <span class="check__box" aria-hidden="true"><svg viewBox="0 0 14 14"><path d="M2 7.5l3.2 3.2L12 3.8"/></svg></span>
            <span>I agree that Traversion Dynamics may use these details to reply to my request. See the <a href="privacy.html">privacy notice</a>.</span>
          </label>
          <p class="field__error" id="err-consent" aria-live="polite"></p>
        </div>

        <div class="field field--full form__actions">
          <button class="btn" id="submitBtn" type="submit"><span class="btn__label">Send message</span> {ARROW}</button>
          <p class="form__hint">We reply to the email address you provide.</p>
        </div>
        <p class="status" id="formStatus" role="alert"></p>
      </form>

      <div class="sent" id="sent" tabindex="-1" hidden>
        <svg class="sent__icon" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="25.5"/><path d="M17 29l8 8 14-17"/></svg>
        <h2>Message received.</h2>
        <p>Thank you. A specialist will reply to the email address you provided.</p>
        <button class="btn btn--ghost" id="sentAgain" type="button">Send another message</button>
      </div>
    </div>
  </div>
</section>
'''
write("contact.html", page(
    "contact",
    head("Contact | Request a Briefing | Traversion Dynamics",
         "Contact Traversion Dynamics to request a briefing on border defense, counter-UAV, coastal security and recon planning systems, or to discuss partnerships.",
         "/contact.html", [ORG, WEBSITE, breadcrumb("Contact", "/contact.html"),
                           {"@type": "ContactPage", "name": "Contact", "url": SITE + "/contact.html", "isPartOf": {"@id": SITE + "/#website"}}],
         js=("site.js", "contact.js")),
    "contact", contact_main))

# ------------------------------------------------------------------ privacy
privacy_main = '''<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <p class="eyebrow">Legal</p>
    <h1 class="page-hero__title page-hero__title--sm" id="page-title"><span class="line"><span>Privacy notice</span></span></h1>
    <p class="lede">What this website collects, why, and what happens to it. Last updated October 2026.</p>
  </div>
</section>

<section class="section" aria-label="Privacy notice">
  <div class="wrap">
    <div class="prose">
      <h2>Who we are</h2>
      <p>This website is operated by Traversion Dynamics. If you have a question about this notice, get in touch through the <a href="contact.html">contact page</a>.</p>

      <h2>What we collect</h2>
      <p>The only way this site collects personal information is the contact form. If you use it, we receive:</p>
      <ul>
        <li>your name and email address;</li>
        <li>your organization and role, if you choose to give them;</li>
        <li>the topic you selected and the message you write.</li>
      </ul>
      <p>Please do not include classified or sensitive operational details in the form.</p>

      <h2>How we use it</h2>
      <p>We use these details only to read and reply to your request. We do not use them for advertising and we do not sell them.</p>

      <h2>Who receives it</h2>
      <p>Your message is passed to our team by email through a mail service we operate or contract. The website does not keep a copy in a database.</p>

      <h2>Cookies and tracking</h2>
      <p>This site does not set cookies and does not use analytics or advertising trackers. Fonts and images are served from our own domain, so your browser does not contact third-party servers to display the pages.</p>

      <h2>How long we keep it</h2>
      <p>We keep an enquiry for as long as it is needed to respond to you and to keep a reasonable record of the conversation.</p>

      <h2>Your choices</h2>
      <p>You can ask us to correct or delete the details you sent us by getting in touch through the <a href="contact.html">contact page</a>.</p>

      <h2>Changes</h2>
      <p>If we change how this site handles personal information, we will update this page and its date.</p>
    </div>
  </div>
</section>
'''
write("privacy.html", page(
    "privacy",
    head("Privacy Notice | Traversion Dynamics",
         "How the Traversion Dynamics website handles the personal information you send through the contact page.",
         "/privacy.html", [ORG, WEBSITE, breadcrumb("Privacy", "/privacy.html")], js=("site.js",)),
    "none", privacy_main))

# ------------------------------------------------------------------ 404 (absolute paths: it is served on any URL)
nf = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | Traversion Dynamics</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#07080C">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{SITE}/favicon.ico" sizes="48x48">
<link rel="icon" href="{SITE}/images/favicon.svg" type="image/svg+xml" sizes="any">
<link rel="stylesheet" href="{SITE}/css/site.css">
</head>
<body>
<main class="nf" id="main">
  <div class="wrap">
    <p class="nf__code">Error 404</p>
    <h1>Off the map.</h1>
    <p>The page you were looking for does not exist or has moved.</p>
    <a class="btn" href="{SITE}/">Back to home {ARROW}</a>
  </div>
</main>
</body>
</html>
'''
write("404.html", nf)
