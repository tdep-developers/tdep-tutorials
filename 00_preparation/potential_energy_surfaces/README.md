So3krates Neural Network Potential
===

This folder contains a neural network potentials for several material. They were trained on reference data created with the harmonic stochastic sampling scheme implemented in TDEP for a variety of conditions.

## Install

**The so3krates potential requires python >=3.8.** Older versions are not supported by jax.

**Please follow the [detailed instruction](#detailed-instructions) below if you want a working environment that is _not_ optimized for speed.**

The requirements should be straightforward to install. **We generally recommend  to create a virtual (conda) environment for testing.** Please note that the potential is implemented in [JAX](https://github.com/google/jax) and there are different ways to use hardware acceleration on your platform of interest. [**Please consider the JAX docs.**](https://github.com/google/jax#installation)

Please install the following repositories in this order:

- https://github.com/sirmarcel/glp
- https://github.com/thorben-frank/mlff
- https://github.com/flokno/tools.mlff

### Detailed instructions

- Make sure you are using python 3.8-3.11. If you are on older versions, you can use `conda` to create e.g. a python3.10 environment via
  ```bash
  conda create -n py310 python=3.10
  conda activate py310
  ```

- Go to the tutorials folder (the folder in which you find this README) and `cd` into the `test` directory:

  ```bash
  cd .../tdep-tutorials/00_preparation/potential_energy_surfaces/pes_gan/test
  ```

- create a virtual environment and activate it:
  ```bash
  python -m venv venv
  # for bash:
  source venv/bin/activate
  # in in other shells:
  # source venv/bin/activate.fish
  # source venv/bin/activate.csh
  ```

- install `glp`, `mlff`, `tdeptools`, and `mlfftools`:
  ```bash
  pip install https://github.com/sirmarcel/glp/archive/main.zip
  pip install https://github.com/flokno/mlff/archive/v0.2.1.zip
  pip install https://github.com/flokno/tools.tdep/archive/v0.0.5.zip
  pip install https://github.com/flokno/tools.mlff/archive/v0.0.2.zip
  pip install 'numpy<2.0' jax==0.4.13 jaxlib==0.4.13 optax==0.2.0 orbax_checkpoint==0.5.3 --no-dependencies
  ```

## Test

You can check your installation for GaN in the folder `pes_gan`, see instructions there.

## Use

You can predict energy, forces, and stress for a set of structures with the command `sokrates_compute`. For example, the command test in the `pes_gan/test` folder runs the command

```bash
sokrates_compute --folder-model ../module/ samples/*/*/*/geometry.in (--format aims)
```

which will compute energy, forces, and stress for all samples saved as `geometry.in` files (these could be `POSCAR`, `positions.xyz`', ..., as well. When you are using a default name that [`ase.io.read`](https://wiki.fysik.dtu.dk/ase/ase/io/io.html#ase.io.read), then you do not need to specify the `--format`), and save them to a dataset `predictions.nc` which is a HDF5 file that can be read easily using , e.g., [`xarray`](https://docs.xarray.dev/en/stable/user-guide/io.html).

`sokrates_compute` can also write TDEP input directly by using the `--tdep` flag.

## References

Background:

- So3krates architecture: https://openreview.net/forum?id=tlUnxtAmcJq
- forces and stress implementation + benchmark: https://arxiv.org/abs/2305.01401
