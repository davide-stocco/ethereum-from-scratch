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

That picture is honest about the **structure** and misleading about the **shape**. Take the identical equation over a small finite field — let's use 97 instead of a 78-digit prime, so it fits on a page — and you get this instead:

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
<figcaption>y² = x³ + 7 modulo 97. The same equation, 78 points, and nothing remotely curved.</figcaption>
</figure>

Same equation, no curve. Just scattered dots, symmetric about the middle because *y* and *p* − *y* are both solutions.

secp256k1 is this second picture, with 97 replaced by a prime of 78 digits and roughly 10⁷⁷ points rather than 78. Nobody draws *that*.

So when you see a smooth curve with points labelled on it, read it as a **diagram of the rules**, not a map of the territory. The rules carry over exactly; the shape does not.

!!! note "Why the real-number picture is still worth having"

    The geometry is where point addition comes from. To add two points on the
    real curve you draw a straight line through them, find the third place it
    crosses, and reflect it across the horizontal axis — the chord-and-tangent
    construction. That's genuinely visual and genuinely how the rule was
    derived.

    Over a finite field the *same algebraic formulas* apply, and they still
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

That's it. Take G, add it to itself as many times as your private key says, and the point you land on is your public key. Since a private key is around 10⁷⁷, "as many times as your private key says" isn't something anyone does literally — see the box further down.

??? example "Try it: private key to public key"

    <div class="tool" markdown="0">
      <label for="pub-priv">Private key (hex)</label>
      <input id="pub-priv" type="text" autocomplete="off" spellcheck="false" value="1">
      <button id="pub-rand" type="button">Random key</button>
      <p class="tool__out" id="pub-out"></p>
    </div>

    Work through it in this order — each step shows something different.

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
