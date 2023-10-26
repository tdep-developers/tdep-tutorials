import os

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from ase.units import GPa


def vinet(vol, e0, v0, b0, bp):
    "Vinet equation from PRB 70, 224107"
    x = (vol / v0)**(1 / 3)
    eta = 1.5 * (bp - 1)

    e = e0 + 2 * b0 * v0 / (bp - 1)**2 * (
        2 - (5 + 3 * bp * (x - 1) - 3 * x) * np.exp(-eta * (x - 1))
        )
    return e


def fit_vinet():
    res_file = "eos_results.dat"
    # Open the vol/energy data (two columns with a**3/at and eV/at)
    vol, en = np.loadtxt("eos_data.dat", unpack=True)

    # Non-linear fitting, we need to have some bounds
    bounds = ([-1, 0, 0, -10], [1, 100, 5, 10])
    popt, _ = curve_fit(vinet, vol, en - en.min(), bounds=bounds)

    # Get the values
    e0, v0, b0, bp = popt
    e0 += en.min()
    b0 /= GPa

    # A little printing
    print("Result of the fit :")
    print(f"Ground state energy :     {e0:6.5f} [eV/at]")
    print(f"Equilibrium volume :      {v0:6.5f} [angs^3]")
    print(f"Bulk modulus :            {b0:6.5f} [GPa]")
    print(f"Everything is printed in file : {res_file}")

    # A little saving
    header = "Energy [eV/at] - V0 [angs^3] - B0 [GPa] - B0' [GPa/K]"
    res = np.c_[e0, v0, b0, bp]
    np.savetxt(res_file, res, header=header)

    # And everything to plot the results
    xvol = np.linspace(vol.min(), vol.max(), 1000)
    yen = vinet(xvol, *popt)
    
    fig = plt.figure(figsize=(10, 5), constrained_layout=True)
    ax0 = fig.add_subplot()

    ax0.plot(xvol, yen + en.min(), zorder=0, lw=2.5, label="fit")
    ax0.plot(vol, en, ls="", marker="o", zorder=1,
             markersize=10, label="data")
    ax0.plot([v0], [e0], ls="", marker="o", zorder=1,
             markersize=10, label=r"V$_0$")

    ax0.set_xlabel(r"Volume [$\mathring{a}$]")
    ax0.set_ylabel("Energy [eV/at]")
    ax0.legend()

    plt.show()

if __name__ == "__main__":
    fit_vinet()
