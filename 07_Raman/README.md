Raman spectra with TDEP
===

We have seen in [the infrared tutorial](../06_Infrared/) that light can couple to the motion of atoms (phonons) in the frequency range corresponding to the spectral range of phonons, which is typically several THz. Light in the visible range (>400 THz) will not directly couple to the phonons. However, it can still exchange quanta of energy with the phonons through variations in the permittivity: the Raman effect.

This tutorial covers the basics to compute temperature-dependent first-order Raman spectra with TDEP. 

What we need to compute is the Raman scattering cross section, Eq. (7) in Ref. [1], 

$$
\sigma(\omega) \propto \sum_{\mu \nu \xi \rho} E_\mu^{\text {out }} E_{\xi}^{\text {out }} I_{\mu \nu, \xi \rho}(\omega) E_\nu^{\text {in }} E_\rho^{\text {in }}
$$

which relates the intensity of incoming with with E-field vector ${\mathbf E}^\mathrm{in}$ to the intensity of the outgoing light with E-field vector ${\mathbf E}^\mathrm{out}$, where $\mu$, $\xi$, $\nu$, $\rho$ are Cartesian indices, $I_{\mu \nu, \xi \rho}$ is the _Raman tensor_, and $\omega$ is the Raman shift frequency.

The Raman tensor is given by the susceptibility-susceptibility response function

$$
I_{\mu \nu, \xi \rho} (\omega)
= \int \langle \chi_{\mu \nu} (t) \chi_{\xi \rho} (0) \rangle {\mathrm e}^{- \mathrm i \omega t} \mathrm d t~,
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

In this tutorial, we will compute the Raman tensor by expanding the susceptibility to first order in the atomic displacements, i.e., the first-order dielectric response, Eq. (10) in [1], which we compute here by finite differences similar to Eq. (9) in Ref. [2]. By including anharmonicity, we can study the temperature dependence of the Raman spectrum as well, as well as polarization dependence.

In first order Raman, the Raman tensor is:

$$
I^{\alpha \beta}_s = \frac{\partial \chi^{\alpha \beta}}{\partial u_s}~,
$$

i.e., the change of the susceptibility with _mode displacement_ $u_s$.

</br>
The Raman tensor can be obtained from atomic displacements (as we will do in this tutorial) via the eigenvectors:

$$
I^{\alpha \beta}_ s  = \sum_{i}v_{i,s}\frac{\partial \chi^{\alpha \beta}}{\partial u_i}
$$

where $v_{i,s}$ is the real part of the eigenvector relative to the $i$-th atomic displacement according to the mode $s$.


The intensity contribution of mode $s$ at frequency $\omega$ for given polarization $\mathbf e_{\mathrm i}$ of incoming and $\mathbf e_\mathrm{o}$ for outgoing light will be given by

$$
\sigma_{s; \mathbf e_\mathrm{i}, \mathbf e_\mathrm{o}} (\omega) = \lvert \mathbf e_\mathrm{i} \cdot I_s \mathbf e_\mathrm{o} \rvert^2 J_s(\omega)~,
$$

