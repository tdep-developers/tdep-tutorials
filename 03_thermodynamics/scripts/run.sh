#!/bin/bash

set -e

# Script for stochastic sampling iterations
# Usage: ./run.sh <target-dir> <n-iter>


# Some hard-cded parameters for Silicon
# Cutoff for calculating second-order force cosntants
RC2=8.0
# Esimate for maximum frequency in THz
MAXFREQ=17.0
# Number of configurations for first iteration
INITCONFS=8
# Number of iterations of self-consistent loop to run
NUM_ITERATIONS=5


# Check for required arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <target-dir> <temp1> <temp2> ..."
    echo "Example: $0 ./a5.40 400 700"
    exit 1
fi

BASE_DIR=$1 
shift
echo "Temperatures: $@"

cd "$BASE_DIR"

# Create symbolic link to So3krates parameters since
# the run_sTDEP.sh script expects it at ../../
# this is specifically for silicon
if [ ! -e module ] && [ ! -L module ]; then
    ln -s ../module module
fi

# Generate 3x3x3 supercell
generate_structure -na 216
mv outfile.ssposcar infile.ssposcar

# Do ground state calculation
# mkdir -p "T0" && cd "T0"
# cp ../infile.ssposcar ./
# sokrates_compute --float32 --folder-model ../module/ ./infile.ssposcar --format=vasp --tdep
# cd ../

for T in "$@"; do
    echo "Temperature: $T Kelvin"

    mkdir -p "T$T" && cd "T$T"
    cp ../infile.ucposcar ../infile.ssposcar .

    # Use the run_sTDEP.sh script from 02_sampling
    bash ../../../../02_sampling/sTDEP/scripts/run_sTDEP.sh --mixing --nconfs ${INITCONFS} --niter ${NUM_ITERATIONS} --maximum_frequency ${MAXFREQ} --temperature ${T} --cutoff ${RC2}

    # Go into each iteration and calculate free-energy and U0
    for ii in $(seq 1 ${NUM_ITERATIONS}); do
        printf -v jj "%03d" $ii
        folder=iter.$jj
        cd $folder

        phonon_dispersion_relations --dos --temperature ${T}
        python ../../../../scripts/plot_dos.py --basepath=$(pwd)

        cd ../
    done

    # Make convergence plots
    python ../../../scripts/plot_dos.py --convergence --basepath=$(pwd)

    # Go back to BASEDIR
    cd ../

done