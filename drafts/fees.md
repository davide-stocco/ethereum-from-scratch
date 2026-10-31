# Fees

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

## Questions this page should answer

- How is the fee actually calculated? (`gas used` × `gas price`, paid in wei.)
- What was wrong with the old system, where you just named a gas price? (Blind auction — you were guessing what everyone else would bid, and usually overpaid or got stuck.)
- What did **EIP-1559** change, in August 2021? Three pieces:
    - **Base fee** — set by the protocol, not by bidders. Rises when blocks are full, falls when they're empty.
    - **Priority fee** — a tip, which actually goes to the validator.
    - **Max fee** — your ceiling. You're refunded the difference.
- Where does the base fee go? (It's **burned** — destroyed. Nobody receives it.)
- Why burn it rather than pay the validator? (If validators received it, they'd be incentivised to fake congestion to drive it up.)
- Why does the base fee adjust so predictably? (It moves by at most 12.5% per block, so you can estimate the next one reliably. This is what fixed the guessing problem.)
- What does `maxFeePerGas` mean for the user in practice? (You can set a high ceiling safely — you pay the base fee, not your ceiling.)

## Notes to self

- The burn is the part people find strangest, so lead with the incentive argument rather than the mechanism.
- Worth noting the second-order effect: the burn means ether supply can shrink when the network is busy. Mention it, but don't turn the page into tokenomics.
- A worked example in gwei, with real numbers, beats the formula.

**Next:** blocks — write `docs/blocks/blocks.md` and add it to `nav` in `mkdocs.yml`.
