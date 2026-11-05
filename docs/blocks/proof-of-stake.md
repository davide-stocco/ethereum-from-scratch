---
tier: 3
description: How Ethereum chooses who proposes a block — validators, stake, attestation, and the penalties that make the arrangement bite.
---

# Proof of stake

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

!!! info "Current as of: _(fill in the fork and date)_"

    **Nearly every number on this page is a parameter a fork can change** —
    the amount a validator stakes, slot and epoch timings, committee sizes,
    reward and penalty rates. Give each one the date it was true and the
    source it came from. The *requirement* this mechanism satisfies is on
    [the previous page](why-somebody-chosen.md) and does not move.

**Expect this page to need revisiting.** It is the most fork-dependent page on the site after gas costs.

## Questions this page should answer

- What is a validator, as distinct from a node? (The [node](../nodes/what-a-node-is.md) page draws the line: a validator is a node plus a paid job. Restate it, because this is where the job gets described.)
- What does staking actually mean? (Locking ether as a deposit that can be reduced. **Not** a payment, not a purchase — collateral, which is why the previous page's "something to lose" requirement is met.)
- What are the two jobs? (**Proposing** a block when it's your turn, and **attesting** — voting that somebody else's block looks valid. Almost all of a validator's work is the second, which surprises people.)
- How is the proposer chosen? (Pseudorandomly, in proportion to stake, from the active set. The *why* is the previous page; the *how* and its parameters belong here with a date.)
- What is a slot, and an epoch? (The timing structure that turns "eventually" into a schedule — and the reason "when it's settled" is answerable at all.)
- What is **finality**, precisely, and how does it differ from "confirmed"? (The sharpest thing on the page. A block can be in the chain and still be revertible; finality is the point at which reverting it would require destroying an enormous amount of staked value. Set up carefully, because [the chain and reorgs](the-chain.md) depends on it.)
- What is the difference between being **offline** and being **dishonest**? (Offline leaks a little stake slowly; equivocating — signing two conflicting things — is **slashing**, and costs a large amount at once. The asymmetry is deliberate and worth explaining: carelessness should be survivable, contradiction should not.)
- Can you get your stake back? (Yes, with exit and withdrawal mechanics — which did not exist at first and were added later. Good history-box material.)
- What does this cost the network, as opposed to the validator? (Issuance: new ether paid to validators. Hand straight to [why security has to be paid for](../economics/security-budget.md), which is the page that treats it as an economic question.)

## Notes to self

- **The why belongs on the previous page.** If this page starts arguing that somebody must be chosen, the split has failed. This page answers *how*, with dates.
- **Finality is the payload.** Everything else here is machinery; finality is the thing a reader actually needs, because it's what makes "is my transaction settled?" a question with an answer. Give it room and keep it honest — including that finality is economic rather than absolute.
- Explain **why attesting dominates**: thousands of validators voting on each block is what makes the chain's history expensive to rewrite, and a reader who thinks proposing is the main job has the mechanism upside down.
- **No client names, no validator counts, no yield figures.** All three date within months, and a yield figure in particular invites being read as advice.
- Resist explaining reorgs — the next page. Resist explaining the fee market — that's [fees](../transactions/fees.md). This page is selection, voting and penalties.
- History box worth having: proof of stake ran as a separate chain for nearly two years before being connected in 2022, which is the clearest way to explain why Ethereum has two layers at all. Ties to [clients and the two layers](../nodes/clients-and-layers.md).
- The comparison with proof of work goes **here**, not on the previous page, because what each costs and who it favours are empirical claims that age.

**Next:** [The chain and reorgs](the-chain.md) — why the recent tip is less certain than what came before.
