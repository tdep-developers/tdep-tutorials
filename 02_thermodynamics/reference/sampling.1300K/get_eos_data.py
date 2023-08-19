from pathlib import Path

import numpy as np
from ase.io import read


maindir = Path().absolute()
latt = [3.61, 3.62, 3.63, 3.64, 3.65]
nit = 12
res = np.zeros((len(latt), 2))
for i, a in enumerate(latt):
    wdir = maindir / f"a{a:2.2f}/iter.{nit:03d}"
    at = read(wdir / "infile.ucposcar", format="vasp")
    res[i, 0] = at.get_volume()
    u0 = np.loadtxt(wdir / "outfile.U0")[1]
    fe_harm = np.loadtxt(wdir / "outfile.free_energy")[1]
    res[i, 1] = fe_harm + u0

np.savetxt("eos_data.dat", res, "%25.20f")
