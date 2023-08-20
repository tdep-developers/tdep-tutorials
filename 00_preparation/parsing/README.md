Parsing
===

Here you find instructions on how to parse forces and displacements from different force engines to generate the [input files for TDEP](http://ollehellman.github.io/page/files.html).

The most convenient way is to use the script `tdep_parse_output` from [`tdeptools`](https://github.com/flokno/tools.tdep), which uses the [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/index.html) and supports all codes supported by ASE – see a complete list [here](https://wiki.fysik.dtu.dk/ase/ase/io/io.html#ase.io.read).

The basic command is

```bash
tdep_parse_output /path/to/your/files/file1 /path/to/your/files/file2 ... --format FORMAT --temperature TEMPERATURE
```

Where `--format` specifies the [IO format](https://wiki.fysik.dtu.dk/ase/ase/io/io.html#ase.io.read) to be used, and `--temperature` is used to specify the simulation temperature. This is important for free energy calculations.

## Tutorials

- [FHI-aims](./FHI-aims/)
- [Quantum Espresso](./QuantumEspresso/)

## Prerequisites

- [TDEP tools are installed](https://github.com/flokno/tools.tdep)
