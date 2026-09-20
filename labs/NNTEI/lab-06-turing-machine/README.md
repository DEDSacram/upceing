# Lab 06 — Turing Machine Simulator + Unary Adder

A textbook Turing machine: finite control, infinite tape, read/write/move. Demo: unary addition.

## 1. Theory

- A **TM** is `(Q, Gamma, blank, delta, q0, q_acc, q_rej)`: `delta(q, a) = (q', b, D)` writes `b`, moves `D in {L,R}`, enters `q'`. The tape is infinite both ways (simulated here with a dict + blank default).
- **Unary adder:** input `1^n + 1^m`; erase the `+` and one `1`, i.e. rewrite to `1^(n+m)`. A 3-state machine suffices: scan right to `+`, replace with `1`, scan to the end, erase the last `1`, halt.
- TMs define **decidability**: a language is decidable iff some TM halts with accept/reject on every input. Everything computable = TM-computable (Church–Turing thesis).
- Cost model preview of Lab 07: count *steps* as the time measure.

## 2. Project layout

```
lab-06-turing-machine/
  README.md
  tm.py   # generic TM + unary adder + step counting
```

## 3. Run

```bash
cd lab-06-turing-machine
python3 tm.py
```

## 4. Verify

1. `python3 -m py_compile tm.py` succeeds.
2. `python3 tm.py` shows `111+11 -> 11111` and `ALL SELF-CHECKS PASSED`.
3. Step counts grow linearly with input length (printed table).

## 5. Tasks

1. Add a unary decrementer (`1^n -> 1^(n-1)`) as a new transition table.
2. Implement a binary incrementer (alphabet `{0,1}`, handle carry `111->1000`).
3. Add a step-limit guard reporting `TIMEOUT` instead of looping forever; demo on a looping machine.
4. Build a 2-tape-concatenation demo (copy `w` to `ww`) reusing the simulator.
5. Argue (comment) why the adder runs in O(n) steps; measure steps for n = 5..50.
