# TDEP basics


[Schematic overview/intro to TDEP method]

```math
 U_{TDEP} = U_{0} + \frac{1}{2}\sum_{ij\alpha\beta} \Phi_{ij}^{\alpha \beta}  u_{i}^{\alpha}u_{j}^{\beta}  + \frac{1}{3!}\sum_{ijk\alpha\beta\gamma} \Phi_{ijk}^{\alpha \beta \gamma}  u_{i}^{\alpha} u_{j}^{\beta} u_{k}^{\gamma} 
    +  ...
```

...

# fcc Al 

In this initial tutorial we will cover the basics of the TDEP method, using fcc Al as a simple example. ....

[Describe how to download provided infiles]

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

[Desribe things to look out for:  R^2, overdetermination ratio, ...]

### Plotting dispersion and DOS

phonon_dispersion_relations

[Show how to specify path through BZ]

### Convergence:

[Supercell size+cutoffs, number of samples]
[plot FC norms]
[Probable provide data for different supercell sizes? some classical potential?]

### Including higher order terms

[Briefly describe the sequential fitting.]

extract_forceconstants -rc2 5 -rc3 X

[lineshape ...]

# Some second a bit more complicated example. Something with the wurtzite structure?

To show: basic LO-TO splitting? provide Born charges and dielectric tensors
Relaxation of internal positions? from FC1 or averaged from MD?

### References:
- [[1] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
