---
tier: 1
description: Accounts persist where coins are consumed — which is what makes programs possible, and what every awkward thing about Ethereum is the price of.
---

# Why accounts, and what they cost

**[Permanent](../about/forks.md).** Accounts were chosen before Ethereum launched in 2015 and the decision has never been reopened, so the costs described below are permanent ones. Work on *reducing* those costs is still going on, which is why the last section describes general approaches rather than naming particular proposals.

!!! definition "The account model"

    Recording value as **balances against persistent addresses**, rather than
    as individually spendable units that are consumed when spent.

    Bitcoin does the latter: a payment destroys specific coins and creates new
    ones. Ethereum does the former: a payment edits two numbers, and the
    [accounts](accounts.md) they belong to go on existing, untouched in every
    other respect. The specification puts it as a mapping from addresses to
    accounts [(Wood, 2014)](#ref-wood-2014) — a *mapping*, with entries that
    persist, rather than a set of items that get used up.

    Everything on this page follows from that one difference.

## One property, and a long invoice

The previous three pages described the account model. This one argues it, because it was a choice and it cost real things.

Here is the whole argument in a sentence: **persistence buys programmability, and everything awkward about Ethereum is the invoice.**

<svg viewBox="0 0 470 302" role="img" aria-label="A diagram. At the top, one property: accounts persist. Below it the consequences split into two columns. On the left, what it buys: programs can exist at all, persistent identity, and composability. On the right, what it costs: order starts to matter, the state only grows, parallel execution is hard, and fees must be held in ether." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="158" y="8" width="154" height="38" rx="5"/><path d="M235 46 L235 70"/><path d="M112 70 L358 70"/><path d="M112 70 L112 92"/><path d="M358 70 L358 92"/><rect x="14" y="120" width="196" height="30" rx="4"/><rect x="14" y="158" width="196" height="30" rx="4"/><rect x="14" y="196" width="196" height="30" rx="4"/><rect x="260" y="120" width="196" height="30" rx="4"/><rect x="260" y="158" width="196" height="30" rx="4"/><rect x="260" y="196" width="196" height="30" rx="4"/><rect x="260" y="234" width="196" height="30" rx="4"/></g><g fill="currentColor" stroke="none"><path d="M107 92 L112 102 L117 92 Z"/><path d="M353 92 L358 102 L363 92 Z"/><text x="235" y="33" font-size="13" text-anchor="middle" font-weight="700">accounts persist</text><text x="14" y="114" font-size="10" font-weight="700">WHAT IT BUYS</text><text x="260" y="114" font-size="10" font-weight="700">WHAT IT COSTS</text><text x="26" y="140" font-size="11">programs can exist at all</text><text x="26" y="178" font-size="11">a lasting identity</text><text x="26" y="216" font-size="11">composability</text><text x="272" y="140" font-size="11">order starts to matter</text><text x="272" y="178" font-size="11">the state only grows</text><text x="272" y="216" font-size="11">parallel execution is hard</text><text x="272" y="254" font-size="11">you must hold ether to act</text><text x="14" y="286" font-size="10" opacity="0.8">The two columns are not separate lists. They are the same property, read</text><text x="14" y="298" font-size="10" opacity="0.8">twice.</text></g></svg>

That last line is the thing to hold on to. The costs aren't flaws that happen to sit beside the benefits — they are the benefits, described by someone who didn't want them.

## What it buys

### Programs need somewhere to live

This is the one that justifies everything else, and it's worth stating starkly: **Bitcoin cannot hold a program, and no amount of engineering would let it.** Not because its scripting language is limited — because there is nowhere for a program to be.

A coin is consumed when spent. It has no address, no permanence, nothing you could send a second message to. A program needs to exist between the times it's used: somewhere to keep its code, somewhere to keep what it remembers, and a name people can reach it at.

An account is exactly that. It has an address that never changes, a `codeHash` for the program and a `storageRoot` for what the program remembers — the four fields the [accounts](accounts.md) page listed. So contracts aren't an addition to the account model, they're a **consequence** of it. The [state machine](../foundations/what-is-ethereum.md) page said Bitcoin lets you agree on who owns what while Ethereum lets you agree on what a program computed. This is why that's possible.

### A lasting identity

Because an address persists and accumulates, things can be attached to it: a name, token balances, a borrowing position, a voting record, a reputation. None of that is a feature anybody built into the protocol. It's a side effect of having somewhere durable to write.

Which is also the privacy cost, seen from the other side. **They are not two facts.** An address that accumulates a history is simultaneously what makes undercollateralised lending conceivable and what makes surveillance straightforward, and any page presenting those as separate items is hiding the trade.

### Composability

Contracts can hold balances, including balances of things other contracts define, and can call each other. That works because accounts are addressable and survive between transactions — a contract can be *pointed at*, and will still be there next block.

Most of what gets described as innovation on Ethereum is this: existing pieces addressed and combined. It needs persistent, nameable places to compose, which is the account model again.

## What it costs

### Order starts to matter

Two Bitcoin transactions spending different coins are independent. Neither refers to anything the other touches, so their order is arbitrary.

Two transactions from one Ethereum account are a **sequence**. Each depends on the balance and the counter the other leaves behind, so "which came first" is a question with a required answer. That's why the [nonce](nonce.md) exists, and why one underpriced transaction blocks every later one from the same account — a problem with no UTXO equivalent, because UTXO transactions were never in a queue to begin with.

### The state only grows

A UTXO is destroyed when spent: the set shrinks as well as grows, and it stays roughly proportional to money actually in use. An account persists whatever happens to it. Balance at zero, contract abandoned, key lost years ago — the entry stays, because the protocol has no notion of state going out of date.

So [the state](state.md) rises monotonically, every node stores all of it, and the cost of running one rises forever. The only deletion mechanism Ethereum has ever had is the narrow cleanup of genuinely empty accounts.

### Parallel execution is hard

If transactions name the coins they spend, a client can look at two of them, see they touch nothing in common, and safely run them at once. The independence is visible in the transaction itself.

Account transactions don't declare what they'll touch. A call to a contract may read or write anything that contract can reach, which is only known once it runs. So the safe default is **one at a time, in order** — and every scheme for executing Ethereum transactions in parallel is an attempt to recover information the UTXO model gives away for free.

### Privacy is the default casualty

Bitcoin wallets generate a fresh address for each payment, so a user's activity is spread across many unlinked addresses. Ethereum does the opposite: **address reuse is universal and necessary**, because contracts, token balances and names all need an address that stays put.

The consequence is that one address is one linkable history, permanently and publicly. And this isn't theoretical even in the system that *does* use fresh addresses — Meiklejohn et al. [(2013)](#ref-meiklejohn-2013) showed Bitcoin activity could be clustered into real identities using heuristics over the public chain, against users who were changing addresses. Ethereum hands over, by design, what those researchers had to work to reconstruct.

This is the loose end the [public keys](../crypto/public-keys.md) page left: the old advice against reusing an address had substance, and Ethereum spent it deliberately for a stable identifier.

### You must hold ether to act

A Bitcoin fee comes out of the inputs being spent — it's the difference between what goes in and what comes out, so paying is part of the payment.

An account has no inputs to shave. The fee comes from the sender's ether balance, which means **holding a thing is not enough to be able to move it.** An account with a million in tokens and no ether can receive anything and send nothing, exactly as the [ether](../foundations/ether.md) page described. Entire mechanisms exist to work around this, letting a third party pay on your behalf, and all of them are compensating for a cost the account model introduced.

??? abstract "And anyone can make every node store more"

    A smaller cost, worth knowing because it shows the shape of the problem.

    Creating an account needs no key and no permission: send one wei to an
    untouched address and an entry appears. So the state isn't only *your*
    liability — it's a public resource any stranger can enlarge, cheaply, for
    everybody.

    Early Ethereum was exploited this way until EIP-161 cleared out entries
    left genuinely empty, which the [accounts](accounts.md) page covers. That
    was the first patch on this, and the fact that a patch was needed at all is
    the tell.

## What it quietly avoids

Less obvious, and the honest accounting requires it: several things are simply *absent* from Ethereum because of this choice, and their absence is why nobody notices them.

- **No dust.** A tiny UTXO becomes unspendable once the fee to move it exceeds its value — real money, permanently stranded in fragments. A balance is one number, so no part of it can be too small to use.
- **No coin selection.** Bitcoin wallets run algorithms to decide which coins to spend, trading off fees, privacy and future flexibility. Ethereum wallets contain no such code, because there is nothing to select.
- **No change.** No change outputs, no change addresses, and none of the machinery or confusion they generate.
- **Constant-size transfers.** A Bitcoin transaction grows with its input count, so consolidating many small coins is expensive precisely when you can least afford it. An Ethereum transfer is the same size whatever the balance behind it.
- **Cheap balance proofs.** "This address holds this much" is a short proof against the [state root](state.md). Bitcoin's headers commit to no equivalent set, so a light client cannot be handed a compact proof of someone's balance at all.

Notice that three of those five are **ordinary users not losing money** to something they'd never have understood. That belongs in the ledger as much as the costs do.

## The bill nobody has paid yet

The sharpest version of all this is not technical, and it's where the account model's real unsettled problem lives.

> **You pay once to write state. Every node then stores it forever.**

A one-time fee against a perpetual liability. The payment is made by one party, at one moment, at a price set by a fee market concerned with present congestion — while the cost falls on thousands of operators who were not consulted, cannot refuse, cannot charge for it, and will carry it indefinitely.

That's a textbook externality, and the classic description of what follows is Hardin's [(1968)](#ref-hardin-1968): a resource nobody owns, which each user is individually rational to consume and collectively ruinous to exhaust. It reframes **state growth** from an engineering nuisance into a **pricing failure** — and that reframing matters, because it tells you no amount of faster disks fixes it. Cheaper storage changes the rate. It doesn't change the sign.

The protocol does have one crude lever: it refunds gas when you *clear* storage, paying you a little to shrink the state. The refunds have been reduced over time because they were gameable, and they only ever applied to people willing to delete their own data. Nothing addresses the general case.

The genuine responses fall into three classes — named as classes, not products, because which of them ships is exactly what this site doesn't try to predict:

- **Rent.** Charge for occupied state over time, so a perpetual cost meets a perpetual payment.
- **Expiry.** Let state untouched for long enough fall out of what nodes must keep, with some way to revive it.
- **Statelessness.** Arrange that validators don't need the state to validate, which doesn't shrink it but moves who must hold it.

None has shipped. All three have been argued over for years. **The problem is permanent; the solutions are plans** — and that distinction is the whole reason this page is fork-proof and the gas-costs page is not.

??? info "History: the trade as the designers saw it"

    Worth reading how this was argued *before* the consequences were known,
    because it was not presented as obvious.

    Ethereum's white paper [(Buterin, 2014)](#ref-buterin-2014) sets the two
    models against each other and credits the UTXO side with real advantages —
    privacy, a degree of parallelism, and simpler proofs for light clients
    checking payments. The case for accounts was made on space savings,
    fungibility, and simplicity for developers.

    Which reads, a decade on, like an understatement of what was being bought
    and an underestimate of what was being spent. The white paper's list
    doesn't mention state growth, because nobody had a large state yet.

    That's not a criticism. It's the ordinary condition of design decisions:
    the benefits are visible at the time and the bills arrive later. Worth
    knowing it was a judgement call rather than a discovery.

## The two models side by side

Prose first, because a table alone reads as a scorecard and this is a trade:

| | Coins (Bitcoin) | Accounts (Ethereum) |
| --- | --- | --- |
| A payment | destroys units, creates new ones | edits two numbers |
| Can hold a program | no — nothing persists to hold it | **yes** |
| Replay protection | the coin is already spent | a [nonce](nonce.md) must be added |
| Transaction order | arbitrary between independent payments | a strict sequence per account |
| Data held by nodes | grows and shrinks with use | **grows only** |
| Parallel execution | independence is visible | must be inferred |
| Privacy by default | fresh address per payment | one address, one history |
| Paying the fee | out of what you're spending | from a separate ether balance |
| Stranded small amounts | dust is a real problem | cannot occur |
| Proving a balance | no committed set to prove against | short proof against the state root |

## So was it the right call?

The honest answer is that the question is badly formed, because the two systems are no longer trying to do the same thing.

If Ethereum were a payment network, this trade would look poor: it gave up privacy and bounded storage to gain programmability it wouldn't need. But the programmability is what Ethereum *is*. Judging the account model against Bitcoin's purposes is like judging a database against a receipt.

What can be said firmly is narrower and more useful:

- The benefit was **real and unobtainable otherwise.** No clever scripting gets you contracts without persistence.
- The costs were **real and mostly unforeseen** in their eventual size, state growth above all.
- The one that remains genuinely unsolved is the **pricing** of permanent storage, not any of the engineering.

Which is a reasonable thing to know about any system you rely on: not whether it was built correctly, but which of its bills are still outstanding.

---

## Recap

- The account model records **balances against persistent addresses** instead of consuming individual units. Everything else follows from that.
- **Persistence is what makes programs possible.** A coin is destroyed when spent, so there is nowhere for code or memory to live. Contracts are a consequence of accounts, not an addition to them.
- The same persistence gives a **lasting identity** — which is why names, token balances and lending positions work, and why privacy is the default casualty. One property, not two.
- It makes **order matter**, hence the nonce and head-of-line blocking; makes **parallel execution hard**, since transactions don't declare what they'll touch; and requires you to **hold ether** to move anything at all.
- It also silently removes **dust, coin selection, change addresses** and transaction sizes that grow with your history — three of which are users not losing money.
- The unsolved problem is **pricing, not engineering**: you pay once to write state and every node stores it forever, which is an externality rather than a nuisance. Faster disks change the rate, not the sign.
- Responses divide into **rent, expiry and statelessness.** None has shipped. The problem is permanent; the solutions are plans.
- It was a **judgement call**, argued at the time with UTXO's advantages acknowledged, and its largest cost unforeseen.

**Next:** [What it reveals](what-it-reveals.md) — the cost this page listed in one line, which deserves rather more than that.

---

## References

<div class="sources" markdown>

- <a id="ref-buterin-2014"></a>**Buterin, V.** (2014). *Ethereum white paper: A next-generation smart contract and decentralized application platform.* Sets the account model against Bitcoin's transaction outputs and credits the latter's advantages explicitly — the contemporaneous statement of the trade. <https://ethereum.org/en/whitepaper/>
- <a id="ref-hardin-1968"></a>**Hardin, G.** (1968). *The tragedy of the commons.* *Science*, 162(3859), 1243–1248. The standard treatment of a resource that is individually rational to consume and collectively ruinous to exhaust — the shape of the state-growth problem, which is a pricing failure rather than a technical one. <https://doi.org/10.1126/science.162.3859.1243>
- <a id="ref-meiklejohn-2013"></a>**Meiklejohn, S., Pomarole, M., Jordan, G., Levchenko, K., McCoy, D., Voelker, G. M., & Savage, S.** (2013). *A fistful of bitcoins: Characterizing payments among men with no names.* *Proceedings of the 2013 Internet Measurement Conference*, 127–140. Clusters chain activity into identities using public data alone, against users who were already rotating addresses. <https://doi.org/10.1145/2504730.2504747>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines the world state as a mapping from addresses to accounts, which is the formal statement of the choice this page examines. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
