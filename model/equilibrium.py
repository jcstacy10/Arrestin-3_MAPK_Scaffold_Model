"""
equilibrium.py

Competitive binding equilibrium calculator for the JARM model.

Core question: Given concentrations of Arr3, p38a, and JNK3 (and their
measured Kd values), what fraction of Arr3 is occupied by each kinase
at equilibrium?

This is the simplest possible model — one Arr3 binding site, two
competing ligands. It does NOT yet account for:
  - ASK1 as a third competitor
  - Conformational switching of Arr3
  - Cooperative effects
  - Kinetics (phosphorylation rates)
Those layers come later. This is the foundation.

Biology note:
  Assumption used here: p38a and JNK3 compete for the SAME site on Arr3.
  This will be validated by the MST competition assay (in progress).
  If they bind at DIFFERENT sites (can co-occupy), the model changes
  significantly — see notes in docs/experimental_notes.md.
"""

import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from typing import Optional


def competitive_occupancy(
    arr3_total: float,
    kd_A: float,
    conc_A: float,
    kd_B: float,
    conc_B: float,
) -> tuple[float, float, float]:
    """
    Calculate fractional occupancy of Arr3 by two competing ligands (A and B)
    assuming a single shared binding site (competitive model).

    Uses the exact solution to the competitive binding equilibrium:
        [Arr3_free] + [Arr3:A] + [Arr3:B] = [Arr3_total]
        [Arr3:A] = [Arr3_free] * [A_free] / Kd_A
        [Arr3:B] = [Arr3_free] * [B_free] / Kd_B

    For simplicity, assumes [A_free] ~ [A_total] and [B_free] ~ [B_total]
    (valid when Kd >> [Arr3], i.e., weak binding regime or excess ligand).
    This approximation will be replaced with the full cubic solution in Phase 2.

    Parameters
    ----------
    arr3_total : float   Total Arr3 concentration (uM)
    kd_A       : float   Kd for ligand A (uM), e.g. p38a
    conc_A     : float   Total concentration of ligand A (uM)
    kd_B       : float   Kd for ligand B (uM), e.g. JNK3
    conc_B     : float   Total concentration of ligand B (uM)

    Returns
    -------
    (frac_A, frac_B, frac_free) : fractional occupancies, sum to 1.0
    """
    # Fractional occupancy in competitive model (simplified)
    # theta_A = (conc_A / kd_A) / (1 + conc_A/kd_A + conc_B/kd_B)
    denom = 1.0 + (conc_A / kd_A) + (conc_B / kd_B)
    frac_A = (conc_A / kd_A) / denom
    frac_B = (conc_B / kd_B) / denom
    frac_free = 1.0 / denom
    return frac_A, frac_B, frac_free


def scan_arr3_concentration(
    kd_p38a: float = 2.6,
    kd_jnk3: float = 1.1,
    conc_p38a: float = 0.5,
    conc_jnk3: float = 0.5,
    arr3_range: tuple = (0.01, 10.0),
    n_points: int = 200,
) -> dict:
    """
    Scan across a range of Arr3 concentrations and calculate partitioning
    between p38a and JNK3 at each concentration.

    This generates the model's central prediction: how does Arr3 partition
    between the two pathways as its concentration changes?

    In the simplified competitive model, fractional occupancy does not depend
    on Arr3 concentration (only on ligand concentrations and Kds). The
    absolute amounts bound scale with [Arr3]. This function returns both.

    Returns dict with keys: arr3_conc, frac_p38a, frac_jnk3, frac_free,
                            abs_p38a_bound, abs_jnk3_bound
    """
    arr3_concs = np.linspace(arr3_range[0], arr3_range[1], n_points)
    results = {'arr3_conc': arr3_concs,
               'frac_p38a': [], 'frac_jnk3': [], 'frac_free': [],
               'abs_p38a_bound': [], 'abs_jnk3_bound': []}

    for arr3 in arr3_concs:
        frac_p38a, frac_jnk3, frac_free = competitive_occupancy(
            arr3, kd_p38a, conc_p38a, kd_jnk3, conc_jnk3
        )
        results['frac_p38a'].append(frac_p38a)
        results['frac_jnk3'].append(frac_jnk3)
        results['frac_free'].append(frac_free)
        results['abs_p38a_bound'].append(frac_p38a * arr3)
        results['abs_jnk3_bound'].append(frac_jnk3 * arr3)

    for key in results:
        if key != 'arr3_conc':
            results[key] = np.array(results[key])
    return results


