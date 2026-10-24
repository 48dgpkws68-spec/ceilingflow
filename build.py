#!/usr/bin/env python3
"""Bouwt de statische Ceilingflow-site: index, /ventilator/, /bedankt/, 404, sitemap en robots."""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
URL = 'https://ceilingflow.nl'
PHONE = '+31 6 34 33 38 09'
MAIL = 'nick@gnc-systems.com'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">'
ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 rx=%2214%22 fill=%22%230d0f10%22/%3E%3Ccircle cx=%2232%22 cy=%2232%22 r=%2218%22 fill=%22none%22 stroke=%22%23ff5a1f%22 stroke-width=%225%22/%3E%3Ccircle cx=%2232%22 cy=%2232%22 r=%225%22 fill=%22%23eef0ee%22/%3E%3C/svg%3E">'
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="1.5" y="1.5" width="29" height="29" rx="7" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="16" cy="16" r="8.5" fill="none" stroke="#ff5a1f" stroke-width="2.6"/><circle cx="16" cy="16" r="2.6" fill="currentColor"/></svg>'

FAQ = [
    ("Past Ceilingflow in ieder systeemplafond?", "Ceilingflow is ontworpen voor het standaard 60×60 cm systeemplafond. Dat is het meest gebruikte formaat in kantoren, scholen, zorginstellingen en andere professionele omgevingen. Heb je een afwijkend formaat? Neem dan contact op voor advies."),
    ("Is Ceilingflow een lamp of verlichtingsarmatuur?", "Nee. Ceilingflow is geen lamp. Het is een ventilatie-oplossing voor het 60×60 systeemplafond die zorgt voor luchtcirculatie, niet voor verlichting. Je plaatst Ceilingflow naast je bestaande verlichting."),
    ("Is Ceilingflow geschikt voor scholen en klaslokalen?", "Ja. De stille werking stoort niet tijdens lessen of toetsen. De geïntegreerde montage is veilig voor kinderen en de strakke uitstraling past in iedere schoolomgeving."),
    ("Kan ik meerdere units bestellen?", "Ja, je bestelt eenvoudig meerdere units. Levering volgt vanaf 25 oktober. Voor grotere aantallen of maatwerk vraag je een zakelijke offerte aan, dan denken we mee over de beste oplossing voor jouw situatie."),
    ("Kan ik een zakelijke factuur ontvangen?", "Ja. Je ontvangt altijd een btw-factuur bij je bestelling. Je kunt je KvK-nummer en btw-nummer opgeven bij het bestellen."),
    ("Hoe werkt de verzending?", "De prijs is €299 excl. btw (€361,79 incl. btw), exclusief verzendkosten. Verzending kost per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50, Duitsland en de rest van West-Europa €24,50, overige EU-landen €34,50. Buiten Europa leveren we alleen op aanvraag via het offerteformulier. Bestellen kan gewoon: levering van beide kleuren volgt vanaf 25 oktober."),
    ("Is de installatie moeilijk?", "Nee. Ceilingflow plaats je in het bestaande 60×60 plafondrooster, net als een verlichtingsarmatuur. Installatie duurt gemiddeld minder dan 5 minuten per unit. Er zijn geen bouwkundige aanpassingen of speciaal gereedschap nodig."),
    ("Is er een speciale prijs voor meerdere units?", "Bij afname van meerdere units vraag je een zakelijke offerte aan. We maken een offerte op maat. Gebruik het offerteformulier of bel ons direct."),
    ("Kan ik een offerte aanvragen?", "Ja, via het offerteformulier op deze site. Geef het gewenste aantal units, de locatie en je contactgegevens op. Je krijgt binnen één werkdag een offerte op maat."),
    ("Hoe stil is Ceilingflow tijdens gebruik?", "Ceilingflow werkt onder 35 dB, vergelijkbaar met een zachte fluisterstem. Geschikt tijdens vergaderingen, lessen, behandelingen en in slaapruimtes van de kinderopvang."),
    ("Heeft Ceilingflow veel onderhoud nodig?", "Het onderhoud is minimaal. De luchtinlaat een paar keer per jaar reinigen is genoeg. Er zijn geen slijtende onderdelen die regelmatig vervangen moeten worden."),
]

SPECS = [("Formaat", "60 × 60 cm"), ("Geluidsniveau", "< 35 dB"), ("Installatietijd", "< 5 minuten"), ("Bescherming", "IP44"),
         ("Motor", "Borstelloos, CE / LVD"), ("Materiaal", "ABS, RoHS gecertificeerd"), ("Kleur", "Wit of Zwart"),
         ("Inbegrepen", "Afstandsbediening"), ("Aansluiting", "Stekker in het stopcontact"), ("SKU", "CF-6060-001")]


def head(title, desc, path, extra=''):
    return f'''<!doctype html>
<html lang="nl" data-kleur="wit">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{URL}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ceilingflow">
<meta property="og:locale" content="nl_NL">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{URL}{path}">
<meta property="og:image" content="{URL}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#eef0ee">
{ICON}
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
<script>try{{var k=new URLSearchParams(location.search).get('kleur')||localStorage.getItem('cf_kleur');if(k==='zwart'||k==='wit')document.documentElement.dataset.kleur=k}}catch(e){{}}</script>
{extra}
</head>
<body>
'''


def nav(home=True):
    p = '' if home else '/'
    return f'''<div class="topbar">Levertijd beide kleuren: vanaf 25 oktober · bestellen blijft mogelijk</div>
<nav class="main"><div class="wrap">
  <a class="logo" href="/" aria-label="Ceilingflow home">{LOGO}<span>Ceiling<i>flow</i></span></a>
  <div class="navl"><a href="{p}#oplossing">Oplossing</a><a href="{p}#toepassingen">Toepassingen</a><a href="/ventilator/">Ventilator</a><a href="{p}#offerte">Zakelijk</a><a href="{p}#faq">FAQ</a></div>
  <div class="navr">
    <a class="btn acc" href="/ventilator/">Bestel</a>
    <button class="cartbtn" type="button" data-cart-open aria-label="Winkelmandje" hidden><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M5 8h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg><span class="cc" data-cart-count></span></button>
  </div>
</div></nav>
'''


