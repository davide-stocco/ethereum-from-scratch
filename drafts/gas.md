# Gas

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

## Questions this page should answer

- What is gas measuring? (Computational work — *not* money. Gas is a unit of effort, like litres of fuel.)
- Why does it need to exist at all? Two reasons, and both matter:
    1. Someone has to pay for the computation.
    2. Without a cost ceiling, an infinite loop in a contract would hang the entire network. (This is the halting problem, dodged by charging per step.)
- Why does a plain ether transfer always cost exactly 21,000 gas?
- Why do different operations cost wildly different amounts? (Writing to storage is permanent and burdens every node forever; adding two numbers isn't.)
- What's the difference between `gasLimit` (what you authorise) and gas *used* (what you actually spend)? What happens to the difference?
- What is "out of gas", and why do you still pay? (The work was genuinely done. Refunding it would make spam free.)

## Notes to self

- Keep gas and *price* strictly separate. Gas is the amount of work; fees are what it costs. Mixing them is the main reason beginners find this confusing — that's why fees get their own page.
- A short table of example opcode costs makes the "writing is expensive" point instantly.
- Good analogy, if you want one: gas is distance, gas price is the price per mile, fee is the total. Don't stretch it further than that.

**Next:** [Fees](fees.md)
