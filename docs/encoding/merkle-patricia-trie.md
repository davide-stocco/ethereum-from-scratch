---
tier: 2
description: How Ethereum fingerprints its entire state in 32 bytes, so a block header can commit to gigabytes of data.
---

# The Merkle Patricia Trie

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

!!! info "Current as of: _(fill in the fork and date)_"

    The trie structure is unchanged since genesis, but a replacement — Verkle
    trees — is actively planned. Check the current status before relying on
    this page.

## Questions this page should answer

- What problem does it solve? (Committing to a huge mapping with a single 32-byte value, such that any change to any entry changes the fingerprint.)
- What's a **Merkle tree** first, and what does it let you prove?
- Why a **trie** as well? (The keys matter: you need to look things up by address, not just verify a list.)
- What does "Patricia" add? (Path compression — collapsing long stretches of shared prefix so the structure stays shallow.)
- What are the node types, and why are there several?
- What is a **proof**, and why does it matter that proofs are small? (It's how a light client verifies a balance without holding the state.)
- Where does Ethereum use this? (The state root, each account's storage root, the transactions root, the receipts root.)
- Why is [RLP](rlp.md) a prerequisite? (Nodes are RLP-encoded before hashing, so canonical encoding is what makes the root well-defined.)

## Notes to self

- The hardest page in the Encoding section. Build it up in the order above — Merkle, then trie, then compression — and resist starting from the finished structure.
- A diagram is essential. Possibly several, one per step.
- Be clear about *why* anyone should care: it's what lets a 500-byte block header commit to hundreds of gigabytes of state, and what makes light clients possible.
- Verkle trees are the reason this is Tier 2. Mention the plan, don't chase it.

**Next:** [Accounts](../accounts/accounts.md)
