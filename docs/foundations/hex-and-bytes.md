---
tier: 1
---

# Hex and bytes

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** This isn't even an Ethereum rule — it's how computers represent data.

## Questions this page should answer

- What is a **byte**, and why is 8 bits the unit everything is measured in?
- What is **hexadecimal**, and why use base 16 instead of decimal? (One byte is exactly two hex characters — `00` to `ff`. The mapping is clean, which decimal isn't.)
- Why does everything in Ethereum start with `0x`? (A convention meaning "what follows is hex." Not part of the value.)
- How do you read the lengths you'll see constantly?
    - 20 bytes = 40 hex characters = an address
    - 32 bytes = 64 hex characters = a hash, or one storage slot
- What's the difference between `0x1234` as a **number** (4,660) and as **bytes** (the two bytes `0x12` and `0x34`)? Why does that distinction cause bugs?
- What does **big-endian** mean, and why does it matter that Ethereum uses it?

## Notes to self

- Short page. It exists so later pages can say "32 bytes" without stopping to explain.
- A hex ⇄ decimal ⇄ bytes table for `0`–`15` is worth including; everything else follows from it.
- Count the characters in a real address on screen so "40 hex characters" stops being abstract.
- Good candidate for an interactive converter widget later.

**Next:** [Keccak-256](../crypto/keccak256.md)
