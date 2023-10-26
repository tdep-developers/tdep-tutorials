from pathlib import Path

import numpy as np
from ase.io import read


maindir = Path().absolute()
latt = [3.61, 3.62, 3.63, 3.64, 3.65]  # All lattice parameters used here
nit = 5  # Iteration for which the free energies will be computed
res = np.zeros((len(latt), 2))
# Loop on every lattice parameters
for i, a in enumerate(latt):
    wdir = maindir / f"a{a:2.2f}/iter.{nit:03d}"
    at = read(wdir / "infile.ucposcar", format="vasp")  # Load ASE atoms object
    res[i, 0] = at.get_volume()  # Compute the volume
    u0 = np.loadtxt(wdir / "outfile.U0")[1]  # Get the U0 correction term
    # Get the harmonic free energy
    fe_harm = np.loadtxt(wdir / "outfile.free_energy")[1]
    res[i, 1] = fe_harm + u0  # And sum the two

np.savetxt("eos_data.dat", res, "%25.20f")
