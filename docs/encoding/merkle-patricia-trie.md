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

Forget hashes for a moment and forget Ethereum. Suppose you want to store three words — `cats`, `cars`, `dog` — so that you can find any of them again.

A **trie** stores them by **spelling them out**. Start at the root. Take the first letter of your key and follow the branch marked with that letter. Take the second letter, follow that branch. Carry on until the key runs out, and whatever you find there is the value.

<svg viewBox="0 0 470 300" role="img" aria-label="A plain trie holding cats, cars and dog. From the root, c leads to a, which divides into t and r, each leading to an s that ends a key. Separately d leads to o, which leads to g. Ten nodes in total, and five of them have a single child and carry no information." style="width:100%;max-width:27rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="160" y="10" width="76" height="26" rx="4"/><rect x="76" y="60" width="40" height="26" rx="4" stroke-dasharray="4 3"/><rect x="300" y="60" width="40" height="26" rx="4" stroke-dasharray="4 3"/><rect x="76" y="110" width="40" height="26" rx="4"/><rect x="300" y="110" width="40" height="26" rx="4" stroke-dasharray="4 3"/><rect x="28" y="160" width="40" height="26" rx="4" stroke-dasharray="4 3"/><rect x="124" y="160" width="40" height="26" rx="4" stroke-dasharray="4 3"/><rect x="300" y="160" width="40" height="26" rx="4"/><rect x="14" y="212" width="68" height="40" rx="4"/><rect x="110" y="212" width="68" height="40" rx="4"/><rect x="286" y="212" width="68" height="40" rx="4"/><path d="M180 36 L96 56"/><path d="M216 36 L320 56"/><path d="M96 86 L96 106"/><path d="M320 86 L320 106"/><path d="M86 136 L58 156"/><path d="M106 136 L134 156"/><path d="M320 136 L320 156"/><path d="M48 186 L48 208"/><path d="M144 186 L144 208"/><path d="M320 186 L320 208"/></g><g fill="currentColor" stroke="none"><text x="198" y="28" font-size="11" text-anchor="middle" font-weight="700">root</text><text x="96" y="78" font-size="12" text-anchor="middle" font-family="monospace">c</text><text x="320" y="78" font-size="12" text-anchor="middle" font-family="monospace">d</text><text x="96" y="128" font-size="12" text-anchor="middle" font-family="monospace">a</text><text x="320" y="128" font-size="12" text-anchor="middle" font-family="monospace">o</text><text x="48" y="178" font-size="12" text-anchor="middle" font-family="monospace">t</text><text x="144" y="178" font-size="12" text-anchor="middle" font-family="monospace">r</text><text x="320" y="178" font-size="12" text-anchor="middle" font-family="monospace">g</text><text x="48" y="230" font-size="12" text-anchor="middle" font-family="monospace">s</text><text x="48" y="245" font-size="8" text-anchor="middle" opacity="0.8">ends cats</text><text x="144" y="230" font-size="12" text-anchor="middle" font-family="monospace">s</text><text x="144" y="245" font-size="8" text-anchor="middle" opacity="0.8">ends cars</text><text x="320" y="230" font-size="8" text-anchor="middle" opacity="0.8">ends dog</text><text x="14" y="276" font-size="10" opacity="0.85">Ten nodes. The five dashed ones have a single child and say only &#8220;keep going&#8221;.</text><text x="14" y="290" font-size="9" opacity="0.7">With 64-nibble keys, almost every node in the tree looks like one of those.</text></g></svg>

Two things to notice, and they're the reasons Ethereum wants this.

**Nothing is ever searched for.** You don't look through the structure comparing keys — you *spell* your key and the spelling walks you there. `cars` means: root, then `c`, then `a`, then `r`, then `s`. Four steps, no comparisons — and it would still be four steps with a billion other words in the tree.

**And the shape comes from the keys alone.** Insert the same three words in any order and you get the identical tree, because where a word sits is decided by its letters and nothing else. There is no rebalancing, no first-come advantage, no history.

That second point is **requirement (4), met for free** — and it is why two nodes that have never communicated compute the same root. Not by agreeing on anything: there was only ever one possible shape for those keys.

### What Ethereum does instead of letters

Same idea, two substitutions.

The keys aren't words, they're **32-byte hashes** — `keccak256` of an address, as the [accounts](../accounts/accounts.md) page described.

And the "letters" aren't letters. Ethereum reads a key **four bits at a time**, a unit called a **[nibble](../glossary.md#nibble "Four bits — half a byte, and exactly one hex digit")** — half a byte, which is exactly one hex digit. So instead of 26 possible branches at each step there are **sixteen**, one per hex digit, and a 32-byte key is **64 nibbles** long: a 64-letter word in a sixteen-letter alphabet.

