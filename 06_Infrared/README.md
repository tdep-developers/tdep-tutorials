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

Infrared absorption describes the phenomenon of a polar insulator or semiconductor absorbing light at infrared wavelengths (few $\text{cm}^{-1}$ to few thousand $\mathrm{cm}^{-1}$), i.e., well below the bandgap. The simplest explanation is that the incident light drives certain phonon modes which couple to electromagnetic radiation (optical modes) and therefore loses energy. The energy loss can be measured as a function of wavelength or frequency, and from the resulting spectrum we can learn which phonons were excited.

A sketch of the scattering geometry copied from [Ref. 1](#Suggested-reading) is shown below. Note that the incident angle is typically (very close to) perpendicular to the sample surface and the angle is exaggerated for visualization.

<p>
	<img src=".assets/figure_infrared_hofmeister_1.png" width="450"/>
  <em>Figure from  <a href=#Suggested-reading>Ref. 1</a> </em>
</p>

The incoming light intensity is denoted as $I_0$ , and an amount $I_0 R$ is reflected upon incidence on the surface, where $R$ is the _reflectivity_, so that the remaining light has an intensity $I_1 = I_0 (1-R)$ within the sample. While passing through the sample, an amount $I_1 \Omega$ is absorbed, hence $\Omega$ denotes the _absorptivity_ of the sample, and an amount $I_2 = I_1 (1-\Omega) = I_0 (1-R)(1-\Omega)$ remains. When leaving the sample, an amount $I_2 R$ is reflected, leaving and amount $I_\text{measure} = I_2 (1-R)= I_0 (1-R)^2(1-\Omega)$ for measurement.

The reflectivity $R$ and absorptivity $\Omega$ are intimately related to the _complex refraction index_ $\tilde n (\omega)$, or likewise the _complex dielectric function_ $\epsilon (\omega)$ of the material, and depend on the frequency (or wavelength) of the incident light. It will be our task to determine these functions from which the optical properties can be determined, as further detailed below.

### Defintions

Reflectivity $R$: Amount of incident light that gets reflected such that $I_\text{reflected} = R I_0$. Related to the complex _index of refraction_ or _optical function_

$$
\tilde n = n + \mathrm{i} k~,
$$

with real component $n$ and complex component $k$:

$$
R=\frac{\left(n-1\right)^2+k^2}{\left(n+1\right)^2+k^2}~.
$$

The complex index of refraction is related to the complex _dielectric function_ $\epsilon$ through

$$
\epsilon = \epsilon_1 + \mathrm{i} \epsilon_2
$$

via

$$
\begin{align}
\epsilon_1 &= n^2 - k^2 \\
\epsilon_2 &= 2nk
\end{align}
$$


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
