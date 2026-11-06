---
tier: 2
description: How one 32-byte number commits to Ethereum's entire state, and how a few kilobytes can prove a single balance against it.
---

# The Merkle Patricia Trie

**Mostly [permanent](../about/forks.md).** The structure has not changed since 2015, and everything it achieves — a single root committing to everything, cheap updates, small proofs — is permanent regardless of how it is built. The *way* it is built is the part under long-running attempts at replacement.

!!! info "Current as of Fusaka (December 2025)"

    A replacement called a **verkle tree** has been proposed for years, to make
    proofs dramatically smaller. **It has not shipped**, and its specification
    [(Buterin et al., 2023)](#ref-eip6800) is currently marked *Stagnant* —
    which is itself the useful status report. Treat verkle as a direction
    rather than a plan, and check before relying on anything about it.

!!! definition "Merkle Patricia Trie"

    The structure behind every **root** on Ethereum: the state root, each
    account's storage root, and a block's transactions and receipts roots.

    It is a tree in which **the path to a value is determined by its key**, and
    **every node is identified by the hash of its contents**. The first makes
    it a lookup table. The second makes the single hash at the top a
    commitment to every value inside.

## What it has to do

Four requirements, and no simpler structure meets all four. The [state](../accounts/state.md) page set out the first three; the fourth is the one usually left out and is arguably the most important.

**1. Commit to everything in 32 bytes.** Change one wei in one account and the root must change. Otherwise two nodes could hold different states and agree.

**2. Be cheap to update.** A block changes perhaps a few hundred accounts out of hundreds of millions. Re-hashing everything per block would be absurd.

**3. Support proofs about parts.** Somebody holding only the root should be able to be *shown* that one account holds one balance, without receiving the rest of the state.

**4. Depend on the contents and nothing else.** Two nodes that applied the same transactions in different *internal orders* — different insertion sequences, different storage layouts, different software — must still arrive at the same root. The structure cannot depend on history or implementation, only on what is in it.

That fourth requirement rules out most of the obvious answers. A sorted list depends on nothing but contents but fails (2) and (3). A hash of everything concatenated fails (2) and (3) too. A binary search tree meets (2) and (3) and fails (4), because its shape depends on the order things were inserted.

## First, the Merkle part

Take a set of values. Hash each one. Then hash the hashes in pairs, and the results in pairs, until one hash is left. That top hash is the **root**, and the arrangement is a **Merkle tree** — the idea comes from Merkle's work on signing many messages with one public value [(Merkle, 1988)](#ref-merkle-1988).

Two properties fall out, and they're the two that matter.

**The root commits to every value.** Change any one of them and its hash changes, so its parent's hash changes, and so on to the top. There is no way to alter a value and leave the root alone — that would require a hash collision.

<svg viewBox="0 0 470 288" role="img" aria-label="Five values A to E are each hashed. The first four are hashed in pairs, giving h(AB) and h(CD), which are then hashed together to give h(ABCD). The fifth hash has no partner at either level, so it is carried upward unchanged, and is finally hashed with h(ABCD) to give the root." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="30" y="26" width="72" height="34" rx="4"/><rect x="114" y="26" width="72" height="34" rx="4"/><rect x="198" y="26" width="72" height="34" rx="4"/><rect x="282" y="26" width="72" height="34" rx="4"/><rect x="366" y="26" width="72" height="34" rx="4"/><rect x="30" y="76" width="72" height="26" rx="4"/><rect x="114" y="76" width="72" height="26" rx="4"/><rect x="198" y="76" width="72" height="26" rx="4"/><rect x="282" y="76" width="72" height="26" rx="4"/><rect x="366" y="76" width="72" height="26" rx="4"/><path d="M66 60 L66 76"/><path d="M150 60 L150 76"/><path d="M234 60 L234 76"/><path d="M318 60 L318 76"/><path d="M402 60 L402 76"/><rect x="66" y="130" width="84" height="26" rx="4"/><rect x="234" y="130" width="84" height="26" rx="4"/><rect x="150" y="186" width="84" height="26" rx="4"/><rect x="255" y="242" width="84" height="30" rx="5"/><path d="M66 102 L108 126"/><path d="M150 102 L108 126"/><path d="M234 102 L276 126"/><path d="M318 102 L276 126"/><path d="M108 156 L192 182"/><path d="M276 156 L192 182"/><path d="M192 212 L297 238"/><path d="M402 102 L402 238 L339 238" stroke-dasharray="4 3"/></g><g fill="currentColor" stroke="none"><text x="66" y="47" font-size="12" text-anchor="middle" font-weight="700">A</text><text x="66" y="93" font-size="10" text-anchor="middle" font-family="monospace">h(A)</text><text x="150" y="47" font-size="12" text-anchor="middle" font-weight="700">B</text><text x="150" y="93" font-size="10" text-anchor="middle" font-family="monospace">h(B)</text><text x="234" y="47" font-size="12" text-anchor="middle" font-weight="700">C</text><text x="234" y="93" font-size="10" text-anchor="middle" font-family="monospace">h(C)</text><text x="318" y="47" font-size="12" text-anchor="middle" font-weight="700">D</text><text x="318" y="93" font-size="10" text-anchor="middle" font-family="monospace">h(D)</text><text x="402" y="47" font-size="12" text-anchor="middle" font-weight="700">E</text><text x="402" y="93" font-size="10" text-anchor="middle" font-family="monospace">h(E)</text><text x="108" y="147" font-size="10" text-anchor="middle" font-family="monospace">h(AB)</text><text x="276" y="147" font-size="10" text-anchor="middle" font-family="monospace">h(CD)</text><text x="192" y="203" font-size="10" text-anchor="middle" font-family="monospace">h(ABCD)</text><text x="297" y="262" font-size="11" text-anchor="middle" font-weight="700">ROOT</text><text x="408" y="150" font-size="9" opacity="0.8">no partner,</text><text x="408" y="162" font-size="9" opacity="0.8">so it rides</text><text x="408" y="174" font-size="9" opacity="0.8">up as it is</text><text x="14" y="16" font-size="10" opacity="0.8">five values &#8212; an odd number, so somebody has to decide what happens</text></g></svg>

**And you can prove one value belongs without revealing the others.** To convince somebody who knows only the root that a particular value is in the tree, you hand them the value plus the **sibling hash at each level** on the way up. They redo the hashing and see whether they arrive at the root they already trust. For a million values that's about twenty hashes — not a million.

That second property is the whole reason this structure exists rather than something simpler. **Verification without possession**, which is the same principle the [node](../nodes/what-a-node-is.md) page used to explain why pruning is safe.

### What happens when the count is odd

Five values, as above, and pairing leaves one hash with no partner — twice over. Something has to be decided, and the diagram shows one answer: **carry the lonely hash up unchanged** until it finds a partner.

That is a choice, not a consequence. Other systems make different ones: Bitcoin duplicates the odd hash and pairs it with itself; some schemes pad the level out with a fixed dummy hash. All three work.

What matters is that **the rule is fixed and the same everywhere.** If one implementation promoted and another duplicated, the same five values would give two different roots — and the fourth requirement above would be broken. The odd case is a small thing that has to be nailed down precisely *because* it is small and easy to leave to taste.

??? abstract "Ethereum doesn't actually pair things up"

    Worth saying before the picture sticks, because the binary tree above is a
    teaching device rather than a description.

    Pairwise hashing is the classic Merkle construction and the easiest way to
    see why a root commits to everything. **Ethereum's execution layer doesn't
    use it.** Its structure branches sixteen ways, not two, and a node hashes
    its children's references rather than pairing siblings — so the odd-number
    question never arises there at all. A branch node has however many
    children it has, and empty slots are simply empty.

    What carries over from Merkle is the *idea*: hash-linked nodes, a root that
    commits to everything beneath it, and membership provable from the values
    along one path. What doesn't carry over is the pairing.

    (Ethereum's **consensus** layer is a different matter — it does use a
    binary construction, padded out to a power of two. Which is one more way
    the two halves of a node differ, on top of the encodings the [RLP](rlp.md)
    page mentioned.)

## Second, the trie part

A Merkle tree commits to a *list*. Ethereum needs a **mapping**: given an address, find its account. So the second ingredient is a structure for looking things up.

Forget hashes for a moment and forget Ethereum. Suppose you want to store three words — `cat`, `car`, `do` — so that you can find any of them again.

A **trie** stores them by **spelling them out**. Start at the root. Take the first letter of your key and follow the branch marked with that letter. Take the second letter, follow that branch. Carry on until the key runs out, and whatever you find there is the value.

<svg viewBox="0 0 470 266" role="img" aria-label="A trie holding the keys cat, car and do. From the root, c leads to a, which divides into t and r, ending the keys cat and car. Separately d leads to o, which ends the key do. The c and d nodes each have a single child and carry no information beyond keep going." style="width:100%;max-width:27rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="150" y="14" width="80" height="28" rx="4"/><rect x="70" y="72" width="44" height="28" rx="4" stroke-dasharray="4 3"/><rect x="290" y="72" width="44" height="28" rx="4" stroke-dasharray="4 3"/><rect x="70" y="130" width="44" height="28" rx="4"/><rect x="268" y="130" width="92" height="40" rx="4"/><rect x="14" y="192" width="92" height="40" rx="4"/><rect x="118" y="192" width="92" height="40" rx="4"/><path d="M172 42 L92 68"/><path d="M208 42 L312 68"/><path d="M92 100 L92 126"/><path d="M312 100 L312 126"/><path d="M80 158 L60 188"/><path d="M104 158 L164 188"/></g><g fill="currentColor" stroke="none"><text x="190" y="33" font-size="11" text-anchor="middle" font-weight="700">root</text><text x="92" y="92" font-size="13" text-anchor="middle" font-family="monospace">c</text><text x="312" y="92" font-size="13" text-anchor="middle" font-family="monospace">d</text><text x="92" y="150" font-size="13" text-anchor="middle" font-family="monospace">a</text><text x="314" y="148" font-size="13" text-anchor="middle" font-family="monospace">o</text><text x="314" y="163" font-size="9" text-anchor="middle" opacity="0.8">ends "do"</text><text x="60" y="210" font-size="13" text-anchor="middle" font-family="monospace">t</text><text x="60" y="225" font-size="9" text-anchor="middle" opacity="0.8">ends "cat"</text><text x="164" y="210" font-size="13" text-anchor="middle" font-family="monospace">r</text><text x="164" y="225" font-size="9" text-anchor="middle" opacity="0.8">ends "car"</text><text x="366" y="88" font-size="9" opacity="0.8">one child,</text><text x="366" y="100" font-size="9" opacity="0.8">says nothing</text><text x="14" y="252" font-size="10" opacity="0.85">Keys: cat, car, do. Nothing is searched for &#8212; you spell the key out and arrive.</text><text x="14" y="264" font-size="9" opacity="0.7">The dashed nodes are the wasteful ones: one child each, carrying no information.</text></g></svg>

Two things to notice, and they're the reasons Ethereum wants this.

**Nothing is ever searched for.** You don't look through the structure comparing keys — you *spell* your key and the spelling walks you there. `car` means: root, then `c`, then `a`, then `r`. Three steps, no comparisons, and it would still be three steps with a billion other words in the tree.

**And the shape comes from the keys alone.** Insert the same three words in any order and you get the identical tree, because where a word sits is decided by its letters and nothing else. There is no rebalancing, no first-come advantage, no history.

That second point is **requirement (4), met for free** — and it is why two nodes that have never communicated compute the same root. Not by agreeing on anything: there was only ever one possible shape for those keys.

### What Ethereum does instead of letters

Same idea, two substitutions.

The keys aren't words, they're **32-byte hashes** — `keccak256` of an address, as the [accounts](../accounts/accounts.md) page described.

And the "letters" aren't letters. Ethereum reads a key **four bits at a time**, a unit called a **[nibble](../glossary.md#nibble "Four bits — half a byte, and exactly one hex digit")** — half a byte, which is exactly one hex digit. So instead of 26 possible branches at each step there are **sixteen**, one per hex digit, and a 32-byte key is **64 nibbles** long: a 64-letter word in a sixteen-letter alphabet.

Which is why the structure is drawn with hex digits on its branches. `a7f3…` is just a word spelled `a`, `7`, `f`, `3`, and finding its account means spelling it out.

## Third, the Patricia part

A pure trie has a problem. Keys here are 32 bytes — **64 nibbles** — so a key followed to its end passes through 64 levels. Where a key has no neighbours sharing its prefix, that means a long chain of nodes each with exactly one child, holding no information beyond "keep going".

The fix is **path compression**: collapse any such run into a single node that says "the next *n* nibbles are all this". The technique and the acronym come from [Morrison (1968)](#ref-morrison-1968) — PATRICIA, *Practical Algorithm To Retrieve Information Coded In Alphanumeric* — which is where Ethereum's structure gets the middle word of its name.

So the full name is a description of its parts: **Merkle** for the hashing that makes it a commitment, **Patricia** for the compression that keeps it shallow, **trie** for the keys determining the path.

## The three kinds of node

Those three ideas produce exactly three node types, specified in Appendix D of the Yellow Paper [(Wood, 2014)](#ref-wood-2014) along with the encoding rules that distinguish them.

| Node | Holds | Exists because |
| --- | --- | --- |
| **Leaf** | the rest of the key, and the value | the path has ended |
| **Extension** | a shared run of nibbles, and one child | path compression — the Patricia part |
| **Branch** | sixteen slots, one per nibble, plus a value | the path divides here |

A branch node has **seventeen** places, not sixteen: the extra one holds a value for a key that *ends* exactly at that branch, when one key is a prefix of another.

<svg viewBox="0 0 470 352" role="img" aria-label="A small trie holding three keys. The root is a branch node using slots 1 and 7. Slot 1 leads to an extension node carrying the shared nibble 2, which leads to a second branch using slots 3 and 5, each ending in a leaf. Slot 7 of the root leads straight to a leaf carrying the remaining nibbles 89a." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="158" y="36" width="154" height="40" rx="5"/><rect x="14" y="110" width="158" height="40" rx="5"/><rect x="296" y="110" width="160" height="54" rx="5"/><rect x="14" y="184" width="158" height="40" rx="5"/><rect x="10" y="258" width="76" height="54" rx="5"/><rect x="98" y="258" width="76" height="54" rx="5"/><path d="M200 76 L120 104"/><path d="M272 76 L350 104"/><path d="M93 150 L93 178"/><path d="M60 224 L48 252"/><path d="M120 224 L136 252"/></g><g fill="currentColor" stroke="none"><text x="14" y="16" font-size="10" opacity="0.8">keys, as nibbles:  1234 &#8594; alice   1256 &#8594; bob   789a &#8594; carol</text><text x="170" y="56" font-size="11" font-weight="700">BRANCH</text><text x="170" y="70" font-size="9" opacity="0.8">slots 1 and 7 are used</text><text x="26" y="130" font-size="11" font-weight="700">EXTENSION</text><text x="26" y="144" font-size="9" opacity="0.8">shared nibble: 2</text><text x="308" y="130" font-size="11" font-weight="700">LEAF</text><text x="308" y="144" font-size="9" opacity="0.8">rest of key: 89a</text><text x="308" y="158" font-size="9" opacity="0.8">value: carol</text><text x="26" y="204" font-size="11" font-weight="700">BRANCH</text><text x="26" y="218" font-size="9" opacity="0.8">slots 3 and 5 are used</text><text x="20" y="276" font-size="10" font-weight="700">LEAF</text><text x="20" y="289" font-size="8" opacity="0.8">rest: 4</text><text x="20" y="302" font-size="8" opacity="0.8">alice</text><text x="108" y="276" font-size="10" font-weight="700">LEAF</text><text x="108" y="289" font-size="8" opacity="0.8">rest: 6</text><text x="108" y="302" font-size="8" opacity="0.8">bob</text><text x="14" y="334" font-size="10" opacity="0.85">Every box is RLP-encoded and hashed, and each parent stores its children&#8217;s</text><text x="14" y="346" font-size="10" opacity="0.85">hashes &#8212; so the hash of the top box depends on all three values.</text></g></svg>

Follow `1256` through it. The root branch takes the `1` and sends you left. The extension says the next nibble is `2`, which matches, so continue. The second branch takes the `5`. The leaf says the rest of the key is `6` — it matches — and the value is yours. Four nibbles, three hops.

Now notice what the extension node bought: without it, `alice` and `bob` would need a separate single-child node for the shared `2`. With 64-nibble keys and millions of accounts, those runs are where nearly all the savings are.

## Why RLP is the prerequisite

Each node is turned into bytes with [RLP](rlp.md), and **the hash of a node is the hash of its RLP.**

Which is why the previous page had to come first, and why its obsession with canonicality was not pedantry. If a node could be encoded two ways, it would have two hashes, so its parent would have two hashes, and the root would not be a function of the state. **The root is well-defined only because the encoding is.**

??? abstract "Two details that surprise people"

    **Small nodes are inlined, not referenced.** A parent normally stores its
    child's 32-byte hash. But if a child's RLP comes to **less than 32 bytes**,
    the child is embedded in the parent directly instead — because a hash
    would be larger than the thing it points at. So the structure is not
    uniformly hash-linked, and a node's encoding can contain whole subtrees
    rather than references to them.

    **The empty trie has a root anyway.** It is the hash of RLP's empty
    string — `keccak256(0x80)`:

    ```
    56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421
    ```

    That constant is the `storageRoot` of every account with nothing stored,
    which is where the [accounts](../accounts/accounts.md) page met it. It is
    the same arrangement as `keccak256("")` being the code hash of an account
    with no code: emptiness still has to have a fingerprint, or "nothing
    stored" could not be distinguished from "anything at all".

## What a proof actually is

This is the payoff, and the reason the structure is worth its complexity.

A **proof** that some account holds some value is the chain of nodes from the root down to that account's leaf. Nothing more.

Given it, somebody holding only the root can check the claim themselves:

1. Hash the leaf, and confirm the node above references that hash.
2. Hash that node, and confirm the node above references *it*.
3. Continue to the top, and confirm the final hash is the root you already trusted.

If every link holds, the value is in the state — and if any byte of it had been altered, some hash along the way would not match.

**The size is the point.** A proof is one node per level, and the depth is bounded by the key length, so it is a handful of kilobytes regardless of whether the state holds a thousand accounts or a billion. Which is what makes a **light client** possible: software that stores no state at all, keeps only block headers, and asks others for proofs it can verify. It isn't trusting the answers. It's checking them against a root it obtained independently.

## Why the keys are hashed — and where they aren't

The [accounts](../accounts/accounts.md) page established that the state trie is keyed by `keccak256(address)` rather than by the address, as a defence: creating an account needs no key, so an attacker could otherwise dust a million addresses sharing a long prefix and force one branch of the trie to be pathologically deep.

What's worth adding here is **the contrast**, because it shows the hashing is a targeted defence and not a reflex.

A block's **transactions** and **receipts** also live in tries. Their keys are not hashed — they are the transaction's index, `0`, `1`, `2`, encoded with RLP. And they don't need hashing, because **nobody can choose them.** Indices are assigned by position in the block, so there is no way to craft one, and therefore nothing to defend against.

So the rule is sharper than "Ethereum hashes trie keys":

> **Hash the keys where an adversary picks them. Don't where they are assigned.**

Which is also a useful test to carry into other systems: ask who chooses the key, and the need for hashing answers itself.

## The four tries

| Trie | Key | Value | Keys hashed? |
| --- | --- | --- | --- |
| **State** | an address | the account's four fields | yes |
| **Storage**, one per contract | a 32-byte slot number | the stored value | yes |
| **Transactions**, one per block | the index in the block | the transaction | no |
| **Receipts**, one per block | the index in the block | the receipt | no |

The first two are the ones this site has been building towards: the state root in the block header, and each account's storage root inside its entry — **a trie whose leaves contain the roots of other tries.** Change one storage slot in one contract and that contract's storage root changes, so its account entry changes, so the state root changes. One number at the top, all the way down.

---

## Recap

- The structure must do four things: **commit to everything in 32 bytes, update cheaply, prove parts, and depend only on contents.** The fourth rules out most alternatives, because it forbids any shape that depends on insertion order.
- **Merkle**: hash the values, hash the hashes, up to one root. Changing any value changes the root, and one value can be proved with the sibling hashes along its path.
- **Trie**: the key is the route, read a nibble at a time, sixteen directions per branch. Lookup needs no search, and the shape comes from the keys rather than from history.
- **Patricia**: collapse single-child runs, so 64-nibble keys don't mean 64 levels.
- Three node types — **leaf, extension, branch** — and a branch has **seventeen** slots because a key can end where another divides.
- Nodes are hashed **after RLP encoding**, so the root is well-defined only because the encoding is canonical.
- A **proof** is the chain of nodes from root to leaf: a few kilobytes whatever the state's size, which is what makes light clients possible. **Verification without possession**, again.
- Keys are hashed in the state and storage tries and **not** in the transactions and receipts tries — because the first two have keys an adversary can choose and the last two do not. **Hash the keys where an adversary picks them.**
- Storage roots sit inside account entries, so it is **tries inside a trie**, and one slot changing reaches the top.

**Next:** [Transactions](../transactions/transactions.md) — what's actually in one, now that there's a way to write it down.

---

## References

<div class="sources" markdown>

- <a id="ref-eip6800"></a>**Buterin, V., Feist, D., Wedderburn, K., Ballet, G., Merriam, P., Herold, G., Hagopian, I., Jasoria, T., Singh, G., & Ferrin, D.** (2023). *EIP-6800: Ethereum state using a unified verkle tree.* Ethereum Improvement Proposals. The proposed replacement, aimed at far smaller proofs; marked *Stagnant* at the time of writing, which is the reason this page describes it as a direction rather than a plan. <https://eips.ethereum.org/EIPS/eip-6800>
- <a id="ref-merkle-1988"></a>**Merkle, R. C.** (1988). *A digital signature based on a conventional encryption function.* *Advances in Cryptology — CRYPTO '87*, 369–378. Springer. The origin of the hash tree: many values committed to by one, with membership provable from the hashes along a single path. <https://doi.org/10.1007/3-540-48184-2_32>
- <a id="ref-morrison-1968"></a>**Morrison, D. R.** (1968). *PATRICIA — Practical Algorithm To Retrieve Information Coded In Alphanumeric.* *Journal of the ACM*, 15(4), 514–534. The path-compressed trie Ethereum's structure takes its middle name from, published twenty-six years before the web. <https://doi.org/10.1145/321479.321481>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix D specifies the trie, including the node types, the hex-prefix encoding and the rule that nodes under 32 bytes are inlined. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
