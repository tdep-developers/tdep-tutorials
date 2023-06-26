
This tutorial covers the lineshape calculation part of the code. The goal will be to go beyond simple perturbation theory and understanding what changes in the phonon spectral quantities when 


# Lineshape Introduction

In the perturbation theory approach (see the thermal conductivity lecture), the phonons are well defined quasiparticles, with their frequencies being only slightly shifted and broadened  due to their interactions, keeping a Lorentzian representation by construction. In that case, the phonon self-energy is given by

$$\Sigma_{\lambda} = \Delta_{\lambda} ~+~ i\Gamma_{\lambda},$$

where $\lambda = (\textbf{q}, s_q)$ denotes phonon momentum and mode (in a compact notation), $\Delta$ is a constant frequency shift and $\Gamma$ is a broadening factor evaluated using the Fermi golden rule for a specific level of interaction. If we consider 3-phonon interactions, for example, it is given by

$$\Gamma_{\lambda} = \frac{\hbar \pi}{16} \sum_{\lambda' \lambda''} \left| \Phi_{\lambda \lambda' \lambda''} \right| \left[ \left( n_{\lambda'} + n_{\lambda''} + 1 \right) \delta \left( \omega_{\lambda} - \omega_{\lambda'} - \omega_{\lambda''} \right) + 2 \left( n_{\lambda'} - n_{\lambda''} \right)  \delta \left( \omega_{\lambda} - \omega_{\lambda'} + \omega_{\lambda''} \right) \right] $$

i.e. it's evaluated at the harmonic phonon frequencies, with the 3-phonon matrix elements

