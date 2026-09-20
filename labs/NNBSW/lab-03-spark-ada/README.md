# Lab 03 — SPARK/Ada Contracts Intro

Design-by-contract in Ada/SPARK: pre/postconditions + loop invariants discharged by GNATprove.

## 1. Theory

- **Ada** = strongly-typed systems language (avionics, rail). **SPARK** = verifiable subset: no pointers-to-nowhere, contracts prove absence of runtime errors (AoRTE).
- **Contracts:** `Pre` (caller obligation), `Post` (callee guarantee, `Old`/`Result` attributes), `Loop_Invariant`, `Assert`. The prover checks them statically — stronger than testing.
- **Workflow:** `gnatprove -P proof.gpr` → flow analysis + proof obligations (each `Post`/`Invariant` = a VC to discharge).
- This lab is **authored carefully without execution** unless GNAT is installed: contracts below are standard SPARK 2014 idioms.

## 2. Project layout

```
lab-03-spark-ada/
  README.md
  speed.ads        # package spec with Pre/Post contracts
  speed.adb        # body with loop invariant example
  proof.gpr        # GNAT project file (gnatprove entry point)
```

## 3. Run

```bash
cd labs/NNBSW/lab-03-spark-ada
# if GNAT is installed:
which gnatprove && gnatprove -P proof.gpr --level=2 || echo "GNAT not installed — review contracts by reading only"
gnatmake -gnata speed.adb 2>/dev/null || true
```

## 4. Verify

1. `speed.ads` compiles under GNAT if present (`gnatmake` clean); otherwise review: every function has `Pre`+`Post`, no `access` types (SPARK subset).
2. `speed.adb` loop carries a `Loop_Invariant` that implies the `Post`.
3. `gnatprove` (if available) reports all VCs discharged; if unavailable, note `GNAT-not-present` and complete Tasks 1–2 by reading.

## 5. Tasks

1. Strengthen `Clamp` postcondition with `Result in Low..High` and prove it.
2. Add a `Saturating_Add` function with overflow-proof contract (`Pre: X <= Natural'Last - Y` or saturating post).
3. Write a failing contract on purpose (wrong `Post`), run gnatprove, paste the unproved VC.
4. Explain in 5 lines when testing (Lab 02) beats proof and vice versa.
