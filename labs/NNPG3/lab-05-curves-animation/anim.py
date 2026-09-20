"""Bezier curves + keyframe animation rendered to PPM frames (stdlib)."""
import argparse
from pathlib import Path

P0 = (10, 50); P1 = (30, 5); P2 = (70, 55); P3 = (90, 15)

def lerp(a, b, t):
    return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)

def bezier(ctrl, t):
    a = lerp(ctrl[0], ctrl[1], t)
    b = lerp(ctrl[1], ctrl[2], t)
    c = lerp(ctrl[2], ctrl[3], t)
    d = lerp(a, b, t)
    e = lerp(b, c, t)
    return lerp(d, e, t)

def smoothstep(t):
    return t*t*(3-2*t)

def draw_frame(path, w, h, trail, ball):
    fb = [[(15, 15, 40) for _ in range(w)] for _ in range(h)]
    for x, y in trail:
        xi, yi = int(x), int(y)
        if 0 <= xi < w and 0 <= yi < h:
            fb[yi][xi] = (80, 80, 120)
    bx, by = int(ball[0]), int(ball[1])
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if dx*dx+dy*dy <= 9 and 0 <= bx+dx < w and 0 <= by+dy < h:
                fb[by+dy][bx+dx] = (230, 200, 80)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"P3\n{w} {h}\n255\n")
        for row in fb:
            f.write(" ".join(f"{r} {g} {b}" for r, g, b in row) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=8)
    ap.add_argument("--out-dir", default="frames")
    ap.add_argument("--ease", choices=["linear", "smooth"], default="smooth")
    a = ap.parse_args()
    ctrl = (P0, P1, P2, P3)
    assert bezier(ctrl, 0.0) == (float(P0[0]), float(P0[1])), "B(0) must equal P0"
    assert bezier(ctrl, 1.0) == (float(P3[0]), float(P3[1])), "B(1) must equal P3"
    mid = bezier(ctrl, 0.5)
    analytic = (
        0.125*P0[0]+0.375*P1[0]+0.375*P2[0]+0.125*P3[0],
        0.125*P0[1]+0.375*P1[1]+0.375*P2[1]+0.125*P3[1])
    assert abs(mid[0]-analytic[0]) < 1e-9 and abs(mid[1]-analytic[1]) < 1e-9
    print(f"B(0)={bezier(ctrl,0.0)} B(0.5)={tuple(round(c,2) for c in mid)} B(1)={bezier(ctrl,1.0)}")
    out = Path(a.out_dir)
    out.mkdir(exist_ok=True)
    trail = [bezier(ctrl, i/100) for i in range(101)]
    ease = smoothstep if a.ease == "smooth" else (lambda t: t)
    for i in range(a.frames):
        t = ease(i/(a.frames-1))
        pos = bezier(ctrl, t)
        draw_frame(out / f"frame_{i:02d}.ppm", 100, 60, trail, pos)
    print(f"wrote {a.frames} frames to {a.out_dir}/ (ease={a.ease})")

if __name__ == "__main__":
    main()
