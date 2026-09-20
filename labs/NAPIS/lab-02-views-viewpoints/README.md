# Lab 02 — Views & Viewpoints

Stakeholder-driven views: pick the right viewpoint per concern, fill the matrix, map stakeholders.

## 1. Theory

- **Stakeholder** = anyone with a concern (owner, user, ops, security, auditor). **Concern** = an interest (cost, risk, usability, compliance).
- **Viewpoint** = a template for a view: purpose, stakeholders, concerns, notation (e.g. ArchiMate layered, BPMN, UML deployment, C4).
- **View** = one concrete diagram/description answering specific concerns for specific stakeholders.
- ISO/IEC/IEEE 42010: architecture description = set of views governed by viewpoints. Rule of thumb: one concern → one view; never one mega-diagram.

## 2. Project layout

```
lab-02-views-viewpoints/
  README.md
  viewpoints.yaml      # viewpoint catalogue + view/viewpoint/stakeholder matrix (starter, fill in TODOs)
  stakeholders.yaml    # stakeholder register starter
```

## 3. Run

```bash
cd labs/NAPIS/lab-02-views-viewpoints
python3 -c "import yaml" 2>/dev/null || echo "(no PyYAML — use python3 check below)"
python3 check.py
```

## 4. Verify

1. `python3 check.py` reports matrix completeness (no TODO left, every concern covered by ≥1 view, every view has an owner).
2. `stakeholders.yaml` lists ≥5 stakeholders each with influence/interest and ≥1 concern.
3. Peer check: can a newcomer answer "which view shows deployment cost?" from the matrix alone?

## 5. Tasks

1. Fill all `TODO` cells in `viewpoints.yaml` for the Shop case (add 2 views: security + data).
2. Add a stakeholder (e.g. Data Protection Officer) with concerns; link to a view.
3. Propose one new viewpoint (purpose, notation, meta-model) and justify it in 5 lines in this README.
4. Detect conflicts: mark two stakeholders whose concerns clash and propose a trade-off decision record.
