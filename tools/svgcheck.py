"""Estimate text boxes in an inline SVG and report collisions.

Catches the three things that have gone wrong by eye: text past the viewBox,
two texts on top of each other, and text sitting on a rect's border line.
Widths are estimates, so treat small overlaps as warnings not proof.
"""
import re, sys

def texts(svg):
    out=[]
    for m in re.finditer(r'<text ([^>]*)>(.*?)</text>', svg, re.S):
        a, raw = m.group(1), m.group(2)
        def at(n, d=None):
            mm=re.search(n+r'="([^"]*)"', a); return mm.group(1) if mm else d
        txt=re.sub(r'<[^>]+>','',raw)
        txt=re.sub(r'&#\d+;','X',txt); txt=re.sub(r'&\w+;','X',txt)
        fs=float(at('font-size','12')); x=float(at('x','0')); y=float(at('y','0'))
        w=len(txt)*fs*0.52
        anch=at('text-anchor','start')
        x0 = x-w/2 if anch=='middle' else (x-w if anch=='end' else x)
        out.append(dict(t=txt.strip()[:40], x0=x0, x1=x0+w, y0=y-fs*0.78, y1=y+fs*0.22, fs=fs))
    return out

def rects(svg):
    out=[]
    for m in re.finditer(r'<rect ([^>]*)/?>', svg):
        a=m.group(1)
        if 'fill="var(' in a:      # a label's own backing chip, not a drawn box
            continue
        def at(n,d='0'):
            mm=re.search(n+r'="([^"]*)"',a); return float(mm.group(1)) if mm else float(d)
        out.append((at('x'),at('y'),at('x')+at('width'),at('y')+at('height')))
    return out

def check(svg, name):
    vb=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    VW,VH=float(vb.group(1)),float(vb.group(2))
    T, R = texts(svg), rects(svg)
    bad=[]
    for t in T:
        if t['x1']>VW+1 or t['y1']>VH+1 or t['x0']<-1 or t['y0']<-1:
            bad.append(f"outside viewBox ({VW:.0f}x{VH:.0f}): {t['t']!r} spans x{t['x0']:.0f}-{t['x1']:.0f} y{t['y0']:.0f}-{t['y1']:.0f}")
    for i in range(len(T)):
        for j in range(i+1,len(T)):
            a,b=T[i],T[j]
            ox=min(a['x1'],b['x1'])-max(a['x0'],b['x0']); oy=min(a['y1'],b['y1'])-max(a['y0'],b['y0'])
            if ox>2 and oy>1: bad.append(f"text overlaps text: {a['t']!r} / {b['t']!r} ({ox:.0f}x{oy:.0f}px)")
    for t in T:
        for (rx0,ry0,rx1,ry1) in R:
            for edge,val in (("top",ry0),("bottom",ry1)):
                if t['y0']-1 < val < t['y1']+1 and t['x1']>rx0+2 and t['x0']<rx1-2:
                    bad.append(f"text sits on a rect {edge} edge y={val:.0f}: {t['t']!r}")
            for edge,val in (("left",rx0),("right",rx1)):
                if t['x0']-1 < val < t['x1']+1 and t['y1']>ry0+2 and t['y0']<ry1-2:
                    bad.append(f"text crosses a rect {edge} edge x={val:.0f}: {t['t']!r}")
    seen=set(); uniq=[b for b in bad if not (b in seen or seen.add(b))]
    print(f"{name}: {len(uniq)} issue(s)")
    for b in uniq: print("   -", b)
    return len(uniq)

if __name__ == "__main__":
    import pathlib, glob
    total=0
    for f in sorted(glob.glob("docs/**/*.md", recursive=True)):
        body=pathlib.Path(f).read_text()
        for i,s in enumerate([x for x in re.findall(r'<svg.*?</svg>', body, re.S) if len(x)>900],1):
            total+=check(s, f"{f} svg{i}")
    print("TOTAL ISSUES:", total)
