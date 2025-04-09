sTDEP for magnesium oxide
===

This tutorial covers self-consistent TDEP, with an example for magnesium oxide, MgO.
For this tutorial, we provide the unitcell, dielectric tensor and Born effective charges for MgO, as well as a machine learning interatomic potential.


# Initializing the structure

To begin the self consistent scheme, we need to create a supercell with which will compute the forces and fit the force-constants.
For this tutorial, we will use a supercell with 216 atoms, but remember that **the size of the supercell is a property to converge**.

Start by reading the documentation of  [`generature_structure`](https://tdep-developers.github.io/tdep/program/generate_structure/).
Then, go in the folder `sampling.300K`, and copy the `infile.ucposcar` as well as the `infile.lotosplitting` files.

Now run 
```bash
generate_structure -na 216
```

This has created a file `outfile.ssposcar` with the supercell that we will use for this tutorial.
Change this file to `infile.ssposcar` using 
```bash
mv outfile.ssposcar infile.ssposcar
```

Remember that to extract force-constants, **TDEP always needs 2 reference structures: the primitive `infile.ucposcar` and the supercell `infile.ssposcar`**.

Remember that **the size of the supercell is a property to converge**.
More on this in the next tutorial.

# The self-consistent scheme

As a start, to get a feeling of the self-consistent process, we will make every steps by running the command line.
In production, it is a good idea to create scripts to automatize this process and avoid mistakes.

## Initialization

To begin the self-consistent cycle, we need initial IFC to start sampling the canonical ensemble.
Using a Debye model, TDEP can create fake force constants that will respect the symmetry of the system.

Have a read of the documentation of  [`canonical_configuration`](https://tdep-developers.github.io/tdep/program/canonical_configuration/).

In the folder `sampling.300K`, create a new folder `iter.000` and go into it.

Copy your unitcell, supercell and dielectric properties inside this folder
```bash
cp ../../infile.ucposcar ../../outfile.ssposcar ../../infile.lotosplitting .
```

Now we will create 4 configurations at 300K with a fake model having a maximum phonon frequency of 20 THz.
This can be done using the flag `--maximum_frequency 20`.
Not that this value of 20 THz was chosen because we know what to expect for the phonon dispersion of MgO.
A good value for this parameter will depend on the system being used.

To do this, run
```bash
canonical_configuration --temperature 300 --quantum -n 4 --maximum_frequency 20 --output_format 4
```
Note that we use `--output_format 4` so that the resulting configurations are in the aims format.
This is just to simplify the work for the machine-learning interatomic potential, but we could also have used Vasp (`--output_format 1`, this is the default), Abinit (`--output_format 2`) or SIESTA (`--output_format 5`).

You should now find four files `aims_conf*`, which are the configurations with atoms displaced due to the temperature, And the initialization step is done !
But before starting, it's a good idea to check the fake forceconstants, to see if they look reasonable. 
You can do this by linking the `outfile.fakeforceconstant` to `infile.forceconstant` (` ln -s outfile.fakeforceconstant infile.forceconstant`) and then running `phonon_dispersion_relations`. If its look reasonable (it doesn't have to be perfect, but the frequencies should make sense with respect to your system) then we are good to go.

## Doing a step

Now that we have initialized everything, we can perform the self-consistent cycle.

Remember that the input files to indicates what is the structure to TDEP are
* `infile.ucposcar`
* `infile.ssposcar`
* `infile.lotosplitting`

while the required input file to inform about the forces displacements and so on are
* `infile.meta`
* `infile.positions`
* `infile.forces`
* `infile.stat`

In this tutorial, we use the so3krates machine-learning potential that can already provide the forces in the infiles required by TDEP by using the `--tdep` flag.
For your applications, you will have to parse the forces on your system to create those files.

For each steps, this is what you have to do

1. Go back in `sampling.300K` and create a folder `iter.n`, with n the current step
2. Copy the input files in the new folder `iter.n`
3. Compute the forces on the configurations generated at the last step with `sokrates_compute --folder-model ../../module ../iter.n-1/aims_conf* --format=aims --tdep`. This will create the infiles with displacements and forces for TDEP (iter.n-1 is the previous iteration. So if you are in iteration 002, it should read iter.001).
4. Extract the force constants using `extract_forceconstant -rc2 10 --polar`
5. Copy the outfile force constants as an infile using `ln -sf outfile.forceconstant infile.forceconstant`
6. Compute the phonons (and/or the property you want to converge) using `phonon_dispersion_relations --dos` 
7. Check for convergence by comparing with previous iterations and exit if you are converged
8. Else, create new configurations with `canonical_configuration --temperature 300 -n X --quantum -of 4`. The number of configuration X will depend on the iteration. We found that doubling the number of configurations at each steps works well to converge will minimizing the number of configurations to generate. This means that you should have 8 configurations at the first step, 16 at the second, 32 at the third, and so on.
9. Go to the next iteration by going back to step 1

Now you can repeat these step and try to find the number of iterations necessary to converge your phonons band structure.


# Note

### Mixing configurations
To improve the convergence, it is a good idea to precondition your self-consistent cycle.
To do this, a simple approach is to use half of the configurations from the previous steps when computing the force constants, so that the force constants at step n is mixed with the results at steps n-1.

### Observe convergence
Try to observe the convergence of the self-consistent process
- At each iteration, observe how the mean-square displacement (that you can find in the log of `canonical_configuration`) evolve
- Inspect how the dispersion converges more and more
- Plot the phonon DOS per iteration. You can do it with the script `plot_dos_convergence.py` provided in the [`scripts`](../scripts) folder. Copy this file in the `sampling.300K` folder and run:
  ```bash
    python plot_dos_convergence.py iter.*/outfile.phonon_dos
  ```
