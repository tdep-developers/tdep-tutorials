Dielectric tensor with Quantum Espresso
===

## Preparation

**We need the most recent version of [ASE](https://gitlab.com/ase/ase) in order to be able to parse dielectric tensors**. Please make sure you have that installed, e.g., by running

```bash
pip install git+https://gitlab.com/ase/ase.git@master
```

Likewise [`tdeptools`](https://github.com/flokno/tools.tdep) need to be installed:

```bash
pip install https://github.com/flokno/tools.tdep/archive/main.zip
```

## Background

We want to parse the dielectric tensor $\epsilon$ and Born effective charges $Z_i$ for each atom $i$ in the unit cell from Quantum Espresso (QE) output for a unit cell of GaN.

QE computes the dielectric properties in two steps: i) `pw.x` solves the Kohn-Sham equations for the electronic ground state, as well as the total energy $E$ and first derivatives such as forces ${\bf F}_i = - \partial E / \partial {\bf R}_i$. These results are saved in `pw.out`. ii) `ph.x` computes second derivatives via density functional perturbation theory (DFPT, see [suggested reading below](#suggested-reading)) from the electronic ground state, in particular the dielectric tensor 

$$\epsilon^{\alpha \beta} = \frac{\partial^2 E}{\partial \mathcal E^\alpha \partial \mathcal E^\beta}~, $$

where $ {\bf \mathcal E}$  denotes an external electric field.

The Born effective charge is the a mixed derivative,

$$Z_i^{\alpha \beta} = \frac{\partial^2 E}{\partial R_i^\alpha \partial \mathcal E^\beta} \equiv \frac{\partial F^\alpha_i}{\partial \mathcal E^\beta}~,$$

i.e., the change of the force on atom $i$ with external electric field.

These are calculated by `ph.x` and written to `ph.out` in the following way (for the GaN example):

```
...
          Dielectric constant in cartesian axis

          (       5.943555652       0.000000000       0.000000000 )
          (       0.000000000       5.943555652      -0.000000000 )
          (       0.000000000      -0.000000000       6.104407167 )

          Effective charges (d Force / dE) in cartesian axis without acoustic sum rule applied (asr)

           atom      1   Ga Mean Z*:        2.67494
      Ex  (        2.62847       -0.00000        0.00000 )
      Ey  (       -0.00000        2.62847        0.00000 )
      Ez  (        0.00000       -0.00000        2.76788 )
           atom      2   Ga Mean Z*:        2.67494
      Ex  (        2.62847       -0.00000       -0.00000 )
      Ey  (        0.00000        2.62847        0.00000 )
      Ez  (        0.00000        0.00000        2.76788 )
           atom      3   N  Mean Z*:       -2.67321
      Ex  (       -2.62749       -0.00000        0.00000 )
      Ey  (       -0.00000       -2.62749       -0.00000 )
      Ez  (       -0.00000        0.00000       -2.76464 )
           atom      4   N  Mean Z*:       -2.67321
      Ex  (       -2.62749        0.00000        0.00000 )
      Ey  (        0.00000       -2.62749        0.00000 )
      Ez  (       -0.00000       -0.00000       -2.76464 )
...
```

Now it is our task to parse this output.

## How to parse

We have used ASE earlier to parse output from arbitrary DFT codes. In this case, we have two output files, and ASE is not natively able to parse this into a single output.

`tdeptools` provides a tool `ase_join_pw_ph` to combine the two results: The structure, its energy and forces from `pw.out`, and the dielectric tensor as well as Born effective charges from `ph.out` are joined and written to a generic ASE output file in `JSON` format. 

In the example folder, `.../qe_dielectric_tensors/qe_pw_and_ph`, run

```bash
ase_join_pw_ph pw.out ph.out
```

This will produce a file `qe.json` which contains both DFT ground state properties (Energy, force, stress), and the dielectric properties computed via DFPT (dielectric tensor, Born effective charges).

`qe.json` is a normal ASE output file that can be parsed with `ase.io.read("qe.json", format="json")`. In turn, the TDEP parser `tdep_parse_output` will be able to parse this file:

```bash
tdep_parse_output qe.json
```

This should write six TDEP input files:

```bash
infile.positions
infile.forces
infile.meta
infile.stat
infile.born_charges
infile.dielectric_tensor
```

i.e., the standard TDEP input files for positions, forces, metadata, and statistics, as well as the dielectric input files with Born effective charges (per sample) and dielectric tensor (per sample).

The input files for longrange polar corrections, `infile.lotosplitting` can be obtained by combining `infile.dielectric_tensor` and `infile.born_charges`:

```bash
cat infile.dielectric_tensor > infile.lotosplitting && cat infile.born_charges >> infile.lotosplitting
```

## Suggested Reading

- [P. Giannozzi *et al.*, Phys Rev B **43**, 7231 (1990)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.43.7231)
- [X. Gonze and C. Lee, Phys Rev B **55**, 10355 (1997)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.55.10355)
- [S. Baroni *et al.*, Rev Mod Phys **73**, 515 (2001)](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.73.515)
