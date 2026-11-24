#!/usr/bin/env python3
"""Bouwt de statische Ceilingflow-site: index, /ventilator/, /bedankt/, 404, sitemap en robots."""
import json, pathlib, hashlib
from datetime import date

ROOT = pathlib.Path(__file__).parent
URL = 'https://ceilingflow.nl'
PHONE = '+31 6 34 33 38 09'
MAIL = 'nick@gnc-systems.com'
INDEXNOW_KEY = '80b241ecbc03c31a2ef300d09e441a73'
LASTMOD = ROOT / '.lastmod.json'  # pad -> hash + datum; lastmod verspringt alleen als een pagina echt verandert (Jekyll serveert dotfiles niet)
ORG = {"@type": "Organization", "@id": "https://ceilingflow.nl/#org", "name": "Ceilingflow", "url": "https://ceilingflow.nl/", "logo": "https://ceilingflow.nl/img/logo.png",
       "email": "nick@gnc-systems.com", "telephone": "+31634333809", "sameAs": ["https://www.linkedin.com/company/ceilingflow/"],
       "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+31634333809", "email": "nick@gnc-systems.com", "availableLanguage": "nl"}}
WEBSITE = {"@type": "WebSite", "@id": "https://ceilingflow.nl/#website", "name": "Ceilingflow", "url": "https://ceilingflow.nl/", "inLanguage": "nl", "publisher": {"@id": "https://ceilingflow.nl/#org"}}
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">'
ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 rx=%2214%22 fill=%22%230d0f10%22/%3E%3Ccircle cx=%2232%22 cy=%2232%22 r=%2218%22 fill=%22none%22 stroke=%22%23ff5a1f%22 stroke-width=%225%22/%3E%3Ccircle cx=%2232%22 cy=%2232%22 r=%225%22 fill=%22%23eef0ee%22/%3E%3C/svg%3E">'
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="1.5" y="1.5" width="29" height="29" rx="7" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="16" cy="16" r="8.5" fill="none" stroke="#ff5a1f" stroke-width="2.6"/><circle cx="16" cy="16" r="2.6" fill="currentColor"/></svg>'

FAQ = [
    ("Past Ceilingflow in ieder systeemplafond?", "Ceilingflow is ontworpen voor het standaard 60×60 cm systeemplafond. Dat is het meest gebruikte formaat in kantoren, scholen, zorginstellingen en andere professionele omgevingen. Heb je een afwijkend formaat? Neem dan contact op voor advies."),
    ("Is Ceilingflow een lamp of verlichtingsarmatuur?", "Nee. Ceilingflow is geen lamp. Het is een ventilatie-oplossing voor het 60×60 systeemplafond die zorgt voor luchtcirculatie, niet voor verlichting. Je plaatst Ceilingflow naast je bestaande verlichting."),
    ("Is Ceilingflow geschikt voor scholen en klaslokalen?", "Ja. De stille werking stoort niet tijdens lessen of toetsen. De geïntegreerde montage is veilig voor kinderen en de strakke uitstraling past in iedere schoolomgeving."),
    ("Kan ik meerdere units bestellen?", "Ja, je bestelt eenvoudig meerdere units. Na je bestelling mailen we je de leverdatum. Voor grotere aantallen of maatwerk vraag je een zakelijke offerte aan, dan denken we mee over de beste oplossing voor jouw situatie."),
    ("Kan ik een zakelijke factuur ontvangen?", "Ja. Je ontvangt altijd een btw-factuur bij je bestelling. Je kunt je KvK-nummer en btw-nummer opgeven bij het bestellen."),
    ("Hoe werkt de verzending?", "De prijs is €299 excl. btw (€361,79 incl. btw), exclusief verzendkosten. Verzending kost per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50, Duitsland en de rest van West-Europa €24,50, overige EU-landen €34,50. Buiten Europa leveren we alleen op aanvraag via het offerteformulier. Bestellen kan direct: na je bestelling mailen we je de leverdatum."),
    ("Is de installatie moeilijk?", "Nee. Ceilingflow plaats je in het bestaande 60×60 plafondrooster, net als een verlichtingsarmatuur. Installatie duurt gemiddeld minder dan 5 minuten per unit. Er zijn geen bouwkundige aanpassingen of speciaal gereedschap nodig."),
    ("Is er een speciale prijs voor meerdere units?", "Bij afname van meerdere units vraag je een zakelijke offerte aan. We maken een offerte op maat. Gebruik het offerteformulier of bel ons direct."),
    ("Kan ik een offerte aanvragen?", "Ja, via het offerteformulier op deze site. Geef het gewenste aantal units, de locatie en je contactgegevens op. Je krijgt binnen één werkdag een offerte op maat."),
    ("Hoe stil is Ceilingflow tijdens gebruik?", "Op de laagste stand werkt Ceilingflow op 35 dB(A), vergelijkbaar met een zachte fluisterstem. Geschikt tijdens vergaderingen, lessen, behandelingen en in slaapruimtes van de kinderopvang. Op de hoogste stand is het 47 dB(A): die hoor je wel, bedoeld voor warme middagen. De stand kies je zelf met de afstandsbediening."),
    ("Wat kost Ceilingflow aan stroom?", "Weinig. Op de laagste stand gebruikt hij 27 W, op de hoogste 41 W. Een werkdag van 8 uur op de hoogste stand is ongeveer 0,33 kWh. Vermenigvuldig dat met je eigen stroomtarief en je weet wat een unit per dag kost. Hij gaat in het stopcontact (220 tot 230 V), een aparte groep is niet nodig."),
    ("Kan hij in de winter uit tot het voorjaar?", "Laat hem liever aan op de laagste stand. Warme lucht van de verwarming stijgt naar het plafond; op de laagste stand brengt Ceilingflow die warmte terug naar werkhoogte zonder dat je een koele luchtstroom voelt. Hoe hoger de ruimte, hoe groter het effect. Meer uitleg staat op ceilingflow.nl/winter/."),
    ("Heeft Ceilingflow veel onderhoud nodig?", "Het onderhoud is minimaal. De luchtinlaat een paar keer per jaar reinigen is genoeg. Er zijn geen slijtende onderdelen die regelmatig vervangen moeten worden."),
]