def kleur_toggle():
    return '<div class="kleur" role="group" aria-label="Kies kleur"><button type="button" data-set-kleur="wit" aria-pressed="true"><i style="background:#f4f4f2"></i>Wit</button><button type="button" data-set-kleur="zwart" aria-pressed="false"><i style="background:#151617"></i>Zwart</button></div>'


def offerte(title='Meerdere lokalen ventileren?'):
    return f'''<section class="b2b" id="offerte"><div class="wrap">
  <div class="rv">
    <span class="eyebrow" style="color:inherit;opacity:.7">Zakelijk aanbod</span>
    <h2 class="h2" style="margin:22px 0 24px">{title}</h2>
    <p class="lead">Voor kantoren, scholen, kinderopvang en zorginstellingen maken we zakelijke offertes op maat. Vertel hoeveel lokalen je wilt ventileren, dan denken we mee over de beste oplossing.</p>
    <div class="perks">
      <div><i></i><p><b>Offerte op maat</b><span>Persoonlijk advies per locatie</span></p></div>
      <div><i></i><p><b>Btw-factuur</b><span>Voor je zakelijke administratie</span></p></div>
      <div><i></i><p><b>Persoonlijk contact</b><span>Reactie binnen 1 werkdag</span></p></div>
    </div>
  </div>
  <form class="form rv d2" data-offerte>
    <div class="two"><label>Naam<input name="naam" required autocomplete="name"></label><label>Organisatie<input name="organisatie" autocomplete="organization"></label></div>
    <div class="two"><label>E-mail<input type="email" name="email" required autocomplete="email"></label><label>Telefoon<input type="tel" name="telefoon" autocomplete="tel"></label></div>
    <div class="two"><label>Aantal units<input type="number" name="aantal" min="1" value="10" inputmode="numeric"></label><label>Kleur<select name="kleur"><option>Wit</option><option>Zwart</option><option>Beide</option></select></label></div>
    <label>Type locatie<select name="locatie"><option>School</option><option>Kinderopvang</option><option>Zorginstelling</option><option>Kantoor</option><option>Anders</option></select></label>
    <label>Bericht<textarea name="bericht" placeholder="Aantal lokalen, plaats, gewenste leverdatum"></textarea></label>
    <button class="btn" type="submit">Offerte aanvragen</button>
    <p class="hint">Liever bellen? {PHONE} · {MAIL}</p>
  </form>
</div></section>
'''


def faq_block(items):
    q = ''.join(f'<details class="rv"><summary>{a}</summary><div class="a"><p>{b}</p></div></details>' for a, b in items)
    return f'''<section id="faq" style="padding:clamp(80px,12vw,150px) 0"><div class="wrap" style="display:grid;gap:40px">
  <div class="rv"><span class="eyebrow">FAQ</span><h2 class="h2" style="margin-top:20px">Veelgestelde<br>vragen</h2></div>
  <div>{q}</div>
</div></section>
'''


def footer():
    return f'''<footer><div class="wrap">
  <div><a class="logo" href="/" style="color:var(--ink)">{LOGO}<span>Ceiling<i>flow</i></span></a><p style="margin-top:14px;max-width:26em">Ventilatie voor 60×60 systeemplafonds. Voor kantoren, scholen, kinderopvang en zorginstellingen.</p></div>
  <div><h4>Product</h4><ul><li><a href="/ventilator/">Ceilingflow Ventilatie Unit</a></li><li><a href="/ventilator/#specs">Specificaties</a></li><li><a href="/#installatie">Installatie</a></li></ul></div>
  <div><h4>Zakelijk</h4><ul><li><a href="/#offerte">Offerte aanvragen</a></li><li>Btw-factuur</li><li>Bulkbestellingen</li></ul></div>
  <div><h4>Contact</h4><ul><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="tel:+31634333809">{PHONE}</a></li></ul></div>
  <div class="big" aria-hidden="true">Ceilingflow</div>
  <p style="grid-column:1/-1;font-size:13px">© 2026 Ceilingflow.nl · Alle rechten voorbehouden</p>
</div></footer>
<div class="toast" id="toast" role="status"></div>
<script src="/assets/shop.js"></script>
'''


def product_ld():
    return json.dumps({
        "@context": "https://schema.org", "@type": "Product", "name": "Ceilingflow Ventilatie Unit", "sku": "CF-6060-001",
        "brand": {"@type": "Brand", "name": "Ceilingflow"},
        "description": "Plafondventilator voor 60x60 systeemplafonds. Onder 35 dB, installatie in minder dan 5 minuten, IP44, borstelloze motor, afstandsbediening inbegrepen. Verkrijgbaar in Wit en Zwart.",
        "image": [f"{URL}/img/wit.webp", f"{URL}/img/zwart.webp"], "color": "Wit, Zwart",
        "offers": [{"@type": "Offer", "name": f"Ceilingflow {c}", "url": f"{URL}/ventilator/?kleur={c.lower()}", "priceCurrency": "EUR", "price": "361.79",
                    "priceSpecification": [{"@type": "UnitPriceSpecification", "price": "361.79", "priceCurrency": "EUR", "valueAddedTaxIncluded": True},
                                           {"@type": "UnitPriceSpecification", "price": "299.00", "priceCurrency": "EUR", "valueAddedTaxIncluded": False}],
                    "availability": "https://schema.org/PreOrder", "availabilityStarts": "2026-10-25", "itemCondition": "https://schema.org/NewCondition",
                    "shippingDetails": [{"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": v, "currency": "EUR"}, "shippingDestination": [{"@type": "DefinedRegion", "addressCountry": cc} for cc in ccs]} for v, ccs in (("9.50", ["NL"]), ("18.50", ["BE"]), ("24.50", ["DE"]))]}
                   for c in ("Wit", "Zwart")]
    }, ensure_ascii=False)


