#! /usr/bin/env python3
from pathlib import Path
from typing import List

import typer
import numpy as np
from ase.io import read
from ase.units import GPa


def main(trajectories: List[Path],
         temperature: float = None,
         nthrow: int = 0,
         format: str = None,
         dt: float = 1.0):
    # We start by reading the trajectories and put them in one big list
    traj = []
    for p in trajectories:
        traj.extend(read(p, index=f"{nthrow}:", format=format))

    # We will need the number of steps and atoms
    nsteps = len(traj)
    nat = len(traj[0])

    # Get the positions, reshape and write
    xred = np.array([at.get_scaled_positions() for at in traj])
    xred = xred.reshape(-1, 3)
    np.savetxt("infile.positions", xred, fmt="%25.12f")

    # Get the forces, reshape and write
    forces = np.array([at.get_forces() for at in traj])
    forces = forces.reshape(-1, 3)
    np.savetxt("infile.forces", forces, fmt="%25.12f")

    # Now we prepare the stat file
    stat = np.zeros((nsteps, 13))
    # First the configuration
    stat[:, 0] = np.arange(1, nsteps+1)
    # Then the time (in fs)
    stat[:, 1] = np.arange(0, nsteps) * dt
    # The total energy
    stat[:, 2] = np.array([at.get_total_energy() for at in traj])
    # The potential energy
    stat[:, 3] = np.array([at.get_potential_energy() for at in traj])
    # The kinetic energy
    stat[:, 4] = np.array([at.get_kinetic_energy() for at in traj])
    # The temperature
    stat[:, 5] = np.array([at.get_temperature() for at in traj])
    # We get the elastic properties - it's in GPa
    stress = np.array([at.get_stress() for at in traj]) / GPa
    pressure = -stress[:, :3].mean(axis=1)
    # The pression (in GPa)
    stat[:, 6] = pressure
    # The stress tensor (in GPa and Voigt notation)
    stat[:, 7:] = stress

    # Set a nice format and write
    fmtstat = "%7d " + 12 * " %15.10f"
    np.savetxt("infile.stat", stat, fmt=fmtstat)

    # Check if we have a temperature and estimate it from the traj if not
    if temperature is None:
        temperature = np.array([at.get_temperature() for at in traj]).mean()

    # And we finish by the meta file
    with open("infile.meta", "w") as fd:
        fd.write(f"{nat:6d}  # Number of atoms\n")
        fd.write(f"{nsteps:6d}  # Number of steps\n")
        fd.write(f"{dt:6.2f}  # Timestep in fs\n")
        fd.write(f"{temperature:6.2f}  # Temperature in K")


if __name__ == "__main__":
    typer.run(main)
