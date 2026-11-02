/* ---------------------------------------------------------------------------
   Tools for the addresses page.
   ---------------------------------------------------------------------------
   Two tools:
     1. the whole derivation, private key -> public key -> hash -> address
     2. an EIP-55 checksum calculator and validator

   Reuses window.EFS.pubFromPriv (secp256k1.js) and
   window.EFS.keccak256Bytes (keccak.js) rather than duplicating either, so
   there is exactly one implementation of each on the site.

   EIP-55 was verified in Python against all four vectors published in the
   EIP before this was written.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var ZERO = BigInt(0);
  var N = BigInt("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141");

  function ready() {
    return window.EFS && window.EFS.pubFromPriv && window.EFS.keccak256Bytes;
  }

  var FAIL = "<span class=\"tool__error\">A dependency failed its self-test, " +
             "so this tool is disabled rather than showing a wrong result.</span>";

  function pad64(v) {
    var h = v.toString(16);
    while (h.length < 64) h = "0" + h;
    return h;
  }

  function hexToBytes(h) {
    var out = [];
    for (var i = 0; i < h.length; i += 2) out.push(parseInt(h.substr(i, 2), 16));
    return out;
  }

  // EIP-55: uppercase a hex letter when the matching nibble of
  // keccak256(lowercase address) is 8 or above.
  function checksum(addrLower) {
    var h = window.EFS.keccak256Bytes(
      Array.prototype.map.call(addrLower, function (c) { return c.charCodeAt(0); })
    );
    var out = "";
    for (var i = 0; i < addrLower.length; i++) {
      var c = addrLower[i];
      out += (c >= "a" && c <= "f" && parseInt(h[i], 16) >= 8) ? c.toUpperCase() : c;
    }
    return out;
  }

  // --- tool 1: the full chain ----------------------------------------------
  function chain() {
    var inp = document.getElementById("addr-priv");
    var btn = document.getElementById("addr-rand");
    var out = document.getElementById("addr-out");
    if (!inp || !out || inp.dataset.bound === "1") return;
    inp.dataset.bound = "1";

    function run() {
      if (!ready()) { out.innerHTML = FAIL; return; }
      var raw = inp.value.trim().replace(/^0[xX]/, "");
      if (!/^[0-9a-fA-F]{1,64}$/.test(raw)) {
        inp.classList.add("tool__input--bad");
        out.innerHTML = "<span class=\"tool__error\">Enter 1 to 64 hex characters.</span>";
        return;
      }
      inp.classList.remove("tool__input--bad");
      var k = BigInt("0x" + raw);
      var pt = window.EFS.pubFromPriv(k);
      if (!pt) {
        out.innerHTML = "<span class=\"tool__error\">Out of range: a key must be " +
                        "at least 1 and below the curve order.</span>";
        return;
      }
      var pub = pad64(pt[0]) + pad64(pt[1]);
      var h = window.EFS.keccak256Bytes(hexToBytes(pub));
      var last20 = h.slice(24);          // 64 hex chars - 40 = 24
      var discarded = h.slice(0, 24);

      out.innerHTML =
        "<span class=\"tool__label\">1 · Public key — 64 bytes</span>" +
        "<code class=\"tool__hash\">" + pub + "</code>" +
        "<span class=\"tool__label\">2 · Keccak-256 of those 64 bytes — 32 bytes</span>" +
        "<code class=\"tool__hash\"><span class=\"tool__faint\">" + discarded +
        "</span><strong>" + last20 + "</strong></code>" +
        "<span class=\"tool__hint\">The first 12 bytes are greyed out because " +
        "they're thrown away. Only the <strong>last 20</strong> are kept.</span>" +
        "<span class=\"tool__label\">3 · The address</span>" +
        "<code class=\"tool__hash\">0x" + checksum(last20) + "</code>" +
        "<span class=\"tool__hint\">Shown with its EIP-55 capitalisation. " +
        "All-lowercase <code>0x" + last20 + "</code> is the same address and " +
        "equally valid.</span>";
    }

    inp.addEventListener("input", run);
    if (btn && btn.dataset.bound !== "1") {
      btn.dataset.bound = "1";
      btn.addEventListener("click", function () {
        var b = new Uint8Array(32), v;
        do {
          crypto.getRandomValues(b);
          v = ZERO;
          for (var i = 0; i < 32; i++) v = (v << BigInt(8)) | BigInt(b[i]);
        } while (v === ZERO || v >= N);
        inp.value = pad64(v);
        run();
      });
    }
    run();
  }

  // --- tool 2: checksum calculator and validator ---------------------------
  function checker() {
    var inp = document.getElementById("sum-in");
    var out = document.getElementById("sum-out");
    if (!inp || !out || inp.dataset.bound === "1") return;
    inp.dataset.bound = "1";

    function run() {
      if (!ready()) { out.innerHTML = FAIL; return; }
      var raw = inp.value.trim().replace(/^0[xX]/, "");
      if (!/^[0-9a-fA-F]{40}$/.test(raw)) {
        inp.classList.add("tool__input--bad");
        out.innerHTML = "<span class=\"tool__error\">An address is exactly 40 hex " +
                        "characters (20 bytes). You have " + raw.length + ".</span>";
        return;
      }
      inp.classList.remove("tool__input--bad");
      var correct = checksum(raw.toLowerCase());
      var isLower = raw === raw.toLowerCase();
      var isUpper = raw === raw.toUpperCase();

      var marked = correct.split("").map(function (ch, i) {
        return ch === raw[i] ? ch : "<em class=\"tool__diff\">" + ch + "</em>";
      }).join("");

      var verdict;
      if (isLower || isUpper) {
        verdict = "<span class=\"tool__hint\">Input is all one case, so it carries " +
                  "<strong>no checksum</strong> — still a perfectly valid address, " +
                  "just with no typo protection. The checksummed form is above.</span>";
      } else if (raw === correct) {
        verdict = "<span class=\"tool__hint\"><strong>Checksum valid.</strong> " +
                  "The capitalisation matches, so this address is almost certainly " +
                  "typed correctly.</span>";
      } else {
        verdict = "<span class=\"tool__error\"><strong>Checksum fails.</strong> " +
                  "The highlighted characters should be capitalised differently. " +
                  "A wallet would refuse this — it suggests a typo.</span>";
      }

      out.innerHTML =
        "<span class=\"tool__label\">Checksummed form</span>" +
        "<code class=\"tool__hash\">0x" + marked + "</code>" + verdict;
    }
    inp.addEventListener("input", run);
    run();
  }

  function run() { chain(); checker(); }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else { run(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(run);
  }
})();