SPECS = [("Formaat", "60 × 60 cm"), ("Geluidsniveau", "35 tot 47 dB(A)"), ("Vermogen", "27 tot 41 W"), ("Installatietijd", "< 5 minuten"), ("Bescherming", "IP44"),
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
<script defer src="https://stats.1v1battles.com/nv.js" data-website-id="1ebd27a4-63bb-4b8e-ae21-0f3f4cb14564"></script>
{extra}
</head>
<body>
'''


def nav(home=True):
    p = '' if home else '/'
    return f'''<div class="topbar">Beide kleuren direct te bestellen · leverdatum volgt per mail</div>
<nav class="main"><div class="wrap">
  <a class="logo" href="/" aria-label="Ceilingflow home">{LOGO}<span>Ceiling<i>flow</i></span></a>
  <div class="navl"><a href="{p}#oplossing">Oplossing</a><a href="{p}#toepassingen">Toepassingen</a><a href="/ventilator/">Ventilator</a><a href="/luchtreiniger/">Luchtreiniger</a><a href="{p}#offerte">Zakelijk</a><a href="{p}#faq">FAQ</a></div>
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
  <div><h4>Product</h4><ul><li><a href="/ventilator/">Ceilingflow Ventilatie Unit</a></li><li><a href="/ventilator/#specs">Specificaties</a></li><li><a href="/#installatie">Installatie</a></li><li><a href="/scholen/">Voor scholen</a></li><li><a href="/kinderopvang/">Voor kinderopvang</a></li><li><a href="/kantoor/">Voor kantoren en praktijken</a></li><li><a href="/winter/">Plafondventilator in de winter</a></li><li><a href="/luchtreiniger/">Luchtreiniger H13 HEPA</a></li></ul></div>
  <div><h4>Zakelijk</h4><ul><li><a href="/#offerte">Offerte aanvragen</a></li><li>Btw-factuur</li><li>Bulkbestellingen</li></ul></div>
  <div><h4>Contact</h4><ul><li><a href="/contact/">Contact</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="tel:+31634333809">{PHONE}</a></li><li><a href="/privacy/">Privacyverklaring</a></li></ul></div>
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
                    "availability": "https://schema.org/PreOrder", "itemCondition": "https://schema.org/NewCondition",
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
    extra += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [ORG, WEBSITE]}, ensure_ascii=False) + '</script>'
    h = head('Plafondventilator voor 60x60 systeemplafond · Ceilingflow', 'Stille plafondventilator voor 60x60 systeemplafonds in scholen, kinderopvang, zorg en kantoren. €299 excl. btw, Wit of Zwart, in minder dan 5 minuten geplaatst.', '/', extra)
    body = nav() + f'''
<main>
<section class="hero"><div class="wrap">
  <div>
    <span class="eyebrow rv">Plafondventilator voor 60×60 systeemplafonds</span>
    <h1 class="rv d1">Frisse lucht.<br>Uit het <em>plafond</em>.</h1>
    <p class="lead rv d2">Ceilingflow past strak in je 60×60 systeemplafond. Voor scholen, kinderopvang, zorg en kantoren. Geen losse ventilatoren, geen kabels op de vloer.</p>
    <div class="row rv d3">{kleur_toggle()}<a class="btn acc" href="/ventilator/">Bekijk de ventilator</a><a class="btn ghost" href="#offerte">Offerte voor meerdere lokalen</a></div>
    <p class="rv d3" style="margin-top:14px;font-size:.95rem"><a href="/scholen/#per-lokaal" data-umami-event="home-naar-scholen" style="text-decoration:underline">Voor scholen: prijs per lokaal</a> · <a href="/kinderopvang/#per-groep" data-umami-event="home-naar-kdv" style="text-decoration:underline">Voor kinderopvang: prijs per groep</a> · <a href="/kantoor/#per-ruimte" data-umami-event="home-naar-kantoor" style="text-decoration:underline">Voor kantoren: prijs per ruimte</a></p>
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
  <p class="rv" style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn ghost" href="/scholen/">Ceilingflow voor scholen</a><a class="btn ghost" href="/kinderopvang/">Ceilingflow voor kinderopvang</a><a class="btn ghost" href="/kantoor/">Ceilingflow voor kantoren</a><a class="btn ghost" href="/winter/">Plafondventilator in de winter</a></p>
</div></section>

<section class="sec" id="product" style="padding-top:0"><div class="wrap">
  <div class="buy">
    <div class="swap rv"><img class="w" src="/img/wit-hoek.webp" alt="Ceilingflow wit schuin van onderen" loading="lazy"><img class="z" src="/img/zwart-hoek.webp" alt="Ceilingflow zwart schuin van onderen" loading="lazy"></div>
    <div>
      <span class="eyebrow rv">Ceilingflow Ventilatie Unit</span>
      <h2 class="h2 rv d1" style="margin-top:20px;font-size:clamp(40px,5.6vw,80px)">Kies je kleur.<br>De site kleurt <em>mee</em>.</h2>
      <div class="pr rv d2"><b>€299</b><span>excl. btw · €361,79 incl. btw</span></div>
      <p class="ship rv d2">Verzending per bestelling: NL €9,50 · BE €18,50 · DE €24,50 · overig EU €34,50 · leverdatum per mail na bestelling</p>
      <div class="rv d3" style="display:flex;flex-wrap:wrap;gap:12px">{kleur_toggle()}<a class="btn acc" href="/ventilator/" id="buyLink">Bestel <span data-kleur-naam>Wit</span></a></div>
    </div>
  </div>
</div></section>

{offerte()}
{faq_block(FAQ)}

<section class="end"><div class="wrap">
  <span class="eyebrow rv">Ceilingflow</span>
  <h2 class="h2 rv d1">Maak iedere werk- of leeromgeving <em>comfortabeler</em>.</h2>
  <p class="lead rv d2" style="margin:0 auto 30px">Bestel vandaag. Na je bestelling mailen we je de leverdatum.</p>
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


LAMP_FAQ = [
    ("Kan Ceilingflow naast een LED-paneel hangen?", "Ja. Ceilingflow en LED-panelen hebben allebei het 60×60 formaat en passen in hetzelfde plafondrooster. Je vervangt een gewone plafondplaat door Ceilingflow en de verlichting blijft zoals hij is."),
    ("Verkopen jullie ook plafondventilatoren met lamp?", "Nee. Wij verkopen Ceilingflow voor het 60×60 systeemplafond en luchtreinigers. Voor een plafondventilator met lamp in de woonkamer of slaapkamer kun je beter bij een verlichtingswinkel terecht."),
]
LAMP_ROWS = [
    ("Verlichting", "Geen lamp. Je bestaande LED-panelen of armaturen blijven in het plafond zitten.", "Een lamp of LED-module zit in de ventilator zelf."),
    ("Plafond", "60×60 systeemplafond: de unit vervangt één plafondplaat.", "Een gewoon plafond met een lichtpunt of plafondhaak."),
    ("Aansluiting", "Stekker in een stopcontact boven het plafond, in minder dan 5 minuten geplaatst.", "Aangesloten op het lichtpunt in het plafond."),
    ("Bediening", "Afstandsbediening voor snelheid, richting en timer.", "Wandschakelaar, trekkoord of afstandsbediening, verschilt per model."),
    ("Bedoeld voor", "Klaslokalen, kinderopvang, kantoren en praktijkruimtes.", "Woonkamer, slaapkamer en andere ruimtes thuis."),
]
LAMP_CSS = """<style>
.lamp{padding:0 0 clamp(80px,12vw,150px)}
.lamp .lead{margin-top:22px;max-width:44em}
.lamp-t{margin-top:40px;border-radius:var(--r);background:var(--card);box-shadow:inset 0 0 0 1px var(--line);overflow-x:auto}
.lamp-t table{width:100%;border-collapse:collapse;min-width:620px;font-size:15px}
.lamp-t th,.lamp-t td{padding:16px 20px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
.lamp-t tr:last-child td{border-bottom:0}
.lamp-t th{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--soft);font-weight:600}
.lamp-t td:first-child{font-weight:600;white-space:nowrap}
.lamp-t td{color:var(--soft)}
.lamp-t td:nth-child(2){color:var(--ink)}
</style>"""


def lamp_html():
    """Zoekgat 'plafondventilator met lamp' (seo-gap 24 nov 2026): eerlijk antwoord, Ceilingflow heeft geen lamp."""
    rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in LAMP_ROWS)
    return f'''<section class="lamp" id="met-lamp"><div class="wrap">
  <span class="eyebrow rv">Met of zonder lamp</span>
  <h2 class="h2 rv d1" style="margin-top:20px;font-size:clamp(38px,5vw,72px)">Plafondventilator<br><em>met lamp?</em></h2>
  <p class="lead rv">Ceilingflow heeft geen lamp. De unit vervangt één plaat van 60×60 cm in het systeemplafond, zodat de LED-panelen of armaturen die er al hangen gewoon blijven zitten. Licht en luchtcirculatie blijven zo twee aparte toestellen. Zoek je een ventilator met lamp voor thuis, dan past een klassieke plafondventilator met schoepen en verlichting beter. Die verkopen wij niet.</p>
  <div class="lamp-t rv"><table><thead><tr><th></th><th>Ceilingflow</th><th>Plafondventilator met lamp</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>'''


def pdp():
    specs = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in SPECS)
    feats = [("Plug &amp; play", "Plafondtegel eruit, Ceilingflow erin, stekker in het stopcontact. Klaar."),
             ("Fluisterstil", "Geluidsniveau onder 35 dB. Je merkt het niet in kantoren, scholen en zorginstellingen."),
             ("Past in 60×60", "Naadloze integratie in standaard systeemplafonds. Geen ingrijpende installatie."),
             ("Afstandsbediening", "Inbegrepen. Snelheid, richting en timer regel je vanaf elke werkplek."),
             ("Energiezuinig", "Borstelloze motor, recyclebaar ABS, RoHS- en CE-gecertificeerd."),
             ("Het hele jaar door", "Koeling in de zomer, betere warmteverdeling in de winter. Eén unit, twee functies.")]
    feats_html = ''.join(f'<article class="rv d{i % 3}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(feats))
    pdp_faq = [FAQ[i] for i in (0, 1, 5, 6, 9, 10, 11, 12)] + LAMP_FAQ
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pdp_faq]}, ensure_ascii=False)
    extra = PDP_CSS + LAMP_CSS + f'<script type="application/ld+json">{product_ld()}</script><script type="application/ld+json">{faq_ld}</script>'
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
    <p style="margin-top:10px;font-size:.9rem;opacity:.85">Liever via bol.com bestellen? Ceilingflow Wit staat ook in onze eigen bol-winkel (Pegasus Depot). <a href="https://www.bol.com/nl/nl/p/pegasus-depot-ceilingflow-plafondventilator-595-x-595-mm-voor-systeemplafonds-plug-and-play-met-afstandsbediening-wit/9300000401948628/" target="_blank" rel="noopener" data-umami-event="bol-alternatief-klik" data-umami-event-plek="ventilator" style="text-decoration:underline">Bekijk op bol.com</a></p>
    <div class="eta"><span class="dot"></span><span>Ceilingflow <span data-kleur-naam>Wit</span> direct te bestellen · leverdatum per mail na bestelling</span></div>
    <div class="usps">
      <div><b>NL €9,50</b>verzending per bestelling</div>
      <div><b>BE €18,50 · DE €24,50</b>overig EU €34,50 · per bestelling</div>
      <div><b>Btw-factuur</b>KvK en btw-nummer op te geven</div>
      <div><b>Afstandsbediening</b>inbegrepen</div>
    </div>
    <div class="acc">
      <details id="specs" open><summary>Specificaties</summary><div class="a"><dl class="specs">{specs}</dl></div></details>
      <details><summary>Verzending en levering</summary><div class="a"><p>Verzending per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50, Duitsland en de rest van West-Europa €24,50, overige EU-landen €34,50. Buiten Europa leveren we alleen op aanvraag via het offerteformulier.</p><p>Na je bestelling mailen we je de leverdatum. Verzendkosten worden in de checkout berekend.</p></div></details>
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

{lamp_html()}

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
{faq_block(pdp_faq)}

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


SCHOOL_CSS = """<style>
.sh{padding:clamp(40px,6vw,80px) 0 0}
.sh .crumb{font-size:13px;color:var(--soft);margin-bottom:22px}
.sh .row{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.sh .hero-img{width:100%;aspect-ratio:16/8;object-fit:cover;border-radius:clamp(24px,4vw,44px);margin-top:clamp(36px,5vw,60px)}
@media(max-width:700px){.sh .hero-img{aspect-ratio:4/3.4}}
.sec2{padding:clamp(80px,11vw,140px) 0}
.vg{display:grid;gap:12px;margin-top:50px}
@media(min-width:700px){.vg{grid-template-columns:1fr 1fr}}
@media(min-width:1100px){.vg{grid-template-columns:repeat(3,1fr)}}
.vg article{padding:28px;border-radius:var(--r);background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}
.vg h3{font-size:24px;letter-spacing:-.03em;margin-bottom:10px}
.vg p,.soft{color:var(--soft);font-size:15px}
.eerlijk{display:grid;gap:30px;padding:clamp(28px,5vw,60px);border-radius:clamp(28px,4vw,52px);background:var(--inv);color:var(--invink)}
.eerlijk p{font-size:17px;opacity:.85}
.eerlijk p+p{margin-top:14px}
@media(min-width:1000px){.eerlijk{grid-template-columns:1fr 1.2fr;align-items:center}}
.kost{display:grid;gap:40px}
@media(min-width:1000px){.kost{grid-template-columns:1fr 1fr;align-items:center}}
.kost .soft{margin-top:14px}
.kost table{width:100%;border-collapse:collapse;font-size:17px}
.kost th{text-align:left;font-size:13px;color:var(--soft);font-weight:500;padding:0 0 12px}
.kost td{padding:16px 0;border-top:1px solid var(--line)}
.kost td+td,.kost th+th{text-align:right}
.st{display:grid;gap:12px;margin-top:24px}
@media(min-width:800px){.st{grid-template-columns:repeat(3,1fr)}}
.st div{padding:24px;border-radius:22px;box-shadow:inset 0 0 0 1px var(--line)}
.st b{font-size:46px;letter-spacing:-.05em;color:var(--acc);line-height:1}
.st p{margin-top:8px;font-weight:600;font-size:18px}
.st span{display:block;margin-top:6px;color:var(--soft);font-size:15px}
</style>"""

SCHOOL_FAQ = [
    ("Stoort Ceilingflow tijdens de les?", "Nee. Ceilingflow werkt onder 35 dB, vergelijkbaar met een zachte fluisterstem. Dat is stil genoeg voor lessen, toetsen en de slaapruimte van de kinderopvang."),
    ("Is een plafondventilator veilig in een klaslokaal?", "Ceilingflow zit in het systeemplafond, buiten bereik van leerlingen. Er staat niets op de vloer en er lopen geen snoeren door het lokaal, dus geen struikelgevaar. De unit is IP44, CE- en RoHS-gecertificeerd."),
    ("Ververst Ceilingflow de lucht of verlaagt hij CO2?", "Nee. Ceilingflow brengt de lucht in het lokaal in beweging, hij voert geen buitenlucht aan en verlaagt CO2 niet. Hij vervangt dus geen mechanische ventilatie of luchten via ramen, maar maakt een warm of benauwd lokaal wel aangenamer."),
    ("Moet de installateur of conciërge veel doen?", "Nee. Plafondtegel eruit, Ceilingflow in het 60×60 rooster, stekker in het stopcontact. Gemiddeld minder dan 5 minuten per unit, zonder bouwkundige aanpassingen of speciaal gereedschap. Er moet wel een stopcontact binnen bereik boven het plafond zitten."),
    ("Heeft Ceilingflow in de winter zin?", "Ja. Warme lucht van de verwarming blijft vaak onder het plafond hangen. Door de lucht rond te laten gaan, komt die warmte beter bij de tafels terecht. In de zomer koelt de luchtstroom zelf."),
    ("Kunnen we op factuur bestellen voor meerdere lokalen?", "Ja. Je ontvangt altijd een btw-factuur. Voor meerdere lokalen of locaties vraag je een zakelijke offerte aan, je krijgt binnen één werkdag een voorstel op maat."),
]


def scholen():
    voordelen = [("Fluisterstil", "Onder 35 dB. Geen geruis tijdens instructie, toetsen of stilwerken."),
                 ("Niets op de vloer", "Geen staande ventilator, geen snoer over de grond, geen struikelgevaar tussen de tafels."),
                 ("Buiten bereik", "De unit zit in het plafond. Leerlingen en peuters kunnen er niet aan zitten."),
                 ("Klaar in 5 minuten", "Plafondtegel eruit, unit erin, stekker erin. Geen bouwkundige aanpassingen."),
                 ("Zomer en winter", "Verkoeling door luchtstroom op warme dagen, warme lucht van het plafond naar beneden in het stookseizoen."),
                 ("Afstandsbediening", "Inbegrepen. De leerkracht regelt snelheid, richting en timer vanaf het bureau.")]
    v_html = ''.join(f'<article class="rv d{i % 3}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(voordelen))
    rows = ''.join(f'<tr><td>{n} {"unit" if n == 1 else "units"}</td><td>€{299 * n:,}'.replace(',', '.') + f'</td><td>€{361.79 * n:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + '</td></tr>' for n in (1, 5, 10, 20))
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in SCHOOL_FAQ]}, ensure_ascii=False)
    extra = SCHOOL_CSS + f'<script type="application/ld+json">{faq_ld}</script>'
    extra += '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ceilingflow.nl/"},{"@type":"ListItem","position":2,"name":"Scholen en kinderopvang","item":"https://ceilingflow.nl/scholen/"}]}</script>'
    h = head('Plafondventilator voor klaslokalen · Ceilingflow voor scholen', 'Stille plafondventilator voor het 60x60 systeemplafond in klaslokalen. Onder 35 dB, niets op de vloer, in 5 minuten geplaatst. €299 excl. btw, offerte per school.', '/scholen/', extra)
    body = nav(False) + f'''
