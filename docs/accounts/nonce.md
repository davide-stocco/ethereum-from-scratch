---
tier: 1
---

# The nonce

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** Nonce semantics have never been revised.

## Questions this page should answer

- What is the nonce? (A per-account counter: how many transactions this account has already sent. Starts at 0, not 1.)
- What problem does it solve? (Replay. Without it, a signed transaction is a reusable cheque — anyone could rebroadcast your 1-ether payment a hundred times, and every copy would be perfectly valid.)
- Why doesn't Bitcoin need one? (A UTXO can only be spent once, so the coin itself provides the protection. [Accounts](accounts.md) have no such property, so a counter supplies it.)
- Why must nonces be used strictly in order, with no gaps? (A transaction with nonce 7 is simply invalid until nonce 6 has been included.)
- Why does that make transactions get **stuck**? (One underpriced transaction blocks every later transaction from the same account, however much they offer.)
- How do you fix a stuck transaction? (Replace it — resubmit the *same nonce* with a higher fee.)
- Contract accounts have a nonce too. What does it count there? (How many contracts that account has created.)

## Notes to self

- The "stuck transaction" section is the most practically useful thing on this page. Everyone who has used Ethereum has hit this and not understood why.
- A diagram of a queue with a gap in it would land well.
- Keep fees out of this page. You'll want to say "underpriced", which is enough — the fee market isn't published yet and isn't fork-proof. Say "a fee too low for anyone to include it" and move on.
- Ordering note: this page needs only the one-sentence notion of a transaction already given in [What is Ethereum?](../foundations/what-is-ethereum.md) — an instruction that changes the state. Resist explaining transaction anatomy here.

**Next:** [State](state.md)
