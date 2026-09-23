---
task: unsupported
engine: none
error_class: support_gap
outcome: support_gap
---
Symptom: The requested calculation is the Gibbs free energy of the multi-species reaction C2H5OH + 3 O2 -> 2 CO2 + 3 H2O.
Attempts: Searched MAESTRO capabilities for "free energy", "thermochemistry", "ethanol combustion", "reaction free energy", and "reaction energy". ThermoTask evaluates one molecule; ReactionProfileTask reports a reaction free energy only from already supplied minimum-energy-path and stationary-point Gibbs values.
Result: No MAESTRO task generates the individual molecular thermochemistry and stoichiometric combustion reaction free energy in one calculation. A raw PySCF script is used as a workaround.
Context: Standard-state gas-phase combustion convention at 298.15 K and 1 atm; no MAESTRO calculation was executed.
