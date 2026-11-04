---
tier: 1
description: Why a network that runs other people's code has to charge for every step of it — and would be trivially attackable otherwise.
---

# Why metering is necessary

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

**[Permanent](../about/forks.md).** The requirement follows from running untrusted code on a shared machine. Only the prices change.

This is the **problem** page. [Gas](gas.md) is the mechanism that answers it, and gas *costs* change at forks — the argument here does not.

## The argument to make

1. The network executes code written by strangers, and every node must run all of it.
2. Some of that code will not terminate — whether by mistake or on purpose.
3. You cannot tell in advance which. (This is the halting problem, and it isn't a limitation of Ethereum's design but of computation itself.)
4. So termination cannot be decided by inspection. It has to be **imposed**.
5. Charging per step imposes it: the caller fixes a budget in advance, and execution stops when the budget runs out.
6. The charge also has to be **paid**, not merely counted — otherwise an attacker spends nothing to make every node work.

## Questions this page should answer

- Why can't the network simply refuse infinite loops? (Step 3 above. Worth stating properly, because it's the real answer.)
- Why charge per *operation* rather than per transaction or per second?
- Why must the price be positive even for cheap work? (Free work is free spam.)
- Why does the caller set a ceiling in advance rather than paying whatever it takes?
- Why is the work paid for **even when it fails**? (It was genuinely performed by every node. Refunding it would make failed spam free.)
- What does Bitcoin do instead, and what does it give up? (Restricts the language so termination is guaranteed — no metering needed, no general computation either. The comparison makes the trade-off visible.)

## Notes to self

- **No numbers on this page.** Not one gas cost. Those live in [the reference table](../reference/gas-costs.md) and change at forks; this page has to stay true regardless.
- The halting-problem point is what makes this more than hand-waving. It explains why metering is *necessary* rather than merely convenient — and almost nothing written about gas says this clearly.
- This page is also the hinge into Economics: it establishes that computation must be paid for, which [who pays](../economics/who-pays.md) then takes up.

**Next:** [Gas](gas.md)
