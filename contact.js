/* Contact form: posts to the site owner's own relay (a Google Apps Script web app), which emails the message to them.
   The request is a plain form post so no CORS preflight is needed. If the relay cannot be reached or refuses the
   message, the visitor gets a one-click fallback that opens the message in their mail app.
   Spam guards sent with every message: _e (seconds since the page loaded) and, when the form carries
   data-turnstile="<site key>", a Cloudflare Turnstile token. The Turnstile script loads only once someone starts
   using the form, so ordinary visitors never fetch it. */
(function () {
  var form = document.getElementById("contact-form"); if (!form) return;
  var loadedAt = Date.now();
  var status = form.querySelector(".status"), button = form.querySelector("button[type=submit]");
  var t = { sending: form.getAttribute("data-sending"), sent: form.getAttribute("data-sent"), error: form.getAttribute("data-error"), open: form.getAttribute("data-open"), captcha: form.getAttribute("data-captcha") };
  var to = form.getAttribute("data-to") || "";
  var sitekey = form.getAttribute("data-turnstile") || "", box = form.querySelector(".captcha");
  var widget = null, token = "", pending = false, loading = false;

  function loadCaptcha() {
    if (!sitekey || !box || loading) return;
    loading = true;
    window.billowTurnstileReady = function () {
      widget = window.turnstile.render(box, {
        sitekey: sitekey, theme: "auto", size: "flexible", appearance: "always",
        callback: function (tk) { token = tk; if (pending) { pending = false; submit(); } },
        "expired-callback": function () { token = ""; },
        "error-callback": function () { token = ""; }
      });
    };
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=billowTurnstileReady";
    s.async = true; s.defer = true;
    document.head.appendChild(s);
  }
  if (sitekey) { form.addEventListener("focusin", loadCaptcha); form.addEventListener("pointerdown", loadCaptcha); }

  function resetCaptcha() { token = ""; if (widget !== null && window.turnstile) try { window.turnstile.reset(widget); } catch (e) {} }
  function mailto(data) {
    var subject = data._subject || "Message from billow-app.org";
    var body = data.message + "\n\n" + data.name + " <" + data.email + ">";
    return "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  }
  function showError(data) {
    status.className = "status err";
    status.innerHTML = t.error + ' <a class="open-mail" href="' + mailto(data).replace(/"/g, "&quot;") + '">' + t.open + "</a>";
  }
  function submit() {
    var data = {}, body = new URLSearchParams();
    new FormData(form).forEach(function (v, k) { data[k] = v; body.append(k, v); });
    body.set("_e", String(Math.round((Date.now() - loadedAt) / 1000)));
    if (token) body.set("cf-turnstile-response", token);
    button.disabled = true; status.className = "status"; status.textContent = t.sending;
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = ctrl && setTimeout(function () { ctrl.abort(); }, 15000);
    fetch(form.action, { method: "POST", body: body, signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { return r.text().then(function (txt) { var j = {}; try { j = JSON.parse(txt); } catch (e) {} return { ok: r.ok && String(j.success) === "true", j: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.j && res.j.message || "failed");
        form.reset(); status.className = "status ok"; status.textContent = t.sent;
      })
      .catch(function () { showError(data); })
      .then(function () { clearTimeout(timer); button.disabled = false; resetCaptcha(); });
  }
  form.addEventListener("submit", function (ev) {
    if (!window.fetch || !window.FormData || !window.URLSearchParams) return;  /* very old browsers: plain POST */
    ev.preventDefault();
    if (!form.reportValidity()) return;
    if (sitekey && !token) {  /* wait for the check, then send automatically */
      pending = true; loadCaptcha();
      status.className = "status"; status.textContent = t.captcha || "…";
      return;
    }
    submit();
  });
})();
