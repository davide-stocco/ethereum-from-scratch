---
tier: 1
---

# Public keys

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** secp256k1 has been Ethereum's curve since genesis.

## Questions this page should answer

- How do you get a public key from a private key? (Elliptic curve multiplication: multiply the curve's fixed generator point **G** by your private key.)
- What *is* a public key, concretely? (A point on a curve — an x coordinate and a y coordinate, 32 bytes each, so 64 bytes in total.)
- Why can't anyone reverse it? (The discrete logarithm problem: given the result, recovering the multiplier is infeasible. Easy one way, hopeless the other.)
- What's the difference between **compressed** (33 bytes) and **uncompressed** (64 or 65 bytes) form? (Given x, there are only two possible y values, so y can be dropped and recomputed.)
- Which form does Ethereum use for deriving addresses? (The 64-byte uncompressed form, **without** the `0x04` prefix byte — a detail that catches people out.)
- Why does `secp256k1` have that name, and why did Ethereum pick the same curve as Bitcoin?

## Notes to self

- Same discipline as [private keys](private-keys.md): teach the *property*, not the algebra. Readers need "one-way and deterministic" — not point addition.
- Worth stating plainly: your public key isn't published when you receive ether. Only your address is. The public key first becomes visible when you *send* something, because it's recovered from the signature.
- Carry the same example key through private key → public key → address across all three pages. One continuous worked example teaches far better than three disconnected ones.

**Next:** [Addresses](addresses.md)
