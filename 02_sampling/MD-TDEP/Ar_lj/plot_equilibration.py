#! /usr/bin/env python3
from pathlib import Path
from typing import List

import typer
import numpy as np
from ase.io import read
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def main(trajectories: List[Path],
         temperature: float = None,
         format: str = None,
         dt: float = 1.0):
    # We start by reading the trajectories
    traj = []
    for p in trajectories:
        traj.extend(read(p, index=":", format=format))
    nsteps = len(traj)

    # Get the potential energy and temperatures
    steps = np.arange(0, nsteps) * dt
    potenergy = np.array([at.get_potential_energy() for at in traj])
    temperatures = np.array([at.get_temperature() for at in traj])

    # Prepare the figure and plot
    fig = plt.figure(figsize=(15, 10), constrained_layout=True)
    gd = GridSpec(2, 1, fig)
    ax0 = fig.add_subplot(gd[0])
    ax1 = fig.add_subplot(gd[1])

    ax0.plot(steps, potenergy)
    ax1.plot(steps, temperatures)
    if temperature is not None:
        ax1.axhline(temperature, ls="--", c="k")

    ax0.set_xlabel("Time [fs]")
    ax1.set_xlabel("Time [fs]")
    ax0.set_ylabel("Potential energy [eV]")
    ax1.set_ylabel("Temperature [K]")

    plt.show()


if __name__ == "__main__":
    typer.run(main)