<main>
<section class="sh"><div class="wrap">
  <div class="crumb rv"><a href="/">Home</a> / Scholen en kinderopvang</div>
  <span class="eyebrow rv">Voor scholen en kinderopvang</span>
  <h1 class="h2 rv d1" style="margin:20px 0 24px">Een fris lokaal.<br>Zonder ventilator <em>op de vloer</em>.</h1>
  <p class="lead rv d2">Ceilingflow is een plafondventilator die in het standaard 60×60 systeemplafond past. Stil genoeg voor de les, buiten bereik van kinderen en binnen 5 minuten geplaatst.</p>
  <div class="row rv d3"><a class="btn acc" href="#offerte">Offerte voor meerdere lokalen</a><a class="btn ghost" href="/ventilator/" data-umami-event="scholen-direct-bestellen">Direct bestellen · €361,79 incl. btw</a></div>
  <p class="rv d3" style="margin-top:14px;font-size:.92rem;opacity:.8">€299 excl. btw per unit · verzending NL €9,50 · btw-factuur op naam van school of opvang</p>
  <p class="rv d3" style="margin-top:10px;font-size:.9rem;opacity:.85">Liever via bol.com bestellen? Ceilingflow Wit staat ook in onze eigen bol-winkel (Pegasus Depot). <a href="https://www.bol.com/nl/nl/p/pegasus-depot-ceilingflow-plafondventilator-595-x-595-mm-voor-systeemplafonds-plug-and-play-met-afstandsbediening-wit/9300000401948628/" target="_blank" rel="noopener" data-umami-event="bol-alternatief-klik" data-umami-event-plek="scholen" style="text-decoration:underline">Bekijk op bol.com</a></p>
  <img class="hero-img rv" src="/img/school.webp" alt="Ceilingflow plafondventilator in het systeemplafond van een klaslokaal" fetchpriority="high">
</div></section>

