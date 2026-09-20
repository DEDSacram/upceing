# Lab 03 — OpenGL Pipeline (Software Rasterizer)

A minimal CPU rasterizer: vertex transform → clip → NDC → viewport → barycentric fill → PPM.

## 1. Theory

- **Pipeline stages:** vertex shader (transform, here identity/model only) → primitive assembly → clipping → perspective divide → viewport transform → rasterization (which pixels does the triangle cover?) → fragment shading (flat color + depth test) → framebuffer.
- **Barycentric edge functions:** pixel center `p` is inside iff all three edge values have the same sign (top-left rule for ties); barycentrics interpolate depth/color.
- **Depth test:** keep closest `z` per pixel (`z-buffer`) so nearer triangles win regardless of draw order.

## 2. Project layout

```
lab-03-opengl-pipeline/
  README.md
  raster.py   # math + rasterizer, draws two overlapping triangles to PPM + ASCII
```

## 3. Run

```bash
cd labs/NNPG3/lab-03-opengl-pipeline
python3 raster.py
python3 raster.py --out scene.ppm --size 120x80
```

## 4. Verify

1. `python3 raster.py` prints pixel counts for both triangles with `front > 0` and `back > 0`, and `overlap` pixels won by the nearer triangle.
2. ASCII preview shows two nested triangle shapes (brighter front triangle inside).
3. `scene.ppm` parses as P3 with the requested dimensions.
4. `python3 -m py_compile raster.py` passes.

## 5. Tasks

1. Add per-vertex color interpolation (varyings) instead of flat shading.
2. Draw the triangles in reverse order; confirm identical output (depth test proof).
3. Implement back-face culling via signed area; verify a CW triangle disappears.
4. Measure overdraw: count fragments shaded more than once.
