/* Contact form: posts to FormSubmit (formsubmit.co), which forwards the message to the site owner's mailbox. */
(function () {
  var form = document.getElementById("contact-form"); if (!form) return;
  var status = form.querySelector(".status"), button = form.querySelector("button[type=submit]");
  var t = { sending: form.getAttribute("data-sending"), sent: form.getAttribute("data-sent"), error: form.getAttribute("data-error") };
  form.addEventListener("submit", function (ev) {
    if (!window.fetch || !window.FormData) return;  /* old browsers: plain POST + redirect */
    ev.preventDefault();
    if (!form.reportValidity()) return;
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    button.disabled = true; status.className = "status"; status.textContent = t.sending;
    fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data)
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok && String(j.success) === "true", j: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.j && res.j.message || "failed");
        form.reset(); status.className = "status ok"; status.textContent = t.sent;
      })
      .catch(function () { status.className = "status err"; status.innerHTML = t.error; })
      .then(function () { button.disabled = false; });
  });
})();
