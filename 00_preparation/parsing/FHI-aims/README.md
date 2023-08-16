Parsing: FHI-aims
===

[FHI-aims](https://fhi-aims.org/) is natively supported by [ASE](https://wiki.fysik.dtu.dk/ase/ase/io/formatoptions.html#aims-output). There is example output for 2 calculations in the files `samples/sample.00001/aims.out` and `samples/sample.00002/aims.out`.

You can parse the files by running

```bash
tdep_parse_output samples/*/aims.out
```

Please not the that IO format specification via `--format` is not necessary in this case because `aims.out` is automatically detected to be FHI-aims output by [`ase.io.read`](https://wiki.fysik.dtu.dk/ase/ase/io/io.html#ase.io.read).

The output should be:

```
Parse 2 file(s)
... empty forces will be ignored: False
*** SIMULATION TEMPERATURE IS NOT GIVEN
--> set to -314.15K to remind you
... parse file   1: samples/sample.00001/aims.out
... parse file   2: samples/sample.00002/aims.out
... found 2 samples
... write forces, positions, and statistics
... forces written to infile.forces
... positions written to infile.positions
... statistics written to infile.stat
... meta info written to infile.meta
```

Inspect these input files.

Note that you can optioncally add the simulation temperature by using e.g. `--temperature 300` to specify 300K.

That's it.