<section class="sec2"><div class="wrap">
  <span class="eyebrow rv">Waarom in de klas</span>
  <h2 class="h2 rv d1" style="margin-top:20px">Gemaakt voor<br>een <em>leeromgeving</em>.</h2>
  <div class="vg">{v_html}</div>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap eerlijk rv">
  <div><span class="eyebrow">Eerlijk is eerlijk</span><h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Wat Ceilingflow <em>niet</em> doet.</h2></div>
  <div><p>Ceilingflow laat de lucht in het lokaal circuleren. Hij voert geen buitenlucht aan en verlaagt CO2 niet. Hij vervangt dus geen mechanische ventilatie of het luchten via ramen.</p><p>Wat hij wel doet: een warm of benauwd lokaal aangenamer maken, zonder losse ventilatoren tussen de tafels en zonder verbouwing. In het stookseizoen brengt hij de warme lucht onder het plafond terug naar de leerlingen.</p></div>
</div></section>

<section class="sec2" id="per-lokaal" style="padding-top:0"><div class="wrap kost">
  <div class="rv">
    <span class="eyebrow">Wat kost het</span>
    <h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Vaste prijs per unit.</h2>
    <p class="lead" style="margin-top:18px">€299 excl. btw per unit, afstandsbediening inbegrepen. Verzending per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50. Wit en Zwart direct te bestellen, leverdatum per mail.</p>
    <p class="soft">Voor meerdere locaties of een levering in de vakantie maken we een offerte op maat.</p>
  </div>
  <table class="rv d1"><thead><tr><th>Aantal</th><th>Excl. btw</th><th>Incl. btw</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap">
  <span class="eyebrow rv">Zo gaat het</span>
  <div class="st">
    <div class="rv"><b>1</b><p>Offerte aanvragen</p><span>Aantal lokalen en locatie, reactie binnen 1 werkdag.</span></div>
    <div class="rv d1"><b>2</b><p>Levering</p><span>Wit of Zwart, met btw-factuur voor de administratie.</span></div>
    <div class="rv d2"><b>3</b><p>Plaatsen</p><span>Tegel eruit, unit erin, stekker erin. Gemiddeld 5 minuten per lokaal.</span></div>
  </div>
</div></section>

{offerte('Offerte voor uw school')}
{faq_block(SCHOOL_FAQ)}
</main>
''' + footer() + '</body>\n</html>\n'
    return h + body

KDV_FAQ = [
    ("Is Ceilingflow stil genoeg voor de slaapruimte?", "Ceilingflow werkt onder 35 dB, vergelijkbaar met een zachte fluisterstem. Op de laagste stand is hij geschikt voor de groepsruimte tijdens het slaapuurtje en voor de slaapkamer van de opvang."),
    ("Kunnen kinderen bij de ventilator komen?", "Nee. Ceilingflow zit in het systeemplafond, buiten bereik van kinderen. Er staat niets op de vloer en er lopen geen snoeren door de groepsruimte, dus ook geen struikelgevaar. De unit is IP44, CE- en RoHS-gecertificeerd."),
    ("Ververst Ceilingflow de lucht in de groepsruimte?", "Nee. Ceilingflow brengt de lucht in de ruimte in beweging, hij voert geen buitenlucht aan en verlaagt CO2 niet. Hij vervangt dus geen ventilatie of het luchten via ramen, maar maakt een warme of benauwde groepsruimte wel aangenamer."),
    ("Wat kost het per groepsruimte?", "Eén unit kost €299 excl. btw (€361,79 incl. btw), afstandsbediening inbegrepen. Verzending is per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50. Voor meerdere groepen of locaties maken we een offerte op maat."),
    ("Wie plaatst de unit?", "Dat kan de huismeester, een klusjesman of de installateur. Plafondtegel eruit, Ceilingflow in het 60×60 rooster, stekker in het stopcontact boven het plafond. Gemiddeld minder dan 5 minuten per unit, zonder verbouwing."),
    ("Kunnen we op factuur bestellen?", "Ja. Je ontvangt altijd een btw-factuur op naam van de opvang. Voor meerdere locaties vraag je een zakelijke offerte aan, je krijgt binnen één werkdag een voorstel."),
]


def kinderopvang():
    voordelen = [("Stil tijdens het slaapuurtje", "Onder 35 dB. Op een lage stand draait hij door terwijl de kinderen slapen."),
                 ("Buiten bereik", "De unit zit in het plafond. Peuters en dreumesen kunnen er niet aan zitten of aan trekken."),
                 ("Niets op de vloer", "Geen staande ventilator in de speelhoek, geen snoer over de grond, geen struikelgevaar."),
                 ("Klaar in 5 minuten", "Plafondtegel eruit, unit erin, stekker erin. Plaatsen kan buiten openingstijd."),
                 ("Zomer en winter", "Verkoeling door luchtstroom op warme dagen, warme lucht van het plafond naar beneden in het stookseizoen."),
                 ("Afstandsbediening", "Inbegrepen. De pedagogisch medewerker regelt snelheid, richting en timer zonder ladder.")]
    v_html = ''.join(f'<article class="rv d{i % 3}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(voordelen))
    rows = ''.join(f'<tr><td>{n} {"groepsruimte" if n == 1 else "groepsruimtes"}</td><td>€{299 * n:,}'.replace(',', '.') + f'</td><td>€{361.79 * n:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + '</td></tr>' for n in (1, 3, 6, 12))
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in KDV_FAQ]}, ensure_ascii=False)
    extra = SCHOOL_CSS + f'<script type="application/ld+json">{faq_ld}</script>'
    extra += '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ceilingflow.nl/"},{"@type":"ListItem","position":2,"name":"Kinderopvang","item":"https://ceilingflow.nl/kinderopvang/"}]}</script>'
    h = head('Plafondventilator voor de kinderopvang · Ceilingflow', 'Stille plafondventilator voor de groepsruimte van kinderopvang en peuteropvang. Onder 35 dB voor het slaapuurtje, buiten bereik van kinderen. €299 excl. btw.', '/kinderopvang/', extra)
    body = nav(False) + f'''
<main>
<section class="sh"><div class="wrap">
  <div class="crumb rv"><a href="/">Home</a> / Kinderopvang</div>
  <span class="eyebrow rv">Voor kinderopvang en peuteropvang</span>
  <h1 class="h2 rv d1" style="margin:20px 0 24px">Een frisse groepsruimte.<br>Ook tijdens het <em>slaapuurtje</em>.</h1>
  <p class="lead rv d2">Ceilingflow is een plafondventilator die in het standaard 60×60 systeemplafond past. Stil genoeg voor slapende kinderen, buiten bereik van kleine handjes en binnen 5 minuten geplaatst.</p>
  <div class="row rv d3"><a class="btn acc" href="#offerte" data-umami-event="kdv-offerte">Offerte voor meerdere groepen</a><a class="btn ghost" href="/ventilator/" data-umami-event="kdv-direct-bestellen">Direct bestellen · €361,79 incl. btw</a></div>
  <p class="rv d3" style="margin-top:14px;font-size:.92rem;opacity:.8">€299 excl. btw per unit · verzending NL €9,50 · btw-factuur op naam van de opvang</p>
  <p class="rv d3" style="margin-top:10px;font-size:.9rem;opacity:.85">Liever via bol.com bestellen? Ceilingflow Wit staat ook in onze eigen bol-winkel (Pegasus Depot). <a href="https://www.bol.com/nl/nl/p/pegasus-depot-ceilingflow-plafondventilator-595-x-595-mm-voor-systeemplafonds-plug-and-play-met-afstandsbediening-wit/9300000401948628/" target="_blank" rel="noopener" data-umami-event="bol-alternatief-klik" data-umami-event-plek="kinderopvang" style="text-decoration:underline">Bekijk op bol.com</a></p>
  <img class="hero-img rv" src="/img/kinderopvang.webp" alt="Ceilingflow plafondventilator in het systeemplafond van een groepsruimte in de kinderopvang" fetchpriority="high">
</div></section>

<section class="sec2"><div class="wrap">
  <span class="eyebrow rv">Waarom in de groepsruimte</span>
  <h2 class="h2 rv d1" style="margin-top:20px">Gemaakt voor<br>de <em>kleinsten</em>.</h2>
  <div class="vg">{v_html}</div>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap eerlijk rv">
  <div><span class="eyebrow">Eerlijk is eerlijk</span><h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Wat Ceilingflow <em>niet</em> doet.</h2></div>
  <div><p>Ceilingflow laat de lucht in de groepsruimte circuleren. Hij voert geen buitenlucht aan en verlaagt CO2 niet. Hij vervangt dus geen ventilatie of het luchten via ramen.</p><p>Wat hij wel doet: een warme of benauwde groepsruimte aangenamer maken, zonder losse ventilator tussen de kinderen en zonder verbouwing. In het stookseizoen brengt hij de warme lucht onder het plafond terug naar de speelvloer.</p></div>
