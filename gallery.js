/* Lightbox for the screenshot strip: tap a phone to see it full size; swipe, arrow keys or buttons move between screens; Esc closes. */
(function () {
  var strip = document.querySelector(".strip"); if (!strip) return;
  var figs = Array.prototype.slice.call(strip.querySelectorAll("figure")); if (!figs.length) return;
  var L = {}; try { L = JSON.parse(strip.getAttribute("data-labels") || "{}"); } catch (e) {}
  var items = figs.map(function (f) { var img = f.querySelector("img"), cap = f.querySelector("figcaption"); return { src: img.currentSrc || img.src, alt: img.alt, cap: cap ? cap.textContent : "" }; });
  var box = document.createElement("div"); box.className = "lightbox"; box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true"); box.hidden = true;
  box.innerHTML = '<div class="lb-backdrop"></div><div class="lb-frame"><button type="button" class="lb-close" aria-label="' + (L.close || "Close") + '">×</button>' +
    '<button type="button" class="lb-prev" aria-label="' + (L.prev || "Previous") + '">‹</button><figure class="lb-fig"><div class="phone"><img alt=""></div><figcaption></figcaption></figure>' +
    '<button type="button" class="lb-next" aria-label="' + (L.next || "Next") + '">›</button></div>';
  document.body.appendChild(box);
  var img = box.querySelector("img"), cap = box.querySelector("figcaption"), fig = box.querySelector(".lb-fig"), current = 0, opener = null;
  function show(i) { current = (i + items.length) % items.length; img.src = items[current].src; img.alt = items[current].alt; cap.textContent = items[current].cap; box.setAttribute("aria-label", items[current].cap); }
  function open(i, from) { opener = from || null; show(i); box.hidden = false; document.body.classList.add("lb-open"); box.querySelector(".lb-close").focus(); }
  function close() { box.hidden = true; document.body.classList.remove("lb-open"); if (opener) opener.focus(); }
  figs.forEach(function (f, i) {
    var btn = f.querySelector("button") || f; btn.addEventListener("click", function () { open(i, btn); });
  });
  box.querySelector(".lb-close").addEventListener("click", close);
  box.querySelector(".lb-backdrop").addEventListener("click", close);
  box.querySelector(".lb-prev").addEventListener("click", function () { show(current - 1); });
  box.querySelector(".lb-next").addEventListener("click", function () { show(current + 1); });
  document.addEventListener("keydown", function (ev) {
    if (box.hidden) return;
    if (ev.key === "Escape") close();
    else if (ev.key === "ArrowLeft") show(current - 1);
    else if (ev.key === "ArrowRight") show(current + 1);
    else if (ev.key === "Tab") {  /* keep focus inside the dialog */
      var f = box.querySelectorAll("button"), first = f[0], last = f[f.length - 1];
      if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
      else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
    }
  });
  var x0 = null;
  fig.addEventListener("touchstart", function (ev) { x0 = ev.touches[0].clientX; }, { passive: true });
  fig.addEventListener("touchend", function (ev) { if (x0 === null) return; var dx = ev.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 40) show(dx < 0 ? current + 1 : current - 1); }, { passive: true });
})();
