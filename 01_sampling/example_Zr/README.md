Stochastic TDEP (sTDEP) for Zirconium
===

This example shows how to perform statistical sampling for bcc zirconium, and how to obtain a positive definite spectrum at high temperatures, in this case, 1300K.

## Steps

1. Go to the folder `sampling.1300K/iter.000` to start the sampling

2. Check the `Makefile` and the target `init`

3. `make init` to create the first 4 samples at target temperature of 1300K.

4. compute the forces with
   ```bash
   sokrates_compute --folder-model ../../module/ samples*/*/geometry.in --tdep
   ```

   this will use the So3krates potential to compute forces for the samples and create TDEP input files.

5. Now we can extract the forceconstants with
   ```bash
   extract_forceconstants -rc2 10 -U0 | tee extract_forceconstants.log
   ```

   Note that `-U0` is used to dump extra statistics at the end of the output.

6. Create phonon dispersion and plot:
   ```bash
   ln -sf outfile.forceconstant infile.forceconstant
   phonon_dispersion_relations -p
   gnuplot -p outfile.dispersion_relations.gnuplot_pdf
   ```

7. Inspect the phonon dispersion.

8. Now create the next iteration. There is a script in `tdeptools` that does everything automatic for you:
   ```bash
   tdep_create_next_iteration -T 1300
   ```

   will create the samples and move them to a folder `iter.001`.

9. Move this folder to your root directory and move to it
   ```bash
   mv iter.000 ..
   cd ../iter.000
   ```

10. To reuse the samples from the previous iteration, use
    ```bash
    tdep_ln_previous_samples
    ```

    this will link the folder `../iter.000/samples` to `samples_prev`.

11. Now we can repeat from 4 until convergence.

Please note that there is a makefile that summarizes each of the steps, once you feel confident try to understand the targets and simply use those via, e.g., `make infile.forces`, or `make iteration` to create an entire step.

## Things to look out for

- At each iteration, `canonical_configuration` is used and its output is saved to `canonical_configuration.log`. Inspect how in particular the mean-square displacement changes from iteration to iteration
- Observe how the dispersion converges more and more.
- Think about computing other observables, e.g., free energies, and check its convergence.
- After how many iteration does the dispersion stabilize?


## Suggested reading

- [Olle Hellman, Peter Steneteg, I. A. Abrikosov, and S. I. Simak, Phys. Rev. B **87**, 104111 (2013)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.87.104111)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)
- [you are familiar with using the so3krates force field (or have your own potential at hand)](https://github.com/tdep-developers/tdep-tutorials/tree/main/00_preparation/potential_energy_surfaces)