</div></section>

<section class="sec2" id="per-groep" style="padding-top:0"><div class="wrap kost">
  <div class="rv">
    <span class="eyebrow">Wat kost het</span>
    <h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Vaste prijs per groepsruimte.</h2>
    <p class="lead" style="margin-top:18px">€299 excl. btw per unit, afstandsbediening inbegrepen. Verzending per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50. Wit en Zwart direct te bestellen, leverdatum per mail.</p>
    <p class="soft">Meerdere locaties of plaatsen in een sluitingsweek? Dan maken we een offerte op maat.</p>
  </div>
  <table class="rv d1"><thead><tr><th>Aantal</th><th>Excl. btw</th><th>Incl. btw</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap">
  <span class="eyebrow rv">Zo gaat het</span>
  <div class="st">
    <div class="rv"><b>1</b><p>Offerte aanvragen</p><span>Aantal groepen en locaties, reactie binnen 1 werkdag.</span></div>
    <div class="rv d1"><b>2</b><p>Levering</p><span>Wit of Zwart, met btw-factuur voor de administratie.</span></div>
    <div class="rv d2"><b>3</b><p>Plaatsen</p><span>Buiten openingstijd. Gemiddeld 5 minuten per groepsruimte.</span></div>
  </div>
  <p class="rv" style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn ghost" href="/scholen/">Ceilingflow voor scholen</a><a class="btn ghost" href="/winter/">Plafondventilator in de winter</a></p>
</div></section>

{offerte('Offerte voor uw kinderopvang')}
{faq_block(KDV_FAQ)}
</main>
''' + footer() + '</body>\n</html>\n'
    return h + body

KANTOOR_FAQ = [
    ("Is Ceilingflow stil genoeg voor een vergadering of een belafspraak?", "Op de laagste stand werkt Ceilingflow op 35 dB(A), vergelijkbaar met een zachte fluisterstem. Dat is stil genoeg tijdens vergaderen, bellen en videogesprekken. Op de hoogste stand is het 47 dB(A), bedoeld voor warme middagen."),
    ("Wat kost Ceilingflow per werkdag aan stroom?", "Op de hoogste stand gebruikt hij 41 W, op de laagste 27 W. Een werkdag van 8 uur op de hoogste stand is ongeveer 0,33 kWh. Vermenigvuldig dat met je eigen stroomtarief voor de kosten per ruimte per dag."),
    ("Hoeveel units heb ik nodig voor een open kantoor?", "Dat hangt af van de indeling, de plafondhoogte en waar de werkplekken staan. Voor een spreekkamer of losse werkkamer is één unit genoeg. Voor een open kantoor of een hele verdieping rekenen we het per ruimte voor je uit in een offerte, binnen één werkdag."),
    ("Ververst Ceilingflow de lucht in het kantoor?", "Nee. Ceilingflow brengt de lucht in de ruimte in beweging, hij voert geen buitenlucht aan en verlaagt CO2 niet. Hij vervangt dus geen mechanische ventilatie. Wil je deeltjes uit de lucht filteren, dan past de luchtreiniger met H13 HEPA-filter ernaast."),
    ("Heeft Ceilingflow ook zin in de winter?", "Ja. Op de laagste stand brengt hij de warme lucht die onder het plafond blijft hangen terug naar werkhoogte, zonder dat je tocht voelt. Dezelfde unit gebruik je in de zomer voor verkoeling door luchtstroom."),
    ("Wie plaatst de unit en moet het kantoor dicht?", "Dat kan de huismeester, de facilitair medewerker of de installateur. Plafondtegel eruit, Ceilingflow in het 60×60 rooster, stekker in het stopcontact boven het plafond. Gemiddeld minder dan 5 minuten per unit, dus gewoon voor of na werktijd."),
    ("Kunnen we op factuur en op naam van het bedrijf bestellen?", "Ja. Je ontvangt altijd een btw-factuur op naam van je bedrijf of praktijk. Voor meerdere ruimtes, verdiepingen of vestigingen vraag je een zakelijke offerte aan, je krijgt binnen één werkdag een voorstel."),
]


def kantoor():
    voordelen = [("Stil tijdens vergaderen", "35 dB(A) op de laagste stand. Hij draait door tijdens een overleg, een belafspraak of een videogesprek."),
                 ("Geen ventilator op het bureau", "Geen tafelventilator die papieren wegblaast en collega's stoort. De unit zit in het plafond."),
                 ("Geen kabels op de vloer", "Geen snoer naar een staande ventilator, geen struikelgevaar tussen de werkplekken. De stekker zit boven het plafond."),
                 ("Zuinig", "41 W op de hoogste stand. Een werkdag van 8 uur is ongeveer 0,33 kWh per ruimte."),
                 ("Zomer en winter", "Verkoeling door luchtstroom op warme dagen. In het stookseizoen brengt de laagste stand de warmte van het plafond terug naar werkhoogte."),
                 ("Klaar in 5 minuten", "Plafondtegel eruit, unit erin, stekker erin. Plaatsen kan voor of na werktijd, zonder verbouwing.")]
    v_html = ''.join(f'<article class="rv d{i % 3}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(voordelen))
    rows = ''.join(f'<tr><td>{n} {"ruimte" if n == 1 else "ruimtes"}</td><td>€{299 * n:,}'.replace(',', '.') + f'</td><td>€{361.79 * n:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + '</td></tr>' for n in (1, 4, 10, 20))
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in KANTOOR_FAQ]}, ensure_ascii=False)
    extra = SCHOOL_CSS + f'<script type="application/ld+json">{faq_ld}</script>'
    extra += '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ceilingflow.nl/"},{"@type":"ListItem","position":2,"name":"Kantoren en praktijkruimtes","item":"https://ceilingflow.nl/kantoor/"}]}</script>'
    h = head('Plafondventilator voor kantoor en spreekkamer · Ceilingflow', 'Stille plafondventilator voor 60x60 systeemplafonds in kantoren en praktijkruimtes. 35 dB(A) tijdens vergaderen, 0,33 kWh per werkdag. €299 excl. btw per ruimte.', '/kantoor/', extra)
    body = nav(False) + f'''
<main>
<section class="sh"><div class="wrap">
  <div class="crumb rv"><a href="/">Home</a> / Kantoren en praktijkruimtes</div>
  <span class="eyebrow rv">Voor kantoren, vergaderruimtes en praktijken</span>
  <h1 class="h2 rv d1" style="margin:20px 0 24px">Een fris kantoor.<br>Zonder ventilator op het <em>bureau</em>.</h1>
  <p class="lead rv d2">Ceilingflow is een plafondventilator die in het standaard 60×60 systeemplafond past. Stil genoeg om door te laten draaien tijdens een vergadering, zonder kabels tussen de werkplekken en binnen 5 minuten geplaatst.</p>
  <div class="row rv d3"><a class="btn acc" href="#offerte" data-umami-event="kantoor-offerte">Offerte voor meerdere ruimtes</a><a class="btn ghost" href="/ventilator/" data-umami-event="kantoor-direct-bestellen">Direct bestellen · €361,79 incl. btw</a></div>
  <p class="rv d3" style="margin-top:14px;font-size:.92rem;opacity:.8">€299 excl. btw per unit · verzending NL €9,50 per bestelling · btw-factuur op naam van je bedrijf</p>
  <p class="rv d3" style="margin-top:10px;font-size:.9rem;opacity:.85">Liever via bol.com bestellen? Ceilingflow Wit staat ook in onze eigen bol-winkel (Pegasus Depot). <a href="https://www.bol.com/nl/nl/p/pegasus-depot-ceilingflow-plafondventilator-595-x-595-mm-voor-systeemplafonds-plug-and-play-met-afstandsbediening-wit/9300000401948628/" target="_blank" rel="noopener" data-umami-event="bol-alternatief-klik" data-umami-event-plek="kantoor" style="text-decoration:underline">Bekijk op bol.com</a></p>
  <img class="hero-img rv" src="/img/kantoor.webp" alt="Ceilingflow plafondventilator in het systeemplafond van een kantoor" fetchpriority="high">
</div></section>

<section class="sec2"><div class="wrap">
  <span class="eyebrow rv">Waarom in het plafond</span>
  <h2 class="h2 rv d1" style="margin-top:20px">Gemaakt voor<br>de <em>werkvloer</em>.</h2>
  <div class="vg">{v_html}</div>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap eerlijk rv">
  <div><span class="eyebrow">Eerlijk is eerlijk</span><h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Wat Ceilingflow <em>niet</em> doet.</h2></div>
  <div><p>Ceilingflow laat de lucht in het kantoor circuleren. Hij voert geen buitenlucht aan en verlaagt CO2 niet. Hij vervangt dus geen mechanische ventilatie of het luchten via ramen.</p><p>Wat hij wel doet: een warme of benauwde werkruimte aangenamer maken, zonder losse ventilator op het bureau en zonder verbouwing. Voor een spreekkamer of werkkamer tot 15 m² past de <a href="/luchtreiniger/#lr125" data-umami-event="kantoor-naar-luchtreiniger" style="text-decoration:underline">Luchtreiniger Klein</a> (€109,09 excl. btw) ernaast, die filtert de lucht met H13 HEPA.</p></div>
