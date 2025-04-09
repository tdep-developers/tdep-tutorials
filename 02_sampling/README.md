Sampling with TDEP
===

TDEP stands for Temperature Dependent Effective Potential, with the important word being *Temperature*.
This means that the force constants extracted with TDEP will already contains information about the canonical ensemble.
In practice, these force constants have to be extracted from configurations representative of the canonical ensemble **at the temperature at which you want to extract properties**.
Yet another way to say this is that these IFC are a thermal average.

This means that an important part of using TDEP is to gather the configurations before extracting IFCs.


Two main approaches exists: using molecular dynamics simulations or a stochastic sampling (sTDEP).


**IMPORTANT NOTES:**
- the theoretical foundation of MD-TDEP and sTDEP are different, be very careful when comparing results from the two approaches (and don't mix them blindly in the same study !).
- You cannot mix configurations from several temperature when extracting the IFCs, this has no physical sense in the TDEP approach



# TDEP with molecular dynamics

The idea is simple: molecular dynamics gives us access to a representative sample of the canonical ensemble.
Using the forces and displacements from this sample, we can fit **the best effective harmonic phonons** to reproduce the *actual* canonical ensemble explored by the system.

More formally, this approach is an application of [the mode-coupling theory of anharmonic lattice dynamics](https://doi.org/10.1063/5.0174255).
You should have a read of this paper if you want to understand the underlying theory.

Some important consideration when using TDEP with molecular dynamics:
- **The molecular dynamics simulations have to be in the NVT ensemble !**. This is because we cannot define displacements with a varying cell.
- **Do not mix simulations at several temperatures**. This completely breaks down the theoretical justification and the phonons would not have a clear physical meaning anymore.

You will find a tutorial on how to use molecular dynamics to extract IFCs in the folder [`MD-TDEP`](./MD-TDEP).



# Stochastic sampling with TDEP: sTDEP

Molecular dynamics can be expensive (particularly when ab initio method are used) and do not give access to nuclear quantum effects.
The stochastic sampling approach allows to reduce the number of configurations used and can also include part of the nuclear quantum effects.

Briefly put, the idea is to generate force constants self-consistently by using them to approximate the atomic displacement distribution in the (harmonic) canonical ensemble, and iteratively improve the approximation by true forces in the system. [Check out the documentation of `canonical_configuration` for some background.](http://ollehellman.github.io/program/canonical_configuration.html) The scheme was first introduced in [[Shulumba2017]](#suggested-reading) and we refer to it as _stochastic TDEP_ (sTDEP).

In the classical case and very simplified mathematical terms, we solve this equation self-consistently for the force constants $\Phi$:

$$
\begin{align}
\langle V_2 \rangle
&= \int {\rm d} R ~ {\rm e}^{- \beta V({\bf R})} V_2 ({\bf R}) \\
&{\color{red} \approx}
\int {\rm d} R ~ {\rm e}^{- \beta {\color{red} V_2} ({\bf R}) } V_2 ({\bf R})~,
\end{align}
$$

where

$$
\begin{align}
V_2({\bf R}) = \frac{1}{2} \sum_{ij} \Phi_{i \alpha, j \beta}({\bf R^0})U^{i \alpha} U^{j \beta}~,
\end{align}
$$

i.e., instead of sampling the true nuclear distribution as it would be obtained with MD simulations (at much higher cost!), we sample the approximate (effective) harmonic distribution and update the force constants self-consistently after each iteration until convergence. The solution will correspond to the (effective) harmonic model that best mimics the true thermodynamic behavior of the system at the given temperature (defined by $1/\beta = k_{\rm B} T$), [and gives the best trial free energy similar to self-consistent phonon schemes.](https://github.com/flokno/notes/blob/main/tdep/note_tdep_self-consistent-sampling.md)

You will find a tutorial for sTDEP in the [`sTDEP`](./sTDEP) folder.

# General comment on Convergence

**You should always check the convergence of the property you are interested in! We cannot stress this enough!**

On purely harmonic level, this can be the density of states (DOS). Compare the bandstructure and DOS at each step in the self-consistent loop. [There is an explicit example in the sTDEP tutorial](./sTDEP/02_convergence/README.md)


# Suggested reading

- [N. Shulumba, O. Hellman, and A. J. Minnich, Phys. Rev. B **95**, 014302 (2017)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.95.014302)
- Appendix of [N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
- [A. Castellano, J.P. Alvarinhas Batista, M.J. Verstraete, J. Chem. Phys. **159**, 234501 (2023)](https://doi.org/10.1063/5.0174255)

# Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)
