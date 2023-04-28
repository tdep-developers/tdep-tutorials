# TDEP basics
In this initial tutorial we will cover the basics of the TDEP method, using fcc Al as a simple example. ....

[Schematic overview/intro to TDEP method]

```math
 U_{TDEP} = U_{0} + \frac{1}{2}\sum_{ij\alpha\beta} \Phi_{ij}^{\alpha \beta}  u_{i}^{\alpha}u_{j}^{\beta}  + \frac{1}{3!}\sum_{ijk\alpha\beta\gamma} \Phi_{ijk}^{\alpha \beta \gamma}  u_{i}^{\alpha} u_{j}^{\beta} u_{k}^{\gamma} 
    +  ...
```
# fcc Al 


[Describe how to download provided infiles]

The following input files are required:
- **infile.ucposcar**: Defines the primitive cell of your system (lattice vectors and equilibrium positions), in the VASP POSCAR format. 
- **infile.ssposcar**: Defines the supercell ....
- **infile.positions**: ...
- **infile.forces**: ...
- **infile.meta**: ...

See http://ollehellman.github.io/page/files.html for detailed description.

### Extracting force-constants


### Plotting dispersion and DOS



### Convergence:

Supercell size+cutoffs, number of samples



### References:
- [[1] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
