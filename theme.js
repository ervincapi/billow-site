/* Appearance toggle: system -> light -> dark. The choice is kept in this browser only (localStorage). */
(function () {
  var KEY = "billow-theme", root = document.documentElement, order = ["system", "light", "dark"];
  function current() { try { var v = localStorage.getItem(KEY); return v === "light" || v === "dark" ? v : "system"; } catch (e) { return "system"; } }
  function apply(v) { if (v === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", v); }
  document.querySelectorAll(".theme-toggle").forEach(function (btn) {
    var labels = {};
    try { labels = JSON.parse(btn.getAttribute("data-labels") || "{}"); } catch (e) {}
    function render() { var v = current(), text = (labels.name || "Appearance") + ": " + (labels[v] || v); btn.setAttribute("data-mode", v); btn.setAttribute("aria-label", text); btn.title = text; }
    btn.addEventListener("click", function () {
      var v = order[(order.indexOf(current()) + 1) % order.length];
      try { if (v === "system") localStorage.removeItem(KEY); else localStorage.setItem(KEY, v); } catch (e) {}
      apply(v); render();
    });
    render();
  });
})();
