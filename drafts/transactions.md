# Transactions

!!! warning "Stub — not written yet"

    This page is an outline. Delete this box when you fill it in.

## Questions this page should answer

- What is a transaction, in one sentence? (A signed instruction from an EOA to change the state.)
- What's inside one?
    - `nonce` — a counter for the sender
    - `gasLimit` — the most work you'll pay for
    - `to` — the recipient, or empty to deploy a contract
    - `value` — how much ether to send, in wei
    - `data` — arbitrary bytes; this is how you call a contract
    - `maxFeePerGas` / `maxPriorityFeePerGas` — what you'll pay
    - `v`, `r`, `s` — the signature
- Where does the *sender's* address live in all that? (Nowhere! It's recovered from the signature. Worth making a point of — it surprises everyone.)
- What are the three things a transaction can do? (Send ether, call a contract, create a contract.)
- What's a transaction *hash*, and when does it exist? (As soon as it's signed — before anyone has accepted it.)
- What does it mean for a transaction to fail? (It still happened, still cost gas, but the state changes were reverted.)

## Notes to self

- Decode one real transaction field by field. That single worked example teaches more than any amount of prose.
- Don't explain the signature maths here — point at the signatures page.
- The `data` field is the gateway to the whole EVM section. Flag it as important and move on.

**Next:** [The nonce](nonce.md)
