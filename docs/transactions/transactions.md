---
tier: 2
description: A signed instruction from an account, and the only thing that makes Ethereum do anything. Here is a real one, decoded byte by byte.
---

# Transactions

**[Permanent, except one part](../about/forks.md).** That a transaction is a signed instruction from an account, that the sender is recovered rather than stated, and that a failed one still costs money, have held since 2015. The *fee fields* changed in 2021, and the format now allows new kinds to be added — both covered below.

Nothing on Ethereum happens by itself. The [accounts](../accounts/accounts.md) page put it flatly: there are no timers, no scheduled jobs, no background processes, and every chain of execution begins with somebody signing something.

**This page is that something.**

!!! definition "Transaction"

    A signed instruction from an [externally owned account](../glossary.md#eoa),
    asking the network to change the state in a particular way. It is the only
    way anything on Ethereum begins. A transaction is not a request to be
    considered — it is an instruction that will be carried out **if it is
    valid and somebody includes it**, and whose effects are then permanent.

## What is in one

Seven things you choose, and three the signature leaves behind.

| Field | What it is |
| --- | --- |
| `nonce` | Which transaction of yours this is — the counter from the [nonce](../accounts/nonce.md) page |
| `gasLimit` | The most work you are willing to pay for |
| `to` | The recipient — or **empty**, which means *create a contract* |
| `value` | How much ether to send, in [wei](../foundations/ether.md) |
| `data` | Arbitrary bytes. Empty for a plain payment; for a contract, this is the call |
| `maxFeePerGas`<br>`maxPriorityFeePerGas` | What you are prepared to pay per unit of work [(Buterin et al., 2019)](#ref-eip1559) |
| `chainId` | Which chain this is for, so a signature valid here is not valid elsewhere [(Buterin, 2016)](#ref-eip155) |
| `v`, `r`, `s` | The [signature](../crypto/signatures.md) |

Two of those deserve attention before anything else.

**`to` being empty is not an omission.** It is the instruction *create a contract*, and it is the only way contracts come into existence — which is why the [smart contracts](../contracts/smart-contracts.md) page could say a contract is deployed by a transaction with nowhere to send it.

**`data` is the entire rest of the subject.** For a payment it is empty. For anything else it carries the function being called and its arguments, laid out by the [ABI](../contracts/smart-contracts.md) convention. Everything the EVM does begins as bytes in this field.

## One real transaction, decoded

Here is a complete, valid, signed transaction. It is 110 bytes:

```
0xf86c098504a817c800825208943535353535353535353535353535353535353535
  880de0b6b3a76400008025a028ef61340bd939bc2195fe537567866003e1a15d3c
  71ff63e1590620aa636276a067cbe9d8997f761aecb703304b3800ccf555c9f3dc
  64214b297fb1966a3b6d83
```

That is the whole thing — everything a node receives. Run it through [RLP](../encoding/rlp.md) and nine fields fall out:

| | Bytes | Value |
| --- | --- | --- |
| `nonce` | `09` | 9 |
| `gasPrice` | `04a817c800` | 20,000,000,000 wei = 20 gwei |
| `gasLimit` | `5208` | 21,000 |
| `to` | `3535…3535` | `0x3535353535353535353535353535353535353535` |
| `value` | `0de0b6b3a7640000` | 1,000,000,000,000,000,000 wei = **1 ether** |
| `data` | — | empty: this is a plain payment |
| `v` | `25` | 37 |
| `r` | `28ef6134…aa636276` | the signature's first half |
| `s` | `67cbe9d8…6a3b6d83` | the signature's second half |

Three things worth stopping on.

**`5208` is 21,000** — the cost of a plain transfer, which is where that number comes from. **`0de0b6b3a7640000` is 10<sup>18</sup>**, exactly one ether in wei, and it takes eight bytes because ether is counted in units that small. And **`data` is empty**, so this transaction does nothing but move money.

This one is an old-style transaction, from the worked example in the EIP that introduced chain ids [(Buterin, 2016)](#ref-eip155). That is deliberate: it is published, anyone can check it, and nothing here depends on taking this page's word for anything.

??? abstract "How this example was verified, and why that matters"

    The EIP publishes the bytes that get signed, and the hash of those bytes
    — the value the signature is actually over:

    ```
    0xdaf5a779ae972f972197303d7b574746c7ef83eadac0f2791ad23db92e4c8e53
    ```

    Hashing the signing bytes with [Keccak-256](../crypto/keccak256.md)
    reproduces exactly that value, and decoding the signed transaction
    reproduces every field the EIP states, including `r` and `s` as decimal
    numbers hundreds of digits long.

    So the table above is not transcribed from somewhere. The bytes were
    decoded, the hash recomputed, and both agreed with a document published
    in 2016 by someone who had no idea this page would exist. That is the
    only kind of claim this site is willing to make about a concrete
    example.

    (Its **transaction hash** — the thing you would paste into a block
    explorer — is `keccak256` of the 110 bytes above, which comes to
    `0x33469b22e9f636356c4160a87eb19df52b7412e8eac32a4a55ffe88ea8350788`.)

## The sender is nowhere in it

Go back through those nine fields and look for the sender's address.

**It is not there.** `to` is present; there is no `from`. A transaction never states who sent it.

The sender is **recovered** from the signature. Given the hash of what was signed, plus `v`, `r` and `s`, anyone can compute the public key that must have produced that signature, and from it the [address](../crypto/addresses.md) — the recovery the [signatures](../crypto/signatures.md) page described. Every node does this for every transaction, and it is where the sender comes from.

This is not a space-saving trick, though it saves twenty bytes. **A stated sender would be a claim; a recovered one is a proof.** If the field existed, a node would have to check that the signature matched it, and a mismatch would be a case to handle. There is no mismatch to handle when the address is *derived from* the signature: an invalid signature does not produce the wrong sender, it produces a different sender — some address nobody controls, whose nonce and balance will not satisfy the rules.

The consequence is one the [accounts](../accounts/accounts.md) page needed and could not yet explain: **a transaction's sender is whoever holds the key, and nothing else about the sender is ever asserted.** Identity here is not stated and checked. It is computed.

## Three things it can do

Every transaction is one of three, decided entirely by `to` and `data`:

- **Send ether.** `to` is an address, `data` is empty. Two numbers change.
- **Call a contract.** `to` is a contract's address, `data` says which function and with what arguments. Code runs.
- **Create a contract.** `to` is **empty**, and `data` is the code that will produce the contract's code. The new address is computed from the sender and their nonce, which is what the [nonce](../accounts/nonce.md) page meant about deployments.

There is no fourth. Anything more elaborate is one of these three with a contract doing the elaboration.

## It has a hash before anybody accepts it

A transaction's hash is `keccak256` of its bytes, and those bytes exist the moment it is signed. So the hash exists **before** any node has seen it, before any block contains it, and before anyone has decided whether it is valid.

Which is why a wallet can show you a transaction hash instantly and the explorer you paste it into says *not found*. Nothing is wrong. You have the name of something that so far exists only on your machine.

**A hash is an identifier, not a receipt.** It tells you what you signed. It tells you nothing about whether it happened.

## Failing is not the same as not happening

A transaction can be included in a block, execute, run out of gas or hit an error, and **fail** — and this is the part that surprises people:

**It still happened.** It is in the block, permanently. It still consumed gas, and you still paid for it. The sender's nonce still went up. What gets undone is only the **state changes the execution made**: balances and storage revert to what they were before it ran.

So failure is not rejection. The two are completely different:

- **Rejected** — the transaction was never valid (bad signature, wrong nonce, cannot cover its own fee). It never enters a block, costs nothing, and leaves no trace.
- **Failed** — it was valid, it ran, and it did not finish successfully. It is on the chain forever, it was paid for, and it changed nothing except the sender's nonce and balance.

That distinction is visible in the [receipt](../glossary.md#receipt), which carries a status code — `1` for success, `0` for failure — put there by the same change that took the intermediate state root out, described in the box further down [(Johnson, 2017)](#ref-eip658).

The reason is the same one that makes [metering](why-metering.md) necessary at all, which is the next page: **the work was done.** Nodes executed the code to discover it would fail. Somebody has to pay for work that has already happened, and letting failed transactions be free would make failing deliberately into a free denial of service.

## There is more than one kind now

The transaction above is a **legacy** transaction, and if a format were going to be permanent, that would be the one. It is not.

Since 2021 a transaction can begin with a **type byte**, declaring which of several formats follows [(Zoltu, 2020)](#ref-eip2718). The current ordinary kind replaces the single `gasPrice` above with the two fee fields in the table [(Buterin et al., 2019)](#ref-eip1559); others add further fields.

The way old and new are told apart is a small piece of elegance that the [RLP](../encoding/rlp.md) page already set up. **Look at the first byte.** RLP can only ever begin a list with a byte from `0xc0` upward, so every legacy transaction starts in that range — and the values from `0x00` to `0x7f`, which RLP would never produce for a list, were free. A transaction starting with one of those is a typed transaction, and the byte says which type [(Zoltu, 2020)](#ref-eip2718).

**Nothing had to be renegotiated to make room.** The space was already unused, because the encoding was specified tightly enough to leave a gap that meant nothing — and that is the practical value of the canonicality the RLP page spent so long on.

What does not change across any of this: a signed instruction, a recovered sender, a nonce, a gas limit, and the three things it can do.

## A transaction doesn't name the state it expects

The natural question, once [state roots](../accounts/state.md) are in view: when you sign a transaction, which one is it computed against? And should it carry that root, so the network knows what you assumed?

**It carries no state root, and no reference to one.** A transaction holds a nonce, a recipient, a value, some data, gas limits, fee terms, a chain id and a signature — the table above goes through them. Nothing in it describes the state it expects to meet.

So a transaction is an **instruction, not a statement about the world.** It says what to do. It says nothing about what it assumes.

The single exception is the [nonce](../accounts/nonce.md), and it's a revealing one. The nonce *is* a claim about state — "my account has sent exactly this many transactions" — but it constrains only your own account's position in its own sequence. About every other account, every balance and every contract's storage, your transaction is silent.

### What yours actually runs against

If it lands in block N, it executes against the state at the end of block N−1, plus the effects of every transaction ordered before it **within** block N.

That intermediate state is perfectly real, and **no root is published for it.** Ethereum commits to the state once per block, after all of it has run — which is the second of the two simplifications flagged back on [What is Ethereum?](../foundations/what-is-ethereum.md).

??? info "History: it used to publish one per transaction"

    This is not how it always worked, and the change is instructive.

    Until the Byzantium upgrade in 2017, every transaction **receipt** carried
    the state root as of that transaction — a published commitment after each
    one, not just each block. **EIP-658** [(Johnson, 2017)](#ref-eip658)
    replaced that field with a plain status code: `1` for success, `0` for
    failure.

    The reason was cost against benefit. Computing an intermediate root per
    transaction is real work for every node, and almost nothing used the
    result, whereas *did this transaction succeed?* was the question everyone
    actually asked and previously had to infer.

    So Ethereum once offered exactly the per-transaction commitment this
    section says doesn't exist, looked at the price, and sold it for a single
    bit of far more useful information.

### Why you shouldn't want to send one

It sounds safer to pin the state you signed against. It would be close to unusable.

A transaction naming a required state root would be invalidated by **any** change anywhere in the state — one unrelated transfer, by a stranger, in the same block. Since the state changes every block and thousands of transactions compete for each one, yours would have a useful life of a few seconds and would usually miss. A **mempool** — the pool of broadcast transactions waiting their turn — could not work at all, because waiting is exactly what would kill them.

So state-agnosticism is deliberate: it's what lets a transaction sit in a queue and remain valid. The bill arrives elsewhere, though, and it's worth knowing where:

- **You cannot pin the conditions you'll meet.** The state your transaction executes against is whatever exists at inclusion, not what existed when you signed.
- **Which is why contracts add their own guards.** Deadlines after which a call reverts, minimum amounts a trade must return — those exist because the protocol declines to offer them.
- **And it's the gap between simulating and executing.** A wallet shows you the outcome against the state as it stands now; the real outcome is against the state at inclusion, which nobody can predict. Much of what gets called front-running lives in that gap — which is this page's territory.

## Recap

- A transaction is a **signed instruction from an account**, and the only way anything on Ethereum starts.
- It holds a nonce, gas limit, recipient, value, data, fee terms, a chain id and a signature. **`to` empty means create a contract**, and `data` is where every contract call lives.
- **The sender is not in it.** It is recovered from the signature — a proof rather than a claim, which is why no mismatch between stated and actual sender is possible.
- Three things it can do: **send ether, call a contract, create a contract.** There is no fourth.
- Its **hash exists as soon as it is signed**, before any node has seen it. A hash is an identifier, not a receipt.
- **Failed is not rejected.** A failed transaction is on the chain forever and was paid for; only its state changes are reverted. A rejected one never existed.
- **It names no state.** It says what to do, never what it assumes — which is what lets it wait in a queue, and why contracts have to write their own guards.
- Since 2021 a leading **type byte** distinguishes formats, using a range of values RLP could never produce for a list. The old encoding left a gap because it was specified tightly.

**Next:** [Why metering is necessary](why-metering.md) — why the work has to be paid for, and counted.

---

## References

<div class="sources" markdown>

- <a id="ref-eip155"></a>**Buterin, V.** (2016). *EIP-155: Simple replay attack protection.* Ethereum Improvement Proposals, no. 155. Status: Final. Introduces the chain id into the signed data, so a signature valid on one chain is invalid on another. Its worked example — fields, signing bytes, signing hash, and the resulting signed transaction — is the one decoded on this page. <https://eips.ethereum.org/EIPS/eip-155>
- <a id="ref-eip1559"></a>**Buterin, V., Conner, E., Dudley, R., Slipper, M., Norden, I., & Bakhta, A.** (2019). *EIP-1559: Fee market change for ETH 1.0 chain.* Ethereum Improvement Proposals, no. 1559. Status: Final. Replaces the single `gasPrice` field with a maximum total fee and a maximum priority fee, separating what the protocol burns from what the proposer receives. <https://eips.ethereum.org/EIPS/eip-1559>
- <a id="ref-eip658"></a>**Johnson, N.** (2017). *EIP-658: Embedding transaction status code in receipts.* Ethereum Improvement Proposals, no. 658. Activated in Byzantium; replaced the per-transaction intermediate state root in receipts with a status code. <https://eips.ethereum.org/EIPS/eip-658>
- <a id="ref-eip2718"></a>**Zoltu, M.** (2020). *EIP-2718: Typed transaction envelope.* Ethereum Improvement Proposals, no. 2718. Status: Final. Defines the leading type byte, and specifies that values from `0x00` to `0x7f` indicate a typed transaction while `0xc0` to `0xfe` indicate a legacy RLP-encoded one — a range RLP leaves free. <https://eips.ethereum.org/EIPS/eip-2718>

</div>
