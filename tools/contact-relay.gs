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
 * Spam guards: hidden honeypot field, minimum fill time (_e seconds sent by contact.js), plain-Latin gibberish filter,
 * an hourly send cap, and Cloudflare Turnstile when the TURNSTILE_SECRET script property is set.
 * After changing this file: Deploy › Manage deployments › edit › Version: New version › Deploy (same /exec URL).
 */
var TO = Session.getEffectiveUser().getEmail();
var MIN_SECONDS = 3;         /* a person needs longer than this to fill in the form */
var MAX_PER_HOUR = 10;       /* cap on emails sent per hour, whatever happens */

/* Captcha (Cloudflare Turnstile) is enforced only when the secret is set:
   Project Settings › Script properties › add TURNSTILE_SECRET. Never paste the secret into this file. */
function turnstileSecret() { return String(PropertiesService.getScriptProperties().getProperty("TURNSTILE_SECRET") || "").trim(); }

/* Run this from the editor (select it next to Debug › Run) to test the secret without revealing it.
   "invalid-input-response" means the secret is fine; "invalid-input-secret" means it is wrong. */
function checkTurnstileSecret() {
  var raw = String(PropertiesService.getScriptProperties().getProperty("TURNSTILE_SECRET") || "");
  console.log("secret length " + raw.length + ", trimmed " + raw.trim().length + ", starts with 0x: " + /^0x/.test(raw.trim()));
  var res = UrlFetchApp.fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "post", payload: { secret: raw.trim(), response: "test" }, muteHttpExceptions: true,
  });
  console.log("Cloudflare says: " + res.getContentText());
}

function doPost(e) {
  var p = readBody(e);
  if (p._honey) return reply({ success: "true" });  /* bot filled the hidden field: pretend it worked */
  var name = String(p.name || "").trim().slice(0, 120), email = String(p.email || "").trim().slice(0, 200), message = String(p.message || "").trim().slice(0, 4000);
  if (!name || !email || !message || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return reply({ success: "false", message: "missing fields" });
  /* Real failures (not fake success) from here on, so a wrongly blocked person gets the site's email fallback. */
  var elapsed = Number(p._e);
  if (!(elapsed >= MIN_SECONDS)) { console.log("rejected: " + "too fast"); return reply({ success: "false", message: "too fast" }); }
  if (looksLikeGibberish(name, message)) { console.log("rejected: " + "rejected"); return reply({ success: "false", message: "rejected" }); }
  var secret = turnstileSecret();
  if (secret && !captchaPassed(secret, p["cf-turnstile-response"])) return reply({ success: "false", message: "captcha" });
  if (!underHourlyLimit()) { console.log("rejected: " + "busy"); return reply({ success: "false", message: "busy" }); }
  MailApp.sendEmail({
    to: TO,
    replyTo: email,
    subject: (p._subject || "Message from billow-app.org") + " · " + name,
    body: message + "\n\n— " + name + " <" + email + ">",
  });
  return reply({ success: "true" });
}

/* JSON, or form-encoded decoded by hand: "+" means a space and %XX is a byte, so "C++" and "a+b@x.com" survive
   because the browser sends those plus signs as %2B. */
function readBody(e) {
  var raw = (e && e.postData && e.postData.contents) || "";
  try { var j = JSON.parse(raw); if (j && typeof j === "object") return j; } catch (err) {}
  if (raw && /=/.test(raw)) {
    var out = {};
    raw.split("&").forEach(function (pair) {
      if (!pair) return;
      var i = pair.indexOf("="), k = i < 0 ? pair : pair.slice(0, i), v = i < 0 ? "" : pair.slice(i + 1);
      try { out[decodeURIComponent(k.replace(/\+/g, " "))] = decodeURIComponent(v.replace(/\+/g, " ")); } catch (err) {}
    });
    return out;
  }
  return (e && e.parameter) || {};
}

/* Only judges plain-Latin letter runs, e.g. "bjawisfdmtumskgycmpgfxxgxeodmq" from "xlvpkmnhjl". Anything with a space,
   digit, punctuation or a non-Latin script (Cyrillic, Greek, Arabic, Chinese…) passes. */
function looksLikeGibberish(name, message) {
  if (/^[A-Za-z]{20,}$/.test(message)) return true;
  var nameNoVowels = /^[A-Za-z]{6,}$/.test(name) && !/[aeiouyAEIOUY]/.test(name);
  return nameNoVowels && /^[A-Za-z]{8,}$/.test(message);
}

function captchaPassed(secret, token) {
  if (!token) return false;
  try {
    var res = UrlFetchApp.fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "post", payload: { secret: secret, response: String(token) }, muteHttpExceptions: true,
    });
    var j = JSON.parse(res.getContentText());
    if (j.success !== true) console.log("captcha rejected: " + JSON.stringify(j["error-codes"] || []));
    return j.success === true;  /* the secret is bound to the hostnames set on the widget in Cloudflare */
  } catch (err) { console.log("captcha check failed: " + err.message); return false; }
}

function underHourlyLimit() {
  var lock = LockService.getScriptLock();
  try { lock.waitLock(5000); } catch (err) { return false; }
  try {
    var cache = CacheService.getScriptCache(), key = "sent-" + Math.floor(Date.now() / 3600000);
    var n = Number(cache.get(key) || 0);
    if (n >= MAX_PER_HOUR) return false;
    cache.put(key, String(n + 1), 3700);
    return true;
  } finally { lock.releaseLock(); }
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
