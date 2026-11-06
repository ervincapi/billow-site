/* Savings calculator: three rows of subscriptions you don't really use; shows the yearly and monthly waste. Nothing is stored. */
(function () {
  var root = document.getElementById("calc-box"); if (!root) return;
  var cfg = {}; try { cfg = JSON.parse(root.getAttribute("data-cfg") || "{}"); } catch (e) {}
  var T = cfg.t || {}, money = new Intl.NumberFormat(cfg.lang || "en", { style: "currency", currency: cfg.currency || "USD" });
  var rows = root.querySelectorAll(".calc-row"), out = root.querySelector(".calc-result"), share = root.querySelector(".calc-share");
  var SUGGEST = { "netflix": 15.49, "spotify": 11.99, "disney": 16.99, "youtube": 13.99, "apple music": 10.99, "icloud": 2.99, "prime": 14.99, "chatgpt": 20, "adobe": 59.99, "microsoft": 9.99, "dropbox": 11.99, "strava": 11.99, "duolingo": 12.99, "times": 25, "playstation": 9.99, "xbox": 19.99, "canva": 12.99, "notion": 10, "hbo": 16.99, "audible": 14.95, "gym": 39, "paramount": 7.99 };
  function fmt(s, o) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); }
  var yearly = 0;
  function update() {
    yearly = 0; var any = false;
    rows.forEach(function (r) {
      var p = parseFloat(r.querySelector("[data-price]").value), cycle = r.querySelector("[data-cycle]").value;
      if (p > 0) { any = true; yearly += cycle === "y" ? p : p * 12; }
    });
    if (!any) { out.className = "calc-result"; out.textContent = T.empty || ""; share.hidden = true; return; }
    out.className = "calc-result on";
    out.innerHTML = '<b>' + money.format(yearly) + '</b><span>' + fmt(T.result, { y: money.format(yearly), m: money.format(yearly / 12) }) + "</span>";
    share.hidden = false;
  }
  rows.forEach(function (r) {
    var name = r.querySelector("[data-name]"), price = r.querySelector("[data-price]");
    name.addEventListener("input", function () {
      var k = name.value.trim().toLowerCase(); if (!k || price.value) return;
      for (var key in SUGGEST) if (k.indexOf(key) >= 0) { price.value = SUGGEST[key]; break; }
      update();
    });
    r.querySelectorAll("input, select").forEach(function (el) { el.addEventListener("input", update); el.addEventListener("change", update); });
  });
  share.addEventListener("click", function () {
    var text = fmt(T.share_text, { y: money.format(yearly) });
    var done = function () { share.classList.add("done"); var old = share.textContent; share.textContent = T.copied; setTimeout(function () { share.classList.remove("done"); share.textContent = old; }, 1800); };
    if (navigator.share) navigator.share({ text: text }).then(done).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(text).then(done);
  });
  update();
})();
