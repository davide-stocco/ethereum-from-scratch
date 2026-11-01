---
tier: 1
description: Bitcoin capped its supply; Ethereum did not. Both choices have costs, and the trade-off between scarcity and a funded security budget is permanent.
---

# Fixed cap or flexible supply

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**Fork-proof.** The trade-off is permanent, even though each chain's current issuance is not.

Bitcoin capped its supply at 21 million. Ethereum has no cap. This is the single clearest design disagreement between the two, and it follows directly from the previous two pages: if [security must be paid for](security-budget.md) and [the money comes from issuance or fees](who-pays.md), then capping supply means eventually paying for security out of fees alone.

## The argument to make

**The trade-off is real and neither side gets it for free.**

A **hard cap** delivers a credible scarcity guarantee — the supply schedule is knowable in advance and politically very hard to change. The cost is that issuance tends to zero, so the security budget must eventually come entirely from transaction fees. Whether fee revenue is sufficient and stable enough to secure a large amount of value over decades is **an open question**.

**No cap** means the protocol can always pay for security, and can adjust what it pays as conditions change. The cost is that there's no scarcity guarantee: the supply schedule depends on parameters that governance can revise, so holders are relying on restraint rather than arithmetic.

**Say plainly that this is unresolved.** Both communities present their choice as obviously correct; neither has run long enough to know.

## Questions this page should answer

- What exactly does a supply cap guarantee, and what does it not? (It constrains quantity; it says nothing about demand, price, or security.)
- Why does a cap force reliance on fees? Work through the arithmetic.
- What would have to be true for fee-only security to work? (Sustained demand for block space at a level that funds the budget — and demand for block space is not the same thing as demand for the currency.)
- What does "no cap" actually mean in practice — unlimited, or merely unconstrained in advance? What *does* constrain it?
- How credible is each commitment? A cap is credible because changing it is politically unthinkable; an uncapped schedule is credible only insofar as governance is trusted. **Credibility is the real variable here**, not the number.
- Is "scarcity" doing economic work, or is it a narrative? Worth addressing directly, because the reader will have met the narrative version.

## Notes to self

- **This is the page most at risk of becoming advocacy.** It's the inflation debate, and both sides have slogans ready. The discipline: describe each mechanism, state who bears which risk, and name what's unknown. Do not reach a verdict the evidence doesn't support.
- Avoid the loaded vocabulary entirely — "sound money", "ultrasound money", "debasement". Each carries a conclusion inside it.
- **Keep current numbers off this page.** Issuance rates and the burn are fork-dependent and usage-dependent; they belong in the later Ethereum-specific page, with a date stamp. This page is about the structure of the choice.
- Worth noting that the question isn't unique to crypto: the trade-off between a credible nominal rule and discretionary flexibility is a very old one in monetary economics. That connection is the kind of thing almost no Ethereum writing makes, and it's yours to make.

## References to work from

Verify before citing.

- Budish, E. (2018). *The Economic Limits of Bitcoin and the Blockchain.* NBER working paper 24717. Relevant to whether fee-funded security scales.
- The monetary-policy-rules literature on rules versus discretion is the natural comparison. Pick whichever treatment you know best — this is your field, not mine.

**Next:** the Tier 3 pages — Ethereum's actual issuance and the fee burn — once the protocol pages they depend on exist.
