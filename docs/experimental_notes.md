# Experimental Notes & Key Decisions

_This file tracks important experimental decisions, assumptions, and open questions that directly affect model architecture. Update when experimental or literature data change any assumption._

---

## Open Questions That Must Be Experimentally Resolved

### 1. Do p38α and JNK3 compete for the same site on Arr3? (HIGH PRIORITY)

**Why it matters:** This determines the fundamental model topology.
- If **competitive (same site):** use the competitive binding equation in `equilibrium.py`
- If **co-occupancy (different sites):** Arr3 can simultaneously scaffold both pathways; the model becomes a co-complex probability problem

**How to answer:** MST competition assay — fix labeled Arr3 + sub-Kd p38a, titrate in JNK3. If JNK3 displaces p38a, sites are shared.

**Current assumption:** Competitive (shared site). Based on: both kinases appear to contact the lariat loop region of Arr3. Update when assay is complete.

---

### 2. Does phospho-p38α lose Arr3 affinity like phospho-JNK3 does?

**Why it matters:** If yes, phosphorylation acts as product release (Arr3 is a catalytic scaffold, not a permanent tether). If no, Arr3 may sequester active p38α.

**How to answer:** MST of Arr3-trunc vs. phospho-p38α

**Current assumption:** Yes, affinity drops to >10 µM upon phosphorylation. Justified by analogy to ppJNK3 (Perry et al. 2019). Flag as assumption in all model outputs.

---

### 3. What are the cellular concentrations of all proteins in the target cell line?

**Why it matters:** Equilibrium partitioning is concentration-dependent. Using wrong concentrations can flip model predictions.

**STATUS: PARTIALLY RESOLVED (2026-06-04)**  
PaxDb v5.0 data retrieved for HEK293 mode. See `data/cellular_concentrations.csv`.  
Open sub-question: p38α and MKK6 values sourced from GPM whole-body proxy — verify with HEK293-specific proteomics if available. JNK3 absent from HEK293; exogenous expression required.

**Current assumption:** See `model/parameters.py` and `data/cellular_concentrations.csv`.

---

### 4. What fraction of cellular ASK1 is phosphorylated at baseline vs. after oxidative stress?

**Why it matters:** pASK1 (Kd = 0.32 µM) vs. unphospho-ASK1 (Kd = 11 µM) represent very different Arr3-binding partners. The ratio of pASK1:totalASK1 at any moment is a critical model input.

**How to answer:** Literature or direct measurement.

**Current assumption:** Not yet parameterized. ASK1 excluded from Phase 1 equilibrium model.

---

## Cellular Concentration Data (HEK293 Mode)

**Source:** PaxDb v5.0 (pax-db.org, accessed 2026-06-04)  
**Primary dataset:** Geiger et al. 2012, MCP — HEK293, spectral counting, 22% proteome coverage  
**Proxy dataset:** GPM Aug 2014 — whole-body human, spectral counting, 97% coverage (used where HEK293 data absent)  
**Full data file:** `data/cellular_concentrations.csv`

### Conversion formula: ppm → nM

PaxDb ppm values represent (copies of protein X) / (total protein copies) × 10⁶.  
To convert to intracellular molarity:

```
[nM] = ppm × (total_protein_g_per_cell / MW_g_per_mol) / cell_vol_L × 10⁹
     = ppm × 200 / MW_kDa
```

Assumptions (from Cho et al. 2022 OpenCell; Wisniewski et al. 2014 Cell Systems):
- Total protein per HEK293 cell: **200 pg**
- Mean cell volume: **1 pL** (= 1 × 10⁻¹² L)

### HEK293 abundance table

| Protein | Gene | UniProt | MW (kDa) | ppm | nM | Source | Flag |
|---|---|---|---|---|---|---|---|
| Arrestin-3 | ARRB2 | P32121 | 46.9 | 3.21 | 13.7 | HEK293 Geiger 2012 | ✓ direct |
| p38α | MAPK14 | Q16539 | 41.3 | 82.10 | 397.6 | GPM 2014 (proxy) | ⚠ verify |
| JNK3 | MAPK10 | P53779 | 52.6 | n/d | ~0 | not detected | ⚠ neuronal; exog. expression |
| ASK1 | MAP3K5 | Q99683 | 154.8 | 6.17 | 8.0 | HEK293 Geiger 2012 | ✓ direct |
| MKK3 | MAP2K3 | P46734 | 34.7 | 1.88 | 10.8 | HEK293 Geiger 2012 | ✓ direct |
| MKK6 | MAP2K6 | P52564 | 37.4 | 8.71 | 46.6 | GPM 2014 (proxy) | ⚠ verify |

**Notes:**
- p38α (82 ppm from GPM) is plausibly high — p38α is among the most abundant MAPK family members across tissues. Flag for confirmation in a dedicated HEK293 proteomics dataset (e.g., CCLE, ProteomicsDB).
- JNK3 is neuronal-restricted and absent from non-neuronal proteomics including brain bulk datasets. For neuronal-mode simulations, a separate concentration file will be needed.
- Brain integrated dataset values are also stored in `data/cellular_concentrations.csv` for future neuronal-mode parameterization.

---

## Decisions Made

| Date | Decision | Rationale |
|---|---|---|
| 2026-06-04 | Phase 1 model: two-competitor (p38a, JNK3), Arr3 excluded | Simplest testable prediction; ASK1 role added in Phase 2 |
| 2026-06-04 | Arr3 cellular range set to 1–5 µM | Perry et al. 2019 estimate; to be confirmed |
| 2026-06-04 | MKK3/6 treated as non-binders | Supported by MST + pulldown; may bind in ternary complex |
| 2026-06-04 | p38a + JNK3 assumed competitive for Phase 1 | Pending MST competition assay |
| 2026-06-04 | HEK293 concentrations sourced from PaxDb v5.0 | Geiger 2012 (primary) + GPM 2014 (gap-filling proxy) |

---

## Proteins In-Hand / In Prep

| Protein | Status | Notes |
|---|---|---|
| Arr3-trunc (1-393) | Purified ✓ | Used for all MST data |
| Arr3-FL | Purified ✓ | Used for conformational pulldowns |
| p38α | Purified ✓ | Unphosphorylated |
| ASK1 | Purified ✓ | Phosphorylated (active) |
| ASK1 | Purified ✓ | Unphosphorylated |
| MKK3 | Purified ✓ | |
| MKK6 | Purified ✓ | |
| JNK3 | Purified ✓ | |
| MKK4 | In expression | Needed for in vitro kinase assay |
| MKK7 | In expression | Needed for in vitro kinase assay |