$$\Phi_{\lambda, \lambda', \lambda''} = \sum_{ijk} \sum_{\alpha \beta \gamma} \frac{\epsilon^{i \alpha}_{\lambda} \epsilon^{j \beta}_{\lambda'} \epsilon^{k \gamma}_{\lambda''}}{\sqrt{m_i m_j m_k} \sqrt{\omega_{\lambda} \omega_{\lambda'} \omega_{\lambda''}}} \Phi^{\alpha \beta \gamma}_{ijk} \exp(i \textbf{q}\cdot\textbf{r}_i +  \textbf{q'}\cdot\textbf{r}_j + i \textbf{q''}\cdot\textbf{r}_k )$$

dictating the strength of the interaction. We therefore only need the second and third order force constants to calculate it. 

In general, however, this is not the case: the self energy (and, consequently, the related quantities) is frequency dependent and is written as

$$\Sigma_{\lambda}(\Omega) = \Delta_{\lambda}(\Omega) ~+~ i\Gamma_{\lambda}(\Omega)$$

where $\Delta_{\lambda}(\Omega)$ and $\Gamma_{\lambda}(\Omega)$ are the now frequency dependent real and imaginary part (phonon shift and lineshape) of the phonon self-energy.

This generalization is necessary since for cases with strong interactions (large anharmonic effects) phonons can substantially deviate from the harmonic picture and are no longer a well defined quasiparticle - the phonon picture is broken. An example of this is the fact that in inelastic neutron scattering experiments this deviation from the Lorentzian behaviour is sometimes observed (see [Li, C.W. et al., Physical review letters 112 (17), 175501] for an example on PbTe). In that case, the one-phonon neutron cross section $\sigma_{\lambda}$ takes on a more general form, and we no longer talk about a linewidth (since the phonon distribution is no longer a single peaked and broadened one) but instead of a lineshape. 

To see what's happening, we start by noting that $\sigma_{\lambda}$ is written in general as

$$\sigma_{\lambda} \propto \frac{2 \omega_{\lambda} \Gamma_{\lambda}(\Omega)}{\left[ \Omega^2 - \omega^2_{\lambda} - 2 \omega_{\lambda} \Delta_{\lambda}(\Omega) \right]^2 + 4 \omega^2_{\lambda} \Gamma^2_{\lambda}(\Omega)}$$

where $\hbar\Omega$ is the energy of the probing neutron. In short, it represents the probability of exciting a phonon with energy $\hbar\Omega$ and momentum $\bf{q}$ in band s given a perturbing neutron of same energy and momentum. By probing through an energy range, what we obtain can be seen as the one-phonon spectral function, a distribution that is peaked at certain frequencies that correspond to the phonon frequencies. 

In the case of non-interacting phonons this distribution reduces to a Dirac delta function and is therefore unbroadened (the phonons have infinite lifetime and once excited keep propagating forever), while for cases with small interactions it reduces to the Lorentzian distribution as one would expect. In general, however, this distribution can have multiple satellite peaks besides the main phonon frequency one, and it is in those cases that the phonon picture is broken - the phonon is no longer a well defined quasiparticle, despite us being able to still write all wanted quantities in terms of phonons. Calculating this cross-section can therefore be used as a means to check for strong anharmonic effects by observing how much it deviates from a Lorentzian distribution.

In the case where anharmonicity is induced by 3-phonon interactions, the imaginary part of the self-energy is now given in perturbation theory by

$$\Gamma_{\lambda}(\Omega) = \frac{\hbar \pi}{16} \sum_{\lambda' \lambda''} \left| \Phi_{\lambda \lambda' \lambda''} \right|^2 \left\{ \left( n_{\lambda'} + n_{\lambda''} + 1 \right)\delta\left( \Omega - \omega_{\lambda'} - \omega_{\lambda''} \right) + \left( n_{\lambda'} - n_{\lambda''} \right) \left[ \delta\left( \Omega - \omega_{\lambda'} + \omega_{\lambda''} \right) - \delta\left( \Omega + \omega_{\lambda'} - \omega_{\lambda''} \right)\right] \right\}~, $$

i.e. it's now a frequency dependent quantity. This is the main quantity calculated by the lineshape part of TDEP. The real part of the self-energy can then be easily calculated via Kramers-Kronig transforming the imaginary part:

$$\Delta_{\lambda}(\Omega) = \frac{1}{\pi} \int \frac{\Gamma_{\lambda}(\omega)}{\omega - \Omega} d\omega~.$$

With these two quantities in hand we can therefore build the phonon spectral representation $\sigma_{\lambda}$. The phonon density of states (DOS) can be then obtained from $\sigma_{\lambda}$ by integrating over the full Brillouin zone:

$$g_s(\Omega) = \frac{(2\pi)^3}{V} \int_{BZ} \sigma_{\textbf{q} s}(\Omega) d\textbf{q}~.$$

# Preparation 

- Have a converged set of 2nd and 3rd order force constants and all related files (if you've just finished an example of this calculation, renaming or soft-linking the forceconstant files from outfile to infile is sufficient).
- Have this data for a wide enough set of temperatures (choose somewhere between 100K and 1300K, as long as it includes one temperature on the lower end and another on the higher end).
- Make sure you can parse files in hdf5 format (h5py for example, if you're using Python) and you have access to a plotting tool (matplotlib for example, if you're using Python).

# Steps

The lineshape executable is composed by 4 different calculation modes, of which we'll explore 3: --highsymmetrypoint, for which the phonon spectral function is calculated for a single high-symmetry point of the crystal; --path, for which this is done now for a path in reciprocal-space along the first Brillouin zone of the crystal; and --grid, in which a grid is generated for the full Brillouin zone and which allows us not only to get spectral quantities but also fully integrated ones like the thermal conductivity (see extra tutorial for more on this).

## Highsymmetrypoint

-  One of the most common uses for this part of the code are Raman applications, where the lineshape at the Gamma point is the only one necessary. In order to calculate it, we run the command

```
mpirun /path/to/TDEP/bin/lineshape --highsymmetrypoint GM --temperature T -qg N N N
```

replacing T for the corresponding temperature of your sampling and adding the proper path to the TDEP binaries. The flag -qg (standing for --qpoint_grid) defines the density of the q-point mesh for Brillouin zone integrations, and the number N therefore needs to be converged.

-  After running, a file named `outfile.phonon_self_energy.hdf5` will be created. This file contains all the information pertaining not only to the real and imaginary parts of the self-energy, but also contains the computed values for the spectral function for each phonon mode. In order to access this, we have to be able to read hdf5 format files. A snippet for Python with hdf5 is provided below:
```
import h5py as h5
import numpy as np

# Open the file
f = h5.File("outfile.phonon_self_energy.hdf5", "r")

# Select the relevant group
anharmonic = f.get("anharmonic")

# Get the frequency axis and the intensity of the spectral function per mode per frequency
frequency = np.array(anharmonic.get("frequency"))
spectralfunction_per_mode = np.array(anharmonic.get("spectralfunction_per_mode"))
```

-  We now have access to the spectral function for each of the phonon modes and the frequency grid. Before proceeding to the plotting, we can first inspect these objects. Start by looking at the first 3 arrays inside spectralfunction_per_mode. What do you see? Is this a general feature? Why? What would happen if instead we ran the calculation at the X point? (Try it out!)

-  You can now plot the spectral function for each of the modes and for all of your temperatures. What do you notice as temperature increases? Is the phonon picture preserved in all cases? Are all modes equally interacting? Is this the same for all systems?

## Path

-  This section of the code is very important as it allows us to focus on specific parts of the Brillouin zone (usually the 1st Brillouin zone). It is the calculation mode that we run when we want to add the effects of the lineshape into our phonon dispersion relations, and in this way show visually how the bands broaden and potentially mix.

-  To run this calculation mode, we do
```
mpirun /path/to/tdep/bin/lineshape --path -qg N N N --temperature T 
```

where again we have to replace T by the temperature we sampled at, add our path to the TDEP binaries and converge our q-point grid. This mode allows us to define a specific path along the Brillouin zone, with the default being the same one as in the phonon dispersion relations (along the high symmetry points of the crystal). 

![[Brillouin_Zone_(1st,_FCC).svg.png | center |  256x256]]



A different path can be specified via the flag --readpath, which will make TDEP read the q-point path from the infile.qpoints_dispersion file. The number of q-points between each high-symmetry point can be tuned via the flag -nq (--nq_on_path, default is 100) for a denser grid. An example file would be
```
FCC                         ! Bravais lattice type
  100                       ! Number of points on each path
    4                       ! Number paths between special points
GM  X                       ! Starting and ending special point
X   U                       !
K   GM                      !
GM  L                       !
```

or, if you want more customization,

```
CUSTOM                      !
  100                       ! Number of points on each path
    4                       ! Number paths between special points
0.000 0.000 0.000   0.000 0.500 0.500 GM X
0.000 0.500 0.500   0.000 0.625 0.375 X  U
0.375 0.750 0.375   0.000 0.000 0.000 K  GM
0.000 0.000 0.000   0.000 0.500 0.000 GM L
```

- After the calculation finishes two new files will be created: a lighter one named `outfile.dispersion_relations.hdf5` and a heavier one named `outfile.phonon_spectral_function.hdf5`. For this tutorial we'll be interested in the latter, but make sure to also explore the first. Again, we'll need a way to read hdf5 format files, for which a similar snippet as before works:

```
import h5py as h5
import numpy as np

# Open the file
f = h5.File("outfile.phonon_spectral_function.hdf5", "r")

# Get the axes 
x = np.array(f.get("q_values"))
y = np.array(f.get("energy_values"))

# Get the intensities
gz = np.array(f.get("spectral_function"))
```

- We now have the frequency dependent phonon spectral function for the first Brillouin zone! This can be now used to plot the phonon dispersion relations with the effects of the lineshape for our chosen temperature displayed. In order to do so, we can resort to the following snippet (continuing from the one above):

```
# Add a little bit so that the logscale does not go nuts
gz=gz+1E-2

# For plotting, turn the axes into 2d arrays
gx, gy = np.meshgrid(x,y)

plt.pcolormesh(gx, gy, gz, norm=LogNorm(vmin=gz.min(), vmax=gz.max()), cmap='viridis')

# Set the limits of the plot to the limits of the data
plt.axis([x.min(), x.max(), y.min(), y.max()])

plt.show()
```

This will result in a plot like the following (Add colour bar?)

![[Figure_1.png | center | 500x400]]


- We can now repeat this procedure for our temperature range. What do you see changing? Why?


## Extras

### Convergence Procedure

### Brief introduction to the --grid calculation mode

### Longer tutorial on the --grid calculation mode


# Thermal Conductivity (starting to be long, maybe have the more theoretical parts on side for whoever is interested)

To obtain the thermal conductivity outside of a well-defined phonon picture, we start by considering the Green-Kubo formula for linear response:

$$\kappa_{\alpha \beta} = \frac{V}{k_B T^2} \int^{\infty}_0 \langle J_{\alpha}(t)J_{\beta}(0)\rangle dt $$

where V is the system volume (in the formal sense we take the limit to infinite volume, in practice it's the supercell volume), $k_B$ is Boltzmann's constant, T is the temperature and J is the heat current, representing the energy flux through the system due to the phonons. This represents a fluctuation-dissipation relationship, where the system's macroscopic ability to carry heat is determined by the fluctuations of the heat current at a microscopic level.

The first thing to consider is the meaning behind the thermal average $\langle ... \rangle$, the key quantity to calculate $\kappa_{\alpha \beta}$. As this thermal average depends on which ensemble is being considered, it is very tightly related to which kind of simulations are being performed in order to calculate it. If we can, for example, perform simulations in a way where the ensemble is the full quantum one (e.g. using PI-MD), then $\langle ... \rangle$ is a Kubo correlation-function and has encoded the full quantum behaviour of the fluctuations. If, on the other hand, our simulations realize a classical ensemble (e.g., using classical MD), then $\langle ... \rangle$ represents a classical correlation function and the quantum behaviour of the fluctuations is not accessible.

A half-way compromise between the two is also possible to obtain, by performing classical level simulations but considering quantum phonon occupations (Bose-Einstein instead of Boltzmann distribution). In that case, $\langle ... \rangle$ represents what is usually called a greater Green's function, defined as 

$$G^{>}_{XY} = -i \langle X(t) Y^{\dagger}(0) \rangle$$

where X and Y are two operators in the Heisenberg representation and the dagger represents hermitian conjugation. In this representation of the heat current autocorrelation, some of the quantum character of the fluctuations can be recovered despite the usage of classical simulations.

In order to evaluate $\kappa$, we start by writing the expression for the heat current in terms of phonon operators (derive this as well?):

$$\bf{J}(t) = \frac{1}{2V} \sum_{\bf{q} s_1 s_2} \omega_{\bf{q} s_1} \bf{v}_{\bf{q} s_1 s_2} B_{q s_1}(t) A_{\bar{q} s_2}(t)$$

Here $\bf{v}$ are the off-diagonal phonon group velocities and couple phonons with the same momentum in different bands, while B and A are the momentum and displacement operators in the phonon representation.

Substituting $J$ into the Green-Kubo equation we obtain

$$\kappa_{\alpha \beta} = \frac{1}{4k_BT^2V} \sum_{\bf{q} s_1 s_2} \sum_{\bf{q'} s_3 s_4} \omega_{\bf{q} s_1} \omega_{\bf{q'} s_2} \bf{v}_{\bf{q} s_1 s_2} \otimes \bf{v}_{\bf{q'} s_3 s_4} \int^{\infty}_0 \langle B_{\bf{q} s_1}(t) A_{\bf{\bar{q}} s_2}(t) B_{\bf{q'} s_3} A_{\bf{\bar{q}'} s_4} \rangle ~dt$$

where the phonon displacement and momentum operators without time argument are at t=0. 

Just as in the Peierls-Boltzmann formulation of thermal conductivity, the phonon frequencies and group velocities are directly related to the second-order force constants, and can therefore be calculated immediately once they have been determined. The thermal conductivity problem is then reduced to the evaluation of the correlation function $\langle ... \rangle$.

The correlation function shown above corresponds to a 2-phonon correlation function. In order to make in manageable, we use the thermal average's version of the famous Wick's theorem, which tells us that if our anharmonicity/phonon-interaction is weak (more technically, if the ensemble is Gaussian or very close to it) we can decouple the correlation function as 

$$\langle B_{\bf{q} s_1}(t) A_{\bf{\bar{q}} s_2}(t) B_{\bf{q'} s_3} A_{\bf{\bar{q}'} s_4} \rangle \simeq \langle \rangle  \langle \rangle \delta \left(  \right)$$ 
