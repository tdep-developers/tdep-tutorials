#!/bin/bash

set -e

# Script for stochastic sampling iterations
# Usage: ./converge_F.sh <num_iterations> <temperature>

# Check for required arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <num_iterations> <temperature>"
    echo "Example: $0 5 1300"
    exit 1
fi

# Parse arguments
NUM_ITERATIONS=$1
TEMPERATURE=$2
BASE_DIR=$(pwd)  # Use current directory as the base directory

echo "Using current directory as base: $BASE_DIR"

# Main loop
for ((iter=2; iter<=$NUM_ITERATIONS; iter++)); do
    # Determine current and next iteration numbers with leading zeros
    CURR_ITER=$(printf "iter.%03d" $iter)
    NEXT_ITER=$(printf "iter.%03d" $((iter+1)))
    
    echo "===== Starting iteration $iter of $NUM_ITERATIONS ====="
    
    # Check if current iteration directory exists
    if [ ! -d "$CURR_ITER" ]; then
        echo "Error: Directory $CURR_ITER does not exist. It should contain necessary input files."
        echo "Please create it with the required input files or adjust the script."
        exit 1
    fi
    
    # Go to the current iteration directory
    cd "$CURR_ITER" || { echo "Failed to change to directory $CURR_ITER"; exit 1; }
    echo "Now in directory: $(pwd)"
    
    # Step 2: Generate configurations
    echo "Generating configurations..."
    canonical_configuration -n 128 -t $TEMPERATURE --output_format 4
    
    # Step 3: Compute forces
    echo "Computing forces with So3krates potential..."
    sokrates_compute --folder-model ../../../module ./aims_conf* --format=aims --tdep
    
    # Step 4: Extract force constants
    echo "Extracting force constants..."
    extract_forceconstants -rc2 10.0 -U0
    
    # Step 5: Link output forceconstant as input for next iteration
    echo "Setting up force constants for next iteration..."
    ln -sf outfile.forceconstant infile.forceconstant
    
    # Step 6: Compute and plot DOS
    echo "Computing phonon dispersion and DOS..."
    phonon_dispersion_relations --dos --temperature $TEMPERATURE
    python ../../plot_dos.py
    
    # Step 7: Create convergence plots (without asking for convergence)
    if [ $iter -gt 1 ]; then
        echo "Creating convergence plots after iteration $iter..."
        python ../../plot_dos.py --basepath="../" --convergence
    fi
    
    # If not the last iteration, prepare next iteration
    if [ $iter -lt $NUM_ITERATIONS ]; then
        echo "Preparing for next iteration..."
        cd "$BASE_DIR" || { echo "Failed to return to base directory"; exit 1; }
        
        # Create next iteration directory and copy necessary files
        if [ ! -d "$NEXT_ITER" ]; then
            mkdir -p "$NEXT_ITER"
            echo "Copying input files from $CURR_ITER to $NEXT_ITER"
            cp "$CURR_ITER/infile.forceconstant" "$CURR_ITER/infile.ucposcar" "$CURR_ITER/infile.ssposcar" "$NEXT_ITER/"
        else
            echo "Warning: Directory $NEXT_ITER already exists. Skipping file copy."
        fi
    fi
    
    echo "===== Completed iteration $iter ====="
    
    # Return to base directory before starting next iteration
    cd "$BASE_DIR" || { echo "Failed to return to base directory"; exit 1; }
done

echo "===== Completed all $NUM_ITERATIONS iterations ====="
echo "To check final convergence, run:"
echo "python ../../plot_dos.py --basepath=\"./\" --convergence"

exit 0