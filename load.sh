#!/usr/bin/env bash

# https://docs.nersc.gov/development/languages/python/parallel-python/#smoketest-for-h5py

[[ "$NERSC_HOST" == "cori" ]] && on_cori=true || on_cori=false

module load python
module load cray-hdf5-parallel
module swap PrgEnv-"${PE_ENV,,}" PrgEnv-gnu
! $on_cori && module load fast-mkl-amd

$on_cori && env=ndlar_flow_env_cori || env=ndlar_flow_env
conda activate $env

# Not necessary on Perlmutter
$on_cori && export HDF5_USE_FILE_LOCKING=FALSE
