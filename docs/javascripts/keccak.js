/* ---------------------------------------------------------------------------
   Keccak-256, and the three tools on the Keccak page.
   ---------------------------------------------------------------------------
   Plain JavaScript, no dependencies. BigInt is used throughout because the
   permutation works on 64-bit lanes and JavaScript's bitwise operators are
   32-bit only.

   Rotation offsets and round constants are COMPUTED rather than typed out, so
   a transcription slip is impossible.

   This file SELF-TESTS on load against two published values. If either fails,
   every tool on the page reports an error instead of showing a hash — a hash
   function that is quietly wrong is worse than one that is visibly broken.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var M = (BigInt(1) << BigInt(64)) - BigInt(1);

  // --- round constants, via the LFSR in the specification -------------------
  function rcBit(t) {
    t %= 255;
    if (t === 0) return 1;
    var R = 1;
    for (var i = 0; i < t; i++) {
      R <<= 1;
      if (R & 0x100) R ^= 0x171;
      R &= 0xff;
    }
    return R & 1;
  }

  var RC = [];
  for (var i = 0; i < 24; i++) {
    var c = BigInt(0);
    for (var j = 0; j < 7; j++) {
      if (rcBit(j + 7 * i)) c ^= BigInt(1) << BigInt((1 << j) - 1);
    }
    RC.push(c);
  }

  // --- rho offsets, via the (x,y) walk in the specification -----------------
  var ROT = [];
  for (var a = 0; a < 5; a++) ROT.push([0, 0, 0, 0, 0]);
  (function () {
    var x = 1, y = 0;
    for (var t = 0; t < 24; t++) {
      ROT[x][y] = (((t + 1) * (t + 2)) / 2) % 64;
      var nx = y, ny = (2 * x + 3 * y) % 5;
      x = nx; y = ny;
    }
  })();

  function rol(v, n) {
    if (n === 0) return v;
    var b = BigInt(n);
    return ((v << b) | (v >> (BigInt(64) - b))) & M;
  }

  function keccakF(A) {
    for (var rnd = 0; rnd < 24; rnd++) {
      var C = [], D = [], x, y;
      for (x = 0; x < 5; x++) C.push(A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4]);
      for (x = 0; x < 5; x++) D.push(C[(x + 4) % 5] ^ rol(C[(x + 1) % 5], 1));
      for (x = 0; x < 5; x++) for (y = 0; y < 5; y++) A[x][y] ^= D[x];

      var B = [];
      for (x = 0; x < 5; x++) B.push([BigInt(0), BigInt(0), BigInt(0), BigInt(0), BigInt(0)]);
      for (x = 0; x < 5; x++) {
        for (y = 0; y < 5; y++) B[y][(2 * x + 3 * y) % 5] = rol(A[x][y], ROT[x][y]);
      }
      for (x = 0; x < 5; x++) {
        for (y = 0; y < 5; y++) {
          A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y] & M) & B[(x + 2) % 5][y]);
        }
      }
      A[0][0] ^= RC[rnd];
    }
    return A;
  }

  // pad 0x01 -> Keccak-256 (Ethereum).  pad 0x06 -> SHA3-256 (FIPS 202).
  function keccak(bytes, pad) {
    var rate = 136, x, y, i;
    var A = [];
    for (x = 0; x < 5; x++) A.push([BigInt(0), BigInt(0), BigInt(0), BigInt(0), BigInt(0)]);

    var msg = Array.prototype.slice.call(bytes);
    msg.push(pad);
    while (msg.length % rate !== 0) msg.push(0x00);
    msg[msg.length - 1] |= 0x80;

    for (var off = 0; off < msg.length; off += rate) {
      for (i = 0; i < rate / 8; i++) {
        var lane = BigInt(0);
        for (var k = 7; k >= 0; k--) lane = (lane << BigInt(8)) | BigInt(msg[off + i * 8 + k]);
        A[i % 5][Math.floor(i / 5)] ^= lane;
      }
      keccakF(A);
    }

    var out = [];
    for (i = 0; i < 4; i++) {
      var lane2 = A[i % 5][Math.floor(i / 5)];
      for (var b = 0; b < 8; b++) {
        out.push(Number((lane2 >> BigInt(8 * b)) & BigInt(0xff)));
      }
    }
    return out;
  }

  function toHex(bytes) {
    return bytes.map(function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
  }

  function utf8(str) {
    var out = [], enc = new TextEncoder().encode(str);
    for (var i = 0; i < enc.length; i++) out.push(enc[i]);
    return out;
  }

  function keccak256(text) { return toHex(keccak(utf8(text), 0x01)); }
  function sha3_256(text)  { return toHex(keccak(utf8(text), 0x06)); }

  // --- self-test ------------------------------------------------------------
  var OK =
    keccak256("") === "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470" &&
    sha3_256("")  === "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a";

  var FAIL = "<span class=\"tool__error\">This hasher failed its self-test " +
             "and has been disabled, because a wrong hash shown confidently " +
             "is worse than none. Please report it.</span>";

  // count differing bits between two hex strings of equal length
  function bitsDiffer(h1, h2) {
    var n = 0;
    for (var i = 0; i < h1.length; i++) {
      var v = parseInt(h1[i], 16) ^ parseInt(h2[i], 16);
      while (v) { n += v & 1; v >>= 1; }
    }
    return n;
  }

  function hasher() {
    var inp = document.getElementById("kec-in");
    var out = document.getElementById("kec-out");
    if (!inp || !out || inp.dataset.bound === "1") return;
    inp.dataset.bound = "1";

    function run() {
      if (!OK) { out.innerHTML = FAIL; return; }
      var h = keccak256(inp.value);
      out.innerHTML =
        "<code class=\"tool__hash\">0x" + h + "</code>" +
        "<span class=\"tool__hint\">" + inp.value.length + " characters in, " +
        "32 bytes out — always.</span>";
    }
    inp.addEventListener("input", run);
    run();
  }

  function avalanche() {
    var a = document.getElementById("av-a");
    var b = document.getElementById("av-b");
    var out = document.getElementById("av-out");
    if (!a || !b || !out || a.dataset.bound === "1") return;
    a.dataset.bound = "1";

    function run() {
      if (!OK) { out.innerHTML = FAIL; return; }
      var ha = keccak256(a.value), hb = keccak256(b.value);
      var same = [];
      for (var i = 0; i < ha.length; i++) same.push(ha[i] === hb[i]);
      function mark(h) {
        return h.split("").map(function (ch, i) {
          return same[i] ? ch : "<em class=\"tool__diff\">" + ch + "</em>";
        }).join("");
      }
      var chars = same.filter(function (s) { return !s; }).length;
      var bits = bitsDiffer(ha, hb);
      out.innerHTML =
        "<code class=\"tool__hash\">0x" + mark(ha) + "</code>" +
        "<code class=\"tool__hash\">0x" + mark(hb) + "</code>" +
        "<span class=\"tool__hint\"><strong>" + chars + " of 64</strong> hex " +
        "characters differ &nbsp;·&nbsp; <strong>" + bits + " of 256</strong> bits differ" +
        (a.value === b.value ? " — identical inputs give identical hashes, every time." : "") +
        "</span>";
    }
    a.addEventListener("input", run);
    b.addEventListener("input", run);
    run();
  }

  function versus() {
    var inp = document.getElementById("sha-in");
    var out = document.getElementById("sha-out");
    if (!inp || !out || inp.dataset.bound === "1") return;
    inp.dataset.bound = "1";

    function run() {
      if (!OK) { out.innerHTML = FAIL; return; }
      var k = keccak256(inp.value), s = sha3_256(inp.value);
      out.innerHTML =
        "<span class=\"tool__label\">Keccak-256 — what Ethereum uses</span>" +
        "<code class=\"tool__hash\">0x" + k + "</code>" +
        "<span class=\"tool__label\">SHA3-256 — the NIST standard</span>" +
        "<code class=\"tool__hash\">0x" + s + "</code>" +
        "<span class=\"tool__hint\">" + bitsDiffer(k, s) + " of 256 bits differ. " +
        "The two functions are identical apart from a single padding byte.</span>";
    }
    inp.addEventListener("input", run);
    run();
  }

  function run() { hasher(); avalanche(); versus(); }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else { run(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(run);
  }
})();
