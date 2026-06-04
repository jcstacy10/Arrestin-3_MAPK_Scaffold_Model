# Experimental Notes & Key Decisions

_This file tracks important experimental decisions, assumptions, and open questions that directly affect model architecture. Update when experimental or literature data change any assumption._

---

## Open Questions That Must Be Experimentally Resolved

### 1. Do p38α and JNK3 compete for the same site on Arr3? (HIGH PRIORITY)

**Why it matters:** This determines the fundamental model topology.
- If **competitive (same site):** use the competitive binding equation in `equilibrium.py`
- If **co-occupancy (different sites):** Arr3 can simultaneously scaffold both pathways; the model becomes a co-complex probability problem

**How to answer:** MST competition assay — fix labeled Arr3 + sub-Kd p38α, titrate in JNK3. If JNK3 displaces p38α, sites are shared.

**Current assumption:** Competitive (shared site). Based on both kinases engaging overlapping Arr3 regions. Update when assay is complete.

---

### 2. Does phospho-p38α lose Arr3 affinity like phospho-JNK3 does?

**Why it matters:** If yes, phosphorylation acts as product release (Arr3 is a catalytic scaffold, not a permanent tether). If no, Arr3 may sequester active p38α.

**How to answer:** MST of Arr3-trunc vs. phospho-p38α.

**Current assumption:** Yes, affinity drops substantially upon phosphorylation. Working assumption by analogy to ppJNK3; must remain flagged until measured directly.

---

### 3. What concentrations should the model use?

**STATUS: RESOLVED FOR PHASE 1 (2026-06-04)**

The model will use **experimentally tractable in vitro concentration ranges**, not bulk whole-cell proteomics values, as the primary simulation regime.

**Decision:**
- Primary simulation mode = **in vitro mode**
- Default Arr3 scan range = **0 to 5–10 µM**
- Bulk PaxDb values are retained only as a **reference layer** for later cellular/localization-aware modeling

**Rationale:**
- Perry et al. (2019, PNAS) used in vitro kinase assays with 5 µM Arr3-trunc and calibrated JARMv1.0 entirely in this regime.
- Their model predicted an optimal Arr3 concentration of ~0.59 µM for maximal JNK3 phosphorylation.
- Bulk HEK293 proteomics places Arr3 at ~13.7 nM, which predicts <1% occupancy for µM-range Kd interactions — experimentally indistinguishable from zero.
- Arrestin localizes strongly upon receptor stimulation, creating scaffold-enriched microenvironments where local concentrations may greatly exceed bulk estimates.
- Recent work (β-arrestin condensates, Nature 2026) further supports local concentration enrichment and signaling compartmentalization as biologically relevant phenomena.

**Interpretation rule for Phase 1:**
Predictions describe **scaffold-enriched in vitro / local microenvironment conditions**, not dilute whole-cell average concentrations.

---

### 4. What fraction of cellular ASK1 is phosphorylated at baseline vs. after oxidative stress?

**Why it matters:** pASK1 and unphosphorylated ASK1 represent very different Arr3-binding states. The ratio pASK1:totalASK1 is a critical model input that changes dynamically with cellular stress.

**Current assumption:** Not yet parameterized. ASK1 is excluded from the first equilibrium model iteration until phospho-state abundances are better constrained.

---

## Bulk Abundance Reference Data (PaxDb)

**Purpose:** Stored for later cellular-reference mode only. NOT the primary Phase 1 modeling concentrations.

**Source:** PaxDb v5.0
**Primary HEK293 dataset:** Geiger et al. 2012, spectral counting, ~22% proteome coverage
**Proxy dataset for absent proteins:** GPM Aug 2014 whole-body, ~97% coverage
**nM conversion:** 200 pg total protein per HEK293T cell, 1 pL cell volume (OpenCell normalization)

**Important annotation correction (2026-06-04):** ENSP00000262519 was previously listed as ASK1 (MAP3K5). That ENSP maps to SETD1A (histone-lysine N-methyltransferase), not MAP3K5. ASK1 now uses the verified STRING ID ENSP00000351908.

| Protein | Gene | HEK-mode ppm | HEK-mode nM | Source | Notes |
|---|---|---:|---:|---|---|
| Arrestin-3 | ARRB2 | 3.21 | 13.7 | HEK293 Geiger 2012 | Directly observed |
| p38α | MAPK14 | 82.10 | 397.6 | GPM proxy | Absent from HEK293 Geiger 2012 |
| JNK3 | MAPK10 | n/d | ~0 | Not detected | Neuronal-restricted; exogenous expression required |
| ASK1 | MAP3K5 | 0.72 | 0.9 | GPM proxy | Corrected; prior value was SETD1A misannotation |
| MKK3 | MAP2K3 | 1.88 | 10.8 | HEK293 Geiger 2012 | Directly observed |
| MKK6 | MAP2K6 | 8.71 | 46.6 | GPM proxy | Absent from HEK293 Geiger 2012 |
| MKK4 | MAP2K4 | 11.00 | 49.7 | GPM proxy | Added for JNK3 cascade completeness |
| MKK7 | MAP2K7 | 5.88 | 24.8 | GPM proxy | Added for JNK3 cascade completeness |

---

## Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-06-04 | Phase 1 model anchored to in vitro concentrations (0–10 µM) | Matches MST/kinase assay regime; experimentally testable |
| 2026-06-04 | Bulk PaxDb values retained as reference layer only | For later local-concentration/cellular model; not current simulation basis |
| 2026-06-04 | MKK4 and MKK7 added to bulk reference table | Needed for JNK3 cascade expansion |
| 2026-06-04 | ASK1 bulk annotation corrected | Previous ENSP mapped to SETD1A, not MAP3K5 |
| 2026-06-04 | MKK3/6 treated as non-binders in current Arr3 binary affinity set | Supported by current MST/pulldown data; ternary scaffold effects remain open |
| 2026-06-04 | p38α + JNK3 assumed competitive for first-pass model | Pending direct MST competition assay |

---

## Proteins In-Hand / In Preparation

| Protein | Status | Notes |
|---|---|---|
| Arr3-trunc (1–393) | Purified ✓ | Used for MST |
| Arr3-FL | Purified ✓ | Used for conformational pulldowns |
| p38α | Purified ✓ | Unphosphorylated |
| ASK1 | Purified ✓ | Phosphorylated and unphosphorylated preparations available |
| MKK3 | Purified ✓ | |
| MKK6 | Purified ✓ | |
| JNK3 | Purified ✓ | |
| MKK4 | In prep | Needed for JNK3 cascade kinase assays |
| MKK7 | In prep | Needed for JNK3 cascade kinase assays |     = ppm × 200 / MW_kDa
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
