#!/bin/bash
#SBATCH -N 1
#SBATCH -J jobname
#SBATCH -t 01:00:00
#SBATCH -p partition
#SBATCH -o /path/to/out.out

if [ -z "$1" ]; then
    echo "Usage: $0 <library_trace_directory>"
    exit 1
fi

BASE_DIR="$1"
PROGRAM="${VERIFYIO_INSTALL_PATH}/verifyio.py"
if [[ ! -f "$PROGRAM" ]]; then
    echo "$PROGRAM not found. Please make sure VERIFYIO_INSTALL_PATH is set properly"
    exit 1
fi

SEMANTICS=("POSIX" "MPI-IO" "Commit" "Session")

# Write all verifyio.py output to a single temporary text file first
LIB_TRACE_DIR=$(basename ${BASE_DIR})
ARR=(${LIB_TRACE_DIR//-/ })
LIB_NAME=${ARR[1]}
TEXT_RESULT_FILE=/tmp/${LIB_NAME}.txt
rm -f ${TEXT_RESULT_FILE}


for dir in "$BASE_DIR"/*/; do
    if [ -d "$dir" ]; then
        echo "Perform verification on $dir"
        for semantic in "${SEMANTICS[@]}"; do
            python3 $PROGRAM $dir --semantics=$semantic | tee -a $TEXT_RESULT_FILE
        done
        echo "==============================================="
    fi
done

# Conver the text output of all tests to a single CSV file
mkdir -p ./result
CSV_RESULT_FILE=./result/${LIB_NAME}.csv
python3 $VERIFYIO_INSTALL_PATH/verifyio_to_csv.py $file $output --group_by_api

