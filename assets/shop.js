/* Ceilingflow · kleurthema, scroll-animaties, winkelmandje (Shopify cart-permalink) en offerteformulier */
const CEILINGFLOW = {
  SHOP: 'https://5wkm0h-xs.myshopify.com',
  VARIANT_WIT: '66312769339741',     // vul hier het Shopify variant-id van Wit in (alleen cijfers)
  VARIANT_ZWART: '66312769372509', // vul hier het Shopify variant-id van Zwart in (alleen cijfers)
  PRICE_EX: 299,
  PRICE_INC: 361.79,
  FORM_EMAIL: 'nick@gnc-systems.com',
  NEXT: 'https://ceilingflow.nl/bedankt/'
};

(function () {
  const C = CEILINGFLOW;
  const BASE = document.currentScript.src.replace(/assets\/shop\.js.*$/, '');
  const COLORS = [
    {k: 'wit', n: 'Wit', v: C.VARIANT_WIT, sw: '#f4f4f2'},
    {k: 'zwart', n: 'Zwart', v: C.VARIANT_ZWART, sw: '#151617'}
  ];
  const byK = Object.fromEntries(COLORS.map(c => [c.k, c]));
  const READY = COLORS.every(c => /^\d+$/.test(String(c.v)));
  const eur = n => '€' + n.toLocaleString('nl-NL', {minimumFractionDigits: 2, maximumFractionDigits: 2});
  const root = document.documentElement;

  /* ---------- kleurthema ---------- */
  function getKleur() {
    const p = new URLSearchParams(location.search).get('kleur');
    if (byK[p]) return p;
    try { const s = localStorage.getItem('cf_kleur'); if (byK[s]) return s; } catch (e) {}
    return 'wit';
  }
  function setKleur(k) {
    if (!byK[k]) return;
    root.dataset.kleur = k;
    try { localStorage.setItem('cf_kleur', k); } catch (e) {}
    const m = document.querySelector('meta[name=theme-color]'); if (m) m.content = k === 'zwart' ? '#0b0c0d' : '#eef0ee';
    document.querySelectorAll('[data-set-kleur]').forEach(b => b.setAttribute('aria-pressed', b.dataset.setKleur === k));
    document.querySelectorAll('[data-kleur-naam]').forEach(s => s.textContent = byK[k].n);
    document.querySelectorAll('select[name=kleur]').forEach(s => { if (!s.dataset.touched) s.value = byK[k].n; });
    document.dispatchEvent(new CustomEvent('cf:kleur', {detail: k}));
  }
  setKleur(getKleur());
  document.addEventListener('click', e => { const b = e.target.closest('[data-set-kleur]'); if (b) setKleur(b.dataset.setKleur); });
  document.querySelectorAll('select[name=kleur]').forEach(s => s.addEventListener('change', () => s.dataset.touched = 1));

  /* ---------- scroll-reveal ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), {rootMargin: '0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(el => io.observe(el));

  /* ---------- formulier ---------- */
  document.querySelectorAll('form[data-offerte]').forEach(f => {
    f.action = 'https://formsubmit.co/' + C.FORM_EMAIL;
    f.method = 'POST';
    f.insertAdjacentHTML('afterbegin', `<input type="hidden" name="_subject" value="Offerteaanvraag Ceilingflow"><input type="hidden" name="_next" value="${C.NEXT}"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">`);
  });
  function toOfferte(k, q) {
    const f = document.querySelector('form[data-offerte]');
    if (!f) { location.href = BASE + '?kleur=' + k + '&aantal=' + q + '#offerte'; return; }
    const s = f.querySelector('select[name=kleur]'); if (s) { s.value = byK[k].n; s.dataset.touched = 1; }
    const a = f.querySelector('[name=aantal]'); if (a && q) a.value = q;
    f.closest('section').scrollIntoView({behavior: 'smooth'});
    setTimeout(() => { const i = f.querySelector('input[name=naam]'); if (i) i.focus({preventScroll: true}); }, 700);
  }
  const qp = new URLSearchParams(location.search).get('aantal');
  if (qp) document.querySelectorAll('form[data-offerte] [name=aantal]').forEach(a => a.value = Math.max(1, parseInt(qp) || 1));

  /* ---------- winkelmandje ---------- */
  let cart = [];
  try { cart = JSON.parse(localStorage.getItem('cf_cart') || '[]').filter(l => byK[l.k] && l.q > 0); } catch (e) {}
  const save = () => { try { localStorage.setItem('cf_cart', JSON.stringify(cart)); } catch (e) {} render(); };
  const count = () => cart.reduce((s, l) => s + l.q, 0);
  const checkoutUrl = lines => C.SHOP + '/cart/' + lines.map(l => byK[l.k].v + ':' + l.q).join(',');
  function add(k, q) {
    if (!READY) { toOfferte(k, q); return; }
    const l = cart.find(x => x.k === k);
    if (l) l.q = Math.min(99, l.q + q); else cart.push({k, q: Math.min(99, q)});
    save(); open();
  }
  function setQ(k, q) { cart = cart.map(l => l.k === k ? {...l, q} : l).filter(l => l.q > 0); save(); }

  const css = `
  .cfc-ov{position:fixed;inset:0;z-index:200;background:rgba(5,6,7,.5);backdrop-filter:blur(4px);opacity:0;pointer-events:none;transition:opacity .5s}
  .cfc-ov.open{opacity:1;pointer-events:auto}
  .cfc{position:fixed;top:0;right:0;bottom:0;z-index:201;width:min(440px,100%);background:#f6f7f5;color:#0d0f10;display:flex;flex-direction:column;transform:translateX(105%);transition:transform .7s cubic-bezier(.16,1,.3,1);box-shadow:-30px 0 80px -30px rgba(0,0,0,.4);font-family:'Inter Tight',Inter,system-ui,sans-serif}
  .cfc.open{transform:none}
  .cfc-h{display:flex;justify-content:space-between;align-items:center;padding:calc(20px + env(safe-area-inset-top)) 24px 18px;border-bottom:1px solid rgba(0,0,0,.1)}
  .cfc-h b{font-size:26px;letter-spacing:-.04em}
  .cfc-h button{background:none;border:0;font-size:30px;line-height:1;cursor:pointer;opacity:.6}
  .cfc-l{flex:1;overflow:auto;padding:6px 24px}
  .cfc-i{display:grid;grid-template-columns:76px 1fr auto;gap:14px;align-items:center;padding:18px 0;border-bottom:1px solid rgba(0,0,0,.08)}
  .cfc-i img{width:76px;height:76px;border-radius:16px;object-fit:contain;background:#e6e8e5}
  .cfc-i .nm{font-weight:600}
  .cfc-i .cl{font-size:13px;opacity:.65}
  .cfc-q{display:inline-flex;align-items:center;margin-top:8px;border-radius:999px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.18)}
  .cfc-q button{width:32px;height:32px;border:0;background:none;cursor:pointer;font-size:16px}
  .cfc-q span{min-width:24px;text-align:center;font-weight:600;font-size:14px}
  .cfc-i .pr{text-align:right;font-weight:600}
  .cfc-i .rm{display:block;margin-top:8px;font-size:12px;opacity:.55;background:none;border:0;cursor:pointer;text-decoration:underline}
  .cfc-e{padding:60px 0;text-align:center;opacity:.7}
  .cfc-f{padding:20px 24px calc(24px + env(safe-area-inset-bottom));border-top:1px solid rgba(0,0,0,.1);background:#fff}
  .cfc-row{display:flex;justify-content:space-between;font-size:15px;margin-bottom:6px}
  .cfc-row.t{font-size:22px;font-weight:600;margin:10px 0 4px}
  .cfc-s{font-size:12px;opacity:.6;margin-bottom:14px}
  .cfc-go{display:flex;align-items:center;justify-content:center;width:100%;padding:18px;border-radius:999px;background:#ff5a1f;color:#fff;font-weight:600;font-size:15px;text-decoration:none}
  .cfc-go[aria-disabled=true]{opacity:.35;pointer-events:none}
  .cfc-bump{animation:cfcb .6s cubic-bezier(.16,1,.3,1)}
  @keyframes cfcb{40%{transform:scale(1.35)}}
  [data-cart-count]:empty{display:none}`;
  document.head.insertAdjacentHTML('beforeend', `<style>${css}</style>`);
  document.body.insertAdjacentHTML('beforeend', `
    <div class="cfc-ov" id="cfcOv"></div>
    <aside class="cfc" id="cfc" aria-label="Winkelmandje" aria-hidden="true">
      <div class="cfc-h"><b>Je mandje</b><button type="button" aria-label="Sluiten" data-cart-close>×</button></div>
      <div class="cfc-l" id="cfcL"></div>
      <div class="cfc-f">
        <div class="cfc-row"><span>Subtotaal excl. btw</span><span id="cfcEx">€0</span></div>
        <div class="cfc-row t"><span>Incl. btw</span><span id="cfcInc">€0</span></div>
        <div class="cfc-s">Verzending per unit (NL €9,50 · BE/DE €18,50 · overig EU €24,95) wordt in de checkout berekend.</div>
        <a class="cfc-go" id="cfcGo" href="#">Veilig afrekenen</a>
      </div>
    </aside>`);
  const el = document.getElementById('cfc'), ov = document.getElementById('cfcOv'), L = document.getElementById('cfcL');
  function render() {
    const n = count();
    document.querySelectorAll('[data-cart-count]').forEach(b => { const o = b.textContent; b.textContent = n || ''; if (n && o !== String(n)) { b.classList.remove('cfc-bump'); void b.offsetWidth; b.classList.add('cfc-bump'); } });
    L.innerHTML = cart.length ? cart.map(l => { const c = byK[l.k]; return `
      <div class="cfc-i"><img src="${BASE}img/${c.k}.webp" alt="">
        <div><div class="nm">Ceilingflow</div><div class="cl">${c.n}</div>
          <div class="cfc-q"><button type="button" data-q="${l.k}" data-d="-1" aria-label="Minder">−</button><span>${l.q}</span><button type="button" data-q="${l.k}" data-d="1" aria-label="Meer">+</button></div></div>
        <div class="pr">${eur(C.PRICE_EX * l.q)}<button type="button" class="rm" data-rm="${l.k}">Verwijder</button></div></div>`; }).join('')
      : '<div class="cfc-e">Je mandje is nog leeg.</div>';
    document.getElementById('cfcEx').textContent = eur(C.PRICE_EX * n);
    document.getElementById('cfcInc').textContent = eur(C.PRICE_INC * n);
    const go = document.getElementById('cfcGo'); go.href = cart.length ? checkoutUrl(cart) : '#'; go.setAttribute('aria-disabled', !cart.length);
  }
  L.addEventListener('click', e => {
    const q = e.target.closest('[data-q]'), r = e.target.closest('[data-rm]');
    if (q) { const l = cart.find(x => x.k === q.dataset.q); setQ(l.k, Math.min(99, l.q + +q.dataset.d)); }
    if (r) setQ(r.dataset.rm, 0);
  });
  function open() { el.classList.add('open'); ov.classList.add('open'); el.setAttribute('aria-hidden', 'false'); }
  function close() { el.classList.remove('open'); ov.classList.remove('open'); el.setAttribute('aria-hidden', 'true'); }
  ov.addEventListener('click', close);
  document.addEventListener('click', e => {
    if (e.target.closest('[data-cart-open]')) { e.preventDefault(); open(); }
    if (e.target.closest('[data-cart-close]')) close();
    const o = e.target.closest('[data-offerte-knop]'); if (o) { e.preventDefault(); toOfferte(root.dataset.kleur, 0); }
  });
  addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  addEventListener('storage', e => { if (e.key === 'cf_cart') { try { cart = JSON.parse(e.newValue || '[]'); } catch (x) {} render(); } });
  document.querySelectorAll('.cartbtn').forEach(b => b.hidden = !READY);
  /* koopknoppen tonen "Offerte aanvragen" zolang de variant-id's ontbreken */
  if (!READY) document.querySelectorAll('[data-koop-label]').forEach(b => b.textContent = 'Offerte aanvragen');
  render();

  window.CF = {COLORS, READY, add, open, close, checkoutUrl, eur, setKleur, toOfferte, C};
})();
