#!/usr/bin/env python3
"""Calculate gas-phase standard Gibbs energy for ethanol combustion.

Reaction: C2H5OH + 3 O2 -> 2 CO2 + 3 H2O

This is a raw PySCF workflow because the available MAESTRO tasks do not
perform multi-species reaction thermochemistry.  It uses B3LYP/def2-SVP,
298.15 K, and 1 atm.  The result is for ideal gases; it is not the standard
free energy of combustion of liquid ethanol or liquid water.
"""

from __future__ import annotations

import json

from pyscf import dft
from pyscf.geomopt.geometric_solver import optimize
from pyscf.hessian import thermo

TEMPERATURE_K = 298.15
PRESSURE_PA = 101325.0
HARTREE_TO_KJ_MOL = 2625.49962
METHOD = "B3LYP/def2-SVP"

# Reasonable starting geometries in angstrom. O2 is explicitly triplet.
SPECIES = {
    "ethanol": {
        "atom": """C  0.000  0.000  0.000
C  1.510  0.000  0.000
O  2.130  1.190  0.000
H  2.990  1.090  0.000
H -0.390  1.030  0.000
H -0.390 -0.510  0.890
H -0.390 -0.510 -0.890
H  1.900 -0.510  0.890
H  1.900 -0.510 -0.890""",
        "spin": 0,
    },
    "oxygen": {"atom": "O 0 0 -0.60; O 0 0 0.60", "spin": 2},
    "carbon_dioxide": {"atom": "O 0 0 -1.16; C 0 0 0; O 0 0 1.16", "spin": 0},
    "water": {"atom": "O 0 0 0; H 0.758 0 0.504; H -0.758 0 0.504", "spin": 0},
}


def gibbs_energy(name: str, spec: dict[str, object]) -> float:
    """Optimize a molecule, run a Hessian, and return G in Hartree."""
    from pyscf import gto

    mol = gto.M(
        atom=spec["atom"],
        basis="def2-svp",
        charge=0,
        spin=spec["spin"],
        unit="Angstrom",
        verbose=4,
    )
    mf_cls = dft.UKS if mol.spin else dft.RKS
    mf = mf_cls(mol)
    mf.xc = "b3lyp"
    mf.conv_tol = 1e-9
    mf.kernel()
    if not mf.converged:
        raise RuntimeError(f"SCF did not converge for {name} before optimization")

    optimized = optimize(mf)
    mf = mf_cls(optimized)
    mf.xc = "b3lyp"
    mf.conv_tol = 1e-9
    mf.kernel()
    if not mf.converged:
        raise RuntimeError(f"SCF did not converge for optimized {name}")

    hessian = mf.Hessian().kernel()
    frequencies = thermo.harmonic_analysis(optimized, hessian)
    thermo_data = thermo.thermo(
        mf,
        frequencies["freq_au"],
        temperature=TEMPERATURE_K,
        pressure=PRESSURE_PA,
    )
    return float(thermo_data["G_tot"][0])


def main() -> None:
    gibbs_hartree = {name: gibbs_energy(name, spec) for name, spec in SPECIES.items()}
    delta_g_hartree = (
        2 * gibbs_hartree["carbon_dioxide"]
        + 3 * gibbs_hartree["water"]
        - gibbs_hartree["ethanol"]
        - 3 * gibbs_hartree["oxygen"]
    )
    result = {
        "method": METHOD,
        "temperature_K": TEMPERATURE_K,
        "pressure_Pa": PRESSURE_PA,
        "phase": "ideal gas",
        "reaction": "C2H5OH + 3 O2 -> 2 CO2 + 3 H2O",
        "gibbs_energies_hartree": gibbs_hartree,
        "delta_g_hartree": delta_g_hartree,
        "delta_g_kj_mol": delta_g_hartree * HARTREE_TO_KJ_MOL,
    }
    with open("ethanol_combustion_gibbs_results.json", "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
