"""
parameters.py

Cellular concentration parameters for the JARM model.

All concentrations are in micromolar (uM). Values are initial estimates
from literature (Perry et al. 2019 neuronal cell line estimates) and will
be updated as cell-line-specific proteomics data are identified.

Each parameter includes a source tag and a flag indicating whether it
has been experimentally confirmed for the target cell line.
"""

from dataclasses import dataclass


@dataclass
class CellularParameter:
    protein: str
    concentration_uM: float
    source: str
    confirmed_in_target_cell_line: bool = False
    notes: str = ''


# ---------------------------------------------------------------------------
# Initial concentration estimates
# Source: Perry et al. 2019 supplemental; neuronal cell line estimates.
# TODO: Replace with proteomics estimates from same cell line used in
#       Perry et al. (likely SH-SY5Y or similar neuronal line).
# ---------------------------------------------------------------------------

CELLULAR_PARAMETERS = [
    CellularParameter(
        protein='Arr3',
        concentration_uM=1.0,   # Range: 1-5 uM; lower estimate used as default
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='CRITICAL: must confirm in target neuronal cell line via literature search'
    ),
    CellularParameter(
        protein='p38a',
        concentration_uM=0.5,
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='Placeholder; ubiquitously expressed at relatively high levels'
    ),
    CellularParameter(
        protein='JNK3',
        concentration_uM=0.5,
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='Placeholder; JNK3 is neuronally enriched'
    ),
    CellularParameter(
        protein='ASK1',
        concentration_uM=0.2,
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='Placeholder'
    ),
    CellularParameter(
        protein='MKK3',
        concentration_uM=0.3,
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='Placeholder'
    ),
    CellularParameter(
        protein='MKK6',
        concentration_uM=0.3,
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='Placeholder'
    ),
    CellularParameter(
        protein='MKK4',
        concentration_uM=0.3,
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='Placeholder'
    ),
    CellularParameter(
        protein='MKK7',
        concentration_uM=0.3,
        source='Perry_et_al_2019_estimate',
        confirmed_in_target_cell_line=False,
        notes='Placeholder'
    ),
]

# Quick-access dictionary
PARAMS = {p.protein: p.concentration_uM for p in CELLULAR_PARAMETERS}


if __name__ == '__main__':
    print("=== JARM Cellular Parameters ===")
    for p in CELLULAR_PARAMETERS:
        confirmed = '✓' if p.confirmed_in_target_cell_line else '? (unconfirmed)'
        print(f"  {p.protein:10s}  {p.concentration_uM:.2f} uM  [{confirmed}]  {p.notes}")
