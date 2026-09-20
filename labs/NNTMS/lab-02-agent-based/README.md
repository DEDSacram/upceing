# Lab 02 — Agent-Based Traffic (Ring Road)

Nagel–Schreckenberg-style toy: N cars on a ring, accelerate/brake/random-slow.

## 1. Theory

- **Agent-based modeling:** global patterns (phantom jams) emerge from local rules — no central controller.
- **Ring road:** periodic boundary removes inflow/outflow effects; density is conserved, so jams are purely emergent.
- **Rules per step:** accelerate (`v=min(v+1,vmax)`), brake to gap (`v=min(v,gap)`), random slowdown with prob `p`, move `x=(x+v) mod L`.
- **Fundamental diagram:** flow rises with density, then collapses past critical density.

## 2. Project layout

```
lab-02-agent-based/
  README.md
  traffic.py   # ring-road sim + ASCII snapshots + flow measurement
```

## 3. Run

```bash
cd labs/NNTMS/lab-02-agent-based
python3 traffic.py
python3 traffic.py --cars 30 --steps 200 --seed 3
```

## 4. Verify

1. Default run prints flow stats and an ASCII ring with at least one jam cluster at high density.
2. Low density (`--cars 5`) shows near-max mean speed; high density (`--cars 40`) shows lower flow than medium (`--cars 20`).
3. `python3 -m py_compile traffic.py` passes.

## 5. Tasks

1. Sweep density 0.05–0.9, plot the fundamental diagram (flow vs density).
2. Set `p=0` (no randomness): do jams still form from the clustered start? Why?
3. Add a slow truck (`vmax=2`) and measure its effect on flow.
4. Animate 3 densities as ASCII frames and describe jam propagation direction.
