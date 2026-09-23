---
task: unsupported
engine: none
error_class: none
outcome: success
method: B3LYP
basis: def2-SVP
cores: 12
mode: local
---
Symptom: None after correcting the installed PySCF thermochemistry API handoff.
Attempts: Optimized ethanol, triplet oxygen, carbon dioxide, and water, evaluated their Hessians and ideal-gas thermochemistry at 298.15 K and 1 atm, and formed the stoichiometric reaction difference.
Result: Delta G for C2H5OH + 3 O2 -> 2 CO2 + 3 H2O is -0.4418984711 Hartree, or -1160.2043 kJ mol-1, at B3LYP/def2-SVP.
Context: This is an ideal-gas calculation. It does not model liquid ethanol/water standard states. MAESTRO has no direct multi-species reaction-thermochemistry task for this request.
