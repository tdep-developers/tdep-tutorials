import matplotlib.pyplot as plt
import argparse
import numpy as np
import glob
import os

def parse_U0(basepath : os.PathLike = os.getcwd()):
    data = np.loadtxt(os.path.join(basepath, "outfile.U0"))
    return data[0,1]

def parse_F0(basepath : os.PathLike = os.getcwd()):
    data = np.loadtxt(os.path.join(basepath, "outfile.free_energy"))
    return data[1]

def plot_convergence(
        basepath: os.PathLike = os.getcwd(), 
        outpath: os.PathLike = os.getcwd(),
        pattern: str = "iter.*"
    ):

    # Find all iteration directories
    iter_dirs = sorted(glob.glob(os.path.join(basepath, pattern)))
    
    if not iter_dirs:
        print(f"No iteration directories matching '{pattern}' found in {basepath}")
        return
    
    # Create plot
    plt.figure(figsize=(10, 6))
    
    # Color map that changes with iteration number
    cmap = plt.cm.viridis
    y_offset = 0.0
    
    for i, iter_dir in enumerate(iter_dirs):
        dos_file = os.path.join(iter_dir, "outfile.phonon_dos")
        
        if not os.path.exists(dos_file):
            print(f"Warning: {dos_file} not found, skipping")
            continue

        y_offset += i*0.25 # hard coded for tutorial, change for your material
            
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

    args = parser.parse_args()

    

if __name__ == "__main__":
    main()
