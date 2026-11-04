---
tier: 1
description: Accounts persist where coins are consumed — which is what makes programs possible, and what every awkward thing about Ethereum is the price of.
---

# Why accounts, and what they cost

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** The choice was made before genesis and has never been revisited. The *responses* to its costs are live engineering and belong in [fork-dependent details](../reference/gas-costs.md).

## The thesis this page exists to argue

**Persistence buys programmability, and everything awkward about Ethereum is the invoice.**

A coin is consumed and gone, so there is nowhere to attach lasting storage or code. An account is a permanent place with an address, so a balance, a counter, storage and a program can all live there. Contracts are not an addition to the account model — they are downstream of it. Write the page so that a reader finishes knowing the trade was deliberate and cost real things.

## Questions this page should answer

**What the model buys**

- Why can't Bitcoin hold a program? (Nothing persists for one to live in. This is the whole answer and it should land early.)
- What else does persistence enable? (Names, token balances, reputation, lending positions — an address accumulates history. Same property as the privacy cost, seen from the other side.)
- Why is composability a consequence rather than a feature? (Contracts can hold and move each other's balances because accounts are addressable and survive between transactions.)

**What it costs**

- Why does order suddenly matter? (Two transactions from one account each depend on what the other leaves behind — hence the [nonce](nonce.md), and hence head-of-line blocking, which UTXO wallets don't have.)
- Why does [state](state.md) only ever grow? (A UTXO is consumed and vanishes; an account persists. The state has no mechanism for shrinking.)
- Why is parallel execution hard? (Transactions touching separate UTXOs are independent. Transactions touching one account are a sequence.)
- Why does reusing an address cost you privacy? (A persistent account accumulates a linkable history by design. Picks up the loose thread on [public keys](../crypto/public-keys.md) — "the old advice not to reuse addresses had some substance to it".)
- Why must fees be paid in ether specifically? (A UTXO fee comes out of the inputs being spent. An account needs a separate ether balance — which is the stuck-tokens situation on [ether](../foundations/ether.md), and the reason paymasters exist.)
- Why can anyone make every node store more? (Send dust to a million addresses. EIP-161 on the [accounts](accounts.md) page is the first patch applied to this.)

**What it quietly avoids** — counter-intuitive, so give it a section

- No **dust**: a tiny UTXO becomes unspendable once the fee to move it exceeds its value. A balance is one number, so no fragment of it can be stranded.
- No **coin selection**: Bitcoin wallets run algorithms to choose inputs. Ethereum wallets have no such code.
- No **change addresses**, and none of the machinery around them.
- **Constant-size transfers**: a Bitcoin transaction grows with its input count, so consolidating small coins is expensive. An Ethereum transfer is one size.
- **Cheap balance proofs**: "address X holds Y" is a short proof against the state root. Bitcoin commits to no UTXO set, so a light client cannot do the equivalent.

**The economics** — likely the strongest section for a reader from outside

- Why is permanent storage mispriced? (**You pay once to write state. Every node then stores it forever.** A one-time fee against a perpetual liability, borne by parties who never agreed to it and cannot charge for it.)
- So what is "state growth" really? (Not an engineering nuisance — a mispriced commons. That reframing is the point of the section.)
- What are the responses? (Three classes, named as classes and not as products: charging **rent** for occupied state, **expiring** state left untouched, and **statelessness** — removing the need for validators to hold the state at all.)

## Notes to self

- **Lead with the benefit.** An earlier draft of this outline was a list of costs, which is the wrong shape: the costs are only interesting because of what they buy. The invoice metaphor is worth keeping explicit.
- **Present privacy and identity as one property, not two.** An address that accumulates history is exactly what makes both lending and surveillance possible. A page that treats them as separate items is hiding the trade.
- **Keep the response classes fork-proof.** Which of rent, expiry or statelessness ships is volatile; that the problem exists is permanent. Name mechanism classes, never products — the standing rule in [FORKS.md](../about/forks.md).
- **A comparison table across dimensions** would summarise well, but write the prose first. A table alone reads as a scorecard and this is a trade, not a contest.
- **One history box**: Buterin's white paper weighs the two models explicitly and credits UTXO's real advantages — privacy, parallelism, light-client payment proofs. Quote the trade as the designers saw it in 2014 rather than presenting accounts as obviously correct.
- **Out of scope deliberately.** MEV, although shared mutable state amplifies it — it needs blocks and ordering, and [blocks](../blocks/blocks.md) claims it. Token approvals too: an ERC-level consequence that belongs with [contracts](../contracts/smart-contracts.md).
- This page ends the Accounts and state section, so it can lean on all three pages before it. It is also the natural place to send a reader who asks "why is Ethereum like this?" rather than "how does Ethereum work?".

**Next:** [RLP encoding](../encoding/rlp.md) — how Ethereum writes structured data down.
