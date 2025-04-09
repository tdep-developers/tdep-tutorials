TDEP with molecular dynamics for argon
===

In this tutorial, we will compute the temperature dependent phonon dispersion of argon.

You will find the unitcell and supercell for fcc Ar in the `infile.ucposcar` and `infile.ssposcar` files, located in the `Ar_lj` folder. 

For the molecular dynamics simulations, we will use a Lennard-Jones potential (so that the simulations are fast) and a Langevin thermostat to sample the canonical ensemble.
Everything will be run using [ASE](https://wiki.fysik.dtu.dk/ase/ase/md.html).

In the folder, you will find a script `run_md.py` that will handle the molecular dynamics simulations.
This script is run using
```bash
python run_md.py supercell T
```
where supercell is the file of the supercell and T is the temperature of the simulation.
Note that the script is using the ASE `io` module, and you might have to add the `--format` flag to indicate the format of your supercell.
For example, runing the script using the `infile.supercell` at 50K looks like `python run_md.py infile.ssposcar 50 --format vasp`. 

You will also find a script `parser.py` that will handle the conversion from the trajectory to the infiles needed by TDEP.
This script can be used with:
```bash
python parser.md trajectory.traj --nthrow X
```
where X is the number of steps to remove from the beginning of the tractory.

**Have a look at these scripts before running them !**

As the force constants extracted with TDEP are a **thermodynamic average** some considerations have to be taken into account:
1. Since molecular dynamics is an iterative algorithm (each step depend on the one before), the configurations are correlated with each other. To remove any bias in the simulation, one should use uncorrelated configurations
2. To have a good sampling of the canonical ensemble, the MD simulation should be long enough to ensure the important part of the phase space have been explored.
3. The configurations used have to be representative of the canonical ensemble. In general, MD simulations starts from ideal positions of the structure, and the first steps are not representative of the actual phase space of the canonical ensemble and should be removed before extracting the force constants.

# Running the molecular dynamics

Go into the `Ar_lj` folder.

We will run the MD simulation for 10 ps using the `run_md.py` script and starting from the supercell given by `infile.ssposcar`
```bash
python run_md.py infile.ssposcar 50 --format vasp --nsteps 10000
```
This should take one or two minutes, and you should now have a file called `trajectory.traj` in the folder.

Once this is done, let's have a look at the simulation.
Using the script `plot_equilibration.py` you can observe the evolution of the potential energy and the temperature during the simulation.
Looking at this plot will give us insight on how many configurations from the start (the equilibriation) should be removed in order to not bias our result.
You can run the script using
```bash
python plot_equilibration.py trajectory.traj
```
You should observe that the potential energy increases for the first steps, before oscillating around a constant value.
For this example, it should be safe to remove the first 1000 configurations.

We can now parse the trajectory to create the infiles needed by tdep using the `parser.py` script:
```bash
python ../parser.py trajectory.traj --nthrow 1000
```
You should now find all the infiles needed by TDEP to extract force constants
- infile.ucposcar
- infile.ssposcar
- infile.meta
- infile.forces
- infile.positions
- infile.stat

And we can now proceed to extract the force constants.
However, we have to keep in mind that configurations in the infiles are correlated with each other since we extracted them from molecular dynamics simulations.
We can avoid this correlation by using the `--stride` flag
```bash
extract_forceconstant -rc2 10 --stride 50
```
This will extract second order force constants using a cutoff of 10 angstrom and only use one configurations every 50 steps from the infiles.
Keep in mind that this stride decrease the actual number of configuration used to extract the force constant.

Now, link the outfile force constants as an infile, and extract the phonon dispersion
```bash
ln -sf outfile.forceconstant infile.forceconstant
phonon_dispersion --dos
```

And that's it, we now have our phonon dispersion at 50K !


# Convergence

As always, we have to check for the convergence of our results.
With MD simulations, apart from the size of the system and the second order cutoff, the main parameter for the convergence is the number of configurations used to extract the force constants.

Extract the force constants with different stride values, compute the phonons (remember to copy the resulting phonons or they will be overwritten every time you run `phonon_dispersion`) and observe the convergence of the phonon dispersion with respect to the number of configurations.

# Notes

1. To reduce the number of steps to throw at the beginning of the simulation, one would have to start at an already thermalized configuration. TDEP can generate configuration in the (approximate) canonical ensemble using the `canonical_configuration` binary, as explained in the [sTDEP tutorial](../../sTDEP). This allows to reduce the time of the equilibration phase.
2. TDEP use only static averages - in the sense that there is no information used of the time dependence when computing averages. This means that TDEP can also be used with Monte-Carlo simulations.
3. It is really important that the configurations provide a thorough exploration of the canonical ensemble, in order for the averages to be converged. When using one MD simulation, this means that the simulation has to be "long enough". But it is also possible to concatenate several MD simulations (in the same ensemble) with different starting point (and different random number for the thermostat). Such an approach allows for a more efficient exploration of the canonical ensemble, but remember to remove the equilibration part for each simulations !
