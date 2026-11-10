---
tier: 1
description: A log is the one thing a contract can write and never read — a record for the outside world, deliberately kept out of the state.
---

# Events and logs

**[Permanent](../about/forks.md).** The structure of logs, and the rule that contracts cannot read them, have not changed since 2015.

!!! definition "Log"

    A record a contract writes **for the outside world**, attached to a
    transaction's result rather than to the [state](../accounts/state.md).

    It holds the address that emitted it, up to four 32-byte **topics** meant
    for searching, and a lump of data of any length.

    A contract can emit one and **can never read one** — not another
    contract's, not even its own.

## One thing a contract cannot read back

Everything else a contract touches, it touches both ways. It writes storage and reads storage. It sends ether and reads its own balance. It calls another contract and receives what that call returned.

Logs are the single exception, and the Solidity documentation states it flatly: *"The Log and its event data is not accessible from within contracts (not even from the contract that created them)"* [(Solidity documentation, v0.8.26)](#ref-solidity-events).

So a contract can speak and cannot listen. Whatever it emits is gone, as far as it is concerned — written down somewhere it has no access to.

**That asymmetry is the design, not a limitation of it.** Everything else on this page follows from it, including the price.

## Why the rule exists

Work backwards from what reading logs would require.

If a contract's behaviour could depend on a log, then **every node would have to keep every log forever** — because any call might consult one, and a node that had discarded old logs could no longer compute the same answer as a node that hadn't. Logs would become part of the state in all but name: permanent, universally replicated, and necessary for execution.

That is precisely the cost the design refuses. Keeping logs **outside execution** means a node needs **none of them** in order to validate a block. It can store them, serve them, prune them, or never keep them at all, and its ability to check the chain is unaffected.

**Outside execution is not outside the chain.** A log is still committed to, permanently, in a way nobody can alter afterwards — the next section says exactly where. What it is outside of is the set of things a node must *have* in order to check that the chain is correct. Those are different questions, and conflating them is the easiest mistake to make here.

Which is why [pruning](../nodes/what-a-node-is.md) is possible, and why the three sizes of node on the [state](../accounts/state.md) page differ in history without differing in what they can verify. **Logs are on the discardable side of that line, and a contract being able to read them would have moved them.**

## Event or log?

The two words are used interchangeably and mean different things, one level apart. Worth taking slowly, because the difference is the same one the [previous page](what-the-code-is.md) was about.

**A log is what exists.** An address, up to four topics, and some data. Bytes in a block. That is the whole of it, and it is all the protocol knows.

**An event is a declaration in source code** — a description, written by the contract's author, of a log they intend to emit. In Solidity it looks roughly like this:

```
event Transfer(address indexed from, address indexed to, uint256 value)
```

That line creates nothing and costs nothing. It is a **schema**: it names three fields, says what type each is, and marks which of them should be searchable. Then, somewhere in the contract's code, the author *emits* a `Transfer` with actual values, and the compiler turns that into the instruction that writes a log.

### What the compiler does with it

The declaration decides how the log is laid out. Emitting the event above produces:

```
topic 0    keccak256("Transfer(address,address,uint256)")
topic 1    the "from" address          ← indexed, so it became a topic
topic 2    the "to" address            ← indexed, so it became a topic
data       the value                   ← not indexed, so it went in the data
```

Two things to notice there.

**The first topic is the event's identity** — the Keccak hash of its name and argument types. That is what makes "find every `Transfer`" a question anybody can ask, and it is the same trick as the [four-byte function selector](smart-contracts.md), taken at full 32-byte length instead of truncated.

**And the names are gone.** `from`, `to` and `value` appear nowhere in the log. What survives is three values in fixed positions. The meaning lives in the positions, and the positions only mean something to somebody who has the declaration.

### Which is the previous page's problem again

A log on its own is an address and four 32-byte blobs. To read it as *"this address sent that address this much"*, you need the event declaration — and the declaration is **source code**, kept off-chain by people, exactly like everything else on the previous page.

So the division is consistent all the way down:

| | What it is | Where it lives |
| --- | --- | --- |
| **Event** | a declaration naming the fields | source code, off-chain |
| **Log** | the bytes that result | in a receipt, fingerprinted by the block header |

### Where a log actually sits

"In a block" is loose enough to mislead, and it is worth being exact, because it is the answer to an obvious objection: *if a node can throw logs away, in what sense are they on the chain at all?*

A log is not in the block body. The body holds the transactions. A log is produced by *running* one of them, and it is written into that transaction's **[receipt](../glossary.md#receipt)** — the record of what the transaction did: gas used, logs emitted, succeeded or failed.

The block header then carries **a fingerprint of all that block's receipts**, in the same way and for the same reason it carries [one of the state](../accounts/state.md). So:

- **The commitment is permanent.** Once the block exists, what its logs were is fixed. Nobody can add one, remove one, or alter one afterwards, because any change would contradict the fingerprint in the header.
- **The bytes are optional.** A node may keep the receipts, or discard them and still validate everything.
- **Discarding is safe because of the commitment.** A node that threw them away can ask any peer for them later and check what comes back against the fingerprint it already has. It does not have to trust the peer, which is why it was free to discard them in the first place.

That is the whole reconciliation. **Permanently committed, optionally stored** — and neither half contradicts the other. Nothing about a log is off-chain. What is off-chain is the declaration that tells you what its bytes mean.

The protocol has never heard of events, in precisely the way it has never heard of [Solidity](../glossary.md#solidity) or of functions. **A log is bytes with meaning attached by convention** — the same arrangement as the [ABI](smart-contracts.md), and as [RLP](../encoding/rlp.md), where position carries the meaning and nothing in the encoding says what the positions are for.

## Why they are cheap

Because nothing has to be able to find them later.

A storage slot is expensive for a reason the [why accounts](../accounts/why-accounts.md) page set out: writing one obliges every node to hold that value, indefinitely, available for instant lookup during execution. You pay once and the network carries it forever.

A log imposes none of that. It is never read by the machine, so no node is required to keep it retrievable, and nothing breaks if every node forgets it. The price reflects exactly that — which makes logs **the clearest case on this site of cost following structure.** Storage is dear because of what it commits others to; logs are cheap because they commit others to nothing.

So the practical advice follows from the mechanism rather than from folklore: **if only humans and software outside Ethereum will ever need a value, emit it rather than storing it.** Storing it would be buying a guarantee nobody needs.

## Finding one among millions of blocks

Here is the problem logs create. They are cheap to write, so there are an enormous number of them, scattered across every block ever made — and the natural question is always *"show me every log from this contract"*, which sounds like reading everything.

The trick is in each block header, and it is the neatest piece of machinery in this part of the site.

<svg viewBox="0 0 470 196" role="img" aria-label="A row of bits representing the logsBloom in a block header, some set and some clear. One search checks three positions which are all set, so the log might be in this block and it must be opened. A second search checks three positions of which one is clear, so the log is certainly not in this block and it can be skipped." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="40" y="46" width="12" height="20" rx="2"/><rect x="54" y="46" width="12" height="20" rx="2"/><rect x="68" y="46" width="12" height="20" rx="2" fill="currentColor" opacity="0.75" stroke="none"/><rect x="82" y="46" width="12" height="20" rx="2"/><rect x="96" y="46" width="12" height="20" rx="2"/><rect x="110" y="46" width="12" height="20" rx="2" fill="currentColor" opacity="0.75" stroke="none"/><rect x="124" y="46" width="12" height="20" rx="2"/><rect x="138" y="46" width="12" height="20" rx="2"/><rect x="152" y="46" width="12" height="20" rx="2"/><rect x="166" y="46" width="12" height="20" rx="2" fill="currentColor" opacity="0.75" stroke="none"/><rect x="180" y="46" width="12" height="20" rx="2"/><rect x="194" y="46" width="12" height="20" rx="2"/><rect x="208" y="46" width="12" height="20" rx="2"/><rect x="222" y="46" width="12" height="20" rx="2"/><rect x="236" y="46" width="12" height="20" rx="2" fill="currentColor" opacity="0.75" stroke="none"/><rect x="250" y="46" width="12" height="20" rx="2"/><rect x="264" y="46" width="12" height="20" rx="2"/><rect x="278" y="46" width="12" height="20" rx="2"/><rect x="292" y="46" width="12" height="20" rx="2" fill="currentColor" opacity="0.75" stroke="none"/><rect x="306" y="46" width="12" height="20" rx="2"/><rect x="320" y="46" width="12" height="20" rx="2"/><rect x="334" y="46" width="12" height="20" rx="2" fill="currentColor" opacity="0.75" stroke="none"/><rect x="348" y="46" width="12" height="20" rx="2"/><rect x="362" y="46" width="12" height="20" rx="2"/></g><g fill="currentColor" stroke="none"><text x="40" y="38" font-size="10" opacity="0.8">logsBloom &#183; 256 bytes in every block header</text><path d="M69 83 L74 74 L79 83 Z"/><path d="M167 83 L172 74 L177 83 Z"/><path d="M293 83 L298 74 L303 83 Z"/><text x="40" y="100" font-size="10">looking for <tspan font-weight="700">X</tspan>: all three positions set &#8212; <tspan font-weight="700">might be here.</tspan> Open the block.</text><path d="M111 129 L116 120 L121 129 Z"/><path d="M195 129 L200 120 L205 129 Z"/><path d="M335 129 L340 120 L345 129 Z"/><text x="40" y="146" font-size="10">looking for <tspan font-weight="700">Y</tspan>: one position clear &#8212; <tspan font-weight="700">certainly not here.</tspan> Skip it.</text><text x="40" y="176" font-size="10" opacity="0.85">A no is always right. A yes only means maybe &#8212; and that asymmetry is the whole</text><text x="40" y="188" font-size="10" opacity="0.85">value, because almost every block gets a no.</text></g></svg>

Every block header carries a **bloom filter** — 256 bytes summarising every address and topic in that block's logs [(Wood, 2014)](#ref-wood-2014). It does not record what is there. It records enough to answer one question: *could this block contain a log matching what I'm after?*

And the answer comes in two strengths:

- **No** — definitive. The block cannot contain it, and there is no need to look.
- **Yes** — provisional. It might, and you now have to open the block and check properly.

**The lopsidedness is the point.** A structure that can be certain in only one direction sounds like a poor one, until you notice which direction gets used: a searcher looking for one contract's logs gets a confident *no* from almost every block in history, and needs to read only the handful that said *maybe*. The occasional false *maybe* costs one wasted look. Nothing is ever missed, because a *no* is never wrong.

??? abstract "Why it can be wrong in one direction and not the other"

    The mechanism in one paragraph, without the arithmetic.

    Each address and topic is hashed, and the hash is used to pick a few fixed
    positions out of the 2048 available. Those positions are set to 1. To test
    for something, compute its positions and look: if **any** of them is 0, the
    thing was definitely never added, because adding it would have set that
    position.

    The gap is that positions are shared. Enough *other* entries can
    collectively set every position your item would have set, so a *yes* may be
    coincidence. There is no way to tell the difference from the filter alone —
    hence *maybe*.

    So the error is one-directional by construction, not by luck: bits are only
    ever turned on, so **a missing bit is proof of absence and a present bit is
    merely consistent with presence.**

## What topics are for

Topics are the searchable part. Everything in a log's data is invisible to the filter and to any index; only the address and the topics can be searched on.

**The first topic is conventionally the hash of the event's signature** — the same Keccak trick as a function selector, except taken at full length rather than truncated to four bytes. That is what lets a searcher say "find me every transfer" rather than "find me every log from this contract and then read them all".

Solidity lets you mark **up to three** further parameters as indexed, which become the remaining topics. Everything else goes into the data, where it can be read once you have the log but cannot be used to find it.

The limit is a cost decision. Indexing is what makes searching cheap for everybody else, so it is rationed — and the choice of what to index is a genuine design decision made once, at writing time, by somebody guessing what people will later want to search for.

## What logs are not

The closing caution, and the reason to be careful using them as data.

**A contract can do something and announce nothing.** Emitting a log is a choice its author made, line by line. There is no rule that state changes must be announced, and no way to tell from the outside whether something happened quietly.

So the honest description is uncomfortable but exact:

> Logs look like a record of events. They are a record of **announcements**.

Which is the same warning the [previous page](what-the-code-is.md) reached from the other direction, and the reason the [smart contracts](smart-contracts.md) page lists three ways of counting a contract's use that disagree. If you are measuring activity from logs, you are measuring what authors chose to publish — a reasonable proxy, and not the thing itself.

---

## Recap

- A **log** is a record a contract writes for the outside world: an emitting address, up to four 32-byte **topics**, and data of any length.
- A contract **can emit a log and can never read one** — not another's, not its own. That asymmetry is the design.
- The reason: if execution could depend on logs, **every node would have to keep every log forever.** Keeping them outside execution means a node needs none of them to validate a block, which is what makes pruning possible.
- An **event** is a declaration in source code — a schema naming the fields and marking which are searchable. A **log** is the bytes that result. The protocol has never heard of events.
- The declaration decides the layout: **topic zero is the hash of the event's name and argument types**, indexed fields become the remaining topics, and the rest goes in the data.
- **A log is permanently committed but optionally stored.** It sits in the transaction's receipt, and the block header fingerprints the receipts — so nobody can alter a log, and no node is obliged to keep one. Outside execution is not outside the chain.
- **The field names never reach the log.** Reading one as anything but blobs requires the declaration, which is off-chain source — the previous page's problem exactly.
- Logs are **cheap because they commit nobody to anything.** Storage is dear because it obliges every node to hold a value retrievably, forever. **Cost follows structure.**
- So: if only software outside Ethereum will need a value, **emit it rather than storing it.**
- Each block header holds a **bloom filter**, 256 bytes, that answers *could this block hold this log?* — **definitively no, or provisionally yes.** Almost every block answers no, which is what makes searching practical.
- The one-sided error is structural: bits are only ever turned on, so **a missing bit proves absence while a present bit is merely consistent with presence.**
- Only the **address and topics** are searchable; data can be read but not found. Topic zero is conventionally the hash of the event signature.
- **Logs record announcements, not events.** A contract can act and say nothing, so activity measured from logs is what authors chose to publish.

**Next:** [Tokens aren't special](tokens.md) — what you actually own when you own one.

---

## References

<div class="sources" markdown>

- <a id="ref-solidity-events"></a>**Solidity documentation**, v0.8.26. *Contracts — events.* States that up to three parameters may be indexed, that the hash of the event signature is one of the topics unless the event is anonymous, and that a log and its data are not accessible from within contracts, including the contract that created them. Version-pinned deliberately: the `latest` URL moves. <https://docs.soliditylang.org/en/v0.8.26/contracts.html>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Defines the log entry, the receipt it travels in, and the 2048-bit bloom filter carried in the block header as the union of the blooms of that block's receipts. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
