---
tier: 3
description: What running a node actually costs in disk, bandwidth and patience — and why that figure is the real constraint on everything else.
---

# Running one yourself

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

!!! info "Current as of: _(fill in the fork and date)_"

    **Every number on this page ages.** Disk requirements grow every block,
    sync times change with client releases, and the hardware people consider
    reasonable moves. Write each figure with the date it was true and the
    source it came from, or write none.

**Expect this page to need updating.** It is the one page in this part that is mostly numbers, and numbers are what a growing state changes.

## Questions this page should answer

- What do you actually need? (Disk, memory, bandwidth, and an always-on machine. Give ranges with dates, and say which requirement binds first — it's disk.)
- How long does it take to catch up? (Hours to days depending on the sync method chosen. Explain that the choice is about *how much history you re-derive*, which ties straight back to [state versus history](../accounts/state.md).)
- What do you get for it? (You stop trusting anyone's answer about your own balance. Plus you can't be lied to about what's in a block, served a stale state, or quietly rate-limited.)
- What don't you get? (No income. Running a node is not [staking](../glossary.md#proof-of-stake) and earns nothing — the distinction the [previous page](what-a-node-is.md) makes, restated here because this is where people expect to be paid.)
- Why does the requirement matter beyond your own inconvenience? (**The argument the page exists for.** If running a node needs a datacentre, almost nobody does it, and "anyone can check for themselves" quietly stops being true. The cost of a node is the price of the property the whole system rests on.)
- So what keeps it affordable? (Nothing automatic. The reason is **ahead** of this page, not behind it: [why accounts](../accounts/why-accounts.md) argues that permanent storage is mispriced and only ever grows. State the fact here — disk requirements rise every block and nothing shrinks them — and point forward for why.)

## Notes to self

- This page is the **concrete end** of an argument the reader hasn't met yet. [Why accounts](../accounts/why-accounts.md) says permanent storage is mispriced and every node carries the cost; this page says what the cost is in gigabytes. Since this one comes first, give the number and the direction of travel, and let that page supply the explanation — then link back from there.
- **Resist a tutorial.** "How to install client X" dates instantly, duplicates far better documentation, and isn't what this site is for. Say what it costs and what it buys; link out for instructions.
- Every figure needs a date and a source, per the site's rule on empirical claims. A number without a date is the single most common way a reference page goes quietly wrong.
- Don't moralise about decentralisation. State the mechanism — cost rises, participation falls, checking becomes theoretical — and let the reader draw the conclusion.
- Honest caveat to include: most readers will never run one, and the page should say so without implying they're failing a duty. The useful version is understanding *what is being assumed on your behalf* when you don't.

**Next:** [Accounts](../accounts/accounts.md) — what all these machines are actually storing.
