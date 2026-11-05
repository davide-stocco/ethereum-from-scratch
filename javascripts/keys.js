/* ---------------------------------------------------------------------------
   Tools for the private keys page.
   ---------------------------------------------------------------------------
   Two tools:
     1. generate a random 256-bit key, using the browser's cryptographic RNG
     2. a brute-force calculator, to put 2^256 on a human scale

   Tool 1 uses BigInt and crypto.getRandomValues — exactness matters, so no
   floating point anywhere near the key itself.

   Tool 2 deliberately DOES use ordinary floating-point numbers. It reports
   orders of magnitude, where 15 significant digits is ample and the exponent
   range is what's needed. Different job, different tool.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  // secp256k1 group order. A valid private key is in [1, n-1].
  var N = BigInt("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141");
  var TWO256 = BigInt(1) << BigInt(256);

  function randomKey() {
    var bytes = new Uint8Array(32);
    // Cryptographically secure, unlike Math.random(). Loop on the
    // astronomically unlikely out-of-range draw rather than biasing it away.
    do {
      crypto.getRandomValues(bytes);
      var v = BigInt(0);
      for (var i = 0; i < 32; i++) v = (v << BigInt(8)) | BigInt(bytes[i]);
    } while (v === BigInt(0) || v >= N);
    return v;
  }

  function hex64(v) {
    var h = v.toString(16);
    while (h.length < 64) h = "0" + h;
    return h;
  }

  function generator() {
    var btn = document.getElementById("key-gen");
    var out = document.getElementById("key-out");
    if (!btn || !out || btn.dataset.bound === "1") return;
    btn.dataset.bound = "1";

    function run() {
      var v = randomKey();
      out.innerHTML =
        "<span class=\"tool__label\">A private key, as 64 hex characters</span>" +
        "<code class=\"tool__hash\">0x" + hex64(v) + "</code>" +
        "<span class=\"tool__label\">The same key, in decimal</span>" +
        "<code class=\"tool__hash\">" + v.toString(10) + "</code>" +
        "<span class=\"tool__hint\">32 bytes &nbsp;·&nbsp; " +
        v.toString(10).length + " decimal digits &nbsp;·&nbsp; " +
        "below the curve order, so valid</span>";
    }
    btn.addEventListener("click", run);
    run();
  }

  function fmt(x) {
    if (!isFinite(x)) return "∞";
    var e = Math.floor(Math.log10(x));
    var m = x / Math.pow(10, e);
    return m.toFixed(2) + " × 10<sup>" + e + "</sup>";
  }

  function bruteforce() {
    var rate = document.getElementById("bf-rate");
    var years = document.getElementById("bf-years");
    var out = document.getElementById("bf-out");
    if (!rate || !years || !out || rate.dataset.bound === "1") return;
    rate.dataset.bound = "1";

    var SPACE = 1.157920892373162e77; // 2^256

    function run() {
      var r = parseFloat(rate.value), y = parseFloat(years.value);
      if (!isFinite(r) || !isFinite(y) || r <= 0 || y <= 0) {
        out.innerHTML = "<span class=\"tool__hint\">Enter a positive rate and number of years.</span>";
        return;
      }
      var tried = r * y * 365.25 * 24 * 3600;
      var frac = tried / SPACE;
      out.innerHTML =
        "<span class=\"tool__hint\">Keys tried: <strong>" + fmt(tried) + "</strong></span>" +
        "<span class=\"tool__hint\">Fraction of all possible keys: <strong>" +
        fmt(frac) + "</strong> — that's about <strong>1 in " + fmt(1 / frac) +
        "</strong></span>" +
        (frac < 1e-20
          ? "<span class=\"tool__hint\">For context, the odds of winning a national lottery are around 1 in 10<sup>7</sup>.</span>"
          : "<span class=\"tool__hint\">Try reducing those numbers to something physically possible.</span>");
    }
    rate.addEventListener("input", run);
    years.addEventListener("input", run);
    run();
  }

  function run() { generator(); bruteforce(); }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else { run(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(run);
  }
})();
