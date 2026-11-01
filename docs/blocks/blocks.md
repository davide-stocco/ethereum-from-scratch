---
tier: 2
description: Why transactions travel in batches, and what a block actually is.
---

# Blocks

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

!!! info "Current as of: _(fill in the fork and date)_"

    The structural idea is stable; the exact field list has grown at several
    forks. See [the block header](block-header.md).

## Questions this page should answer

- What is a block? (A batch of transactions, plus the metadata needed to place it in the chain.)
- Why batch at all, rather than processing transactions one at a time? (Agreement is expensive: agreeing once per batch amortises it. Also connects to why [state is recorded per block](../foundations/what-is-ethereum.md).)
- How are blocks linked? (Each names the hash of its parent — which is what makes rewriting history expensive.)
- Who decides what goes in a block, and in what order? (A proposer, with wide discretion. The consequences of that discretion are an economics question — see [MEV](../economics/security-budget.md).)
- What limits a block's size? (A gas limit, not a byte limit — the constraint is work, not space.)
- What's the difference between a block being *produced* and being *final*?

## Notes to self

- Keep this page structural. Who proposes and why they're trusted is consensus, and it comes later.
- "Linked by parent hash" is the whole of why a chain is hard to rewrite. Give it room — it's one idea that pays for itself repeatedly.
- The gas-limit-not-byte-limit point surprises people and is worth stating plainly.

**Next:** [The block header](block-header.md)
