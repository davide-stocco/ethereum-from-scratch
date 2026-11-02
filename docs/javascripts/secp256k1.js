/* ---------------------------------------------------------------------------
   secp256k1 — deriving a public key from a private key.
   ---------------------------------------------------------------------------
   Plain JavaScript, BigInt throughout. Exactness is the entire point here, so
   there is no floating point anywhere in this file.

   The arithmetic was verified in Python before porting: G satisfies
   y^2 = x^3 + 7 (mod p), 1*G = G, n*G is the point at infinity, and
   a*(b*G) = (ab mod n)*G. This file self-tests the first three on load.

   Exposes window.EFS.pubFromPriv so the addresses page can reuse it.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var P  = (BigInt(1) << BigInt(256)) - (BigInt(1) << BigInt(32)) - BigInt(977);
  var N  = BigInt("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141");
  var GX = BigInt("0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798");
  var GY = BigInt("0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8");
  var ZERO = BigInt(0), ONE = BigInt(1), TWO = BigInt(2), THREE = BigInt(3);

  // BigInt % can return a negative; normalise into [0, P).
  function mod(a) { var r = a % P; return r < ZERO ? r + P : r; }

  function powmod(b, e, m) {
    var r = ONE; b = b % m;
    while (e > ZERO) {
      if (e & ONE) r = (r * b) % m;
      b = (b * b) % m;
      e >>= ONE;
    }
    return r;
  }

  function inv(a) { return powmod(mod(a), P - TWO, P); }  // Fermat

  // null is the point at infinity
  function add(p, q) {
    if (p === null) return q;
    if (q === null) return p;
    var lam;
    if (p[0] === q[0]) {
      if (mod(p[1] + q[1]) === ZERO) return null;       // vertical line
      lam = mod(THREE * p[0] * p[0] * inv(TWO * p[1])); // doubling
    } else {
      lam = mod((q[1] - p[1]) * inv(q[0] - p[0]));
    }
    var x = mod(lam * lam - p[0] - q[0]);
    return [x, mod(lam * (p[0] - x) - p[1])];
  }

  function mul(k, point) {
    var r = null, a = point || [GX, GY];
    while (k > ZERO) {
      if (k & ONE) r = add(r, a);
      a = add(a, a);
      k >>= ONE;
    }
    return r;
  }

  function hex(v, chars) {
    var h = v.toString(16);
    while (h.length < chars) h = "0" + h;
    return h;
  }

  function pubFromPriv(k) {
    if (k <= ZERO || k >= N) return null;
    return mul(k, null);
  }

  // --- self-test ------------------------------------------------------------
  var onCurve = mod(GY * GY - GX * GX * GX - BigInt(7)) === ZERO;
  var gIsOne  = (function () { var p = mul(ONE, null); return p && p[0] === GX && p[1] === GY; })();
  var orderOk = mul(N, null) === null;
  var OK = onCurve && gIsOne && orderOk;

  window.EFS = window.EFS || {};
  window.EFS.pubFromPriv = OK ? pubFromPriv : null;
  window.EFS.secpHex = hex;
  // Shared with the signatures page, which needs the group operations.
  window.EFS.secp = OK ? { P: P, N: N, G: [GX, GY], add: add, mul: mul, mod: mod,
                           powmod: powmod, inv: inv } : null;

  function tool() {
    var inp = document.getElementById("pub-priv");
    var btn = document.getElementById("pub-rand");
    var out = document.getElementById("pub-out");
    if (!inp || !out || inp.dataset.bound === "1") return;
    inp.dataset.bound = "1";

    function run() {
      if (!OK) {
        out.innerHTML = "<span class=\"tool__error\">Curve self-test failed; " +
                        "this tool has been disabled.</span>";
        return;
      }
      var raw = inp.value.trim().replace(/^0[xX]/, "");
      if (!/^[0-9a-fA-F]{1,64}$/.test(raw)) {
        inp.classList.add("tool__input--bad");
        out.innerHTML = "<span class=\"tool__error\">Enter 1 to 64 hex characters.</span>";
        return;
      }
      inp.classList.remove("tool__input--bad");
      var k = BigInt("0x" + raw);
      var pt = pubFromPriv(k);
      if (!pt) {
        out.innerHTML = "<span class=\"tool__error\">Out of range: a key must be " +
                        "at least 1 and below the curve order n.</span>";
        return;
      }
      var x = hex(pt[0], 64), y = hex(pt[1], 64);
      var prefix = (pt[1] & ONE) === ZERO ? "02" : "03";
      out.innerHTML =
        "<span class=\"tool__hint\">Your public key is a <strong>point on the " +
        "curve</strong> — a pair of coordinates. These two numbers are it:</span>" +
        "<span class=\"tool__label\">↳ x &nbsp;(32 bytes)</span>" +
        "<code class=\"tool__hash\">" + x + "</code>" +
        "<span class=\"tool__label\">↳ y &nbsp;(32 bytes)</span>" +
        "<code class=\"tool__hash\">" + y + "</code>" +
        "<span class=\"tool__hint\">Everything below is the <em>same point</em>, " +
        "just written down differently — see <em>The several written forms</em> " +
        "further down the page.</span>" +
        "<span class=\"tool__label\">Raw: x then y &nbsp;(64 bytes)</span>" +
        "<code class=\"tool__hash\">" + x + y + "</code>" +
        "<span class=\"tool__label\">Compressed: y replaced by one byte &nbsp;(33 bytes)</span>" +
        "<code class=\"tool__hash\">" + prefix + x + "</code>" +
        "<span class=\"tool__hint\">Here y is <strong>" +
        ((pt[1] & ONE) === ZERO ? "even" : "odd") +
        "</strong>, so the compressed form starts <code>" + prefix + "</code>. " +
        "That single byte is enough to recompute y from x.</span>";
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
        inp.value = hex(v, 64);
        run();
      });
    }
    run();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", tool);
  } else { tool(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(tool);
  }
})();
