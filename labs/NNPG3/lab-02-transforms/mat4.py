"""4x4 matrix library in pure Python (row-major, column vectors)."""
import math

def identity():
    return [[1 if i == j else 0 for j in range(4)] for i in range(4)]

def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def matvec(A, v):
    return [sum(A[i][j]*v[j] for j in range(4)) for i in range(4)]

def translate(tx, ty, tz):
    M = identity(); M[0][3], M[1][3], M[2][3] = tx, ty, tz
    return M

def scale(sx, sy, sz):
    M = identity(); M[0][0], M[1][1], M[2][2] = sx, sy, sz
    return M

def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return [[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]]

def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return [[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]]

def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return [[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]]

def perspective(fovy, aspect, near, far):
    f = 1 / math.tan(fovy/2)
    nf = 1 / (near - far)
    return [[f/aspect,0,0,0],[0,f,0,0],[0,0,(far+near)*nf,2*far*near*nf],
            [0,0,-1,0]]

def _flat(m):
    for x in m:
        if isinstance(x, list):
            yield from _flat(x)
        else:
            yield x

def approx(a, b, eps=1e-9):
    if isinstance(a, list):
        return all(abs(x-y) < eps for x, y in zip(_flat(a), _flat(b)))
    return abs(a-b) < eps

def run_tests(verbose=False):
    T = []
    T.append(("identity", approx(matvec(identity(), [1,2,3,1]), [1,2,3,1])))
    T.append(("translate", approx(matvec(translate(1,2,3), [0,0,0,1]), [1,2,3,1])))
    T.append(("rot-z-90", approx(matvec(rot_z(math.pi/2), [1,0,0,1])[:2], [0,1])))
    T.append(("rot-x-90", approx(matvec(rot_x(math.pi/2), [0,1,0,1])[1:3], [0,1])))
    T.append(("scale", approx(matvec(scale(2,3,4), [1,1,1,1]), [2,3,4,1])))
    T.append(("compose", approx(matvec(matmul(translate(1,0,0), scale(2,1,1)), [1,0,0,1]), [3,0,0,1])))
    T.append(("non-commute", not approx(matmul(rot_x(0.5), rot_y(0.5)), matmul(rot_y(0.5), rot_x(0.5)))))
    # full pipeline: cube at origin, camera at z=5 -> all corners in NDC
    P = perspective(math.radians(60), 1.0, 0.1, 100)
    V = translate(0, 0, -5)
    ok = True
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                clip = matvec(matmul(P, V), [sx, sy, sz, 1])
                ndc = [clip[i]/clip[3] for i in range(3)]
                if not all(-1 <= c <= 1 for c in ndc):
                    ok = False
    T.append(("cube-in-frustum", ok))
    for name, passed in T:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    good = sum(1 for _, p in T if p)
    print(f"ALL {good} TESTS PASSED" if good == len(T) else f"{len(T)-good} TESTS FAILED")
    assert good == len(T)
    if verbose:
        print("P =", perspective(math.radians(60), 1.0, 0.1, 100)[0])

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    run_tests(a.verbose)

if __name__ == "__main__":
    main()
