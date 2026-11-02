/* ---------------------------------------------------------------------------
   Interactive converters.
   ---------------------------------------------------------------------------
   Plain JavaScript, no dependencies. Each tool checks for its own elements
   and does nothing if they aren't on the page, so this file is safe to load
   site-wide.

   Everything uses BigInt rather than Number. That matters here: an address is
   160 bits and a hash is 256, both far beyond the 53 bits a JavaScript Number
   can hold exactly. BigInt has no such limit.
   --------------------------------------------------------------------------- */

(function () {
  "use strict";

  function baseConverter() {
    var dec = document.getElementById("conv-dec");
    var hex = document.getElementById("conv-hex");
    var bin = document.getElementById("conv-bin");
    var out = document.getElementById("conv-out");
    if (!dec || !hex || !bin || !out) return; // tool not on this page

    // Material swaps pages without reloading and re-runs this file, so guard
    // against binding the same listeners twice.
    if (dec.dataset.bound === "1") return;
    dec.dataset.bound = "1";

    // Render the byte breakdown for a value.
    function describe(value) {
      if (value === null) {
        out.innerHTML = "";
        return;
      }
      var h = value.toString(16);
      if (h.length % 2 === 1) h = "0" + h; // whole bytes only
      var pairs = h.match(/../g) || ["00"];
      var label = pairs.length === 1 ? "byte" : "bytes";
      out.innerHTML =
        "<strong>" + pairs.length + " " + label + "</strong>: " +
        pairs.map(function (p) { return "<code>" + p + "</code>"; }).join(" ") +
        "<span class=\"tool__hint\">" + value.toString(10) +
        " &nbsp;=&nbsp; 0x" + h +
        " &nbsp;=&nbsp; " + value.toString(2) + "</span>";
    }

    function error(field, message) {
      field.classList.add("tool__input--bad");
      out.innerHTML = "<span class=\"tool__error\">" + message + "</span>";
    }

    function clearErrors() {
      [dec, hex, bin].forEach(function (f) {
        f.classList.remove("tool__input--bad");
      });
    }

    // Parse one field and push the result into the other two.
    function update(source) {
      clearErrors();
      var raw = source.value.trim();

      if (raw === "") {
        [dec, hex, bin].forEach(function (f) { if (f !== source) f.value = ""; });
        describe(null);
        return;
      }

      var value;
      try {
        if (source === dec) {
          if (!/^[0-9]+$/.test(raw)) throw new Error("Decimal takes digits 0-9 only.");
          value = BigInt(raw);
        } else if (source === hex) {
          var h = raw.replace(/^0[xX]/, "");
          if (!/^[0-9a-fA-F]+$/.test(h)) throw new Error("Hex takes 0-9 and a-f only.");
          value = BigInt("0x" + h);
        } else {
          if (!/^[01]+$/.test(raw)) throw new Error("Binary takes 0 and 1 only.");
          value = BigInt("0b" + raw);
        }
      } catch (e) {
        error(source, e.message);
        return;
      }

      if (source !== dec) dec.value = value.toString(10);
      if (source !== hex) hex.value = "0x" + value.toString(16);
      if (source !== bin) bin.value = value.toString(2);
      describe(value);
    }

    [dec, hex, bin].forEach(function (field) {
      field.addEventListener("input", function () { update(field); });
    });

    // Start with the worked example from the page above.
    hex.value = "0x1234";
    update(hex);
  }

  function run() {
    baseConverter();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }

  // Material loads pages without a full reload, so re-initialise on navigation.
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(run);
  }
})();
