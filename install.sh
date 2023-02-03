#!/usr/bin/env bash

## https://docs.nersc.gov/development/languages/python/parallel-python/#parallel-io-with-h5py
module load python
module load cray-hdf5-parallel
module swap PrgEnv-${PE_ENV,,} PrgEnv-gnu

## https://docs.nersc.gov/development/languages/python/python-amd/
## XXX Do we still want the numpy / cython from the conda "defaults" channel?
module load fast-mkl-amd

## Don't use lazy-h5py since its h5py was built against HDF5 1.12.1 while
## cray-hdf5-parallel provides HDF5 1.12.2. May be harmless, but we're getting
## warnings that it "may cause problems".
# conda create -n module0_flow_env --clone lazy-h5py

conda create -n module0_flow_env --clone lazy-mpi4py
conda activate module0_flow_env
pip install --upgrade pip

## See comment above re fast-mkl-amd
conda install -c defaults --override-channels numpy cython

HDF5_MPI=ON CC=cc pip install -v --force-reinstall --no-cache-dir --no-binary=h5py --no-build-isolation --no-deps h5py

## See setup.py from module0_flow and h5flow for dependencies.
## Some are already installed; others aren't strictly necessary.
## The below is the bare minimum we need to add.
# pip install pyyaml-include tqdm

pip install scipy scikit-image scikit-learn pyyaml pyyaml-include tqdm

pip install git+https://github.com/peter-madigan/h5flow.git

# git clone https://github.com/peter-madigan/module0_flow.git -b module2/add-module2-yamls
# ( cd module0_flow && python setup.py install )
# export PYTHONPATH=$PWD/module0_flow:$PYTHONPATH

# pip install git+https://github.com/mjkramer/module0_flow.git@module3-nersc

git clone https://github.com/mjkramer/module0_flow.git -b module3-nersc
( cd module0_flow && pip install -e . )

pip install git+https://github.com/mjkramer/zeroworker.git

## for accessing the run log (drift field, light file):
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
