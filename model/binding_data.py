"""
binding_data.py

Structured representation of all experimentally measured and literature-sourced
binding affinities for the Arrestin-3 MAPK Scaffold Model (JARM).

Kd values are in micromolar (uM).
None = not detected / above assay range (treated as no binding in model).
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BindingPair:
    """Represents a single binary binding interaction."""
    protein_a: str           # e.g. 'Arr3-trunc'
    state_a: str             # e.g. 'basal', 'IP6_activated'
    protein_b: str           # e.g. 'p38a'
    state_b: str             # e.g. 'unphosphorylated', 'phosphorylated'
    kd_uM: Optional[float]   # Dissociation constant in micromolar; None if not detected
    kd_error_uM: Optional[float] = None
    method: str = 'MST'
    source: str = ''
    notes: str = ''

    def __repr__(self):
        kd_str = f"{self.kd_uM} uM" if self.kd_uM is not None else "not detected"
        return (f"<BindingPair {self.protein_a}({self.state_a}) + "
                f"{self.protein_b}({self.state_b}): Kd = {kd_str}>")


# ---------------------------------------------------------------------------
# Experimental affinities — Stacy et al. (in preparation)
# All measured with Arr3 truncated at residue 393 (C-tail removed, basal-like
# but with exposed effector surfaces) unless otherwise noted.
# ---------------------------------------------------------------------------

STACY_DATA = [
    BindingPair(
        protein_a='Arr3-trunc', state_a='basal',
        protein_b='p38a', state_b='unphosphorylated',
        kd_uM=2.6, kd_error_uM=1.0,
        method='MST', source='Stacy_et_al_in_prep',
        notes='Primary scaffold target; C-lobe of p38a contacts lariat loop of Arr3'
    ),
    BindingPair(
        protein_a='Arr3-trunc', state_a='basal',
        protein_b='ASK1', state_b='phosphorylated',
        kd_uM=0.32, kd_error_uM=None,
        method='MST', source='Stacy_et_al_in_prep',
        notes='Tight binding; pASK1 favors basal Arr3 conformation'
    ),
    BindingPair(
        protein_a='Arr3-trunc', state_a='basal',
        protein_b='ASK1', state_b='unphosphorylated',
        kd_uM=11.0, kd_error_uM=2.0,
        method='MST', source='Stacy_et_al_in_prep',
        notes='Weak binding; unphospho-ASK1 has low affinity for Arr3'
    ),
    BindingPair(
        protein_a='Arr3-trunc', state_a='basal',
        protein_b='MKK3', state_b='unphosphorylated',
        kd_uM=None, kd_error_uM=None,
        method='MST', source='Stacy_et_al_in_prep',
        notes='No detectable binding; consistent with pulldown result (<2% retention)'
    ),
    BindingPair(
        protein_a='Arr3-trunc', state_a='basal',
        protein_b='MKK6', state_b='unphosphorylated',
        kd_uM=None, kd_error_uM=None,
        method='MST', source='Stacy_et_al_in_prep',
        notes='No detectable binding; consistent with pulldown result (<2% retention)'
    ),
]

# ---------------------------------------------------------------------------
# Literature affinities — Perry et al. 2019 (JNK3 cascade)
# ---------------------------------------------------------------------------

PERRY_DATA = [
    BindingPair(
        protein_a='Arr3-trunc', state_a='basal',
        protein_b='JNK3', state_b='unphosphorylated',
        kd_uM=1.1, kd_error_uM=None,
        method='MST', source='Perry_et_al_2019',
        notes='Primary JNK3 cascade scaffold target'
    ),
    BindingPair(
        protein_a='Arr3-trunc', state_a='basal',
        protein_b='JNK3', state_b='doubly_phosphorylated',
        kd_uM=15.0, kd_error_uM=None,
        method='MST', source='Perry_et_al_2019',
        notes='Approximate; phosphorylation dramatically reduces Arr3 affinity'
    ),
]

# ---------------------------------------------------------------------------
# Combined registry
# ---------------------------------------------------------------------------

ALL_BINDING_DATA = STACY_DATA + PERRY_DATA


def get_kd(protein_b: str, state_b: str, state_a: str = 'basal') -> Optional[float]:
    """
    Convenience lookup: return Kd (uM) for Arr3 + protein_b in given states.
    Returns None if not detected or not measured.
    """
    for pair in ALL_BINDING_DATA:
        if (pair.protein_b == protein_b and
                pair.state_b == state_b and
                pair.state_a == state_a):
            return pair.kd_uM
    return None


if __name__ == '__main__':
    print("=== JARM Binding Affinity Registry ===")
    for pair in ALL_BINDING_DATA:
        print(pair)
