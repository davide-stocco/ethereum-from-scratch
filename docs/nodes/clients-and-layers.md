---
tier: 2
description: Ethereum is run by two pieces of software per node — one holding the accounts, one deciding the order — and by several independent implementations of each.
---

# Clients and the two layers

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

!!! info "Current as of: _(fill in the fork and date)_"

    The two-layer split and the reasons for many implementations are durable.
    **Client names, their market shares and which teams maintain them are
    not** — they change, teams stop, new ones start. Name the *classes* and
    the *reasons*; keep specific products and percentages out, or on the
    [fork history](../reference/fork-history.md) page with a date on them.

**Mostly [permanent](../about/forks.md).** That a node runs two cooperating programs, and why having several independent implementations matters, are structural. Which programs exist is not.

## Questions this page should answer

- Why **two** pieces of software? (One keeps the accounts and runs the code — the [state machine](../foundations/what-is-ethereum.md). The other decides the *order* of transactions. They do different jobs and talk to each other over a defined interface.)
- Where did that split come from? (The Merge, 2022. The consensus layer ran separately for nearly two years before being connected — history is the clearest way in, per the site's usual approach.)
- What is a **client**? (An implementation of the rules. Not an app, not a wallet — the program that *is* a node's half of the job.)
- Why are there several of each, rather than one official one? (**The key argument of the page.** A single implementation means a single bug is a network-wide bug. Several independent ones mean a bug in any one is outvoted rather than fatal — so diversity is a safety property, not an accident or a failure to standardise.)
- And the sharp edge of that: what happens when one implementation has most of the network? (A bug in it can finalise something wrong, or stall the chain. This is why client share is watched and published.)
- Who writes them, and who pays for that? (Several independent teams, variously funded. Worth stating plainly, because "nobody is in charge" raises the obvious question of who maintains the thing.)
- Does a user ever choose? (Running a node, yes. Using a wallet, no — and it's worth saying that most people are relying on somebody else's client without knowing it.)

## Notes to self

- **Name mechanism classes, never products.** Per [FORKS.md](../about/forks.md), the sentence "there are several independent implementations, and that is deliberate" stays true forever; a list of names and shares is stale within a year. If specific clients must appear, date-stamp them.
- The **two-layer split** is already introduced in a collapsed box on [What is Ethereum?](../foundations/what-is-ethereum.md). That box should become a pointer here once this page exists, rather than two explanations drifting apart.
- Lead with the *problem* diversity solves, not with the list. The problem is permanent; the list is not. Same pattern as "why metering is necessary" sitting above "gas".
- Worth a history box: the 2016 and 2020 incidents where implementation differences caused real trouble are the concrete argument for why this is taken seriously. **Verify them against primary sources before writing** — exactly the kind of detail that gets misremembered.
- Likely diagram: one node as two boxes with an arrow between them, labelled with what each half owns — accounts and code on one side, ordering on the other.

**Next:** [Running one yourself](running-one.md) — what it actually takes, and why that number is an argument rather than a footnote.
