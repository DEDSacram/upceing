# Lab 04 — Shaders (GLSL + CPU Reference)

A Lambert vertex/fragment shader pair plus a bit-exact CPU reference in Python.

## 1. Theory

- **Vertex shader** runs per vertex: transforms position (`uMVP * vec4(aPos,1)`), passes normal/color varyings.
- **Fragment shader** runs per pixel: interpolates varyings, evaluates lighting (here Lambert diffuse + ambient), outputs `fragColor`.
- **Uniforms** (`uMVP`, `uLightDir`) are constant per draw call; **attributes** per vertex; **varyings** interpolated across the triangle.
- The CPU reference implements the same math so results can be checked without a GPU; GLSL sources are validated by careful authoring + a local syntax sanity script (balanced braces/parens, `void main`, precision).

## 2. Project layout

```
lab-04-shaders/
  README.md
  lambert.vert     # GLSL vertex shader
  lambert.frag     # GLSL fragment shader
  cpu_shader.py    # CPU reference: transforms 3 verts, shades, checks GLSL files
```

## 3. Run

```bash
cd labs/NNPG3/lab-04-shaders
python3 cpu_shader.py
```

## 4. Verify

1. `python3 cpu_shader.py` prints per-vertex NDC + shaded RGB and `GLSL SANITY OK`.
2. Top vertex (normal facing light) is brighter than the two base vertices.
3. `python3 -m py_compile cpu_shader.py` passes. (GLSL needs a GPU driver to truly compile — noted, not executed here.)

## 5. Tasks

1. Add a `uShininess` specular term in both `.frag` and `cpu_shader.py`; keep outputs in sync.
2. Add an `aColor` attribute blended with the light (verify CPU vs GPU by screenshots if a GPU is available).
3. Break `lambert.frag` on purpose (delete a semicolon); confirm the sanity script catches it.
4. Port the shaders to WebGL (add `precision mediump float;`) and render in a browser.
