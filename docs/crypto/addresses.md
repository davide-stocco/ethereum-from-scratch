---
tier: 1
---

# Addresses

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** Address derivation and EIP-55 checksums have never changed.

## Questions this page should answer

- How do you get from a public key to an address? (Keccak-256 the 64-byte public key, keep the **last 20 bytes**.)
- Why 20 bytes / 40 hex characters, when the hash is 32 bytes?
- Why does every address start with `0x`? (It's just the convention for "this is hexadecimal" — not part of the address.)
- What is the mixed-case capitalisation about? (EIP-55 checksum: the capitalisation itself encodes a checksum, so typos are detectable. An all-lowercase address is still valid.)
- Why do contract addresses look identical to normal ones, and how are they derived differently? (From the creator's address and [nonce](../accounts/nonce.md "A per-account counter of transactions already sent"), not from a public key.)
- Can an address exist before anyone has used it? (Yes — all 2<sup>160</sup> of them exist in principle, holding nothing.)

## Notes to self

- Needs [Keccak-256](keccak256.md) — but only the *fact* that it's a hash function, which that page covers first.
- A worked example with real bytes at each step is the whole value of this page. Carry forward the same key used on [private keys](private-keys.md) and [public keys](public-keys.md).
- Good candidate for an interactive widget later: paste a public key, watch the address come out.

**Next:** [RLP encoding](../encoding/rlp.md)
