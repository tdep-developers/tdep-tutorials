Stochastic sampling with TDEP: sTDEP
===

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

## Outline

- [Example on MgO](./01_MgO/README.md)
- [Convergence tutorial](./02_convergence/README.md)
- [BCC zirconium at 1300K: dynamical stabilization](./03_Zr/README.md)

## General comment on Convergence

**You should always check the convergence of the property you are interested in! We cannot stress this enough!**

On purely harmonic level, this can be the density of states (DOS). Compare the bandstructure and DOS at each step in the self-consistent loop.


## Suggested reading

- [N. Shulumba, O. Hellman, and A. J. Minnich, Phys. Rev. B **95**, 014302 (2017)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.95.014302)
- Appendix of [N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)
