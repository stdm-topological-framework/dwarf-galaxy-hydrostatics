# dwarf-galaxy-hydrostatics
Python model for 3D gas geometry, hydrostatic equilibrium, and asymmetric drift in dwarf galaxies (Camelopardalis B).
# Dwarf Galaxy Hydrostatic Equilibrium & Flaring Model

This repository contains a Python tool for modeling the 3D geometry, hydrostatics, and kinematics of dwarf galaxy disks using observational data from the **SPARC** catalog (Spitzer Photometry and Accurate Rotation Curves). 

The code is configured for **Camelopardalis B (CamB)** but can be easily adapted for any other dwarf or spiral system.

## 🌌 Physical Background

The script solves equations of vertical hydrostatic equilibrium and computes:
1. **Epicyclic frequency ($\kappa$)** from the observed rotation curve.
2. **Toomre $Q_{\text{gas}}$ stability parameter** to analyze star formation thresholds.
3. **Gas disk thickness ($2h$)** as a function of radius, modeling the geometric flaring effect.
4. **Asymmetric drift corrections ($V_{\text{hydro}}$)** caused by turbulent and thermal gas pressure gradient ($\sigma_{\text{gas}} \approx 6.2$ km/s).

## 🛠️ Requirements
* Python 3.x
* NumPy
* Matplotlib

## 📜 License
This project is licensed under the MIT License - feel free to use and adapt it for your own research!
