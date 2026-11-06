/**
 * Billow contact relay for Google Apps Script (script.google.com).
 * Receives the website's contact form and emails it to the account that deploys this script.
 *
 * Setup (about 2 minutes, once):
 *   1. script.google.com › New project › paste this file › Save.
 *   2. Deploy › New deployment › type "Web app" › Execute as: Me › Who has access: Anyone › Deploy.
 *   3. Copy the Web app URL (ends with /exec) and give it to Claude; the site is rebuilt to post there.
 * Nothing else is needed: no third party, no activation email, free within Gmail's daily quota.
 */
var TO = Session.getEffectiveUser().getEmail();
var ALLOWED_ORIGIN = "https://billow-app.org";

function doPost(e) {
  var p = {};
  try { p = JSON.parse(e.postData.contents); } catch (err) { p = e.parameter || {}; }  /* JSON or form-encoded */
  if (p._honey) return reply({ success: "true" });  /* bot filled the hidden field: pretend it worked */
  var name = String(p.name || "").slice(0, 120), email = String(p.email || "").slice(0, 200), message = String(p.message || "").slice(0, 4000);
  if (!name || !email || !message || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return reply({ success: "false", message: "missing fields" });
  MailApp.sendEmail({
    to: TO,
    replyTo: email,
    subject: (p._subject || "Message from billow-app.org") + " · " + name,
    body: message + "\n\n— " + name + " <" + email + ">",
  });
  return reply({ success: "true" });
}

function doGet() { return reply({ success: "false", message: "POST only" }); }

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
