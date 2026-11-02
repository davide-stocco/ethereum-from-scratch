---
tier: 1
description: A public key is a point on a curve, computed from a private key by a step that is easy forwards and infeasible backwards.
---

# Public keys

**Fork-proof.** secp256k1 has been Ethereum's curve since genesis.

A [private key](private-keys.md) is a number you keep. A **public key** is what you get by running that number through a one-way calculation, and it's safe to publish.

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

<figure markdown="span">
<svg viewBox="0 0 420 260" role="img" aria-label="The curve y squared equals x cubed plus 7 drawn over the real numbers, a smooth continuous shape" style="width:100%;max-width:26rem;height:auto">
  <g stroke="currentColor" stroke-width="1" opacity="0.25">
    <line x1="35" y1="127.5" x2="405" y2="127.5"/>
    <line x1="183.0" y1="15" x2="183.0" y2="235"/>
  </g>
  <path d="M 404.4,228.6 L 403.4,228.0 L 402.4,227.4 L 401.4,226.8 L 400.4,226.1 L 399.4,225.5 L 398.4,224.9 L 397.5,224.3 L 396.5,223.7 L 395.5,223.1 L 394.5,222.4 L 393.5,221.8 L 392.5,221.2 L 391.5,220.6 L 390.5,220.0 L 389.6,219.4 L 388.6,218.8 L 387.6,218.2 L 386.6,217.6 L 385.6,217.0 L 384.6,216.4 L 383.6,215.8 L 382.7,215.2 L 381.7,214.7 L 380.7,214.1 L 379.7,213.5 L 378.7,212.9 L 377.7,212.3 L 376.7,211.8 L 375.7,211.2 L 374.8,210.6 L 373.8,210.0 L 372.8,209.5 L 371.8,208.9 L 370.8,208.3 L 369.8,207.8 L 368.8,207.2 L 367.9,206.6 L 366.9,206.1 L 365.9,205.5 L 364.9,205.0 L 363.9,204.4 L 362.9,203.9 L 361.9,203.3 L 360.9,202.8 L 360.0,202.2 L 359.0,201.7 L 358.0,201.1 L 357.0,200.6 L 356.0,200.1 L 355.0,199.5 L 354.0,199.0 L 353.1,198.5 L 352.1,198.0 L 351.1,197.4 L 350.1,196.9 L 349.1,196.4 L 348.1,195.9 L 347.1,195.4 L 346.1,194.8 L 345.2,194.3 L 344.2,193.8 L 343.2,193.3 L 342.2,192.8 L 341.2,192.3 L 340.2,191.8 L 339.2,191.3 L 338.3,190.8 L 337.3,190.3 L 336.3,189.8 L 335.3,189.4 L 334.3,188.9 L 333.3,188.4 L 332.3,187.9 L 331.3,187.4 L 330.4,187.0 L 329.4,186.5 L 328.4,186.0 L 327.4,185.6 L 326.4,185.1 L 325.4,184.6 L 324.4,184.2 L 323.5,183.7 L 322.5,183.3 L 321.5,182.8 L 320.5,182.4 L 319.5,181.9 L 318.5,181.5 L 317.5,181.0 L 316.5,180.6 L 315.6,180.2 L 314.6,179.7 L 313.6,179.3 L 312.6,178.9 L 311.6,178.5 L 310.6,178.0 L 309.6,177.6 L 308.7,177.2 L 307.7,176.8 L 306.7,176.4 L 305.7,176.0 L 304.7,175.6 L 303.7,175.2 L 302.7,174.8 L 301.7,174.4 L 300.8,174.0 L 299.8,173.6 L 298.8,173.3 L 297.8,172.9 L 296.8,172.5 L 295.8,172.1 L 294.8,171.8 L 293.9,171.4 L 292.9,171.0 L 291.9,170.7 L 290.9,170.3 L 289.9,170.0 L 288.9,169.6 L 287.9,169.3 L 286.9,169.0 L 286.0,168.6 L 285.0,168.3 L 284.0,168.0 L 283.0,167.6 L 282.0,167.3 L 281.0,167.0 L 280.0,166.7 L 279.1,166.4 L 278.1,166.1 L 277.1,165.8 L 276.1,165.5 L 275.1,165.2 L 274.1,164.9 L 273.1,164.6 L 272.1,164.3 L 271.2,164.0 L 270.2,163.8 L 269.2,163.5 L 268.2,163.2 L 267.2,163.0 L 266.2,162.7 L 265.2,162.5 L 264.3,162.2 L 263.3,162.0 L 262.3,161.7 L 261.3,161.5 L 260.3,161.3 L 259.3,161.0 L 258.3,160.8 L 257.3,160.6 L 256.4,160.4 L 255.4,160.2 L 254.4,160.0 L 253.4,159.8 L 252.4,159.6 L 251.4,159.4 L 250.4,159.2 L 249.5,159.0 L 248.5,158.8 L 247.5,158.6 L 246.5,158.5 L 245.5,158.3 L 244.5,158.1 L 243.5,158.0 L 242.5,157.8 L 241.6,157.7 L 240.6,157.5 L 239.6,157.4 L 238.6,157.3 L 237.6,157.1 L 236.6,157.0 L 235.6,156.9 L 234.7,156.8 L 233.7,156.6 L 232.7,156.5 L 231.7,156.4 L 230.7,156.3 L 229.7,156.2 L 228.7,156.1 L 227.7,156.0 L 226.8,155.9 L 225.8,155.9 L 224.8,155.8 L 223.8,155.7 L 222.8,155.6 L 221.8,155.5 L 220.8,155.5 L 219.9,155.4 L 218.9,155.4 L 217.9,155.3 L 216.9,155.2 L 215.9,155.2 L 214.9,155.1 L 213.9,155.1 L 212.9,155.0 L 212.0,155.0 L 211.0,155.0 L 210.0,154.9 L 209.0,154.9 L 208.0,154.9 L 207.0,154.8 L 206.0,154.8 L 205.1,154.8 L 204.1,154.8 L 203.1,154.7 L 202.1,154.7 L 201.1,154.7 L 200.1,154.7 L 199.1,154.7 L 198.1,154.7 L 197.2,154.7 L 196.2,154.7 L 195.2,154.6 L 194.2,154.6 L 193.2,154.6 L 192.2,154.6 L 191.2,154.6 L 190.3,154.6 L 189.3,154.6 L 188.3,154.6 L 187.3,154.6 L 186.3,154.6 L 185.3,154.6 L 184.3,154.6 L 183.3,154.6 L 182.4,154.6 L 181.4,154.6 L 180.4,154.6 L 179.4,154.6 L 178.4,154.6 L 177.4,154.6 L 176.4,154.6 L 175.5,154.6 L 174.5,154.6 L 173.5,154.6 L 172.5,154.6 L 171.5,154.6 L 170.5,154.6 L 169.5,154.6 L 168.5,154.6 L 167.6,154.6 L 166.6,154.5 L 165.6,154.5 L 164.6,154.5 L 163.6,154.5 L 162.6,154.5 L 161.6,154.5 L 160.7,154.4 L 159.7,154.4 L 158.7,154.4 L 157.7,154.4 L 156.7,154.3 L 155.7,154.3 L 154.7,154.3 L 153.7,154.2 L 152.8,154.2 L 151.8,154.1 L 150.8,154.1 L 149.8,154.0 L 148.8,154.0 L 147.8,153.9 L 146.8,153.8 L 145.9,153.8 L 144.9,153.7 L 143.9,153.6 L 142.9,153.6 L 141.9,153.5 L 140.9,153.4 L 139.9,153.3 L 138.9,153.2 L 138.0,153.1 L 137.0,153.0 L 136.0,152.9 L 135.0,152.8 L 134.0,152.7 L 133.0,152.5 L 132.0,152.4 L 131.1,152.3 L 130.1,152.1 L 129.1,152.0 L 128.1,151.8 L 127.1,151.6 L 126.1,151.5 L 125.1,151.3 L 124.1,151.1 L 123.2,150.9 L 122.2,150.7 L 121.2,150.5 L 120.2,150.3 L 119.2,150.0 L 118.2,149.8 L 117.2,149.6 L 116.3,149.3 L 115.3,149.0 L 114.3,148.7 L 113.3,148.5 L 112.3,148.1 L 111.3,147.8 L 110.3,147.5 L 109.3,147.1 L 108.4,146.8 L 107.4,146.4 L 106.4,146.0 L 105.4,145.6 L 104.4,145.1 L 103.4,144.7 L 102.4,144.2 L 101.5,143.7 L 100.5,143.1 L 99.5,142.5 L 98.5,141.9 L 97.5,141.2 L 96.5,140.5 L 95.5,139.7 L 94.5,138.9 L 93.6,138.0 L 92.6,136.9 L 91.6,135.7 L 90.6,134.2 L 89.6,132.3 L 88.6,127.5 L 88.6,127.5 L 89.6,122.7 L 90.6,120.8 L 91.6,119.3 L 92.6,118.1 L 93.6,117.0 L 94.5,116.1 L 95.5,115.3 L 96.5,114.5 L 97.5,113.8 L 98.5,113.1 L 99.5,112.5 L 100.5,111.9 L 101.5,111.3 L 102.4,110.8 L 103.4,110.3 L 104.4,109.9 L 105.4,109.4 L 106.4,109.0 L 107.4,108.6 L 108.4,108.2 L 109.3,107.9 L 110.3,107.5 L 111.3,107.2 L 112.3,106.9 L 113.3,106.5 L 114.3,106.3 L 115.3,106.0 L 116.3,105.7 L 117.2,105.4 L 118.2,105.2 L 119.2,105.0 L 120.2,104.7 L 121.2,104.5 L 122.2,104.3 L 123.2,104.1 L 124.1,103.9 L 125.1,103.7 L 126.1,103.5 L 127.1,103.4 L 128.1,103.2 L 129.1,103.0 L 130.1,102.9 L 131.1,102.7 L 132.0,102.6 L 133.0,102.5 L 134.0,102.3 L 135.0,102.2 L 136.0,102.1 L 137.0,102.0 L 138.0,101.9 L 138.9,101.8 L 139.9,101.7 L 140.9,101.6 L 141.9,101.5 L 142.9,101.4 L 143.9,101.4 L 144.9,101.3 L 145.9,101.2 L 146.8,101.2 L 147.8,101.1 L 148.8,101.0 L 149.8,101.0 L 150.8,100.9 L 151.8,100.9 L 152.8,100.8 L 153.7,100.8 L 154.7,100.7 L 155.7,100.7 L 156.7,100.7 L 157.7,100.6 L 158.7,100.6 L 159.7,100.6 L 160.7,100.6 L 161.6,100.5 L 162.6,100.5 L 163.6,100.5 L 164.6,100.5 L 165.6,100.5 L 166.6,100.5 L 167.6,100.4 L 168.5,100.4 L 169.5,100.4 L 170.5,100.4 L 171.5,100.4 L 172.5,100.4 L 173.5,100.4 L 174.5,100.4 L 175.5,100.4 L 176.4,100.4 L 177.4,100.4 L 178.4,100.4 L 179.4,100.4 L 180.4,100.4 L 181.4,100.4 L 182.4,100.4 L 183.3,100.4 L 184.3,100.4 L 185.3,100.4 L 186.3,100.4 L 187.3,100.4 L 188.3,100.4 L 189.3,100.4 L 190.3,100.4 L 191.2,100.4 L 192.2,100.4 L 193.2,100.4 L 194.2,100.4 L 195.2,100.4 L 196.2,100.3 L 197.2,100.3 L 198.1,100.3 L 199.1,100.3 L 200.1,100.3 L 201.1,100.3 L 202.1,100.3 L 203.1,100.3 L 204.1,100.2 L 205.1,100.2 L 206.0,100.2 L 207.0,100.2 L 208.0,100.1 L 209.0,100.1 L 210.0,100.1 L 211.0,100.0 L 212.0,100.0 L 212.9,100.0 L 213.9,99.9 L 214.9,99.9 L 215.9,99.8 L 216.9,99.8 L 217.9,99.7 L 218.9,99.6 L 219.9,99.6 L 220.8,99.5 L 221.8,99.5 L 222.8,99.4 L 223.8,99.3 L 224.8,99.2 L 225.8,99.1 L 226.8,99.1 L 227.7,99.0 L 228.7,98.9 L 229.7,98.8 L 230.7,98.7 L 231.7,98.6 L 232.7,98.5 L 233.7,98.4 L 234.7,98.2 L 235.6,98.1 L 236.6,98.0 L 237.6,97.9 L 238.6,97.7 L 239.6,97.6 L 240.6,97.5 L 241.6,97.3 L 242.5,97.2 L 243.5,97.0 L 244.5,96.9 L 245.5,96.7 L 246.5,96.5 L 247.5,96.4 L 248.5,96.2 L 249.5,96.0 L 250.4,95.8 L 251.4,95.6 L 252.4,95.4 L 253.4,95.2 L 254.4,95.0 L 255.4,94.8 L 256.4,94.6 L 257.3,94.4 L 258.3,94.2 L 259.3,94.0 L 260.3,93.7 L 261.3,93.5 L 262.3,93.3 L 263.3,93.0 L 264.3,92.8 L 265.2,92.5 L 266.2,92.3 L 267.2,92.0 L 268.2,91.8 L 269.2,91.5 L 270.2,91.2 L 271.2,91.0 L 272.1,90.7 L 273.1,90.4 L 274.1,90.1 L 275.1,89.8 L 276.1,89.5 L 277.1,89.2 L 278.1,88.9 L 279.1,88.6 L 280.0,88.3 L 281.0,88.0 L 282.0,87.7 L 283.0,87.4 L 284.0,87.0 L 285.0,86.7 L 286.0,86.4 L 286.9,86.0 L 287.9,85.7 L 288.9,85.4 L 289.9,85.0 L 290.9,84.7 L 291.9,84.3 L 292.9,84.0 L 293.9,83.6 L 294.8,83.2 L 295.8,82.9 L 296.8,82.5 L 297.8,82.1 L 298.8,81.7 L 299.8,81.4 L 300.8,81.0 L 301.7,80.6 L 302.7,80.2 L 303.7,79.8 L 304.7,79.4 L 305.7,79.0 L 306.7,78.6 L 307.7,78.2 L 308.7,77.8 L 309.6,77.4 L 310.6,77.0 L 311.6,76.5 L 312.6,76.1 L 313.6,75.7 L 314.6,75.3 L 315.6,74.8 L 316.5,74.4 L 317.5,74.0 L 318.5,73.5 L 319.5,73.1 L 320.5,72.6 L 321.5,72.2 L 322.5,71.7 L 323.5,71.3 L 324.4,70.8 L 325.4,70.4 L 326.4,69.9 L 327.4,69.4 L 328.4,69.0 L 329.4,68.5 L 330.4,68.0 L 331.3,67.6 L 332.3,67.1 L 333.3,66.6 L 334.3,66.1 L 335.3,65.6 L 336.3,65.2 L 337.3,64.7 L 338.3,64.2 L 339.2,63.7 L 340.2,63.2 L 341.2,62.7 L 342.2,62.2 L 343.2,61.7 L 344.2,61.2 L 345.2,60.7 L 346.1,60.2 L 347.1,59.6 L 348.1,59.1 L 349.1,58.6 L 350.1,58.1 L 351.1,57.6 L 352.1,57.0 L 353.1,56.5 L 354.0,56.0 L 355.0,55.5 L 356.0,54.9 L 357.0,54.4 L 358.0,53.9 L 359.0,53.3 L 360.0,52.8 L 360.9,52.2 L 361.9,51.7 L 362.9,51.1 L 363.9,50.6 L 364.9,50.0 L 365.9,49.5 L 366.9,48.9 L 367.9,48.4 L 368.8,47.8 L 369.8,47.2 L 370.8,46.7 L 371.8,46.1 L 372.8,45.5 L 373.8,45.0 L 374.8,44.4 L 375.7,43.8 L 376.7,43.2 L 377.7,42.7 L 378.7,42.1 L 379.7,41.5 L 380.7,40.9 L 381.7,40.3 L 382.7,39.8 L 383.6,39.2 L 384.6,38.6 L 385.6,38.0 L 386.6,37.4 L 387.6,36.8 L 388.6,36.2 L 389.6,35.6 L 390.5,35.0 L 391.5,34.4 L 392.5,33.8 L 393.5,33.2 L 394.5,32.6 L 395.5,31.9 L 396.5,31.3 L 397.5,30.7 L 398.4,30.1 L 399.4,29.5 L 400.4,28.9 L 401.4,28.2 L 402.4,27.6 L 403.4,27.0 L 404.4,26.4" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="408" y="141.5" font-size="11" fill="currentColor" opacity="0.6" text-anchor="end">x</text>
  <text x="191.0" y="22" font-size="11" fill="currentColor" opacity="0.6">y</text>
