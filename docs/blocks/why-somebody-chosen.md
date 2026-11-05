---
tier: 1
description: Transactions reach every node in a different order, and the rules don't pick one — so somebody has to propose, be paid for it, and have something to lose.
---

# Why somebody has to be chosen

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**[Permanent](../about/forks.md).** The requirement follows from the design and from arithmetic. *How* Ethereum currently satisfies it is the next page, and that one carries a date.

## The thesis this page exists to argue

Determinism does not pick an order. It only guarantees that **given** an order, everybody computes the same result — which the [node](../nodes/what-a-node-is.md) page showed as three machines reaching one state root without consulting each other.

But transactions arrive at different nodes in different orders, and nothing in the rules says which order is right. So the ordering has to come from **somewhere outside the rules**: somebody proposes, everybody else checks. That role then has to be paid, has to be costly to obtain, and has to carry a penalty — and each of those three follows from a problem, not from a preference.

## Questions this page should answer

- Why is an order needed at all? (Two transactions spending the same balance are each individually valid; only their *sequence* makes one of them fail. The [nonce](../accounts/nonce.md) page established that accounts make order matter — this is the network-level consequence.)
- Why can't nodes work the order out among themselves by a rule? (The obvious rule is "by timestamp", and there is **no shared clock** — the same objection the accounts page raises against self-starting code. Any rule needing agreement about *when* is a rule needing the thing it's trying to produce.)
- So why not just let anybody propose whenever? (Then everybody proposes, and the network has thousands of candidate orderings and no way to choose. Proposal has to be a **scarce** right.)
- Why must the role be paid? (It costs hardware, bandwidth and attention. An unpaid role gets filled by whoever has a motive other than payment — which is a worse set of people than those who want the money.)
- Why must the right to propose be **expensive to acquire**? (If it's free, acquiring a majority of it is free. Any scheme where identities are cheap can be swamped by one party pretending to be many — the problem that makes naive voting useless here. Name the problem; don't dress it up.)
- And why penalties rather than only rewards? (With rewards alone, misbehaving costs nothing but a forgone bonus. For a proposer to be *deterrable*, there has to be something they already hold that can be taken.)
- Why can't users vote? (Voting needs a register of who counts as a user, which is precisely what a system with no identities cannot have. Every answer to "who votes" is an answer to "who is in charge".)
- What, then, is the irreducible requirement? (**A scarce, verifiable, costly claim to the right to propose, with something at stake behind it.** Proof of work and proof of stake are two ways of meeting it; the requirement is older than either.)

## Notes to self

- This is the **mechanism-design page**, and Davide's own field — write it as an argument in the register of [why accounts](../accounts/why-accounts.md), and let him pick the outside frame rather than choosing one for him. The obvious candidates are the literature on costly signalling and on Sybil-resistance.
- Keep **proof of stake out of it entirely.** The test of whether this page works: every sentence should still be true if Ethereum changed consensus mechanism tomorrow. That is what makes it permanent while the next page isn't.
- The two strongest hooks already exist elsewhere on the site and should be used: **there is no shared clock** (accounts), and **order matters because accounts make it matter** (nonce). This page is the point where those two converge.
- Worth a history box on the Byzantine-generals framing — the problem of agreeing on one order among parties who can't be assumed honest predates cryptocurrency by decades. **Verify the citation properly before using it**; it's the kind of reference that gets attributed loosely.
- Don't let this become "proof of work versus proof of stake". The comparison is interesting and belongs on the next page, where it can be dated.

**Next:** [Proof of stake](proof-of-stake.md) — how Ethereum meets that requirement now.
