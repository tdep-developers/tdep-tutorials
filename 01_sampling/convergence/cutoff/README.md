TDEP: Cutoff convergence
===

Study convergence with respect to the real-space cutoff for 2nd order force constants.

The current folder has a supercell with 1000 atoms. We will create a set of samples and study how the TDEP fit improves when increasing the realspace cutoff `--rc2`.

## Steps

- Create 32 samples with the converged force constants from the [MgO sampling tutorial](../../example_materials/MgO/README.md).

- Create the forces using the potential.

- Extract forceconstants with a cutoff of 3, 4, 5, …, 11 Angstrom and `tee` the output to `extract_forceconstants_03.0.log`, `extract_forceconstants_04.0.log`, etc.

- Check the diagnostics for the fit quality after `... diagnostics from three-fold cross-validation:`, something like:
  ```
   ... diagnostics from three-fold cross-validation:
                                     R^2     stddev energy (meV/atom)
                           input:                 0.0545500
                    second order:  0.81727        0.1225550
            second order + polar:  0.96439        0.0881981
  ```

- Plot the R2 **for the `second order`** as function of the cutoff. Ignore the **`second order + polar`** (why?)

- After what cutoff does it not increase anymore? → **This is the converged cutoff! Increasing the cutoff further does not improve the fit quality.**

- Compare with the real-space range of the force constants that you can compute and plot with `tdep_plot_fc_norms`.

## Hints

- There are scripts and a `Makefile` to help you.
