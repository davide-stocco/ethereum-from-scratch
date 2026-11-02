/* ---------------------------------------------------------------------------
   Smooth open/close for collapsible boxes.
   ---------------------------------------------------------------------------
   A <details> element cannot be animated with CSS alone: its content is
   removed from layout entirely when closed, so there is no height to
   transition between. The fix is to drive the height from JavaScript — measure
   before and after, animate between the two, then hand control back.

   Written defensively. If anything at all goes wrong, the listener bails out
   and the browser's own instant toggle happens instead, so the worst case is
   the behaviour we had before.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var DURATION = 260; // ms — matches the sidebar's easing feel

  function animate(details) {
    var summary = details.querySelector("summary");
    if (!summary || summary.dataset.animBound === "1") return;
    summary.dataset.animBound = "1";

    summary.addEventListener("click", function (event) {
      // Let modified clicks and in-progress animations alone.
      if (event.metaKey || event.ctrlKey || event.shiftKey) return;
      if (details.dataset.animating === "1") {
        event.preventDefault();
        return;
      }

      var reduced = window.matchMedia &&
                    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduced) return; // honour the OS setting: no animation at all

      try {
        var startH = details.offsetHeight;
        var closing = details.open;
        var endH;

        if (closing) {
          endH = summary.offsetHeight;
        } else {
          details.open = true;            // open to measure
          endH = details.offsetHeight;
        }

        if (!startH || !endH || startH === endH) {
          if (!closing) return;           // already handled by setting open
          return;                         // nothing sensible to animate
        }

        event.preventDefault();
        details.dataset.animating = "1";
        details.classList.add("is-animating");
        details.style.height = startH + "px";

        // Two frames: the first commits the start height, the second starts
        // the transition. One frame is not reliably enough.
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            details.style.height = endH + "px";
          });
        });

        var done = false;
        function finish() {
          if (done) return;
          done = true;
          details.style.height = "";
          details.classList.remove("is-animating");
          delete details.dataset.animating;
          if (closing) details.open = false;
          details.removeEventListener("transitionend", onEnd);
        }
        function onEnd(e) {
          if (e.propertyName === "height") finish();
        }
        details.addEventListener("transitionend", onEnd);
        setTimeout(finish, DURATION + 120); // fallback if transitionend misses
      } catch (err) {
        // Give up quietly and let the browser do its normal thing.
        details.style.height = "";
        details.classList.remove("is-animating");
        delete details.dataset.animating;
      }
    });
  }

  function run() {
    var all = document.querySelectorAll(".md-typeset details");
    for (var i = 0; i < all.length; i++) animate(all[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else { run(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(run);
  }
})();
