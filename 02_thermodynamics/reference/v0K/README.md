Computing the free energy with TDEP for Zirconium
===

This example shows how to compute free energy for bcc zirconium using TDEP when you have access to configurations.

## Steps

1. Extract force constants and the U0 correction term using `extract_forceconstants -rc 10 -U0`
2. Copy the `outfile.forceconstants` as `infile.forceconstants`
3. Extract the harmonic free energy using `phonon_dispersion_relations --dos --temperature 1300 -qg 4 4 4`
4. Compute the total free energy by adding the second terms in `outfile.free_energy` and `outfile.U0`

## Things to look out for

- Try to look at the evolution of each term with parameters
    - For the U0, try to change the number of configurations with the `--stride N` variable (with N an integer) in 1.
    - For the harmonic free energy, try to change the q-point grid integration by changing the values of the `-qg ` variable. Observe also it's evolution with the number of configurations.


## Suggested reading

- [O. Hellman, P. Steneteg, I. A. Abrikosov, and S. I. Simak, Phys. Rev. B **87**, 104111 (2013)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.87.104111)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)
- [you are familiar with using the so3krates force field (or have your own potential at hand)](https://github.com/tdep-developers/tdep-tutorials/tree/main/00_preparation/potential_energy_surfaces)
