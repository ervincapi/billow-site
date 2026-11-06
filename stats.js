/* Page-view counter: one anonymous ping per page view to the site owner's own relay (no cookies, no identifiers, no IP stored).
   Skipped when the browser asks not to be tracked. */
(function () {
  var s = document.currentScript; if (!s) return;
  var relay = s.getAttribute("data-relay"); if (!relay) return;
  if (navigator.doNotTrack === "1" || window.doNotTrack === "1" || navigator.globalPrivacyControl) return;
  if (/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)) return;
  var ref = ""; try { ref = document.referrer ? new URL(document.referrer).hostname : ""; } catch (e) {}
  if (ref === location.hostname) ref = "";
  var img = new Image();
  img.src = relay + "?view=1&p=" + encodeURIComponent(location.pathname) + "&l=" + encodeURIComponent(document.documentElement.lang || "") + "&r=" + encodeURIComponent(ref) + "&t=" + Date.now();
})();
