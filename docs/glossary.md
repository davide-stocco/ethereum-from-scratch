---
tier: meta
description: Short definitions of every Ethereum term used on this site, each linking to the page that explains it properly.
---

# Glossary

Definitions here are deliberately **one or two sentences** — just enough to unstick you. Each links to the page that explains the thing properly.

If you arrived from a search engine and a word on some page made no sense, this is where to look.

!!! note "Scope"

    This covers every term used on the published pages. It grows as the site
    does — so if something is missing, it's because no page uses it yet. Terms
    without a link don't have their own page yet.

---

## A

**ABI**{ #abi } (Application Binary Interface)
: The convention for encoding calls to a contract — which function, and what arguments. Not a protocol rule, just an agreement everyone follows.

**Account**{ #account }
: An entry in Ethereum's state, identified by a 20-byte [address](crypto/addresses.md). Has four fields: nonce, balance, storage root, code hash. Comes in two kinds — EOA and contract. → [Accounts](accounts/accounts.md)

**Address**{ #address }
: The 20-byte identifier of an account, written as 40 hex characters. For an EOA it's the last 20 bytes of the Keccak-256 hash of the public key. → [Addresses](crypto/addresses.md)

## B

**Balance**{ #balance }
: How much ether an account holds, counted in [wei](foundations/ether.md).

**Beacon Chain**{ #beacon-chain }
: The Proof of Stake chain that ran separately from December 2020, holding no accounts or transactions. The Merge connected Ethereum's execution layer to it. → [What is Ethereum?](foundations/what-is-ethereum.md)

**Block**{ #block }
: A batch of transactions, added to the chain as a single unit. State is recorded once per block, not per transaction.

**Byte**{ #byte }
: Eight bits. The unit everything in Ethereum is measured in — addresses are 20 bytes, hashes are 32. → [Hex and bytes](foundations/hex-and-bytes.md)

## C

**Canonical**{ #canonical }
: Agreed on and permanently recorded by the network, as opposed to merely having existed. Intermediate states inside a block are real but not canonical.

**Consensus layer**{ #consensus-layer }
: The half of Ethereum that decides the *order* of transactions, using Proof of Stake. → [What is Ethereum?](foundations/what-is-ethereum.md)

**Contract account**{ #contract-account }
: An account with code attached. It cannot start a transaction — it only runs when something calls it. → [Accounts](accounts/accounts.md)

## D

**Determinism**{ #determinism }
: The property that the same state plus the same transaction always produces the same result, for everyone. This is what makes independent verification possible, and therefore what makes trust unnecessary. → [What is Ethereum?](foundations/what-is-ethereum.md)

## E

**EIP**{ #eip } (Ethereum Improvement Proposal)
: A numbered, published proposal for changing Ethereum. The authoritative description of any protocol rule. <https://eips.ethereum.org>

**EOA**{ #eoa } (Externally Owned Account)
: An account controlled by a private key rather than by code — what people mean by a wallet. The only kind that can start a transaction. → [Accounts](accounts/accounts.md)

**ether**{ #ether }
: Ethereum's native currency. Counted internally in [wei](foundations/ether.md), never in decimals.

**EVM**{ #evm } (Ethereum Virtual Machine)
: The machine that executes contract code — a stack machine working on 256-bit words. Every node runs it identically.

**Execution layer**{ #execution-layer }
: The half of Ethereum that holds the accounts and runs the code. The state machine proper. → [What is Ethereum?](foundations/what-is-ethereum.md)

## G

**Gas**{ #gas }
: The unit measuring computational work. Not money — gas is the *amount* of work, and the fee is what that work costs. Exists so that computation is paid for and so no contract can run forever.

**gwei**{ #gwei }
: 10<sup>9</sup> wei. The unit fees are normally quoted in. → [Ether, wei and gwei](foundations/ether.md)

## H

**Hard fork**{ #hard-fork }
: A coordinated rule change that every node adopts at an agreed point. Ethereum has had roughly twenty. → [Ethereum changes](about/forks.md)

**Hexadecimal (hex)**{ #hexadecimal-hex }
: Base 16, written with `0`–`9` and `a`–`f`. Used everywhere because one byte is exactly two hex characters. The `0x` prefix just means "hex follows". → [Hex and bytes](foundations/hex-and-bytes.md)

## K

**Keccak-256**{ #keccak-256 }
: Ethereum's hash function. Takes any input, returns 32 bytes. Nearly the same as SHA-3 but **not identical** — the padding differs, so the two give different results. → [Keccak-256](crypto/keccak256.md)

## N

**NIST**{ #nist } (National Institute of Standards and Technology)
: The United States government agency that publishes technical standards, cryptography among them, as documents called FIPS. It ran the competition that chose Keccak as SHA-3 — and then altered the padding before publication, which is why Ethereum's Keccak-256 and the SHA3-256 standard are different functions. → [Keccak-256](crypto/keccak256.md)

**Nonce**{ #nonce }
: A per-account counter of transactions already sent. Prevents the same signed transaction being replayed, and forces strict ordering. → [The nonce](accounts/nonce.md "A per-account counter of transactions already sent")

## O

**Oracle**{ #oracle }
: A service that reports off-chain facts to a contract. Necessary because contracts can't see outside the chain — and a point of trust whenever you need one. → [What is Ethereum?](foundations/what-is-ethereum.md)

## P

**Private key**{ #private-key }
: A 256-bit number. Whoever knows it can produce valid signatures for the matching address, which is what "owning" ether actually means. → [Private keys](crypto/private-keys.md)

**Proof of Stake**{ #proof-of-stake }
: The mechanism Ethereum uses to agree transaction order, where validators stake ether rather than spending electricity. Replaced mining at The Merge in September 2022.

**Public key**{ #public-key }
: A point on the secp256k1 curve, derived from a private key by one-way multiplication. An address is derived from it in turn. → [Public keys](crypto/public-keys.md)

## R

**Receipt**{ #receipt }
: The record of what a transaction did — gas used, logs emitted, success or failure. Committed per transaction, unlike state.

**RLP**{ #rlp } (Recursive Length Prefix)
: Ethereum's encoding for turning structured data into bytes. Canonical by design: one piece of data has exactly one valid encoding. → [RLP encoding](encoding/rlp.md)

## S

**secp256k1**{ #secp256k1 }
: The elliptic curve Ethereum uses for signatures — the same one Bitcoin uses. → [Public keys](crypto/public-keys.md)

**Script**{ #script }
: Bitcoin's scripting language. Deliberately stateless and limited, which is the real contrast with Ethereum's contracts — not that Bitcoin lacks code. → [What is Ethereum?](foundations/what-is-ethereum.md)

**Smart contract**{ #smart-contract }
: A program stored at an account, run by the network when called. Stateful and general-purpose, but metered and capped. → [What is Ethereum?](foundations/what-is-ethereum.md)

**State**{ #state }
: Everything Ethereum stores right now: every account and what it holds. → [What is Ethereum?](foundations/what-is-ethereum.md)

**State machine**{ #state-machine }
: A system with some state plus rules for changing it. Ethereum's own formal specification describes it this way. → [What is Ethereum?](foundations/what-is-ethereum.md)

**State root**{ #state-root }
: A single 32-byte fingerprint committing to the entire state, carried in each block header. Any change to any account changes it.

## T

**The Merge**{ #the-merge }
: The September 2022 upgrade that connected Ethereum's execution layer to the Beacon Chain, retiring mining. Called a merge because two existing systems were joined. → [What is Ethereum?](foundations/what-is-ethereum.md)

**Transaction**{ #transaction }
: A signed instruction from an EOA that changes the state. The only way anything on Ethereum ever changes.

**Turing-complete**{ #turing-complete }
: Able to express any computation, loops included. Ethereum's contracts are; Bitcoin's Script deliberately isn't. On Ethereum the limit is gas, not expressiveness. → [What is Ethereum?](foundations/what-is-ethereum.md)

## U

**UTXO**{ #utxo } (Unspent Transaction Output)
: Bitcoin's model, where individual coins are the state and each can be spent once. Ethereum uses accounts instead — which is why it needs a nonce. → [Accounts](accounts/accounts.md)

## W

**wei**{ #wei }
: The smallest unit of ether. 10<sup>18</sup> wei = 1 ether. All amounts are integers in wei; Ethereum never uses decimals. → [Ether, wei and gwei](foundations/ether.md)

## Y

**Yellow Paper**{ #yellow-paper }
: Ethereum's formal specification, by Gavin Wood. The authority on how the execution layer behaves. <https://ethereum.github.io/yellowpaper/paper.pdf>
