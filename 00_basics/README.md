# TDEP basics

This tutorial will introduces the basics of the TDEP method. It covers how to obtain effective second order interatomic forceconstants (IFCs) from position-force data from and ab initio molecular dynamics (AIMD) simulation and how to then extract phonon dispersion relations, density of states and the vibrational free energy from these.

The first test case will be Si, and the required input files are provided in the TODO directory. The dataset is from a short AIMD run at 300 K using a 64 atom supercell. Please note that this data is not meant to provida quantitatively converged results. For real production calculations, relevant convergence paramters should be carefully checked. In particular, a 64 atom supercell is likely to small to provide converged results for most systems.

- **infile.ucposcar**: Defines the primitive cell of your system (lattice vectors and equilibrium positions), in the VASP POSCAR format. 
- **infile.ssposcar**: Defines the supercell of your system (lattice vectors and equilibrium positions), for which the position-force dataset was produced, in the VASP POSCAR format. 
- **infile.positions and infile.forces**: Contains the position and force data, respectively. In this particular example from an AIMD run at 300 K.
- **infile.meta**: Contains certain relevant metadata.
- **infile.stat**: 

See https://ollehellman.github.io/page/files.html for a detailed description of the content of these input files. 

## Extracting forceconstants

In a directory containing all of the above input files, second order effective force constants can be extracted using the command 

`extract_forceconstant -rc2 100 -s 50 > fc2.log`. 

A least-squares solution for the set of second order IFCs that best fit the position-force data (in `infile.{positions,forces}) will then be performed. Schematically, the program solves for the set IFCs:

```math
\mathbf{\Phi} = argmin_{\Phi} ... TODO
```
Before the fit is performed, the number of indepedent IFCs are reduced by enforcing the appropriate symmetries. These include the symmetries of the crystal being considered, as well as general translational and rotational invariances. This typically drastically reduces the number of IFCs that need to be fit. See https://ollehellman.github.io/program/extract_forceconstants.html or Refs. [TODO] for more details on how this is practically done.

Some notes:
- The option `-rc2 X` specfies the interaction cutoff for the second order IFCs, i.e. only interactions between pairs of atoms less than a distance X apart will be considered.
- Specyfing a large number, such as ` -rc2 100 `, will force the largets possible cutoff that fits in `infile.ssposcar` to be used. Similarily, you may specify a small number (eg. 0) to force only first nearest neighbor interactions to be included.
- This cutoff-distance is an important convergence parameter to check. After completing the (this and other) tutorials, consider going back and calculate eg. phonon dispersion relations for different `rc2` values and try to get a feeling for how this affect things.
- The option `-s 50` instructs that we will only use every 50:th sample from `infile{positions,forces}`. The number of samples used in the fit is another important convergence-parameter, note that closely spaced samples along an MD trajectory are highly correlated.

Have a look through the ouput of `extract_forceconstant`, redirected into `fc2.log` in this case. Several usefull things are printed. Try to find the following:
- The minimum (nearest neighbor distance) and maximum cutoffs for the current structure and supercell.
- The total number of (irreducible) second order IFCs that were fitted.
- The total number of equations that were used to in the fit (how would you calculate this number?).
- The `R^2` of the fit, which is a measure of how well the obtained effective harmonic IFCs describes the position-force data.


Two output files should have been produced:

- `outfile.forceconstant`, containing the full second order IFCs
- 'outfile.irrifc_secondorder' containing a list of the irreducible second order IFCs. 

## Phonon dispersion relations and density of states (DOS)

For further processing `outfile.forceconstant` needs to be copied or symlinked into `infile.forceconstant`:

`ln -s outfile.forceconstant infile.forceconstant`

Now, to use these IFCs to produce a phonon dispersion relation, simply run 

`phonon_dispersion_relations`

This produces a set of output files. Most important for us is the 'outfile.dispersion_relations' which contains the dispersion data. A convenient '.gnuplot' file is also produced so that the dispersion may be plotted simply by running:

`gnuplot --persists outfile.dispersion_relations.gnuplot`

Confirm that this dispersion relation corresponds to what you expect the phonon dispersion relation of Si to look like by eg. comparing to the litterature. 

To also obtain the phonon DOS, simply add the `--dos`:

`phonon_dispersion_relations --dos`

Similarily, this produces a gnuplot script which can be used to view the DOS:

`gnuplot --persist outfile.phonon_dos.gnuplot`


Some note:
- If no Brillouin Zone (BZ) path is speecified (like in the case above), a default one for the space-group under consideration will be used. You can specify a custom BZ path by providing an `infile.qpoints_dispersion` file ( see format https://ollehellman.github.io/page/files.html#infile.qpoints_dispersion ) and the `--readpath` option.
- TODO Something about BZ q-grid, smearing etc


## Phonon free energy

The phonon free energy may be calulcated through the `--temperature` (single temperature) or `--temperature_range` (range of temperature) options to `phonon_dispersion_relations`. For example, to obtain the phonon free energy for a range of 50 temperatures between 0 and 1000 K you may run:

`phonon_dispersion_relations --temperature_range 0 1000 50` 

This will produce a file `outfile.free_energy` which contains the temperature, phonon free energy, vibrational entropy and heat capacity. To plot the phonon free energy in eg. gnuplot run eg. `plot "outfile.free_energy" u 1:2 w l`

Some notes:
- TODO Something about BZ q-grid convergence, smearing etc

TDEP phonon thermodynamics will be covered in more detail in tutorial TODO. 

## Higher order IFCs

`extract_forceconstants` can also be used to extract higher order IFCs. To also obtain the third-order IFCs, within a cutoff of 4 Å, run

`extract_forceconstants -rc2 100 -rc3 4 -s 50 > fc2_fc3.log`

This will, in addition to the `outfile.forceconstant` file, write a `outfile.forceconstant_thirdorder` containing the third order IFCS, file. 

Again, Some usefull information is printed in the log file:
- How many third order IFCs were fitted?
- Do you see an improvement on R^2 by also including the third order IFCs in the fit?


What you can do with these third order IFCs will be coverd in Tutorials TODO and TODO.

## A second example: GaN
TODO: Just tell them to do everything again + show how to include LO-TO splitting. Providing a infile.lotosplitting file.













## OLD STUFF

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