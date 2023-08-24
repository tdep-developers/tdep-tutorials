# Tutorial for the Thermal Conductivity
 
In this tutorial, you will learn how to compute lattice thermal conductivity in solids using the TDEP method. 
Useful references on the topic:

[R.E. Peierls, Quantum Theory of Solids (1955)](https://books.google.es/books?id=WvPcBUsSJBAC&redir_esc=y)


[M. Omini and A. Sparavigna Phys. Rev. B 53, 9064 (1996)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.53.9064)


[D. A. Broido et al., Appl. Phys. Lett. 91, 231922 (2007)](https://pubs.aip.org/aip/apl/article-abstract/91/23/231922/334217/Intrinsic-lattice-thermal-conductivity-of?redirectedFrom=fulltext)

# General scope
In this tutorial we will learn how to calculate the lattice thermal conductivity from the iterative solution of the phonon Boltzmann equation.

The tutorial covers:
* the basic features included in the thermal conductivity routine of TDEP
* thermal conductivity as a function of temperature
* thermal conductivity for a given isotope distribution
* thermal conductivity vs q-point grid
* plot and analysis of the results

The tutorial **does not cover**:
* Relax the structure
* Supercell convergence
* Extract force constants

  
There are two test cases: Al and MgO. 
The data provided includes the IFCs and the unitcell obtained from previous DFT calculations. This data is not meant to produce converged results. 

# Before running the tutorial:
* TDEP installed
* [H5PY](https://docs.h5py.org/en/stable/) for Python installed
* Access to a plotting tool (for example  [matplotlib](https://matplotlib.org/), if you are using Python)
* Have a converged set of 2nd and 3rd order IFCs (you can use some previous examples or the data provided in this tutorial)

## Input files:
  `infile.ucposcar` 
  
  `infile.forceconstant` 
  
  `infile.forceconstant_thirdorder` 
  
  
## Optional input file:
  `infile.isotopes` (for non-natural isotope distribution)
  
You can create your customized isotope distribution specifying the number of isotopes per atom, followed by the appropriate number of concentrations and masses (in atomic mass units). An example is reported below:

```
1         # number of isotopes for first atom in infile.ucposcar
1 28.0855 # concentration, mass, one line per isotope
2         # number of isotopes for second atom
0.5 12.0  # concentration, mass
0.5 13.0  # concentration, mass
...
```

# Basic steps

## Preparation

Read the documentation for the [thermal conductivity](https://tdep-developers.github.io/tdep/program/thermal_conductivity/)

Go now into your work directory and copy the files provided.


#### Note: The tutorial files can be downloaded from the school webpage [tdep_school](https://github.com/tdep-developers/tdep-tutorials/tree/main)

 
Inspect the content of the folder: 

You can see some examples. 

Go in Examples/Al

It contains the minimum input files needed for the thermal conductivity
* [infile.ucposcar](https://tdep-developers.github.io/tdep/files/#infile.ucposcar)
* [infile.forceconstant](https://tdep-developers.github.io/tdep/program/extract_forceconstants/#outfileforceconstant)
* [infile.forceconstant_thirdorder](https://tdep-developers.github.io/tdep/program/extract_forceconstants/#outfileforceconstant_thirdorder)

## Compute the thermal conductivity

If you run it using:

```
mpirun thermal_conductivity > kappa.log
```

you will be able to get *output _thermal_conductivity* which contains the components of the thermal conductivity tensor  $\kappa_{\alpha \beta}$  for each temperature.

```
Row 	Description
1 	T1 κxx κyy κzz κxz κyz κxy κzx κzy κyx
2 	T2 κxx κyy κzz κxz κyz κxy κzx κzy κyx

```

As explained in the documentation, without specifying any optional flag, you will obtain the thermal conductivity for a natural isotope distribution, with a q-mesh of 26 26 26 (default value), for 5 different temperatures between 100K and 300K.

You can check the status of the calculation by looking at the file kappa.log printed
```
... using 4 MPI ranks
 ... read unitcell poscar
 ... read second order forceconstant
 ... read third order forceconstant
 ... getting the full dispersion relations
  
Counting scattering events and calculating integration weights
 ... adaptive gaussian smearing, scalingfactor=   1.0000000000000000     
  ... counting scattering events         100.0% |========================================| 
 ... found  2.29% of threephonon events to be relevant,  0.37057E+08 +  0.34372E+08 events
 ... found 12.48% of isotope events to be relevant,   0.65007E+08 events
 ... calculating scatteringrates, remaining time: 00:05:45, estimated total time: 00:06:16  (8.1%)
 ... calculating scatteringrates, remaining time: 00:02:23, estimated total time: 00:04:24  (46.0%)
 ... calculating scatteringrates, remaining time: 00:00:38, estimated total time: 00:04:09  (85.1%)
 Counted and got scattering amplitudes in 240.77429
 
 THERMAL CONDUCTIVITY
 
 Temperature: 100.00000
 iter         kxx            kyy            kzz            kxy            kxz            kyz       DeltaF/F
    0        54.0887        54.0887        54.0887         0.0000         0.0000         0.0000
    1        61.6716        61.6716        61.6716         0.0000         0.0000         0.0000   0.463E+01
    2        67.2627        67.2627        67.2627         0.0000         0.0000         0.0000   0.613E-01
    3        69.3412        69.3412        69.3412         0.0000         0.0000         0.0000   0.240E-01
    4        70.6782        70.6782        70.6782         0.0000         0.0000         0.0000   0.277E-02
    5        71.2635        71.2635        71.2635         0.0000         0.0000         0.0000   0.187E-02
    6        71.6217        71.6217        71.6217         0.0000         0.0000         0.0000   0.775E-03
    7        71.7914        71.7914        71.7914         0.0000         0.0000         0.0000   0.102E-03
    8        71.8916        71.8916        71.8916         0.0000         0.0000         0.0000   0.528E-04
    9        71.9413        71.9413        71.9413         0.0000         0.0000         0.0000   0.152E-04
   10        71.9699        71.9699        71.9699         0.0000         0.0000         0.0000   0.308E-05
   11        71.9845        71.9845        71.9845         0.0000         0.0000         0.0000   0.105E-05
             71.9928        71.9928        71.9928         0.0000         0.0000         0.0000

 
 Temperature: 200.00000
 iter         kxx            kyy            kzz            kxy            kxz            kyz       DeltaF/F
    0        26.9798        26.9798        26.9798         0.0000         0.0000         0.0000
    1        30.9707        30.9707        30.9707         0.0000         0.0000         0.0000   0.144E+01
    2        33.5624        33.5624        33.5624         0.0000         0.0000         0.0000   0.464E-01
    3        34.5355        34.5355        34.5355         0.0000         0.0000         0.0000   0.296E-01
    4        35.1090        35.1090        35.1090         0.0000         0.0000         0.0000   0.231E-02
    5        35.3569        35.3569        35.3569         0.0000         0.0000         0.0000   0.110E-02
    6        35.5003        35.5003        35.5003         0.0000         0.0000         0.0000   0.214E-03
    7        35.5665        35.5665        35.5665         0.0000         0.0000         0.0000   0.650E-04
    8        35.6041        35.6041        35.6041         0.0000         0.0000         0.0000   0.125E-04
    9        35.6221        35.6221        35.6221         0.0000         0.0000         0.0000   0.462E-05
   10        35.6322        35.6322        35.6322         0.0000         0.0000         0.0000   0.996E-06
             35.6372        35.6372        35.6372         0.0000         0.0000         0.0000
 
 Temperature: 300.00000
 iter         kxx            kyy            kzz            kxy            kxz            kyz       DeltaF/F
    0        18.2872        18.2872        18.2872         0.0000         0.0000         0.0000
    1        21.0233        21.0233        21.0233         0.0000         0.0000         0.0000   0.113E+01
    2        22.7525        22.7525        22.7525         0.0000         0.0000         0.0000   0.485E-01
    3        23.4036        23.4036        23.4036         0.0000         0.0000         0.0000   0.269E-01
    4        23.7802        23.7802        23.7802         0.0000         0.0000         0.0000   0.230E-02
    5        23.9428        23.9428        23.9428         0.0000         0.0000         0.0000   0.109E-02
    6        24.0357        24.0357        24.0357         0.0000         0.0000         0.0000   0.167E-03
    7        24.0785        24.0785        24.0785         0.0000         0.0000         0.0000   0.710E-04
    8        24.1026        24.1026        24.1026         0.0000         0.0000         0.0000   0.134E-04
    9        24.1141        24.1141        24.1141         0.0000         0.0000         0.0000   0.517E-05
   10        24.1205        24.1205        24.1205         0.0000         0.0000         0.0000   0.108E-05
             24.1236        24.1236        24.1236         0.0000         0.0000         0.0000
  
 Timings:
            initialization:       1.449 s,   0.289%
       integration weights:     106.087 s,  21.175%
           matrix elements:     240.774 s,  48.058%
            QS calculation:      58.925 s,  11.761%
                     kappa:       0.000 s,   0.000%
          self consistency:      79.013 s,  15.771%
          cumulative plots:      14.494 s,   2.893%
                     total:     501.006 seconds


```
The first step (iter 0) represents the RTA solution. The last step is the converged iterative solution. For reference, take a look at the documentation about the [thermal conductivity](https://tdep-developers.github.io/tdep/program/thermal_conductivity/).

plot the results with 
```
gnuplot outfile.thermal_conductivity.gnuplot -persist
```
and study the plot. 

![here you can see how the plot should look like](https://github.com/RobertaFarris93/tdep-tutorials/blob/thermal_conductivity/04_thermal_conductivity/Plots/Al_kappa.png)

## Understand the results

* Does the trend look reasonable?
* Are the values comparable with the literature ([thermal conductivity of pure aluminum is estimated to be in the range between 220 and 250 (W/mK)](https://thermtest.com/thermal-resources/materials-database))? Why?

Get familiar with the optional flags available for thermal conductivity.
You may decide to compute the thermal conductivity for a given temperature. 

```
mpirun thermal_conductivity --temperature 300
```
or for a given range 
```
mpirun thermal_conductivity --temperature_range 100 500 50
```
where you can specify the minimum, the maximum and the number of points. 


## Study the convergence 

### q-points

* Perform the same calculation using different grids of q-points
* Plot the thermal conductivity as a function of 1/q

What is a good grid for the thermal conductivity of Al? 

The calculation of thermal conductivity, being a integrated quantity, requires its evaluation under the assumption of an infinitely refined q-point grid. Unfortunately, this is impossible from a computational point of view, but using progressively finer grids, the behavior of thermal conductivity should scale linearly with q. Thus, in order to converge the thermal conductivity value, we could perform the calculation for a set of q-grids and then evaluating then studing the convergence by plotting the thermal conductivity against 1/q and extrapolating the value for 1/q at 0.  The point of intersection on the y-axis resulting from this regression corresponds to the thermal conductivity within the hypothetical context of an infinitely dense q-point grid. 
For more details, see [Esfarjani, K. et. al., Phys. Rev. B 84, 085204 (2011)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.84.085204).


![Here the convergence test for thermal conductivity of aluminum](https://github.com/RobertaFarris93/tdep-tutorials/blob/thermal_conductivity/04_thermal_conductivity/Plots/Al_convergence.png)

### Thermal conductivity of MgO

Now you should be familiar with the thermal_conductivity routine. 
So far you learnt how to run the calculations for different grids of q-points and different ranges of temperatures. 
Let's now see what are the available output information you can extract from TDEP.

We analyze the thermal conductivity for a well-known semiconductor. 
Go to Examples/MgO. 

Create a folder and copy all the input files there. 
Perform the calculation using:

```
mpirun thermal_conductivity -qg 10 10 10 --temperature 300

```

By default, TDEP uses the isotope natural distribution.(tabulated in the code, taken from the symbol in infile.ucposcar). In case you want to specify some other distribution, you can write in the same directory the [inpute.isotopes file](https://tdep-developers.github.io/tdep/files/#infileisotopes) following the example linked here. 
```
1         # number of isotopes for first atom in infile.ucposcar
1 28.0855 # concentration, mass, one line per isotope
2         # number of isotopes for second atom
0.5 12.0  # concentration, mass
0.5 13.0  # concentration, mass
...
```

Now repeat the calculation in a different folder with for the case of pure MgO by using:

```
mpirun thermal_conductivity -qg 10 10 10 --temperature 300 --noisotope

```

Compare the outputs. 
The isotope scattering is known to decrease the thermal conductivity of MgO by 30%-40% at 300K. Did you observe that? For reference, see [Florian Knoop et.al, PRB 107, 224304 (2023)](https://journals.aps.org/prb/pdf/10.1103/PhysRevB.107.224304). 


![MgO: comparison betweeen natural isotope distribution and pure cases](https://github.com/RobertaFarris93/tdep-tutorials/blob/thermal_conductivity/04_thermal_conductivity/Plots/MgO_isotope.png)


#### Extrapolation for an infinite grid of q-points

Compute the thermal conductivity using different grids. For doing that, you can use a very simple script like the example reported here:


```
#!/bin/sh
for i in {4..28..4};
do
        mkdir q_$i
        cp infile* q_$i
        cd q_$i
        mpirun thermal_conductivity -qg $i $i $i --temperature 300
        cd ..
done

```
![Fit the k_xx against 1/qx and extrapolate the value for qx=0](https://github.com/RobertaFarris93/tdep-tutorials/blob/thermal_conductivity/04_thermal_conductivity/Plots/MgO_convergence.png). 

In order to reach convergence, you will need access to a cluster/HPC. 


# Post-processing options
So far we see how to extract the thermal conductivity tensor using TDEP routine.  Let's have a look at the other output files in may find in the working directory. In case your calculations are not finished yet, you can use the output file provided in the MgO directory, using a q-grid of 28x28x28 points and using a temperature of 300K. 

*outfile.cumulative_kappa.hdf5*

The file contains the information on the cumulative thermal conductivity plots described in the manual, per each computed temperature. You can inspect the information contained in the file using the following minimal Python script:
```
import numpy
import matplotlib.pyplot as plt
import h5py
fn = h5py.File('outfile.cumulative_kappa.hdf5', 'r')
print(fn['temperature_1'].keys())
```

```
<KeysViewHDF5 ['angular_momentum_tensor', 'boundary_scattering_kappa', 'boundary_scattering_lengths', 'cumulative_kappa_vs_mean_free_path_per_atom', 'cumulative_kappa_vs_mean_free_path_per_mode', 'cumulative_kappa_vs_mean_free_path_per_species', 'cumulative_kappa_vs_mean_free_path_total', 'frequency_axis', 'mean_free_path_axis', 'spectral_angmom_vs_frequency_per_direction', 'spectral_kappa_vs_frequency_per_atom', 'spectral_kappa_vs_frequency_per_direction', 'spectral_kappa_vs_frequency_per_mode', 'spectral_kappa_vs_frequency_per_species', 'spectral_kappa_vs_frequency_total']>
```

##### 1. Cumulative thermal conductivity vs mean free path
The cumulative thermal conductivity can then be computed as a sum of the fraction of heat that is carried by phonons with mean free paths smaller than l, where l is:
```math
l_{\lambda} = \left| v_{\lambda} \right| \tau_{\lambda} \,,
```

```math
\kappa_{\alpha\beta}^{\textrm{acc}}(l)= \frac{1}{V} \sum_{\lambda} C_{\lambda} v^{\alpha}_{\lambda} v^{\beta}_{\lambda} \tau_{\lambda} \Theta(l- l_{\lambda} ) \,,
```
##### 2.  The spectral thermal conductivity 

which is a measure which frequencies contribute most to thermal transport.
```math
\kappa_{\alpha\beta}(\omega)=\frac{1}{V} \sum_{\lambda}C_{\lambda} v^{\alpha}_{\lambda} v^{\beta}_{\lambda} \tau_{\lambda} \delta(\omega- \omega_{\lambda})
```
#### Read and analyze the output
Let's analyze the output file with the following script

```
import numpy
import matplotlib.pyplot as plt
import h5py

#customized parameters
params = {'legend.fontsize': 20,
          'figure.figsize': (15, 5),
         'axes.labelsize': 30,
         'axes.titlesize':30,
         'xtick.labelsize':20,
         'ytick.labelsize':20}
plt.rcParams.update(params)


fn = h5py.File('outfile.cumulative_kappa.hdf5', 'r')
#plot the spectral thermal conductivity as a function of frequency
plt.plot(fn['frequencies'][:], fn['temperature_1']['spectral_kappa_vs_frequency_total'][:], lw = 4)
#add labels, titles etc.
plt.title('Spectral thermal conductivity of MgO')
plt.xlabel('Frequency [THz]')
plt.ylabel(r'$\kappa$ [W/K/m/THz]')
plt.savefig('Spectral_thermal_conductivity_MgO.png')
plt.show()
#plot the cumulative thermal conductivity as a function of the total mean free path
plt.semilogx(fn['temperature_1']['mean_free_path_axis'][:], 
             fn['temperature_1']['cumulative_kappa_vs_mean_free_path_total'][:], lw = 4)
#add labels, titles etc.
plt.title('Cumulative kappa vs mean free path of MgO')
plt.xlabel('Mean Free Path [m]')
plt.ylabel(r'$\kappa$ [W/K/m]')
plt.xlim(1E-9,1E-5)
plt.savefig('thermal_conductivity_vs_mfp_MgO.png')
```
The script should give you the plots reported below. 
![Spectral thermal conductivity of MgO](https://github.com/RobertaFarris93/tdep-tutorials/blob/thermal_conductivity/04_thermal_conductivity/Plots/Spectral_thermal_conductivity_MgO.png)


![Cumulative kappa vs mean free path of MgO](https://github.com/RobertaFarris93/tdep-tutorials/blob/thermal_conductivity/04_thermal_conductivity/Plots/thermal_conductivity_vs_mfp_MgO.png)


# Convergence of thermal conductivity 

So far we consider converged the forces used for the thermal conductivity. As for the other physical quantities, the thermal conductivity needs to be tested against all the parameters used in the calculations. In particular:

* supercell size
* number of configurations used
* range of the forces cutoffs (number of neighbours used included in the integral)
* number of iterations in the self-consistent loop 

## Supercell size convergence

you can test the size of the supercells used by following the steps explained in Tutorial 01 for the case of MgO.


## Self-consistent loop

In order to converge the thermal conductivity, we should test it against the sampling in a iterative way. For doing that, we should repeat the steps explained in the Tutorial 01 and test the goodness of our fit for the desired property, in this case the thermal conductivity (sTDEP scheme). 

To do so, with the data provided in the folder ``convergence_tests/input_MgO/``` we can:


* Create a set of canonical configurations using:
  ```
  canonical_configuration --quantum  --temperature 300 -n 2
   ```
  Here, we are using an initial set of IFCs in order to create a set of configurations, in case you want to start from scratch without an initial set of forceconstants, you can use two flags ```--debye_temperature ``` and  ``` --maximum_frequency```. For the details, read the documentation on the [canonical_configuration](https://tdep-developers.github.io/tdep/program/canonical_configuration/) .
  
  You should see now three configurations in your folder: `
  
  ```contcar_conf0001```
  
  ```contcar_conf0002```

* Compute the atomic forces using a DFT code of your choice.
* 
  **Tip**: in order to avoid this step, that could require a significant amount of time, we provided a potential for MgO. You can download that from the first Tutorial. Create a folder "iter0" and copy your input files and the potential there.


    * perform a self-consistent loop as described in [Tutorial 1](https://github.com/tdep-developers/tdep-tutorials/tree/main/01_sampling) for MgO for 10 iterations
    * compute thermal conductivity at each step:
          ```
          mpirun thermal_conductivity -qg 8 8 8 --temperature 300
          ```
    * study the convergence
      
![Here an example of the thermal conductivity convergence.](https://github.com/RobertaFarris93/tdep-tutorials/blob/thermal_conductivity/04_thermal_conductivity/Plots/MgO_SC.png)
 
**How many steps did you need to reach convergence?**

## Cutoffs of IFcs

In the data provided, you will find a directory named ```convergence_tests/input_MgO```.

Inspect the folder. It contains the tdep input files needed for fitting the forceconstant and calculated the related properties. 

In Tutorial 01, you learnt how to increase your force constants cutoff (rc2) and observe how the phonon dispersion changes. 

Repeat the same steps, but this time keep fixed rc2 and change rc3. 

```
mpirun extract_forceconstants  -rc2 8 -rc3 4
```

**How the thermal conductivity changes with the 3rd order IFCs cutoff?**

# Next steps
 

# Use your material of interest

You may now use your own structure to calculate the thermal conductivity. 

Copy your primitive structure and the forceconstants in your work folder and repeat the previous steps.

Alternatively, you will find the needed input files for Si, that will be used as example in the next tutorial. 