where $e_\mathrm{i}$, $e_\mathrm{o}$ and $I_s$ are respectively two vectors and a matrix, and $J_s$ is the spectral function of mode $s$, which, of course, depends on temperature. There are a couple of approximations here that we go over, I refer to [[Benshalom2022, Benshalom2023, Knoop-arxiv2412.17711]](#Suggested-reading) for a more complete treating. The full intensity will be given as a sum over modes (**equation (1)**):

$$
\sigma_{\mathbf e_\mathrm{i}, \mathbf e_\mathrm{o}} (\omega) 
= \sum_s \sigma_{s; \mathbf e_\mathrm{i}, \mathbf e_\mathrm{o}} (\omega)
= \sum_s \lvert \mathbf e_\mathrm{i} \cdot I_s \mathbf e_\mathrm{o} \rvert^2 J_s(\omega)
$$


and this will be what experimentalists can measure. Mapping out the full dependency of the intensity as a function of the incoming/outgoing polarization is called _polarization-orientation (PO) Raman_. Eq. (1) is the topic of this tutorial.

### Note on orientation

To understand experimental Raman spectra for single crystals, we need to understand the _Porto notation_ [[Arguello1969]](#Suggested-reading):

<p>
	<img src=".assets/porto_notation.png" width="600"/>
  <figcaption><center><em>Figure from  <a href=#Suggested-reading>Ref. 4</a></em></center></figcaption>
</p>

This $X(YX)Z$ is to be read as:

- X: Direction of incoming light (its $\mathbf k$ vector)
- Y: Polarization of incoming light $\mathbf e_\mathrm{i}$
- X: Polarization of outgoing light $\mathbf e_\mathrm{o}$
- Z: Direction of outgoing light (its $\mathbf k$ vector)

#### Backscattering experiment

We will deal only with the most common type of experiment, the _backscattering experiment_, where incoming and outgoing light have the same direction, $\mathbf k_{\mathrm i} = - \mathbf{k}_{\mathrm o}$, denoted in Porto notation as, e.g., $Z (XY) \bar Z$.

### Note on polarization and averages
The cross-section $\sigma_{e_\mathrm{i}, e_\mathrm{o}} (\omega)$ can be measured by sending the probing light polarized along $\mathbf e_\mathrm{i}$ and detecting only the $\mathbf e_\mathrm{o}$-polarized component of the outcoming light from the crystal.
</br>
For an unpolarized backscattering experiment (e.g. no polarizers are useed for either probing and detecting), the spectrum is an average of the cross-sections for all the parallel and orthogonal pairs $(e_\mathrm{i}, e_\mathrm{o})$ that can be defined on the plane orthogonal to the wavevector of the incoming light. The result is an unpolarized spectrum.
</br>
For a powder sample, not only the considerations made so far hold, but we also have to make an average over all the possible wavevectors of the incoming light (isotropic average). The same result can be obtained by averaging the raman tensor elements as explained in [Knoop-arxiv2412.17711]. The result is an isotropically averaged spectrum.
</br>
Note that for powders of polar materials there is also another possible complication that is not taken into account in this tutorial: since the Raman tensor depends on the polarization of the mode, it might considerably change by varying the wavevector of the incoming light (which means probing long-wavelength phonons from different directions of the BZ), because of the LO-TO splitting. In order to solve this, a spherical integration over all the possible wavevectors should be performed (i.e. the entire process displaied in this tutorial should be done a very large number of times). Depending on the symmetry of your system and on the entity of the LO-TO splitting, this effect might be neglected. 

## Outline

We will compute Raman spectra for wurtzite gallium nitride (GaN) and compare to the experimental reference in Ref. [[Siegle1995]](#suggested-reading).

## Preparation

- Have a converged set of 2nd and 3rd order force constants.

- Have a DFT code ready that can compute the dielectric tensor $\varepsilon$ for you (not necessary for the tutorial, but it is for production).


## Steps

We will start with backscattering in $z$ direction:
1. Go to the `example_GaN/` folder
2. Create a new working directory for the $z$ direction
   ```bash
   mkdir raman_z
   cd raman_z
   ``` 
3. Copy the infiles into `raman_z/`:
    ```bash
    cp ../infile.lotosplitting ../infile.ucposcar ../infile.ssposcar ./
    ```
4. Copy your (converged) force constant outfiles that you got previously (see tutorial 01) and change their prefix to `infile`. For time reasons, we will use some pre-computed ones:
   ```bash
   cp ../.assets/infile.forceconstant ../.assets/infile.forceconstant_thirdorder .
   ```   
5. Create the spectral functions:
   ```bash
   lineshape --temperature 300 --qdirin 0 0 1
   ```
   this should give the file `outfile.phonon_self_energy.hdf5` that you already encountered in previous tutorials.

6. Now we create the atomic displacements via:
   ```bash
   tdep_displace_atoms infile.ucposcar
   ```

   which will create positive and negative displacements for each atom and cartesian direction and write them to `outfile.ucposcar.displacement.00001.x.plus`, `outfile.ucposcar.displacement.00002.x.minus`, etc. Tidy up the mess by moving these outfiles inside a dedicated folder (e.g. `displacements`):
   ```bash
   mkdir displacements
   mv outfile.ucposcar.displacement* displacements/
   ```

7. **Now comes the DFPT part:** convert these geometry files into the input format of the DFT code of your choice which is capable of computing the dielectric tensor (Born charges are not needed) and compute the dielectric tensor for each sample.

8. When you are finished with all dielectric calculations, parse them and write them in a new file called `infile.dielectric_tensor`. The order to follow when writing the tensors in this file is the same used in the numbering of the outfiles obtained from `tdep_displace_atoms` (that is the order of the atoms in the `infile.ucposcar` and first + and then - displacement).
   </br>
   Note that the units of the dielectric tensor are not important (of course they must be consistent among the displacements), as they renormalize the whole spectrum intensity.
   </br>
   Copy or link the infile to your working directory `raman_z`.
   </br>
   **We will skip steps 7 and 8 now, due to time reasons, but naturally this is something you need to do for production runs. For the time being, we will use the hidden input file `07_Raman/example_GaN/.assets/.infile.dielectric_tensor`.**
   ```bash
   cp ../.assets/infile.dielectric_tensor .
   ```
9. Good, now we can compute the Raman tensors, and convolute them with the spectral functions, i.e., evaluate Eq. (1). There is a script to do this in several ways:
   ```bash
   tdep_compute_raman_intensities
   ```
Done.


## The output files
Several output files are produced by the last step
- ```outfile.raman_activity_mode_001.csv```
  The mode index, the frequency (in THz and $cm^{-1}$), the isotropic and unpolarized Raman activities are listed for each mode. No information on the peak shape.
- ```outfile.raman_intensity_001.csv```
  The actual spectra: frequency (in $cm^{-1}$), the parallel and perpendicular intensities, and the unpolarized and isotropic intensities are listed. Here the parallel and perpendicular intensities are averages computed by only considering respectively the parallel and orthogonal pairs of polarizations lying on the plane orthogonal to the photon wavevector.
- ```outfile.raman_intensity_001_po.h5```
  This hdf5 file has attributes:
     - direction1
     - direction2
     - direction3
  
     where the first is the propagation direction of the incoming light, and the last two define the polarization plane of both the incoming and scattered light.

  Then there are two coordinates:
     - angle (size=361): the array of the possible angles of rotation of the (fixed) pairs of polarization around the propagation direction of the light (it uniquely identifies the pair of polarisations on the plane)
     - frequency (size=1200): the frequency in $cm^{-1}$

  Finally, two data variables:
     - parallel (shape=361,1200): Raman spectrum (1200 values, one for each frequency) for each angle of rotation of the fixed pair of *parallel* polarizations on the plane   
     - perpendicular (shape=361,1200): Raman spectrum (1200 values, one for each frequency) for each angle of rotation of the fixed pair of *perpendicular* polarizations on the plane

## Analysis
Here are some examples of python scripts to plot the spectra.
#### Unpolarized and isotropically averaged spectra
  ```python
  import numpy as np
  from matplotlib import pyplot as plt
  
  data = np.loadtxt(fname='outfile.raman_intensity_001.csv', skiprows=1, delimiter=',').T
  freqs = data[0]
  unpo = data[3]
  iso = data[4]
  
  Fig = plt.figure(figsize=(15,5))
  
  Fig.add_subplot(1,2,1)
  # UNPOLARIZED
  plt.plot(freqs, unpo)
  plt.xlim(0,800)
  plt.title('Unpolarized spectrum')
  plt.xlabel('Raman shift ($cm^{-1}$)')
  plt.yticks([])
  plt.ylabel('Intensity (a.u.)')
  
  Fig.add_subplot(1,2,2)
  # ISOTROPIC
  plt.plot(freqs, iso)
  plt.xlim(0,800)
  plt.title('Isotropically averaged spectrum')
  plt.xlabel('Raman shift ($cm^{-1}$)')
  plt.yticks([])
  plt.ylabel('Intensity (a.u.)')
  ```
#### Polarization orientation spectra
  ```Python
  import numpy as np
  import xarray as xr
  from matplotlib import pyplot as plt
  
  ds = xr.open_dataset('outfile.raman_intensity_001_po.h5')
  angles = np.array(ds['angle'])
  freqs = np.array(ds['frequency'])
  paral = np.array(ds['parallel'])
  perp = np.array(ds['perpendicular'])
  #directions = np.array([ds.direction1, ds.direction2, ds.direction3]) # we don't need this
  
  
  # z(xx)-z ------ parallel, theta = 0 
  i_0 = np.argmin(angles) # find the position of theta=0 in the angles array
  spec1 = paral[i_0] 
  plt.plot(freqs, spec1)
  plt.xlim(0,800)
  plt.title('z(xx)-z')
  plt.xlabel('Raman shift ($cm^{-1}$)')
  plt.yticks([])
  plt.ylabel('Intensity (a.u.)')
  
  # z(xy)-z ------ perpendicular, theta = 0
  plt.figure()
  spec2 = paral[i_0]
  plt.plot(freqs, spec2)
  plt.xlim(0,800)
  plt.title('z(xy)-z')
  plt.xlabel('Raman shift ($cm^{-1}$)')
  plt.yticks([])
  plt.ylabel('Intensity (a.u.)')
  ```


**Task:** Plot all the equivalents of the first 4 plots of Fig. 2b in [[Siegle1995]](#Suggested-reading) and discuss your findings (hint: you need to run the steps of this tutorial again, changing a single parameter).

Congratulations, you have performed a complete description of first-order Raman scattering in wurtzite GaN at room temperature from first principles.


## Suggested reading

- [[0]R. A. Cowley, P Phys Soc **84**, 281 (1964)](https://iopscience.iop.org/article/10.1088/0370-1328/84/2/311)
- [[1] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
- [[2] J. M. Skelton, L. A. Burton, A. J. Jackson, F. Oba, S. C. Parker, and A. Walsh, Phys Chem Chem Phys **19**, 12452 (2017)](https://pubs.rsc.org/en/content/articlelanding/2017/CP/C7CP01680H)  
- [[3] N. Benshalom et al., arxiv 2204.12528 (2023)](https://arxiv.org/abs/2204.12528)
- [[4]C. A. Arguello, D. L. Rousseau, and S. P. S. Porto, Phys Rev **181**, 1351 (1968)](https://journals.aps.org/pr/abstract/10.1103/PhysRev.181.1351)
- [[5]H. Siegle *et al.*, Solid State Commun. **96**, 943 (1995)](https://www.sciencedirect.com/science/article/pii/0038109895005617)
- [[6]K. Florian *et al.*, arXiv:2412.17711](https://arxiv.org/abs/2412.17711v1)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
