#! /usr/bin/env python3
from pathlib import Path

import xarray as xr
import numpy as np
import typer
from rich import print as echo


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def main(file: Path, file_reference: Path = "predictions_reference.nc"):
    """Get all distances for structure in FILE and write them as pandas Dataframe"""
    ds = xr.load_dataset(file)
    ds_reference = xr.load_dataset(file_reference)

    for key in ds.keys():
        y, x = ds[key].data, ds_reference[key].data
        if np.linalg.norm(x) < 1e-5:
            continue
        err = np.linalg.norm(x - y) / np.linalg.norm(x)
        echo(f"... error for {key:30} = {err}")
        assert err < 1e-5


if __name__ == "__main__":
    app()
