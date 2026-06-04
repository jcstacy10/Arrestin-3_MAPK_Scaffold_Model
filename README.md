# Arrestin-3 MAPK Scaffold Model (JARM)

Computational model of arrestin-3 scaffold-dependent MAPK cascade partitioning. Uses experimental binding affinities (MST) and in vitro kinase activity data to predict equilibrium distribution of arrestin-3 complexes across the p38α and JNK3 signaling cascades.

**Lead:** J.C. Stacy, Gurevich Lab, Vanderbilt University Department of Biochemistry

---

## Project Goal

Given a defined set of cellular parameters (protein concentrations, phosphorylation states), predict how arrestin-3 partitions its scaffolding activity between the p38α MAPK cascade (ASK1–MKK3/6–p38α) and the JNK3 cascade (ASK1–MKK4/7–JNK3). The model uses experimentally measured binary binding affinities and in vitro kinase activation data as its training foundation.

## Core Question

> When arrestin-3 is present, how much of the p38α cascade does it scaffold for activation versus how much of the JNK3 cascade?

---

## Repository Structure

```
├── data/
│   ├── binding_affinities.csv     # All Kd values (experimental + literature)
│   └── kinase_assay/              # In vitro phosphorylation time-course data (future)
├── model/
│   ├── binding_data.py            # Structured Kd data as Python objects
│   ├── equilibrium.py             # Competitive binding equilibrium calculator
│   └── parameters.py              # Cellular concentration parameters
├── notebooks/
│   └── 01_equilibrium_explorer.ipynb  # Interactive model exploration (future)
├── tests/
│   └── test_equilibrium.py        # Unit tests for model functions
├── docs/
│   └── experimental_notes.md      # Key experimental decisions and assumptions
├── .gitignore
└── README.md
```

---

## Current Data Status

| Interaction | State | Kd (µM) | Method | Source |
|---|---|---|---|---|
| Arr3-trunc (1-393) + p38α | Unphosphorylated | 2.6 ± 1.0 | MST | Stacy et al. (in prep) |
| Arr3-trunc (1-393) + ASK1 | Phosphorylated | 0.32 | MST | Stacy et al. (in prep) |
| Arr3-trunc (1-393) + ASK1 | Unphosphorylated | 11.0 ± 2.0 | MST | Stacy et al. (in prep) |
| Arr3-trunc (1-393) + MKK3 | Unphosphorylated | No binding detected | MST | Stacy et al. (in prep) |
| Arr3-trunc (1-393) + MKK6 | Unphosphorylated | No binding detected | MST | Stacy et al. (in prep) |
| Arr3-trunc (1-393) + JNK3 | Unphosphorylated | 1.1 | MST | Perry et al. 2019 |
| Arr3-trunc (1-393) + JNK3 | Doubly phosphorylated | ~15 | MST | Perry et al. 2019 |

> **Note:** ASK1 affinities in manuscript draft are placeholders — values above reflect corrected experimental data.

---

## Model Development Phases

- [x] Phase 0: Experimental data collection (MST affinities)
- [ ] Phase 1: Equilibrium binding calculator (competitive, two-pathway)
- [ ] Phase 2: In vitro kinase assay training data (pp38α vs. ppJNK3 ± Arr3)
- [ ] Phase 3: MST competition assay data (JNK3 vs. p38α competing for Arr3)
- [ ] Phase 4: ODE-based kinetic model
- [ ] Phase 5: Cellular concentration parameterization
- [ ] Phase 6: ML-assisted pattern recognition layer

---

## Key Assumptions (as of project start)

1. Phosphorylated p38α and phosphorylated JNK3 both lose significant Arr3 affinity (Kd > 10 µM), analogous to ppJNK3 data from Perry et al. 2019. Assumed until measured directly.
2. MKK3 and MKK6 enter the scaffold only via bridge contacts through p38α or ASK1, not through direct stable binary interaction with Arr3.
3. Cellular Arr3 concentration range: 1–5 µM (to be confirmed by literature search in neuronal cell lines).
4. Binding sites for p38α and JNK3 on Arr3 are assumed independent until competition MST assay is complete.

---

## Dependencies

```
python >= 3.10
numpy
scipy
matplotlib
pandas
```

Install with: `pip install numpy scipy matplotlib pandas`
