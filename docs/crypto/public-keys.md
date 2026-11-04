---
tier: 1
description: A public key is a point on a curve, computed from a private key by a step that is easy forwards and infeasible backwards.
---

# Public keys

**[Won't go out of date](../about/forks.md).** secp256k1 has been Ethereum's curve since it launched in 2015.

A [private key](private-keys.md) is a number you keep. A **public key** is what you get by running that number through a one-way calculation, and it's safe to publish.

!!! definition "Public key"

    A **point on the secp256k1 curve**, computed from a private key by
    multiplying a fixed, published point by it. Two coordinates, 32 bytes
    each, so 64 bytes in total.

    Easy to compute from the private key and infeasible to reverse — which
    is what makes it safe to publish.

The calculation involves an elliptic curve, which sounds forbidding and mostly isn't. You need three things from this page: what a public key *is*, why the step can't be reversed, and which of its several written forms Ethereum actually uses.

## The curve

secp256k1 is the set of points satisfying one equation:

```
y² = x³ + 7
```

### "Over a finite field" means clock arithmetic

Every number in that equation is kept inside a fixed range by **wrapping round**, exactly the way a clock does. Four hours after eleven o'clock is three, because the hours wrap at twelve. Written as arithmetic:

```
11 + 4 = 15,  and  15 wraps to 3   (because 15 − 12 = 3)
```

That's arithmetic *modulo 12*. secp256k1 does the same thing, with an enormous prime instead of twelve:

```
p = 2²⁵⁶ − 2³² − 977
```

So whenever a calculation on the curve produces a number at or above *p*, you subtract *p* until it fits. Every coordinate is a whole number between 0 and *p* − 1 — no decimals, no square roots in the ordinary sense, and nothing ever grows without limit.

Two consequences matter. There are **finitely many points**, which is what makes the set a usable mathematical object. And the points are **integer pairs**, not positions on a smooth line.

### So why does everyone draw a curve?

Because the same equation over the *real* numbers really is a smooth curve, and it's the easiest way to show how point addition works. Here it is:

<figure>
<svg viewBox="0 0 420 260" role="img" aria-label="The curve y squared equals x cubed plus 7 drawn over the real numbers, a smooth continuous shape" style="width:100%;max-width:26rem;height:auto"> <g stroke="currentColor" stroke-width="1" opacity="0.25"> <line x1="35" y1="127.5" x2="405" y2="127.5"/> <line x1="183.0" y1="15" x2="183.0" y2="235"/> </g> <path d="M 404.4,228.6 L 403.4,228.0 L 402.4,227.4 L 401.4,226.8 L 400.4,226.1 L 399.4,225.5 L 398.4,224.9 L 397.5,224.3 L 396.5,223.7 L 395.5,223.1 L 394.5,222.4 L 393.5,221.8 L 392.5,221.2 L 391.5,220.6 L 390.5,220.0 L 389.6,219.4 L 388.6,218.8 L 387.6,218.2 L 386.6,217.6 L 385.6,217.0 L 384.6,216.4 L 383.6,215.8 L 382.7,215.2 L 381.7,214.7 L 380.7,214.1 L 379.7,213.5 L 378.7,212.9 L 377.7,212.3 L 376.7,211.8 L 375.7,211.2 L 374.8,210.6 L 373.8,210.0 L 372.8,209.5 L 371.8,208.9 L 370.8,208.3 L 369.8,207.8 L 368.8,207.2 L 367.9,206.6 L 366.9,206.1 L 365.9,205.5 L 364.9,205.0 L 363.9,204.4 L 362.9,203.9 L 361.9,203.3 L 360.9,202.8 L 360.0,202.2 L 359.0,201.7 L 358.0,201.1 L 357.0,200.6 L 356.0,200.1 L 355.0,199.5 L 354.0,199.0 L 353.1,198.5 L 352.1,198.0 L 351.1,197.4 L 350.1,196.9 L 349.1,196.4 L 348.1,195.9 L 347.1,195.4 L 346.1,194.8 L 345.2,194.3 L 344.2,193.8 L 343.2,193.3 L 342.2,192.8 L 341.2,192.3 L 340.2,191.8 L 339.2,191.3 L 338.3,190.8 L 337.3,190.3 L 336.3,189.8 L 335.3,189.4 L 334.3,188.9 L 333.3,188.4 L 332.3,187.9 L 331.3,187.4 L 330.4,187.0 L 329.4,186.5 L 328.4,186.0 L 327.4,185.6 L 326.4,185.1 L 325.4,184.6 L 324.4,184.2 L 323.5,183.7 L 322.5,183.3 L 321.5,182.8 L 320.5,182.4 L 319.5,181.9 L 318.5,181.5 L 317.5,181.0 L 316.5,180.6 L 315.6,180.2 L 314.6,179.7 L 313.6,179.3 L 312.6,178.9 L 311.6,178.5 L 310.6,178.0 L 309.6,177.6 L 308.7,177.2 L 307.7,176.8 L 306.7,176.4 L 305.7,176.0 L 304.7,175.6 L 303.7,175.2 L 302.7,174.8 L 301.7,174.4 L 300.8,174.0 L 299.8,173.6 L 298.8,173.3 L 297.8,172.9 L 296.8,172.5 L 295.8,172.1 L 294.8,171.8 L 293.9,171.4 L 292.9,171.0 L 291.9,170.7 L 290.9,170.3 L 289.9,170.0 L 288.9,169.6 L 287.9,169.3 L 286.9,169.0 L 286.0,168.6 L 285.0,168.3 L 284.0,168.0 L 283.0,167.6 L 282.0,167.3 L 281.0,167.0 L 280.0,166.7 L 279.1,166.4 L 278.1,166.1 L 277.1,165.8 L 276.1,165.5 L 275.1,165.2 L 274.1,164.9 L 273.1,164.6 L 272.1,164.3 L 271.2,164.0 L 270.2,163.8 L 269.2,163.5 L 268.2,163.2 L 267.2,163.0 L 266.2,162.7 L 265.2,162.5 L 264.3,162.2 L 263.3,162.0 L 262.3,161.7 L 261.3,161.5 L 260.3,161.3 L 259.3,161.0 L 258.3,160.8 L 257.3,160.6 L 256.4,160.4 L 255.4,160.2 L 254.4,160.0 L 253.4,159.8 L 252.4,159.6 L 251.4,159.4 L 250.4,159.2 L 249.5,159.0 L 248.5,158.8 L 247.5,158.6 L 246.5,158.5 L 245.5,158.3 L 244.5,158.1 L 243.5,158.0 L 242.5,157.8 L 241.6,157.7 L 240.6,157.5 L 239.6,157.4 L 238.6,157.3 L 237.6,157.1 L 236.6,157.0 L 235.6,156.9 L 234.7,156.8 L 233.7,156.6 L 232.7,156.5 L 231.7,156.4 L 230.7,156.3 L 229.7,156.2 L 228.7,156.1 L 227.7,156.0 L 226.8,155.9 L 225.8,155.9 L 224.8,155.8 L 223.8,155.7 L 222.8,155.6 L 221.8,155.5 L 220.8,155.5 L 219.9,155.4 L 218.9,155.4 L 217.9,155.3 L 216.9,155.2 L 215.9,155.2 L 214.9,155.1 L 213.9,155.1 L 212.9,155.0 L 212.0,155.0 L 211.0,155.0 L 210.0,154.9 L 209.0,154.9 L 208.0,154.9 L 207.0,154.8 L 206.0,154.8 L 205.1,154.8 L 204.1,154.8 L 203.1,154.7 L 202.1,154.7 L 201.1,154.7 L 200.1,154.7 L 199.1,154.7 L 198.1,154.7 L 197.2,154.7 L 196.2,154.7 L 195.2,154.6 L 194.2,154.6 L 193.2,154.6 L 192.2,154.6 L 191.2,154.6 L 190.3,154.6 L 189.3,154.6 L 188.3,154.6 L 187.3,154.6 L 186.3,154.6 L 185.3,154.6 L 184.3,154.6 L 183.3,154.6 L 182.4,154.6 L 181.4,154.6 L 180.4,154.6 L 179.4,154.6 L 178.4,154.6 L 177.4,154.6 L 176.4,154.6 L 175.5,154.6 L 174.5,154.6 L 173.5,154.6 L 172.5,154.6 L 171.5,154.6 L 170.5,154.6 L 169.5,154.6 L 168.5,154.6 L 167.6,154.6 L 166.6,154.5 L 165.6,154.5 L 164.6,154.5 L 163.6,154.5 L 162.6,154.5 L 161.6,154.5 L 160.7,154.4 L 159.7,154.4 L 158.7,154.4 L 157.7,154.4 L 156.7,154.3 L 155.7,154.3 L 154.7,154.3 L 153.7,154.2 L 152.8,154.2 L 151.8,154.1 L 150.8,154.1 L 149.8,154.0 L 148.8,154.0 L 147.8,153.9 L 146.8,153.8 L 145.9,153.8 L 144.9,153.7 L 143.9,153.6 L 142.9,153.6 L 141.9,153.5 L 140.9,153.4 L 139.9,153.3 L 138.9,153.2 L 138.0,153.1 L 137.0,153.0 L 136.0,152.9 L 135.0,152.8 L 134.0,152.7 L 133.0,152.5 L 132.0,152.4 L 131.1,152.3 L 130.1,152.1 L 129.1,152.0 L 128.1,151.8 L 127.1,151.6 L 126.1,151.5 L 125.1,151.3 L 124.1,151.1 L 123.2,150.9 L 122.2,150.7 L 121.2,150.5 L 120.2,150.3 L 119.2,150.0 L 118.2,149.8 L 117.2,149.6 L 116.3,149.3 L 115.3,149.0 L 114.3,148.7 L 113.3,148.5 L 112.3,148.1 L 111.3,147.8 L 110.3,147.5 L 109.3,147.1 L 108.4,146.8 L 107.4,146.4 L 106.4,146.0 L 105.4,145.6 L 104.4,145.1 L 103.4,144.7 L 102.4,144.2 L 101.5,143.7 L 100.5,143.1 L 99.5,142.5 L 98.5,141.9 L 97.5,141.2 L 96.5,140.5 L 95.5,139.7 L 94.5,138.9 L 93.6,138.0 L 92.6,136.9 L 91.6,135.7 L 90.6,134.2 L 89.6,132.3 L 88.6,127.5 L 88.6,127.5 L 89.6,122.7 L 90.6,120.8 L 91.6,119.3 L 92.6,118.1 L 93.6,117.0 L 94.5,116.1 L 95.5,115.3 L 96.5,114.5 L 97.5,113.8 L 98.5,113.1 L 99.5,112.5 L 100.5,111.9 L 101.5,111.3 L 102.4,110.8 L 103.4,110.3 L 104.4,109.9 L 105.4,109.4 L 106.4,109.0 L 107.4,108.6 L 108.4,108.2 L 109.3,107.9 L 110.3,107.5 L 111.3,107.2 L 112.3,106.9 L 113.3,106.5 L 114.3,106.3 L 115.3,106.0 L 116.3,105.7 L 117.2,105.4 L 118.2,105.2 L 119.2,105.0 L 120.2,104.7 L 121.2,104.5 L 122.2,104.3 L 123.2,104.1 L 124.1,103.9 L 125.1,103.7 L 126.1,103.5 L 127.1,103.4 L 128.1,103.2 L 129.1,103.0 L 130.1,102.9 L 131.1,102.7 L 132.0,102.6 L 133.0,102.5 L 134.0,102.3 L 135.0,102.2 L 136.0,102.1 L 137.0,102.0 L 138.0,101.9 L 138.9,101.8 L 139.9,101.7 L 140.9,101.6 L 141.9,101.5 L 142.9,101.4 L 143.9,101.4 L 144.9,101.3 L 145.9,101.2 L 146.8,101.2 L 147.8,101.1 L 148.8,101.0 L 149.8,101.0 L 150.8,100.9 L 151.8,100.9 L 152.8,100.8 L 153.7,100.8 L 154.7,100.7 L 155.7,100.7 L 156.7,100.7 L 157.7,100.6 L 158.7,100.6 L 159.7,100.6 L 160.7,100.6 L 161.6,100.5 L 162.6,100.5 L 163.6,100.5 L 164.6,100.5 L 165.6,100.5 L 166.6,100.5 L 167.6,100.4 L 168.5,100.4 L 169.5,100.4 L 170.5,100.4 L 171.5,100.4 L 172.5,100.4 L 173.5,100.4 L 174.5,100.4 L 175.5,100.4 L 176.4,100.4 L 177.4,100.4 L 178.4,100.4 L 179.4,100.4 L 180.4,100.4 L 181.4,100.4 L 182.4,100.4 L 183.3,100.4 L 184.3,100.4 L 185.3,100.4 L 186.3,100.4 L 187.3,100.4 L 188.3,100.4 L 189.3,100.4 L 190.3,100.4 L 191.2,100.4 L 192.2,100.4 L 193.2,100.4 L 194.2,100.4 L 195.2,100.4 L 196.2,100.3 L 197.2,100.3 L 198.1,100.3 L 199.1,100.3 L 200.1,100.3 L 201.1,100.3 L 202.1,100.3 L 203.1,100.3 L 204.1,100.2 L 205.1,100.2 L 206.0,100.2 L 207.0,100.2 L 208.0,100.1 L 209.0,100.1 L 210.0,100.1 L 211.0,100.0 L 212.0,100.0 L 212.9,100.0 L 213.9,99.9 L 214.9,99.9 L 215.9,99.8 L 216.9,99.8 L 217.9,99.7 L 218.9,99.6 L 219.9,99.6 L 220.8,99.5 L 221.8,99.5 L 222.8,99.4 L 223.8,99.3 L 224.8,99.2 L 225.8,99.1 L 226.8,99.1 L 227.7,99.0 L 228.7,98.9 L 229.7,98.8 L 230.7,98.7 L 231.7,98.6 L 232.7,98.5 L 233.7,98.4 L 234.7,98.2 L 235.6,98.1 L 236.6,98.0 L 237.6,97.9 L 238.6,97.7 L 239.6,97.6 L 240.6,97.5 L 241.6,97.3 L 242.5,97.2 L 243.5,97.0 L 244.5,96.9 L 245.5,96.7 L 246.5,96.5 L 247.5,96.4 L 248.5,96.2 L 249.5,96.0 L 250.4,95.8 L 251.4,95.6 L 252.4,95.4 L 253.4,95.2 L 254.4,95.0 L 255.4,94.8 L 256.4,94.6 L 257.3,94.4 L 258.3,94.2 L 259.3,94.0 L 260.3,93.7 L 261.3,93.5 L 262.3,93.3 L 263.3,93.0 L 264.3,92.8 L 265.2,92.5 L 266.2,92.3 L 267.2,92.0 L 268.2,91.8 L 269.2,91.5 L 270.2,91.2 L 271.2,91.0 L 272.1,90.7 L 273.1,90.4 L 274.1,90.1 L 275.1,89.8 L 276.1,89.5 L 277.1,89.2 L 278.1,88.9 L 279.1,88.6 L 280.0,88.3 L 281.0,88.0 L 282.0,87.7 L 283.0,87.4 L 284.0,87.0 L 285.0,86.7 L 286.0,86.4 L 286.9,86.0 L 287.9,85.7 L 288.9,85.4 L 289.9,85.0 L 290.9,84.7 L 291.9,84.3 L 292.9,84.0 L 293.9,83.6 L 294.8,83.2 L 295.8,82.9 L 296.8,82.5 L 297.8,82.1 L 298.8,81.7 L 299.8,81.4 L 300.8,81.0 L 301.7,80.6 L 302.7,80.2 L 303.7,79.8 L 304.7,79.4 L 305.7,79.0 L 306.7,78.6 L 307.7,78.2 L 308.7,77.8 L 309.6,77.4 L 310.6,77.0 L 311.6,76.5 L 312.6,76.1 L 313.6,75.7 L 314.6,75.3 L 315.6,74.8 L 316.5,74.4 L 317.5,74.0 L 318.5,73.5 L 319.5,73.1 L 320.5,72.6 L 321.5,72.2 L 322.5,71.7 L 323.5,71.3 L 324.4,70.8 L 325.4,70.4 L 326.4,69.9 L 327.4,69.4 L 328.4,69.0 L 329.4,68.5 L 330.4,68.0 L 331.3,67.6 L 332.3,67.1 L 333.3,66.6 L 334.3,66.1 L 335.3,65.6 L 336.3,65.2 L 337.3,64.7 L 338.3,64.2 L 339.2,63.7 L 340.2,63.2 L 341.2,62.7 L 342.2,62.2 L 343.2,61.7 L 344.2,61.2 L 345.2,60.7 L 346.1,60.2 L 347.1,59.6 L 348.1,59.1 L 349.1,58.6 L 350.1,58.1 L 351.1,57.6 L 352.1,57.0 L 353.1,56.5 L 354.0,56.0 L 355.0,55.5 L 356.0,54.9 L 357.0,54.4 L 358.0,53.9 L 359.0,53.3 L 360.0,52.8 L 360.9,52.2 L 361.9,51.7 L 362.9,51.1 L 363.9,50.6 L 364.9,50.0 L 365.9,49.5 L 366.9,48.9 L 367.9,48.4 L 368.8,47.8 L 369.8,47.2 L 370.8,46.7 L 371.8,46.1 L 372.8,45.5 L 373.8,45.0 L 374.8,44.4 L 375.7,43.8 L 376.7,43.2 L 377.7,42.7 L 378.7,42.1 L 379.7,41.5 L 380.7,40.9 L 381.7,40.3 L 382.7,39.8 L 383.6,39.2 L 384.6,38.6 L 385.6,38.0 L 386.6,37.4 L 387.6,36.8 L 388.6,36.2 L 389.6,35.6 L 390.5,35.0 L 391.5,34.4 L 392.5,33.8 L 393.5,33.2 L 394.5,32.6 L 395.5,31.9 L 396.5,31.3 L 397.5,30.7 L 398.4,30.1 L 399.4,29.5 L 400.4,28.9 L 401.4,28.2 L 402.4,27.6 L 403.4,27.0 L 404.4,26.4" fill="none" stroke="currentColor" stroke-width="2"/> <text x="408" y="141.5" font-size="11" fill="currentColor" opacity="0.6" text-anchor="end">x</text> <text x="191.0" y="22" font-size="11" fill="currentColor" opacity="0.6">y</text> </svg>
<figcaption>y² = x³ + 7 over the real numbers — a genuine curve, and what every diagram of this shows.</figcaption>
</figure>

That picture is honest about the **structure** and misleading about the **shape**.

Now keep the equation exactly as it is and change only one thing: every calculation wraps round, in the clock sense above. The modulus is doing all the work here — it isn't a detail alongside the equation, it's the entire difference between the two pictures.

Here's what that does, with 97 as the modulus. Ask whether *x* = 1 has a point on the curve:

```
x³ + 7  =  1 + 7  =  8
```

Over the real numbers you'd need *y* = √8 ≈ 2.828 — not a whole number, so there's no integer point there at all. With wrapping, try *y* = 28:

```
28²  =  784
784  =  8 × 97 + 8      so 784 wraps round to 8   ✓
```

Which is exactly *x*³ + 7. So **(1, 28) is on the curve**, even though 28 is nothing like √8. Wrapping lets large coordinates satisfy the equation, and that's why the solutions end up scattered rather than lying along a line.

Doing that for every *x* from 0 to 96 gives:

<figure>
<svg viewBox="0 0 300 300" role="img" aria-label="The same equation over the field of 97 elements: 78 scattered points with no curved shape" style="width:100%;max-width:22rem;height:auto"> <g stroke="currentColor" stroke-width="1" opacity="0.25"> <line x1="30" y1="275" x2="290" y2="275"/> <line x1="30" y1="15" x2="30" y2="275"/> </g> <circle cx="32.7" cy="200.6" r="2.6" fill="currentColor"/><circle cx="32.7" cy="91.7" r="2.6" fill="currentColor"/><circle cx="43.3" cy="179.4" r="2.6" fill="currentColor"/><circle cx="43.3" cy="113.0" r="2.6" fill="currentColor"/><circle cx="61.9" cy="174.1" r="2.6" fill="currentColor"/><circle cx="61.9" cy="118.3" r="2.6" fill="currentColor"/><circle cx="64.5" cy="224.5" r="2.6" fill="currentColor"/><circle cx="64.5" cy="67.8" r="2.6" fill="currentColor"/><circle cx="67.2" cy="179.4" r="2.6" fill="currentColor"/><circle cx="67.2" cy="113.0" r="2.6" fill="currentColor"/><circle cx="75.2" cy="224.5" r="2.6" fill="currentColor"/><circle cx="75.2" cy="67.8" r="2.6" fill="currentColor"/><circle cx="83.1" cy="219.2" r="2.6" fill="currentColor"/><circle cx="83.1" cy="73.1" r="2.6" fill="currentColor"/><circle cx="85.8" cy="219.2" r="2.6" fill="currentColor"/><circle cx="85.8" cy="73.1" r="2.6" fill="currentColor"/><circle cx="91.1" cy="256.4" r="2.6" fill="currentColor"/><circle cx="91.1" cy="35.9" r="2.6" fill="currentColor"/><circle cx="101.7" cy="216.6" r="2.6" fill="currentColor"/><circle cx="101.7" cy="75.8" r="2.6" fill="currentColor"/><circle cx="107.0" cy="256.4" r="2.6" fill="currentColor"/><circle cx="107.0" cy="35.9" r="2.6" fill="currentColor"/><circle cx="115.0" cy="174.1" r="2.6" fill="currentColor"/><circle cx="115.0" cy="118.3" r="2.6" fill="currentColor"/><circle cx="117.7" cy="190.0" r="2.6" fill="currentColor"/><circle cx="117.7" cy="102.3" r="2.6" fill="currentColor"/><circle cx="123.0" cy="200.6" r="2.6" fill="currentColor"/><circle cx="123.0" cy="91.7" r="2.6" fill="currentColor"/><circle cx="125.6" cy="160.8" r="2.6" fill="currentColor"/><circle cx="125.6" cy="131.6" r="2.6" fill="currentColor"/><circle cx="146.9" cy="261.7" r="2.6" fill="currentColor"/><circle cx="146.9" cy="30.6" r="2.6" fill="currentColor"/><circle cx="149.5" cy="256.4" r="2.6" fill="currentColor"/><circle cx="149.5" cy="35.9" r="2.6" fill="currentColor"/><circle cx="168.1" cy="232.5" r="2.6" fill="currentColor"/><circle cx="168.1" cy="59.8" r="2.6" fill="currentColor"/><circle cx="170.8" cy="174.1" r="2.6" fill="currentColor"/><circle cx="170.8" cy="118.3" r="2.6" fill="currentColor"/><circle cx="176.1" cy="195.3" r="2.6" fill="currentColor"/><circle cx="176.1" cy="97.0" r="2.6" fill="currentColor"/><circle cx="178.8" cy="219.2" r="2.6" fill="currentColor"/><circle cx="178.8" cy="73.1" r="2.6" fill="currentColor"/><circle cx="181.4" cy="195.3" r="2.6" fill="currentColor"/><circle cx="181.4" cy="97.0" r="2.6" fill="currentColor"/><circle cx="189.4" cy="155.5" r="2.6" fill="currentColor"/><circle cx="189.4" cy="136.9" r="2.6" fill="currentColor"/><circle cx="192.0" cy="200.6" r="2.6" fill="currentColor"/><circle cx="192.0" cy="91.7" r="2.6" fill="currentColor"/><circle cx="194.7" cy="160.8" r="2.6" fill="currentColor"/><circle cx="194.7" cy="131.6" r="2.6" fill="currentColor"/><circle cx="197.3" cy="155.5" r="2.6" fill="currentColor"/><circle cx="197.3" cy="136.9" r="2.6" fill="currentColor"/><circle cx="202.7" cy="261.7" r="2.6" fill="currentColor"/><circle cx="202.7" cy="30.6" r="2.6" fill="currentColor"/><circle cx="208.0" cy="224.5" r="2.6" fill="currentColor"/><circle cx="208.0" cy="67.8" r="2.6" fill="currentColor"/><circle cx="210.6" cy="232.5" r="2.6" fill="currentColor"/><circle cx="210.6" cy="59.8" r="2.6" fill="currentColor"/><circle cx="218.6" cy="155.5" r="2.6" fill="currentColor"/><circle cx="218.6" cy="136.9" r="2.6" fill="currentColor"/><circle cx="221.2" cy="216.6" r="2.6" fill="currentColor"/><circle cx="221.2" cy="75.8" r="2.6" fill="currentColor"/><circle cx="223.9" cy="190.0" r="2.6" fill="currentColor"/><circle cx="223.9" cy="102.3" r="2.6" fill="currentColor"/><circle cx="226.6" cy="232.5" r="2.6" fill="currentColor"/><circle cx="226.6" cy="59.8" r="2.6" fill="currentColor"/><circle cx="237.2" cy="179.4" r="2.6" fill="currentColor"/><circle cx="237.2" cy="113.0" r="2.6" fill="currentColor"/><circle cx="247.8" cy="195.3" r="2.6" fill="currentColor"/><circle cx="247.8" cy="97.0" r="2.6" fill="currentColor"/><circle cx="255.8" cy="261.7" r="2.6" fill="currentColor"/><circle cx="255.8" cy="30.6" r="2.6" fill="currentColor"/><circle cx="263.8" cy="190.0" r="2.6" fill="currentColor"/><circle cx="263.8" cy="102.3" r="2.6" fill="currentColor"/><circle cx="282.3" cy="216.6" r="2.6" fill="currentColor"/><circle cx="282.3" cy="75.8" r="2.6" fill="currentColor"/><circle cx="285.0" cy="160.8" r="2.6" fill="currentColor"/><circle cx="285.0" cy="131.6" r="2.6" fill="currentColor"/> <text x="290" y="291" font-size="10" fill="currentColor" opacity="0.6" text-anchor="end">x → 96</text> <text x="14" y="22" font-size="10" fill="currentColor" opacity="0.6">96</text> </svg>
<figcaption>The same equation, with the arithmetic wrapped at 97 instead of carried out over the reals. 78 points, and nothing remotely curved.</figcaption>
</figure>

Same equation, no curve. The wrapping is what destroys the shape: a coordinate that would have carried on climbing instead falls back to the bottom of the range, so neighbouring values of *x* land nowhere near each other. What's left is scattered dots, symmetric about the middle because *y* and *p* − *y* are both solutions.

secp256k1 is this second picture, with 97 replaced by a prime of 78 digits and roughly 10⁷⁷ points rather than 78. Nobody draws *that*.

So when you see a smooth curve with points labelled on it, read it as a **diagram of the rules**, not a map of the territory. The rules carry over exactly; the shape does not.

??? note "Why the real-number picture is still worth having"

    The geometry is where point addition comes from, and it's genuinely
    visual. To add two points **P** and **Q** on the real curve:

    1. Draw a straight line through them.
    2. That line crosses the curve at exactly one more place. Call it **R**.
    3. Reflect **R** across the horizontal axis. That reflection is **P + Q**.

    Only **R** gets reflected. P and Q stay exactly where they are — they're
    the inputs, and the answer appears somewhere else entirely.

    <svg viewBox="0 0 470 320" role="img" aria-label="Adding two points P and Q on the real curve. A straight line through P and Q crosses the curve a third time at R. Reflecting R across the horizontal axis gives P plus Q." style="width:100%;max-width:28rem;height:auto"> <g stroke="currentColor" stroke-width="1" opacity="0.22"> <line x1="40" y1="158.0" x2="456" y2="158.0"/> <line x1="196.4" y1="12" x2="196.4" y2="292"/> </g> <path d="M 437.7,287.4 L 436.8,286.7 L 435.9,286.1 L 435.0,285.4 L 434.1,284.8 L 433.2,284.1 L 432.3,283.5 L 431.4,282.9 L 430.5,282.2 L 429.6,281.6 L 428.7,280.9 L 427.8,280.3 L 426.9,279.7 L 426.0,279.0 L 425.1,278.4 L 424.1,277.8 L 423.2,277.1 L 422.3,276.5 L 421.4,275.9 L 420.5,275.3 L 419.6,274.6 L 418.7,274.0 L 417.8,273.4 L 416.9,272.8 L 416.0,272.2 L 415.1,271.5 L 414.2,270.9 L 413.3,270.3 L 412.4,269.7 L 411.5,269.1 L 410.6,268.5 L 409.7,267.9 L 408.8,267.3 L 407.9,266.7 L 407.0,266.1 L 406.1,265.5 L 405.2,264.9 L 404.3,264.3 L 403.4,263.7 L 402.5,263.1 L 401.6,262.5 L 400.7,262.0 L 399.8,261.4 L 398.9,260.8 L 398.0,260.2 L 397.1,259.6 L 396.2,259.1 L 395.3,258.5 L 394.4,257.9 L 393.5,257.3 L 392.6,256.8 L 391.7,256.2 L 390.8,255.6 L 389.9,255.1 L 389.0,254.5 L 388.1,254.0 L 387.2,253.4 L 386.3,252.9 L 385.4,252.3 L 384.5,251.8 L 383.6,251.2 L 382.6,250.7 L 381.7,250.1 L 380.8,249.6 L 379.9,249.0 L 379.0,248.5 L 378.1,248.0 L 377.2,247.4 L 376.3,246.9 L 375.4,246.4 L 374.5,245.8 L 373.6,245.3 L 372.7,244.8 L 371.8,244.3 L 370.9,243.8 L 370.0,243.2 L 369.1,242.7 L 368.2,242.2 L 367.3,241.7 L 366.4,241.2 L 365.5,240.7 L 364.6,240.2 L 363.7,239.7 L 362.8,239.2 L 361.9,238.7 L 361.0,238.2 L 360.1,237.7 L 359.2,237.2 L 358.3,236.7 L 357.4,236.3 L 356.5,235.8 L 355.6,235.3 L 354.7,234.8 L 353.8,234.4 L 352.9,233.9 L 352.0,233.4 L 351.1,232.9 L 350.2,232.5 L 349.3,232.0 L 348.4,231.6 L 347.5,231.1 L 346.6,230.7 L 345.7,230.2 L 344.8,229.8 L 343.9,229.3 L 343.0,228.9 L 342.1,228.4 L 341.1,228.0 L 340.2,227.6 L 339.3,227.1 L 338.4,226.7 L 337.5,226.3 L 336.6,225.9 L 335.7,225.4 L 334.8,225.0 L 333.9,224.6 L 333.0,224.2 L 332.1,223.8 L 331.2,223.4 L 330.3,223.0 L 329.4,222.6 L 328.5,222.2 L 327.6,221.8 L 326.7,221.4 L 325.8,221.0 L 324.9,220.6 L 324.0,220.2 L 323.1,219.9 L 322.2,219.5 L 321.3,219.1 L 320.4,218.7 L 319.5,218.4 L 318.6,218.0 L 317.7,217.6 L 316.8,217.3 L 315.9,216.9 L 315.0,216.6 L 314.1,216.2 L 313.2,215.9 L 312.3,215.5 L 311.4,215.2 L 310.5,214.9 L 309.6,214.5 L 308.7,214.2 L 307.8,213.9 L 306.9,213.6 L 306.0,213.2 L 305.1,212.9 L 304.2,212.6 L 303.3,212.3 L 302.4,212.0 L 301.5,211.7 L 300.6,211.4 L 299.6,211.1 L 298.7,210.8 L 297.8,210.5 L 296.9,210.3 L 296.0,210.0 L 295.1,209.7 L 294.2,209.4 L 293.3,209.2 L 292.4,208.9 L 291.5,208.6 L 290.6,208.4 L 289.7,208.1 L 288.8,207.9 L 287.9,207.6 L 287.0,207.4 L 286.1,207.1 L 285.2,206.9 L 284.3,206.7 L 283.4,206.4 L 282.5,206.2 L 281.6,206.0 L 280.7,205.8 L 279.8,205.6 L 278.9,205.3 L 278.0,205.1 L 277.1,204.9 L 276.2,204.7 L 275.3,204.5 L 274.4,204.3 L 273.5,204.2 L 272.6,204.0 L 271.7,203.8 L 270.8,203.6 L 269.9,203.4 L 269.0,203.3 L 268.1,203.1 L 267.2,202.9 L 266.3,202.8 L 265.4,202.6 L 264.5,202.5 L 263.6,202.3 L 262.7,202.2 L 261.8,202.0 L 260.9,201.9 L 260.0,201.7 L 259.1,201.6 L 258.1,201.5 L 257.2,201.4 L 256.3,201.2 L 255.4,201.1 L 254.5,201.0 L 253.6,200.9 L 252.7,200.8 L 251.8,200.7 L 250.9,200.6 L 250.0,200.5 L 249.1,200.4 L 248.2,200.3 L 247.3,200.2 L 246.4,200.1 L 245.5,200.0 L 244.6,199.9 L 243.7,199.8 L 242.8,199.8 L 241.9,199.7 L 241.0,199.6 L 240.1,199.6 L 239.2,199.5 L 238.3,199.4 L 237.4,199.4 L 236.5,199.3 L 235.6,199.3 L 234.7,199.2 L 233.8,199.2 L 232.9,199.1 L 232.0,199.1 L 231.1,199.0 L 230.2,199.0 L 229.3,198.9 L 228.4,198.9 L 227.5,198.9 L 226.6,198.8 L 225.7,198.8 L 224.8,198.8 L 223.9,198.7 L 223.0,198.7 L 222.1,198.7 L 221.2,198.7 L 220.3,198.6 L 219.4,198.6 L 218.5,198.6 L 217.6,198.6 L 216.6,198.6 L 215.7,198.6 L 214.8,198.5 L 213.9,198.5 L 213.0,198.5 L 212.1,198.5 L 211.2,198.5 L 210.3,198.5 L 209.4,198.5 L 208.5,198.5 L 207.6,198.5 L 206.7,198.5 L 205.8,198.5 L 204.9,198.5 L 204.0,198.5 L 203.1,198.5 L 202.2,198.5 L 201.3,198.5 L 200.4,198.5 L 199.5,198.5 L 198.6,198.5 L 197.7,198.5 L 196.8,198.5 L 195.9,198.5 L 195.0,198.5 L 194.1,198.5 L 193.2,198.5 L 192.3,198.5 L 191.4,198.5 L 190.5,198.5 L 189.6,198.5 L 188.7,198.5 L 187.8,198.5 L 186.9,198.5 L 186.0,198.4 L 185.1,198.4 L 184.2,198.4 L 183.3,198.4 L 182.4,198.4 L 181.5,198.4 L 180.6,198.4 L 179.7,198.4 L 178.8,198.4 L 177.9,198.4 L 177.0,198.4 L 176.1,198.4 L 175.1,198.3 L 174.2,198.3 L 173.3,198.3 L 172.4,198.3 L 171.5,198.3 L 170.6,198.2 L 169.7,198.2 L 168.8,198.2 L 167.9,198.2 L 167.0,198.1 L 166.1,198.1 L 165.2,198.1 L 164.3,198.0 L 163.4,198.0 L 162.5,197.9 L 161.6,197.9 L 160.7,197.9 L 159.8,197.8 L 158.9,197.8 L 158.0,197.7 L 157.1,197.7 L 156.2,197.6 L 155.3,197.5 L 154.4,197.5 L 153.5,197.4 L 152.6,197.3 L 151.7,197.3 L 150.8,197.2 L 149.9,197.1 L 149.0,197.0 L 148.1,196.9 L 147.2,196.9 L 146.3,196.8 L 145.4,196.7 L 144.5,196.6 L 143.6,196.5 L 142.7,196.4 L 141.8,196.2 L 140.9,196.1 L 140.0,196.0 L 139.1,195.9 L 138.2,195.8 L 137.3,195.6 L 136.4,195.5 L 135.5,195.3 L 134.6,195.2 L 133.6,195.0 L 132.7,194.9 L 131.8,194.7 L 130.9,194.6 L 130.0,194.4 L 129.1,194.2 L 128.2,194.0 L 127.3,193.8 L 126.4,193.6 L 125.5,193.4 L 124.6,193.2 L 123.7,193.0 L 122.8,192.8 L 121.9,192.5 L 121.0,192.3 L 120.1,192.1 L 119.2,191.8 L 118.3,191.6 L 117.4,191.3 L 116.5,191.0 L 115.6,190.7 L 114.7,190.4 L 113.8,190.1 L 112.9,189.8 L 112.0,189.5 L 111.1,189.2 L 110.2,188.8 L 109.3,188.5 L 108.4,188.1 L 107.5,187.7 L 106.6,187.3 L 105.7,186.9 L 104.8,186.5 L 103.9,186.0 L 103.0,185.6 L 102.1,185.1 L 101.2,184.6 L 100.3,184.1 L 99.4,183.6 L 98.5,183.1 L 97.6,182.5 L 96.7,181.9 L 95.8,181.3 L 94.9,180.6 L 94.0,180.0 L 93.1,179.2 L 92.1,178.5 L 91.2,177.7 L 90.3,176.9 L 89.4,176.0 L 88.5,175.0 L 87.6,174.0 L 86.7,172.8 L 85.8,171.6 L 84.9,170.2 L 84.0,168.6 L 83.1,166.7 L 82.2,164.2 L 81.3,158.0 L 81.3,158.0 L 82.2,151.8 L 83.1,149.3 L 84.0,147.4 L 84.9,145.8 L 85.8,144.4 L 86.7,143.2 L 87.6,142.0 L 88.5,141.0 L 89.4,140.0 L 90.3,139.1 L 91.2,138.3 L 92.1,137.5 L 93.1,136.8 L 94.0,136.0 L 94.9,135.4 L 95.8,134.7 L 96.7,134.1 L 97.6,133.5 L 98.5,132.9 L 99.4,132.4 L 100.3,131.9 L 101.2,131.4 L 102.1,130.9 L 103.0,130.4 L 103.9,130.0 L 104.8,129.5 L 105.7,129.1 L 106.6,128.7 L 107.5,128.3 L 108.4,127.9 L 109.3,127.5 L 110.2,127.2 L 111.1,126.8 L 112.0,126.5 L 112.9,126.2 L 113.8,125.9 L 114.7,125.6 L 115.6,125.3 L 116.5,125.0 L 117.4,124.7 L 118.3,124.4 L 119.2,124.2 L 120.1,123.9 L 121.0,123.7 L 121.9,123.5 L 122.8,123.2 L 123.7,123.0 L 124.6,122.8 L 125.5,122.6 L 126.4,122.4 L 127.3,122.2 L 128.2,122.0 L 129.1,121.8 L 130.0,121.6 L 130.9,121.4 L 131.8,121.3 L 132.7,121.1 L 133.6,121.0 L 134.6,120.8 L 135.5,120.7 L 136.4,120.5 L 137.3,120.4 L 138.2,120.2 L 139.1,120.1 L 140.0,120.0 L 140.9,119.9 L 141.8,119.8 L 142.7,119.6 L 143.6,119.5 L 144.5,119.4 L 145.4,119.3 L 146.3,119.2 L 147.2,119.1 L 148.1,119.1 L 149.0,119.0 L 149.9,118.9 L 150.8,118.8 L 151.7,118.7 L 152.6,118.7 L 153.5,118.6 L 154.4,118.5 L 155.3,118.5 L 156.2,118.4 L 157.1,118.3 L 158.0,118.3 L 158.9,118.2 L 159.8,118.2 L 160.7,118.1 L 161.6,118.1 L 162.5,118.1 L 163.4,118.0 L 164.3,118.0 L 165.2,117.9 L 166.1,117.9 L 167.0,117.9 L 167.9,117.8 L 168.8,117.8 L 169.7,117.8 L 170.6,117.8 L 171.5,117.7 L 172.4,117.7 L 173.3,117.7 L 174.2,117.7 L 175.1,117.7 L 176.1,117.6 L 177.0,117.6 L 177.9,117.6 L 178.8,117.6 L 179.7,117.6 L 180.6,117.6 L 181.5,117.6 L 182.4,117.6 L 183.3,117.6 L 184.2,117.6 L 185.1,117.6 L 186.0,117.6 L 186.9,117.5 L 187.8,117.5 L 188.7,117.5 L 189.6,117.5 L 190.5,117.5 L 191.4,117.5 L 192.3,117.5 L 193.2,117.5 L 194.1,117.5 L 195.0,117.5 L 195.9,117.5 L 196.8,117.5 L 197.7,117.5 L 198.6,117.5 L 199.5,117.5 L 200.4,117.5 L 201.3,117.5 L 202.2,117.5 L 203.1,117.5 L 204.0,117.5 L 204.9,117.5 L 205.8,117.5 L 206.7,117.5 L 207.6,117.5 L 208.5,117.5 L 209.4,117.5 L 210.3,117.5 L 211.2,117.5 L 212.1,117.5 L 213.0,117.5 L 213.9,117.5 L 214.8,117.5 L 215.7,117.4 L 216.6,117.4 L 217.6,117.4 L 218.5,117.4 L 219.4,117.4 L 220.3,117.4 L 221.2,117.3 L 222.1,117.3 L 223.0,117.3 L 223.9,117.3 L 224.8,117.2 L 225.7,117.2 L 226.6,117.2 L 227.5,117.1 L 228.4,117.1 L 229.3,117.1 L 230.2,117.0 L 231.1,117.0 L 232.0,116.9 L 232.9,116.9 L 233.8,116.8 L 234.7,116.8 L 235.6,116.7 L 236.5,116.7 L 237.4,116.6 L 238.3,116.6 L 239.2,116.5 L 240.1,116.4 L 241.0,116.4 L 241.9,116.3 L 242.8,116.2 L 243.7,116.2 L 244.6,116.1 L 245.5,116.0 L 246.4,115.9 L 247.3,115.8 L 248.2,115.7 L 249.1,115.6 L 250.0,115.5 L 250.9,115.4 L 251.8,115.3 L 252.7,115.2 L 253.6,115.1 L 254.5,115.0 L 255.4,114.9 L 256.3,114.8 L 257.2,114.6 L 258.1,114.5 L 259.1,114.4 L 260.0,114.3 L 260.9,114.1 L 261.8,114.0 L 262.7,113.8 L 263.6,113.7 L 264.5,113.5 L 265.4,113.4 L 266.3,113.2 L 267.2,113.1 L 268.1,112.9 L 269.0,112.7 L 269.9,112.6 L 270.8,112.4 L 271.7,112.2 L 272.6,112.0 L 273.5,111.8 L 274.4,111.7 L 275.3,111.5 L 276.2,111.3 L 277.1,111.1 L 278.0,110.9 L 278.9,110.7 L 279.8,110.4 L 280.7,110.2 L 281.6,110.0 L 282.5,109.8 L 283.4,109.6 L 284.3,109.3 L 285.2,109.1 L 286.1,108.9 L 287.0,108.6 L 287.9,108.4 L 288.8,108.1 L 289.7,107.9 L 290.6,107.6 L 291.5,107.4 L 292.4,107.1 L 293.3,106.8 L 294.2,106.6 L 295.1,106.3 L 296.0,106.0 L 296.9,105.7 L 297.8,105.5 L 298.7,105.2 L 299.6,104.9 L 300.6,104.6 L 301.5,104.3 L 302.4,104.0 L 303.3,103.7 L 304.2,103.4 L 305.1,103.1 L 306.0,102.8 L 306.9,102.4 L 307.8,102.1 L 308.7,101.8 L 309.6,101.5 L 310.5,101.1 L 311.4,100.8 L 312.3,100.5 L 313.2,100.1 L 314.1,99.8 L 315.0,99.4 L 315.9,99.1 L 316.8,98.7 L 317.7,98.4 L 318.6,98.0 L 319.5,97.6 L 320.4,97.3 L 321.3,96.9 L 322.2,96.5 L 323.1,96.1 L 324.0,95.8 L 324.9,95.4 L 325.8,95.0 L 326.7,94.6 L 327.6,94.2 L 328.5,93.8 L 329.4,93.4 L 330.3,93.0 L 331.2,92.6 L 332.1,92.2 L 333.0,91.8 L 333.9,91.4 L 334.8,91.0 L 335.7,90.6 L 336.6,90.1 L 337.5,89.7 L 338.4,89.3 L 339.3,88.9 L 340.2,88.4 L 341.1,88.0 L 342.1,87.6 L 343.0,87.1 L 343.9,86.7 L 344.8,86.2 L 345.7,85.8 L 346.6,85.3 L 347.5,84.9 L 348.4,84.4 L 349.3,84.0 L 350.2,83.5 L 351.1,83.1 L 352.0,82.6 L 352.9,82.1 L 353.8,81.6 L 354.7,81.2 L 355.6,80.7 L 356.5,80.2 L 357.4,79.7 L 358.3,79.3 L 359.2,78.8 L 360.1,78.3 L 361.0,77.8 L 361.9,77.3 L 362.8,76.8 L 363.7,76.3 L 364.6,75.8 L 365.5,75.3 L 366.4,74.8 L 367.3,74.3 L 368.2,73.8 L 369.1,73.3 L 370.0,72.8 L 370.9,72.2 L 371.8,71.7 L 372.7,71.2 L 373.6,70.7 L 374.5,70.2 L 375.4,69.6 L 376.3,69.1 L 377.2,68.6 L 378.1,68.0 L 379.0,67.5 L 379.9,67.0 L 380.8,66.4 L 381.7,65.9 L 382.6,65.3 L 383.6,64.8 L 384.5,64.2 L 385.4,63.7 L 386.3,63.1 L 387.2,62.6 L 388.1,62.0 L 389.0,61.5 L 389.9,60.9 L 390.8,60.4 L 391.7,59.8 L 392.6,59.2 L 393.5,58.7 L 394.4,58.1 L 395.3,57.5 L 396.2,56.9 L 397.1,56.4 L 398.0,55.8 L 398.9,55.2 L 399.8,54.6 L 400.7,54.0 L 401.6,53.5 L 402.5,52.9 L 403.4,52.3 L 404.3,51.7 L 405.2,51.1 L 406.1,50.5 L 407.0,49.9 L 407.9,49.3 L 408.8,48.7 L 409.7,48.1 L 410.6,47.5 L 411.5,46.9 L 412.4,46.3 L 413.3,45.7 L 414.2,45.1 L 415.1,44.5 L 416.0,43.8 L 416.9,43.2 L 417.8,42.6 L 418.7,42.0 L 419.6,41.4 L 420.5,40.7 L 421.4,40.1 L 422.3,39.5 L 423.2,38.9 L 424.1,38.2 L 425.1,37.6 L 426.0,37.0 L 426.9,36.3 L 427.8,35.7 L 428.7,35.1 L 429.6,34.4 L 430.5,33.8 L 431.4,33.1 L 432.3,32.5 L 433.2,31.9 L 434.1,31.2 L 435.0,30.6 L 435.9,29.9 L 436.8,29.3 L 437.7,28.6" fill="none" stroke="currentColor" stroke-width="2" opacity="0.8"/> <!-- the chord through P and Q --> <line x1="52.0" y1="192.6" x2="443.0" y2="37.2" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.7"/> <!-- the reflection, R up to P+Q --> <line x1="90.7" y1="177.2" x2="90.7" y2="138.8" stroke="currentColor" stroke-width="2" opacity="0.5" stroke-dasharray="3 3"/> <polygon points="90.7,137.8 86.7,145.8 94.7,145.8" fill="currentColor" opacity="0.6"/> <text x="99.7" y="154.0" font-size="10" fill="currentColor" opacity="0.65">reflect</text> <circle cx="244.5" cy="116.1" r="4.5" fill="currentColor"/> <text x="252.5" y="120.1" font-size="13" font-weight="bold" fill="currentColor">P</text> <circle cx="400.9" cy="53.9" r="4.5" fill="currentColor"/> <text x="384.9" y="57.9" font-size="13" font-weight="bold" fill="currentColor">Q</text> <circle cx="90.7" cy="177.2" r="4.5" fill="currentColor"/> <text x="73.7" y="182.2" font-size="13" font-weight="bold" fill="currentColor">R</text> <circle cx="90.7" cy="138.8" r="4.5" fill="currentColor"/> <text x="50.7" y="143.8" font-size="13" font-weight="bold" fill="currentColor">P+Q</text> </svg>

    *P and Q are the two points being added. The dashed chord through them meets the curve a third time at R. Reflecting R across the horizontal axis gives P + Q. Note that neither P nor Q moves — only R is reflected.*

    That's the **chord** construction. When you add a point to *itself* there's
    no second point to draw a line through, so you use the **tangent** at that
    point instead — and the rest is the same. Hence "chord and tangent".

    The reflection in step 3 looks arbitrary and isn't: it's what makes the
    operation behave like addition, so that adding points is associative and
    every point has an inverse. Without it the structure doesn't work.

    Over a finite field the **same algebraic formulas** apply, and they still
    produce a valid third point. There's simply no line to draw any more. The
    arithmetic survives the move; the picture doesn't.

## Deriving a public key

The curve comes with one fixed, published point called the **generator**, written **G**. Everyone uses the same one — it's part of the standard, not something you choose:

```
G.x = 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798
G.y = 483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8
```

Those two numbers are in the specification [(SECG, 2010)](#ref-secg-2010) and have been identical for every Ethereum and Bitcoin key ever made. Keep them in view — the tool below lets you check them.

Your public key is then:

```
public key = private key × G
```

That's it. Take G, add it to itself as many times as your private key says, and **the point you land on is your public key.** Since a private key is around 10⁷⁷, "as many times as your private key says" isn't something anyone does literally — see the box further down.

Worth being clear about what you end up with, because it catches people out:

> **The public key is a point.** Not a string, not a hash — a pair of coordinates, *x* and *y*, each a 32-byte number. Any hex string you see called "a public key" is just one of several ways of writing that pair down.

So the whole derivation is two steps and no more:

```
a number you chose          ──×G──►      a point on the curve
   (private key)                            (public key)
```

??? example "Try it: private key to public key"

    <div class="tool" markdown="0">
      <label for="pub-priv">Private key (hex)</label>
      <input id="pub-priv" type="text" autocomplete="off" spellcheck="false" value="1">
      <button id="pub-rand" type="button">Random key</button>
      <p class="tool__out" id="pub-out"></p>
    </div>

    The two coordinates at the top **are** the public key. The byte strings
    below them are the same point written in the different formats explained
    later on this page — not extra things, just other spellings.

    Work through it in this order; each step shows something different.

    **Step 1 — check the tool is honest.** The field starts at `1`, so it's
    computing 1 × G, which should be G itself. Compare the x and y it gives
    you against the two values printed above. They match, which means
    everything below is trustworthy.

    **Step 2 — type `2`.** That's G + G. Notice the coordinates have nothing
    in common with G's. Not larger, not similar — unrelated.

    **Step 3 — type `3`, then `4`, then `5`.** Watch the x coordinate as you
    go. There's no drift, no pattern, no sense in which 5 is "further along"
    than 4. **This scattering is the entire security of the scheme**, and
    it's the thing to take away from this page.

    **Step 4 — press Random key**, a few times. This is what a wallet
    actually does when it makes you an account.

    **Step 5 — try to break it.** Enter `0`, or `ffffffff...` (64 f's, which
    is above the curve order). Both are rejected, for the reason given on the
    [private keys](private-keys.md) page.

## Why it can't be reversed

Going forwards is fast. Going backwards — given a public key, find the private key — is the **discrete logarithm problem**, and nobody has a practical method.

The reason is the same one that makes [Keccak-256](keccak256.md) one-way, and it's worth noticing the parallel: **the output gives you nothing to follow.**

Try the tool with 1, then 2, then 3. The coordinates jump about with no pattern. They don't increase. "Close to the right answer" doesn't exist, because a private key one away from yours produces a point bearing no resemblance to yours. So there's no gradient to climb, no way to narrow the search, nothing to do but guess — and [guessing is hopeless](private-keys.md) at this scale.

??? abstract "Then how is the forward direction fast?"

    A fair question, since adding G to itself 10⁷⁷ times is obviously not
    happening.

    The trick is **doubling**. Rather than stepping one G at a time, you
    repeatedly double — G, 2G, 4G, 8G, 16G — and add together whichever of
    those you need. Any number up to 2²⁵⁶ is the sum of at most 256 such
    powers, which is exactly what its binary representation tells you.

    So the whole computation is around 256 doublings and at most 256
    additions, and it finishes in well under a millisecond. The tool above is
    doing it in your browser.

    The asymmetry is the entire point: **about 256 operations forwards, no
    known shortcut backwards.** Multiplying is cheap; dividing is not
    available.

## The several written forms

A public key is a pair of coordinates, each 32 bytes, so 64 bytes in total. But you'll meet it written several ways, which is a common source of confusion:

| Form | Size | What it looks like |
| --- | --- | --- |
| **Raw** | 64 bytes | `x` then `y` |
| **Uncompressed** | 65 bytes | `0x04` then `x` then `y` |
| **Compressed** | 33 bytes | `0x02` or `0x03` then `x` |

The `0x04` prefix in the second form is a marker meaning "uncompressed point follows". It is **not** part of the key, and this trips people up constantly — see the note below.

**Compressed** form drops `y` entirely, which works because the curve equation nearly determines it. Given `x`, the equation `y² = x³ + 7` has exactly two solutions, and they always have opposite parity — one even, one odd. So a single byte recording which one it was (`02` for even, `03` for odd) is enough to recompute `y`. Half the size, no information lost.

??? warning "Ethereum hashes the 64-byte form, with no prefix"

    When deriving an [address](addresses.md), Ethereum hashes the **raw 64
    bytes** — `x` followed by `y`, and *no* `0x04` prefix.

    The Yellow Paper is explicit about this — address derivation takes the
    64-byte representation [(Wood, 2014)](#ref-wood-2014).

    Include the prefix and you hash 65 bytes instead of 64, which by the
    avalanche property gives you a completely unrelated hash, and therefore a
    completely wrong address. Nothing errors; you just get an address that
    isn't yours.

    This is probably the single most common mistake when implementing address
    derivation by hand.

## Why this curve?

The name decodes piece by piece: **sec** for the standards group that published it, **p** because the field is a prime one, **256** for the size in bits, **k** for Koblitz, and **1** because it's the first curve of that kind in the list [(SECG, 2010)](#ref-secg-2010).

Bitcoin chose it, and Ethereum followed — which brought along a decade of implementations, review and hardware support.

??? info "History: who Koblitz was, and what a Koblitz curve is"

    **Koblitz** is a person. Neal Koblitz was one of two mathematicians who,
    working independently in the mid-1980s, proposed using elliptic curves for
    cryptography — the other was Victor Miller. Until then elliptic curves
    were a subject in pure number theory with no particular connection to
    keeping secrets.

    A **Koblitz curve** is one whose constants are chosen to have deliberate
    structure rather than being picked arbitrarily, because structure makes
    the arithmetic faster.

    You can see it in secp256k1's own numbers. The equation is `y² = x³ + 7`,
    with no *x* term at all and a tiny constant, and the field prime sits just
    below a power of two:

    ```
    p = 2²⁵⁶ − 2³² − 977
    ```

    Both choices speed up the computation. But they have a second property
    that turned out to matter more: **they're plainly visible.** Anyone can see
    why each constant is what it is, because there's nothing to see — a 7, and
    a prime chosen to sit near a round binary number.

    That becomes the interesting part when you compare it with the
    alternative, which is the next box.

??? question "There was another candidate, and the choice is interesting"

    The obvious alternative was **secp256r1**, where `r` stands for random.
    It's the curve NIST recommends and most of the wider internet uses.

    The two were generated differently. secp256k1's parameters are
    structurally derived — a Koblitz curve, with the small constant 7 and a
    prime close to a power of two, chosen because they make the arithmetic
    fast and the choices visible. secp256r1's parameters come from hashing an
    unexplained seed value, and nobody has said where that seed came from.

    There is no published attack on secp256r1, and this is not evidence of
    one. But "we can see exactly why every constant is what it is" is a
    property cryptographers value for its own sake, and it's part of why the
    k1 curve was attractive for a system meant to need no trusted authority.

## Why have both a public key and an address?

A reasonable question, since the address is just a hash of the public key and carries no extra information. Why not use the public key directly as the thing people send to?

Because the two do **different jobs.**

**The public key does the cryptography.** It's the mathematical object that signature verification needs: checking a signature means checking it against a public key, and there's no way round that.

**The address does the naming.** It's what goes in a transaction's recipient field, gets stored in contracts, is typed into wallets and read down the phone. For that job the public key is a poor choice, for one blunt reason:

| | Size |
| --- | --- |
| Public key | 64 bytes — 128 hex characters |
| Address | 20 bytes — 40 hex characters |

An address is less than a third the size. It appears in every transaction, in storage, in logs, in every interface — so that saving is paid out constantly, in storage costs, bandwidth and human effort.

And here's the part that makes it work: **you don't need to publish the public key separately.** A [signature](signatures.md) lets anyone recover the public key that produced it. So the public key is available exactly when verification needs it, and need never be stored or sent on its own.

So: short identifier for naming, full key recovered on demand for the maths. The hash in between costs nothing and, as the box at the end of this section explains, happens to buy a little extra protection too.

## When your public key becomes visible

Which leads to a detail worth knowing, because it isn't obvious.

Receiving ether reveals nothing. People send to your **[address](addresses.md)** — and a hash can't be reversed, so an unused account exposes only the address.

Your public key becomes known the first time you **sign** something. A [signature](signatures.md) lets anyone recover the public key that produced it; that's how verification works at all. So the moment you send your first transaction, your public key is on the chain for good.

This doesn't put anything at risk today. The public key is meant to be public, and the private key stays unreachable behind the discrete logarithm problem.

So why mention it at all? Because it's a second lock, and it only matters if the first one ever fails.

??? note "When the distinction would actually matter"

    Everything on this page rests on the discrete logarithm problem being
    hard. Suppose one day it isn't — because someone finds a flaw in the
    curve, or because a sufficiently large quantum computer is eventually
    built. Shor's algorithm, published in 1994, would solve discrete
    logarithms efficiently on such a machine.

    **Machines capable of this do not exist**, and when or whether they will
    is genuinely unknown. Treat any confident timeline with suspicion.

    But note the asymmetry if it ever happened:

    - An account that **has** transacted has published its public key. Anyone
      who could break the curve could compute its private key.
    - An account that has **never** transacted has published only its
      [address](addresses.md) — a Keccak hash. Breaking the curve wouldn't
      help, because you'd first have to reverse the hash to get the public
      key, and hashes resist quantum attack far better than curves do.

    So untouched accounts sit behind two different kinds of problem rather
    than one. That's the entire practical content of "your public key is
    secret until you sign".

    **And it's where the old advice against reusing addresses came from.**
    Once you've spent from an address, its public key is published for good.
    Anything you send to that same address afterwards sits behind the curve
    alone — the hash layer is spent. Use a fresh address for each receipt and
    every balance keeps both layers until the moment you spend it.

    Bitcoin wallets do this automatically, generating a new address for every
    payment. **Ethereum does the opposite**: address reuse is universal, and
    deliberately so, because contracts, token balances and ENS names all need
    an address that stays put. A stable identifier is worth more in practice
    than a speculative hedge against a machine that doesn't exist.

    That's a real trade-off Ethereum has chosen, not an oversight. Worth
    knowing it was chosen — and it's one instance of a larger pattern, since
    the same persistence that makes an address worth reusing is what makes it
    worth watching. [Why accounts, and what they
    cost](../accounts/why-accounts.md) takes that apart.

---

## Recap

- A public key is a **point on the secp256k1 curve**: two coordinates, 32 bytes each.
- It's computed as **private key × G**, where G is a fixed published point everyone shares.
- Forwards takes about **256 doublings**; backwards is the discrete logarithm problem, with no known shortcut.
- It's one-way for the same reason hashing is: **the output offers nothing to follow.** Neighbouring private keys give unrelated points.
- Three written forms — raw (64 bytes), uncompressed with an `0x04` prefix (65), compressed (33).
- **Ethereum hashes the raw 64 bytes.** Including the prefix silently produces the wrong address.

**Next:** [Addresses](addresses.md) — the last step, and the one that finally produces something you'd paste into a wallet.

---

## References

<div class="sources" markdown>

- <a id="ref-secg-2010"></a>**Standards for Efficient Cryptography Group** (2010). *SEC 1: Elliptic Curve Cryptography* and *SEC 2: Recommended Elliptic Curve Domain Parameters*, version 2.0. SEC 1 defines the point encodings used above; SEC 2 defines secp256k1 itself, including the generator G and the field prime. <https://www.secg.org/sec2-v2.pdf>
- <a id="ref-wood-2014"></a>**Wood, G.** (2014). *Ethereum: A secure decentralised generalised transaction ledger.* Ethereum project yellow paper. Appendix F specifies the use of secp256k1 and the 64-byte public key form for address derivation. <https://ethereum.github.io/yellowpaper/paper.pdf>

</div>
