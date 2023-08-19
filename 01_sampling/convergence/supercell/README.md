TDEP: Supercell convergence
===

Study supercell size convergence.

## Prerequisite:

- Study the range of force constants in our MgO potential [**and determine a converged real-space cutoff from the previous tutorial.**](../cutoff/README.md)

- The largest cutoff you can obtain in a given supercell is given by the radius of the largest sphere you can put inside. TDEP prints the smallest (nearest neighbor distance) and largest possible cutoffs at the beginning of the `extract_forceconstants` output:
  ```
   ... reading unitcell
   ... min cutoff: 2.11499
   ... max cutoff: 6.33859
  ```

  these are the cutoffs in Angstrom.

## Steps

- Pick one supercell size, say [216.](./n_0216)
- Create 512 samples with the converged force constants from the [MgO sampling tutorial](../../example_materials/MgO/README.md).
- Create the forces using the potential.
- extract forceconstants with a step size (`--stride`) of 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 and create phonon dispersions.
- Plot the convergence of the phonon dispersion as function of number of samples.
- Repeat for a different supercell size. Check the convergence of phonon frequencies. How does supercell size influence the dispersion, in particular when going to smaller supercells that artificially truncate their range?

## Hints

- There are scripts and Makefiles in `skeleton` to help you with this task.
- There is a jupyter notebook `notebook_check_number_samples.ipynb` to help you check the convergence w.r.t. to sample number for a given supercell size.
- There is a jupyter notebook `notebook_check_supercell_size.ipynb` to help you check the convergence w.r.t. to supercell size.