Which is why the structure is drawn with hex digits on its branches. `a7f3…` is just a word spelled `a`, `7`, `f`, `3`, and finding its account means spelling it out.

## Third, the Patricia part

Look again at the dashed nodes in that diagram. Five of the ten exist only to say *keep going*: `c` has one child, `d` has one child, `o` has one child. They hold no value and make no decision. They are pure overhead.

With real keys this is not a minor inefficiency — it is nearly the whole tree. A key is 64 nibbles. Once a key's path diverges from everybody else's, every remaining nibble gets a node of its own, each with exactly one child. A single account could easily account for fifty such nodes, every one of them storing one nibble and a pointer.

**The fix is to collapse any run of single-child nodes into one node that holds the whole run.** Instead of `d → o → g`, a single node saying *"the rest of this path is `og`"*.

Applied to the same three keys:

<svg viewBox="0 0 470 258" role="img" aria-label="The same three keys after path compression. The root is a branch using slots c and d. Slot c leads to an extension node holding the shared letter a, then a branch on t and r, then two leaves each holding the remaining letter s. Slot d leads straight to a single leaf holding the whole remainder og. Six nodes instead of ten." style="width:100%;max-width:28rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="150" y="10" width="150" height="34" rx="5"/><rect x="20" y="70" width="150" height="34" rx="5"/><rect x="282" y="70" width="174" height="48" rx="5"/><rect x="20" y="130" width="150" height="34" rx="5"/><rect x="14" y="190" width="76" height="48" rx="5"/><rect x="100" y="190" width="76" height="48" rx="5"/><path d="M180 44 L95 66"/><path d="M270 44 L340 66"/><path d="M95 104 L95 126"/><path d="M80 164 L52 186"/><path d="M110 164 L138 186"/></g><g fill="currentColor" stroke="none"><text x="162" y="26" font-size="11" font-weight="700">BRANCH</text><text x="162" y="39" font-size="9" opacity="0.8">slots c and d used</text><text x="32" y="86" font-size="11" font-weight="700">EXTENSION</text><text x="32" y="99" font-size="9" opacity="0.8">shared letters: a</text><text x="294" y="86" font-size="11" font-weight="700">LEAF</text><text x="294" y="99" font-size="9" opacity="0.8">rest of key: og</text><text x="294" y="112" font-size="9" opacity="0.8">value for dog</text><text x="32" y="146" font-size="11" font-weight="700">BRANCH</text><text x="32" y="159" font-size="9" opacity="0.8">slots t and r used</text><text x="26" y="206" font-size="10" font-weight="700">LEAF</text><text x="26" y="219" font-size="8" opacity="0.8">rest: s</text><text x="26" y="231" font-size="8" opacity="0.8">cats</text><text x="112" y="206" font-size="10" font-weight="700">LEAF</text><text x="112" y="219" font-size="8" opacity="0.8">rest: s</text><text x="112" y="231" font-size="8" opacity="0.8">cars</text><text x="196" y="208" font-size="9" opacity="0.8">d, o and g became</text><text x="196" y="220" font-size="9" opacity="0.8">one leaf holding</text><text x="196" y="232" font-size="9" opacity="0.8">the whole tail</text><text x="14" y="252" font-size="10" opacity="0.85">Six nodes instead of ten, holding exactly the same three keys.</text></g></svg>

Walk it and nothing has changed about what's stored. `cars` still means root → `c` → `a` → `r` → `s`; it just takes three nodes to say it rather than five, because the shared `a` sits inside one node and the final `s` sits inside a leaf.

What's been removed is every node that had nothing to contribute. **Ten nodes became six, and with 64-nibble keys the same move turns tens of thousands into a handful.**

