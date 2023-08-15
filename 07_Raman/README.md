Raman spectra with TDEP
===

This tutorial covers the basics to compute first-order Raman spectra with TDEP. What we need to compute is the Raman scattering cross section, Eq. (7) in Ref. [1], 

$$
\sigma(\Omega) \propto \sum_{\mu \nu \xi \rho} E_\mu^{\text {out }} E_{\xi}^{\text {out }} I_{\mu \nu, \xi \rho}(\Omega) E_\nu^{\text {in }} E_\rho^{\text {in }}
$$

which relates the intensity of incoming with with E-field vector ${\mathbf E}^\mathrm{in}$ to the intensity of the outgoing light with E-field vector ${\mathbf E}^\mathrm{out}$, where $\mu$, $\xi$, $\nu$, $\rho$ are Cartesian indices, and $I_{\mu \nu, \xi \rho}$ is the _Raman tensor_.

The Raman tensor is given by the susceptibility-susceptibility response function

$$
I_{\mu \nu, \xi \rho} (\Omega)
= \int \langle \chi_{\mu \nu} \chi_{\xi \rho} \rangle {\mathrm e}^{- \mathrm i \Omega t} \mathrm d t~,
$$

with the polarizability also known from the dielectric tensor

$$
\epsilon = \epsilon_0 ( 1 + \chi )
$$

in SI units, or

$$
\epsilon = 1 + 4 \pi \chi
$$

in atomic units.

In this tutorial, we will compute the Raman tensor by expanding the susceptibility to first order in the atomic displacements, i.e., the first-order dielectric response, Eq. (10) in [1], which we compute here by finite differences similar to Eq. (9) in Ref. [2]. By including anharmonicity, we can study the temperature dependence of the Raman spectrum as well.

## Intuition

We have seen in [the infrared tutorial](../06_Infrared/) that light can couple to the motion of atoms (phonons) in the frequency range corresponding to the spectral range of phonons, which is typically several THz. Light in the visible range (>400 THz) will not directly couple to the phonons. However, it can still exchange quanta of energy with the phonons through variations in the permittivity/

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

- [[0]R. A. Cowley, P Phys Soc **84**, 281 (1964)](https://iopscience.iop.org/article/10.1088/0370-1328/84/2/311)
- [[1] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
- [[2] J. M. Skelton, L. A. Burton, A. J. Jackson, F. Oba, S. C. Parker, and A. Walsh, Phys Chem Chem Phys **19**, 12452 (2017)](https://pubs.rsc.org/en/content/articlelanding/2017/CP/C7CP01680H)  

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
