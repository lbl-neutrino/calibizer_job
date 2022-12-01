#!/usr/bin/env python3

# https://docs.nersc.gov/development/languages/python/parallel-python/#smoketest-for-h5py
# salloc -q interactive -C cpu -N 2 --ntasks-per-node 2 -t 5
# srun mpi_smoketest.py

from mpi4py import MPI
import h5py

rank = MPI.COMM_WORLD.rank

with h5py.File('test.h5', 'w', driver='mpio', comm=MPI.COMM_WORLD) as f:
    dset = f.create_dataset('test', (4,), dtype='i')
    dset[rank] = rank
