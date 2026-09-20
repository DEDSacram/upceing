# Lab 05 — Curves & Keyframe Animation

Cubic Bézier evaluation (de Casteljau) plus keyframe interpolation; renders PPM frames of a ball on a curve.

## 1. Theory

- **Cubic Bézier:** `B(t) = (1−t)³P0 + 3(1−t)²tP1 + 3(1−t)t²P2 + t³P3`; endpoints interpolated, middle points weighted. **de Casteljau** evaluates by repeated linear interpolation (numerically stable).
- **Keyframe animation:** poses at key times; in-betweens via interpolation — linear (`lerp`) for positions, easing (`smoothstep`) for velocity control.
- **Frames:** sample `t ∈ [0,1]` at N steps, draw the ball + curve trail into PPMs (`frame_00.ppm`, …).

## 2. Project layout

```
lab-05-curves-animation/
  README.md
  anim.py   # bezier + keyframes + PPM frame renderer
```

## 3. Run

```bash
cd labs/NNPG3/lab-05-curves-animation
python3 anim.py
python3 anim.py --frames 12 --out-dir frames
ls frames/
```

## 4. Verify

1. `python3 anim.py` prints `B(0)=P0`, `B(1)=P3` exactly and midpoint `B(0.5)` matching the analytic value.
2. `frames/` contains N valid P3 PPMs; first frame ball near P0, last near P3.
3. `python3 -m py_compile anim.py` passes.

## 5. Tasks

1. Add a second segment (piecewise path) with C1 continuity; render the joined motion.
2. Compare `lerp` vs `smoothstep` easing: print velocity profiles.
3. Draw velocity vectors (tangent via `B(t+ε)−B(t)`) into each frame.
4. Convert frames to GIF (`convert frames/*.ppm anim.gif`) and embed in this README.