</svg>
<figcaption>y² = x³ + 7 over the real numbers — a genuine curve, and what every diagram of this shows.</figcaption>
</figure>

That picture is honest about the **structure** and misleading about the **shape**.

Now keep the equation exactly as it is, and change only one thing: do the arithmetic with wrapping, modulo a small prime. The modulus is doing the work here — it's not a detail, it's the whole difference between the two pictures. Using 97, so the result fits on a page:

<figure markdown="span">
<svg viewBox="0 0 300 300" role="img" aria-label="The same equation over the field of 97 elements: 78 scattered points with no curved shape" style="width:100%;max-width:22rem;height:auto">
  <g stroke="currentColor" stroke-width="1" opacity="0.25">
    <line x1="30" y1="275" x2="290" y2="275"/>
    <line x1="30" y1="15" x2="30" y2="275"/>
  </g>
  <circle cx="32.7" cy="200.6" r="2.6" fill="currentColor"/><circle cx="32.7" cy="91.7" r="2.6" fill="currentColor"/><circle cx="43.3" cy="179.4" r="2.6" fill="currentColor"/><circle cx="43.3" cy="113.0" r="2.6" fill="currentColor"/><circle cx="61.9" cy="174.1" r="2.6" fill="currentColor"/><circle cx="61.9" cy="118.3" r="2.6" fill="currentColor"/><circle cx="64.5" cy="224.5" r="2.6" fill="currentColor"/><circle cx="64.5" cy="67.8" r="2.6" fill="currentColor"/><circle cx="67.2" cy="179.4" r="2.6" fill="currentColor"/><circle cx="67.2" cy="113.0" r="2.6" fill="currentColor"/><circle cx="75.2" cy="224.5" r="2.6" fill="currentColor"/><circle cx="75.2" cy="67.8" r="2.6" fill="currentColor"/><circle cx="83.1" cy="219.2" r="2.6" fill="currentColor"/><circle cx="83.1" cy="73.1" r="2.6" fill="currentColor"/><circle cx="85.8" cy="219.2" r="2.6" fill="currentColor"/><circle cx="85.8" cy="73.1" r="2.6" fill="currentColor"/><circle cx="91.1" cy="256.4" r="2.6" fill="currentColor"/><circle cx="91.1" cy="35.9" r="2.6" fill="currentColor"/><circle cx="101.7" cy="216.6" r="2.6" fill="currentColor"/><circle cx="101.7" cy="75.8" r="2.6" fill="currentColor"/><circle cx="107.0" cy="256.4" r="2.6" fill="currentColor"/><circle cx="107.0" cy="35.9" r="2.6" fill="currentColor"/><circle cx="115.0" cy="174.1" r="2.6" fill="currentColor"/><circle cx="115.0" cy="118.3" r="2.6" fill="currentColor"/><circle cx="117.7" cy="190.0" r="2.6" fill="currentColor"/><circle cx="117.7" cy="102.3" r="2.6" fill="currentColor"/><circle cx="123.0" cy="200.6" r="2.6" fill="currentColor"/><circle cx="123.0" cy="91.7" r="2.6" fill="currentColor"/><circle cx="125.6" cy="160.8" r="2.6" fill="currentColor"/><circle cx="125.6" cy="131.6" r="2.6" fill="currentColor"/><circle cx="146.9" cy="261.7" r="2.6" fill="currentColor"/><circle cx="146.9" cy="30.6" r="2.6" fill="currentColor"/><circle cx="149.5" cy="256.4" r="2.6" fill="currentColor"/><circle cx="149.5" cy="35.9" r="2.6" fill="currentColor"/><circle cx="168.1" cy="232.5" r="2.6" fill="currentColor"/><circle cx="168.1" cy="59.8" r="2.6" fill="currentColor"/><circle cx="170.8" cy="174.1" r="2.6" fill="currentColor"/><circle cx="170.8" cy="118.3" r="2.6" fill="currentColor"/><circle cx="176.1" cy="195.3" r="2.6" fill="currentColor"/><circle cx="176.1" cy="97.0" r="2.6" fill="currentColor"/><circle cx="178.8" cy="219.2" r="2.6" fill="currentColor"/><circle cx="178.8" cy="73.1" r="2.6" fill="currentColor"/><circle cx="181.4" cy="195.3" r="2.6" fill="currentColor"/><circle cx="181.4" cy="97.0" r="2.6" fill="currentColor"/><circle cx="189.4" cy="155.5" r="2.6" fill="currentColor"/><circle cx="189.4" cy="136.9" r="2.6" fill="currentColor"/><circle cx="192.0" cy="200.6" r="2.6" fill="currentColor"/><circle cx="192.0" cy="91.7" r="2.6" fill="currentColor"/><circle cx="194.7" cy="160.8" r="2.6" fill="currentColor"/><circle cx="194.7" cy="131.6" r="2.6" fill="currentColor"/><circle cx="197.3" cy="155.5" r="2.6" fill="currentColor"/><circle cx="197.3" cy="136.9" r="2.6" fill="currentColor"/><circle cx="202.7" cy="261.7" r="2.6" fill="currentColor"/><circle cx="202.7" cy="30.6" r="2.6" fill="currentColor"/><circle cx="208.0" cy="224.5" r="2.6" fill="currentColor"/><circle cx="208.0" cy="67.8" r="2.6" fill="currentColor"/><circle cx="210.6" cy="232.5" r="2.6" fill="currentColor"/><circle cx="210.6" cy="59.8" r="2.6" fill="currentColor"/><circle cx="218.6" cy="155.5" r="2.6" fill="currentColor"/><circle cx="218.6" cy="136.9" r="2.6" fill="currentColor"/><circle cx="221.2" cy="216.6" r="2.6" fill="currentColor"/><circle cx="221.2" cy="75.8" r="2.6" fill="currentColor"/><circle cx="223.9" cy="190.0" r="2.6" fill="currentColor"/><circle cx="223.9" cy="102.3" r="2.6" fill="currentColor"/><circle cx="226.6" cy="232.5" r="2.6" fill="currentColor"/><circle cx="226.6" cy="59.8" r="2.6" fill="currentColor"/><circle cx="237.2" cy="179.4" r="2.6" fill="currentColor"/><circle cx="237.2" cy="113.0" r="2.6" fill="currentColor"/><circle cx="247.8" cy="195.3" r="2.6" fill="currentColor"/><circle cx="247.8" cy="97.0" r="2.6" fill="currentColor"/><circle cx="255.8" cy="261.7" r="2.6" fill="currentColor"/><circle cx="255.8" cy="30.6" r="2.6" fill="currentColor"/><circle cx="263.8" cy="190.0" r="2.6" fill="currentColor"/><circle cx="263.8" cy="102.3" r="2.6" fill="currentColor"/><circle cx="282.3" cy="216.6" r="2.6" fill="currentColor"/><circle cx="282.3" cy="75.8" r="2.6" fill="currentColor"/><circle cx="285.0" cy="160.8" r="2.6" fill="currentColor"/><circle cx="285.0" cy="131.6" r="2.6" fill="currentColor"/>
  <text x="290" y="291" font-size="10" fill="currentColor" opacity="0.6" text-anchor="end">x →  96</text>
  <text x="14" y="22" font-size="10" fill="currentColor" opacity="0.6">96</text>
