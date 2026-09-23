---
task: unsupported
engine: none
error_class: input_error
failure_class: setup_error
outcome: workaround
wall_time_s: 183
n_atoms: 9
method: B3LYP
basis: def2-SVP
cores: 12
mode: local
---
Symptom: The ethanol geometry optimization converged, then PySCF thermochemistry raised AttributeError: 'dict' object has no attribute 'real'.
Attempts: Inspected the installed PySCF thermo implementation. Its harmonic_analysis function returns a dictionary, while thermo expects the freq_au member; G_tot is also returned as a value-and-unit pair.
Result: Updated the raw workflow to pass frequencies['freq_au'] and extract G_tot[0]; rerun pending.
Context: Gas-phase standard-state ethanol combustion workflow at 298.15 K and 1 atm. The MAESTRO support-gap episode is recorded separately.
