/* ---------------------------------------------------------------------------
   Open links to other sites in a new tab.
   ---------------------------------------------------------------------------
   Mostly for the references at the foot of every page: following a citation
   should not cost you your place in the page you were reading.

   Done in JS rather than by writing {:target="_blank"} on every link because
   there are over a hundred of them across the references sections, and one
   missed attribute would be an inconsistency nobody could see.

   `rel="noopener"` goes on with it. Without it, the opened page gets a
   reference to this one through window.opener and can navigate it elsewhere —
   a small but real hazard, and the reason modern guidance pairs the two.

   Internal links are left alone deliberately: the reading path is meant to be
   followed in one tab, and a site that opens its own pages in new tabs buries
   the reader in them.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  function mark() {
    var here = window.location.host;
    var links = document.querySelectorAll(".md-content a[href]");
    Array.prototype.forEach.call(links, function (a) {
      // Skip anything that isn't an absolute link to a different host:
      // in-page anchors, relative paths, mailto:, and our own pages.
      if (!/^https?:\/\//i.test(a.getAttribute("href"))) return;
      if (a.host === here) return;
      a.setAttribute("target", "_blank");
      var rel = (a.getAttribute("rel") || "").split(/\s+/).filter(Boolean);
      if (rel.indexOf("noopener") === -1) rel.push("noopener");
      a.setAttribute("rel", rel.join(" "));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mark);
  } else { mark(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(mark);
  }
})();