INDEX_CSS = '''<style>
.hero{padding:clamp(40px,6vw,80px) 0 0;overflow:hidden}
.hero .wrap{display:grid;gap:30px}
.hero h1{font-size:clamp(56px,12.5vw,200px);margin:22px 0 26px}
.hero .row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:30px}
.stage{position:relative;margin-top:clamp(20px,4vw,40px);aspect-ratio:16/10;border-radius:clamp(26px,4vw,48px);overflow:hidden;background:radial-gradient(120% 90% at 50% 0%,color-mix(in srgb,var(--ink) 7%,var(--bg)),var(--bg2));transition:background .9s}
@media(max-width:700px){.stage{aspect-ratio:4/5}}
.stage .grid{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:calc(100%/6) calc(100%/4);opacity:.7}
@media(max-width:700px){.stage .grid{background-size:calc(100%/3) calc(100%/5)}}
.stage .swap{position:absolute;left:50%;top:50%;width:min(62%,560px);aspect-ratio:1;translate:-50% -50%;transform:perspective(1200px) rotateX(calc(var(--p,0)*28deg)) scale(calc(1 + var(--p,0)*.18));transition:transform .1s linear}
@media(max-width:700px){.stage .swap{width:86%}}
.stage .swap img{width:100%;height:100%;object-fit:cover;border-radius:22px;box-shadow:0 50px 80px -30px rgba(0,0,0,.45),0 0 0 1px var(--line)}
html[data-kleur=wit] .stage .swap img{mix-blend-mode:multiply;box-shadow:none}
.chips{position:absolute;left:16px;right:16px;bottom:16px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
@media(max-width:700px){.chips{grid-template-columns:repeat(2,1fr)}}
.chips div{padding:12px 14px;border-radius:18px;background:color-mix(in srgb,var(--bg) 78%,transparent);backdrop-filter:blur(12px);box-shadow:inset 0 0 0 1px var(--line)}
.chips b{display:block;font-size:clamp(18px,2vw,26px);letter-spacing:-.03em}
.chips span{font-size:12px;color:var(--soft)}
.marq{overflow:hidden;border-block:1px solid var(--line);padding:22px 0;margin-top:clamp(60px,8vw,110px)}
.marq div{display:flex;gap:48px;width:max-content;animation:mq 38s linear infinite;font-size:clamp(28px,4vw,56px);font-weight:600;letter-spacing:-.04em;white-space:nowrap}
.marq span::after{content:"·";margin-left:48px;color:var(--acc)}
@keyframes mq{to{transform:translateX(-50%)}}
.sec{padding:clamp(90px,13vw,170px) 0}
.probs{display:grid;gap:12px;margin-top:50px}
@media(min-width:700px){.probs{grid-template-columns:1fr 1fr}}
@media(min-width:1100px){.probs{grid-template-columns:repeat(3,1fr)}}
.probs article{padding:28px;border-radius:var(--r);background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}
.probs .n{font-size:13px;color:var(--acc);font-weight:700;letter-spacing:.1em}
.probs h3{font-size:26px;margin:14px 0 10px;letter-spacing:-.03em;line-height:1.05}
.probs p{color:var(--soft);font-size:15px}
.sol{display:grid;gap:50px}
@media(min-width:1000px){.sol{grid-template-columns:1.1fr 1fr;align-items:center;gap:80px}}
.sol ul{list-style:none;margin-top:30px;display:grid;gap:2px}
.sol li{display:flex;gap:14px;padding:16px 0;border-bottom:1px solid var(--line);font-size:17px}
.sol li::before{content:"";flex:0 0 10px;height:10px;margin-top:8px;border-radius:50%;background:var(--acc)}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.stats div{padding:28px 22px;border-radius:var(--r);background:var(--inv);color:var(--invink);transition:background-color .9s,color .9s}
.stats b{display:block;font-size:clamp(34px,4.4vw,60px);letter-spacing:-.05em;line-height:1}
.stats span{display:block;margin-top:10px;font-size:14px;opacity:.7}
.vid{margin-top:50px;border-radius:clamp(24px,4vw,44px);overflow:hidden;background:#000}
.vid video{width:100%;aspect-ratio:16/9;object-fit:cover}
.steps{display:grid;gap:12px;margin-top:16px}
@media(min-width:800px){.steps{grid-template-columns:repeat(3,1fr)}}
.steps div{padding:24px;border-radius:22px;box-shadow:inset 0 0 0 1px var(--line)}
.steps b{font-size:46px;letter-spacing:-.05em;color:var(--acc);line-height:1}
.steps p{margin-top:8px;font-weight:600;font-size:18px}
.apps{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:50px 16px 10px;margin:0 -16px;scrollbar-width:none}
.apps::-webkit-scrollbar{display:none}
.apps article{flex:0 0 min(84%,440px);scroll-snap-align:start;border-radius:var(--r);overflow:hidden;background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}
.apps img{width:100%;aspect-ratio:4/3.4;object-fit:cover}
.apps .t{padding:22px 24px 26px}
.apps h3{font-size:28px;letter-spacing:-.03em}
.apps p{color:var(--soft);font-size:15px;margin-top:8px}
.apps .tags{display:flex;gap:6px;margin-top:14px;flex-wrap:wrap}
.apps .tags span{font-size:12px;padding:6px 12px;border-radius:999px;box-shadow:inset 0 0 0 1px var(--line)}
.buy{display:grid;gap:40px;padding:clamp(28px,5vw,64px);border-radius:clamp(28px,4vw,52px);background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}
@media(min-width:1000px){.buy{grid-template-columns:1fr 1fr;align-items:center}}
.buy .swap{aspect-ratio:1}
.buy .swap img{width:100%;height:100%;object-fit:cover;border-radius:26px}
html[data-kleur=wit] .buy .swap img{mix-blend-mode:multiply}
.pr{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:26px 0 6px}
.pr b{font-size:clamp(56px,7vw,96px);letter-spacing:-.06em;line-height:1}
.pr span{color:var(--soft);font-size:15px}
.ship{font-size:14px;color:var(--soft);margin:10px 0 26px}
.end{text-align:center;padding:clamp(90px,13vw,170px) 0}
.end .h2{max-width:12em;margin:20px auto 26px}
.mbar{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:80;display:flex;align-items:center;gap:12px;padding:10px 10px 10px 18px;border-radius:999px;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);box-shadow:inset 0 0 0 1px var(--line),0 20px 50px -20px rgba(0,0,0,.4);transform:translateY(140%);transition:transform .7s var(--ease),background-color .9s}
.mbar.show{transform:none}
.mbar .t{flex:1;min-width:0;font-size:13px;line-height:1.25}
.mbar .t b{display:block;font-size:15px}
.mbar .btn{padding:14px 20px}
@media(min-width:1000px){.mbar{left:50%;right:auto;width:560px;translate:-50% 0}}
</style>'''


