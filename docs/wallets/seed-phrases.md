---
tier: 1
description: What a wallet actually is, and how one phrase can stand behind thousands of private keys.
---

# Wallets and seed phrases

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** These are conventions above the protocol, and the protocol has never defined them.

## Questions this page should answer

- What *is* a wallet? (Not a container of money. A keeper of keys — the money is state on the chain, and the wallet holds the authority to move it.)
- Why don't wallets just store one private key?
- What is a **seed phrase**, and how do 12 or 24 ordinary words encode a 256-bit secret?
- How does one seed produce **many** keys? (A deterministic tree, so every key is derived from the seed by a repeatable procedure.)
- What is a **derivation path**, and why do two wallets sometimes show different addresses for the same seed?
- Why words rather than a hex string? (Transcribable by hand, and the wordlist makes most typos detectable.)
- **None of this is Ethereum.** Seed phrases come from a Bitcoin standard the rest of the ecosystem adopted. Ethereum sees only keys and signatures.

## Notes to self

- The last point matters and is nearly always skipped: a beginner assumes seed phrases are part of Ethereum. They're a usability layer, which is *why* two wallets can disagree about what your addresses are.
- Name BIP-39 and BIP-44 and cite them, but don't walk through the derivation. The reader needs the shape, not the algorithm.
- Resist giving security advice. Explain the mechanism and what it implies; "never share your seed phrase" follows from the mechanism without being preached.

## References to work from

Verify before citing.

- BIP-39, *Mnemonic code for generating deterministic keys.*
- BIP-32 / BIP-44, hierarchical deterministic wallets and derivation paths.

**Next:** [What losing your keys means](losing-your-keys.md)