def plot_partitioning(results: dict, save_path: Optional[str] = None):
    """
    Plot Arr3 partitioning between p38a and JNK3 across Arr3 concentrations.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Arr3 Scaffold Partitioning: p38\u03b1 vs. JNK3\n'
                 '(Competitive equilibrium model, Phase 1)', fontsize=13)

    # Panel 1: Fractional occupancy
    ax1.plot(results['arr3_conc'], results['frac_p38a'] * 100,
             color='#2E86AB', lw=2.5, label='p38\u03b1')
    ax1.plot(results['arr3_conc'], results['frac_jnk3'] * 100,
             color='#E84855', lw=2.5, label='JNK3')
    ax1.plot(results['arr3_conc'], results['frac_free'] * 100,
             color='#A8A8A8', lw=1.5, ls='--', label='Arr3 free')
    ax1.set_xlabel('[Arr3] (\u03bcM)', fontsize=11)
    ax1.set_ylabel('Arr3 Occupancy (%)', fontsize=11)
    ax1.set_title('Fractional Occupancy', fontsize=11)
    ax1.legend()
    ax1.set_ylim(0, 100)
    ax1.axvspan(1.0, 5.0, alpha=0.07, color='green', label='Cellular [Arr3] range')

    # Panel 2: Absolute amounts bound
    ax2.plot(results['arr3_conc'], results['abs_p38a_bound'],
             color='#2E86AB', lw=2.5, label='[Arr3:p38\u03b1]')
    ax2.plot(results['arr3_conc'], results['abs_jnk3_bound'],
             color='#E84855', lw=2.5, label='[Arr3:JNK3]')
    ax2.set_xlabel('[Arr3] (\u03bcM)', fontsize=11)
    ax2.set_ylabel('Concentration bound (\u03bcM)', fontsize=11)
    ax2.set_title('Absolute Amounts Bound', fontsize=11)
    ax2.legend()
    ax2.axvspan(1.0, 5.0, alpha=0.07, color='green')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    # Run with current best Kd estimates
    print("=== JARM Phase 1: Competitive Equilibrium Prediction ===")
    print("  Kd(Arr3-p38a)  = 2.6 uM  [Stacy et al., in prep]")
    print("  Kd(Arr3-JNK3)  = 1.1 uM  [Perry et al. 2019]")
    print("  [p38a]_cell    = 0.5 uM  (placeholder)")
    print("  [JNK3]_cell    = 0.5 uM  (placeholder)")
    print()

    # Single-point prediction at 1 uM Arr3 (lower cellular estimate)
    frac_p38a, frac_jnk3, frac_free = competitive_occupancy(
        arr3_total=1.0,
        kd_A=2.6, conc_A=0.5,
        kd_B=1.1, conc_B=0.5
    )
    print(f"  At [Arr3] = 1.0 uM:")
    print(f"    Arr3 occupied by p38a : {frac_p38a*100:.1f}%")
    print(f"    Arr3 occupied by JNK3 : {frac_jnk3*100:.1f}%")
    print(f"    Arr3 free             : {frac_free*100:.1f}%")
    print(f"    p38a/JNK3 ratio       : {frac_p38a/frac_jnk3:.2f}")
    print()

    results = scan_arr3_concentration()
    plot_partitioning(results)