def index():
    probs = [("Warme klaslokalen", "Leerlingen en docenten presteren slechter in benauwde, warme ruimtes. Hitte gaat ten koste van concentratie."),
             ("Benauwde kantoren", "Stilstaande lucht in kantoren maakt werken zwaarder en drukt de productiviteit."),
             ("Slechte luchtcirculatie", "In grote open ruimtes hoopt warme lucht zich op aan het plafond terwijl werkplekken benauwd aanvoelen."),
             ("Losse ventilatoren", "Tafel- en staande ventilatoren passen niet in een professionele omgeving. Ze storen collega's."),
             ("Ruimte op de vloer", "Staande ventilatoren blokkeren loopruimte, zorgen voor struikelgevaar en zijn onveilig in scholen en kinderopvang."),
             ("Kabels en rommel", "Snoeren over de vloer zijn gevaarlijk en onrustig. Ze horen niet in een werk- of leeromgeving.")]
    probs_html = ''.join(f'<article class="rv d{i % 3}"><div class="n">0{i + 1}</div><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(probs))
    apps = [("school", "Scholen", "Frisse lucht helpt leerlingen focussen. Veilig, stil en onopvallend in klaslokalen en aula's.", ["Klaslokalen", "Aula's"]),
            ("kinderopvang", "Kinderopvang", "Ventilatie op hoogte, buiten bereik van kinderen. Stil genoeg tijdens slapen en spelen.", ["Speelruimtes", "Slaapkamers"]),
            ("kantoor", "Kantoren", "Prettiger werken in een aangename ruimte. Ceilingflow valt weg in het plafond.", ["Open kantoren", "Werkplekken"]),
            ("school-2", "Zorg en praktijken", "Stille luchtcirculatie voor klinieken, wachtkamers en behandelruimtes, zonder renovatie.", ["Wachtkamers", "Behandelkamers"]),
            ("showroom", "Showrooms", "Ook in showrooms en winkels past Ceilingflow strak in het systeemplafond.", ["Showrooms", "Winkels"]),
            ("showroom-2", "Vergaderruimtes", "Houd vergaderingen fris. Stil genoeg voor elke bespreking of presentatie.", ["Boardrooms", "Spreekkamers"])]
    apps_html = ''.join(f'<article class="rv"><img src="/img/{i}.webp" alt="Ceilingflow in een systeemplafond: {t.lower()}" loading="lazy"><div class="t"><h3>{t}</h3><p>{p}</p><div class="tags">{"".join(f"<span>{x}</span>" for x in tg)}</div></div></article>' for i, t, p, tg in apps)
    sectors = ''.join(f'<span>{s}</span>' for s in ["Scholen", "Kinderopvang", "Zorg", "Kantoren", "Vergaderruimtes", "Praktijkruimtes", "Showrooms"] * 2)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}, ensure_ascii=False)
    extra = INDEX_CSS + f'<script type="application/ld+json">{product_ld()}</script><script type="application/ld+json">{faq_ld}</script>'
    extra += '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Ceilingflow","url":"https://ceilingflow.nl/","email":"' + MAIL + '","telephone":"' + PHONE + '"}</script>'
    h = head('Ceilingflow · Plafondventilator voor 60x60 systeemplafond', 'Ceilingflow is de stille plafondventilator voor 60x60 systeemplafonds in scholen, kinderopvang, zorg en kantoren. €299 excl. btw, in Wit en Zwart, installatie in minder dan 5 minuten.', '/', extra)
    body = nav() + f'''
<main>
<section class="hero"><div class="wrap">
  <div>
    <span class="eyebrow rv">Plafondventilator voor 60×60 systeemplafonds</span>
    <h1 class="rv d1">Frisse lucht.<br>Uit het <em>plafond</em>.</h1>
    <p class="lead rv d2">Ceilingflow past strak in je 60×60 systeemplafond. Voor scholen, kinderopvang, zorg en kantoren. Geen losse ventilatoren, geen kabels op de vloer.</p>
    <div class="row rv d3">{kleur_toggle()}<a class="btn acc" href="/ventilator/">Bekijk de ventilator</a><a class="btn ghost" href="#offerte">Offerte voor meerdere lokalen</a></div>
  </div>
  <div class="stage rv" id="stage">
    <div class="grid"></div>
    <div class="swap"><img class="w" src="/img/wit.webp" alt="Ceilingflow plafondventilator in wit" fetchpriority="high"><img class="z" src="/img/zwart.webp" alt="Ceilingflow plafondventilator in zwart"></div>
    <div class="chips"><div><b>&lt; 35 dB</b><span>Fluisterstil</span></div><div><b>&lt; 5 min</b><span>Installatie</span></div><div><b>60×60</b><span>Systeemplafond</span></div><div><b>IP44</b><span>Bescherming</span></div></div>
  </div>
</div>
<div class="marq" aria-hidden="true"><div>{sectors}</div></div>
</section>

<section class="sec" id="probleem"><div class="wrap">
  <span class="eyebrow rv">Herkenbaar?</span>
  <h2 class="h2 rv d1" style="margin-top:20px">Ventilatie&shy;problemen die<br>iedereen <em>kent</em>.</h2>
  <div class="probs">{probs_html}</div>
</div></section>

<section class="sec" id="oplossing" style="padding-top:0"><div class="wrap sol">
  <div>
    <span class="eyebrow rv">De oplossing</span>
    <h2 class="h2 rv d1" style="margin-top:20px">Ventilatie die<br><em>erbij hoort</em>.</h2>
    <p class="lead rv d2" style="margin-top:24px">Ceilingflow zorgt voor comfortabele luchtverplaatsing zonder gedoe. Strak, stil en professioneel.</p>
    <ul>
      <li class="rv">Naadloos geïntegreerd in je bestaande systeemplafond</li>
      <li class="rv">Stille werking, geen hinder tijdens vergaderingen of lessen</li>
      <li class="rv">Snelle installatie: minder dan 5 minuten per unit</li>
      <li class="rv">Veilig: geen bewegende delen op ooghoogte</li>
      <li class="rv">Afstandsbediening voor snelheid, richting en timer</li>
      <li class="rv">Koelt in de zomer, verdeelt warmte in de winter</li>
    </ul>
  </div>
  <div class="stats">
    <div class="rv"><b>60×60</b><span>Standaard systeemplafond</span></div>
    <div class="rv d1"><b>&lt;35 dB</b><span>Geluidsniveau</span></div>
    <div class="rv d2"><b>&lt;5 min</b><span>Plug &amp; play installatie</span></div>
    <div class="rv d3"><b>IP44</b><span>Borstelloze motor, laag verbruik</span></div>
  </div>
</div></section>

<section class="sec" id="installatie" style="padding-top:0"><div class="wrap">
  <span class="eyebrow rv">Installatie</span>
  <h2 class="h2 rv d1" style="margin-top:20px">In een paar<br>minuten <em>klaar</em>.</h2>
  <div class="vid rv"><video controls playsinline preload="none" poster="/img/installatie-poster.webp"><source src="/img/installatie.mp4" type="video/mp4"></video></div>
  <div class="steps"><div class="rv"><b>01</b><p>Plafondtegel eruit</p></div><div class="rv d1"><b>02</b><p>Ceilingflow erin</p></div><div class="rv d2"><b>03</b><p>Stekker in het stopcontact</p></div></div>
</div></section>

<section class="sec" id="toepassingen" style="padding-top:0"><div class="wrap">
  <span class="eyebrow rv">Toepassingen</span>
  <h2 class="h2 rv d1" style="margin-top:20px">Werkt overal waar<br>een <em>systeemplafond</em> hangt.</h2>
  <div class="apps">{apps_html}</div>
</div></section>

<section class="sec" id="product" style="padding-top:0"><div class="wrap">
  <div class="buy">
    <div class="swap rv"><img class="w" src="/img/wit-hoek.webp" alt="Ceilingflow wit schuin van onderen" loading="lazy"><img class="z" src="/img/zwart-hoek.webp" alt="Ceilingflow zwart schuin van onderen" loading="lazy"></div>
    <div>
      <span class="eyebrow rv">Ceilingflow Ventilatie Unit</span>
      <h2 class="h2 rv d1" style="margin-top:20px;font-size:clamp(40px,5.6vw,80px)">Kies je kleur.<br>De site kleurt <em>mee</em>.</h2>
      <div class="pr rv d2"><b>€299</b><span>excl. btw · €361,79 incl. btw</span></div>
      <p class="ship rv d2">Verzending per bestelling: NL €9,50 · BE €18,50 · DE €24,50 · overig EU €34,50 · levering vanaf 25 oktober</p>
      <div class="rv d3" style="display:flex;flex-wrap:wrap;gap:12px">{kleur_toggle()}<a class="btn acc" href="/ventilator/" id="buyLink">Bestel <span data-kleur-naam>Wit</span></a></div>
    </div>
  </div>
</div></section>

{offerte()}
{faq_block(FAQ)}

<section class="end"><div class="wrap">
  <span class="eyebrow rv">Ceilingflow</span>
  <h2 class="h2 rv d1">Maak iedere werk- of leeromgeving <em>comfortabeler</em>.</h2>
  <p class="lead rv d2" style="margin:0 auto 30px">Bestel vandaag. Levering van beide kleuren volgt vanaf 25 oktober.</p>
  <div class="rv d3" style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn acc" href="/ventilator/">Bestel Ceilingflow · €299 excl. btw</a><a class="btn ghost" href="#offerte">Zakelijke offerte</a></div>
</div></section>
</main>

<div class="mbar" id="mbar"><div class="t"><b>Ceilingflow · <span data-kleur-naam>Wit</span></b>€299 excl. btw · €361,79 incl.</div><a class="btn acc" href="/ventilator/">Bestel</a></div>
''' + footer() + '''<script>
const stage = document.getElementById('stage');
function sp(){ const r = stage.getBoundingClientRect(), h = innerHeight; const p = Math.min(1, Math.max(0, (h * .35 - r.top) / (r.height + h * .2))); stage.style.setProperty('--p', p.toFixed(3)); }
addEventListener('scroll', sp, {passive:true}); sp();
const mbar = document.getElementById('mbar');
new IntersectionObserver(([e]) => mbar.classList.toggle('show', !e.isIntersecting && e.boundingClientRect.top < 0)).observe(document.querySelector('.hero .row'));
document.addEventListener('cf:kleur', e => { const b = document.getElementById('buyLink'); if (b) b.href = '/ventilator/?kleur=' + e.detail; });
document.getElementById('buyLink').href = '/ventilator/?kleur=' + document.documentElement.dataset.kleur;
</script>
</body>
</html>
'''
    return h + body


