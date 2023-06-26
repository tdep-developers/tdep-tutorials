# Tutorial for the Thermal Conductivity
 
In this tutorial, you will learn how to compute lattice thermal conductivity in solids. 

#Before running the tutorial:
* TDEP installed
* [H5PY](https://docs.h5py.org/en/stable/) for Python installed

# Basic steps

## Preparation
Read the documentation for the [thermal conductivity](https://ollehellman.github.io/program/thermal_conductivity.html)
 
Go now into your work directory and copy the tar directory provided and extract it.

```
tar -xvf Thermal_conductivity.tar
cd Therml_conductivity
```

#### Note: The tutorial files can be downloaded from the school webpage [tdep_school](https://)

 
Inspect the content of the folder: 

You can see some examples. 

Go in Examples/Al

It contains the minimum input files needed for the thermal conductivity
* infile.ucposcar
* infile.forceconstant
* infile.forceconstant_thirdorder

## Compute the thermal conductivity

If you run it using:

```
mpirun thermal_conductivity
```

you will be able to get *output _thermal_conductivity* which contains the components of the thermal conductivity tensor  &kappa;_&alpha;_&beta;  for each temperature.

```
Row 	Description
1 	T1 κxx κyy κzz κxz κyz κxy κzx κzy κyx
2 	T2 κxx κyy κzz κxz κyz κxy κzx κzy κyx

```
As explained in the documentation, 


plot the results with 
```
gnuplot outfile.thermal conducitivity.gnuplot -persist
```
and study the plot. 

## Understand the results

* Does the trend look reasonable?
* Are the values comparable with the literature?

Get familiar with the optional flags available for thermal conductivity.
You may decide to compute the thermal conductivity for a given temperature. 
```
mpirun thermal_conductivity --temperature 300
```
or for a given range 
```
mpirun thermal_conductivity --temperature_range 100 500 50
```
Where you can specify the minimum, the maximum and the number of points. 


## Study the convergence 

### q-points

*Perform the same calculation using different grids of q-points
*Plot the thermal conductivity as a function of 1/q

What is a good grid for the thermal conductivity of Al? 

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

By default, TDEP uses the isotope natural distribution.(tabulated in the code, taken from the symbol in infile.ucposcar). In case you want to specify some other distribution, you can write in the same directory the [inpute.isotopes file](https://ollehellman.github.io/page/files.html#infile.isotopes) following the example linked here. 

Now repeat the calculation in a different folder with for the case of pure MgO by using:

```
mpirun thermal_conductivity -qg 10 10 10 --temperature 300 --noisotope

```

Compare the outputs. 

The isotope scattering is known to decrease the thermal conductivity of MgO by 30%-40%. Did you observe that?



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
Fit the k_xx against 1/qx and extrapolate the value for qx=0. 


# Post-processing options
So far we see how to extract the thermal conductivity tensor using TDEP routine.  Let's have a look at the other output files in may find in the working directory. 

*outfile.cumulative_kappa.hdf5*

It contains the information on the cumulative thermal conductivity plots described in the manual:
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


fn = h5py.File('outfile.cumulative_kappa.hdf5', 'r')
#plot the spectral thermal conductivity as a function of frequency
plt.plot(fn['frequencies'][:], fn['temperature_1']['spectral_kappa_vs_frequency_total'][:])
#add labels, titles etc.
plt.title('Spectral thermal conductivity of MgO')
plt.xlabel('Frequency [THz]')
plt.ylabel(r'$it{\kappa}$ [W/K/m/THz])
plt.savefig('Spectral_thermal_conductivity_MgO.png')

#plot the cumulative thermal conductivity as a function of the total mean free path
plt.plot(fn['temperature_1']['mean_free_path_axis'][:], fn['temperature_1']['cumulative_kappa_vs_mean_free_path_total'][:])
#add labels, titles etc.
plt.title('Cumulative kappa vs mean free path of MgO')
plt.xlabel('Mean Free Path [ps]')
plt.ylabel(r'$it{\kappa}$ [W/K/m])
plt.savefig('thermal_conductivity_vs_mfp_MgO.png')
```


# Next steps

# Use your material of interest

You may now use your own structure to calculate the thermal conductivity. 
Copy your primitive structure and the forceconstants in your work folder.
Repeat the previous steps



