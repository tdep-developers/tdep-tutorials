Raman spectra with TDEP
===

This tutorial covers the basics to compute first-order Raman spectra with TDEP. What we need to compute is the Raman scattering cross section, Eq. (7) in Ref. [1], with the first-order dielectric response, Eq. (10) in [1], which we compute here by finite differences similar to Eq. (9) in Ref. [2]. By including anharmonicity, we can study the temperature dependence of the Raman spectrum as well.

## Preparation

- Have a converged set of 2nd and 3rd order force constants.

- Have a DFT code ready that can compute the dielectric tensor $\varepsilon$ for you.

- **We need the most recent version of ASE in order to be able to parse dielectric tensors**. Please make sure you have that installed, e.g., by running

  ```
  pip install git+https://gitlab.com/ase/ase.git@master
  ```

  The parsers will work for VASP, Quantum Espresso, and FHI-aims. For Quantum Espresso, please note the extra step explained in the `00_preparation/qe_dielectric_tensors` tutorial.

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

- [[1] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
- [[2] J. M. Skelton, L. A. Burton, A. J. Jackson, F. Oba, S. C. Parker, and A. Walsh, Phys Chem Chem Phys **19**, 12452 (2017)](https://pubs.rsc.org/en/content/articlelanding/2017/CP/C7CP01680H)  

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)