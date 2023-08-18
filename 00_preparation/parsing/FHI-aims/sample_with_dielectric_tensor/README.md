Parsing DFPT dielectric tensors from FHI-aims
===

## Prerequisites

- ASE is up to date:`master` branch is installed, e.g., via 
  ````
  pip install git+https://gitlab.com/ase/ase.git@master
  ````

- FHI-aims is newer than August 2022 (commit `4eaa4715634d5e7d234c06f4c4d0ddb35fb350e5`)

In this case you can parse the `aims.out` file in this folder with

```bash
tdep_parse_output --ignore-forces aims.out
```

Note that no forces were computed and `tdep_parse_output` will therefore raise an error if the flag `--ignore-forces` is not used.

If everything works, you should get a file a file `infile.dielectric_tensor` that contains the dielectric tensor, and the statistics files (which you can probably ignore).

