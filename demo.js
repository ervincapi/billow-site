/* Billow website demo: a small, self-contained simulation of the app. Nothing is stored. */
(function () {
  var root = document.getElementById("demo"); if (!root || !window.BILLOW_DEMO) return;
  var CFG = window.BILLOW_DEMO, T = CFG.t, LANG = CFG.lang;
  var money = new Intl.NumberFormat(LANG, { style: "currency", currency: CFG.currency });
  var dShort = new Intl.DateTimeFormat(LANG, { weekday: "short", month: "short", day: "numeric" });
  var dLong = new Intl.DateTimeFormat(LANG, { month: "long", day: "numeric" });
  var dMonth = new Intl.DateTimeFormat(LANG, { month: "long", year: "numeric" });
  var DAY = 86400000;
  var CATALOG = [
    ["Netflix", 15.49, "m", "#E50914"], ["Spotify Premium", 11.99, "m", "#1DB954"], ["Disney+", 16.99, "m", "#0E3B8C"],
    ["YouTube Premium", 13.99, "m", "#FF0000"], ["Apple Music", 10.99, "m", "#FA2D48"], ["iCloud+", 2.99, "m", "#3B82F6"],
    ["Amazon Prime", 14.99, "m", "#FF9900"], ["ChatGPT Plus", 20, "m", "#10A37F"], ["Adobe Creative Cloud", 59.99, "m", "#DA1F26"],
    ["Microsoft 365", 9.99, "m", "#D83B01"], ["Dropbox", 11.99, "m", "#0061FF"], ["Strava", 11.99, "m", "#FC4C02"],
    ["Duolingo", 12.99, "m", "#58CC02"], ["The New York Times", 25, "m", "#1A1A1A"], ["PlayStation Plus", 9.99, "m", "#003791"],
    ["Xbox Game Pass", 19.99, "m", "#107C10"], ["Canva", 12.99, "m", "#00C4CC"], ["Notion", 10, "m", "#1A1A1A"],
    ["HBO Max", 16.99, "m", "#5822B4"], ["Nintendo Switch Online", 19.99, "y", "#E60012"], ["Audible", 14.95, "m", "#F8991C"],
    ["Headspace", 69.99, "y", "#F47D31"], ["Paramount+", 7.99, "m", "#0064FF"], ["Gym", 39, "m", "#0E7490"]
  ].map(function (c, i) { return { id: i, name: c[0], price: c[1], cycle: c[2], color: c[3] }; });

  function today() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }
  function addDays(d, n) { return new Date(d.getTime() + n * DAY); }
  function days(d) { return Math.round((d - today()) / DAY); }
  function monthly(s) { return s.cycle === "y" ? s.price / 12 : s.price; }
  function fmt(s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }
  function initials(n) { var p = n.replace(/[^\w+ ]/g, "").split(/\s+/); return (p[0][0] + (p[1] ? p[1][0] : (p[0][1] || ""))).toUpperCase(); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function when(d) { var n = days(d); return n === 0 ? T.today : n === 1 ? T.tomorrow : n < 0 ? dShort.format(d) : fmt(T.in_days, { n: n }); }

  var state, nextId = 100;
  function seed() {
    var t = today();
    state = { tab: "home", form: null, query: "", payday: 28, toast: "", subs: [
      { id: 1, name: "Spotify Premium", price: 11.99, cycle: "m", color: "#1DB954", next: addDays(t, 2) },
      { id: 2, name: "Strava", price: 11.99, cycle: "m", color: "#FC4C02", next: addDays(t, 1), trial: true },
      { id: 3, name: "Netflix", price: 15.49, cycle: "m", color: "#E50914", next: addDays(t, 4) },
      { id: 4, name: "iCloud+", price: 2.99, cycle: "m", color: "#3B82F6", next: addDays(t, 5) },
      { id: 5, name: "Disney+", price: 16.99, cycle: "m", color: "#0E3B8C", next: addDays(t, 15), oldPrice: 13.99 }
    ] };
  }

  function paydayDate() {
    var t = today(), d = new Date(t.getFullYear(), t.getMonth(), state.payday);
    if (d < t) d = new Date(t.getFullYear(), t.getMonth() + 1, state.payday);
    return d;
  }
  function logo(s, cls) { return '<i class="logo ' + (cls || "") + '" style="background:' + s.color + '">' + esc(initials(s.name)) + "</i>"; }
  function row(s, extra) {
    var trial = s.trial ? ' <em class="tag">' + esc(T.trial_tag) + "</em>" : "";
    var sub = when(s.next) + (s.trial ? " · " + fmt(T.converts, { x: money.format(s.price) }) : "");
    return '<div class="item">' + logo(s) + '<div class="meta"><b>' + esc(s.name) + trial + "</b><small>" + esc(sub) + "</small></div><strong" + (s.trial ? ' class="amber"' : "") + ">" + money.format(s.price) + "</strong>" + (extra || "") + "</div>";
  }

  function homeView() {
    var subs = state.subs, paid = subs.filter(function (s) { return !s.trial; }), trials = subs.filter(function (s) { return s.trial; });
    var total = paid.reduce(function (a, s) { return a + monthly(s); }, 0);
    var trialAdd = trials.reduce(function (a, s) { return a + monthly(s); }, 0);
    var pd = paydayDate(), before = subs.filter(function (s) { return s.next <= pd; });
    var beforeTotal = before.reduce(function (a, s) { return a + (s.trial ? 0 : s.price); }, 0);
    var attention = trials.length + subs.filter(function (s) { return s.oldPrice; }).length;
    var next7 = subs.filter(function (s) { return days(s.next) <= 7; }).sort(function (a, b) { return a.next - b.next; });
    var h = "";
    h += '<div class="hd"><div class="dbrand"><i></i>Billow</div><div class="greet"><b>' + esc(dShort.format(today())) + "</b><small" + (attention ? ' class="amber"' : "") + ">" + esc(attention === 0 ? T.all_good : attention === 1 ? T.attention_one : fmt(T.attention_many, { n: attention })) + "</small></div></div>";
    h += '<div class="body">';
    h += '<section class="dcard total"><small>' + esc(dMonth.format(today())).toUpperCase() + "</small><div><b>" + money.format(total) + "</b><span>" + esc(T.per_month) + "</span></div>" + (trialAdd ? '<em class="amber">' + esc(fmt(T.trials_add, { x: money.format(trialAdd) })) + "</em>" : "") + "</section>";
    h += '<section class="dcard payday"><div><small>' + esc(T.before_payday) + " · " + esc(dLong.format(pd)) + "</small><b>" + money.format(beforeTotal) + "</b></div><label>" + esc(T.payday) + ' <select data-act="payday" aria-label="' + esc(T.payday) + '">' + Array.from({ length: 28 }, function (_, i) { return '<option value="' + (i + 1) + '"' + (state.payday === i + 1 ? " selected" : "") + ">" + (i + 1) + "</option>"; }).join("") + "</select></label></section>";
    var alerts = "";
    trials.forEach(function (s) { var n = days(s.next); alerts += '<div class="alert amber"><small>' + esc(n <= 0 ? T.trial_ends_today : fmt(T.trial_ends_in, { n: n })) + "</small><b>" + esc(s.name) + "</b><span>" + esc(fmt(T.cancel_by, { d: dShort.format(addDays(s.next, -1)), x: money.format(s.price) })) + "</span></div>"; });
    subs.filter(function (s) { return s.oldPrice; }).forEach(function (s) { alerts += '<div class="alert teal"><small>' + esc(T.price_up) + "</small><b>" + esc(s.name) + "</b><span>" + esc(fmt(T.price_up_body, { old: money.format(s.oldPrice), "new": money.format(s.price), diff: money.format(s.price - s.oldPrice) })) + "</span></div>"; });
    if (alerts) h += '<div class="alerts">' + alerts + "</div>";
    h += '<h4>' + esc(T.next7) + "<span>" + money.format(next7.reduce(function (a, s) { return a + (s.trial ? 0 : s.price); }, 0)) + "</span></h4>";
    h += '<section class="list">' + (next7.length ? next7.map(function (s) { return row(s); }).join("") : '<p class="empty">' + esc(T.empty) + "</p>") + "</section>";
    h += "<h4>" + esc(T.all_subs) + "<span>" + subs.length + "</span></h4>";
    h += '<section class="list">' + (subs.length ? subs.slice().sort(function (a, b) { return a.next - b.next; }).map(function (s) { return row(s, '<button type="button" class="x" data-act="remove" data-id="' + s.id + '" aria-label="' + esc(T.remove) + '">×</button>'); }).join("") : '<p class="empty">' + esc(T.empty) + "</p>") + "</section>";
    h += "</div>";
    return h;
  }

  function addView() {
    var f = state.form;
    if (f) {
      var c = f.service;
      return '<div class="hd light"><button type="button" class="back" data-act="back">‹ ' + esc(T.back) + "</button></div>" +
        '<div class="body form"><div class="svc">' + logo(c, "big") + "<b>" + esc(c.name) + "</b></div>" +
        '<label><span>' + esc(T.price) + '</span><input type="number" step="0.01" min="0" value="' + f.price + '" data-field="price"></label>' +
        '<div class="seg"><span>' + esc(T.billing) + '</span><div><button type="button" data-act="cycle" data-v="m" class="' + (f.cycle === "m" ? "on" : "") + '">' + esc(T.monthly) + '</button><button type="button" data-act="cycle" data-v="y" class="' + (f.cycle === "y" ? "on" : "") + '">' + esc(T.yearly) + "</button></div></div>" +
        '<label><span>' + esc(T.next_charge) + '</span><input type="date" value="' + f.next + '" data-field="next"></label>' +
        '<label class="toggle"><span>' + esc(T.trial) + '<small>' + esc(fmt(T.trial_hint, { x: money.format(+f.price || 0) })) + '</small></span><input type="checkbox" data-field="trial"' + (f.trial ? " checked" : "") + "><i></i></label>" +
        '<button type="button" class="primary" data-act="save">' + esc(T.add_btn) + "</button></div>";
    }
    var q = state.query.trim().toLowerCase();
    var list = CATALOG.filter(function (c) { return !q || c.name.toLowerCase().indexOf(q) >= 0; });
    return '<div class="hd light"><input type="search" placeholder="' + esc(T.search) + '" aria-label="' + esc(T.search) + '" value="' + esc(state.query) + '" data-field="query" autocomplete="off"></div>' +
      '<div class="body"><section class="list">' + list.map(function (c) { return '<button type="button" class="item pick" data-act="pick" data-id="' + c.id + '">' + logo(c) + '<div class="meta"><b>' + esc(c.name) + "</b><small>" + money.format(c.price) + esc(c.cycle === "y" ? T.per_year : T.per_month) + "</small></div><span>+</span></button>"; }).join("") + "</section></div>";
  }

  function calendarView() {
    var t = today(), y = t.getFullYear(), m = t.getMonth(), first = new Date(y, m, 1), n = new Date(y, m + 1, 0).getDate();
    var start = (first.getDay() + 6) % 7, pd = paydayDate(), byDay = {};
    state.subs.forEach(function (s) { if (s.next.getMonth() === m && s.next.getFullYear() === y && !s.trial) byDay[s.next.getDate()] = (byDay[s.next.getDate()] || 0) + s.price; });
    var cells = "";
    for (var i = 0; i < start; i++) cells += "<div></div>";
    for (var d = 1; d <= n; d++) {
      var cls = (d === t.getDate() ? " today" : "") + (pd.getMonth() === m && d === pd.getDate() ? " payday" : "");
      cells += '<div class="cell' + cls + '"><b>' + d + "</b>" + (byDay[d] ? "<small>" + money.format(byDay[d]).replace(/[.,]\d\d(?=\D*$)/, "") + "</small>" : "") + "</div>";
    }
    var wd = []; for (var k = 0; k < 7; k++) wd.push(new Intl.DateTimeFormat(LANG, { weekday: "narrow" }).format(new Date(2024, 0, k + 1)));
    return '<div class="hd light"><b>' + esc(dMonth.format(t)) + "</b></div><div class=\"body\"><div class=\"grid\">" + wd.map(function (w) { return "<span>" + w + "</span>"; }).join("") + cells + "</div>" +
      '<section class="dcard payday"><div><small>' + esc(T.before_payday) + " · " + esc(dLong.format(pd)) + "</small><b>" + money.format(state.subs.filter(function (s) { return s.next <= pd && !s.trial; }).reduce(function (a, s) { return a + s.price; }, 0)) + "</b></div></section></div>";
  }

  function render() {
    var view = state.tab === "home" ? homeView() : state.tab === "add" ? addView() : calendarView();
    var tabs = [["home", T.home, '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>'], ["add", T.add, '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'], ["calendar", T.calendar, '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>']];
    root.innerHTML = '<div class="view ' + state.tab + '" role="tabpanel" id="demo-panel" aria-labelledby="demo-tab-' + state.tab + '">' + view + "</div>" + (state.toast ? '<div class="toast" aria-hidden="true">' + esc(state.toast) + "</div>" : "") +
      '<nav class="tabs" role="tablist">' + tabs.map(function (t) { var on = state.tab === t[0]; return '<button type="button" role="tab" id="demo-tab-' + t[0] + '" aria-selected="' + on + '" aria-controls="demo-panel" tabindex="' + (on ? "0" : "-1") + '" data-act="tab" data-v="' + t[0] + '" class="' + (on ? "on" : "") + '"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + t[2] + "</svg>" + esc(t[1]) + "</button>"; }).join("") + "</nav>";
    if (state.focus) { var target = root.querySelector(state.focus); if (target) target.focus(); state.focus = null; }
    var q = root.querySelector('[data-field="query"]'); if (q && state.tab === "add" && document.activeElement !== q && state.focusQuery) { q.focus(); q.setSelectionRange(q.value.length, q.value.length); }
  }
  var live = document.getElementById("demo-live");
  function announce(msg) { if (live) { live.textContent = ""; setTimeout(function () { live.textContent = msg; }, 50); } }
  function toast(msg) { state.toast = msg; announce(msg); render(); clearTimeout(toast.t); toast.t = setTimeout(function () { state.toast = ""; render(); }, 1800); }

  root.addEventListener("click", function (ev) {
    var el = ev.target.closest("[data-act]"); if (!el) return;
    var act = el.getAttribute("data-act"), id = +el.getAttribute("data-id");
    if (act === "tab") { state.tab = el.getAttribute("data-v"); state.form = null; state.focusQuery = false; state.focus = '[role="tab"][aria-selected="true"]'; }
    else if (act === "pick") { var c = CATALOG[id]; state.form = { service: c, price: c.price, cycle: c.cycle, next: addDays(today(), 3 + (id % 20)).toISOString().slice(0, 10), trial: false }; state.focus = '[data-field="price"]'; }
    else if (act === "back") { state.form = null; state.focus = '[data-field="query"]'; }
    else if (act === "cycle") { state.form.cycle = el.getAttribute("data-v"); }
    else if (act === "save") {
      var f = state.form, next = new Date(f.next + "T00:00:00"); if (isNaN(next)) next = addDays(today(), 7);
      if (f.trial) next = addDays(today(), 14);
      state.subs.push({ id: nextId++, name: f.service.name, price: +f.price || 0, cycle: f.cycle, color: f.service.color, next: next, trial: !!f.trial });
      state.form = null; state.query = ""; state.tab = "home"; state.focus = '[role="tab"][aria-selected="true"]'; toast(fmt(T.added, { name: f.service.name })); return;
    }
    else if (act === "remove") { var gone = state.subs.filter(function (s) { return s.id === id; })[0]; state.subs = state.subs.filter(function (s) { return s.id !== id; }); if (gone) announce(T.remove + ": " + gone.name); state.focus = '[role="tab"][aria-selected="true"]'; }
    render();
  });
  root.addEventListener("keydown", function (ev) {
    var tab = ev.target.closest('[role="tab"]'); if (!tab || (ev.key !== "ArrowLeft" && ev.key !== "ArrowRight")) return;
    var order = ["home", "add", "calendar"], i = order.indexOf(state.tab), n = order[(i + (ev.key === "ArrowRight" ? 1 : -1) + order.length) % order.length];
    ev.preventDefault(); state.tab = n; state.form = null; state.focus = '[role="tab"][aria-selected="true"]'; render();
  });
  root.addEventListener("input", function (ev) {
    var f = ev.target.getAttribute("data-field"); if (!f) return;
    if (f === "query") { state.query = ev.target.value; state.focusQuery = true; render(); return; }
    if (!state.form) return;
    if (f === "trial") { state.form.trial = ev.target.checked; render(); return; }
    state.form[f] = ev.target.value;
    if (f === "price") { var hint = root.querySelector(".toggle small"); if (hint) hint.textContent = fmt(T.trial_hint, { x: money.format(+ev.target.value || 0) }); }
  });
  root.addEventListener("change", function (ev) { if (ev.target.getAttribute("data-act") === "payday") { state.payday = +ev.target.value; render(); } });
  var reset = document.getElementById("demo-reset"); if (reset) reset.addEventListener("click", function () { seed(); render(); history.replaceState(null, "", location.pathname + location.search + "#try"); });
  /* Share: the demo state travels in the URL hash (#try=...), nothing is stored anywhere. */
  function encodeState() {
    var t = today();
    return btoa(unescape(encodeURIComponent(JSON.stringify({ p: state.payday, s: state.subs.map(function (s) { return [s.name, s.price, s.cycle, s.color, days(s.next), s.trial ? 1 : 0, s.oldPrice || 0]; }) })))).replace(/=+$/, "");
  }
  function decodeState(str) {
    try {
      var o = JSON.parse(decodeURIComponent(escape(atob(str)))); if (!o || !o.s) return false;
      state.payday = Math.min(28, Math.max(1, +o.p || 28));
      state.subs = o.s.slice(0, 30).map(function (a) { return { id: nextId++, name: String(a[0]).slice(0, 60), price: Math.max(0, +a[1] || 0), cycle: a[2] === "y" ? "y" : "m", color: /^#[0-9a-fA-F]{6}$/.test(a[3]) ? a[3] : "#0E7490", next: addDays(today(), Math.max(0, Math.min(365, +a[4] || 0))), trial: !!a[5], oldPrice: +a[6] || undefined }; });
      return true;
    } catch (e) { return false; }
  }
  var share = document.getElementById("demo-share");
  if (share) share.addEventListener("click", function () {
    var url = location.origin + location.pathname + "#try=" + encodeState();
    var done = function () { share.classList.add("done"); var label = share.lastChild.textContent; share.lastChild.textContent = share.getAttribute("data-copied"); setTimeout(function () { share.classList.remove("done"); share.lastChild.textContent = label; }, 1800); };
    if (navigator.share) { navigator.share({ title: document.title, url: url }).then(done).catch(function () {}); }
    else if (navigator.clipboard) { navigator.clipboard.writeText(url).then(done); }
    else { prompt("URL", url); }
  });
  seed();
  var m = location.hash.match(/^#try=(.+)$/);
  if (m && decodeState(m[1])) { setTimeout(function () { var el = document.getElementById("try"); if (el) el.scrollIntoView(); }, 50); }
  render();
})();

/* Nudge the demo phone when someone arrives via a "Try it" link, so it reads as interactive, not a picture. */
(function () {
  var phone = document.querySelector(".demo .phone"); if (!phone) return;
  function nudge() { phone.classList.remove("nudge"); void phone.offsetWidth; phone.classList.add("nudge"); setTimeout(function () { phone.classList.remove("nudge"); }, 1100); }
  if (location.hash.indexOf("#try") === 0) setTimeout(nudge, 700);
  document.querySelectorAll('a[href="#try"]').forEach(function (a) { a.addEventListener("click", function () { setTimeout(nudge, 650); }); });
})();
