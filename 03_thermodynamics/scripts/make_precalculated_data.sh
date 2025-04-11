#!/bin/bash

set -e

#Check if GNU Parallel is installed
if ! command -v parallel &> /dev/null; then
    echo "GNU Parallel is not installed. Please install it first or use the alternative method below."
    echo "On most systems, you can install it with: sudo apt-get install parallel (Debian/Ubuntu)"
    echo "or sudo yum install parallel (CentOS/RHEL)"
    exit 1
fi

# Create a temporary file with all the commands to run
TEMP_CMD_FILE=$(mktemp)

# Generate all commands
for i in $(seq 5.40 0.02 5.52); do
  folder_name="a$(printf "%.2f" $i)"
  echo "sh ./run.sh ../example_Si/$folder_name 100 200 400 600 800 1000 1200" >> "$TEMP_CMD_FILE"
done

# Define how many jobs to run in parallel
# This will use the number of available CPU cores
NUM_CORES=$(nproc)  # Get the number of CPU cores
PARALLEL_JOBS=$NUM_CORES  # One job per core

echo "Running $PARALLEL_JOBS jobs in parallel (one per CPU core)..."

# Run the commands in parallel
parallel --jobs $PARALLEL_JOBS < "$TEMP_CMD_FILE"

# Clean up
rm "$TEMP_CMD_FILE"

echo "All jobs completed!"
