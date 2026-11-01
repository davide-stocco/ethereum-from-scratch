---
tier: 1
description: How a signature proves you hold a private key, and how the sender's address is recovered from it rather than stated.
---

# Signatures

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** ECDSA over secp256k1, unchanged since genesis.

## Questions this page should answer

- What does a signature actually prove? (That whoever produced it knew the private key — without revealing it.)
- What are `v`, `r` and `s`, the three values a transaction carries?
- What is **signature recovery**, and why is it the surprising part? (The sender's address appears nowhere in a transaction. It's *recovered* from the signature and the signed data.)
- What exactly gets signed? (A hash of the transaction's contents — so changing any field invalidates the signature.)
- Why does `v` exist at all? (Two public keys can produce the same `r`; `v` picks which one. It also encodes the chain id, which is what stops a transaction being replayed on a different network.)
- What is **malleability**, and why is `s` restricted to the lower half of its range?
- Can you sign something that isn't a transaction? (Yes — message signing, which is how "log in with your wallet" works. No gas, no chain involvement.)

## Notes to self

- The recovery point is the one to lead with. Everyone assumes a transaction says who sent it. It doesn't, and that's genuinely elegant: the signature *is* the claim of identity.
- Don't derive ECDSA. State what it guarantees and link out, same discipline as [private keys](private-keys.md).
- A worked example is worth more than the algebra: take a signed transaction, recover the address, show it matches.
- Replay protection via chain id connects to [the nonce](../accounts/nonce.md) — the nonce stops replay on the *same* chain, chain id stops it across chains. Worth stating together.
- Natural candidate for an interactive tool later: paste a signature, recover the signer.

**Next:** [Wallets and seed phrases](../wallets/seed-phrases.md)