</div></section>

<section class="sec2" id="per-ruimte" style="padding-top:0"><div class="wrap kost">
  <div class="rv">
    <span class="eyebrow">Wat kost het</span>
    <h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Vaste prijs per ruimte.</h2>
    <p class="lead" style="margin-top:18px">€299 excl. btw per unit, afstandsbediening inbegrepen. Verzending per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50. Wit en Zwart direct te bestellen, leverdatum per mail.</p>
    <p class="soft">Een spreekkamer of werkkamer: één unit. Een open kantoor of een hele verdieping: we rekenen het aantal per ruimte voor je uit in een offerte.</p>
  </div>
  <table class="rv d1"><thead><tr><th>Aantal</th><th>Excl. btw</th><th>Incl. btw</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap">
  <span class="eyebrow rv">Zo gaat het</span>
  <div class="st">
    <div class="rv"><b>1</b><p>Offerte aanvragen</p><span>Aantal ruimtes, verdiepingen of vestigingen, reactie binnen 1 werkdag.</span></div>
    <div class="rv d1"><b>2</b><p>Levering</p><span>Wit of Zwart, met btw-factuur op naam van je bedrijf.</span></div>
    <div class="rv d2"><b>3</b><p>Plaatsen</p><span>Voor of na werktijd. Gemiddeld 5 minuten per ruimte.</span></div>
  </div>
  <p class="rv" style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn ghost" href="/winter/">Plafondventilator in de winter</a><a class="btn ghost" href="/luchtreiniger/">Luchtreiniger H13 HEPA</a><a class="btn ghost" href="/scholen/">Ceilingflow voor scholen</a></p>
</div></section>

{offerte('Offerte voor uw kantoor of praktijk')}
{faq_block(KANTOOR_FAQ)}
</main>
''' + footer() + '</body>\n</html>\n'
    return h + body


WINTER_FAQ = [
    ("Heeft een plafondventilator zin in de winter?", "Ja. Warme lucht stijgt op en blijft onder het plafond hangen, terwijl het bij de vloer en de bureaus kouder aanvoelt. Ceilingflow zet die lucht in beweging, zodat de warmte van de verwarming beter verdeeld wordt over de ruimte."),
    ("Welke stand gebruik je in de winter?", "Gebruik een lage snelheid. Dan mengt de warme lucht onder het plafond met de rest van de ruimte zonder dat je een koele luchtstroom voelt. Snelheid en richting stel je in met de meegeleverde afstandsbediening."),
    ("Bespaar ik hiermee op de stookkosten?", "Dat hangt af van je ruimte, plafondhoogte en verwarming, dus we noemen geen percentage. Wat Ceilingflow wel doet: de warmte die al in de ruimte is, terugbrengen naar waar mensen zitten in plaats van onder het plafond te laten hangen."),
    ("Ververst Ceilingflow ook de lucht?", "Nee. Ceilingflow laat de lucht in de ruimte circuleren. Hij voert geen buitenlucht aan en verlaagt CO2 niet, dus hij vervangt geen mechanische ventilatie of luchten."),
    ("Kan ik hem nu bestellen en in de zomer gebruiken?", "Ja. Het is dezelfde unit voor zomer en winter. In de winter verdeelt hij de warmte, op warme dagen zorgt de luchtstroom voor verkoeling."),
]


def winter():
    punten = [("Warmte naar beneden", "Warme lucht van de verwarming blijft onder het plafond hangen. Ceilingflow brengt die weer in beweging, naar de bureaus en tafels."),
              ("Lage stand, geen tocht", "Op een lage snelheid meng je de lucht zonder koele luchtstroom. Je voelt geen wind, alleen een gelijkere temperatuur."),
              ("Afstandsbediening", "Snelheid, richting en timer regel je vanaf je plek. Inbegrepen bij elke unit."),
              ("Fluisterstil", "Onder 35 dB. Ook in de winterstand stoort hij niet tijdens vergaderingen of lessen."),
              ("Klaar in 5 minuten", "Plafondtegel eruit, unit erin, stekker erin. Geen verbouwing midden in het stookseizoen."),
              ("Eén unit, het hele jaar", "In de winter verdeelt hij de warmte, in de zomer koelt de luchtstroom. Geen tweede apparaat nodig.")]
    p_html = ''.join(f'<article class="rv d{i % 3}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(punten))
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in WINTER_FAQ]}, ensure_ascii=False)
    extra = SCHOOL_CSS + f'<script type="application/ld+json">{faq_ld}</script>'
    extra += '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://ceilingflow.nl/"},{"@type":"ListItem","position":2,"name":"Plafondventilator in de winter","item":"https://ceilingflow.nl/winter/"}]}</script>'
    h = head('Plafondventilator in de winter · warmte omlaag · Ceilingflow', 'Warme lucht blijft onder het plafond hangen. Een plafondventilator op lage stand brengt die terug naar beneden. Ceilingflow voor 60x60 plafonds, €299 excl. btw.', '/winter/', extra)
    body = nav(False) + f'''
<main>
<section class="sh"><div class="wrap">
  <div class="crumb rv"><a href="/">Home</a> / Plafondventilator in de winter</div>
  <span class="eyebrow rv">Stookseizoen</span>
  <h1 class="h2 rv d1" style="margin:20px 0 24px">Warm aan het plafond.<br>Koud aan je <em>bureau</em>?</h1>
  <p class="lead rv d2">Warme lucht stijgt op. In kantoren, klaslokalen en praktijkruimtes met een systeemplafond blijft de warmte van de verwarming daardoor boven hangen. Ceilingflow brengt die lucht weer in beweging, terug naar waar mensen zitten.</p>
  <div class="row rv d3"><a class="btn acc" href="/ventilator/" data-umami-event="winter-bestellen">Bestellen · €361,79 incl. btw</a><a class="btn ghost" href="#offerte">Offerte voor meerdere ruimtes</a></div>
  <p class="rv d3" style="margin-top:14px;font-size:.92rem;opacity:.8">€299 excl. btw per unit · verzending NL €9,50 · afstandsbediening inbegrepen</p>
  <img class="hero-img rv" src="/img/kantoor.webp" alt="Ceilingflow plafondventilator in het systeemplafond van een kantoor" fetchpriority="high">
</div></section>

<section class="sec2"><div class="wrap">
  <span class="eyebrow rv">Zo werkt het in de winter</span>
  <h2 class="h2 rv d1" style="margin-top:20px">De warmte is er al.<br>Hij zit alleen <em>boven</em>.</h2>
  <div class="vg">{p_html}</div>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap eerlijk rv">
  <div><span class="eyebrow">Eerlijk is eerlijk</span><h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Wat Ceilingflow <em>niet</em> doet.</h2></div>
  <div><p>Ceilingflow verwarmt niet zelf en we beloven geen vast besparingspercentage: dat hangt af van je ruimte, plafondhoogte en verwarming. Hij voert ook geen buitenlucht aan en verlaagt CO2 niet.</p><p>Wat hij wel doet: de warmte die je al betaalt gelijker over de ruimte verdelen, zonder losse ventilator op de vloer en zonder verbouwing.</p></div>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap">
  <span class="eyebrow rv">In 3 stappen</span>
  <div class="st">
    <div class="rv"><b>1</b><p>Plafondtegel eruit</p><span>Elk standaard 60×60 systeemplafond.</span></div>
    <div class="rv d1"><b>2</b><p>Ceilingflow erin</p><span>Stekker in een stopcontact boven het plafond.</span></div>
    <div class="rv d2"><b>3</b><p>Lage stand aan</p><span>Met de afstandsbediening, ook richting en timer.</span></div>
  </div>
  <p class="rv" style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn ghost" href="/kantoor/">Ceilingflow voor kantoren</a><a class="btn ghost" href="/scholen/">Ceilingflow voor scholen</a><a class="btn ghost" href="/kinderopvang/">Ceilingflow voor kinderopvang</a></p>
</div></section>

