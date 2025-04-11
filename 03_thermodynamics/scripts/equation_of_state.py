import os
from pathlib import Path
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from ase.units import GPa
from ase.io import read
import argparse
import re

def get_eos_data(
        basepath : Path,
        lattice_params : list,
        temperature : float,
        iter_to_parse : int,
        n_atom_ss : int
    ):

    maindir = basepath.absolute()
    res = np.zeros((len(lattice_params), 2))
    # Loop on every lattice parameters
    for i, a in enumerate(lattice_params):
        wdir = maindir / f"a{a:2.2f}/T{temperature}/iter.{iter_to_parse:03d}"
        at = read(wdir / "infile.ucposcar", format="vasp")  # Load ASE atoms object
        res[i, 0] = at.get_volume()  # Compute the volume
        u0 = np.loadtxt(wdir / "outfile.U0")[1]  # Get the U0 correction term
        # u0_0K = np.loadtxt(maindir / f"a{a:2.2f}/T0/infile.stat")[3] / n_atom_ss
        # Get the harmonic free energy
        fe_harm = np.loadtxt(wdir / "outfile.free_energy")[1]
        res[i, 1] = fe_harm + u0  # And sum the two
        # res[i, 2] = fe_harm + u0_0K

    np.savetxt(os.path.join(basepath, f"eos_data_{temperature}K.dat"), res, "%25.20f",
                header = "Volume [Ang^3], F_TDEP [eV / atom]")

def vinet(vol, e0, v0, b0, bp):
    "Vinet equation from PRB 70, 224107"
    x = (vol / v0)**(1 / 3)
    eta = 1.5 * (bp - 1)

    e = e0 + 2 * b0 * v0 / (bp - 1)**2 * (
        2 - (5 + 3 * bp * (x - 1) - 3 * x) * np.exp(-eta * (x - 1))
        )
    return e


def fit_vinet(basepath, temperature : float):
    # Open the vol/energy data (two columns with a**3/at and eV/at)
    vol, en = np.loadtxt(os.path.join(basepath, f"eos_data_{temperature}K.dat"), unpack=True)
    

    res_file = os.path.join(basepath,f"eos_results_{temperature}K.dat")

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

    ax0.set_xlabel(r"Volume [$\mathring{A}^3$]")
    ax0.set_ylabel("Energy [eV/at]")
    ax0.legend()

    plt.savefig(os.path.join(basepath, f"vinet_{temperature}K.png"))
    plt.close()

    return v0

def parse_lattice_params(basepath : os.PathLike):

    directories = [d for d in os.listdir(basepath) if os.path.isdir(d)]
    pattern = re.compile(r'a(5\.\d+)')
    values = []

    for directory in directories:
        match = pattern.match(directory)
        if match:
            values.append(float(match.group(1)))

    print(f"Found the following lattice parameters: {values}")

    return np.sort(values)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Fit and plot Vinet equation of state for all temperatures")
    
    parser.add_argument(
        "--basepath", 
        type=str, 
        default=os.getcwd(),
        help="Path to directory containing the a5.40, a5.41 etc. folders"
    )

    args = parser.parse_args()

    lattice_parameters = parse_lattice_params(args.basepath)
    assert len(lattice_parameters) > 0
    temperatures = [100,200,400,600,800,1000,1200] # could also parse but this is easier
    n_iter = 5
    n_atoms_ss = 216

    

    # equilibrium_volumes_0K = []
    equilibrium_volumes_TDEP = []
    for T in temperatures:
        path_T = os.path.join(args.basepath, f"T{T}")
        get_eos_data(Path(args.basepath), lattice_parameters, T, n_iter, n_atoms_ss)
        v0_TDEP = fit_vinet(args.basepath, T)
        equilibrium_volumes_TDEP.append(v0_TDEP)

    # Assuming conventional cell
    # equilibrium_lattice_constants_0K = np.cbrt(4*np.array(equilibrium_volumes_0K))
    equilibrium_lattice_constants_TDEP = np.cbrt(4*np.array(equilibrium_volumes_TDEP))

    np.savetxt(os.path.join(args.basepath, "equilibrium_lattice_constants.txt"),
                np.column_stack([temperatures, equilibrium_lattice_constants_TDEP]), 
                header = "Temperature [K], a_0K [Ang] a_TDEP [Ang]")
    
    # Make a plot comparing to experiment
    a_true = np.loadtxt(os.path.join(args.basepath, "ground_truth.txt"))

    a0_exp = a_true[0,1]
    a0_TDEP = equilibrium_lattice_constants_TDEP[0]

    plt.scatter(a_true[:,0], a_true[:,1]/a0_exp, s = 100, color = "#ffbd52", label = "Experiment")
    plt.scatter(temperatures, equilibrium_lattice_constants_TDEP/a0_TDEP,
                    facecolors = 'none', edgecolors = "#52bdff", s = 100, lw = 2, label = "s-TDEP")
    plt.xlabel("Temperature [K]")
    plt.ylabel("Lattice Constant / 100K Lattice Constant")
    plt.legend(loc = "lower right")
    plt.savefig(os.path.join(args.basepath, "lattice_constant_scaled.png"))
    plt.close()

    plt.scatter(temperatures, equilibrium_lattice_constants_TDEP, s = 100, color = "#52bdff", label = "s-TDEP")
    plt.scatter(a_true[:,0], a_true[:,1], color = "#ffbd52", s = 100, label = "Experiment")
    plt.xlabel("Temperature [K]")
    plt.ylabel("Lattice Constant [Angstrom]")
    plt.legend(loc = "lower right")
    plt.savefig(os.path.join(args.basepath, "lattice_constant.png"))
