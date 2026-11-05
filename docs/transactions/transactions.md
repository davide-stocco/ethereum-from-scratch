---
tier: 2
---

# Transactions

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

## Questions this page should answer

- What is a transaction, in one sentence? (A signed instruction from an EOA to change the state.)
- What's inside one?
    - `nonce` — a counter for the sender
    - `gasLimit` — the most work you'll pay for
    - `to` — the recipient, or empty to deploy a contract
    - `value` — how much ether to send, in wei
    - `data` — arbitrary bytes; this is how you call a contract
    - `maxFeePerGas` / `maxPriorityFeePerGas` — what you'll pay
    - `v`, `r`, `s` — the signature
- Where does the *sender's* address live in all that? (Nowhere! It's recovered from the signature. Worth making a point of — it surprises everyone.)
- What are the three things a transaction can do? (Send ether, call a contract, create a contract.)
- What's a transaction *hash*, and when does it exist? (As soon as it's signed — before anyone has accepted it.)
- What does it mean for a transaction to fail? (It still happened, still cost gas, but the state changes were reverted.)

## Already written: moved here from the state page

This was on [state](../accounts/state.md), where it needed a mempool to make
its argument and so arrived before the reader had one. It belongs here. Build
the surrounding section around it; the heading can stay as it is.

### A transaction doesn't name the state it expects

The natural question, once roots are in view: when you sign a transaction, which state root is it computed against? And should it carry that root, so the network knows what you assumed?

**It carries no state root, and no reference to one.** A transaction holds a nonce, a recipient, a value, some data, gas limits, fee terms, a chain id and a signature — the field list above goes through them. Nothing in it describes the state it expects to meet.

So a transaction is an **instruction, not a statement about the world.** It says what to do. It says nothing about what it assumes.

The single exception is the [nonce](../accounts/nonce.md), and it's a revealing one. The nonce *is* a claim about state — "my account has sent exactly this many transactions" — but it constrains only your own account's position in its own sequence. About every other account, every balance and every contract's storage, your transaction is silent.

#### What yours actually runs against

If it lands in block N, it executes against the state at the end of block N−1, plus the effects of every transaction ordered before it **within** block N.

That intermediate state is perfectly real, and **no root is published for it.** Ethereum commits to the state once per block, after all of it has run — which is the second of the two simplifications flagged back on [What is Ethereum?](../foundations/what-is-ethereum.md).

??? info "History: it used to publish one per transaction"

    This is not how it always worked, and the change is instructive.

    Until the Byzantium upgrade in 2017, every transaction **receipt** carried
    the state root as of that transaction — a published commitment after each
    one, not just each block. **EIP-658** [(Johnson, 2017)](#ref-eip658)
    replaced that field with a plain status code: `1` for success, `0` for
    failure.

    The reason was cost against benefit. Computing an intermediate root per
    transaction is real work for every node, and almost nothing used the
    result, whereas *did this transaction succeed?* was the question everyone
    actually asked and previously had to infer.

    So Ethereum once offered exactly the per-transaction commitment this
    section says doesn't exist, looked at the price, and sold it for a single
    bit of far more useful information.

#### Why you shouldn't want to send one

It sounds safer to pin the state you signed against. It would be close to unusable.

A transaction naming a required state root would be invalidated by **any** change anywhere in the state — one unrelated transfer, by a stranger, in the same block. Since the state changes every block and thousands of transactions compete for each one, yours would have a useful life of a few seconds and would usually miss. A **mempool** — the pool of broadcast transactions waiting their turn — could not work at all, because waiting is exactly what would kill them.

So state-agnosticism is deliberate: it's what lets a transaction sit in a queue and remain valid. The bill arrives elsewhere, though, and it's worth knowing where:

- **You cannot pin the conditions you'll meet.** The state your transaction executes against is whatever exists at inclusion, not what existed when you signed.
- **Which is why contracts add their own guards.** Deadlines after which a call reverts, minimum amounts a trade must return — those exist because the protocol declines to offer them.
- **And it's the gap between simulating and executing.** A wallet shows you the outcome against the state as it stands now; the real outcome is against the state at inclusion, which nobody can predict. Much of what gets called front-running lives in that gap — which is this page's territory.

## Notes to self

- Decode one real transaction field by field. That single worked example
  teaches more than any amount of prose.

- **Make it a tool, and make it prove itself.** Embed the raw bytes of an
  actual transaction, decode them in the browser with the [RLP](../encoding/rlp.md)
  decoder, then **hash the bytes and show the result equals the published
  transaction hash**. The reader isn't told the example is real — they watch
  it check out. Nothing else on the site can do that.

  Hard-coded bytes, not a live API: it then works offline, cannot break when
  somebody's endpoint dies, and makes no request that reveals who is reading.

- **Second tool: validation, split by what it needs.** This is the stronger
  one, because the split is the lesson.

    - **Stateless checks** compute for real in the browser — does the RLP
      parse, does the signature recover to an address, is the chain id right,
      does it cover intrinsic gas?
    - **Stateful checks** need the state, which a static site doesn't have. So
      let the reader *supply* it: two inputs for the account's nonce and
      balance.

    The tool then reports **accept or reject, and which check failed** — which
    turns the four steps on [what a node is](../nodes/what-a-node-is.md) into
    something you operate, and teaches the stateless/stateful distinction by
    making you provide one half of it.
- Don't explain the signature maths here — point at the signatures page.
- The `data` field is the gateway to the whole EVM section. Flag it as important and move on.

**Next:** [Why metering is necessary](why-metering.md)

## References

<div class="sources" markdown>

- <a id="ref-eip658"></a>**Johnson, N.** (2017). *EIP-658: Embedding transaction status code in receipts.* Ethereum Improvement Proposals. Activated in Byzantium; replaced the per-transaction intermediate state root in receipts with a status code. <https://eips.ethereum.org/EIPS/eip-658>

</div>
