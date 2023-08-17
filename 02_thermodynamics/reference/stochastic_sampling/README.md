Free energy with stochastic TDEP (sTDEP) for Zirconium
===

This example shows how to compute free energy for bcc zirconium using sTDEP.

## Steps

1. Go to the folder `iter.000` to start the sampling
2. Check the `Makefile` and the target `init`
3. `make init` to create the first 4 samples
4. compute the forces with `make compute`, this will use the So3krates potential to compute forces for the samples and create TDEP input files
5. now we can extract the forceconstants → `make fc`
6. inspect the phonon dispersion
7. create the next iteration from the current set of force constants, `make iteration`
8. move the folder `iter.001` down and `cd` there
9. repeat until convergence

## Things to look out for

- At each iteration, the harmonic free energy and the U0 correction term are computed. Look at their evolution with the number of configurations.
- After how many iteration does the total free energy stabilize ? Is it the same as for the phonon dispersion stabilization ?


## Suggested reading

- [O. Hellman, P. Steneteg, I. A. Abrikosov, and S. I. Simak, Phys. Rev. B **87**, 104111 (2013)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.87.104111)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)
- [you are familiar with using the so3krates force field (or have your own potential at hand)](https://github.com/tdep-developers/tdep-tutorials/tree/main/00_preparation/potential_energy_surfaces)
