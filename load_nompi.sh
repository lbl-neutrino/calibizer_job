#!/usr/bin/env bash

[[ "$NERSC_HOST" == "cori" ]] && on_cori=true || on_cori=false

module load python

# ! $on_cori && module load fast-mkl-amd

env=ndlar_flow_env_nompi
conda activate $env

# Not necessary on Perlmutter
$on_cori && export HDF5_USE_FILE_LOCKING=FALSE
