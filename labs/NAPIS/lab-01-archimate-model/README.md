# Lab 01 — ArchiMate Model (Open Exchange)

Small ArchiMate 3.x model with Business/Application/Technology layers, validated by a stdlib XML check.

## 1. Theory

- **Enterprise architecture (EA)** aligns business goals, processes, applications, and infrastructure. TOGAF ADM is the process; **ArchiMate** is the modeling language.
- **ArchiMate layers:** Business (actors, processes, services), Application (components, interfaces), Technology (nodes, networks), plus Motivation and Implementation extensions.
- **Open Exchange Format** is the XML interchange standard for ArchiMate tools (Archi, etc.). Elements live under `<elements>`, relationships under `<relationships>`, diagrams under `<views>`.
- **Validation idea:** well-formed XML + required element/relationship integrity (every relationship references existing elements) + every element used in at least one view (warning, not error).

## 2. Project layout

```
lab-01-archimate-model/
  README.md
  model.xml      # ArchiMate Open Exchange starter (order-management example)
  validate.py    # stdlib xml check: parse + referential integrity
```

## 3. Run

```bash
cd labs/NAPIS/lab-01-archimate-model
python3 validate.py model.xml
python3 validate.py --strict model.xml
```

## 4. Verify

1. `python3 validate.py model.xml` prints `OK: N elements, M relationships, K views` and exits 0.
2. Break it on purpose: duplicate an `id` or point a relationship at a missing `source` — validator must exit non-zero with a clear error.
3. Open `model.xml` in Archi (File → Import → Open Exchange) — diagram renders without errors.

## 5. Tasks

1. Add a `Technology` node (e.g. `PostgreSQL Server`) + `Realization` relationship from the DB component; re-validate.
2. Add a second view (e.g. deployment view) referencing the new node.
3. Extend `validate.py` to check ArchiMate relationship legality (e.g. `Serving` may not connect two Business Actors) — start with an allow-list of 3 types.
4. Export a PNG of the view from Archi and compare element counts with the validator output.
