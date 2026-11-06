/**
 * Billow contact relay for Google Apps Script (script.google.com).
 * Receives the website's contact form and emails it to the account that deploys this script.
 * Also counts page views (GET ?view=1) into a private Google Sheet in the same account.
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

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.view) return countView(p);
  return reply({ success: "false", message: "POST only" });
}

/* ---- Page views: one row per view in a private Google Sheet ("Billow site views"). No cookies, no IP, no identifiers. */
function countView(p) {
  try {
    var sheet = viewsSheet();
    sheet.appendRow([new Date(), String(p.p || "").slice(0, 120), String(p.l || "").slice(0, 8), String(p.r || "").slice(0, 120)]);
  } catch (err) {}
  return reply({ success: "true" });
}
function viewsSheet() {
  var props = PropertiesService.getScriptProperties(), id = props.getProperty("VIEWS_SHEET_ID"), ss;
  try { ss = id && SpreadsheetApp.openById(id); } catch (err) { ss = null; }
  if (!ss) {
    ss = SpreadsheetApp.create("Billow site views");
    ss.getActiveSheet().appendRow(["When", "Page", "Language", "Referrer"]);
    props.setProperty("VIEWS_SHEET_ID", ss.getId());
  }
  return ss.getSheets()[0];
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
