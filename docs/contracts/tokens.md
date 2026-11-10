---
tier: 1
description: A token is not a protocol feature. It is a contract keeping a list of numbers, and owning one means a number in somebody else's storage.
---

# Tokens aren't special

**[Permanent](../about/forks.md).** That tokens are contracts rather than a protocol feature has been true since the first one, and the standards describing them are finalised documents that cannot be revised.

Ethereum has **one** native asset: [ether](../foundations/ether.md). Everything else anyone holds on it — every stablecoin, every governance token, every collectible — is not a thing the protocol knows about.

It is a [contract](smart-contracts.md) keeping a list of numbers. Owning a token means **there is a number recorded against your address in somebody else's storage.**

That sounds reductive. It is the literal mechanism, and almost everything that surprises people about holding tokens falls out of it.

!!! definition "Token"

    A contract that records quantities against addresses and offers functions
    to move them. The protocol has **no concept** of a token: no field, no
    opcode, no rule. What makes a token a token is that its contract follows a
    published convention well enough for other software to recognise it.

## What a token actually is

Strip away everything optional and the core of a token contract is one line of storage and one function:

```
mapping(address => uint256) balances

function transfer(to, amount):
    require(balances[msg.sender] >= amount)
    balances[msg.sender] -= amount
    balances[to]         += amount
    emit Transfer(msg.sender, to, amount)
```

That is the whole idea. A transfer is **two numbers changed in one contract's storage**, plus a [log](events-and-logs.md) announcing it.

Nothing moved. Nothing was sent anywhere. One contract decremented an entry and incremented another, exactly as the [what is Ethereum](../foundations/what-is-ethereum.md) page described a balance transfer — except that there, the two numbers were fields of the accounts themselves, and here they are rows in a contract that happens to keep a list.

## Where your ether is, and where your tokens are

This is the whole page in one picture, and it is worth being slow about.

<svg viewBox="0 0 470 212" role="img" aria-label="On the left, your account with its four fields, the balance field marked as holding ether. On the right, a token contract whose storage holds a list of addresses and numbers, with one row marked as yours. Ether is a field of your own account; a token balance is a row in a contract's storage." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="10" y="30" width="180" height="112" rx="4"/><rect x="258" y="30" width="202" height="112" rx="4"/></g><g fill="currentColor" stroke="none"><text x="10" y="22" font-size="10" opacity="0.8">YOUR ACCOUNT</text><text x="258" y="22" font-size="10" opacity="0.8">A TOKEN CONTRACT &#183; its storage</text><text x="24" y="54" font-size="10" opacity="0.65">nonce</text><text x="24" y="76" font-size="10" font-weight="700">balance &#8212; your ether</text><text x="24" y="98" font-size="10" opacity="0.65">storageRoot</text><text x="24" y="120" font-size="10" opacity="0.65">codeHash</text><text x="272" y="54" font-size="10" opacity="0.65">0x9c&#8230; &#8594; 500</text><text x="272" y="76" font-size="10" opacity="0.65">0x4e&#8230; &#8594; 12</text><text x="272" y="98" font-size="10" font-weight="700">you &#8594; 240</text><text x="272" y="120" font-size="10" opacity="0.65">0xb1&#8230; &#8594; 9</text><text x="10" y="170" font-size="10">Your ether is a field of <tspan font-weight="700">your own account</tspan>. A token balance is a row in</text><text x="10" y="184" font-size="10"><tspan font-weight="700">a contract&#8217;s storage</tspan> &#8212; and that contract&#8217;s code decides what the row means,</text><text x="10" y="198" font-size="10">who may change it, and whether you can.</text></g></svg>

**Your ether balance is one of the four fields of your own account.** The [accounts](../accounts/accounts.md) page established those four, and `balance` is the second. Nobody's code sits between you and it. The protocol itself debits and credits that field, under rules no contract can alter.

**A token balance is a row in a different account's storage.** It lives under the [storageRoot](../accounts/accounts.md#the-two-fingerprints) of the token contract, not yours. Your account's four fields say nothing about it. If you held a thousand of some token and nothing else, your account would read: nonce, zero balance, empty storage, no code.

