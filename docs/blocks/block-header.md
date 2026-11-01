---
tier: 3
description: Field by field through a block header — and what each one commits to.
---

# The block header

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

!!! danger "Fork-dependent — verify before writing"

    The header field list has grown at several forks: `baseFeePerGas` in
    London, `withdrawalsRoot` in Shanghai, blob fields and the parent beacon
    block root in Cancun. **Write this page from the current specification**,
    not from any secondary source including this outline.

    <https://github.com/ethereum/execution-specs>

## Questions this page should answer

- What is in a header, and what does each field commit to?
- Which fields are **roots**, and what does each one fingerprint? (State, transactions, receipts, withdrawals.)
- Why is the header so small, when it commits to so much? (Because the roots do the work — see [the Merkle Patricia Trie](../encoding/merkle-patricia-trie.md).)
- Which fields are vestigial, kept only for compatibility after the switch to Proof of Stake?
- Which fields exist because of a specific fork, and what problem did each solve?

## Notes to self

- This is the most fork-volatile page on the site. Date-stamp it clearly and expect to revisit it after every upgrade.
- The vestigial fields are genuinely interesting — `difficulty` and `nonce` survive as fixed values, which tells a small story about how upgrades preserve compatibility. Good candidate for a `??? info "History"` box.
- One table, one row per field, with a "why it exists" column. That column is what makes this teaching material rather than a spec dump.

**Next:** [The chain and reorgs](the-chain.md)
