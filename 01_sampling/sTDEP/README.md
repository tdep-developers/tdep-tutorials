sTDEP with DFT forces 
===

This tutorial covers self-consistent TDEP sampling using a DFT force engine. The example is for magnesium oxide, MgO.

## General scope

This tutorial covers:

1. generate a supercell using `generature_structure`,
2. create an initial set of configurations corresponding to a temperature with `canonical_configuration` in which forces are computed with a DFT or force field of choice,
3. parse the output to TDEP input files with `tdep_parse_output`,
4. fit the force constants to the forces obtained from the sampling via `extract_forceconstants`,
5. obtain and plot phonon dispersion relations using `phonon_dispersion_relations` and `gnuplot`,
   - choose a cutoff of the second-order force constants by examining overdetermination ratio, fit quality, and the range of force constants via `tdep_plot_fc_norms`,
6. generate a new iteration with more samples from the force constants using `canonical_configuration`,
7. repeat until convergence.

This tutorial **does not cover**:

- how to relax a structure,
- how to check symmetry of your structure,
- supercell convergence,
- convergence of anharmonic properties.

## Basic steps

### Preparation

- Read the documentation of [`generature_structure`](https://tdep-developers.github.io/tdep/program/generate_structure/)
- prepare a primitive cell for the material of your interest. This should be a POSCAR file called `infile.ucposcar`. An example is given for MgO in the current folder.
- To get LO/TO splitting right, add [`infile.lotosplitting`](https://tdep-developers.github.io/tdep/files/#infilelotosplitting) with dielectric tensor and Born effective charges.
- Generate a supercell of at least 200 atoms (for testing you might choose a smaller one)
  - e.g. `generate_structure -na 64` for 64 atoms, this will create `outfile.ssposcar`
  - copy `outfile.ssposcar` to `infile.ssposcar`. 
  - **TDEP always needs 2 reference structures: primitive `infile.ucposcar` and supercell `infile.ssposcar`**
- read the documentation of [`canonical_configuration`](https://tdep-developers.github.io/tdep/program/canonical_configuration/)
- generate an initial guess for force constants in your sytem by using the `--maximum_frequency XX` flag, where `XX` is the (approximate) maximum frequency in THz that you expect in your system
  - e.g. `canonical_configuration --quantum --maximum_frequency 20 --temperature 300 -n 1` will create 1 sample (`-n 1`) according to the quantum canonical distribution (`--quantum`) at 300K (`--temperature 300`) for an initial guess assuming a max. frequency of 20 THz.
  - this will create one sample with displacements (and velocities) in `contcar_conf0001`
- link the resulting output file `outfile.fakeforceconstant` to `infile.forceconstant` (` ln -s outfile.fakeforceconstant infile.forceconstant`)
- run `phonon_dispersion_relations -p` to compute the phonon dispersions and create gnuplot input files
- plot the dispersion with `gnuplot outfile.dispersion_relations.gnuplot_pdf -p` and inspect the plot in `outfile.dispersion_relations.pdf` to check if it looks reasonable and you get the maximum frequency you used earlier.

## Self-consistent loop

We will now perform self-consistent sampling at 300K in the folder `sampling.300K`.

###  Initial step

Change to the folder `sampling.300K`

#### Compute forces in structure

- Now create a folder `iter.000` which will contain the 0th iteration (from the initial guess)
- in that folder, create a folder `samples` with a subfolder `sample.00001`
  - e.g. `mkdir -p samples/sample.00001/`
- move the initial sample (`contcar_conf0001`) to that folder and compute forces using your force field or DFT of choice
  - note that you might need to rename this geometry input file, or convert it to the format of your DFT code, e.g., using [`ase convert	`](https://wiki.fysik.dtu.dk/ase/ase/io/io.html#module-ase.io)
  - run the calculation
- from the working directory (`iter.000`), parse the output of the calculation using `tdep_parse_output`:
  - FHI-aims: `tdep_parse_output samples/*/*/aims.out --format aims-output`
  - VASP: `tdep_parse_output samples/*/vasprun.xml --format vasp-xml`
  - Any other code supported by ASE ([see docs of `ase.io.read`](https://wiki.fysik.dtu.dk/ase/ase/io/io.html#ase.io.read) with `format=FORMAT`):
    - `tdep_parse_output samples/*/OUTPUT --format FORMAT `
- You should now see [TDEP input files](https://tdep-developers.github.io/tdep/files/) in your working directory

#### Obtain force constants

- First read the docs for [`extract_forceconsants`](https://tdep-developers.github.io/tdep/program/extract_forceconstants/)

- You can now run `extract_forceconstants` in to extract the force constants. At this initial stage, we should restrict the range of the cutoffs to close neighbors by choosing a small cutoff (via `-rc2`)

  - `extract_forceconstants --polar -rc2 0` will include nearest neighbors only, this might be a good start

  - make sure to save the output, e.g., by running
    `extract_forceconstants --polar -rc2 0 2>&1 | tee extract_forceconstants.log`

  - inspect the output carefully. Check in particular:

    - Number of force constants

      > ```
      > ...
      > Interactions:
      >         firstorder forceconstant:           0           0
      >        secondorder forceconstant:           2           4
      > ...
      > ```

    - Overdetermination ratio under `REPORT GRADE OF OVERDETERMINATION` tells you how many equations you have for the unknowns. This number should always be well above 1, rather in the 100s, but difficult to give general advice here. Try to get a feeling for this

    - Check the statistics on how well your forces are described by the TDEP model:

      > ```
      > ...
      > 
      >  FORCES (eV/A):
      >                      rms          rms(res)     std(res)     R2           normalized std(res)
      >           input:     1.108995     1.108995     0.640279     -            -
      >           polar:     0.494640     0.849566     0.490497     0.413140     0.766068
      >    second order:     0.814332     0.242125     0.139791     0.952333     0.218328             <-- anharmonicity measure
      > ...
      > ```

      - `rms`: The root mean square of the quantity (input forces, polar forces, second-order forces, …)
      - `rms(res)`: root mean square of the input forces minus the model forces (root mean square error, RMSE)
      - `std(res)`: standard deviation of the input forces minus the model forces
      - `R2`: R2 of the model fit
      - `normalized std(res)`: RMSE/STD, corresponds to anharmonicity measure from [this reference](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.4.083809)

      **The different force terms in this example are:**

      - `input`: input forces from DFT or potential of choice
      - `polar`: polar forces from long-range corrections
      - `second order`: forces from second-order force constants
  
  - Link the output file to make it an input file for the next steps:
  
    - `ln -s outfile.forceconstant infile.forceconstant`
  
  - create and plot the phonon dispersions, do they look fine?
  
  - Bonus: use `tdep_plot_fc_norms` to create a plot of the norm of the force constants resolved by pair vs. the pair distance. This is usefull to decide how long-ranged the interactions in the material actually are, and choose appropriate cutoffs at the final stages.

###  Next steps

- In the current working directory, create 2 new samples via

  `canonical_configuration --quantum --temperature 300 -n 2`

  - **Make sure _not_ to use the `--maximum_frequency` option again, otherwise you will create samples from the initial guess and not the force constants you obtained earlier**

- Now create a folder `iter.001` which will contain the 1st iteration that is not the initial guess
- in that folder, create a folder `samples` with a subfolder `sample.00001` and `sample.00002`
  - e.g. `mkdir -p samples/sample.00001/ samples/sample.00002/`
- move the sample (`contcar_conf000{1,2}`) to the respective folders and compute forces using your force field or DFT of choice
- repeat the postprocessing steps from above to get new force constants and phonon dispersions.
- Try to increase your force constants cutoff (``rc2`) and observe if the phonon dispersion changes. Also check the statistics dumped by `extract_forceconstant`. When your R2 does not increase, you're not fitting any new information and should not increase the cutoff further. Also check the range of the cutoff with `tdep_plot_fc_norms`.
- Repeat with 4, 8, 16, 32, ... samples in `iter.002`, `iter.003`, ...,  until your phonon dispersion does not change noticeably anymore.
- **Tip:** We can perform a _pre-conditioned_ self-consistent loop by re-using samples from previous iterations:

  - in iteration 2 (`iter.002`), link the samples from iteration 1:
    ```bash
    ln -s ../iter.001/samples/ samples_prev
    ```
  - then parse _all_ samples before the postprocessing step:
    ```bash
    tdep_parse_output samples/*/OUTPUT samples_prev/*/OUTPUT --format FORMAT
    ```
  - this will stabilize the self-consistent loop, and increase data efficiency.


## Notes on convergence

- In general you should converge the quantity of your interest. E.g., the free energy computed at each iteration might not change anymore when the dispersion still changes a by a few meV between iterations.

## Tips

- you will find a `Makefile` in `sampling.300K`. My personal advice is that you create one for each working directory and write down your commands there. Then you execute them via `make TARGET` instead of running directly in the terminal. This way you will always remember how you ran which command in your folder.


## Suggested reading

- [N. Shulumba, O. Hellman, and A. J. Minnich, Phys. Rev. B **95**, 014302 (2017)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.95.014302)
- Appendix of [N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)
