import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import glob
from typing import Callable


def parse_U0(basepath : os.PathLike = os.getcwd()):
    data = np.loadtxt(os.path.join(basepath, "outfile.U0"))
    return data[1]

def parse_F0(basepath : os.PathLike = os.getcwd()):
    data = np.loadtxt(os.path.join(basepath, "outfile.free_energy"))
    return data[1]

def plot_y_conv(
        y : np.ndarray,
        y_label : str,
        var_name : str,
        outpath : os.PathLike = os.getcwd()
    ):

    plt.scatter(np.arange(1, len(y) + 1), y);
    plt.xlabel("Iteration");
    plt.xticks(np.arange(1, len(y) + 1))
    plt.ylabel(y_label);
    plt.tight_layout()
    plt.savefig(os.path.join(outpath, "convergence_of_" + var_name.replace(" ", "_") + ".png"));
    plt.close();

def plot_dos(
        basepath : os.PathLike = os.getcwd(),
        outpath : os.PathLike = os.getcwd()
    ):

    dos_data = np.loadtxt(os.path.join(basepath, "outfile.phonon_dos"))
    plt.plot(dos_data[:,0], dos_data[:,1], lw = 2.5, color = "#21deb2");
    plt.xlabel("Frequency [THz]");
    plt.ylabel("DOS [1/THz]");
    plt.tight_layout()
    plt.savefig(os.path.join(outpath, "DOS.png"));
    plt.close();

    print(f"DOS plot saved to {os.path.join(outpath, 'DOS.png')}")

def get_iter_dirs(basepath : os.PathLike = os.getcwd(), pattern : str = "iter.*"):
    iter_dirs = sorted(glob.glob(os.path.join(basepath, pattern)))
    
    if not iter_dirs:
        print(f"No iteration directories matching '{pattern}' found in {basepath}")
        return

    return iter_dirs

def plot_convergence(
        parse_function : Callable[[os.PathLike], float],
        var_name : str, 
        basepath: os.PathLike = os.getcwd(), 
        outpath: os.PathLike = os.getcwd(),
    ):

    iter_dirs = get_iter_dirs(basepath)
    
    plt.figure(figsize=(10, 6))
    
    y_data = []
    for iter_dir in iter_dirs:
        dos_file = os.path.join(iter_dir, "outfile.phonon_dos")
        
        # Skipp iter.000 if its there
        if not os.path.exists(dos_file):
            print(f"Warning: {dos_file} not found, skipping")
            continue
            
        y_data.append(parse_function(iter_dir))


    plot_y_conv(y_data, f"{var_name} [eV / atom]", var_name, outpath)


def plot_dos_convergence(
        basepath: os.PathLike = os.getcwd(), 
        outpath: os.PathLike = os.getcwd(),
    ):

    iter_dirs = get_iter_dirs(basepath)
    
    plt.figure(figsize=(10, 6))
    cmap = plt.cm.viridis
    
    for i, iter_dir in enumerate(iter_dirs):
        dos_file = os.path.join(iter_dir, "outfile.phonon_dos")
        
        if not os.path.exists(dos_file):
            print(f"Warning: {dos_file} not found, skipping")
            continue

        y_offset = i*0.25 # hard coded for tutorial, change for your material
            
        dos_data = np.loadtxt(dos_file)
        color = cmap(i / len(iter_dirs))
        alpha = 0.3 + 0.7 * (i / len(iter_dirs))
        label = os.path.basename(iter_dir)
        plt.plot(dos_data[:,0], dos_data[:,1] + y_offset, lw=2, 
                    color=color, alpha=alpha, label=label)
            
    plt.xlabel("Frequency [THz]")
    plt.ylabel("DOS [1/THz]")
    plt.title("Phonon DOS Convergence Across Iterations")
    plt.legend(loc='best')
    plt.grid(alpha=0.3)
    
    # Save the convergence plot
    plt.tight_layout()
    plt.savefig(os.path.join(outpath, "DOS_convergence.png"), dpi=300)
    plt.close()
    
    print(f"Convergence plot saved to {os.path.join(outpath, 'DOS_convergence.png')}")

def main():
    parser = argparse.ArgumentParser(description="Plot phonon density of states from outfile.phonon_dos")
    
    parser.add_argument(
        "--basepath", 
        type=str, 
        default=os.getcwd(),
        help="Path to the directory containing outfile.phonon_dos (default: current directory)"
    )
    
    parser.add_argument(
        "--outpath", 
        type=str, 
        default=os.getcwd(),
        help="Path to save the output DOS.png file (default: current directory)"
    )

    parser.add_argument(
        "--convergence",
        action = "store_true",
        help = "Compare DOS across multiple iterations",
        default = False
    )

    args = parser.parse_args()
    
    if args.convergence:
        plot_dos_convergence(basepath=args.basepath, outpath=args.outpath)
        plot_convergence(parse_U0, "U0", args.basepath, args.outpath)
        plot_convergence(parse_F0, "Harmonic Free Energy", args.basepath, args.outpath)
    else:
        plot_dos(basepath=args.basepath, outpath=args.outpath)

if __name__ == "__main__":
    main()