PDP_CSS = '''<style>
.pdp{display:grid;gap:34px;padding:24px 0 90px}
@media(min-width:1000px){.pdp{grid-template-columns:1.15fr 1fr;gap:64px;padding:40px 0 120px;align-items:start}}
.gal{position:relative;min-width:0}
@media(min-width:1000px){.gal{position:sticky;top:96px}}
.slides{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;border-radius:32px;scrollbar-width:none}
.slides::-webkit-scrollbar{display:none}
.slide{flex:0 0 100%;aspect-ratio:1;scroll-snap-align:center;overflow:hidden;background:radial-gradient(120% 90% at 50% 0%,color-mix(in srgb,var(--ink) 7%,var(--bg)),var(--bg2));transition:background .9s}
.slide img{width:100%;height:100%}
.slide img.cut{object-fit:cover;background:#fff}
.slide img.cover{object-fit:cover}
.gnav{display:flex;gap:10px;margin-top:12px;overflow-x:auto;scrollbar-width:none;padding-bottom:4px}
.gnav::-webkit-scrollbar{display:none}
.gnav button{flex:0 0 70px;height:70px;border-radius:16px;border:0;padding:0;overflow:hidden;cursor:pointer;background:var(--bg2);box-shadow:inset 0 0 0 1px var(--line);opacity:.55;transition:opacity .3s,box-shadow .3s}
.gnav button[aria-current=true]{opacity:1;box-shadow:inset 0 0 0 2px var(--ink)}
.gnav img{width:100%;height:100%;object-fit:cover}
.gnav img.c{object-fit:cover}
.info h1{font-size:clamp(46px,5.6vw,84px);margin:14px 0 12px}
.info h1 em{font-style:normal;color:var(--acc)}
.crumb{font-size:13px;color:var(--soft)}
.crumb a{text-decoration:underline;text-underline-offset:3px}
.price{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:24px 0 6px}
.price b{font-size:58px;letter-spacing:-.06em;line-height:1}
.price span{font-size:14px;color:var(--soft)}
.lbl{display:flex;justify-content:space-between;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:28px 0 12px}
.lbl em{font-style:normal;font-weight:500;text-transform:none;letter-spacing:0;color:var(--soft)}
.info .kleur{display:flex}
.info .kleur button{flex:1;justify-content:center;padding:14px}
.qrow{display:flex;gap:12px;margin-top:26px;flex-wrap:wrap}
.qty{display:inline-flex;align-items:center;border-radius:999px;box-shadow:inset 0 0 0 1px var(--line);background:var(--card)}
.qty button{width:50px;height:58px;border:0;background:none;cursor:pointer;font-size:20px}
.qty input{width:44px;border:0;background:none;text-align:center;font-weight:600;font-size:17px;-moz-appearance:textfield}
.qty input::-webkit-outer-spin-button,.qty input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.qrow .btn{flex:1 1 200px}
.tot{font-size:14px;color:var(--soft);margin-top:14px}
.tot b{color:var(--ink)}
.alt{display:block;text-align:center;margin-top:14px;font-size:14px;font-weight:600;text-decoration:underline;text-underline-offset:4px;cursor:pointer;background:none;border:0;width:100%}
.eta{display:flex;gap:12px;align-items:center;margin-top:22px;padding:16px 18px;border-radius:18px;background:var(--card);box-shadow:inset 0 0 0 1px var(--line);font-size:14px}
.eta .dot{width:9px;height:9px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 5px color-mix(in srgb,var(--acc) 22%,transparent);flex:0 0 auto}
.usps{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.usps div{padding:14px 16px;border-radius:16px;background:var(--card);box-shadow:inset 0 0 0 1px var(--line);font-size:13px;line-height:1.35;color:var(--soft)}
.usps b{display:block;font-size:14px;color:var(--ink)}
.acc{margin-top:30px;border-top:1px solid var(--line)}
.why{padding:clamp(80px,12vw,150px) 0}
.feat{display:grid;gap:12px;margin-top:46px}
@media(min-width:700px){.feat{grid-template-columns:1fr 1fr}}
@media(min-width:1100px){.feat{grid-template-columns:repeat(3,1fr)}}
.feat article{padding:28px;border-radius:var(--r);background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}
.feat h3{font-size:26px;letter-spacing:-.03em;margin-bottom:10px;line-height:1.05}
.feat p{color:var(--soft);font-size:15px}
.about{display:grid;gap:30px;padding-bottom:clamp(80px,12vw,150px)}
@media(min-width:1000px){.about{grid-template-columns:1fr 1fr;gap:70px;align-items:center}}
.about img{border-radius:var(--r);width:100%;aspect-ratio:4/3;object-fit:cover}
.about p{color:var(--soft);margin-top:16px;font-size:17px}
.mbar{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:80;display:flex;align-items:center;gap:12px;padding:10px 10px 10px 18px;border-radius:999px;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);box-shadow:inset 0 0 0 1px var(--line),0 20px 50px -20px rgba(0,0,0,.4);transform:translateY(140%);transition:transform .7s var(--ease),background-color .9s}
.mbar.show{transform:none}
.mbar .t{flex:1;min-width:0;font-size:13px;line-height:1.25}
.mbar .t b{display:block;font-size:15px}
.mbar .btn{padding:14px 20px}
@media(min-width:1000px){.mbar{left:50%;right:auto;width:580px;translate:-50% 0}}
</style>'''


