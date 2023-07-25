Infrared spectra with TDEP
===

This tutorial covers the basics to compute first-order Infrared spectra with TDEP. What we need to compute is the Infrared scattering cross section.

## Preparation

- Have a converged set of 2nd and 3rd order force constants.

- Have a DFT code ready that can compute the dielectric tensor $\varepsilon$ and Born effective charge tensors $Z_i$ for you.

- **We need the most recent version of ASE in order to be able to parse dielectric tensors and Born effective charges**. Please make sure you have that installed, e.g., by running

  ```
  pip install git+https://gitlab.com/ase/ase.git@master
  ```

  The parsers will work for VASP, Quantum Espresso, and FHI-aims (the latter only computes the dielectric tensor). For Quantum Espresso, please note the extra step explained in the `00_preparation/qe_dielectric_tensors` tutorial.

## Background

Add background of IR scattering

<p>
	<img src=".assets/figure_infrared_hofmeister_1.png" width="450"/>
  <em>Figure from  <a href=#Suggested-reading>Ref. 1</a> </em>
</p>


## Steps

### Start: Inspect phonon dispersion and selection rules

- Create the phonon dispersion for your forceconstants

  ```
  FILL COMMAND
  ```

- Check you many Raman active modes you have
  ```
  FILL SHELL OUTPUT
  ```

- Check the file `outfile.mode_activity.csv` which contains the mode frequencies at the Gamma point, and whether they are Raman active (1) or not (0). (Same for IR activity).

- Plot this file.

### Compute mode intensities

- Displacements for each phonon mode with the command

  ```
  FILL COMMAND
  ```

  This will create 2 displacement (+ and -) for each mode.

- Filter out modes that are not Raman active with the command

  ```
  FILL COMMAND
  ```

- Move the files to folders and compute the dielectric tensor, e.g., with Quantum Espresso.

- Parse the outputs with the command
  ```
  FILL COMMAND
  ```

- Now we can compute the mode intensities (Eq. (9) in [2]) by running
  ```
  FILL COMMAND
  ```

- This will return `outfile.mode_intensity.csv`

- Plot that file

## Raman scattering cross section including temperature effects

- We need the `lineshape` for the Gamma point. To get it, run
  ```
  FILL COMMAND
  ```

  this will create the output file `FILE`

- We can now get the full spectrum by combining the intensities with the spectral function
  ```
  FILL COMMAND
  ```

- Inspect the output


## Suggested reading

- [[0] M. T. Dove, *Introduction to Lattice Dynamics* (Cambridge University Press, 1993), Chp. 10](https://doi.org/10.1017/CBO9780511619885)
- [[1] A. M. Hofmeister, E. Keppel, and A. K. Speck, Mon. Not. R. Astron. Soc. **345**, 16 (2003)](https://academic.oup.com/mnras/article/345/1/16/984419)
- [[2] G. Fugallo, B. Rousseau, and M. Lazzeri, Phys Rev B **98**, 184307 (2018)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.98.184307)
- [[3] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
