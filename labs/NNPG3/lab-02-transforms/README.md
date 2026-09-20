# Lab 02 — 4×4 Transforms (Pure Python)

Homogeneous transform library: translate/rotate/scale/compose, view + perspective projection.

## 1. Theory

- **Homogeneous coordinates** add `w=1` so translation becomes matrix multiplication; point pipeline: `clip = P·V·M·pos`, then perspective divide `ndc = clip.xyz/clip.w`.
- **Column-vector convention** here (as in OpenGL math): transforms compose right-to-left, `M = T·R·S` applies S first.
- **Perspective matrix** maps the frustum (`near..far`) to NDC `[-1,1]`; `w = -z_eye` gives the foreshortening divide.
- Tests assert known results (90° rotation, translate-then-divide, full cube projection inside NDC).

## 2. Project layout

```
lab-02-transforms/
  README.md
  mat4.py   # mat4 lib + self-test (no dependencies)
```

## 3. Run

```bash
cd labs/NNPG3/lab-02-transforms
python3 mat4.py
python3 mat4.py --verbose
```

## 4. Verify

1. `python3 mat4.py` prints `ALL 8 TESTS PASSED`.
2. Cube corners projected with the demo camera all land in NDC `[-1,1]`.
3. `python3 -m py_compile mat4.py` passes.

## 5. Tasks

1. Add `look_at` validation: camera looking straight down `-Z` must equal identity rotation.
2. Add `ortho()` and compare a cube rendering vs perspective (size constancy).
3. Implement matrix inverse for rigid transforms (transpose rotation, fix translation) and test `M·M⁻¹=I`.
4. Explain in 3 lines why rotation order matters (show `Rx·Ry ≠ Ry·Rx` numerically).