def pdp():
    specs = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in SPECS)
    feats = [("Plug &amp; play", "Plafondtegel eruit, Ceilingflow erin, stekker in het stopcontact. Klaar."),
             ("Fluisterstil", "Geluidsniveau onder 35 dB. Je merkt het niet in kantoren, scholen en zorginstellingen."),
             ("Past in 60×60", "Naadloze integratie in standaard systeemplafonds. Geen ingrijpende installatie."),
             ("Afstandsbediening", "Inbegrepen. Snelheid, richting en timer regel je vanaf elke werkplek."),
             ("Energiezuinig", "Borstelloze motor, recyclebaar ABS, RoHS- en CE-gecertificeerd."),
             ("Het hele jaar door", "Koeling in de zomer, betere warmteverdeling in de winter. Eén unit, twee functies.")]
    feats_html = ''.join(f'<article class="rv d{i % 3}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(feats))
    extra = PDP_CSS + f'<script type="application/ld+json">{product_ld()}</script>'
    extra += '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ceilingflow.nl/"},{"@type":"ListItem","position":2,"name":"Ceilingflow Ventilatie Unit","item":"https://ceilingflow.nl/ventilator/"}]}</script>'
    h = head('Ceilingflow Ventilatie Unit · €299 excl. btw · Wit of Zwart', 'Bestel de Ceilingflow plafondventilator voor 60x60 systeemplafonds. €299 excl. btw (€361,79 incl.), Wit of Zwart, onder 35 dB, afstandsbediening inbegrepen.', '/ventilator/', extra)
    body = nav(False) + f'''
<main class="wrap">
<div class="pdp" id="buy">
  <div class="gal">
    <div class="slides" id="slides"></div>
    <div class="gnav" id="gnav"></div>
  </div>
  <div class="info">
    <div class="crumb"><a href="/">Home</a> / Ventilator</div>
    <h1>Ceilingflow <em>Ventilatie Unit</em></h1>
    <p class="crumb">SKU CF-6060-001 · Past naadloos in een standaard 60×60 systeemplafond</p>
    <div class="price"><b>€299</b><span>excl. btw · €361,79 incl. btw · excl. verzending</span></div>
    <div class="lbl">Kleur <em data-kleur-naam>Wit</em></div>
    {kleur_toggle()}
    <div class="lbl">Aantal units <em>Meer dan 10? Vraag een offerte</em></div>
    <div class="qrow">
      <div class="qty"><button type="button" id="qm" aria-label="Minder">−</button><input id="q" type="number" min="1" max="99" value="1" inputmode="numeric" aria-label="Aantal"><button type="button" id="qp" aria-label="Meer">+</button></div>
      <button class="btn acc" type="button" id="addBtn" data-koop-label>In winkelmandje</button>
    </div>
    <p class="tot" id="tot"></p>
    <button class="alt" type="button" data-offerte-knop>Zakelijke offerte voor meerdere lokalen</button>
    <div class="eta"><span class="dot"></span><span>Levering van <span data-kleur-naam>Wit</span> vanaf 25 oktober · bestellen blijft mogelijk</span></div>
    <div class="usps">
      <div><b>NL €9,50</b>verzending per bestelling</div>
      <div><b>BE €18,50 · DE €24,50</b>overig EU €34,50 · per bestelling</div>
      <div><b>Btw-factuur</b>KvK en btw-nummer op te geven</div>
      <div><b>Afstandsbediening</b>inbegrepen</div>
    </div>
    <div class="acc">
      <details id="specs" open><summary>Specificaties</summary><div class="a"><dl class="specs">{specs}</dl></div></details>
      <details><summary>Verzending en levering</summary><div class="a"><p>Verzending per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50, Duitsland en de rest van West-Europa €24,50, overige EU-landen €34,50. Buiten Europa leveren we alleen op aanvraag via het offerteformulier.</p><p>Levering van beide kleuren volgt vanaf 25 oktober. Verzendkosten worden in de checkout berekend.</p></div></details>
      <details><summary>Retour</summary><div class="a"><p>Vragen over retourneren? Neem contact op via <a href="mailto:{MAIL}" style="text-decoration:underline">{MAIL}</a> of bel {PHONE}. Dan kijken we samen naar je situatie.</p></div></details>
      <details><summary>Montage</summary><div class="a"><p>Ceilingflow plaats je in het bestaande 60×60 plafondrooster, net als een verlichtingsarmatuur. Plafondtegel eruit, Ceilingflow erin, stekker in het stopcontact.</p><p>Gemiddeld minder dan 5 minuten per unit. Geen bouwkundige aanpassingen of speciaal gereedschap nodig. Onderhoud: de luchtinlaat een paar keer per jaar reinigen.</p></div></details>
    </div>
  </div>
</div>
</main>

<section class="why"><div class="wrap">
  <span class="eyebrow rv">Waarom Ceilingflow</span>
  <h2 class="h2 rv d1" style="margin-top:20px">Een aangenaam<br>binnenklimaat, <em>elk seizoen</em>.</h2>
  <div class="feat">{feats_html}</div>
</div></section>

<section><div class="wrap about">
  <img class="rv" src="/img/kantoor.webp" alt="Ceilingflow in het systeemplafond van een kantoor" loading="lazy">
  <div class="rv d1">
    <span class="eyebrow">Over Ceilingflow</span>
    <h2 class="h2" style="margin-top:20px;font-size:clamp(38px,5vw,72px)">Nieuw op de<br>Nederlandse <em>markt</em>.</h2>
    <p>Een comfortabel binnenklimaat maakt werken prettiger. Op warme dagen koelt Ceilingflow door luchtcirculatie. Op koudere dagen benut je de warmte van je verwarming beter, omdat warme lucht niet aan het plafond blijft hangen.</p>
    <p>Door het lage geluidsniveau, het lage stroomverbruik, de instelbare snelheid en de plug &amp; play installatie is Ceilingflow geschikt voor kantoren, werkplaatsen, showrooms, winkels, scholen, horecakeukens, vergaderzalen en serverruimtes.</p>
  </div>
</div></section>

{offerte('Offerte voor meerdere lokalen')}
{faq_block([FAQ[i] for i in (0, 1, 5, 6, 9, 10)])}

<div class="mbar" id="mbar"><div class="t"><b>Ceilingflow · <span data-kleur-naam>Wit</span></b><span id="mTot">€299 excl. btw</span></div><button class="btn acc" type="button" id="mAdd" data-koop-label>In mandje</button></div>
''' + footer() + '''<script>
const $ = s => document.querySelector(s), root = document.documentElement;
const G = {
  wit: [['cut','wit','Ceilingflow wit van onderen'],['cut','wit-hoek','Ceilingflow wit schuin'],['cut','wit-2','Ceilingflow wit met stekker'],['cover','school','Ceilingflow wit in een klaslokaal'],['cover','kinderopvang','Ceilingflow in de kinderopvang'],['cover','kantoor','Ceilingflow in een kantoor']],
  zwart: [['cut','zwart','Ceilingflow zwart met afstandsbediening'],['cut','zwart-hoek','Ceilingflow zwart schuin'],['cut','zwart-2','Ceilingflow zwart van opzij'],['cover','showroom','Ceilingflow zwart in een showroom'],['cover','showroom-2','Ceilingflow in een showroom met zwart plafond']]
};
const slides = $('#slides'), gnav = $('#gnav');
function gallery(k){
  const g = G[k];
  slides.innerHTML = g.map((s, i) => `<div class="slide"><img class="${s[0]}" src="/img/${s[1]}.webp" alt="${s[2]}" ${i ? 'loading="lazy"' : 'fetchpriority="high"'}></div>`).join('');
  gnav.innerHTML = g.map((s, i) => `<button type="button" aria-label="Foto ${i + 1}" aria-current="${i === 0}"><img class="${s[0] === 'cut' ? 'c' : ''}" src="/img/${s[1]}.webp" alt="" loading="lazy"></button>`).join('');
  slides.scrollLeft = 0;
}
gnav.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; slides.scrollTo({left: [...gnav.children].indexOf(b) * slides.clientWidth, behavior: 'smooth'}); });
slides.addEventListener('scroll', () => { const i = Math.round(slides.scrollLeft / slides.clientWidth); [...gnav.children].forEach((b, j) => b.setAttribute('aria-current', j === i)); }, {passive: true});
const qi = $('#q'); let q = 1;
function upd(){ q = Math.max(1, Math.min(99, parseInt(qi.value) || 1)); qi.value = q;
  $('#tot').innerHTML = `Totaal <b>${CF.eur(299 * q)}</b> excl. btw · ${CF.eur(361.79 * q)} incl. btw${q > 1 ? ` · ${q} units` : ''}`;
  $('#mTot').textContent = `${CF.eur(299 * q)} excl. btw${q > 1 ? ` · ${q}×` : ''}`; }
$('#qm').onclick = () => { qi.value = q - 1; upd(); };
$('#qp').onclick = () => { qi.value = q + 1; upd(); };
qi.addEventListener('change', upd);
function doAdd(){ const k = root.dataset.kleur; CF.add(k, q); if (CF.READY) { const t = $('#toast'); t.textContent = `${q}× Ceilingflow ${k === 'zwart' ? 'Zwart' : 'Wit'} toegevoegd`; t.classList.add('on'); setTimeout(() => t.classList.remove('on'), 2200); } }
$('#addBtn').onclick = doAdd; $('#mAdd').onclick = doAdd;
document.addEventListener('cf:kleur', e => { gallery(e.detail); history.replaceState(null, '', '?kleur=' + e.detail); });
gallery(root.dataset.kleur); upd();
const mbar = $('#mbar');
new IntersectionObserver(([e]) => mbar.classList.toggle('show', !e.isIntersecting && e.boundingClientRect.top < 0)).observe($('#addBtn'));
</script>
</body>
</html>
'''
    return h + body


def simple(title, path, h1, text):
    return head(title, text, path, '<meta name="robots" content="noindex">') + nav(False) + f'''
<main class="wrap" style="padding:clamp(90px,14vw,180px) 0;min-height:60vh">
  <span class="eyebrow">Ceilingflow</span>
  <h1 class="h2" style="margin:20px 0 24px">{h1}</h1>
  <p class="lead">{text}</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:30px"><a class="btn acc" href="/ventilator/">Bekijk de ventilator</a><a class="btn ghost" href="/">Naar home</a></div>
</main>
''' + footer() + '</body>\n</html>\n'


def main():
    (ROOT / 'index.html').write_text(index())
    (ROOT / 'ventilator').mkdir(exist_ok=True)
    (ROOT / 'ventilator/index.html').write_text(pdp())
    (ROOT / 'bedankt').mkdir(exist_ok=True)
    (ROOT / 'bedankt/index.html').write_text(simple('Bedankt · Ceilingflow', '/bedankt/', 'Bedankt voor je <em>aanvraag</em>.', 'We hebben je offerteaanvraag ontvangen en reageren binnen één werkdag.'))
    (ROOT / '404.html').write_text(simple('Pagina niet gevonden · Ceilingflow', '/404.html', 'Deze pagina <em>bestaat niet</em>.', 'De pagina die je zoekt is verplaatst of bestaat niet meer.'))
    (ROOT / 'sitemap.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>{URL}/ventilator/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>
</urlset>
''')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /bedankt/\n\nSitemap: {URL}/sitemap.xml\n')
    (ROOT / 'CNAME').write_text('ceilingflow.nl\n')
    print('klaar')


if __name__ == '__main__':
    main()
