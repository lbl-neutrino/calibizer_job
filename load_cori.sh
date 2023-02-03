#!/usr/bin/env bash

# https://docs.nersc.gov/development/languages/python/parallel-python/#smoketest-for-h5py

module load python
module load cray-hdf5-parallel

conda activate module0_flow_env_cori
export PYTHONPATH=$PWD/module0_flow:$PYTHONPATH

# https://docs.nersc.gov/development/libraries/hdf5/#known-issues-on-cori
export HDF5_USE_FILE_LOCKING=FALSE
