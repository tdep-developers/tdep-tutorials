Computing the equilibrium volume of bcc Zirconium at high temperature
===

This example shows how to compute equilibrium volume of bcc Zr using the equation of state fitting method.
For this, harmonic free energy and U0 computed with sTDEP are provided (in the `outfile.U0` and `outfile.free_energy` files), with a total of 12 iterations per volume.

## Steps

1. Choose an iteration
2. Extract the total free energy of each volume at this iteration, and put it in a `eos_data.dat` file. For this, you can modify and use the `get_eos_data.py` script.
3. Fit a Vinet equation of state using the `fit_eos.py` script. Note that because of statistical noise, the fit might not work for some iterations without enough data !
4. Repeat for a different iteration.

## Things to look out for

- Observe how the fitted volume (and lattice parameter) evolve with the number of iterations.
- How many iterations are necessary to converge the volume of this system at this temperature ?
- Compare your result to the lattice parameter computed at 0K (3.58 angstrom). (Note : the lattice parameter for a bcc crystal is given by $a = (2 V)^{1/3}$.)


## Suggested reading

- [O. Hellman, P. Steneteg, I. A. Abrikosov, and S. I. Simak, Phys. Rev. B **87**, 104111 (2013)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.87.104111)

## Prerequisites

- [TDEP is installed](http://ollehellman.github.io/page/0_installation.html)
- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
- [gnuplot is installed](http://www.gnuplot.info/)
- [you are familiar with using the so3krates force field (or have your own potential at hand)](https://github.com/tdep-developers/tdep-tutorials/tree/main/00_preparation/potential_energy_surfaces)