That technique is where the middle word of the name comes from: [Morrison (1968)](#ref-morrison-1968) called it PATRICIA — *Practical Algorithm To Retrieve Information Coded In Alphanumeric* — twenty-six years before the web.

So the full name describes its three parts: **Merkle** for the hashing that makes it a commitment, **Patricia** for the compression that keeps it shallow, and **trie** for the keys deciding the path.

## Building the node types one at a time

The compressed structure needs exactly three kinds of node, and the easiest way to see why is to build a trie from nothing and add what each step forces.

**Step 1 — one key.** You have a single key and a single value, and nothing to divide. So you need a node that says *"the rest of the path is this, and here's the value"*. That's a **leaf**: a remaining path plus a value. With only one key in the whole structure, the root *is* that leaf, and its remaining path is the entire key.

**Step 2 — a second key that goes elsewhere.** Add a key whose first nibble differs. Now the first nibble has to choose between two destinations, so you need a node that offers a choice. That's a **branch**: sixteen slots, one per possible nibble, each holding either nothing or a reference to the node you'd go to. Taking a step through a branch consumes one nibble of the key.

**Step 3 — two keys that agree for a while.** Add a key that shares the first twenty nibbles with an existing one. Branching on each of those twenty in turn would give twenty branch nodes with one slot filled each — the waste the previous section removed. So you need a node that says *"the next twenty nibbles are all this, then continue"*. That's an **extension**: a run of shared nibbles plus a single child.

**Step 4 — one key that stops where another carries on.** Here's the case most explanations skip. Suppose one key ends exactly at a point where other keys divide — the path `a7` has a value, and so do `a7f1` and `a7c2`. The branch at `a7` has to hold both the choices *and* a value for the key that finished there.

Which is why a branch has **seventeen** places rather than sixteen: sixteen slots for the nibbles, and a seventeenth for a value belonging to a key that ended right here. It's empty almost always — on hashed keys, one being a prefix of another is vanishingly rare — and the slot has to exist regardless, because the structure must handle it.

So, assembled:

| Node | Holds | Exists because |
| --- | --- | --- |
| **Leaf** | the rest of the key, and a value | the path ends here |
| **Extension** | a run of shared nibbles, and one child | a stretch of path divides nothing |
| **Branch** | sixteen slots, plus a value | the path divides here |

All three are specified in Appendix D of the Yellow Paper [(Wood, 2014)](#ref-wood-2014), along with the encoding trick that tells a leaf from an extension — both hold a path and something else, so a flag in the encoding distinguishes them.

<svg viewBox="0 0 470 352" role="img" aria-label="A small trie holding three keys. The root is a branch node using slots 1 and 7. Slot 1 leads to an extension node carrying the shared nibble 2, which leads to a second branch using slots 3 and 5, each ending in a leaf. Slot 7 of the root leads straight to a leaf carrying the remaining nibbles 89a." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="158" y="36" width="154" height="40" rx="5"/><rect x="14" y="110" width="158" height="40" rx="5"/><rect x="296" y="110" width="160" height="54" rx="5"/><rect x="14" y="184" width="158" height="40" rx="5"/><rect x="10" y="258" width="76" height="54" rx="5"/><rect x="98" y="258" width="76" height="54" rx="5"/><path d="M200 76 L120 104"/><path d="M272 76 L350 104"/><path d="M93 150 L93 178"/><path d="M60 224 L48 252"/><path d="M120 224 L136 252"/></g><g fill="currentColor" stroke="none"><text x="14" y="16" font-size="10" opacity="0.8">keys, as nibbles:  1234 &#8594; alice   1256 &#8594; bob   789a &#8594; carol</text><text x="170" y="56" font-size="11" font-weight="700">BRANCH</text><text x="170" y="70" font-size="9" opacity="0.8">slots 1 and 7 are used</text><text x="26" y="130" font-size="11" font-weight="700">EXTENSION</text><text x="26" y="144" font-size="9" opacity="0.8">shared nibble: 2</text><text x="308" y="130" font-size="11" font-weight="700">LEAF</text><text x="308" y="144" font-size="9" opacity="0.8">rest of key: 89a</text><text x="308" y="158" font-size="9" opacity="0.8">value: carol</text><text x="26" y="204" font-size="11" font-weight="700">BRANCH</text><text x="26" y="218" font-size="9" opacity="0.8">slots 3 and 5 are used</text><text x="20" y="276" font-size="10" font-weight="700">LEAF</text><text x="20" y="289" font-size="8" opacity="0.8">rest: 4</text><text x="20" y="302" font-size="8" opacity="0.8">alice</text><text x="108" y="276" font-size="10" font-weight="700">LEAF</text><text x="108" y="289" font-size="8" opacity="0.8">rest: 6</text><text x="108" y="302" font-size="8" opacity="0.8">bob</text><text x="14" y="334" font-size="10" opacity="0.85">Every box is RLP-encoded and hashed, and each parent stores its children&#8217;s</text><text x="14" y="346" font-size="10" opacity="0.85">hashes &#8212; so the hash of the top box depends on all three values.</text></g></svg>

Follow `1256` through it, nibble by nibble, and all four steps above appear in order:

1. **`1`** — the root is a **branch**. Slot 1 holds a reference, so take it. One nibble used, three left: `256`.
2. **`2`** — next is an **extension** saying the shared run is `2`. It matches what you hold, so continue past it. Two nibbles left: `56`.
3. **`5`** — a **branch** again, because this is where `alice` and `bob` part company. Slot 5 takes you onward. One nibble left: `6`.
4. **`6`** — a **leaf**, whose remaining path is `6`. It matches, so its value is the answer.

Four nibbles, four nodes, no comparisons and no searching. And had you asked for `1299`, step 3 would have found slot 9 of that branch empty — which is how the structure says *no such key* without looking anywhere else.

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
