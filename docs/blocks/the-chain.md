---
tier: 3
description: How blocks form a chain, why the tip is uncertain, and what a reorganisation is.
---

# The chain and reorgs

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

!!! info "Current as of: _(fill in the fork and date)_"

    Chaining by parent hash is permanent. How the network picks between
    competing branches is consensus, and that was replaced wholesale in 2022.

## Questions this page should answer

- How does linking by parent hash make a chain? And why does changing an old block invalidate everything after it?
- Why can two valid blocks exist at the same height?
- What is a **reorganisation**, and what happens to transactions in the discarded branch? (They aren't invalid — they go back to being pending.)
- Why is the recent tip of the chain less certain than older blocks?
- What does **finality** mean, and how is it different from "probably settled"? (Forward-reference to consensus; don't explain the mechanism here.)
- Why do exchanges wait for confirmations?

## Notes to self

- The practical question a reader actually has is "when is my transaction safe?" Build towards that.
- Keep the fork-choice mechanism out. This page is about what a chain *is* and why its tip wobbles; how the network chooses is consensus.
- A diagram of a short reorg, showing a transaction returning to pending, would carry most of the page.

**Next:** [Gas costs](../reference/gas-costs.md)
