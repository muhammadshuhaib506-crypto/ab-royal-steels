#!/usr/bin/env python3
"""Builds the AB Royal Steels static site into dist/. Run: python3 src/build.py"""
import os, sys, html, re
sys.path.insert(0, os.path.dirname(__file__))
from data import CATEGORIES, INDUSTRIES, PROCESS, PROJECT_CATS, PROJECTS

OUT = os.path.join(os.path.dirname(__file__), '..')
E = html.escape

def ph(text):
    return f'<em class="ph">[{E(text)}]</em>'

# ---------- Icons (24px line icons, stroke = currentColor) ----------
ICONS = {
    'arrow': '<path d="M4 12h15M13 6l6 6-6 6"/>',
    'left': '<path d="M15 5l-7 7 7 7"/>', 'right': '<path d="M9 5l7 7-7 7"/>', 'down': '<path d="M5 9l7 7 7-7"/>', 'up': '<path d="M12 19V5M6 11l6-6 6 6"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    'layers': '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    'ruler': '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    'check': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16.5 9"/>',
    'search': '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>',
    'box': '<path d="M3 7.5L12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/>',
    'truck': '<path d="M2 6h12v10H2zM14 9h4l3 3.5V16h-7"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'shield': '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    'stack': '<path d="M3 6h18v3H3zM3 11h18v3H3zM3 16h18v3H3z"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'handshake': '<path d="M2 11l4-4 4 2 3-2 4 1 5 4"/><path d="M6 13l3 3c.8.8 2 .8 2.8 0l3.7-3.7M9 9l-2 2"/>',
    'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    'flag': '<path d="M5 21V4M5 4h12l-2 4 2 4H5"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.5-3.6 3.2-5.5 6.5-5.5s6 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 010 6.8M18 14.8c2 .7 3.3 2.4 3.5 5.2"/>',
    'phone': '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 006 6L16 13l5 2v4a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z"/>',
    'mail': '<path d="M3 5h18v14H3z"/><path d="M3 6l9 7 9-7"/>',
    'pin': '<path d="M12 21s7-6.2 7-11.5A7 7 0 005 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'factory': '<path d="M3 21V10l6 3.5V10l6 3.5V5h6v16z"/><path d="M7 17h2M12 17h2M17 17h2"/>',
    'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9L7 7M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    'doc': '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>',
    'award': '<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 22l5-3 5 3-1.5-8"/>',
    'crane': '<path d="M5 21V4h2v17M4 21h6M7 5h14M7 5l4-2M17 5v6"/><path d="M15.5 11h3v2h-3z"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
}
def icon(name, cls='ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
ARROW = icon('arrow', '')
CHEV = '<svg class="chev" viewBox="0 0 100 120" aria-hidden="true"><polygon points="0,0 44,0 100,60 44,120 0,120 56,60" fill="#E31824"/><polygon points="0,0 44,0 100,60 44,120 0,120 56,60" fill="none" stroke="#fff" stroke-width="6" transform="translate(-34 0)"/></svg>'

def art(kind, key, cls='', alt='', extra=''):
    return f'<div class="art {cls}" data-art="{kind}" data-key="{key}" data-alt="{E(alt)}" role="img" aria-label="{E(alt)}"{extra}></div>'

ALL_PRODUCTS = []
for c in CATEGORIES:
    for p in c['products']:
        ALL_PRODUCTS.append(dict(slug=p[0], name=p[1], art=p[2], desc=p[3], apps=p[4], cat=c))

# ---------- Layout ----------
NAV = [('index.html', 'Home'), ('about.html', 'About Us'), ('products.html', 'Products'), ('industries.html', 'Industries'),
       ('process.html', 'Our Process'), ('projects.html', 'Projects')]
COMPANY = [('infrastructure.html', 'Infrastructure'), ('quality.html', 'Quality & Standards'), ('leadership.html', 'Founder & Leadership')]

def header(r, active):
    def cur(h): return ' aria-current="page"' if h == active else ''
    mega_cols = ''.join(
        f'<div class="col"><h4>{c["letter"]}. {E(c["name"])}</h4>' +
        ''.join(f'<a href="{r}products/{p[0]}.html">{E(p[1])}</a>' for p in c['products']) + '</div>' for c in CATEGORIES)
    items = []
    for h, label in NAV:
        if h == 'products.html':
            items.append(f'<li class="has-menu"><a class="nav-link" href="{r}{h}"{cur(h)} aria-haspopup="true">{label} {icon("down","")}</a>'
                         f'<div class="menu mega">{mega_cols}<div class="all"><a href="{r}products.html">View the full product catalogue →</a></div></div></li>')
        else:
            items.append(f'<li><a class="nav-link" href="{r}{h}"{cur(h)}>{label}</a></li>')
    comp_active = any(h == active for h, _ in COMPANY)
    items.append(f'<li class="has-menu"><button class="nav-link" type="button" aria-haspopup="true"{" aria-current=\"page\"" if comp_active else ""}>Company {icon("down","")}</button><ul class="menu">' +
                 ''.join(f'<li><a href="{r}{h}">{l}</a></li>' for h, l in COMPANY) + '</ul></li>')
    items.append(f'<li><a class="nav-link" href="{r}contact.html"{cur("contact.html")}>Contact</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span class="hide-sm">Steel sheets · Pipes · Structural sections · Iron &amp; metal products</span>
<ul><li>{icon("phone","") if False else ""}<a href="{r}contact.html">Phone: {ph("Add phone number")}</a></li><li class="hide-sm"><a href="{r}contact.html">Email: {ph("Add email")}</a></li></ul></div></div>
<header class="site-header"><div class="header-inner">
<a class="brand" href="{r}index.html" aria-label="AB Royal Steels home"><img src="{r}assets/img/logo-white.svg" alt="AB Royal Steels" width="276" height="100"></a>
<button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
<nav class="nav" id="site-nav" aria-label="Main"><ul>{"".join(items)}</ul><a class="btn btn-red btn-sm" href="{r}quote.html">Request a Quote {ARROW}</a></nav>
</div></header>'''

def footer(r):
    cats = ''.join(f'<li><a href="{r}products.html#{c["id"]}">{E(c["name"])}</a></li>' for c in CATEGORIES)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-top">
<div class="foot-brand"><img src="{r}assets/img/logo-white.svg" alt="AB Royal Steels" width="276" height="100" loading="lazy">
<p>Supplier of steel sheets, steel pipes, structural sections and iron &amp; metal products for construction, fabrication and industry.</p>
<div class="btn-row" style="margin-top:26px"><a class="btn btn-red btn-sm" href="{r}quote.html">Request a Quote {ARROW}</a></div></div>
<div><h4>Company</h4><ul><li><a href="{r}about.html">About Us</a></li><li><a href="{r}leadership.html">Founder &amp; Leadership</a></li><li><a href="{r}infrastructure.html">Infrastructure</a></li><li><a href="{r}quality.html">Quality &amp; Standards</a></li><li><a href="{r}projects.html">Projects</a></li></ul></div>
<div><h4>Products</h4><ul>{cats}<li><a href="{r}products.html">Full catalogue</a></li></ul></div>
<div><h4>Work with us</h4><ul><li><a href="{r}industries.html">Industries We Serve</a></li><li><a href="{r}process.html">Our Process</a></li><li><a href="{r}quote.html">Request a Quote</a></li><li><a href="{r}contact.html">Contact Us</a></li></ul></div>
<div><h4>Contact</h4><ul><li>{ph("Street address, city, country")}</li><li>Phone: {ph("Add phone number")}</li><li>Email: {ph("Add email")}</li><li>Hours: {ph("e.g. Mon–Sat, 9:00–18:00")}</li></ul></div>
</div>
<div class="foot-bottom"><span>© <span id="year">2026</span> AB Royal Steels. All rights reserved.</span><span>Strong Materials. Stronger Foundations.</span></div>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{icon("up","")}</button>'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Barlow:wght@400;500;600&display=swap">'

def page(filename, title, desc, body, active=None, depth=0, artifact=False):
    r = '../' * depth
    head = (f'<title>{E(title)}</title>\n<meta name="description" content="{E(desc)}">\n'
            f'<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="theme-color" content="#E31824">\n<link rel="icon" href="{r}assets/img/mark-red.svg" type="image/svg+xml">\n'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">\n'
            f'{FONTS}\n<link rel="stylesheet" href="{r}assets/css/site.css">')
    content = (f'{header(r, active or filename)}\n<main id="main">\n{body}\n</main>\n{footer(r)}\n'
               f'<script>window.ABRS_ROOT="{r}";</script><script src="{r}assets/js/photos.js"></script><script src="{r}assets/js/art.js"></script><script src="{r}assets/js/site.js"></script>')
    if artifact:
        doc = f'{head}\n{content}\n'
    else:
        doc = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
               f'{head}\n</head>\n<body>\n{content}\n</body>\n</html>\n')
    path = os.path.join(OUT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(doc)

def page_hero(title, lead, crumbs, kind, key, r=''):
    cr = ''.join(f'<li><a href="{r}{h}">{E(l)}</a></li>' if h else f'<li aria-current="page">{E(l)}</li>' for h, l in crumbs)
    return f'''<section class="page-hero">{art(kind, key, alt=title)}{CHEV}<div class="wrap">
<ol class="crumbs">{cr}</ol><h1 class="h-lg">{title}</h1><p class="lead">{lead}</p></div></section>'''

def cta_band(r='', title='Need steel for your next project?', text='Tell us what you need: product, size, quantity and delivery location. We will come back with a clear quotation.'):
    return f'''<section class="cta-band"><div class="wrap"><div><h2 class="h-lg">{title}</h2><p>{text}</p></div>
<div class="btn-row"><a class="btn btn-white" href="{r}quote.html">Request a Quote {ARROW}</a><a class="btn btn-ghost" href="{r}contact.html">Contact Us</a></div></div></section>'''

def enquiry_form(product='', r='', heading='Send an enquiry', sub='Share your requirement and our team will respond with availability and pricing.'):
    opts = ''.join(f'<option{" selected" if p["name"] == product else ""}>{E(p["name"])}</option>' for p in ALL_PRODUCTS)
    return f'''<div class="form-card"><h2 class="h-md">{heading}</h2><p class="muted">{sub}</p>
<form class="form" data-enquiry>
<div class="field"><label for="f-name">Full name <span class="req">*</span></label><input id="f-name" name="name" autocomplete="name" required><span class="err">Please enter your name.</span></div>
<div class="field"><label for="f-company">Company</label><input id="f-company" name="company" autocomplete="organization"></div>
<div class="field"><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="err">Please enter a valid email.</span></div>
<div class="field"><label for="f-phone">Phone <span class="req">*</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required><span class="err">Please enter a phone number.</span></div>
<div class="field"><label for="f-product">Product</label><select id="f-product" name="product"><option value="">Select a product</option>{opts}</select></div>
<div class="field"><label for="f-qty">Quantity</label><input id="f-qty" name="quantity" placeholder="e.g. 5 tonnes, 200 pieces"></div>
<div class="field full"><label for="f-msg">Requirement details <span class="req">*</span></label><textarea id="f-msg" name="message" placeholder="Sizes, thickness, grade, delivery location and timeline" required></textarea><span class="err">Please describe what you need.</span></div>
<div class="full"><button class="btn btn-red" type="submit">Send Enquiry {ARROW}</button></div>
<div class="form-status" role="status" aria-live="polite"></div>
</form></div>'''

# ---------- HOME ----------
def home(artifact=False):
    r = ''
    slides = [
        ('truck', 'warehouse', 'hero-truck', 'AB Royal Steels', 'STRONG MATERIALS.<em>STRONGER FOUNDATIONS.</em>',
         'Your Trusted Partner for Premium Steel Products, Industrial Materials and Reliable Steel Supply Solutions.',
         [('products.html', 'Explore Our Products', 'btn-red'), ('quote.html', 'Request a Quote', 'btn-ghost')], 'Steel Supply'),
        ('', 'coils', 'hero-sheets', 'Steel Sheets &amp; Plates', 'SHEETS FOR EVERY<em>SURFACE AND SPAN.</em>',
         'Mild steel, GI, colour coated, stainless, hot rolled and cold rolled sheets for construction, roofing and fabrication.',
         [('products.html#steel-sheets', 'View Steel Sheets', 'btn-red'), ('quote.html', 'Request a Quote', 'btn-ghost')], 'Sheets &amp; Plates'),
        ('', 'pipes', 'hero-pipes', 'Pipes, Tubes &amp; Sections', 'BUILT TO CARRY<em>THE LOAD.</em>',
         'MS and GI pipes, hollow sections, beams, channels and angles for structures that have to last.',
         [('products.html#steel-pipes', 'View Steel Pipes', 'btn-red'), ('quote.html', 'Request a Quote', 'btn-ghost')], 'Pipes &amp; Sections'),
    ]
    sl = ''
    for i, (cls, kind, key, eb, h, lead, btns, label) in enumerate(slides):
        truck = f'<img class="hero-truck" src="assets/img/truck.png" alt="AB Royal Steels branded delivery truck" width="873" height="486">' if cls == 'truck' else ''
        b = ''.join(f'<a class="btn {c}" href="{r}{u}">{t} {ARROW}</a>' for u, t, c in btns)
        hx = 'h1' if i == 0 else 'h2'
        sl += (f'<div class="slide {cls}{" is-active" if i == 0 else ""}" aria-roledescription="slide" aria-label="{i+1} of 3" aria-hidden="{"false" if i == 0 else "true"}">{art(kind, key, alt="")}{truck}'
               f'<div class="slide-body"><div class="wrap"><div class="inner slide-anim"><span class="eyebrow">{eb}</span><{hx} class="h-xl">{h}</{hx}><p class="lead">{lead}</p><div class="btn-row">{b}</div></div></div></div></div>')
    dots = ''.join(f'<button class="dot{" is-active" if i == 0 else ""}" type="button" aria-label="Show slide {i+1}"><i></i><span>0{i+1} · {s[7]}</span></button>' for i, s in enumerate(slides))
    hero = f'''<section class="hero" aria-roledescription="carousel" aria-label="Highlights" tabindex="-1"><div class="slides">{sl}</div>
<div class="hero-controls"><div class="wrap"><div class="dots">{dots}</div><div style="display:flex"><span class="counter"><b>01</b> / 03</span><div class="arrows"><button class="arrow prev" type="button" aria-label="Previous slide">{icon("left","")}</button><button class="arrow next" type="button" aria-label="Next slide">{icon("right","")}</button></div></div></div></div></section>'''

    names = [p['name'] for p in ALL_PRODUCTS[:14]]
    marquee = '<div class="marquee" aria-hidden="true"><div class="marquee-track">' + ''.join(f'<span>{E(n)}</span>' for n in names * 2) + '</div></div>'

    intro = f'''<section class="section"><div class="wrap">
<div class="intro-band reveal"><div><span class="eyebrow">Who we are</span><h2 class="h-lg" style="margin-top:18px">A dependable source for steel and metal products.</h2></div>
<div class="stack"><p class="lead">AB Royal Steels sells and supplies steel sheets, steel pipes, structural sections and iron &amp; metal products to builders, fabricators, manufacturers and project teams.</p>
<p class="muted">We focus on getting the right material to the right place: correct specification, careful handling and delivery you can plan around.</p>
<a class="link-arrow" href="{r}about.html">More about us {ARROW}</a></div></div>
<div class="pillars reveal">
<div class="pillar">{icon("stack")}<h3>Complete range</h3><p>Sheets, pipes, sections and metal products from one supplier, so a single order covers the whole job.</p></div>
<div class="pillar">{icon("shield")}<h3>Checked material</h3><p>Every order is inspected against the agreed specification before it leaves for your site.</p></div>
<div class="pillar">{icon("truck")}<h3>Reliable delivery</h3><p>Bundled, labelled and dispatched on schedule, with transport coordinated to your location.</p></div>
</div></div></section>'''

    panels = ''.join(f'''<a class="cat-panel zoom" href="{r}products.html#{c["id"]}">{art(c["art"], c["key"], alt=c["name"])}<div class="body"><span class="idx">{c["letter"]} / {len(c["products"]):02d} products</span><h3>{E(c["name"])}</h3>
<ul>{"".join(f"<li>{E(p[1])}</li>" for p in c["products"][:5])}</ul><span class="link-arrow">Explore {ARROW}</span></div></a>''' for c in CATEGORIES)
    products = f'''<section class="section bg-grey"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Our products</span><h2 class="h-lg">Four product families. One supply partner.</h2></div>
<a class="btn btn-line" href="{r}products.html">Full catalogue {ARROW}</a></div></div><div class="cat-panels reveal">{panels}</div></section>'''

    why_items = [('shield', 'Specification first', 'We confirm grade, size and finish before quoting, so what arrives matches what you ordered.'),
                 ('layers', 'Wide product range', 'Sheets, pipes, sections, rods and accessories, combined into one order and one delivery.'),
                 ('handshake', 'Straight answers', 'Clear quotations with material, quantities and delivery terms spelled out.'),
                 ('clock', 'On-time dispatch', 'Orders are planned around your site schedule, with updates until delivery.'),
                 ('search', 'Inspected before dispatch', 'Material is checked for specification, dimensions and surface condition.'),
                 ('users', 'People who know steel', 'Help choosing the right product and size for the application.')]
    why = f'''<section class="section bg-navy"><div class="wrap grid-2 top">
<div class="stack-lg reveal"><div><span class="eyebrow">Why AB Royal Steels</span><h2 class="h-lg" style="margin-top:18px">Strength you can specify. Service you can count on.</h2></div>
<p class="lead">Steel is only as good as the supply behind it. We make the buying side simple, so your team can focus on building.</p>
<div class="frame">{art("warehouse-left", "why-warehouse", alt="Steel warehouse")}<span class="frame-tag">Stock · Inspect · Dispatch</span></div></div>
<ul class="why-list reveal">{"".join(f"<li>{icon(i)}<div><h3>{t}</h3><p>{d}</p></div></li>" for i, t, d in why_items)}</ul>
</div></section>'''

    ind = ''.join(f'''<a class="ind-card zoom" href="{r}industries.html#{s}">{art(a, "ind-" + s, alt=n)}<div class="body"><span class="bar"></span><h3>{E(n)}</h3><p>{E(d)}</p></div></a>''' for s, n, a, d, _ in INDUSTRIES)
    industries = f'''<section class="section"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Industries we serve</span><h2 class="h-lg">Steel for the sectors that build and make.</h2></div>
<a class="btn btn-line" href="{r}industries.html">All industries {ARROW}</a></div><div class="ind-grid wide reveal">{ind}</div></div></section>'''

    steps = ''.join(f'<li><span class="node">{icon(ic, "")}</span><span class="num">{i+1:02d}</span><h3>{E(t)}</h3></li>' for i, (t, ic, _, _) in enumerate(PROCESS))
    process = f'''<section class="section bg-char"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Our process</span><h2 class="h-lg">From first call to final delivery.</h2></div>
<a class="btn btn-ghost" href="{r}process.html">See how we work {ARROW}</a></div><ol class="proc-h reveal">{steps}</ol></div></section>'''

    fleet = f'''<section class="fleet"><div class="wrap"><div class="stack reveal"><span class="eyebrow">Logistics</span><h2 class="h-lg">From our yard to your site.</h2>
<p class="lead">Material leaves our yard bundled, strapped and labelled, loaded for safe transport and delivered to your location.</p>
<p class="muted">{ph("Add delivery coverage, e.g. cities or regions served, and fleet details")}</p>
<div class="btn-row"><a class="btn btn-navy" href="{r}infrastructure.html">Our infrastructure {ARROW}</a></div></div>
<div class="fleet-img reveal"><img src="{r}assets/img/truck.png" alt="AB Royal Steels branded truck in red, navy and white" width="873" height="486" loading="lazy"></div></div></section>'''

    projs = ''.join(f'''<article class="proj zoom">{art(a, f"home-proj-{i}", alt=c)}<div class="body"><span class="cat">{E(c)}</span><h3>{ph("Project name")}</h3><p>{ph("Short description of the project and scope of supply")}</p></div></article>''' for i, (c, a, _, _) in enumerate(PROJECTS[:3]))
    projects = f'''<section class="section bg-grey"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Projects</span><h2 class="h-lg">Where our steel goes to work.</h2></div>
<a class="btn btn-line" href="{r}projects.html">View projects {ARROW}</a></div><div class="gallery reveal">{projs}</div></div></section>'''

    body = hero + marquee + intro + products + why + industries + process + fleet + projects + cta_band(r)
    page('artifact-index.html' if artifact else 'index.html', 'AB Royal Steels', 'AB Royal Steels supplies steel sheets, steel pipes, structural sections and iron & metal products for construction, fabrication and industry.', body, 'index.html', artifact=artifact)

# ---------- ABOUT ----------
def about():
    values = [('shield', 'Integrity', 'We quote honestly, specify accurately and stand behind what we supply.'),
              ('award', 'Quality', 'We check material against the order before it leaves us, every time.'),
              ('handshake', 'Partnership', 'We build long-term relationships by being easy to work with and dependable.'),
              ('clock', 'Reliability', 'We plan dispatch around your schedule and keep you informed until delivery.'),
              ('users', 'Respect', 'For our customers, our team and the people who work on every site we supply.'),
              ('target', 'Responsibility', 'Safe handling, careful loading and accountability for every order.')]
    body = page_hero('About AB Royal Steels', 'A steel products supplier built on accurate specification, careful handling and dependable delivery.', [('index.html', 'Home'), (None, 'About Us')], 'warehouse', 'about-hero')
    body += f'''<section class="section"><div class="wrap grid-2">
<div class="stack reveal"><span class="eyebrow">Company overview</span><h2 class="h-lg">Supplying the materials that hold projects together.</h2>
<p class="lead">AB Royal Steels sells and supplies steel sheets, steel pipes, steel sections and structural products, and iron &amp; metal products.</p>
<p>We work with contractors, builders, fabricators, manufacturers and project teams who need the right material, in the right specification, delivered when they need it.</p>
<p class="muted">{ph("Add company background: year established, location, and how the business started")}</p></div>
<div class="frame reveal">{art("coils", "about-overview", alt="Steel coils in a warehouse")}<span class="frame-tag">Est. {ph("Year")}</span></div>
</div></section>
<section class="section bg-grey"><div class="wrap grid-2">
<div class="frame navy reveal">{art("pipes", "about-who", alt="Stacked steel pipes")}</div>
<div class="stack reveal"><span class="eyebrow">Who we are</span><h2 class="h-lg">A team that knows steel and respects deadlines.</h2>
<p>We are a steel supply business focused on four product families: sheets, pipes, structural sections, and iron &amp; metal products. Our role is to make buying steel straightforward: clear advice, accurate quotations, inspected material and organised delivery.</p>
<p class="muted">{ph("Add details about the team, ownership and areas served")}</p>
<a class="link-arrow" href="leadership.html">Meet our leadership {ARROW}</a></div>
</div></section>
<section class="section"><div class="wrap grid-2" style="align-items:stretch;gap:4px">
<div class="vm navy reveal"><span class="eyebrow">Our vision</span><h3>To be the steel supplier builders trust first.</h3><p>To be recognised for dependable steel supply, known for quality material, honest dealing and delivery that keeps projects on track.</p>{CHEV}</div>
<div class="vm red reveal"><span class="eyebrow">Our mission</span><h3>The right steel, on time, every time.</h3><p>To supply steel and metal products that meet each customer's specification, backed by clear communication, careful inspection and organised delivery.</p>{CHEV}</div>
<p class="note" style="margin-top:18px">Vision and mission are drafted for you to review and edit.</p></div></section>
<section class="section bg-grey"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Core values</span><h2 class="h-lg">What we stand for.</h2></div></div>
<div class="grid-3 two-md reveal">{"".join(f'<div class="value">{icon(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in values)}</div></div></section>
<section class="section bg-navy"><div class="wrap grid-2 top">
<div class="stack reveal"><span class="eyebrow">Why choose AB Royal Steels</span><h2 class="h-lg">One supplier for the whole steel list.</h2><p class="lead">From sheets and pipes to beams, rods and accessories, we bring your steel requirement together into one quotation and one coordinated delivery.</p></div>
<ul class="why-list reveal" style="grid-template-columns:1fr">
<li>{icon("layers")}<div><h3>Broad product range</h3><p>Four product families covering most construction, fabrication and industrial needs.</p></div></li>
<li>{icon("doc")}<div><h3>Clear quotations</h3><p>Material, specification, quantity and delivery terms written down before you commit.</p></div></li>
<li>{icon("truck")}<div><h3>Coordinated delivery</h3><p>Dispatch planned to your site schedule, with updates along the way.</p></div></li>
</ul></div></section>
<section class="feature-row reveal">{art("chequer", "about-quality", alt="Chequered steel plate")}<div class="txt"><span class="eyebrow">Our commitment to quality</span><h2 class="h-lg">Checked before it ships.</h2>
<p class="lead">Quality is built into how we handle every order, not added at the end.</p>
<ul><li>Specification confirmed with you before quotation</li><li>Material checked against the order before dispatch</li><li>Careful bundling and handling to avoid damage in transit</li><li>{ph("Add certifications or test documentation you provide")}</li></ul>
<a class="link-arrow" href="quality.html">Quality &amp; standards {ARROW}</a></div></section>
<section class="feature-row rev bg-grey reveal">{art("structure", "about-customers", alt="Steel structure under construction")}<div class="txt"><span class="eyebrow">Our commitment to customers</span><h2 class="h-lg">Easy to reach. Easy to work with.</h2>
<p class="lead">You get a clear point of contact, straight answers and follow-through from enquiry to delivery.</p>
<ul><li>Fast, clear responses to enquiries</li><li>Honest advice on product choice and alternatives</li><li>Delivery updates until material reaches site</li><li>Support after delivery if anything needs attention</li></ul>
<a class="link-arrow" href="contact.html">Talk to us {ARROW}</a></div></section>
''' + cta_band()
    page('about.html', 'About Us · AB Royal Steels', 'About AB Royal Steels: company overview, vision, mission, values and our commitments to quality and customers.', body)

# ---------- PRODUCTS ----------
def product_card(p, r=''):
    return f'''<article class="prod"><a href="{r}products/{p["slug"]}.html" tabindex="-1" aria-hidden="true" class="zoom" style="position:relative;display:block">{art(p["art"], "p-" + p["slug"], alt=p["name"])}<span class="tag">{E(p["cat"]["name"])}</span></a>
<div class="body"><h3><a href="{r}products/{p["slug"]}.html">{E(p["name"])}</a></h3><p>{E(p["desc"])}</p>
<div class="acts"><a class="btn btn-navy" href="{r}products/{p["slug"]}.html">Explore Product</a><a class="btn btn-red" href="{r}products/{p["slug"]}.html#enquiry">Request Price</a></div></div></article>'''

def products():
    body = page_hero('Product Catalogue', 'Steel sheets, steel pipes, structural sections, and iron &amp; metal products. Explore each product, or send one enquiry for your full list.', [('index.html', 'Home'), (None, 'Products')], 'pipes', 'products-hero')
    body += '<nav class="cat-nav" aria-label="Product categories"><div class="wrap">' + ''.join(f'<a href="#{c["id"]}"><b>{c["letter"]}</b>{E(c["name"])}</a>' for c in CATEGORIES) + '</div></nav>'
    for c in CATEGORIES:
        prods = [p for p in ALL_PRODUCTS if p['cat'] is c]
        body += f'''<section class="cat-block" id="{c["id"]}"><div class="wrap"><div class="cat-head reveal"><div><span class="letter" aria-hidden="true">{c["letter"]}</span><span class="eyebrow">Category {c["letter"]}</span><h2 class="h-lg" style="margin-top:14px">{E(c["name"])}</h2></div>
<div class="stack"><p class="lead">{E(c["intro"])}</p><a class="link-arrow" href="quote.html">Quote for this category {ARROW}</a></div></div>
<div class="prod-grid">{"".join(product_card(p) for p in prods)}</div></div></section>'''
    body += cta_band(title="Have a full steel list?", text="Send the whole list in one go. We will quote each item with specification, quantity and delivery terms.")
    page('products.html', 'Products · AB Royal Steels', 'Steel sheets, steel pipes, structural sections, and iron & metal products from AB Royal Steels.', body)

FAMILY_ART = {'steel-sheets': ['sheets', 'plates', 'coils'], 'steel-pipes': ['pipes', 'square', 'warehouse'], 'steel-sections': ['ibeam', 'channel', 'angle'], 'iron-metal-products': ['rebar', 'bars', 'plates']}

def product_detail(p):
    r = '../'
    c = p['cat']
    thumbs = ([a for a in FAMILY_ART[c['id']] if a != p['art']] + ['warehouse', 'coils'])
    thumbs = list(dict.fromkeys(t for t in thumbs if t != p['art']))[:3]
    specs = [('Product', E(p['name'])), ('Category', E(c['name'])), ('Material / grade', ph('Add grade(s) supplied')), ('Standard', ph('Add applicable standard, e.g. IS / ASTM / EN')),
             ('Thickness range', ph('Add thickness range in mm')), ('Sizes / dimensions', ph('Add width × length or OD / section sizes')), ('Length', ph('Add standard lengths')),
             ('Surface / finish', ph('Add finish or coating')), ('Packaging', ph('Add bundle or packing details')), ('Test certificate', ph('Confirm whether provided'))]
    rows = ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in specs)
    size_rows = ''.join(f'<tr><td>{ph("Size")}</td><td>{ph("Thickness")}</td><td>{ph("Length")}</td><td>{ph("Weight")}</td></tr>' for _ in range(4))
    related = [x for x in ALL_PRODUCTS if x['cat'] is c and x is not p][:4]
    body = page_hero(E(p['name']), E(p['desc']), [('index.html', 'Home'), ('products.html', 'Products'), (f'products.html#{c["id"]}', c['name']), (None, p['name'])], p['art'], 'p-' + p['slug'] + '-hero', r)
    body += f'''<section class="section"><div class="wrap pd-top">
<div class="pd-gallery reveal">{art(p["art"], "p-" + p["slug"], alt=p["name"])}<div class="pd-thumbs">{"".join(art(t, f"p-{p['slug']}-{i}", alt=p['name']) for i, t in enumerate(thumbs))}</div></div>
<div class="pd-info reveal"><span class="eyebrow">{E(c["name"])}</span><h1>{E(p["name"])}</h1><p class="lead">{E(p["desc"])}</p>
<dl class="pd-facts"><div><dt>Category</dt><dd>{E(c["name"])}</dd></div><div><dt>Grade</dt><dd>{ph("Add grade")}</dd></div><div><dt>Thickness</dt><dd>{ph("Add range")}</dd></div><div><dt>Sizes</dt><dd>{ph("Add sizes")}</dd></div></dl>
<div class="btn-row"><a class="btn btn-red" href="#enquiry">Request Price {ARROW}</a><a class="btn btn-line" href="{r}quote.html">Add to a Quote</a></div>
<p class="note">Specifications and sizes are confirmed with each quotation. Contact us for availability.</p></div>
</div></section>
<section class="section bg-grey"><div class="wrap grid-2 top">
<div class="reveal"><span class="eyebrow">Specifications</span><h2 class="h-md" style="margin:14px 0 26px">Technical details</h2><div class="spec-table-wrap"><table class="spec-table"><tbody>{rows}</tbody></table></div></div>
<div class="reveal"><span class="eyebrow">Available sizes</span><h2 class="h-md" style="margin:14px 0 26px">Size chart</h2><div class="spec-table-wrap"><table class="spec-table"><thead><tr><th>Size</th><th>Thickness</th><th>Length</th><th>Weight</th></tr></thead><tbody>{size_rows}</tbody></table></div>
<p class="note">Add the size chart for this product. Rows can be added or removed in the page source.</p></div>
</div></section>
<section class="section"><div class="wrap grid-2 top">
<div class="reveal stack"><span class="eyebrow">Applications</span><h2 class="h-md">Where it is used</h2><ul class="app-list">{"".join(f"<li>{E(a)}</li>" for a in p["apps"])}</ul></div>
<div id="enquiry" class="reveal" style="scroll-margin-top:110px">{enquiry_form(p["name"], r, "Request a price", "Tell us the size, thickness, quantity and delivery location for " + E(p["name"]) + ".")}</div>
</div></section>
<section class="section bg-grey"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Related products</span><h2 class="h-lg">More {E(c["name"])}</h2></div><a class="btn btn-line" href="{r}products.html#{c["id"]}">All {E(c["name"])} {ARROW}</a></div>
<div class="prod-grid reveal">{"".join(product_card(x, r) for x in related)}</div></div></section>''' + cta_band(r)
    page(f'products/{p["slug"]}.html', f'{p["name"]} · AB Royal Steels', f'{p["name"]} from AB Royal Steels: {p["desc"]}', body, 'products.html', depth=1)

# ---------- INDUSTRIES ----------
def industries():
    body = page_hero('Industries We Serve', 'Steel for the sectors that build, make and move. Here is how our products are used across the industries we supply.', [('index.html', 'Home'), (None, 'Industries')], 'structure', 'industries-hero')
    body += f'<section class="section tight"><div class="wrap"><div class="ind-grid reveal">' + ''.join(f'<a class="ind-card zoom" href="#{s}">{art(a, "indx-" + s, alt=n)}<div class="body"><span class="bar"></span><h3>{E(n)}</h3></div></a>' for s, n, a, d, _ in INDUSTRIES) + '</div></div></section>'
    name_to_slug = {x['name']: x['slug'] for x in ALL_PRODUCTS}
    name_to_slug.update({'MS Sheets': 'ms-sheets', 'GI Sheets': 'gi-sheets'})
    for i, (s, n, a, d, prods) in enumerate(INDUSTRIES):
        links = ''.join(f'<li><a href="products/{name_to_slug.get(x, "")}.html">{E(x)}</a></li>' if x in name_to_slug else f'<li>{E(x)}</li>' for x in prods)
        body += f'''<section id="{s}" class="feature-row{" rev bg-grey" if i % 2 else ""} reveal" style="scroll-margin-top:90px">{art(a, "ind-" + s, alt=n)}<div class="txt"><span class="eyebrow">Industry {i+1:02d}</span><h2 class="h-lg">{E(n)}</h2><p class="lead">{E(d)}</p>
<h3 class="h-sm" style="margin-top:6px">Products commonly supplied</h3><ul>{links}</ul><div><a class="btn btn-red btn-sm" href="quote.html">Request a Quote {ARROW}</a></div></div></section>'''
    body += cta_band(title='Your industry not listed?', text='If your work uses steel, we can likely help. Tell us about your application.')
    page('industries.html', 'Industries · AB Royal Steels', 'Industries served by AB Royal Steels: construction, real estate, manufacturing, fabrication, warehousing, commercial, roofing and industrial projects.', body)

# ---------- PROCESS ----------
def process():
    body = page_hero('Our Process', 'Seven clear steps from your first enquiry to material delivered on site.', [('index.html', 'Home'), (None, 'Our Process')], 'warehouse', 'process-hero')
    items = ''.join(f'''<li class="tl-item reveal"><div class="tl-media">{art(a, f"proc-{i}", cls="", alt=t)}</div><span class="tl-node">{icon(ic, "")}</span>
<div class="tl-text"><span class="tl-num">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div></li>''' for i, (t, ic, a, d) in enumerate(PROCESS))
    items = items.replace('<div class="tl-media"><div class="art "', '<div class="tl-media"><div class="art" style="height:100%"')
    body += f'''<section class="section"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">How we work</span><h2 class="h-lg">A supply workflow built for accuracy.</h2></div><p class="lead">Each step has one job: make sure what arrives on site is exactly what the project needs.</p></div>
<ol class="timeline">{items}</ol></div></section>''' + cta_band(title='Start with step one.', text='Share your requirement and we will take it from there.')
    page('process.html', 'Our Process · AB Royal Steels', 'How AB Royal Steels works: from understanding requirements to quotation, inspection, dispatch and delivery.', body)

# ---------- PROJECTS ----------
def projects():
    body = page_hero('Projects', 'Steel supplied for commercial, industrial, roofing, infrastructure and fabrication work.', [('index.html', 'Home'), (None, 'Projects')], 'structure-night', 'projects-hero')
    filt = '<button class="filter is-active" type="button" data-filter="all" aria-pressed="true">All projects</button>' + ''.join(f'<button class="filter" type="button" data-filter="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in PROJECT_CATS)
    cards = ''.join(f'''<article class="proj {size} zoom" data-cat="{E(c)}">{art(a, f"proj-{i}", alt=c)}<div class="body"><span class="cat">{E(c)}</span><h3>{ph("Project name")}</h3>
<p>{ph("Location · year · short description of the work")}</p><p class="mats"><b>Materials supplied</b>{ph("e.g. " + m)}</p></div></article>''' for i, (c, a, size, m) in enumerate(PROJECTS))
    body += f'''<section class="section"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Portfolio</span><h2 class="h-lg">Steel at work.</h2></div>
<p class="note" style="max-width:46ch">These portfolio entries are placeholders. Replace each with a completed project: photo, title, category, description and materials supplied.</p></div>
<div class="filters" role="group" aria-label="Filter projects by category">{filt}</div><div class="gallery">{cards}</div></div></section>''' + cta_band(title='Planning a project?', text='Tell us about the build and the steel it needs. We will quote the full list.')
    page('projects.html', 'Projects · AB Royal Steels', 'Projects and applications supplied by AB Royal Steels.', body)

# ---------- INFRASTRUCTURE ----------
def infrastructure():
    body = page_hero('Infrastructure', 'The storage, handling and logistics that keep steel moving from our yard to your site.', [('index.html', 'Home'), (None, 'Infrastructure')], 'warehouse-left', 'infra-hero')
    facts = [('Location', 'Add yard / warehouse address'), ('Storage area', 'Add covered and open area'), ('Handling equipment', 'Add cranes, forklifts, etc.'), ('Fleet', 'Add number and type of vehicles'), ('Delivery coverage', 'Add regions served'), ('Processing', 'Add cutting or other services, if offered')]
    body += f'''<section class="section"><div class="wrap grid-2">
<div class="stack reveal"><span class="eyebrow">Facilities</span><h2 class="h-lg">Organised stock. Safe handling. Ready to load.</h2><p class="lead">Steel is heavy, long and easily damaged when handled badly. Our facilities are set up to store, sort and load material safely.</p>
<p class="muted">{ph("Describe your warehouse or stockyard: location, layout and how material is stored")}</p></div>
<div class="spec-table-wrap reveal"><table class="spec-table"><thead><tr><th colspan="2">Facility overview</th></tr></thead><tbody>{"".join(f"<tr><th scope='row'>{k}</th><td>{ph(v)}</td></tr>" for k, v in facts)}</tbody></table></div>
</div></section>
<section class="feature-row reveal">{art("warehouse", "infra-warehouse", alt="Steel warehouse with racking")}<div class="txt"><span class="eyebrow">Warehouse &amp; storage</span><h2 class="h-lg">Stored by product, size and grade.</h2>
<p class="lead">Material is racked and stacked by product family so orders can be picked accurately and quickly.</p><ul><li>Separate storage for sheets, pipes, sections and rods</li><li>Clear identification of size and grade</li><li>{ph("Add covered storage details")}</li></ul></div></section>
<section class="feature-row rev bg-grey reveal">{art("crane" if False else "ibeam", "infra-handling", alt="Structural steel sections")}<div class="txt"><span class="eyebrow">Material handling</span><h2 class="h-lg">Lifted and loaded with care.</h2>
<p class="lead">Long and heavy items are moved with the right equipment to protect the material and the people around it.</p><ul><li>{ph("Add handling equipment: overhead cranes, forklifts, etc.")}</li><li>Bundling and strapping before loading</li><li>Load checks before dispatch</li></ul></div></section>
<section class="fleet"><div class="wrap"><div class="stack reveal"><span class="eyebrow">Logistics &amp; fleet</span><h2 class="h-lg">Delivered in our colours.</h2><p class="lead">Our red, navy and white livery is a familiar sight on delivery routes. Each load is secured, documented and tracked to your site.</p>
<p class="muted">{ph("Add fleet size, vehicle types and delivery regions")}</p><div class="btn-row"><a class="btn btn-red" href="quote.html">Request a Quote {ARROW}</a></div></div>
<div class="fleet-img reveal"><img src="assets/img/truck.png" alt="AB Royal Steels branded truck" width="873" height="486" loading="lazy"></div></div></section>
<section class="feature-row reveal">{art("fabrication", "infra-processing", alt="Steel processing")}<div class="txt"><span class="eyebrow">Processing support</span><h2 class="h-lg">{ph("Processing services")}</h2>
<p class="lead">{ph("If AB Royal Steels offers cutting, bending, slitting or other processing, describe it here. Remove this section if not offered.")}</p></div></section>''' + cta_band()
    page('infrastructure.html', 'Infrastructure · AB Royal Steels', 'AB Royal Steels infrastructure: warehouse and storage, material handling, logistics and fleet.', body)

# ---------- QUALITY ----------
def quality():
    checks = [('doc', 'Specification review', 'Grade, size, thickness and finish confirmed with you before quotation.'),
              ('search', 'Visual inspection', 'Surface condition checked for visible defects, rust and damage.'),
              ('ruler', 'Dimension check', 'Key dimensions and thickness checked against the order.'),
              ('layers', 'Quantity & identification', 'Counts, weights and markings verified against the order.'),
              ('box', 'Packing check', 'Bundles strapped and protected for safe handling in transit.'),
              ('truck', 'Dispatch verification', 'Load and documents checked before the vehicle leaves.')]
    body = page_hero('Quality &amp; Standards', 'Quality starts with getting the specification right, and continues through inspection, packing and dispatch.', [('index.html', 'Home'), (None, 'Quality & Standards')], 'chequer', 'quality-hero')
    body += f'''<section class="section"><div class="wrap grid-2">
<div class="stack reveal"><span class="eyebrow">Our approach</span><h2 class="h-lg">The right material, verified.</h2><p class="lead">We treat each order as a specification to be met. Material is checked against what was agreed before it is released for dispatch.</p>
<p class="muted">{ph("Add your quality policy statement")}</p></div>
<div class="frame reveal">{art("plates", "quality-approach", alt="Steel plates")}<span class="frame-tag">Inspect before dispatch</span></div></div></section>
<section class="section bg-grey"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Quality checkpoints</span><h2 class="h-lg">What we check on every order.</h2></div><p class="note" style="max-width:44ch">Review these checkpoints and edit them to match your inspection practice.</p></div>
<ol class="checks reveal">{"".join(f"<li>{icon(i)}<h3>{t}</h3><p>{d}</p></li>" for i, t, d in checks)}</ol></div></section>
<section class="section"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Standards &amp; certifications</span><h2 class="h-lg">Certifications</h2></div><p class="lead">Add the certifications, memberships and product standards that apply to AB Royal Steels.</p></div>
<div class="grid-4 reveal">{"".join(f'<div class="cert-slot"><span class="seal">{icon("award","")}</span><h3>{ph("Certification name")}</h3><p class="muted">{ph("Issuing body and scope")}</p></div>' for _ in range(4))}</div></div></section>
<section class="section bg-navy"><div class="wrap grid-2">
<div class="stack reveal"><span class="eyebrow">Product standards</span><h2 class="h-lg">Grades and standards by product.</h2><p class="lead">Each product page has a specification table where the applicable grades and standards can be listed.</p><a class="btn btn-ghost" href="products.html">Browse products {ARROW}</a></div>
<div class="spec-table-wrap reveal"><table class="spec-table"><thead><tr><th>Product family</th><th>Standards / grades</th></tr></thead><tbody>{"".join(f"<tr><th scope='row'>{E(c['name'])}</th><td>{ph('Add standards and grades')}</td></tr>" for c in CATEGORIES)}</tbody></table></div>
</div></section>''' + cta_band(title='Need documents with your order?', text='Ask about the documentation available for your products when you request a quote.')
    page('quality.html', 'Quality & Standards · AB Royal Steels', 'Quality approach, inspection checkpoints and standards at AB Royal Steels.', body)

# ---------- LEADERSHIP ----------
def leadership():
    body = page_hero('Founder &amp; Leadership', 'The people responsible for how AB Royal Steels serves its customers.', [('index.html', 'Home'), (None, 'Founder & Leadership')], 'structure', 'leadership-hero')
    body += f'''<section class="section"><div class="wrap leader-hero">
<div class="portrait reveal" data-key="founder-portrait"><span class="initials">AB</span><span class="ph-label">Add founder photo</span></div>
<div class="stack reveal"><span class="eyebrow">Founder's message</span><span class="quote-mark" aria-hidden="true">“</span>
<p class="founder-msg">{ph("Add the founder's message: why AB Royal Steels was started, what the company stands for, and the commitment to customers.")}</p>
<div class="sig"><b>{ph("Founder name")}</b><span class="muted">Founder &amp; {ph("Designation")}, AB Royal Steels</span></div></div>
</div></section>
<section class="section bg-grey"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">Leadership team</span><h2 class="h-lg">Leadership</h2></div><p class="lead">Add the people who lead sales, operations, logistics and finance.</p></div>
<div class="team reveal">{"".join(f'<div class="member"><div class="portrait"><span class="initials">{ini}</span></div><h3>{ph("Name")}</h3><p>{ph(role)}</p></div>' for ini, role in [("01", "Designation"), ("02", "Designation"), ("03", "Designation"), ("04", "Designation")])}</div></div></section>
<section class="section bg-navy"><div class="wrap"><div class="split-head reveal"><div><span class="eyebrow">How we lead</span><h2 class="h-lg">Principles behind every order.</h2></div></div>
<ul class="why-list reveal"><li>{icon("handshake")}<div><h3>Customer first</h3><p>Decisions are made around what keeps the customer's project on track.</p></div></li>
<li>{icon("shield")}<div><h3>Accountability</h3><p>We own every order from quotation to delivery.</p></div></li>
<li>{icon("users")}<div><h3>A capable team</h3><p>We invest in people who know the products and care about the details.</p></div></li>
<li>{icon("target")}<div><h3>Steady growth</h3><p>We grow by earning repeat business, one delivery at a time.</p></div></li></ul></div></section>''' + cta_band()
    page('leadership.html', 'Founder & Leadership · AB Royal Steels', 'Founder and leadership team of AB Royal Steels.', body)

# ---------- CONTACT ----------
def contact():
    body = page_hero('Contact Us', 'Questions about products, availability or delivery? Get in touch with our team.', [('index.html', 'Home'), (None, 'Contact Us')], 'road', 'contact-hero')
    body += f'''<section class="section"><div class="wrap grid-2 top">
<div class="stack-lg reveal"><div class="stack"><span class="eyebrow">Get in touch</span><h2 class="h-lg">Talk to AB Royal Steels.</h2><p class="lead">Call, email or visit us. For pricing, the quickest route is the quote form with your full requirement.</p></div>
<div class="contact-cards">
<div class="cc">{icon("pin")}<div><h3>Visit</h3><p>{ph("Street address")}<br>{ph("City, State, Postcode")}<br>{ph("Country")}</p></div></div>
<div class="cc">{icon("phone")}<div><h3>Call</h3><p>{ph("Phone number")}<br>{ph("WhatsApp number, if used")}</p></div></div>
<div class="cc">{icon("mail")}<div><h3>Email</h3><p>{ph("Sales email")}<br>{ph("General email")}</p></div></div>
<div class="cc" style="background:var(--red)">{icon("clock")}<div><h3>Working hours</h3><p>{ph("e.g. Monday to Saturday, 9:00 to 18:00")}</p></div></div>
</div></div>
<div class="reveal">{enquiry_form()}</div></div></section>
<section class="map-slot" aria-label="Location map placeholder"><div class="grid-lines"></div><div><div class="pin"></div><h2 class="h-md" style="color:#fff">Find us</h2><p style="margin-top:10px;color:rgba(255,255,255,0.75)">{ph("Add a map link or embed for your location")}</p></div></section>'''
    page('contact.html', 'Contact · AB Royal Steels', 'Contact AB Royal Steels for steel sheets, pipes, sections and metal products.', body)

# ---------- QUOTE ----------
def quote():
    opts = ''.join(f'<optgroup label="{E(c["name"])}">' + ''.join(f'<option>{E(p[1])}</option>' for p in c['products']) + '</optgroup>' for c in CATEGORIES)
    def row(n):
        return f'''<div class="item-row"><div class="field"><label for="it-p-{n}">Product</label><select id="it-p-{n}" name="item_product_{n}"><option value="">Select product</option>{opts}</select></div>
<div class="field"><label for="it-s-{n}">Size / spec</label><input id="it-s-{n}" name="item_size_{n}" placeholder="e.g. 50×50×3 mm"></div>
<div class="field"><label for="it-q-{n}">Quantity</label><input id="it-q-{n}" name="item_qty_{n}" placeholder="e.g. 100"></div>
<div class="field"><label for="it-u-{n}">Unit</label><select id="it-u-{n}" name="item_unit_{n}"><option>Pieces</option><option>Tonnes</option><option>Kg</option><option>Metres</option><option>Bundles</option></select></div>
<button class="rm" type="button" aria-label="Remove item">×</button></div>'''
    body = page_hero('Request a Quote', 'List the products you need. We will reply with a clear quotation covering specification, quantity and delivery.', [('index.html', 'Home'), (None, 'Request a Quote')], 'sheets', 'quote-hero')
    body += f'''<section class="section bg-grey"><div class="wrap grid-2 top quote-grid">
<div class="form-card reveal"><h2 class="h-md">Your requirement</h2><p class="muted">Fields marked * are required.</p>
<form class="form" data-enquiry>
<div class="field"><label for="q-name">Full name <span class="req">*</span></label><input id="q-name" name="name" autocomplete="name" required><span class="err">Please enter your name.</span></div>
<div class="field"><label for="q-company">Company <span class="req">*</span></label><input id="q-company" name="company" autocomplete="organization" required><span class="err">Please enter your company.</span></div>
<div class="field"><label for="q-email">Email <span class="req">*</span></label><input id="q-email" name="email" type="email" autocomplete="email" required><span class="err">Please enter a valid email.</span></div>
<div class="field"><label for="q-phone">Phone <span class="req">*</span></label><input id="q-phone" name="phone" type="tel" autocomplete="tel" required><span class="err">Please enter a phone number.</span></div>
<div class="items-table full"><h3 class="h-sm" style="margin:12px 0 16px">Products required</h3><div id="items">{row(1)}</div>
<button class="btn btn-line btn-sm" id="add-item" type="button">{icon("plus","")} Add another product</button></div>
<div class="field"><label for="q-loc">Delivery location <span class="req">*</span></label><input id="q-loc" name="delivery_location" required placeholder="City / site address"><span class="err">Please enter a delivery location.</span></div>
<div class="field"><label for="q-date">Required by</label><input id="q-date" name="required_by" type="date"></div>
<div class="field"><label for="q-type">Customer type</label><select id="q-type" name="customer_type"><option>Contractor / builder</option><option>Fabricator</option><option>Manufacturer</option><option>Developer</option><option>Trader / dealer</option><option>Other</option></select></div>
<div class="field"><label for="q-file">Drawings or BOQ (optional)</label><input id="q-file" name="attachment" type="file" accept=".pdf,.xls,.xlsx,.csv,.jpg,.png,.dwg"></div>
<div class="field full"><label for="q-notes">Additional notes</label><textarea id="q-notes" name="message" placeholder="Grades, standards, finish, packing or anything else we should know"></textarea></div>
<div class="full"><button class="btn btn-red" type="submit">Submit Quote Request {ARROW}</button></div>
<div class="form-status" role="status" aria-live="polite"></div>
</form>
<template id="item-template">{row("__N__")}</template></div>
<aside class="stack-lg reveal"><div class="vm navy"><span class="eyebrow">What happens next</span><h3 style="font-size:32px">Clear, written quotations.</h3>
<ol class="proc-h" style="grid-template-columns:1fr;row-gap:22px;margin-top:20px">{"".join(f'<li style="display:grid;grid-template-columns:64px 1fr;gap:16px;align-items:center"><span class="node">{icon(ic,"")}</span><div><span class="num" style="margin:0">{n}</span><h3 style="margin:2px 0 0">{t}</h3></div></li>' for n, ic, t in [("01", "doc", "We review your list"), ("02", "chat", "We confirm any details"), ("03", "check", "You receive a quotation")])}</ol></div>
<div class="cc" style="background:var(--char)">{icon("phone")}<div><h3>Prefer to call?</h3><p>{ph("Phone number")}</p></div></div></aside>
</div></section>'''
    page('quote.html', 'Request a Quote · AB Royal Steels', 'Request a quotation for steel sheets, pipes, sections and metal products from AB Royal Steels.', body)

if __name__ == '__main__':
    home(); home(artifact=True); about(); products(); industries(); process(); projects(); infrastructure(); quality(); leadership(); contact(); quote()
    for p in ALL_PRODUCTS: product_detail(p)
    print('built', 11 + len(ALL_PRODUCTS), 'pages')
