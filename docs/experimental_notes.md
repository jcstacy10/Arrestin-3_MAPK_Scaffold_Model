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

**How to answer:** Literature search — Perry et al. 2019 cell line (likely SH-SY5Y neuronal). Search proteomics databases (Human Protein Atlas, ProteomicsDB, CCLE).

**Current assumption:** See `model/parameters.py`. All values are placeholders from Perry et al. estimates.

---

### 4. What fraction of cellular ASK1 is phosphorylated at baseline vs. after oxidative stress?

**Why it matters:** pASK1 (Kd = 0.32 µM) vs. unphospho-ASK1 (Kd = 11 µM) represent very different Arr3-binding partners. The ratio of pASK1:totalASK1 at any moment is a critical model input.

**How to answer:** Literature or direct measurement.

**Current assumption:** Not yet parameterized. ASK1 excluded from Phase 1 equilibrium model.

---

## Decisions Made

| Date | Decision | Rationale |
|---|---|---|
| 2026-06-04 | Phase 1 model: two-competitor (p38a, JNK3), Arr3 excluded | Simplest testable prediction; ASK1 role added in Phase 2 |
| 2026-06-04 | Arr3 cellular range set to 1–5 µM | Perry et al. 2019 estimate; to be confirmed |
| 2026-06-04 | MKK3/6 treated as non-binders | Supported by MST + pulldown; may bind in ternary complex |
| 2026-06-04 | p38a + JNK3 assumed competitive for Phase 1 | Pending MST competition assay |

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
