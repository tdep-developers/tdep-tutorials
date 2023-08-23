# Parsing VASP output files for TDEP

This tutorial covers how to produce TDEP input files from VASP ouput data. It requires the `tdeptools` package ( https://github.com/flokno/tools.tdep )

**We need the most recent version of [ASE](https://gitlab.com/ase/ase) in order to be able to parse dielectric tensors**. Please make sure you have that installed, e.g., by running

```bash
pip install git+https://gitlab.com/ase/ase.git@master
```

To parse data into the TDEP format from a vasprun.xml file simply do

`tdep_parse_output vasprun.xml`

This will provide infile.forces, infile.meta, infile.positions and  infile.stat files. For (eg.) an MD run at 300 K you may also add the option `--temperature 300` to get the correct temperature in infile.meta.

In addition, from a VASP run with (eg.) `LEPSILON=.TRUE.`, the dielectric tensor and Born effective charges will be printed to files infile.dielectric tensor and infile.born_charges. This should be combined for further use:  

`cat infile.dielectric_tensor infile.born_charges > infile.lotosplitting`

Alternatively, from an VASP run with `LEPSILON=.TRUE.`, a file `outfile.lotosplitting` can be obtained by running the command:

`tdep_read_lotosplitting_from_outcar OUTCAR`

This file should then be copied or symlinked for further use: `ln -s outfile.lotosplitting infile.lotosplitting`
