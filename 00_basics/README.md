# TDEP basics

This tutorial will introduces the basics of the TDEP method. It covers how to obtain effective second order interatomic forceconstants (IFCs) from position-force data from an ab initio molecular dynamics (AIMD) simulation and how to then extract phonon dispersion relations, density of states and the vibrational free energy.

The first test case will be Si. The dataset is from a short AIMD run at 300 K using a 64 atom supercell. Please note that this data is not meant to provide quantitatively converged results. For real production calculations, relevant convergence parameters should be carefully checked. In particular, a 64 atom supercell is likely too small to provide converged results for most systems.
 
The following required input files are provided in the `Si_infiles` directory:
- **infile.ucposcar**: Defines the primitive cell of your system (lattice vectors and equilibrium positions), in the VASP POSCAR format. 
- **infile.ssposcar**: Defines the supercell of your system (lattice vectors and equilibrium positions), for which the position-force dataset was produced, in the VASP POSCAR format. 
- **infile.positions and infile.forces**: Contains the position and force data, respectively. In this particular example from an AIMD run at 300 K.
- **infile.meta**: Contains certain relevant metadata.
- **infile.stat**: Contains additional data from the AIMD run. 

See https://tdep-developers.github.io/tdep/files/ for a detailed description of the content of these input files. 

## Extracting forceconstants

In a directory containing all of the above input files, second order effective force constants can be extracted using the command 

`extract_forceconstants -rc2 100 -s 50 > fc2.log`. 

A least-squares solution for the set of second order IFCs that best fit the position-force data (in `infile.{positions,forces}) will then be performed. Before the fit is performed, the number of independent IFCs are reduced by enforcing the appropriate symmetries. These include the symmetries of the crystal being considered, as well as general translational and rotational invariances. This typically drastically reduces the number of IFCs that need to be fit. See https://tdep-developers.github.io/tdep/program/extract_forceconstants/ or Ref. [1] for more details on how this is practically done.

A few notes:
- The option `-rc2 X` specifies the interaction cutoff for the second order IFCs, i.e. only interactions between pairs of atoms less than a distance X apart will be considered.
- Specifying a large number, such as ` -rc2 100 `, will force the largest possible cutoff that fits in `infile.ssposcar` to be used. Similarly, you may specify a small number (eg. 0) to force only the first nearest neighbor interactions to be included.
- This cutoff distance is an important convergence parameter to check. After completing this and other tutorials, consider going back and calculate eg. phonon dispersion relations for different `rc2` values and try to get a feeling for the effect.
- The option `-s 50` instructs that we will only use every 50:th sample from `infile{positions,forces}`. The number of samples used in the fit is another important convergence-parameter, note that closely spaced samples along an MD trajectory are highly correlated.

Have a look through the output of `extract_forceconstant`, redirected into `fc2.log` in this case. Several useful things are printed. Try to find the following:
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

`gnuplot --persist outfile.dispersion_relations.gnuplot`

Confirm that this dispersion relation corresponds to what you expect the phonon dispersion relation of Si to look like by eg. comparing to the literature. 

To also obtain the phonon DOS, simply add the `--dos` option:

`phonon_dispersion_relations --dos`

Similarly, this produces a gnuplot script which can be used to view the DOS:

`gnuplot --persist outfile.phonon_dos.gnuplot`


A few notes:
- If no Brillouin Zone (BZ) path is specified (like in the case above), a default one for the space-group under consideration will be used. You can specify a custom BZ path by providing an `infile.qpoints_dispersion` file ( see format https://tdep-developers.github.io/tdep/files/ ) and the `--readpath` option.
- The BZ grid and the smearing method and related parameters are influential on the resulting DOS. These may be edited using switches to `phonon_dispersion_relations`. Run the command `phonon_dispersion_relations -h` and spend some time looking through what your options are.


## Phonon free energy

The phonon free energy may be calculated through the `--temperature` (single temperature) or `--temperature_range` (range of temperature) options to `phonon_dispersion_relations`. For example, to obtain the phonon free energy for a range of 50 temperatures between 0 and 1000 K you may run:

`phonon_dispersion_relations --temperature_range 0 1000 50` 

This will produce a file `outfile.free_energy` which contains the temperature, phonon free energy, vibrational entropy and heat capacity. To plot the phonon free energy in eg. gnuplot run eg. `plot "outfile.free_energy" u 1:2 w l`

TDEP phonon thermodynamics will be covered in more detail in tutorial TODO. 

## Higher order IFCs

`extract_forceconstants` can also be used to extract higher order IFCs. To also obtain the third-order IFCs, within a (for example) cutoff of 4 Å, run

`extract_forceconstants -rc2 100 -rc3 4 -s 50 > fc2_fc3.log`

This will, in addition to the `outfile.forceconstant` file, write a `outfile.forceconstant_thirdorder` containing the third order IFCS, file. 

Again, some useful information is printed in the log file:
- How many third order IFCs were fitted?
- Do you see an improvement on R^2 by also including the third order IFCs in the fit?


What you can do with these third order IFCs will be covered in upcoming tutorials.

## A second example: GaN

A second set of input files for GaN is provided in the `GaN_infiles` directory. Here we will simply repeat the above procedure to obtain phonon dispersion relations and dos for GaN. However, since GaN is a polar material, we will additionally include the effect of long-range electrostatics, resulting in the well known LO-TO splitting. This requires knowing the dielectric tensor and Born effective charges. These are provided in the `infile.lotosplitting` file, in the format specified here: https://ollehellman.github.io/page/files.html .

To include long-range electrostatics in the fit, simply add the `--polar` option to `extract_forceconstants`:

`extract_forceconstants -rc2 100 --polar -s 50 > fc2_polar.log`


Full details on how the long-range electrostatic interactions are included in the TDEP fit can be found in Ref. [2].

Repeat the procedure you performed for Si to obtain phonon dispersion relations and DOS for GaN and compare the obtained results to the literature to confirm they are what you would expect. 



### References:
- [[1] O. Hellman, P. Steneteg, I.A. Abrikosov and S.I. Simak, Phys. Rev. B **87** 104111 (2013)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.87.104111)
- [[2] N. Benshalom, G. Reuveni, R. Korobko, O. Yaffe, and O. Hellman, Phys Rev Mater **6**, 033607 (2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.033607)