From which the rest of this page follows.

## Your ownership is exactly as good as that contract's code

Ether obeys the protocol. A token obeys **whatever its contract says**, and the contract was written by somebody.

If the code lets its author create new units, the author can. If it lets them freeze an address, they can. If it was written so that the code itself can be replaced later — and that is a thing contracts can be written to allow — then every rule above is provisional.

This is not a flaw being reported. It is what "a contract keeping a list" means. The [what a smart contract is](smart-contracts.md) page made the point that a contract is interesting because of what it is *forbidden* to do; a token is interesting for the same reason, and the forbidding is done by its own code rather than by Ethereum.

**So "can the issuer take mine?" is a question about that contract, not about Ethereum.** The honest general answer is: read the code, or accept that you are trusting someone. There is no protocol-level guarantee to fall back on, because at the protocol level there is no token.

## Your wallet doesn't hold your tokens. It asks.

A wallet, as the [seed phrases](../wallets/seed-phrases.md) page said, holds keys. It does not hold tokens — there is nothing to hold.

What it does is **call `balanceOf(your address)` on each token contract it has been told about**, and display the answers. The list you see is a list of questions your wallet decided to ask.

Two consequences follow, and both confuse people regularly.

**A token you have never heard of can appear in your wallet.** Somebody wrote your address into their contract and emitted a log saying so. You did not receive anything, you were not consulted, and nothing entered your account. Someone else's storage mentions you — which anyone can arrange, for anyone, since addresses [all exist already](../crypto/addresses.md) and need nobody's permission to be written down.

**A token you do hold can be invisible.** If your wallet does not know the contract exists, it never asks, and nothing appears. The balance is unaffected; it was never in the wallet to begin with.

The [events and logs](events-and-logs.md) page is what makes this workable in practice: the `Transfer` log is how any watcher learns that a row changed, since storage itself cannot be searched. **The log is the announcement; the storage row is the fact.** They are produced together by honest contracts, and nothing in the protocol requires a contract to be honest about it.

## You cannot move a token without ether

The fee for any transaction is payable in ether, as the [ether](../foundations/ether.md) page said, and only in ether. Moving a token requires a transaction. So:

**An account holding a fortune in tokens and no ether can receive anything and send nothing.** Not the tokens, not anything else. Receiving needs no transaction from you, so things can keep arriving, and the holdings sit there — visible, genuinely yours, and immovable — until somebody sends a little ether to the account.

The [why accounts](../accounts/why-accounts.md) page listed this among the costs of the account model, and here is the full reason. The protocol charges for work in the one asset it has any concept of. Everything else is a number in a contract, and a number in a contract cannot pay for the computation that changes it. Arrangements exist to have a third party supply the ether on your behalf, and all of them are machinery built to compensate for this one fact.

## A standard is an agreement, not a rule

Nothing in Ethereum defines what functions a token contract must have. What exists instead is a published document that most of them follow.

