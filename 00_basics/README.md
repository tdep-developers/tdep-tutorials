# TDEP basics

This tutorial will introduces the basics of the TDEP method. It covers how to obtain effective forceconstants from position-force data from and ab initio molecular dynamics simulation and how to then extract phonon dispersion relations, density of states and the vibrational free energy from these.

The first test case will be Si, and the required input files are provided in the TODO directory.

The se
- **infile.ucposcar**: Defines the primitive cell of your system (lattice vectors and equilibrium positions), in the VASP POSCAR format. 
- **infile.ssposcar**: Defines the supercell of your system (lattice vectors and equilibrium positions), for which the position-force dataset was produced, in the VASP POSCAR format. 
- **infile.positions and infile.forces**: Contains positions and forces of for 
-  ...
- **infile.meta**: ...

See https://ollehellman.github.io/page/files.html for a detailed description of the content of these input files. 


-Schematic overview/intro to TDEP method

```math
 U_{TDEP} = U_{0} + \frac{1}{2}\sum_{ij\alpha\beta} \Phi_{ij}^{\alpha \beta}  u_{i}^{\alpha}u_{j}^{\beta}  + \frac{1}{3!}\sum_{ijk\alpha\beta\gamma} \Phi_{ijk}^{\alpha \beta \gamma}  u_{i}^{\alpha} u_{j}^{\beta} u_{k}^{\gamma} 
    +  ...
```

...

# fcc Al 

In this initial tutorial we will cover the basics of the TDEP method, using fcc Al as a simple example. ....

-Describe how to download provided infiles

The following input files are required:
- **infile.ucposcar**: Defines the primitive cell of your system (lattice vectors and equilibrium positions), in the VASP POSCAR format. 
- **infile.ssposcar**: Defines the supercell ....
- **infile.positions**: ...
- **infile.forces**: ...
- **infile.meta**: ...

See http://ollehellman.github.io/page/files.html for detailed description.

### Extracting force-constants

extract_forceconstants -rc2 5

....

-Describe things to look for: Number of FCs, R^2 of fit, overdetermination ratio, ...

### Plotting dispersion and DOS

phonon_dispersion_relations

-Show how to specify path through BZ

### Get a free energy

### Mention Canonical sampling


### Convergence:

-Supercell size+cutoffs, number of samples
-plot FC norms
-Probable provide data for different supercell sizes? some classical potential?

### Including higher order terms

-Briefly describe the sequential fitting.

extract_forceconstants -rc2 5 -rc3 X

lineshape ...

# Some second a bit more complicated example. Something with the wurtzite structure?

To show: basic LO-TO splitting? provide Born charges and dielectric tensors
Relaxation of internal positions? from FC1 or averaged from MD?

# Introducing the stochastic TDEP version? Here or in another tutorial?

### References:
- [[1] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
