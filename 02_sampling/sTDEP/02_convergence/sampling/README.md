TDEP: Sampling convergence
===

This tutorial is supposed to help you to converge quantities with the number of samples once you have force constants. **This is implicitly done already when performing self-consistend (sTDEP) sampling for the second order force constants, but will become important when converging higher order force constants in later tutorials.**

## Prerequisite:

- Study the range of force constants in our MgO potential [**and determine a converged real-space cutoff from the previous tutorial.**](../cutoff/README.md)

## Steps

- [Create a supercell with 216 atoms](https://tdep-developers.github.io/tdep/program/generate_structure/).
- Create 512 samples with the converged force constants from the [MgO sampling tutorial](../../01_MgO/README.md).
- Create the forces using the potential.
- Extract forceconstants with a step size (`--stride`) of 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 and create phonon dispersions.
- Plot the convergence of the phonon dispersion as function of number of samples.
- Repeat for a larger supercell but same cutoff. Does the convergence get faster or slower? Why?

## Hints

- There is a script `get_infiles.sh` to generate the configurations and creates the infiles needed by TDEP. To use it, copy your converged forceconstants from the [MgO sampling tutorial](../../01_MgO/README.md) inside this folder and run
```bash
./get_infiles.sh
```

- There is a script `range_of_strides.sh` to automatize the extraction of force constants with different strides. Once you have generated the configurations, simply run
```bash
./range_of_strides.sh
```
With this, you should find all the results in the corresponding folder, starting with `stride_`.
Remember, the stride number is the number of steps between configurations read for extracting the force constants. So the higher the stride, the lower the number of configurations.

- To plot the convergence of the phonon density of states, you can use the script `plot_dos_convergence.py` that you can find [the `scripts` folder](../../scripts). To use it, copy this file in the folder and run:
  ```bash
    python plot_dos_convergence.py stride_*/outfile.phonon_dos
  ```
assuming that the phonon density of states for each stride are in their respective `stride_` folder.

Have a look at the scripts and try to understand what they are doing !
