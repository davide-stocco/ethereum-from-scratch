/* ---------------------------------------------------------------------------
   Signing, and recovering the signer's address from a signature.
   ---------------------------------------------------------------------------
   Reuses window.EFS.secp (secp256k1.js) and window.EFS.keccak256Bytes
   (keccak.js). No duplicated cryptography anywhere on the site.

   Both directions were verified in Python before porting: 40 out of 40
   random sign-then-recover round-trips returned the signing key's own
   address. This file re-checks one round-trip on load and disables the tool
   if it fails.

   Note: real Ethereum message signing prefixes the message per EIP-191.
   This hashes the message directly, which keeps the demonstration about
   signing rather than about framing. The page says so.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var ZERO = BigInt(0), ONE = BigInt(1), TWO = BigInt(2);

  function ready() {
    return window.EFS && window.EFS.secp && window.EFS.keccak256Bytes;
  }

  function hex64(v) {
    var h = v.toString(16);
    while (h.length < 64) h = "0" + h;
    return h;
  }

  function utf8(s) {
    var e = new TextEncoder().encode(s), out = [];
    for (var i = 0; i < e.length; i++) out.push(e[i]);
    return out;
  }

  function msgHash(text) {
    var h = window.EFS.keccak256Bytes(utf8(text));
    return BigInt("0x" + h) % window.EFS.secp.N;
  }

  function randScalar() {
    var N = window.EFS.secp.N, b = new Uint8Array(32), v;
    do {
      crypto.getRandomValues(b);
      v = ZERO;
      for (var i = 0; i < 32; i++) v = (v << BigInt(8)) | BigInt(b[i]);
    } while (v === ZERO || v >= N);
    return v;
  }

  function sign(z, d, k) {
    var s_ = window.EFS.secp, N = s_.N;
    var R = s_.mul(k, null);
    var r = R[0] % N;
    var s = (s_.powmod(k, N - TWO, N) * (z + r * d)) % N;
    var v = (R[1] % TWO === ZERO) ? 0 : 1;
    // Consensus requires the lower of the two equivalent s values.
    if (s > N / TWO) { s = N - s; v ^= 1; }
    return { r: r, s: s, v: v };
  }

  function recover(z, r, s, v) {
    var s_ = window.EFS.secp, N = s_.N, P = s_.P;
    if (r <= ZERO || r >= N || s <= ZERO || s >= N) return null;
    // Rebuild R from r, picking the y whose parity matches v.
    var alpha = s_.mod(r * r % P * r + BigInt(7));
    var y = s_.powmod(alpha, (P + ONE) / BigInt(4), P);
    if (s_.mod(y * y) !== alpha) return null;          // r wasn't a valid x
    if ((y % TWO === ZERO ? 0 : 1) !== v) y = P - y;
    var R = [r, y];
    var rinv = s_.powmod(r, N - TWO, N);
    var sR = s_.mul(s, R);
    var eG = s_.mul((N - z) % N, null);
    return s_.mul(rinv, s_.add(sR, eG));
  }

  function addrOf(pt) {
    if (!pt) return null;
    var pub = hex64(pt[0]) + hex64(pt[1]);
    var bytes = [];
    for (var i = 0; i < pub.length; i += 2) bytes.push(parseInt(pub.substr(i, 2), 16));
    return window.EFS.keccak256Bytes(bytes).slice(24);
  }

  var selfTestOK = null;
  function okOnce() {
    if (selfTestOK !== null) return selfTestOK;
    if (!ready()) return (selfTestOK = false);
    try {
      var d = BigInt(1);
      var z = msgHash("self test");
      var sig = sign(z, d, BigInt("0x1234567890abcdef"));
      var got = addrOf(recover(z, sig.r, sig.s, sig.v));
      selfTestOK = got === addrOf(window.EFS.pubFromPriv(d));
    } catch (e) { selfTestOK = false; }
    return selfTestOK;
  }

  var FAIL = "<span class=\"tool__error\">This tool failed its self-test and " +
             "has been disabled rather than show a wrong result.</span>";

  function tool() {
    var msg = document.getElementById("sig-msg");
    var key = document.getElementById("sig-key");
    var chk = document.getElementById("sig-check");
    var btn = document.getElementById("sig-again");
    var out = document.getElementById("sig-out");
    if (!msg || !key || !chk || !out || msg.dataset.bound === "1") return;
    msg.dataset.bound = "1";

    var current = null;   // the signature as last produced

    function doSign() {
      if (!okOnce()) { out.innerHTML = FAIL; return; }
      var raw = key.value.trim().replace(/^0[xX]/, "");
      if (!/^[0-9a-fA-F]{1,64}$/.test(raw)) {
        key.classList.add("tool__input--bad");
        out.innerHTML = "<span class=\"tool__error\">The key must be 1 to 64 hex characters.</span>";
        current = null;
        return;
      }
      key.classList.remove("tool__input--bad");
      var d = BigInt("0x" + raw);
      if (d === ZERO || d >= window.EFS.secp.N) {
        out.innerHTML = "<span class=\"tool__error\">Key out of range.</span>";
        current = null;
        return;
      }
      current = sign(msgHash(msg.value), d, randScalar());
      current.signer = addrOf(window.EFS.pubFromPriv(d));
      current.signed = msg.value;
      render();
    }

    function render() {
      if (!current) return;
      var zc = msgHash(chk.value);
      var rec = addrOf(recover(zc, current.r, current.s, current.v));
      var same = rec === current.signer;
      var tampered = chk.value !== current.signed;

      var verdict;
      if (same) {
        verdict = "<span class=\"tool__hint\"><strong class=\"tool__hi\">The " +
                  "recovered address matches the signer.</strong> Nobody told the " +
                  "verifier who signed — it was computed from the signature " +
                  "alone.</span>";
      } else if (rec) {
        verdict = "<span class=\"tool__error\"><strong>Recovered a different " +
                  "address.</strong> The message was altered after signing, so " +
                  "recovery yields some unrelated address — not an error, just " +
                  "a stranger. Nothing in the signature says who it should " +
                  "have been.</span>";
      } else {
        verdict = "<span class=\"tool__error\">Recovery failed outright for this " +
                  "combination.</span>";
      }

      out.innerHTML =
        "<span class=\"tool__label\">The signature — r</span>" +
        "<code class=\"tool__hash\">" + hex64(current.r) + "</code>" +
        "<span class=\"tool__label\">The signature — s</span>" +
        "<code class=\"tool__hash\">" + hex64(current.s) + "</code>" +
        "<span class=\"tool__label\">v &nbsp;(which of two possible keys)</span>" +
        "<code class=\"tool__hash\">" + current.v + "</code>" +
        "<span class=\"tool__label\">Address of the key that signed</span>" +
        "<code class=\"tool__hash\">0x" + current.signer + "</code>" +
        "<span class=\"tool__label\">Address recovered from the signature" +
        (tampered ? " + the altered message" : "") + "</span>" +
        "<code class=\"tool__hash\">" + (rec ? "0x" + rec : "—") + "</code>" +
        verdict;
    }

    msg.addEventListener("input", function () { chk.value = msg.value; doSign(); });
    key.addEventListener("input", doSign);
    chk.addEventListener("input", render);
    if (btn && btn.dataset.bound !== "1") {
      btn.dataset.bound = "1";
      btn.addEventListener("click", doSign);
    }
    doSign();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", tool);
  } else { tool(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(tool);
  }
})();
