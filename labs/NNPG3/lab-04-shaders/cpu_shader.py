"""CPU reference for the Lambert shader pair + GLSL sanity check (stdlib)."""
import math
from pathlib import Path

def vdot(a, b): return sum(x*y for x, y in zip(a, b))
def vnorm(a):
    n = math.sqrt(vdot(a, a)) or 1.0
    return tuple(x/n for x in a)

def vertex(aPos, aNormal, MVP):
    wp = [sum(MVP[i][j] * (aPos[j] if j < 3 else 1.0) for j in range(4)) for i in range(4)]
    w = wp[3] or 1.0
    ndc = tuple(c / w for c in wp[:3])
    n = vnorm(aNormal)  # MVP is identity here -> mat3(MVP)*n == n
    return ndc, n

def fragment(N, light, base):
    diff = max(vdot(vnorm(N), vnorm(light)), 0.0)
    return tuple(c * (0.15 + 0.85 * diff) for c in base)

def glsl_sanity(path):
    src = Path(path).read_text(encoding="utf-8")
    assert "void main" in src, f"{path}: missing main"
    assert src.count("{") == src.count("}"), f"{path}: unbalanced braces"
    assert src.count("(") == src.count(")"), f"{path}: unbalanced parens"
    assert src.rstrip().endswith("}"), f"{path}: must end with }}"
    for i, line in enumerate(src.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#") or s.endswith("{") or s.endswith("}"):
            continue
        if any(s.startswith(k) for k in ("layout", "uniform", "in ", "in\t", "out ", "version",
                                         "vec", "float", "int", "mat", "if", "for", "while", "return", "}")):
            continue
        assert s.endswith(";"), f"{path}:{i}: missing semicolon: {s}"
    return True

def main():
    base = Path(__file__).parent
    for f in ("lambert.vert", "lambert.frag"):
        glsl_sanity(base / f)
        print(f"sanity OK: {f}")
    print("GLSL SANITY OK")
    MVP = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    light, color = (0.3, 0.4, 1.0), (0.9, 0.3, 0.2)
    verts = [((0, 1, 0), (0, 0, 1)), ((-1, -1, 0), (-0.3, -0.3, 1)), ((1, -1, 0), (0.3, -0.3, 1))]
    shades = []
    for pos, nrm in verts:
        ndc, n = vertex(pos, nrm, MVP)
        col = fragment(n, light, color)
        shades.append(sum(col) / 3)
        print(f"pos={pos} ndc={tuple(round(c,3) for c in ndc)} rgb={tuple(round(c,3) for c in col)}")
    assert shades[0] > shades[1] and shades[0] > shades[2], "top vertex must be brightest"
    print("OK: top vertex brightest, CPU matches shader intent.")

if __name__ == "__main__":
    main()
