/* ---------------------------------------------------------------------------
   Seed phrase -> private keys -> addresses.  (BIP-39 + BIP-32 + BIP-44)
   ---------------------------------------------------------------------------
   Uses the browser's own PBKDF2-HMAC-SHA512 and HMAC-SHA512 via SubtleCrypto
   rather than a hand-written SHA-512. Less code, and no bespoke cryptography
   to get wrong. Reuses window.EFS.pubFromPriv (secp256k1.js) and
   keccak256Bytes (keccak.js) for the last two steps.

   Verified in Python before porting: the BIP-39 seed matches the published
   test vector, and m/44'/60'/0'/0/0 for the "abandon … about" mnemonic gives
   0x9858EfFD232B4033E47d90003D41EC34EcaEda94. This file re-checks the second
   of those on load and disables the tool if it fails.

   SubtleCrypto needs a secure context. localhost counts as one, as does the
   published https site.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var N = BigInt("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141");
  var HARD = 0x80000000;

  function ready() {
    return window.EFS && window.EFS.pubFromPriv && window.EFS.keccak256Bytes &&
           window.crypto && window.crypto.subtle;
  }

  function utf8(s) { return new TextEncoder().encode(s.normalize("NFKD")); }
  function hex(b) {
    return Array.prototype.map.call(b, function (x) {
      return ("0" + x.toString(16)).slice(-2);
    }).join("");
  }
  function toBig(bytes) {
    var v = BigInt(0);
    for (var i = 0; i < bytes.length; i++) v = (v << BigInt(8)) | BigInt(bytes[i]);
    return v;
  }
  function from32(v) {
    var out = new Uint8Array(32);
    for (var i = 31; i >= 0; i--) { out[i] = Number(v & BigInt(0xff)); v >>= BigInt(8); }
    return out;
  }

  // --- BIP-39: mnemonic -> 64-byte seed ------------------------------------
  function bip39Seed(mnemonic, passphrase) {
    return crypto.subtle
      .importKey("raw", utf8(mnemonic), "PBKDF2", false, ["deriveBits"])
      .then(function (key) {
        return crypto.subtle.deriveBits({
          name: "PBKDF2",
          salt: utf8("mnemonic" + (passphrase || "")),
          iterations: 2048,
          hash: "SHA-512"
        }, key, 512);
      })
      .then(function (bits) { return new Uint8Array(bits); });
  }

  function hmac512(keyBytes, dataBytes) {
    return crypto.subtle
      .importKey("raw", keyBytes, { name: "HMAC", hash: "SHA-512" }, false, ["sign"])
      .then(function (k) { return crypto.subtle.sign("HMAC", k, dataBytes); })
      .then(function (sig) { return new Uint8Array(sig); });
  }

  // --- BIP-32 --------------------------------------------------------------
  function masterNode(seed) {
    return hmac512(utf8("Bitcoin seed"), seed).then(function (I) {
      return { k: toBig(I.slice(0, 32)), c: I.slice(32) };
    });
  }

  function serPub(k) {
    var pt = window.EFS.pubFromPriv(k);
    var x = from32(pt[0]);
    var out = new Uint8Array(33);
    out[0] = (pt[1] & BigInt(1)) === BigInt(0) ? 2 : 3;
    out.set(x, 1);
    return out;
  }

  function childNode(node, index) {
    var data;
    if (index >= HARD) {
      data = new Uint8Array(37);
      data[0] = 0;
      data.set(from32(node.k), 1);
    } else {
      data = new Uint8Array(37);
      data.set(serPub(node.k), 0);
    }
    // big-endian index in the last four bytes
    data[33] = (index >>> 24) & 0xff;
    data[34] = (index >>> 16) & 0xff;
    data[35] = (index >>> 8) & 0xff;
    data[36] = index & 0xff;

    return hmac512(node.c, data).then(function (I) {
      return { k: (toBig(I.slice(0, 32)) + node.k) % N, c: I.slice(32) };
    });
  }

  function derivePath(node, parts) {
    return parts.reduce(function (p, part) {
      return p.then(function (n) {
        var hard = /'$/.test(part);
        var i = parseInt(part.replace(/'$/, ""), 10) + (hard ? HARD : 0);
        return childNode(n, i);
      });
    }, Promise.resolve(node));
  }

  function addressOf(k) {
    var pt = window.EFS.pubFromPriv(k);
    var pub = [];
    var xb = from32(pt[0]), yb = from32(pt[1]);
    for (var i = 0; i < 32; i++) pub.push(xb[i]);
    for (i = 0; i < 32; i++) pub.push(yb[i]);
    return "0x" + window.EFS.keccak256Bytes(pub).slice(24);
  }

  // --- self-test -----------------------------------------------------------
  var VECTOR_M = "abandon abandon abandon abandon abandon abandon abandon " +
                 "abandon abandon abandon abandon about";
  var VECTOR_A = "0x9858effd232b4033e47d90003d41ec34ecaeda94";
  var selfTest = null;

  function checkOnce() {
    if (selfTest) return selfTest;
    selfTest = bip39Seed(VECTOR_M, "")
      .then(masterNode)
      .then(function (n) { return derivePath(n, ["44'", "60'", "0'", "0", "0"]); })
      .then(function (n) { return addressOf(n.k).toLowerCase() === VECTOR_A; })
      .catch(function () { return false; });
    return selfTest;
  }

  function tool() {
    var mn = document.getElementById("hd-phrase");
    var pw = document.getElementById("hd-pass");
    var out = document.getElementById("hd-out");
    if (!mn || !out || mn.dataset.bound === "1") return;
    mn.dataset.bound = "1";

    var token = 0;

    function run() {
      var mine = ++token;
      if (!ready()) {
        out.innerHTML = "<span class=\"tool__error\">A dependency is unavailable, " +
                        "so this tool is disabled rather than showing a wrong result.</span>";
        return;
      }
      var phrase = mn.value.trim().replace(/\s+/g, " ");
      if (!phrase) { out.innerHTML = "<span class=\"tool__hint\">Enter a phrase.</span>"; return; }
      out.innerHTML = "<span class=\"tool__hint\">Deriving…</span>";

      checkOnce().then(function (ok) {
        if (!ok) {
          out.innerHTML = "<span class=\"tool__error\">This tool failed its " +
                          "self-test against the published BIP-39 vector and has " +
                          "been disabled. Please report it.</span>";
          return;
        }
        var seedHex;
        return bip39Seed(phrase, pw ? pw.value : "")
          .then(function (seed) {
            seedHex = hex(seed);
            return masterNode(seed);
          })
          .then(function (n) { return derivePath(n, ["44'", "60'", "0'", "0"]); })
          .then(function (account) {
            var jobs = [];
            for (var i = 0; i < 5; i++) {
              jobs.push(childNode(account, i).then(function (c) { return c.k; }));
            }
            return Promise.all(jobs);
          })
          .then(function (keys) {
            if (mine !== token) return;   // a newer run superseded this one
            var words = phrase.split(" ").length;
            var rows = keys.map(function (k, i) {
              return "<span class=\"tool__label\">m/44'/60'/0'/0/" + i + "</span>" +
                     "<code class=\"tool__hash\">" + addressOf(k) +
                     "<span class=\"tool__faint\">  ·  key " +
                     from32(k)[0].toString(16).padStart(2, "0") + "…</span></code>";
            }).join("");
            out.innerHTML =
              "<span class=\"tool__label\">The 64-byte seed your phrase becomes</span>" +
              "<code class=\"tool__hash\">" + seedHex + "</code>" +
              "<span class=\"tool__hint\">" + words + " words in, 512 bits out. " +
              "Every key below comes from this one value.</span>" +
              rows +
              "<span class=\"tool__hint\">Five different keys, five different " +
              "addresses, one phrase — and the same five on any wallet that " +
              "follows the same path.</span>";
          });
      }).catch(function () {
        if (mine !== token) return;
        out.innerHTML = "<span class=\"tool__error\">Derivation failed in this browser.</span>";
      });
    }

    mn.addEventListener("input", run);
    if (pw) pw.addEventListener("input", run);
    run();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", tool);
  } else { tool(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(tool);
  }
})();
