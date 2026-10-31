---
tier: 1
---

# Private keys

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** secp256k1 and 256-bit keys date from genesis.

## Questions this page should answer

- What *is* a private key? (Just a number — a random 256-bit integer.)
- How big is 2<sup>256</sup>, really? Give a concrete comparison so "unguessable" means something.
- What's the valid range, and why isn't it quite all 256-bit numbers? (Must be less than the secp256k1 curve order `n`.)
- How do you get a public key from it? (Multiply the curve's generator point by the private key — elliptic curve multiplication.)
- Why is that one-way? Easy forwards, infeasible backwards — the discrete logarithm problem.
- What does "owning" ether actually mean, given the state is public? (Knowing the one number that can produce valid signatures for that address.)

## Notes to self

- Don't try to teach elliptic curves properly. Teach the *property*: one-way, deterministic. Link out for the maths.
- Worth stating plainly: a private key isn't stored anywhere on the chain. The network never sees it.
- Mention seed phrases exist but are a *convenience layer* on top (BIP-39) — not part of Ethereum itself. Resist going down that road here.

**Next:** [Public keys](public-keys.md)
