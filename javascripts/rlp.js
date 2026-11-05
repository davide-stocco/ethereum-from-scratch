/* ---------------------------------------------------------------------------
   RLP: decode, encode, and explain.
   ---------------------------------------------------------------------------
   The engine for three pages. This one has the interactive tool; the
   transactions and block-header pages reuse `EFS.rlp.decode` to take a real
   example apart field by field, so the parsing lives here and those pages are
   presentation over it.

   Decoding is STRICT. Every canonicality rule is enforced and violations
   throw with a reason, because the whole argument for RLP existing is that
   one value has exactly one valid encoding. A lenient decoder would quietly
   accept the encodings the page says are impossible, which would undercut
   the page while appearing to support it.

   Verified on load against the published examples — "dog", ["cat","dog"],
   1024, the nested-list case and the 56-byte boundary — all of which were
   independently computed from the specification before being written here.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  var EFS = (window.EFS = window.EFS || {});

  function hexToBytes(h) {
    h = String(h).trim().replace(/^0x/i, "").replace(/[\s_]/g, "");
    if (h.length === 0) return new Uint8Array(0);
    if (h.length % 2 !== 0) throw new Error("odd number of hex digits");
    if (!/^[0-9a-fA-F]*$/.test(h)) throw new Error("not hexadecimal");
    var out = new Uint8Array(h.length / 2);
    for (var i = 0; i < out.length; i++) out[i] = parseInt(h.substr(i * 2, 2), 16);
    return out;
  }

  function bytesToHex(b) {
    var s = "";
    for (var i = 0; i < b.length; i++) s += ("0" + b[i].toString(16)).slice(-2);
    return s;
  }

  /* --- decode -------------------------------------------------------------
     Returns a node describing what was found and exactly which bytes carried
     it, so a caller can show the structure against the original hex:

       { kind: "string"|"list", start, headerEnd, end, note,
         payload: Uint8Array          (strings)
         items:   [node, ...]         (lists) }
  */
  function decodeItem(buf, pos) {
    if (pos >= buf.length) throw new Error("ran out of bytes at offset " + pos);
    var p = buf[pos];

    // 0x00-0x7f: the byte is its own encoding
    if (p <= 0x7f) {
      return { kind: "string", start: pos, headerEnd: pos, end: pos + 1,
               payload: buf.subarray(pos, pos + 1),
               note: "single byte below 0x80, so it stands for itself" };
    }

    // 0x80-0xb7: short string, length = p - 0x80
    if (p <= 0xb7) {
      var n = p - 0x80;
      var end = pos + 1 + n;
      if (end > buf.length) throw new Error("string at offset " + pos + " claims " + n + " bytes, and there aren't that many left");
      if (n === 1 && buf[pos + 1] <= 0x7f) {
        throw new Error("non-canonical at offset " + pos + ": the single byte 0x" +
          ("0" + buf[pos + 1].toString(16)).slice(-2) + " is below 0x80, so it must encode as itself, not with a length prefix");
      }
      return { kind: "string", start: pos, headerEnd: pos + 1, end: end,
               payload: buf.subarray(pos + 1, end),
               note: "short string: 0x" + p.toString(16) + " − 0x80 = " + n + " byte" + (n === 1 ? "" : "s") };
    }

    // 0xb8-0xbf: long string, next (p - 0xb7) bytes give the length
    if (p <= 0xbf) {
      var lenLen = p - 0xb7;
      if (pos + 1 + lenLen > buf.length) throw new Error("truncated length at offset " + pos);
      if (buf[pos + 1] === 0) throw new Error("non-canonical at offset " + pos + ": the length has a leading zero byte");
      var len = 0;
      for (var i = 0; i < lenLen; i++) len = len * 256 + buf[pos + 1 + i];
      if (len < 56) throw new Error("non-canonical at offset " + pos + ": length " + len + " is under 56, so it must use the short form");
      var e = pos + 1 + lenLen + len;
      if (e > buf.length) throw new Error("string at offset " + pos + " claims " + len + " bytes, and there aren't that many left");
      return { kind: "string", start: pos, headerEnd: pos + 1 + lenLen, end: e,
               payload: buf.subarray(pos + 1 + lenLen, e),
               note: "long string: 0x" + p.toString(16) + " − 0xb7 = " + lenLen +
                     " byte" + (lenLen === 1 ? "" : "s") + " of length, giving " + len };
    }

    // 0xc0-0xf7: short list, payload length = p - 0xc0
    if (p <= 0xf7) {
      var pl = p - 0xc0;
      var stop = pos + 1 + pl;
      if (stop > buf.length) throw new Error("list at offset " + pos + " claims " + pl + " bytes, and there aren't that many left");
      return { kind: "list", start: pos, headerEnd: pos + 1, end: stop,
               items: decodeRange(buf, pos + 1, stop),
               note: "short list: 0x" + p.toString(16) + " − 0xc0 = " + pl + " byte" + (pl === 1 ? "" : "s") + " of contents" };
    }

    // 0xf8-0xff: long list
    var ll = p - 0xf7;
    if (pos + 1 + ll > buf.length) throw new Error("truncated length at offset " + pos);
    if (buf[pos + 1] === 0) throw new Error("non-canonical at offset " + pos + ": the length has a leading zero byte");
    var plen = 0;
    for (var j = 0; j < ll; j++) plen = plen * 256 + buf[pos + 1 + j];
    if (plen < 56) throw new Error("non-canonical at offset " + pos + ": payload length " + plen + " is under 56, so it must use the short form");
    var stop2 = pos + 1 + ll + plen;
    if (stop2 > buf.length) throw new Error("list at offset " + pos + " claims " + plen + " bytes, and there aren't that many left");
    return { kind: "list", start: pos, headerEnd: pos + 1 + ll, end: stop2,
             items: decodeRange(buf, pos + 1 + ll, stop2),
             note: "long list: 0x" + p.toString(16) + " − 0xf7 = " + ll +
                   " byte" + (ll === 1 ? "" : "s") + " of length, giving " + plen };
  }

  function decodeRange(buf, from, to) {
    var out = [], pos = from;
    while (pos < to) {
      var node = decodeItem(buf, pos);
      if (node.end > to) throw new Error("item at offset " + pos + " runs past the end of its list");
      out.push(node);
      pos = node.end;
    }
    return out;
  }

  function decode(input) {
    var buf = (input instanceof Uint8Array) ? input : hexToBytes(input);
    if (buf.length === 0) throw new Error("nothing to decode");
    var node = decodeItem(buf, 0);
    if (node.end !== buf.length) {
      throw new Error("decoded one item ending at offset " + node.end +
                      ", but " + (buf.length - node.end) + " byte(s) follow it — RLP encodes exactly one item");
    }
    return node;
  }

  /* --- encode, for the worked examples ---------------------------------- */
  function encodeLength(n, offset) {
    if (n < 56) return [offset + n];
    var bytes = [];
    for (var v = n; v > 0; v = Math.floor(v / 256)) bytes.unshift(v % 256);
    return [offset + 55 + bytes.length].concat(bytes);
  }

  function encode(x) {
    var out = [];
    if (typeof x === "string") {
      var s = [];
      for (var i = 0; i < x.length; i++) s.push(x.charCodeAt(i) & 0xff);
      if (s.length === 1 && s[0] <= 0x7f) return new Uint8Array(s);
      return new Uint8Array(encodeLength(s.length, 0x80).concat(s));
    }
    if (x instanceof Uint8Array) {
      if (x.length === 1 && x[0] <= 0x7f) return x;
      return new Uint8Array(encodeLength(x.length, 0x80).concat(Array.prototype.slice.call(x)));
    }
    if (Array.isArray(x)) {
      for (var k = 0; k < x.length; k++) {
        out = out.concat(Array.prototype.slice.call(encode(x[k])));
      }
      return new Uint8Array(encodeLength(out.length, 0xc0).concat(out));
    }
    throw new Error("encode takes a string, a byte array, or a list of those");
  }

  EFS.rlp = { decode: decode, encode: encode, hexToBytes: hexToBytes, bytesToHex: bytesToHex };

  /* --- self-test against values computed from the specification ---------- */
  var VECTORS = [
    ["", "80"], ["dog", "83646f67"],
    [["cat", "dog"], "c88363617483646f67"],
    [[], "c0"], [[[], [[]], [[], [[]]]], "c7c0c1c0c3c0c1c0"],
    [new Uint8Array([0x0f]), "0f"], [new Uint8Array([0x80]), "8180"],
    [new Uint8Array([0x04, 0x00]), "820400"]
  ];
  var ok = true;
  try {
    for (var t = 0; t < VECTORS.length; t++) {
      if (bytesToHex(encode(VECTORS[t][0])) !== VECTORS[t][1]) { ok = false; break; }
      if (decode(VECTORS[t][1]).end !== hexToBytes(VECTORS[t][1]).length) { ok = false; break; }
    }
    // a 56-byte string must cross into the long form
    var long = new Uint8Array(56); long.fill(0x61);
    if (bytesToHex(encode(long)).indexOf("b838") !== 0) ok = false;
  } catch (e) { ok = false; }
  EFS.rlp.selfTestPassed = ok;

  /* --- the tool ----------------------------------------------------------- */
  function render(node, buf, depth) {
    var pad = "";
    for (var i = 0; i < depth; i++) pad += "    ";
    var head = bytesToHex(buf.subarray(node.start, node.headerEnd));
    var lines = [];
    var label = pad + "<span class=\"tool__rowlbl\">" +
      ("000" + node.start).slice(-3) + "</span>  ";
    if (node.kind === "list") {
      lines.push(label + "<strong>list</strong>" +
        (head ? " <span class=\"tool__hi\">" + head + "</span>" : "") +
        "  <span class=\"tool__faint\">" + node.note + "</span>");
      for (var j = 0; j < node.items.length; j++) {
        lines = lines.concat(render(node.items[j], buf, depth + 1));
      }
    } else {
      var hex = bytesToHex(node.payload);
      var printable = "";
      for (var k = 0; k < node.payload.length; k++) {
        var c = node.payload[k];
        printable += (c >= 0x20 && c < 0x7f) ? String.fromCharCode(c) : ".";
      }
      var shown = node.payload.length === 0 ? "<em>empty</em>" : hex;
      lines.push(label + "string " +
        (head ? "<span class=\"tool__hi\">" + head + "</span> " : "") +
        shown +
        (node.payload.length && /^[ -~]+$/.test(printable) ? " <span class=\"tool__faint\">&quot;" + printable + "&quot;</span>" : "") +
        "  <span class=\"tool__faint\">" + node.note + "</span>");
    }
    return lines;
  }

  function tool() {
    var inp = document.getElementById("rlp-in");
    var out = document.getElementById("rlp-out");
    if (!inp || !out || inp.dataset.bound === "1") return;
    inp.dataset.bound = "1";

    function run() {
      if (!EFS.rlp.selfTestPassed) {
        out.innerHTML = "<span class=\"tool__error\">This tool failed its self-test " +
          "against the published RLP examples and has been disabled rather than " +
          "showing a wrong result. Please report it.</span>";
        return;
      }
      var v = inp.value.trim();
      if (!v) { out.innerHTML = "<span class=\"tool__hint\">Paste some hex.</span>"; return; }
      try {
        var buf = hexToBytes(v);
        var node = decode(buf);
        out.innerHTML =
          "<span class=\"tool__label\">" + buf.length + " byte" + (buf.length === 1 ? "" : "s") + " in</span>" +
          "<code class=\"tool__hash tool__align\">" + render(node, buf, 0).join("\n") + "</code>" +
          "<span class=\"tool__hint\">The highlighted bytes are prefixes — structure, " +
          "not content. Everything else is the data itself.</span>";
      } catch (e) {
        out.innerHTML = "<span class=\"tool__error\">" + String(e.message) + "</span>" +
          "<span class=\"tool__hint\">A strict decoder rejects anything with more than " +
          "one possible meaning. That refusal is the whole point of the format.</span>";
      }
    }

    Array.prototype.forEach.call(document.querySelectorAll("[data-rlp]"), function (b) {
      if (b.dataset.bound === "1") return;
      b.dataset.bound = "1";
      b.addEventListener("click", function () { inp.value = b.getAttribute("data-rlp"); run(); });
    });

    inp.addEventListener("input", run);
    run();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", tool);
  } else { tool(); }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(tool);
  }
})();
