/* ---------------------------------------------------------------------------
   Tag sidebar sections with the part they belong to.
   ---------------------------------------------------------------------------
   The five parts are a reading structure, not a nav level: sections in the
   same part share one accent colour, so the grouping is visible without
   making the sidebar deeper.

   Done in JS rather than CSS because Material writes RELATIVE hrefs in the
   nav — on a page inside foundations/, the link to a sibling is "../ether/"
   with no "foundations" in it — so a :has([href*="…"]) selector matches on
   some pages and not others. Section label text is stable and visible, which
   makes it the honest thing to key on.

   Fails safe: no JS, or a renamed section, means no accent and nothing else
   changes.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var PART = {
    "Foundations": 1,
    "Cryptography": 2,
    "Wallets": 2,
    "Accounts and state": 3,
    "Contracts": 3,
    "Encoding": 3,
    "Transactions": 4,
    "Blocks": 4,
    "Economics": 5
    // Fork-dependent details, Glossary and About are reference material and
    // deliberately carry no accent — they aren't part of the reading path.
  };

  function apply() {
    var items = document.querySelectorAll(".md-nav--primary .md-nav__item--nested");
    Array.prototype.forEach.call(items, function (item) {
      var link = item.querySelector(":scope > .md-nav__link");
      if (!link) return;
      var label = (link.textContent || "").trim();
      var part = PART[label];
      if (part) {
        item.setAttribute("data-part", String(part));
      } else {
        item.removeAttribute("data-part");
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else { apply(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(apply);
  }
})();
