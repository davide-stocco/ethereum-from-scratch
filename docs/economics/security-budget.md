---
tier: 1
description: Why a blockchain has to pay someone, continuously, to order its transactions — and what that payment buys.
---

# Why security has to be paid for

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** The requirement is structural: it follows from the design, not from any particular fork's rules.

This is the **root** of the Economics section. Everything else here depends on it, so it's worth getting exactly right.

## The argument to make

The chain of reasoning, which the page should establish in order:

1. Someone has to decide the **order** of transactions. The [state machine](../foundations/what-is-ethereum.md) is deterministic given an order, so ordering is the only genuinely contested decision in the system.
2. Whoever holds that power could **abuse it** — reorder, exclude, or rewrite recent history.
3. So the system must make abuse **more expensive than it's worth**.
4. Making it expensive means the honest work has to be **rewarded**, continuously. An unpaid network is a cheap network to capture.
5. Therefore **security is a recurring cost**, not a one-off property. It has to be paid for every block, forever.

## Questions this page should answer

- What is actually being bought? Not secrecy, not correctness of computation — **ordering that is expensive to change.**
- Why can't security be a one-time investment? What makes it a flow rather than a stock?
- What determines how much security is enough? (Roughly: the cost of attacking must exceed the gain from attacking. Both sides of that are hard to measure, which is itself worth saying.)
- Where does the money come from? Only two possible sources — see [who pays](who-pays.md).
- What's the relationship between the **value secured** and the **amount paid**? This is Budish's question, and the uncomfortable part of the answer is the heart of the page.

## Notes to self

- This is the page where being an economist shows. Most Ethereum writing treats security as a technical property. It's a **budget**, and framing it that way reorganises everything downstream.
- Budish (2018) is the load-bearing reference. Read it before writing, and be careful to represent the argument accurately rather than as a slogan — it's a claim about the relationship between flow payments and the value a chain can safely secure, with explicit assumptions.
- Be careful with proof-of-work versus proof-of-stake here. The *requirement* to pay is common to both and is what makes this page Tier 1. **How** each mechanism makes attacks expensive is Tier 3 and belongs elsewhere. Resist the temptation to compare mechanisms on this page.
- State plainly what is **unknown**: whether fee revenue alone can fund security in the long run is an open question, not a settled one. That honesty is worth more than a confident answer.

## References to work from

Verify before citing.

- Budish, E. (2018). *The Economic Limits of Bitcoin and the Blockchain.* NBER working paper 24717.

**Next:** [Who pays: issuance or fees](who-pays.md)
