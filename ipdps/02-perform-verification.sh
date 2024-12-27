#!/bin/bash
#SBATCH -N 1
#SBATCH -J jobname
#SBATCH -t 01:00:00
#SBATCH -p partition
#SBATCH -o /path/to/out.out

if [ -z "$1" ]; then
    echo "Usage: $0 <base_directory>"
    exit 1
fi

BASE_DIR="$1"
PROGRAM="${VERIFYIO_INSTALL_PATH}/verifyio.py"
if [[ ! -f "$PROGRAM" ]]; then
    echo "$PROGRAM not found. Please make sure VERIFYIO_INSTALL_PATH is set properly"
    exit 1
fi


#SEMANTICS=("POSIX" "MPI-IO" "Commit" "Session")
SEMANTICS=("POSIX" "MPI-IO")

for dir in "$BASE_DIR"/*/; do
    if [ -d "$dir" ]; then
        echo "Perform verification on $dir"
        for semantic in "${SEMANTICS[@]}"; do
            python3 "$PROGRAM" "$dir" "--semantics=$semantic"
        done
	echo "==============================================="
    fi
done
