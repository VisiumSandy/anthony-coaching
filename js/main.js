/* ============================================================
   TODO (PERSONNALISATION) : toutes les infos modifiables ici
   ============================================================ */
const CONFIG = {
  phoneE164: "+33663959355",       // numéro au format international
  phoneDisplay: "06 63 95 93 55",  // numéro affiché
  clients: "+120"                  // TODO: nombre de clients satisfaits (hero)
  // Chiffres clés animés : attributs data-count dans index.html (section Biographie)
};

(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Téléphone, depuis CONFIG
  $$("[data-call]").forEach(a => a.setAttribute("href", "tel:" + CONFIG.phoneE164));
  $$("[data-phone-label]").forEach(e => (e.textContent = CONFIG.phoneDisplay));
  $$("[data-clients]").forEach(e => (e.textContent = CONFIG.clients));
  $("#year").textContent = new Date().getFullYear();

  // Header : bordure après scroll
  const header = $("#header");
  const progress = $("#progress");
  // Parallax hero
  const img = $("#heroImg");
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = scrollY;
      header.classList.toggle("is-stuck", y > 20);
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.setProperty("--p", max > 0 ? Math.min(y / max, 1) : 0);
      if (!reduce && y < innerHeight * 1.2) img.style.transform = `translate3d(0, ${y * 0.18}px, 0) scale(1.12)`;
      ticking = false;
    });
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Reveal au scroll (décalage léger entre frères)
  const groups = new Map();
  $$("[data-reveal]").forEach(el => {
    const p = el.parentElement;
    const n = groups.get(p) || 0;
    groups.set(p, n + 1);
    el.style.setProperty("--d", Math.min(n, 4) * 90 + "ms");
  });
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add("in");
      io.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  $$("[data-reveal]").forEach(el => io.observe(el));

  // Compteurs
  const fmt = new Intl.NumberFormat("fr-FR");
  const runCount = (el) => {
    const end = +el.dataset.count, pre = el.dataset.prefix || "", suf = el.dataset.suffix || "";
    const dur = reduce ? 900 : 1600, t0 = performance.now();
    const tick = (t) => {
      const k = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - k, 3);
      el.textContent = pre + fmt.format(Math.round(end * eased)) + suf;
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const cio = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { runCount(e.target); cio.unobserve(e.target); } });
  }, { threshold: 0.6 });
  $$("[data-count]").forEach(el => cio.observe(el));

  // Avant / après : curseur + cadre de secours si la photo manque
  $$(".ba__stage").forEach(st => {
    const r = $(".ba__range", st);
    r.addEventListener("input", () => st.style.setProperty("--pos", r.value + "%"));
    $$("img", st).forEach(im => {
      const miss = () => im.setAttribute("data-missing", "");
      if (im.complete && !im.naturalWidth) miss();
      im.addEventListener("error", miss);
    });
  });

  // Menu mobile
  const burger = $("#burger"), menu = $("#menu");
  const setMenu = (open) => {
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    menu.hidden = !open;
    document.body.classList.toggle("menu-open", open);
  };
  burger.addEventListener("click", () => setMenu(menu.hidden));
  menu.addEventListener("click", e => { if (e.target.closest("a")) setMenu(false); });
  addEventListener("keydown", e => { if (e.key === "Escape" && !menu.hidden) { setMenu(false); burger.focus(); } });
  matchMedia("(min-width: 960px)").addEventListener("change", e => { if (e.matches) setMenu(false); });

  // Bouton flottant : visible une fois le CTA du hero passé, caché sur le CTA final
  const fab = $("#fab");
  let heroOut = false, finalIn = false;
  const upd = () => fab.classList.toggle("is-on", heroOut && !finalIn);
  new IntersectionObserver(([e]) => { heroOut = !e.isIntersecting; upd(); }).observe($("#heroCall"));
  new IntersectionObserver(([e]) => { finalIn = e.isIntersecting; upd(); }, { threshold: 0.25 }).observe($("#contact"));
})();