</svg>
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

    <figure markdown="span">
    <svg viewBox="0 0 460 300" role="img" aria-label="Adding two points on the real curve: a line through P and Q crosses the curve at a third point R, which is reflected across the horizontal axis to give P plus Q" style="width:100%;max-width:28rem;height:auto">
      <g stroke="currentColor" stroke-width="1" opacity="0.25">
        <line x1="40" y1="148.0" x2="445" y2="148.0"/>
        <line x1="194.9" y1="12" x2="194.9" y2="272"/>
      </g>
      <path d="M 444.2,261.3 L 443.0,260.5 L 441.8,259.8 L 440.7,259.1 L 439.5,258.3 L 438.3,257.6 L 437.1,256.9 L 435.9,256.1 L 434.7,255.4 L 433.5,254.7 L 432.3,254.0 L 431.1,253.3 L 429.9,252.5 L 428.7,251.8 L 427.6,251.1 L 426.4,250.4 L 425.2,249.7 L 424.0,249.0 L 422.8,248.3 L 421.6,247.6 L 420.4,246.9 L 419.2,246.2 L 418.0,245.5 L 416.8,244.8 L 415.6,244.2 L 414.5,243.5 L 413.3,242.8 L 412.1,242.1 L 410.9,241.4 L 409.7,240.8 L 408.5,240.1 L 407.3,239.4 L 406.1,238.8 L 404.9,238.1 L 403.7,237.4 L 402.5,236.8 L 401.3,236.1 L 400.2,235.5 L 399.0,234.8 L 397.8,234.2 L 396.6,233.5 L 395.4,232.9 L 394.2,232.3 L 393.0,231.6 L 391.8,231.0 L 390.6,230.4 L 389.4,229.7 L 388.2,229.1 L 387.1,228.5 L 385.9,227.9 L 384.7,227.3 L 383.5,226.6 L 382.3,226.0 L 381.1,225.4 L 379.9,224.8 L 378.7,224.2 L 377.5,223.6 L 376.3,223.0 L 375.1,222.4 L 374.0,221.9 L 372.8,221.3 L 371.6,220.7 L 370.4,220.1 L 369.2,219.5 L 368.0,219.0 L 366.8,218.4 L 365.6,217.8 L 364.4,217.3 L 363.2,216.7 L 362.0,216.2 L 360.8,215.6 L 359.7,215.1 L 358.5,214.5 L 357.3,214.0 L 356.1,213.4 L 354.9,212.9 L 353.7,212.4 L 352.5,211.8 L 351.3,211.3 L 350.1,210.8 L 348.9,210.3 L 347.7,209.8 L 346.6,209.3 L 345.4,208.8 L 344.2,208.3 L 343.0,207.8 L 341.8,207.3 L 340.6,206.8 L 339.4,206.3 L 338.2,205.8 L 337.0,205.3 L 335.8,204.9 L 334.6,204.4 L 333.5,203.9 L 332.3,203.5 L 331.1,203.0 L 329.9,202.6 L 328.7,202.1 L 327.5,201.7 L 326.3,201.2 L 325.1,200.8 L 323.9,200.4 L 322.7,199.9 L 321.5,199.5 L 320.3,199.1 L 319.2,198.7 L 318.0,198.3 L 316.8,197.9 L 315.6,197.5 L 314.4,197.1 L 313.2,196.7 L 312.0,196.3 L 310.8,195.9 L 309.6,195.5 L 308.4,195.2 L 307.2,194.8 L 306.1,194.4 L 304.9,194.1 L 303.7,193.7 L 302.5,193.4 L 301.3,193.0 L 300.1,192.7 L 298.9,192.4 L 297.7,192.0 L 296.5,191.7 L 295.3,191.4 L 294.1,191.1 L 293.0,190.8 L 291.8,190.5 L 290.6,190.2 L 289.4,189.9 L 288.2,189.6 L 287.0,189.3 L 285.8,189.0 L 284.6,188.8 L 283.4,188.5 L 282.2,188.3 L 281.0,188.0 L 279.8,187.8 L 278.7,187.5 L 277.5,187.3 L 276.3,187.0 L 275.1,186.8 L 273.9,186.6 L 272.7,186.4 L 271.5,186.2 L 270.3,186.0 L 269.1,185.8 L 267.9,185.6 L 266.7,185.4 L 265.6,185.2 L 264.4,185.0 L 263.2,184.8 L 262.0,184.7 L 260.8,184.5 L 259.6,184.4 L 258.4,184.2 L 257.2,184.1 L 256.0,183.9 L 254.8,183.8 L 253.6,183.6 L 252.5,183.5 L 251.3,183.4 L 250.1,183.3 L 248.9,183.2 L 247.7,183.0 L 246.5,182.9 L 245.3,182.8 L 244.1,182.7 L 242.9,182.7 L 241.7,182.6 L 240.5,182.5 L 239.3,182.4 L 238.2,182.3 L 237.0,182.3 L 235.8,182.2 L 234.6,182.1 L 233.4,182.1 L 232.2,182.0 L 231.0,181.9 L 229.8,181.9 L 228.6,181.9 L 227.4,181.8 L 226.2,181.8 L 225.1,181.7 L 223.9,181.7 L 222.7,181.7 L 221.5,181.6 L 220.3,181.6 L 219.1,181.6 L 217.9,181.6 L 216.7,181.5 L 215.5,181.5 L 214.3,181.5 L 213.1,181.5 L 212.0,181.5 L 210.8,181.5 L 209.6,181.5 L 208.4,181.4 L 207.2,181.4 L 206.0,181.4 L 204.8,181.4 L 203.6,181.4 L 202.4,181.4 L 201.2,181.4 L 200.0,181.4 L 198.8,181.4 L 197.7,181.4 L 196.5,181.4 L 195.3,181.4 L 194.1,181.4 L 192.9,181.4 L 191.7,181.4 L 190.5,181.4 L 189.3,181.4 L 188.1,181.4 L 186.9,181.4 L 185.7,181.4 L 184.6,181.4 L 183.4,181.4 L 182.2,181.4 L 181.0,181.4 L 179.8,181.4 L 178.6,181.4 L 177.4,181.4 L 176.2,181.3 L 175.0,181.3 L 173.8,181.3 L 172.6,181.3 L 171.5,181.3 L 170.3,181.3 L 169.1,181.2 L 167.9,181.2 L 166.7,181.2 L 165.5,181.1 L 164.3,181.1 L 163.1,181.1 L 161.9,181.0 L 160.7,181.0 L 159.5,180.9 L 158.3,180.9 L 157.2,180.8 L 156.0,180.7 L 154.8,180.7 L 153.6,180.6 L 152.4,180.5 L 151.2,180.5 L 150.0,180.4 L 148.8,180.3 L 147.6,180.2 L 146.4,180.1 L 145.2,180.0 L 144.1,179.9 L 142.9,179.8 L 141.7,179.7 L 140.5,179.6 L 139.3,179.4 L 138.1,179.3 L 136.9,179.1 L 135.7,179.0 L 134.5,178.8 L 133.3,178.7 L 132.1,178.5 L 131.0,178.3 L 129.8,178.1 L 128.6,177.9 L 127.4,177.7 L 126.2,177.5 L 125.0,177.3 L 123.8,177.1 L 122.6,176.8 L 121.4,176.6 L 120.2,176.3 L 119.0,176.1 L 117.8,175.8 L 116.7,175.5 L 115.5,175.2 L 114.3,174.9 L 113.1,174.5 L 111.9,174.2 L 110.7,173.8 L 109.5,173.4 L 108.3,173.1 L 107.1,172.6 L 105.9,172.2 L 104.7,171.8 L 103.6,171.3 L 102.4,170.8 L 101.2,170.3 L 100.0,169.7 L 98.8,169.2 L 97.6,168.5 L 96.4,167.9 L 95.2,167.2 L 94.0,166.5 L 92.8,165.7 L 91.6,164.9 L 90.5,164.0 L 89.3,163.1 L 88.1,162.0 L 86.9,160.9 L 85.7,159.6 L 84.5,158.1 L 83.3,156.3 L 82.1,153.9 L 80.9,148.0 L 80.9,148.0 L 82.1,142.1 L 83.3,139.7 L 84.5,137.9 L 85.7,136.4 L 86.9,135.1 L 88.1,134.0 L 89.3,132.9 L 90.5,132.0 L 91.6,131.1 L 92.8,130.3 L 94.0,129.5 L 95.2,128.8 L 96.4,128.1 L 97.6,127.5 L 98.8,126.8 L 100.0,126.3 L 101.2,125.7 L 102.4,125.2 L 103.6,124.7 L 104.7,124.2 L 105.9,123.8 L 107.1,123.4 L 108.3,122.9 L 109.5,122.6 L 110.7,122.2 L 111.9,121.8 L 113.1,121.5 L 114.3,121.1 L 115.5,120.8 L 116.7,120.5 L 117.8,120.2 L 119.0,119.9 L 120.2,119.7 L 121.4,119.4 L 122.6,119.2 L 123.8,118.9 L 125.0,118.7 L 126.2,118.5 L 127.4,118.3 L 128.6,118.1 L 129.8,117.9 L 131.0,117.7 L 132.1,117.5 L 133.3,117.3 L 134.5,117.2 L 135.7,117.0 L 136.9,116.9 L 138.1,116.7 L 139.3,116.6 L 140.5,116.4 L 141.7,116.3 L 142.9,116.2 L 144.1,116.1 L 145.2,116.0 L 146.4,115.9 L 147.6,115.8 L 148.8,115.7 L 150.0,115.6 L 151.2,115.5 L 152.4,115.5 L 153.6,115.4 L 154.8,115.3 L 156.0,115.3 L 157.2,115.2 L 158.3,115.1 L 159.5,115.1 L 160.7,115.0 L 161.9,115.0 L 163.1,114.9 L 164.3,114.9 L 165.5,114.9 L 166.7,114.8 L 167.9,114.8 L 169.1,114.8 L 170.3,114.7 L 171.5,114.7 L 172.6,114.7 L 173.8,114.7 L 175.0,114.7 L 176.2,114.7 L 177.4,114.6 L 178.6,114.6 L 179.8,114.6 L 181.0,114.6 L 182.2,114.6 L 183.4,114.6 L 184.6,114.6 L 185.7,114.6 L 186.9,114.6 L 188.1,114.6 L 189.3,114.6 L 190.5,114.6 L 191.7,114.6 L 192.9,114.6 L 194.1,114.6 L 195.3,114.6 L 196.5,114.6 L 197.7,114.6 L 198.8,114.6 L 200.0,114.6 L 201.2,114.6 L 202.4,114.6 L 203.6,114.6 L 204.8,114.6 L 206.0,114.6 L 207.2,114.6 L 208.4,114.6 L 209.6,114.5 L 210.8,114.5 L 212.0,114.5 L 213.1,114.5 L 214.3,114.5 L 215.5,114.5 L 216.7,114.5 L 217.9,114.4 L 219.1,114.4 L 220.3,114.4 L 221.5,114.4 L 222.7,114.3 L 223.9,114.3 L 225.1,114.3 L 226.2,114.2 L 227.4,114.2 L 228.6,114.1 L 229.8,114.1 L 231.0,114.1 L 232.2,114.0 L 233.4,113.9 L 234.6,113.9 L 235.8,113.8 L 237.0,113.7 L 238.2,113.7 L 239.3,113.6 L 240.5,113.5 L 241.7,113.4 L 242.9,113.3 L 244.1,113.3 L 245.3,113.2 L 246.5,113.1 L 247.7,113.0 L 248.9,112.8 L 250.1,112.7 L 251.3,112.6 L 252.5,112.5 L 253.6,112.4 L 254.8,112.2 L 256.0,112.1 L 257.2,111.9 L 258.4,111.8 L 259.6,111.6 L 260.8,111.5 L 262.0,111.3 L 263.2,111.2 L 264.4,111.0 L 265.6,110.8 L 266.7,110.6 L 267.9,110.4 L 269.1,110.2 L 270.3,110.0 L 271.5,109.8 L 272.7,109.6 L 273.9,109.4 L 275.1,109.2 L 276.3,109.0 L 277.5,108.7 L 278.7,108.5 L 279.8,108.2 L 281.0,108.0 L 282.2,107.7 L 283.4,107.5 L 284.6,107.2 L 285.8,107.0 L 287.0,106.7 L 288.2,106.4 L 289.4,106.1 L 290.6,105.8 L 291.8,105.5 L 293.0,105.2 L 294.1,104.9 L 295.3,104.6 L 296.5,104.3 L 297.7,104.0 L 298.9,103.6 L 300.1,103.3 L 301.3,103.0 L 302.5,102.6 L 303.7,102.3 L 304.9,101.9 L 306.1,101.6 L 307.2,101.2 L 308.4,100.8 L 309.6,100.5 L 310.8,100.1 L 312.0,99.7 L 313.2,99.3 L 314.4,98.9 L 315.6,98.5 L 316.8,98.1 L 318.0,97.7 L 319.2,97.3 L 320.3,96.9 L 321.5,96.5 L 322.7,96.1 L 323.9,95.6 L 325.1,95.2 L 326.3,94.8 L 327.5,94.3 L 328.7,93.9 L 329.9,93.4 L 331.1,93.0 L 332.3,92.5 L 333.5,92.1 L 334.6,91.6 L 335.8,91.1 L 337.0,90.7 L 338.2,90.2 L 339.4,89.7 L 340.6,89.2 L 341.8,88.7 L 343.0,88.2 L 344.2,87.7 L 345.4,87.2 L 346.6,86.7 L 347.7,86.2 L 348.9,85.7 L 350.1,85.2 L 351.3,84.7 L 352.5,84.2 L 353.7,83.6 L 354.9,83.1 L 356.1,82.6 L 357.3,82.0 L 358.5,81.5 L 359.7,80.9 L 360.8,80.4 L 362.0,79.8 L 363.2,79.3 L 364.4,78.7 L 365.6,78.2 L 366.8,77.6 L 368.0,77.0 L 369.2,76.5 L 370.4,75.9 L 371.6,75.3 L 372.8,74.7 L 374.0,74.1 L 375.1,73.6 L 376.3,73.0 L 377.5,72.4 L 378.7,71.8 L 379.9,71.2 L 381.1,70.6 L 382.3,70.0 L 383.5,69.4 L 384.7,68.7 L 385.9,68.1 L 387.1,67.5 L 388.2,66.9 L 389.4,66.3 L 390.6,65.6 L 391.8,65.0 L 393.0,64.4 L 394.2,63.7 L 395.4,63.1 L 396.6,62.5 L 397.8,61.8 L 399.0,61.2 L 400.2,60.5 L 401.3,59.9 L 402.5,59.2 L 403.7,58.6 L 404.9,57.9 L 406.1,57.2 L 407.3,56.6 L 408.5,55.9 L 409.7,55.2 L 410.9,54.6 L 412.1,53.9 L 413.3,53.2 L 414.5,52.5 L 415.6,51.8 L 416.8,51.2 L 418.0,50.5 L 419.2,49.8 L 420.4,49.1 L 421.6,48.4 L 422.8,47.7 L 424.0,47.0 L 425.2,46.3 L 426.4,45.6 L 427.6,44.9 L 428.7,44.2 L 429.9,43.5 L 431.1,42.7 L 432.3,42.0 L 433.5,41.3 L 434.7,40.6 L 435.9,39.9 L 437.1,39.1 L 438.3,38.4 L 439.5,37.7 L 440.7,36.9 L 441.8,36.2 L 443.0,35.5 L 444.2,34.7" fill="none" stroke="currentColor" stroke-width="2" opacity="0.85"/>
      <line x1="51.9" y1="125.5" x2="409.3" y2="89.5"
            stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.75"/>
      <line x1="148.7" y1="115.7" x2="148.7" y2="180.3"
            stroke="currentColor" stroke-width="1.4" stroke-dasharray="2 3" opacity="0.6"/>
      <circle cx="135.3" cy="117.1" r="4" fill="currentColor"/><text x="141.3" y="109.1" font-size="12" font-weight="bold" fill="currentColor">P</text>
      <circle cx="314.0" cy="99.1" r="4" fill="currentColor"/><text x="322.0" y="93.1" font-size="12" font-weight="bold" fill="currentColor">Q</text>
      <circle cx="148.7" cy="115.7" r="4" fill="currentColor"/><text x="132.7" y="107.7" font-size="12" font-weight="bold" fill="currentColor">R</text>
      <circle cx="148.7" cy="180.3" r="4" fill="currentColor"/><text x="114.7" y="196.3" font-size="12" font-weight="bold" fill="currentColor">P+Q</text>
    </svg>
    <figcaption>Adding P and Q: the chord meets the curve again at R, and P + Q is R reflected downwards.</figcaption>
    </figure>

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

