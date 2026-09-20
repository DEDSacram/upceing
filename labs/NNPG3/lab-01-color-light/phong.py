"""RGB/HSL conversion + CPU Phong shading with ASCII/PPM output (stdlib)."""
import argparse, math

def rgb_to_hsl(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = ((g - b) / d + (6 if g < b else 0)) / 6
    elif mx == g:
        h = ((b - r) / d + 2) / 6
    else:
        h = ((r - g) / d + 4) / 6
    return h * 360, s, l

def hsl_to_rgb(h, s, l):
    h = (h % 360) / 360
    if s == 0:
        return l, l, l
    def hue(p, q, t):
        t %= 1.0
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    return hue(p, q, h + 1/3), hue(p, q, h), hue(p, q, h - 1/3)

def vsub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def vdot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def vnorm(a):
    n = math.sqrt(vdot(a, a)) or 1.0
    return (a[0]/n, a[1]/n, a[2]/n)

def phong(N, L, V, base, ka=0.1, kd=0.7, ks=0.5, shin=32, light=(1, 1, 1)):
    N, L, V = vnorm(N), vnorm(L), vnorm(V)
    nl = max(vdot(N, L), 0.0)
    R = vnorm((2*nl*N[0]-L[0], 2*nl*N[1]-L[1], 2*nl*N[2]-L[2]))
    spec = max(vdot(R, V), 0.0) ** shin
    return tuple(min(1.0, ka*c + kd*c*nl*li + ks*li*spec) for c, li in zip(base, light))

def render(w=40, h=20):
    ramp = " .:-=+*#%@"
    rows, img = [], []
    for y in range(h):
        line, irow = "", []
        for x in range(w):
            nx = (x / (w - 1)) * 2 - 1
            ny = -((y / (h - 1)) * 2 - 1)
            r2 = nx*nx + ny*ny
            if r2 > 1:
                line += " "; irow.append((0, 0, 0)); continue
            nz = math.sqrt(1 - r2)
            c = phong((nx, ny, nz), (0.5, 0.5, 1.0), (0, 0, 1), (0.9, 0.25, 0.2))
            lum = 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
            line += ramp[min(int(lum * len(ramp)), len(ramp)-1)]
            irow.append(c)
        rows.append(line); img.append(irow)
    return rows, img

def write_ppm(path, img):
    h, w = len(img), len(img[0])
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"P3\n{w} {h}\n255\n")
        for row in img:
            f.write(" ".join(f"{int(r*255)} {int(g*255)} {int(b*255)}" for r, g, b in row) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="sphere.ppm")
    a = ap.parse_args()
    h, s, l = rgb_to_hsl(1, 0, 0)
    print(f"RGB(1,0,0) -> HSL({h:.1f},{s:.1f},{l:.1f})")
    err = 0.0
    import random
    rng = random.Random(0)
    for _ in range(200):
        c = (rng.random(), rng.random(), rng.random())
        back = hsl_to_rgb(*rgb_to_hsl(*c))
        err = max(err, max(abs(x - y) for x, y in zip(c, back)))
    print(f"round-trip max error: {err:.2e}")
    assert err < 1e-9
    rows, img = render()
    print("\n".join(rows))
    write_ppm(a.out, img)
    print(f"wrote {a.out}")

if __name__ == "__main__":
    main()
