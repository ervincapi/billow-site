/* Contact form: posts to FormSubmit (formsubmit.co), which forwards the message to the site owner's mailbox.
   If the relay cannot be reached, the visitor gets a one-click fallback that opens the message in their mail app. */
(function () {
  var form = document.getElementById("contact-form"); if (!form) return;
  var status = form.querySelector(".status"), button = form.querySelector("button[type=submit]");
  var t = { sending: form.getAttribute("data-sending"), sent: form.getAttribute("data-sent"), error: form.getAttribute("data-error"), open: form.getAttribute("data-open") };
  var to = (form.action.match(/formsubmit\.co\/(?:ajax\/)?([^/?#]+)/) || [])[1] || "";
  function mailto(data) {
    var subject = data._subject || "Message from billow-app.org";
    var body = data.message + "\n\n" + data.name + " <" + data.email + ">";
    return "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  }
  function showError(data) {
    status.className = "status err";
    status.innerHTML = t.error + ' <a class="open-mail" href="' + mailto(data).replace(/"/g, "&quot;") + '">' + t.open + "</a>";
  }
  form.addEventListener("submit", function (ev) {
    if (!window.fetch || !window.FormData) return;  /* old browsers: plain POST + redirect */
    ev.preventDefault();
    if (!form.reportValidity()) return;
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    button.disabled = true; status.className = "status"; status.textContent = t.sending;
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = ctrl && setTimeout(function () { ctrl.abort(); }, 12000);
    fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data), signal: ctrl ? ctrl.signal : undefined
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok && String(j.success) === "true", j: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.j && res.j.message || "failed");
        form.reset(); status.className = "status ok"; status.textContent = t.sent;
      })
      .catch(function () { showError(data); })
      .then(function () { clearTimeout(timer); button.disabled = false; });
  });
})();
