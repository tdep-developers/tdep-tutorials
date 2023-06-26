Thermodynamics with TDEP
========================

The goal of this tutorial is to show how to compute thermodynamic properties with TDEP.
In the harmonic approximation, the free energy, as well as all every other thermodynamic properties, can computed exactly using the phonon density of states defined as:

```math
g(\omega) = \sum_\lambda \delta(\omega - \omega_\lambda)
```

For instance, the harmonic free energy $\mathcal{F}_0$ is computed by integrating this density of states with the free energy of each phonons modes
```math
\mathcal{F}_0 = k_BT \int_0^\infty d\omega g(\omega) \ln\big[2 \sinh(\frac{\hbar\omega}{2k_BT}\big] 
```
Consequently, the free energy of the system at a given temperature can be obtained using this formula with a given set of phonons.
However, by definition, the harmonic approach is missing the anharmonic contribution, which can dramatically modify the thermodynamic of the sytem.

Fortunately TDEP is able to include part of the anharmonicity.
For a fixed volume, and staying at the second order in the force constants, the TDEP free energy is given by
```math
\mathcal{F}^{\mathrm{TDEP}} = \mathcal{F}_0^{\mathrm{TDEP}} + \lange V(\vec{R}) - V^{\mathrm{TDEP}}(\vec{R}) \range
```

Compared to the harmonic approximations, two corrections are to be observed
* The temperature dependence of the phonons, that will bring a modification of the $\mathcal{F}_0$
* The $U_0 = < V(\vec{R}) - V^{\mathrm{TDEP}}(\vec{R}) >$ term



## General scope

This tutorial covers:

1. Obtaining the effective harmonic free energy as well as the $U_0$ correction
2. Interpolating force constants along a temperature range
4. Comparison of the method of sampling (MD or generate_structure) on the results
5. Obtaining higher order corrections

This tutorial **does not cover**:

- how to relax a structure,
- how to check symmetry of your structure,
- supercell convergence,
- convergence of anharmonic properties.

## Basic steps

For this tutorial, we will need to perform simulations for several temperatures.
If you want to follow this tutorial with a material of your interest, you need to choose a range of temperature below the melting point and perform simulations for 5 temperatures in this range.
In order to compare the effects of the sampling method on the thermodynamic properties, you need to run molecular dynamics simulations as well as the canonical configuration method.

Otherwise, some reference data will be available in the `references` directory.


### Preparation of the data

- If you use the reference data
    - In the folder `reference/md` you will find 5 folders, each containing thermalized structures extracted from molecular dynamics.
    - Copy these data and the infile.ucposcar files in a new directory.

- You will find informations concerning free energy on [`extract_forceconsants`](http://ollehellman.github.io/program/extract_forceconstants.html) and [`phonon_dispersions`](https://ollehellman.github.io/program/phonon_dispersion_relations.html#sec_tdepthermo)

# Computing the free energy for one temperature

- Go into the directory for the lowest temperature and prepare the data for TDEP
- Compute the force constants using the command: `extract_forceconstants -rc2 XX -U0`
- Compute the phonon dispersion with the command: `phonon_dispersions --dos --temperature 300`
    - In the directory, you should find two files related to thermodynamic properites: `outfile.free_energy` and `outfile.U0` 
    - In the first one, created with the use of the `--temperature` options of `phonon_dispersions`, you will find 4 values :
        1. The temperature
        2. The harmonic free energy, in eV/atom
        3. The harmonic entropy, in ev/K/atom
        4. The harmonic heat capacity in eV/K/atom
    - The second one has been activated with the `--U0` options of `extract_forceconstants` and contains the $U_0$ correction to the harmonic free energy

- For this temperature, try to converge the value of the harmonic free energy and its correction. For this, you have several parameters to control
    1. The number of samples
    2. The cutoff for the force constants
    3. The q-point grid used to compute the harmonic properties. The grid can be controlled with the `--qg` option of the `phonon_dispersions` binary.
    - Each of these parameters will have a different influence on the free energy. For instance, the $U_0$ value is computed using single point energy. This means that contrary to the force constants, which benefit from $3 \times N_{\mathrm{at}}$ values per configurations, only one point is added to the average per configurations. Try to observe the effect of each of the parameter on the convergence of the $U_0$ and the harmonic free energy.

- Once this step is done, you can compute the free energy for the 4 other temperatures. To accelerate the process, you can use a script.


## Interpolating the free energy : the naïve way

- To interpolate the free energy on the temperature range, you will find a script `naive_interpolation.py`in `references/scripts` using XX order polynomial to fit the data
    - Copy the script in the root folder, and prepare a file `reference_free_energy.dat` with two columns: one for the temperature and one for the total free energy $\mathcal{F} = \mathcal{F}_0 + U_0$.
    - Running the script will produce files `naive_interpolation.pdf` and `naive_interpolation.dat` in the folder, with the resulting interpolated free energy.


## Interpolating the free energy : the TDEP way

- In the naïve approach, the harmonic free energy is fitted only a scalar value with a small number of references. With TDEP, we can improve the interpolation by doing it on the force constant instead of the free energy directly.
- Create a map for each temperature
- Interpolate irrifc
- Generate interpolated phonons
- Compare with naïve interpolation


## Comparing the canonical_configuration sampling with the MD

- Do the same thing but with canonical_sampling, without the `--quantum` options (reference files in `references/canonical_configurations`).
- 
- (Note to myself - need to have reference data (thermodynamic integration)
- Things to discuss here:
    - The separation of free energies when increasing temperature
    - The nuclear quantum effects


## Beyond the second order

- Inclusion of Phi3 + Phi4
- Comparison to harmonic results


## Suggested reading


## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)


## Notes for myself

- Reference data needed
    - MD configurations
    - SCHA configurations
    - Thermodynamic integrations for comparison
    - A harmonic results to compare ?
