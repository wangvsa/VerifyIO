#!/usr/bin/bash

DATASET_DIR=./dataset
mkdir ${DATASET_DIR}
cd ${DATASET_DIR}
wget https://zenodo.org/records/14553174/files/hdf5-1.14.4-3-recorder-traces.tar.gz 
wget https://zenodo.org/records/14553174/files/netcdf-4.9.2-recorder-traces.tar.gz
wget https://zenodo.org/records/14553174/files/pnetcdf-1.13.0-recorder-traces.tar.gz
tar -zxvf hdf5-1.14.4-3-recorder-traces.tar.gz
tar -zxvf netcdf-4.9.2-recorder-traces.tar.gz
tar -zxvf pnetcdf-1.13.0-recorder-traces.tar.gz
rm -rf *.tar.gz
cd ../
