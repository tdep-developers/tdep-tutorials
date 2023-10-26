#! /usr/bin/env python3
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
import typer
from typing import List


def read_file(file="outfile.phonon_dos"):
    """Read outfile.phonon_dos

    Returns:
        (x, y): (frequency axis, total DOS)
    """
    data = np.loadtxt(file).T
    x = data[0]  # frequency
    y = data[1:].sum(axis=0)  # total DOS
    return x, y


def main(
    files: List[Path],
    outfile: Path = "plot_DOS_convergence.pdf",
):

    fig, ax = plt.subplots()

    for ii, file in enumerate(files):
        typer.echo(f'... read file: {file}')
        x, y = read_file(file)

        alpha = (ii + 1) / len(files)
        ax.plot(x, y + ii, color="k", alpha=alpha)
        ax.text(0, ii + 0.2, file.parent, alpha=alpha)

    ax.set_xlabel("Frequency (THz)")
    ax.set_ylabel("DOS")

    typer.echo(f"--> save plot to {outfile}")
    fig.savefig(outfile)


if __name__ == "__main__":
    typer.run(main)
