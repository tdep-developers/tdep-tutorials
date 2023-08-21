TDEP: Sampling convergence
===

This tutorial is supposed to help you to converge quantities with the number of samples once you have force constants. **This is implicitly done already when performing self-consistend (sTDEP) sampling for the second order force constants, but will become important when converging higher order force constants in later tutorials.**

## Prerequisite:

- Study the range of force constants in our MgO potential [**and determine a converged real-space cutoff from the previous tutorial.**](../cutoff/README.md)

## Steps

- [Create a supercell with 216 atoms](https://tdep-developers.github.io/tdep/program/generate_structure/) and copy the input files to `n_216`.
- Create 512 samples with the converged force constants from the [MgO sampling tutorial](../../example_materials/MgO/README.md).
- Create the forces using the potential.
- Extract forceconstants with a step size (`--stride`) of 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 and create phonon dispersions.
- Plot the convergence of the phonon dispersion as function of number of samples.
- Repeat for a larger supercell but same cutoff. Does the convergence get faster or slower? Why?

## Hints

- There are scripts and Makefiles in `skeleton` to help you with this task.
- There is a jupyter notebook `notebook_check_number_samples.ipynb` to help you check the convergence w.r.t. to sample number for a given supercell size.
