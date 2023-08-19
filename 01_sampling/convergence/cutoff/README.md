TDEP: Cutoff convergence
===

Study convergence with respect to the real-space cutoff for 2nd order force constants.

The current folder has a supercell with 512 atoms. We will create a set of samples and study how the TDEP fit improves when increasing the realspace cutoff `--rc2`. This is larger than you would typically have it in DFT. The point is to illustrate how to estimate the physical cutoff of the model, which usually lies in the range 5-10 $\mathrm \AA$ depending on the material. **This needs to be checked on a case by case basis.** 

## Steps

- Create 32 samples with the converged force constants from the [MgO sampling tutorial](../../example_materials/MgO/README.md).

- Create the forces using the potential.

- Extract forceconstants with a cutoff of 3, 4, 5, …, 11 Angstrom and save the relevant output in a folder `rc_3.0`, `rc_4.0`, etc.

- Check the diagnostics for the fit quality after `... diagnostics from three-fold cross-validation:`, something like:
  ```
   ... diagnostics from three-fold cross-validation:
                                     R^2     stddev energy (meV/atom)
                           input:                 0.0545500
                    second order:  0.81727        0.1225550
            second order + polar:  0.96439        0.0881981
  ```

  **This cross-validation R2 is bit different from the pure fit R2 that is written towards the end of the output. Its purpose is to tell you about the robustness of the fit against variation.**
  
- Plot the R2 **for the `second order`** as function of the cutoff. Ignore the **`second order + polar` here** (why?)

- After what cutoff does it not increase anymore? → **This is the converged cutoff! Increasing the cutoff further does not improve the model, on the contrary.**

- Compare with the real-space range of the force constants that you can compute and plot with `tdep_plot_fc_norms`.

In the current case, the optimal cutoff should be around 6A. This cutoff would also fit in a supercell with 216 atoms. Good to know.

## Hints

- There are scripts and a `Makefile` to help you.

## More practical advice

- The R2 is only one things to look at. It is a good hint for when all significant interactions are captured.This range is typically reached when the R2 is not increasing anymore with cutoff.
- In practice, one should be more concerned with the observables of interest. These should be robust against changes in the cutoff(s, when going to higher orders), as with any numerical parameter. If your results change a lot with the choice of the cutoff, there might be something wrong elsewhere.
