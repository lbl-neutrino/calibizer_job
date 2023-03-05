#!/usr/bin/env bash

[[ "$NERSC_HOST" == "cori" ]] && on_cori=true || on_cori=false

## https://docs.nersc.gov/development/languages/python/parallel-python/#parallel-io-with-h5py
module load python
module load cray-hdf5-parallel
module swap PrgEnv-"${PE_ENV,,}" PrgEnv-gnu

## https://docs.nersc.gov/development/languages/python/python-amd/
## XXX Do we still want the numpy / cython from the conda "defaults" channel?
if ! $on_cori; then
    module load fast-mkl-amd
fi

## Don't use lazy-h5py since its h5py was built against HDF5 1.12.1 while
## cray-hdf5-parallel provides HDF5 1.12.2. May be harmless, but we're getting
## warnings that it "may cause problems".
# conda create -n module0_flow_env --clone lazy-h5py

$on_cori && env=ndlar_flow_env_cori || env=ndlar_flow_env

conda create -n $env --clone lazy-mpi4py
conda activate $env
pip install --upgrade pip setuptools wheel

## See comment above re fast-mkl-amd
conda install -c defaults --override-channels numpy cython

HDF5_MPI=ON CC=cc pip install -v --force-reinstall --no-cache-dir --no-binary=h5py --no-build-isolation --no-deps h5py

## See setup.py from module0_flow and h5flow for dependencies.
## Some are already installed; others aren't strictly necessary.
## The below is the bare minimum we need to add.
# pip install pyyaml-include tqdm

pip install scipy scikit-image scikit-learn pyyaml pyyaml-include tqdm pytest

# pip install git+https://github.com/larpix/h5flow.git
[[ ! -d h5flow ]] && git clone https://github.com/larpix/h5flow.git
pushd h5flow || exit
pip install -e .
popd || exit


pip install adc64format

# git clone https://github.com/peter-madigan/module0_flow.git -b module2/add-module2-yamls
# ( cd module0_flow && python setup.py install )
# export PYTHONPATH=$PWD/module0_flow:$PYTHONPATH

# pip install git+https://github.com/mjkramer/module0_flow.git@module3-nersc

# git clone https://github.com/mjkramer/module0_flow.git -b module3-nersc
# ( cd module0_flow && pip install -e . )
[[ ! -d ndlar_flow ]] && git clone https://github.com/larpix/ndlar_flow.git # -b develop
# develop branch
pushd ndlar_flow || exit
git checkout 0aaa40eea9a0de0d2e9191c12ee4c89e520b1340 # develop branch
pip install -e .
popd || exit

pip install git+https://github.com/mjkramer/zeroworker.git

## for accessing the run log (drift field, light file):
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

## used for reading runlist.txt
pip install pandas
