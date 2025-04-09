#! /usr/bin/env python3
from pathlib import Path

import typer
import numpy as np
from ase.io import read
from ase.calculators.lj import LennardJones
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md import MDLogger
from ase.units import fs


def main(supercell: Path,
         temperature: float,
         nsteps: int = 5000,
         dt: float = 1.0,
         friction: float = 0.01,
         format: str = None,
         seed: int = None):
    # First we read the supercell
    at = read(supercell, format=format)

    # We define the random number generator
    rng = np.random.default_rng(seed)

    # If the structure doesn't have temperature, we set it
    if at.get_temperature() < 1e-4:
        MaxwellBoltzmannDistribution(at, temperature_K=temperature, rng=rng)

    # We define the Lennard Jones potential for Argon
    calc = LennardJones(sigma=3.4,
                        epsilon=0.010325,
                        ro=7.5,
                        rc=8.5,
                        smooth=True)
    at.calc = calc

    # Now we setup the MD simulation
    md = Langevin(at, dt * fs, temperature_K=temperature, rng=rng,
                  friction=friction / fs, trajectory="trajectory.traj")
    # We attach a log
    md.attach(MDLogger(md, at, '-'), 100)
    # And we run
    md.run(nsteps)


if __name__ == "__main__":
    typer.run(main)
