# Gas costs

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**This page is the single source of truth for every number on this site.**

No concept page should hardcode a gas cost. They explain *why* an operation is expensive; this page says *how much*. When a hard fork reprices something, you edit this file and nothing else.

!!! info "Current as of: _(fill in the fork and date)_"

    Gas costs change at hard forks. Verify against
    [execution-specs](https://github.com/ethereum/execution-specs) before trusting this table.

## Questions this page should answer

- What are the baseline costs? (21,000 for a plain transaction; 4 gas per zero byte and 16 per non-zero byte of calldata.)
- What do storage operations cost, and why are they the expensive ones?
    - `SSTORE` on a zero → non-zero slot
    - `SSTORE` on an existing slot
    - The refund for clearing a slot
- What's the difference between a **cold** and a **warm** access, and where did that distinction come from? (EIP-2929, Berlin.)
- What do the cheap operations cost? (Arithmetic, comparisons, stack ops — single digits.)
- What does contract deployment cost per byte of code?
- What are the hard limits? (Contract code size, initcode size, block gas limit.)

## Notes to self

- One table, sorted by cost, with a "why" column. The "why" is what makes this page teaching material rather than a spec dump.
- Record which fork last changed each cost — this is what makes the page maintainable, and it doubles as a mini fork history.
- Several costs have been repriced more than once (`SLOAD` notably). A "changed in" column is worth the space.
- Link here from [gas](../transactions/gas.md), [fees](../transactions/fees.md), and every EVM page.

## Table skeleton

| Operation | Gas | Why | Last changed |
| --- | --- | --- | --- |
| Plain transaction | 21,000 | Base charge: signature recovery, nonce check, state lookup | Genesis |
| | | | |
