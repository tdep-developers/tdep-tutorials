import os

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from ase.units import GPa


def vinet(vol, e0, v0, b0, bp):
    x = (vol / v0)**(1 / 3)
    eta = 1.5 * (bp - 1)

    e = e0 + 2 * b0 * v0 / (bp - 1)**2 * (
        2 - (5 + 3 * bp * (x - 1) - 3 * x) * np.exp(-eta * (x - 1))
        )
    return e


def fit_vinet():
    res_file = "eos_results.dat"
    vol, en = np.loadtxt("eos_data.dat", unpack=True)

    bounds = ([-1, 0, -10, 0], [1, 5, 10, 100])
    bounds = ([-1, 0, 0, -10], [1, 100, 5, 10])
    popt, _ = curve_fit(vinet, vol, en - en.min(), bounds=bounds)

    e0, v0, b0, bp = popt
    e0 += en.min()
    b0 /= GPa
    bp /= GPa

    print("Result of the fit :")
    print(f"Ground state energy :     {e0:6.5f} [eV/at]")
    print(f"Equilibrium volume :      {v0:6.5f} [angs^3]")
    print(f"Bulk modulus :            {b0:6.5f} [GPa]")
    print(f"Bulk modulus derivative : {bp:6.5f} [GPa / K]")
    print(f"Everything is printed in file : {res_file}")

    header = "Energy [eV/at] - V0 [angs^3] - B0 [GPa] - B0' [GPa/K]"
    np.savetxt(res_file, [e0, v0, b0, bp])

    xvol = np.linspace(vol.min(), vol.max(), 1000)
    yen = vinet(xvol, *popt)
    
    fig = plt.figure(figsize=(10, 5), constrained_layout=True)
    ax0 = fig.add_subplot()

    ax0.plot(xvol, yen + en.min(), zorder=0, lw=2.5)
    ax0.plot(vol, en, ls="", marker="o", zorder=1,
             markersize=10)

    ax0.set_xlabel(r"Volume [$\mathring{a}$]")
    ax0.set_ylabel("Energy [eV/at]")

    plt.show()

if __name__ == "__main__":
    fit_vinet()