{offerte('Meerdere ruimtes voor deze winter?')}
{faq_block(WINTER_FAQ)}
</main>
''' + footer() + '</body>\n</html>\n'
    return h + body


LR = [
    {"k": "lr600", "naam": "Luchtreiniger Groot", "ruimte": "42 tot 74 m²", "inc": 359, "ex": "296,69", "inc_s": "359,00", "sku": "24-0600",
     "voor": "Klaslokalen, vergaderruimtes, groepsruimtes en open kantoren",
     "specs": [("Ruimte", "42 tot 74 m²"), ("Filter", "H13 HEPA + actieve kool + anionen"), ("CADR fijnstof", "600 m³/u"), ("CADR geurstoffen (TVOC)", "200 tot 390 m³/u"), ("Geluid", "32,9 dB (slaapstand) tot 69,5 dB"), ("Standen", "6, met afstandsbediening"), ("Vermogen", "60 W, 220-240 V"), ("Afmetingen", "479 × 269 × 710 mm, 10,5 kg, op wieltjes"), ("Extra", "kinderslot, filtermelding")]},
    {"k": "lr125", "naam": "Luchtreiniger Klein", "ruimte": "8 tot 15 m²", "inc": 132, "ex": "109,09", "inc_s": "132,00", "sku": "24-0125",
     "voor": "Werkplekken, spreekkamers, slaapkamers en kleine kantoren",
     "specs": [("Ruimte", "8 tot 15 m²"), ("Filter", "H13 HEPA + actieve kool"), ("CADR fijnstof", "125 m³/u"), ("CADR geurstoffen (TVOC)", "40 tot 60 m³/u"), ("Geluid", "27 / 35 / 42 dB"), ("Standen", "3"), ("Vermogen", "25 W, met adapter"), ("Afmetingen", "190 × 200 × 313 mm, 1,8 kg"), ("Extra", "kinderslot, 360° luchtinlaat")]},
]
LR_FAQ = [
    ("Wat is het verschil met de Ceilingflow?", "De Ceilingflow verplaatst lucht: hij koelt in de zomer en brengt warme lucht in de winter terug naar beneden. Een luchtreiniger filtert de lucht: fijnstof, pollen, huisstof, schimmelsporen en geuren blijven achter in het filter. Samen zorgen ze voor frisse én gelijkmatig verdeelde lucht."),
    ("Welke maat heb ik nodig?", "De Groot is voor ruimtes van 42 tot 74 m², zoals een klaslokaal of groepsruimte. De Klein is voor 8 tot 15 m², zoals een spreekkamer, werkplek of slaapkamer. Twijfel je? Vraag een offerte aan en we rekenen het per ruimte voor je uit."),
    ("Haalt een luchtreiniger CO2 weg?", "Nee. Een luchtreiniger filtert deeltjes en geurstoffen, maar voert geen buitenlucht aan. Voor CO2 blijft ventileren met buitenlucht nodig."),
    ("Wat kost verzending?", "Verzending kost per bestelling, ongeacht het aantal: Nederland €9,50, België €18,50, Duitsland en de rest van West-Europa €24,50, overige EU-landen €34,50. Je kunt luchtreinigers en Ceilingflow samen in één bestelling afrekenen."),
    ("Krijg ik een btw-factuur?", "Ja. Bij elke bestelling krijg je een factuur met btw. Voor meerdere stuks of locaties maken we graag een offerte op maat."),
]
LR_CSS = """<style>
.lrg{display:grid;gap:28px;margin-top:40px}
@media(min-width:900px){.lrg{grid-template-columns:1fr 1fr}}
.lrc{background:var(--card,#fff);border-radius:28px;overflow:hidden;box-shadow:0 1px 0 rgba(0,0,0,.06),0 30px 60px -40px rgba(0,0,0,.35);display:flex;flex-direction:column}
.lrc img{width:100%;aspect-ratio:4/3;object-fit:cover;background:#f1f1f0}
.lrc .in{padding:26px 26px 30px;display:flex;flex-direction:column;gap:14px;flex:1}
.lrc h2{font-size:clamp(28px,3vw,38px);letter-spacing:-.04em;margin:0}
.lrc .vr{opacity:.7;margin:0}
.lrc .pr b{font-size:34px;letter-spacing:-.04em}
.lrc .pr span{display:block;font-size:.92rem;opacity:.7}
.lrc table{width:100%;border-collapse:collapse;font-size:.93rem}
.lrc td{padding:8px 0;border-bottom:1px solid rgba(0,0,0,.08);vertical-align:top}
.lrc td:first-child{opacity:.65;padding-right:14px;white-space:nowrap}
.lrc .act{display:flex;gap:10px;flex-wrap:wrap;margin-top:auto;padding-top:8px}
.lrq{display:inline-flex;align-items:center;border-radius:999px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.18)}
.lrq button{width:42px;height:46px;border:0;background:none;font-size:18px;cursor:pointer;color:inherit}
.lrq span{min-width:26px;text-align:center;font-weight:600}
</style>"""


def luchtreiniger():
    kaarten = ''
    for i, p in enumerate(LR):
        rows = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in p["specs"])
        kaarten += f'''<article class="lrc rv d{i}" id="{p["k"]}">
  <img src="/img/{p["k"]}.webp" alt="{p["naam"]} met H13 HEPA-filter voor {p["ruimte"]}" loading="{"eager" if i == 0 else "lazy"}">
  <div class="in">
    <h2>{p["naam"]}</h2>
    <p class="vr">{p["voor"]} · {p["ruimte"]}</p>
    <div class="pr"><b>€{p["ex"]}</b><span>excl. btw · €{p["inc_s"]} incl. btw · excl. verzending</span></div>
    <table>{rows}</table>
    <div class="act"><div class="lrq" data-lrq="{p["k"]}"><button type="button" data-d="-1" aria-label="Minder">−</button><span>1</span><button type="button" data-d="1" aria-label="Meer">+</button></div><button class="btn acc" type="button" data-lr-add="{p["k"]}" data-umami-event="luchtreiniger-in-mandje-{p["k"]}">In mandje</button></div>
  </div>
</article>'''
    ld = [{"@context": "https://schema.org", "@type": "Product", "name": f'{p["naam"]} H13 HEPA', "sku": p["sku"], "image": f'{URL}/img/{p["k"]}.webp',
           "description": f'Luchtreiniger met H13 HEPA-filter en actieve kool voor {p["ruimte"]}.', "brand": {"@type": "Brand", "name": "Ceilingflow"},
           "offers": {"@type": "Offer", "price": f'{p["inc"]:.2f}', "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": f'{URL}/luchtreiniger/#{p["k"]}'}} for p in LR]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in LR_FAQ]}, ensure_ascii=False)
    extra = SCHOOL_CSS + LR_CSS + f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script><script type="application/ld+json">{faq_ld}</script>'
    h = head('Luchtreiniger H13 HEPA voor klas en kantoor · Ceilingflow', 'Luchtreinigers met H13 HEPA en actieve kool. Groot voor 42 tot 74 m² (CADR 600 m³/u, €296,69 excl. btw), Klein voor 8 tot 15 m² (€109,09 excl. btw).', '/luchtreiniger/', extra)
    body = nav(False) + f'''
<main>
<section class="sh"><div class="wrap">
  <div class="crumb rv"><a href="/">Home</a> / Luchtreiniger</div>
  <span class="eyebrow rv">Schone lucht</span>
  <h1 class="h2 rv d1" style="margin:20px 0 24px">Ceilingflow verplaatst de lucht.<br>Deze luchtreinigers <em>filteren</em> hem.</h1>
  <p class="lead rv d2">H13 HEPA met actieve kool vangt fijnstof, pollen, huisstof, schimmelsporen en geuren. Voor klaslokalen, groepsruimtes, spreekkamers en kantoren. Uit Nederlandse voorraad, samen met je Ceilingflow af te rekenen.</p>
  <div class="lrg">{kaarten}</div>
</div></section>

<section class="sec2" style="padding-top:0"><div class="wrap eerlijk rv">
  <div><span class="eyebrow">Eerlijk is eerlijk</span><h2 class="h2" style="margin-top:20px;font-size:clamp(34px,4.4vw,60px)">Wat een luchtreiniger <em>niet</em> doet.</h2></div>
  <div><p>Een luchtreiniger voert geen buitenlucht aan en verlaagt CO2 niet. Ventileren blijft dus nodig. Wat hij wel doet: deeltjes en geurstoffen uit de lucht in de ruimte filteren, ook als de ramen dicht moeten blijven.</p><p>Het filter vervang je als de filtermelding (Groot) aangeeft dat het vol is.</p></div>
</div></section>

