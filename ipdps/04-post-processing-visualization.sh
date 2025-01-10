#!/bin/bash

python3 $VERIFYIO_INSTALL_PATH/verifyio_plot_violation_heatmap.py --files "/ipdps/results/HDF5.csv" "/ipdps/results/NetCDF.csv" "/ipdps/results/PnetCDF.csv"
