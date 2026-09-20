"""Software rasterizer: two overlapping triangles -> PPM + ASCII (stdlib)."""
import argparse

def edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)

def raster_tri(v, w, h):
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = v
    area = edge(x0, y0, x1, y1, x2, y2)
    if area == 0:
        return {}
    xs = [x0, x1, x2]; ys = [y0, y1, y2]
    minx, maxx = max(0, int(min(xs))), min(w - 1, int(max(xs)) + 1)
    miny, maxy = max(0, int(min(ys))), min(h - 1, int(max(ys)) + 1)
    out = {}
    for py in range(miny, maxy + 1):
        for px in range(minx, maxx + 1):
            cx, cy = px + 0.5, py + 0.5
            e0 = edge(x1, y1, x2, y2, cx, cy)
            e1 = edge(x2, y2, x0, y0, cx, cy)
            e2 = edge(x0, y0, x1, y1, cx, cy)
            if (e0 >= 0 and e1 >= 0 and e2 >= 0) or (e0 <= 0 and e1 <= 0 and e2 <= 0):
                l0, l1, l2 = e0 / area, e1 / area, e2 / area
                out[(px, py)] = l0 * z0 + l1 * z1 + l2 * z2
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="scene.ppm")
    ap.add_argument("--size", default="60x40")
    a = ap.parse_args()
    w, h = map(int, a.size.split("x"))
    # back triangle (z=0.8, dim) and front triangle (z=0.3, bright), overlapping
    back = [(8, 5, 0.8), (w - 8, 5, 0.8), (w / 2, h - 5, 0.8)]
    front = [(w*0.3, h*0.35, 0.3), (w*0.7, h*0.35, 0.3), (w/2, h*0.8, 0.3)]
    fb = [[(10, 10, 30) for _ in range(w)] for _ in range(h)]
    zb = [[1.0 for _ in range(w)] for _ in range(h)]
    stats = {}
    for name, tri, col in (("back", back, (60, 60, 160)), ("front", front, (220, 180, 60))):
        frags = raster_tri(tri, w, h)
        drawn, overlap = 0, 0
        for (px, py), z in frags.items():
            if z < zb[py][px]:
                if fb[py][px] != (10, 10, 30):
                    overlap += 1
                zb[py][px] = z
                fb[py][px] = col
                drawn += 1
        stats[name] = (len(frags), drawn, overlap)
    for name, (frags, drawn, overlap) in stats.items():
        print(f"{name}: fragments={frags} drawn={drawn} overdraw_wins={overlap}")
    assert stats["front"][1] > 0 and stats["back"][1] > 0
    assert stats["front"][2] > 0, "front triangle should cover part of back"
    ramp = " .:-=+*#%@"
    for row in fb[::2]:
        print("".join(ramp[(r + g + b) // 3 * (len(ramp) - 1) // 255] for r, g, b in row[::1]))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(f"P3\n{w} {h}\n255\n")
        for row in fb:
            f.write(" ".join(f"{r} {g} {b}" for r, g, b in row) + "\n")
    print(f"wrote {a.out}")

if __name__ == "__main__":
    main()
