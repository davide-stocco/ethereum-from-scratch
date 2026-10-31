# Keccak-256

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** Ethereum's hash function since genesis. Everything from addresses to the state root depends on it, so it cannot be changed.

## Questions this page should answer

- What does a hash function do? (Any input, however large → a fixed 32-byte output.)
- What are the four properties that make it useful?
    - **Deterministic** — same input always gives the same output
    - **One-way** — you can't work backwards from the output
    - **Avalanche** — change one bit of input, and roughly half the output bits flip
    - **Collision-resistant** — nobody can find two inputs with the same output
- Why is it called *Keccak* and not *SHA-3*, when they're nearly the same? (Ethereum adopted Keccak before SHA-3 was finalised; the standard then changed its padding. Ethereum kept the original. So `keccak256("")` and `sha3_256("")` give **different** answers — a genuine source of bugs.)
- Where does Ethereum use it? Worth listing, because it's everywhere:
    - Deriving an [address](addresses.md) from a public key
    - [EIP-55](addresses.md) address checksums
    - Transaction and block hashes
    - Function selectors in the ABI
    - Every key in the state and storage tries
- What does it *not* do? (It isn't encryption — nothing is ever recovered from a hash. It isn't random — it's completely predictable.)

## Notes to self

- Don't explain the sponge construction. Explain the *properties*, and link out for internals. The properties are what every later page actually relies on.
- Demonstrate avalanche concretely: hash `hello`, then `hellp`, and show the two outputs side by side. That single example does the teaching.
- The Keccak-vs-SHA-3 confusion is worth real space — it trips up almost everyone, and nowhere explains it clearly.
- Prime candidate for an interactive hasher widget later.

**Next:** [Private keys](private-keys.md)