!!! warning "Ethereum hashes the 64-byte form, with no prefix"

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

**Koblitz** is a person — Neal Koblitz, one of the mathematicians who proposed using elliptic curves for cryptography in the mid-1980s. A Koblitz curve is one whose constants are chosen to have deliberate structure rather than being picked arbitrarily, because structure makes the arithmetic faster. You can see it in secp256k1's own numbers: the equation is `y² = x³ + 7`, with no *x* term at all and a tiny constant, and the field prime sits just below a power of two. Both choices speed up the computation, and both are plainly visible rather than the output of some opaque procedure.

That last part turns out to matter, and it's the subject of the box below.

Bitcoin chose it, and Ethereum followed — which brought a decade of implementations, review and hardware support along with it.

??? info "There was another candidate, and the choice is interesting"

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

## When your public key becomes visible

A detail worth knowing, because it isn't obvious.

Receiving ether reveals nothing. People send to your **[address](addresses.md)**, which is a hash of your public key — and a hash can't be reversed, so an unused account exposes only the address.

Your public key becomes known the first time you **sign** something. A [signature](signatures.md) lets anyone recover the public key that produced it; that's how verification works at all. So the moment you send your first transaction, your public key is on the chain for good.

This doesn't put anything at risk today. The public key is meant to be public, and the private key stays unreachable behind the discrete logarithm problem.

So why mention it at all? Because it's a second lock, and it only matters if the first one ever fails.

??? abstract "When the distinction would actually matter"

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
    secret until you sign", and why the old advice not to reuse addresses had
    some substance to it.

    It isn't a reason to do anything differently today. It's a reason to know
    which assumption each part of the system is leaning on.

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
