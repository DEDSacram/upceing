# Lab 01 — Hazard Analysis & Risk Matrix

Systematic hazard log with a 5×5 severity×likelihood matrix and a runnable risk-score calculator.

## 1. Theory

- **Hazard** = system state that can lead to an accident (e.g. "uncommanded braking"). **Risk = severity × likelihood**.
- **5×5 matrix:** severity S1–S5 (negligible → catastrophic) × likelihood L1–L5 (improbable → frequent). Score = S×L (1–25). Bands: 1–4 low (green), 5–9 medium (yellow), 10–16 high (orange), 17–25 extreme (red).
- **ALARP:** reduce risk As Low As Reasonably Practicable; extreme risks are intolerable without mitigation. Mitigations lower likelihood (interlocks) or severity (fail-safe defaults).
- This lab logs 5 railway-crossing style hazards, scores them, and re-scores after mitigations.

## 2. Project layout

```
lab-01-hazard-analysis/
  README.md
  hazards.yaml       # hazard log starter (5 hazards with S/L + mitigations)
  risk_matrix.txt    # ASCII 5x5 matrix reference
  risk_calc.py       # scores hazards, prints bands, verifies mitigations lower risk
```

## 3. Run

```bash
cd labs/NNBSW/lab-01-hazard-analysis
python3 risk_calc.py hazards.yaml
```

## 4. Verify

1. `python3 risk_calc.py hazards.yaml` exits 0, prints 5 hazards with scores/bands, and confirms every mitigated score ≤ original.
2. `python3 -m py_compile risk_calc.py` passes.
3. `risk_matrix.txt` band boundaries match the script constants (edit both if you change them).

## 5. Tasks

1. Add hazard H-06 (e.g. sensor freeze) with S/L + mitigation; re-run.
2. Add a `--strict` flag failing on any residual risk ≥ 10.
3. Draw the matrix with your 5 hazards plotted pre/post mitigation.
4. Write a 5-line ALARP argument for the highest residual risk.
