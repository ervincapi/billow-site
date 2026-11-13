/* Google Analytics 4, opt-in only. Nothing is loaded and no request reaches Google until the visitor
   accepts the consent bar; the choice is kept in this browser (localStorage) and can be changed from the
   privacy page. Skipped when the browser asks not to be tracked. */
(function () {
  var s = document.currentScript; if (!s) return;
  var id = s.getAttribute("data-id"); if (!id) return;
  if (navigator.doNotTrack === "1" || window.doNotTrack === "1" || navigator.globalPrivacyControl) return;
  if (/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname) && !/[?&]ga=debug\b/.test(location.search)) return;

  var KEY = "billow-analytics", root = document.documentElement, loaded = false;
  var L = {
    en: { text: "May we count your visit? Billow uses Google Analytics to see which pages help people. Only if you say yes.", yes: "Yes, that's fine", no: "No thanks", more: "Privacy" },
    de: { text: "Dürfen wir deinen Besuch zählen? Billow nutzt Google Analytics, um zu sehen, welche Seiten helfen. Nur wenn du zustimmst.", yes: "Ja, in Ordnung", no: "Nein danke", more: "Datenschutz" },
    es: { text: "¿Podemos contar tu visita? Billow usa Google Analytics para ver qué páginas ayudan. Solo si dices que sí.", yes: "Sí, de acuerdo", no: "No, gracias", more: "Privacidad" },
    it: { text: "Possiamo contare la tua visita? Billow usa Google Analytics per capire quali pagine sono utili. Solo se dici di sì.", yes: "Sì, va bene", no: "No, grazie", more: "Privacy" },
    sq: { text: "A mund ta numërojmë vizitën tënde? Billow përdor Google Analytics për të parë cilat faqe ndihmojnë. Vetëm nëse pranon.", yes: "Po, në rregull", no: "Jo, faleminderit", more: "Privatësia" }
  };
  var t = L[(root.lang || "en").slice(0, 2)] || L.en;
  var privacyHref = s.getAttribute("data-privacy") || "privacy.html";

  function choice() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function remember(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied" });

  function enable() {
    gtag("consent", "update", { analytics_storage: "granted" });
    if (loaded) return; loaded = true;
    gtag("js", new Date());
    gtag("config", id, { anonymize_ip: true });
    var g = document.createElement("script");
    g.async = true; g.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(g);
  }

  var bar = null;
  function hide() { if (bar) { bar.remove(); bar = null; } }
  function show() {
    if (bar) return;
    if (!document.getElementById("ga-consent-style")) {
      var st = document.createElement("style"); st.id = "ga-consent-style";
      st.textContent =
        ".ga-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:60;max-width:560px;margin:0 auto;padding:14px 16px;border:1px solid var(--line,#d9e2e6);border-radius:16px;background:var(--card,var(--ground,#fff));color:var(--fg,var(--ink,#0b1b22));box-shadow:0 18px 40px -18px rgba(6,32,42,.45);font:15px/1.45 inherit;display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center}" +
        ".ga-consent p{margin:0;flex:1 1 260px}.ga-consent p a{color:inherit;text-decoration:underline}" +
        ".ga-consent .ga-actions{display:flex;gap:8px;margin-left:auto}" +
        ".ga-consent button{font:inherit;border-radius:999px;padding:8px 16px;cursor:pointer;border:1px solid var(--line,#d9e2e6);background:transparent;color:inherit}" +
        ".ga-consent button.yes{background:var(--accent,#0e7490);border-color:var(--accent,#0e7490);color:var(--ground,var(--bg,#fff))}" +
        "@media (prefers-reduced-motion:no-preference){.ga-consent{animation:ga-in .3s ease-out}@keyframes ga-in{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}}";
      document.head.appendChild(st);
    }
    bar = document.createElement("div");
    bar.className = "ga-consent"; bar.setAttribute("role", "region"); bar.setAttribute("aria-label", "Analytics");
    var p = document.createElement("p"), a = document.createElement("a");
    p.textContent = t.text + " "; a.href = privacyHref; a.textContent = t.more; p.appendChild(a);
    var actions = document.createElement("div"); actions.className = "ga-actions";
    var no = document.createElement("button"), yes = document.createElement("button");
    no.type = "button"; no.textContent = t.no; yes.type = "button"; yes.className = "yes"; yes.textContent = t.yes;
    no.addEventListener("click", function () { remember("denied"); hide(); });
    yes.addEventListener("click", function () { remember("granted"); hide(); enable(); });
    actions.appendChild(no); actions.appendChild(yes);
    bar.appendChild(p); bar.appendChild(actions);
    document.body.appendChild(bar);
  }

  var c = choice();
  if (c === "granted") enable(); else if (c !== "denied") show();

  // Links with data-analytics-settings (privacy page) reopen the bar so the choice can be changed.
  document.addEventListener("click", function (ev) {
    var el = ev.target.closest && ev.target.closest("[data-analytics-settings]"); if (!el) return;
    ev.preventDefault();
    try { localStorage.removeItem(KEY); } catch (e) {}
    gtag("consent", "update", { analytics_storage: "denied" });
    show();
  });
})();