{offerte('Meerdere ruimtes schone lucht?')}
{faq_block(LR_FAQ)}
</main>
''' + footer() + '''<script>
document.querySelectorAll('[data-lrq]').forEach(q => q.addEventListener('click', e => {{ const b = e.target.closest('[data-d]'); if (!b) return; const s = q.querySelector('span'); s.textContent = Math.max(1, Math.min(99, +s.textContent + +b.dataset.d)); }}));
document.querySelectorAll('[data-lr-add]').forEach(b => b.addEventListener('click', () => {{ const k = b.dataset.lrAdd; const q = +document.querySelector('[data-lrq="' + k + '"] span').textContent || 1; window.CF && CF.add(k, q); }}));
</script>
</body>
</html>
'''
    return h + body


PROSE_CSS = """<style>
.prose{max-width:46em;padding:clamp(60px,10vw,120px) 0}
.prose h1{margin:20px 0 24px}
.prose h2{font-size:clamp(22px,2.4vw,30px);letter-spacing:-.03em;margin:44px 0 12px}
.prose p,.prose li{color:var(--soft);font-size:17px;line-height:1.55;margin-top:12px}
.prose ul{padding-left:1.2em}
.prose a{text-decoration:underline;text-underline-offset:3px}
.prose .cards{display:grid;gap:12px;margin-top:30px}
@media(min-width:700px){.prose .cards{grid-template-columns:1fr 1fr}}
.prose .cards div{padding:22px;border-radius:var(--r);background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}
.prose .cards b{display:block;font-size:18px;color:var(--ink);margin-bottom:6px}
</style>"""


def crumb_ld(name, path):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": URL + "/"}, {"@type": "ListItem", "position": 2, "name": name, "item": URL + path}]}, ensure_ascii=False) + '</script>'


def contact():
    h = head('Contact en offerte · Ceilingflow', 'Contact met Ceilingflow: bel +31 6 34 33 38 09, mail nick@gnc-systems.com of vraag een offerte aan voor meerdere lokalen. Reactie binnen 1 werkdag.', '/contact/', PROSE_CSS + crumb_ld('Contact', '/contact/'))
    return h + nav(False) + f'''
<main class="wrap"><div class="prose">
  <span class="eyebrow">Contact</span>
  <h1 class="h2">Vragen of een <em>offerte?</em></h1>
  <p class="lead">Bel, mail of vul het offerteformulier in. Je krijgt binnen 1 werkdag persoonlijk antwoord.</p>
  <div class="cards">
    <div><b>Bellen</b><a href="tel:+31634333809">{PHONE}</a></div>
    <div><b>Mailen</b><a href="mailto:{MAIL}">{MAIL}</a></div>
    <div><b>Direct bestellen</b><a href="/ventilator/">Ceilingflow Wit of Zwart</a>, of een <a href="/luchtreiniger/">luchtreiniger</a></div>
    <div><b>Retour of levering</b>Vragen over je bestelling of een retour? Bel of mail ons, dan kijken we samen naar je situatie.</div>
  </div>
</div></main>
{offerte('Offerte voor meerdere ruimtes')}
''' + footer() + '</body>\n</html>\n'


def privacy():
    h = head('Privacyverklaring · Ceilingflow', 'Welke gegevens Ceilingflow.nl verwerkt bij het offerteformulier en bij bestellen, welke diensten we gebruiken en welke rechten je hebt. Geen trackingcookies.', '/privacy/', PROSE_CSS + crumb_ld('Privacyverklaring', '/privacy/'))
    return h + nav(False) + f'''
<main class="wrap"><div class="prose">
  <span class="eyebrow">Privacy</span>
  <h1 class="h2">Privacy<em>verklaring</em></h1>
  <p class="lead">Ceilingflow.nl verkoopt de Ceilingflow plafondventilator en luchtreinigers aan scholen, kinderopvang, zorg en bedrijven. Hier lees je welke gegevens we daarbij verwerken en waarom.</p>
  <h2>Offerteformulier</h2>
  <p>Vraag je een offerte aan, dan ontvangen we je naam, organisatie, e-mailadres, telefoonnummer, het aantal units, de kleur, het type locatie en je bericht. We gebruiken die gegevens alleen om je een offerte te sturen en contact met je op te nemen. Het formulier wordt verstuurd via FormSubmit (formsubmit.co), een externe dienst die je aanvraag als e-mail naar ons doorstuurt en je een bevestiging mailt.</p>
  <h2>Bestellen en betalen</h2>
  <p>Je winkelmandje staat alleen in je eigen browser tot je gaat afrekenen. Afrekenen gebeurt in een beveiligde Shopify-checkout van onze webwinkel Pegasus Depot. Daar vul je je naam, adres, e-mailadres en betaalgegevens in. Shopify en de betaaldienst die je kiest verwerken die gegevens om je bestelling en betaling af te handelen. Wij gebruiken je gegevens om de bestelling te leveren, de factuur te maken en je de leverdatum te mailen.</p>
  <h2>Bezoekersstatistieken en cookies</h2>
  <p>We tellen bezoeken met Umami op een eigen server. Dat gebeurt zonder cookies en zonder dat we zien wie je bent: we zien alleen hoeveel bezoekers welke pagina bekijken. Ceilingflow.nl plaatst geen tracking- of advertentiecookies. In je browser bewaren we alleen je kleurkeuze en je winkelmandje (localStorage). Die gegevens gaan pas naar de checkout als je afrekent.</p>
  <h2>Andere diensten</h2>
  <ul>
    <li>De lettertypen komen van Google Fonts. Je browser haalt ze op bij Google, dat daarbij je IP-adres ziet.</li>
    <li>De website staat op GitHub Pages. GitHub verwerkt technische gegevens zoals je IP-adres om de site veilig te leveren.</li>
    <li>Links naar bol.com en LinkedIn brengen je naar die websites. Daar geldt hun eigen privacybeleid.</li>
  </ul>
  <h2>Bewaren</h2>
  <p>Offerteaanvragen bewaren we zolang dat nodig is voor de offerte en de opvolging daarvan. Bestel- en factuurgegevens bewaren we zeven jaar, omdat de wet dat voorschrijft. We verkopen je gegevens niet en delen ze alleen met de diensten hierboven.</p>
  <h2>Jouw rechten</h2>
  <p>Je mag je gegevens inzien, laten verbeteren of laten verwijderen. Ook kun je bezwaar maken tegen het gebruik ervan. Mail daarvoor naar <a href="mailto:{MAIL}">{MAIL}</a> of bel {PHONE}. Ben je het niet eens met hoe we met je gegevens omgaan, dan kun je een klacht indienen bij de Autoriteit Persoonsgegevens.</p>
  <p style="margin-top:30px;font-size:14px">Laatst bijgewerkt: 24 november 2026.</p>
</div></main>
''' + footer() + '</body>\n</html>\n'


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
    pages = {'/': index(), '/ventilator/': pdp(), '/scholen/': scholen(), '/kinderopvang/': kinderopvang(), '/kantoor/': kantoor(),
             '/winter/': winter(), '/luchtreiniger/': luchtreiniger(), '/contact/': contact(), '/privacy/': privacy()}
    for p, html_ in pages.items():
        d = ROOT / p.strip('/') if p != '/' else ROOT
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(html_)
    oud = json.loads(LASTMOD.read_text()) if LASTMOD.exists() else {}
    lm = {}
    for p, html_ in pages.items():
        hs = hashlib.sha1(html_.encode()).hexdigest()
        lm[p] = {'h': hs, 'd': oud[p]['d'] if p in oud and oud[p].get('h') == hs else date.today().isoformat()}
    LASTMOD.write_text(json.dumps(lm, indent=0))
    (ROOT / f'{INDEXNOW_KEY}.txt').write_text(INDEXNOW_KEY)
    logo = ROOT / 'img' / 'logo.png'
    if not logo.exists():  # beeldmerk uit het favicon als PNG voor Organization.logo
        from PIL import Image, ImageDraw
        s = 8; im = Image.new('RGBA', (64 * s, 64 * s), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
        dr.rounded_rectangle((0, 0, 64 * s - 1, 64 * s - 1), radius=14 * s, fill='#0d0f10')
        dr.ellipse(((32 - 18) * s, (32 - 18) * s, (32 + 18) * s, (32 + 18) * s), outline='#ff5a1f', width=5 * s)
        dr.ellipse(((32 - 5) * s, (32 - 5) * s, (32 + 5) * s, (32 + 5) * s), fill='#eef0ee')
        im.save(logo, 'PNG', optimize=True)
    (ROOT / 'bedankt').mkdir(exist_ok=True)
    (ROOT / 'bedankt/index.html').write_text(simple('Bedankt · Ceilingflow', '/bedankt/', 'Bedankt voor je <em>aanvraag</em>.', 'We hebben je offerteaanvraag ontvangen en reageren binnen één werkdag.'))
    (ROOT / '404.html').write_text(simple('Pagina niet gevonden · Ceilingflow', '/404.html', 'Deze pagina <em>bestaat niet</em>.', 'De pagina die je zoekt is verplaatst of bestaat niet meer.'))
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + ''.join(f'  <url><loc>{URL}{p}</loc><lastmod>{lm[p]["d"]}</lastmod></url>\n' for p in pages) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /bedankt/\n\nSitemap: {URL}/sitemap.xml\n')
    (ROOT / 'CNAME').write_text('ceilingflow.nl\n')
    print('klaar')


if __name__ == '__main__':
    main()
