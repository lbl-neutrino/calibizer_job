#!/usr/bin/env bash

# https://docs.nersc.gov/development/languages/python/parallel-python/#pre-built-h5py-conda-environment
module load python
module load cray-hdf5-parallel
conda create -n module0_flow_env --clone lazy-h5py
conda activate module0_flow_env
pip install --upgrade pip

# See setup.py from module0_flow and h5flow for dependencies.
# Some are already installed; others aren't strictly necessary.
# The below is the bare minimum we need to add.
# pip install pyyaml-include tqdm

pip install scipy scikit-image scikit-learn pyyaml pyyaml-include tqdm

pip install git+https://github.com/peter-madigan/h5flow.git

# git clone https://github.com/peter-madigan/module0_flow.git -b module2/add-module2-yamls
# ( cd module0_flow && python setup.py install )
# export PYTHONPATH=$PWD/module0_flow:$PYTHONPATH

# pip install git+https://github.com/mjkramer/module0_flow.git@module3-nersc

git clone https://github.com/mjkramer/module0_flow.git -b module3-nersc
( cd module0_flow && pip install . )

pip install git+https://github.com/mjkramer/zeroworker.git

# for accessing the run log (drift field, light file):
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
