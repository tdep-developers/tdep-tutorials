sTDEP for zirconium
===

This example shows how to perform statistical sampling for bcc zirconium, and how to obtain a positive definite spectrum at high temperatures, in this case, 1300K.

This example is interesting as this system is dynamically unstable in the harmonic approximation.
You can observe this from the phonon dispersion located in the [harmonic folder](./harmonic) which contains a lot of imaginary modes (represented as negatives).
However, the bcc phase of zirconium is stable at high temperature.

And remember: to extract properties, such as the free energy, the lineshape or the thermal conductivity, **you need to have stable phonons, otherwise results would not be physical !**

So our goal here is to obtain the phonon dispersion of the temperature-stabilized bcc phase of zirconium at 1300K.

This tutorial assumes that you are already familiar with the [sTDEP sampling scheme from the MgO example](../01_MgO/README.md).

However, with its unstability, it is more complicated to converge the self-consistent cycle for zirconium than for MgO.
To improve the convergence, we will precondition the cycle by mixing configurations from the current iteration and the previous one.

# Run the self-consistent cycle

But before looking at the mixing scheme, let's observe what happens without the preconditioning.

Go into the `sampling.1300K` folder and perform a self-consistent cycle (following the same steps as for MgO).

Copy the `infile.ucposcar` into the folder and generate a supercell with 128 atoms:
```bash
generate_structure -na 128
mv outfile.ssposcar infile.ssposcar
```

The initialize the self-consistent scheme.
Create a folder `iter.000`, copy the input files and generate some starting configuration at 1300K
```bash
mkdir -p iter.000
cd iter.000
canonical_configuration --quantum --temperature 1300 -n 4 -of 4 --maximum_frequency 6.0
cd ../
```

*Note*: Why is the maximum frequency parameter different than from MgO ?

Now we can do the self-consistent cycle

1. Go back in `sampling.1300K` and create a folder `iter.n`, with n the current step
2. Copy the input files in the new folder `iter.n`
3. Compute the forces on the configurations generated at the last step with `sokrates_compute --folder-model ../../module ../iter.n-1/aims_conf* --format=aims --tdep`. This will create the infiles with displacements and forces for TDEP (iter.n-1 is the previous iteration. So if you are in iteration 002, it should read iter.001).
4. Extract the force constants using `extract_forceconstant -rc2 10`
5. Copy the outfile force constants as an infile using `ln -sf outfile.forceconstant infile.forceconstant`
6. Compute the phonons (and/or the property you want to converge) using `phonon_dispersion_relations --dos` 
7. Check for convergence by comparing with previous iterations and exit if you are converged
8. Else, create new configurations with `canonical_configuration --temperature 1300 -n X --quantum -of 4`. The number of configuration X will depend on the iteration. We found that doubling the number of configurations at each steps works well to converge will minimizing the number of configurations to generate. This means that you should have 8 configurations at the first step, 16 at the second, 32 at the third, and so on.
9. Go to the next iteration by going back to step 1


Repeat the cycle until getting to the fifth iteration and observe the convergence of the phonons frequencies.

How do the convergence compare to the MgO case ?


# The self-consistent scheme with mixing

The preconditioning of the self-consistent cycle consists simply by re-using configurations from the previous iteration when extracting the IFC.

In our case, this consists simply in replacing the thid step (when computing the forces by)

```bash
sokrates_compute --folder-model ../../module --/iter.n-1/aims_conf* ../iter.n-2/aims_conf* --format=aims --tdep
```
where `n-1` and `n-2` are respectively the previous iteration and the one even before.
For example, if you are at iteration `iter.004`, replace `iter.n-1` by `003` and `iter.n-2` by `iter.002`.

Now go into the `sampling_with_mixing` folder and do the self-consistent cycle with mixing for 5 iterations.

Compare the convergence of the frequencies with and without mixing.


## Initialization


# Note

## Helping the start

With a lot of unstable modes, the self-consistent process can be more difficult to start for zirconium.
But you can improve the starting point by using more configuration in the initialization step.
For example you can try to generate more configurations by using
```bash
canonical_configuration --temperature 1300 --quantum -n 8 --maximum_frequency X --output_format 4
```
in the initialization (where `X` is the value of the maximum frequency that you have to guess...)

Remember to adapt the number of configurations for the following steps after that !

## Script

Repeating the different steps of self-consistent process is long and repetitive.
It is a good idea to make a script to automatize the process and avoid mistakes !

You can find the bash script `run_sTDEP.sh` in the [scripts folder](../scripts) that performs automatically all the steps needed for this tutorial.
*You should still try to perform them yourself to have a better understanding of what is happening !*
You can run this script by copying it in the folder where you want to do the sampling and running
```bash
./run_sTDEP.sh --temperature T --niter N
```
where `T` is the temperature in K and `N` the number of iterations.
You can also use the flags
- `--polar` to activate the polar flag with TDEP
- `--mixing` to perform the mixing introduced in this example
- `--nconfs N` to start the initialization with `N` configurations
- `--maximum_frequency F` to initiliaze with a maximum frequency of `F` THz
- `--cutoff R` to use a cutoff of `R` angstrom
