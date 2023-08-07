Symmetry refinement
===

The crystal structure symmetry detection of TDEP is very strict, input structures should therefore be as symmetric as possible, ideally down to the numerical precision of the computer.

If you have [`tdeptools` installed](#Prerequisites), you can use the script `ase_geometry_info` to print basic information about a given structure, and `ase_geometry_refine` to find high-symmetry reference structures.

## Contents

- [Geometry information](#Geometry-information)
- [Geometry refinement](#Geometry-refinement)
- [Check with TDEP](#Check-with-TDEP)
- [Prerequisites](#Prerequisites)

## Geometry information

### Information for symmetric input

`infile.ucposcar` containts the primitive unitcell Magnesium Oxide. We can inspect the file by running

```bash
ase_geometry_info infile.ucposcar
```

You should see the output

```
Read 'infile.ucposcar'
... autodetect format `vasp` for infile.ucposcar
Geometry info
  input geometry:    Atoms(symbols='OMg', pbc=True, cell=[[-0.0, 2.112879622735, 2.112879622735], [2.112879622735, -0.0, 2.112879622735], [2.112879622735, 2.112879622735, -0.0]])
  Symmetry prec.:    1e-10
  Number of atoms:   2
  Species:           Mg (1), O (1)
  Periodicity:       [ True  True  True]
  Positions:            x (Å)            y (Å)           z (Å)
        0, 'O' :        2.112880         2.112880        2.112880
        1, 'Mg':        0.000000         0.000000        0.000000
  Lattice:
    [-0.          2.11287962  2.11287962]
    [ 2.11287962 -0.          2.11287962]
    [ 2.11287962  2.11287962 -0.        ]

Cell lengths and angles:
  a, b, c (Å):      2.9881      2.9881      2.9881
  α, β, γ (°):     60.0000     60.0000     60.0000
  Volume:                 18.865 Å**3
  Volume per atom:         9.432 Å**3

Report symmetry information from spglib:
  Spacegroup:          Fm-3m (225)
  Wyckoff positions:   1*a, 1*b
  Equivalent atoms:    1*0, 1*1
```

The symmetry information is obtained from [spglib](https://spglib.readthedocs.io/en/latest/index.html), and we see that the MgO input file has the correct symmetry (Rock salt, Fm-3m, space group 225).

### Information for noisy input

Often, input files obtained from different sources (materialsproject, DFT relaxations, …) are not perfectly symmetric. As an example, we include the `infile.ucposcar.rattled` file which was obtained by rattling the atoms from `infile.ucposcar`. In turn, we find the following geometry information from

```
ase_geometry_info infile.ucposcar.rattled
```

```
Read 'infile.ucposcar.rattled'
... autodetect format `vasp` for infile.ucposcar.rattled
Geometry info
  input geometry:    Atoms(symbols='OMg', pbc=True, cell=[[-0.0, 2.112879622735, 2.112879622735], [2.112879622735, -0.0, 2.112879622735], [2.112879622735, 2.112879622735, -0.0]])
  Symmetry prec.:    1e-10
  Number of atoms:   2
  Species:           Mg (1), O (1)
  Periodicity:       [ True  True  True]
  Positions:            x (Å)            y (Å)           z (Å)
        0, 'O' :        2.117847         2.111497        2.119357
        1, 'Mg':        0.015230        -0.002342       -0.002341
  Lattice:
    [-0.          2.11287962  2.11287962]
    [ 2.11287962 -0.          2.11287962]
    [ 2.11287962  2.11287962 -0.        ]

Cell lengths and angles:
  a, b, c (Å):      2.9881      2.9881      2.9881
  α, β, γ (°):     60.0000     60.0000     60.0000
  Volume:                 18.865 Å**3
  Volume per atom:         9.432 Å**3

Report symmetry information from spglib:
  Spacegroup:          P1 (1)
```

This time, no symmetry (space group 1, P1) is detected.

### Symmetry tolerance

By decreasing the symmetry tolerance (`-t / --symprec` ), the original symmetry can be found.

**Task: Decrease the symmetry tolerance until you find spacegroup 225 again**

## Geometry refinement

To refine the symmetry of a given structure, there is the tool `ase_geometry_refine` which can be used to [find standardized, high-symmetry representations of the primitive of conventional unitcells](https://spglib.readthedocs.io/en/latest/definition.html#spglib-conventions-of-standardized-unit-cell).

**Task: See if you can manage to refine `infile.ucposcar.rattled` and obtain high-symmetry primitive and conventional unitcells. *Such high-symmetry structures should be used with TDEP at all times.***

## Check with TDEP

The [TDEP binary `crystal_structure_info`](http://ollehellman.github.io/program/crystal_structure_info.html) can be used to check which symmetry TDEP will be detecting for a given `infile.ucposcar`. It will dump output for this structure in the following way:

```
   git branch: fk_devel
 git revision: e9f23aa84778807a816bcb402c78b7329d74ba22
 Info about the crystal structure:
 ... I believe the basis is face centered cubic (FCC) with the basis vectors
 a1:      0.000000000000      2.112879622735      2.112879622735
 a2:      2.112879622735      0.000000000000      2.112879622735
 a3:      2.112879622735      2.112879622735      0.000000000000
 ... and the atoms at these positions (in fractional coordinates)
        O  0.5000000000000  0.5000000000000  0.5000000000000
       Mg  0.0000000000000  0.0000000000000  0.0000000000000
 I believe this is the conventional lattice:
 a1:      4.225759245470      0.000000000000      0.000000000000
 a2:      0.000000000000      4.225759245470      0.000000000000
 a3:      0.000000000000      0.000000000000      4.225759245470

 Available high symmetry points:
 (the ones called NP are in fact high symmetry points, but noone has bothered to name them)
       Cartesian coordinates                        Fractional coordinates
  1 GM    0.0000000000  0.0000000000  0.0000000000     0.0000000000  0.0000000000  0.0000000000
  2 L     0.1183219325  0.1183219325  0.1183219325     0.5000000000  0.5000000000  0.5000000000
  3 K     0.1774828987  0.1774828987  0.0000000000     0.3750000000  0.3750000000  0.7500000000
  4 W     0.2366438649  0.1183219325  0.0000000000     0.2500000000  0.5000000000  0.7500000000
  5 U     0.2366438649  0.0591609662  0.0591609662     0.2500000000  0.6250000000  0.6250000000
  6 X     0.2366438649  0.0000000000  0.0000000000     0.0000000000  0.5000000000  0.5000000000

 Per default, the following path will be used:
 GM -> X
 X -> U
 K -> GM
 GM -> L
 It is written in "outfile.qpoints_dispersion", modify and
 copy it to "infile.qpoints_dispersion" if you want
 All done!
```

## Prerequisites

- [TDEP tools are installed](https://github.com/flokno/tools.tdep)

