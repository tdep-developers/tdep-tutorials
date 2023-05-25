So3krates Neural Network Potential for GaN
===

This folder contains a neural network potential for GaN. It was trained on reference data created with the harmonic stochastic sampling scheme implemented in TDEP for a variety of conditions.

## Install

**The so3krates potential requires python3.8+.**

**Please follow the [detailed instruction](#detailed-instructions) below if you want a working environment that is _not_ optimized for speed.**

The requirements should be straightforward to install. **We generally recommend  to create a virtual (conda) environment for testing.** Please note that the potential is implemented in [JAX](https://github.com/google/jax) and there are different ways to use hardware acceleration on your platform of interest. [**Please consider the JAX docs.**](https://github.com/google/jax#installation)

Please install the following repositories in this order:

- https://github.com/sirmarcel/glp
- https://github.com/thorben-frank/mlff
- https://github.com/flokno/tools.mlff

### Detailed instructions

- Go to the tutorials folder (the folder in which you find this README) and `cd` into the `test` directory:

  ```bash
  cd .../tdep-tutorials/00_preparation/gan_potential/test
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
  pip install https://github.com/thorben-frank/mlff/archive/main.zip
  pip install https://github.com/flokno/tools.tdep/archive/main.zip
  pip install https://github.com/flokno/tools.mlff/archive/main.zip
  ```
  
- Run the test:
  ```bash
  make test
  ```

  this will take a few minutes.

  - you fill find a report of the errors against the reference values in `predictions_reference.nc` and a plot `plot_test.png` that you can compare against the reference `plot_test_reference.png`



## References

Background:

- So3krates architecture: https://openreview.net/forum?id=tlUnxtAmcJq
- forces and stress implementation + benchmark: https://arxiv.org/abs/2305.01401