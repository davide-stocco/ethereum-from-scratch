# State

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

## Questions this page should answer

- What exactly is "the state"? (A mapping from every address to that address's four fields.)
- Where does the state live? (Not in the blocks. Each node keeps its own copy and updates it as blocks arrive.)
- If the state isn't in the block, how do nodes agree on it? (The block header carries a **state root** — one 32-byte fingerprint of the entire state.)
- What does a contract's **storage** look like? (Its own private mapping of 32-byte slots to 32-byte values, fingerprinted as `storageRoot`.)
- What's the difference between *state* and *history*? (History is the chain of blocks. State is the current situation that history produced. You can discard history and still use the chain; you can't discard state.)

## Notes to self

- The state root is the hinge that connects accounts to blocks. It's worth being very clear here, because it's how a tiny block header commits to gigabytes of data.
- You need the [Merkle Patricia Trie](../technical/merkle-patricia-trie.md) for the *how*. On this page, only promise that a fingerprint exists and that any change to any account changes it.
- Worth stating: Ethereum's state is several hundred gigabytes and grows constantly. This is a real, ongoing design problem ("state growth") — and good motivation for the scaling section.

**Next:** [Transactions](../transactions/transactions.md)
