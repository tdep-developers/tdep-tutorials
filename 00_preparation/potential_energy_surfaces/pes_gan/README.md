So3krates Neural Network Potential for GaN
===

This folder contains a neural network potential for GaN. It was trained on reference data created with the harmonic stochastic sampling scheme implemented in TDEP for a variety of conditions.

## Install

See [installation instructions in the root folder.](../README.md#Install)

## Test

Run the test:
```bash
make test
```

this will take a few minutes.

You fill find a report of the errors against the reference values in `predictions_reference.nc` and a plot `plot_test.png` that you can compare against the reference `plot_test_reference.png`

## Use

You can predict energy, forces, and stress for a set of structures with the command `sokrates_compute`. For example, the command test in the `test` folder runs the command

```bash
sokrates_compute --folder-model ../module/ samples/*/*/*/geometry.in
```

which will compute energy, forces, and stress for all samples saved as `geometry.in` files (these could be `POSCAR`, `positions.xyz`', ..., as well), and save them to a dataset `predictions.nc` which is a HDF5 file that can be read easily using , e.g., [`xarray`](https://docs.xarray.dev/en/stable/user-guide/io.html).

`sokrates_compute` can also write TDEP input directly by using the `--tdep` flag.