**ERC-20** [(Vogelsteller & Buterin, 2015)](#ref-erc20) specifies six required functions — `totalSupply`, `balanceOf`, `transfer`, `transferFrom`, `approve`, `allowance` — two required events, `Transfer` and `Approval`, and three optional ones: `name`, `symbol` and `decimals`.

That is the entire standard. Six functions, two events, three niceties.

**Nothing enforces it.** A contract that ignores the standard is a perfectly valid contract; it simply has no name every wallet already knows to call, so no wallet can display it and no exchange can list it. It is not rejected. It is unreadable.

Which makes the standard the same species of thing as the [ABI](smart-contracts.md), the derivation path on the [seed phrases](../wallets/seed-phrases.md) page, and the wordlist beside it: **a convention sitting above a protocol that has never heard of it.** Conventions all the way down, as the previous two pages kept finding.

??? abstract "Why a voluntary standard became compulsory in practice"

    This is an ordinary network externality, and the economics is well
    understood [(Katz & Shapiro, 1985)](#ref-katz-shapiro): the value of
    adopting a compatibility standard rises with the number of others who
    have adopted it, so beyond some threshold the private incentive to
    comply becomes overwhelming without anyone compelling anything.

    The threshold was crossed early here. Once wallets and exchanges
    supported the six functions, a new contract that chose differently
    would have had to persuade every piece of software in the ecosystem to
    make an exception for it. The standard is not enforced and is not
    optional either, which is a familiar position for a successful
    standard to end up in.

    Note what this costs. Defects in a widely-adopted standard are nearly
    impossible to repair, because the fix breaks compatibility — which is
    why the approval mechanism below still works the way it did in 2015.

`decimals` is worth a sentence, because it is purely cosmetic. A token contract stores whole numbers; `decimals` tells software where to draw a decimal point when displaying one. A balance of `240000000000000000000` with `decimals` of 18 is shown as 240. Nothing in the contract's arithmetic knows about it — the same arrangement as [wei and ether](../foundations/ether.md), which is where the convention of 18 came from in the first place.

## Approvals, and why they are the real hazard

`transfer` moves your own tokens. The other function, `transferFrom`, lets **somebody else** move them — which is how any contract you interact with gets paid, since a contract cannot reach into a token contract on your behalf without being allowed to.

Permission is granted by `approve`, and this is where loss actually happens.

<svg viewBox="0 0 470 236" role="img" aria-label="You call approve on the token contract, which records an allowance for another contract. At any later time that contract calls transferFrom, and the token contract moves your balance without asking you again." style="width:100%;max-width:30rem;height:auto"><g fill="none" stroke="currentColor" stroke-width="1"><rect x="10" y="44" width="116" height="34" rx="4"/><rect x="10" y="140" width="116" height="34" rx="4"/><rect x="286" y="34" width="174" height="146" rx="4"/><path d="M126 61 L270 61"/><path d="M126 157 L270 157"/></g><g fill="currentColor" stroke="none"><path d="M284 61 L270 56 L270 66 Z"/><path d="M284 157 L270 152 L270 162 Z"/><text x="68" y="65" font-size="10" text-anchor="middle">You</text><text x="68" y="161" font-size="10" text-anchor="middle">Another contract</text><text x="286" y="26" font-size="10" opacity="0.8">THE TOKEN CONTRACT</text><text x="300" y="60" font-size="10" opacity="0.65">balances</text><text x="312" y="78" font-size="10">you: 1000</text><text x="300" y="110" font-size="10" opacity="0.65">allowances</text><text x="312" y="128" font-size="10" font-weight="700">you &#8594; them: 1000</text><text x="300" y="160" font-size="10" opacity="0.65">&#8230; balances change</text><text x="132" y="52" font-size="10">1 &#183; approve(them, 1000)</text><text x="132" y="148" font-size="10">2 &#183; transferFrom(you, &#8230;)</text><text x="10" y="206" font-size="10">Step 2 can happen <tspan font-weight="700">at any time after step 1</tspan>, as many times as the</text><text x="10" y="220" font-size="10">allowance permits, and needs nothing further from you.</text></g></svg>

**The permission persists.** It is a row in storage, not a one-off authorisation. A [signature](../crypto/signatures.md) authorises exactly one message, once — that was the point of the whole signatures page. An allowance is the opposite: it sits there until something removes it, and every later `transferFrom` draws on it without consulting you again.

**And the token contract cannot judge the spender.** It has no way to know whether the address you approved is trustworthy, whether its code does what its authors claimed, or whether that code can be replaced tomorrow. It was told to record a permission, so it recorded one. The responsibility sits entirely with whoever granted it, and the token contract is not in a position to help.

!!! warning "What makes this structural rather than a bug"

    An approval is a **standing permission granted to an address**, and the
    address is the only thing it is bound to. Nothing ties it to a purpose,
    an amount you had in mind, a deadline, or a version of the code.

    So two facts, neither of which any software can fix:

    - An allowance you granted once remains in force until it is set back to
      zero, however long ago you granted it and whether or not you remember.
    - If the contract you approved is one whose code can be changed, you did
      not approve the behaviour you read about. You approved an address.

The standard itself carries a warning about one specific sharp edge. Changing an existing allowance is not atomic: a spender watching the chain can draw the old allowance and the new one. The document's own advice is that clients *"SHOULD make sure to create user interfaces in such a way that they set the allowance first to `0` before setting it to another value for the same spender"* [(Vogelsteller & Buterin, 2015)](#ref-erc20).

It is worth noticing what that sentence is. A finalised standard, acknowledging a defect it cannot repair, and asking the software around it to work around the problem. That is the cost named in the box above, made concrete.

## A collectible is the same shape

**ERC-721** [(Entriken et al., 2018)](#ref-erc721) is the convention behind non-fungible tokens, and mechanically it is the same object with the mapping turned around: instead of address to quantity, it records **token identifier to owner**. Everything on this page still applies — it is a contract keeping a list, the list is in its own storage, and owning one means that list names you.

The one addition worth knowing is `tokenURI`, which the standard describes as returning *"A distinct Uniform Resource Identifier (URI) for a given asset"* — ordinarily a web address. The picture, the name, the description: generally not on Ethereum. What is on Ethereum is a row saying you own identifier 4,312, and a string pointing somewhere else.

And the standard is explicit that the pointer need not be stable: *"The URI MAY be mutable (i.e. it changes from time to time)"* [(Entriken et al., 2018)](#ref-erc721). The rationale gives a perfectly sensible reason — an NFT representing a house should be able to update the house's details — but the consequence for an image is the same either way. **What the chain guarantees is the row. What the URI points at is somebody's web server**, with all the permanence that implies.

## Recap

- **Ethereum has one native asset, ether.** Every token is a contract keeping a list of numbers; the protocol has no field, no opcode and no rule concerning tokens.
- **Your ether is a field of your own account. A token balance is a row in someone else's storage.** That single difference generates everything else here.
- A transfer is **two numbers changed in one contract's storage**, plus a log announcing it. Nothing moves.
- **Your ownership is as good as that contract's code** — minting, freezing and upgrading are possible exactly when the code allows them, and Ethereum has no opinion on the matter.
- **Your wallet asks `balanceOf` and displays the answers.** So an unknown token can appear without your receiving anything, and a real holding can stay invisible.
- **Moving a token requires ether**, because fees are payable in nothing else. Tokens plus no ether is a holding you cannot move.
- **ERC-20 is six functions, two events and three optional extras** — an agreement, not a rule. Ignoring it produces a valid contract that no wallet can read.
- **An approval is a standing permission bound to an address**, lasting until revoked, and the token contract cannot assess who you gave it to.
- **A collectible is the same shape**, with a URI that the standard permits to change, pointing at something the chain never held.

**Next:** [RLP encoding](../encoding/rlp.md) — how all of this gets written down as bytes.

---

## References

<div class="sources" markdown>

- <a id="ref-erc721"></a>**Entriken, W., Shirley, D., Evans, J., & Sachs, N.** (2018). *EIP-721: Non-Fungible Token Standard.* Ethereum Improvement Proposals, no. 721. Status: Final. Defines `tokenURI` as returning "A distinct Uniform Resource Identifier (URI) for a given asset", and states in its rationale that "The URI MAY be mutable (i.e. it changes from time to time)." <https://eips.ethereum.org/EIPS/eip-721>
- <a id="ref-katz-shapiro"></a>**Katz, M. L., & Shapiro, C.** (1985). *Network externalities, competition, and compatibility.* American Economic Review 75(3), 424–440. The standard treatment of why the value of adopting a compatibility standard increases with the number of others who have adopted it, and why such standards become effectively compulsory without being enforced. <https://www.jstor.org/stable/1814809>
- <a id="ref-erc20"></a>**Vogelsteller, F., & Buterin, V.** (2015). *EIP-20: Token Standard.* Ethereum Improvement Proposals, no. 20. Status: Final. Specifies the six required methods, the `Transfer` and `Approval` events, and the three optional methods; and contains the warning that clients "SHOULD make sure to create user interfaces in such a way that they set the allowance first to `0` before setting it to another value for the same spender." <https://eips.ethereum.org/EIPS/eip-20>

</div>
