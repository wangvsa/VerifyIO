#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

DIRECTORY=$1

for file in "${DIRECTORY}"/*; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")
    output="${DIRECTORY}/${filename}.csv"

    # Run the verifyio_to_csv.python with input file and output file path
    python3 $VERIFYIO_INSTALL_PATH/verifyio_to_csv.py "$file" "$output" --group_by_api
  fi
done

python3 $VERIFYIO_INSTALL_PATH/verifyio_plot_violation_heatmap.py --files "/ipdps/results/HDF5.csv" "/ipdps/results/NetCDF.csv" "/ipdps/results/PnetCDF.csv"