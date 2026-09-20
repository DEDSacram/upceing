# Labs

Hands-on labs for ITN coursework. Every lab follows the same contract
(mirroring `upce/NNPDA/lab-01-jdbc`): a `README.md` with
**1. Theory, 2. Project layout, 3. Run, 4. Verify, 5. Tasks**
plus runnable starter code with TODOs for students.

## Map

| Subject | Coursework | Labs | Stack |
|---------|-----------|------|-------|
| KAM/NNTEI | Theoretical Informatics | `labs/NNTEI/` (7) | Python 3 stdlib |
| KST/NAPIS | Arch. & Design of Inf. Systems | `labs/NAPIS/` (5) | Python + ArchiMate/BPMN XML |
| KST/NNDSA | Data Structures and Algorithms | `labs/NNDSA/` (8) | Python 3 stdlib |
| KST/NNPIA | Programming of Internet Applications | `labs/NNPIA/` (8) | Java 17 / Spring Boot 3 + Node + React |
| KAM/NNTEF | Queueing Theory | `labs/NNTEF/` (6) | Python 3 stdlib |
| KIT/NNOS1 | Operating Systems 1 | `labs/NNOS1/` (8) | C / POSIX, gcc |
| KST/NNPDA | Programming Database Applications | `upce/NNPDA/` (13) — pre-existing | Java 17 / Maven / Docker |
| KST/NNPRO | Year's Project | — (project templates live in coursework) | — |
| KIT/NNDSK | Data Warehousing | `labs/NNDSK/` (6) | SQL / Postgres + Python stdlib |
| KST/NNOS2 | Operating Systems 2 | `labs/NNOS2/` (6) | PowerShell / Windows (+ Linux counterparts) |
| KST/NNBSW | Software Safety and Reliability | `labs/NNBSW/` (5) | Python + Ada/SPARK |
| KST/NNTMS | Modeling and Simulation | `labs/NNTMS/` (6) | Python 3 stdlib |
| KST/NNPG3 | 3D Graphics and Graphic API | `labs/NNPG3/` (5) | Python CPU + GLSL sources |
| KST/NNTPS | Modern Trends of Computer Networks | `upce/NNTPS/` (labs + programming + projects) — pre-existing | Mininet / RYU / Floodlight |

Subjects without labs (no meaningful runnable lab; theory covered in coursework):
KST/NNDIP (Diploma Thesis), KST/NNDIS (Diploma Seminar), State Final Exam.

## Prerequisites by stack

- **Python labs:** `python3` only (stdlib, incl. `sqlite3`). Verify with `python3 -m py_compile <file>.py`, then run it.
- **C labs (NNOS1):** `gcc` + `make`. Each lab has a `Makefile`; `make && ./main`.
- **Java labs (NNPIA):** JDK 17 + Maven 3.9+. `mvn test` (H2-backed, no Docker needed); Docker only for the Postgres-backed runs.
- **JS labs (NNPIA):** Node 18+. `node --check` + `node demo.js`.
- **SQL labs (NNDSK):** Docker + Compose for Postgres; Python parts run on stdlib `sqlite3`.
- **Windows labs (NNOS2):** `.ps1`/`.reg` files run on student Windows machines (PowerShell 5.1); each lab ships a Linux runnable counterpart.
- **SPARK lab (NNBSW):** GNAT/SPARK tools for full proof; Python counterparts run anywhere.
- **GLSL (NNPG3):** sources provided + CPU reference implementations in Python (no GPU needed).

## Lab READMEs

Each lab README ends with **Tasks** — the graded extension work.
Starters contain `TODO` markers; self-check asserts print `ALL SELF-CHECKS PASSED`
where applicable.
