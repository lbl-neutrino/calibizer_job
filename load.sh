#!/usr/bin/env bash

# https://docs.nersc.gov/development/languages/python/parallel-python/#smoketest-for-h5py

module load python
module load cray-hdf5-parallel
module swap PrgEnv-${PE_ENV,,} PrgEnv-gnu
module load fast-mkl-amd

conda activate ndlar_flow_env

# Not necessary on Perlmutter
# export HDF5_USE_FILE_LOCKING=FALSE
