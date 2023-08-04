from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from ase.eos import EquationOfState
from ase.build import bulk
from ase.io import read, write

# We define a root directory to know where to get data
root = Path().absolute()
# Put all the lattice parameters in a list
latt = [3.60, 3.61, 3.62, 3.63, 3.64]
# Initialize some array
vol = np.zeros(len(latt))
en = np.zeros(len(latt))
for i, a in enumerate(latt):
    # First, we read the unitcell in order to get the volume
    at = read(root / f"a{a:2.2f}/Tdep/infile.ucposcar", format="vasp")
    vol[i] = at.get_volume()  # We can use an ASE function to get the volume
    # Then we read the free_energy and U0 files
    fe = np.loadtxt(root / f"a{a:2.2f}/Tdep/outfile.free_energy")
    u0 = np.loadtxt(root / f"a{a:2.2f}/Tdep/outfile.U0")
    # We can now compute the TDEP free energy by adding the harmonic
    # free energy and the U0 correction parameter
    en[i] = fe[1] + u0[1]

# Now that we have the volumes and the free energy
# we can compute the equation of state
eos = EquationOfState(vol, en, eos="birchmurnaghan")

v = np.linspace(23.6, 24.1, 1000)
plt.show()
# Lets plot a nice figure
fig = plt.figure(figsize=(20, 10), constrained_layout=True)
ax0 = fig.add_subplot()
eos.plot("EquationOfState_1210K.pdf", ax=ax0)  # Lets plot the EOS
plt.show()


# Now, let's get the unitcell at this temperature
v0 = eos.v0  # we can get the volume from the equation of state
# The unitcell is bcc, so the lattice parameter can be computed with
# this formula
a0 = (2 * v0)**(1/3)
ucell = bulk("Zr", "bcc", a0)  # We create a new atom object using ASE function
write("infile.ucposcar", ucell, format="vasp", direct=True)  # And we write it
