# Parsing VASP output files for TDEP

This tutorial covers how to produce TDEP input files from VASP ouput data. It requires the `tdeptools` package ( https://github.com/flokno/tools.tdep )

## Molecular Dynamics run

Given a `vasprun.xml` file produced from a VASP MD run, you may simply run:

`tdep_parse_output vasprun.xml`

This will produce the following set of infiles: infile.forces, infile.meta, infile.positions, infile.stat.

## LO-TO splitting

To include the effect of long-range electrostatics in TDEP, an `infile.lotosplitting` containing the Dielectric tensor and Born effective charges is required.

From an VASP run with `LEPSILON=.TRUE.`, a file `outfile.lotosplitting` can be obtained by running the command:

`tdep_read_lotosplitting_from_outcar OUTCAR`

This file should then be copied or symlinked for further use: `ln -s outfile.lotosplitting infile.lotosplitting`
