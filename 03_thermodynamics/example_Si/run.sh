#!/bin/bash

set -e

# Script for stochastic sampling iterations
# Usage: ./run.sh <target-dir> <n-iter>


# Some hard-cded parameters for Silicon
# Temperatures to run self-consistent loop for
TEMPERATURES=(400 700 1000 1400)
# Cutoff for calculating second-order force cosntants
RC2=4.0
# Esimate for maximum frequency in THz
MAXFREQ=18
# Number of configurations for first iteration
INITCONFS=8


# Check for required arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <target-dir>"
    echo "Example: $0 ./a5.40"
    exit 1
fi

BASE_DIR=$1  # Use current directory as the base directory
NUM_ITERATIONS=$2


for T in "${TEMPERATURES[@]}"; do
    echo "Processing: $T"

    # Generate 3x3x3 supercell
    generate_structure -na 216
    mv outfile.ssposcar infile.ssposcar

    mkdir -p "$T" && cd "$T"

    # Create symbolic link to So3krates parameters as the run_sTDEP.sh
    # scripts expects them at ../../
    ln -s ../module module

    # Use the run_sTDEP.sh script from 02_sampling
    bash ../../../02_sampling/sTDEP/scripts/run_sTDEP.sh --temperature ${T} --niter ${NUM_ITERATIONS} --maximum_freuqency ${MAXFREQ} --cutoff ${RC2} --nconfs ${INITCONFS}

    # Go into each iteration and calculate free-energy and U0
    for i in $(seq 1 $NUM_ITERATIONS); do
        folder=iter.$i
        pushd $folder

        phonon_dispersion_relations --dos --temperature ${T}
        python ../../../../scripts/plot_dos.py 

        popd
    done

    # Make convergence plots
    python ../../../scripts/plot_dos.py --convergence 

done