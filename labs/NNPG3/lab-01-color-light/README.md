# Lab 01 — Color & Light (Phong on CPU)

RGB/HSL conversion plus per-vertex Phong shading computed in pure Python; output as ASCII + PPM.

## 1. Theory

- **RGB** = additive primaries for displays; **HSL** (hue/saturation/lightness) matches human color tweaking. Conversion is closed-form (see `rgb_to_hsl`).
- **Phong model:** `I = ambient + diffuse + specular`, with diffuse `kd·max(N·L,0)` and specular `ks·max(R·V,0)^shininess` per light. All vectors normalized.
- **Gamma:** shading math happens in linear space; PPM output here is raw linear values (note where sRGB encoding would apply).

## 2. Project layout

```
lab-01-color-light/
  README.md
  phong.py   # conversions + Phong + ASCII ramp + PPM writer
```

## 3. Run

```bash
cd labs/NNPG3/lab-01-color-light
python3 phong.py
python3 phong.py --out sphere.ppm
# view sphere.ppm with any image viewer (eog, GIMP, browser)
```

## 4. Verify

1. `python3 phong.py` prints `RGB(1,0,0) -> HSL(0.0,1.0,0.5)` and round-trip errors < 1e-9.
2. ASCII sphere shows a bright lobe toward the light and dark limb (not uniform).
3. `sphere.ppm` is a valid P3 file (`head -1` → `P3`, size line matches pixels).
4. `python3 -m py_compile phong.py` passes.

## 5. Tasks

1. Add a second (blue rim) light and re-render; compare ASCII output.
2. Implement sRGB encode (`c^(1/2.2)`) before PPM output; describe the visual change.
3. Sweep `shininess ∈ {4, 32, 256}`; note highlight size change.
4. Explain in 3 lines why `N·L` is clamped and what breaks without normalization.
