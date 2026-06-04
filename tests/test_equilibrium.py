"""
test_equilibrium.py

Basic unit tests for the equilibrium calculator.
Run with: python -m pytest tests/
"""

import sys
sys.path.insert(0, '..')

from model.equilibrium import competitive_occupancy


def test_equal_kd_equal_conc():
    """When both ligands have identical Kd and concentration, they split 50/50."""
    frac_A, frac_B, frac_free = competitive_occupancy(
        arr3_total=1.0, kd_A=1.0, conc_A=1.0, kd_B=1.0, conc_B=1.0
    )
    assert abs(frac_A - frac_B) < 1e-10, "Equal competitors should split equally"


def test_fractions_sum_to_one():
    """Fractional occupancies must always sum to 1."""
    frac_A, frac_B, frac_free = competitive_occupancy(
        arr3_total=1.0, kd_A=2.6, conc_A=0.5, kd_B=1.1, conc_B=0.5
    )
    assert abs(frac_A + frac_B + frac_free - 1.0) < 1e-10


def test_higher_affinity_wins():
    """Lower Kd (higher affinity) should produce higher fractional occupancy."""
    frac_A, frac_B, _ = competitive_occupancy(
        arr3_total=1.0,
        kd_A=1.1, conc_A=0.5,   # JNK3: tighter
        kd_B=2.6, conc_B=0.5    # p38a: weaker
    )
    assert frac_A > frac_B, "Higher affinity ligand should occupy more Arr3"


def test_no_binding_ligand():
    """A ligand at zero concentration should have zero occupancy."""
    frac_A, frac_B, frac_free = competitive_occupancy(
        arr3_total=1.0, kd_A=2.6, conc_A=0.0, kd_B=1.1, conc_B=0.5
    )
    assert abs(frac_A) < 1e-10


if __name__ == '__main__':
    test_equal_kd_equal_conc()
    test_fractions_sum_to_one()
    test_higher_affinity_wins()
    test_no_binding_ligand()
    print("All tests passed.")
